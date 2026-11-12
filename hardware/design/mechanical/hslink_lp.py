"""HSLink-LP 结构 C 参数化设计。uv/CadQuery 2.8；不是实测装配合格证明。"""
from pathlib import Path
import argparse
import json
import math
import hashlib
import cadquery as cq

HERE = Path(__file__).resolve().parent
P = json.loads((HERE / 'parameters.json').read_text())


def block(x, y, z, cx=0, cy=0, bottom=0, radius=0):
    q = cq.Workplane('XY').box(x, y, z, centered=(True, True, False))
    if radius:
        q = q.edges('|Z').fillet(radius)
    return q.translate((cx, cy, bottom))


def cylinder(d, h, x, y, z):
    return cq.Workplane('XY').circle(d / 2).extrude(h).translate((x, y, z))


def cut_window(part, rectangle, height):
    x1, y1, x2, y2 = rectangle
    tool = block(x2-x1, y2-y1, height+2, (x1+x2)/2, -(y1+y2)/2,
                 -1, P['notch_radius'])
    return part.cut(tool)


def build(pcb_step=None, reports=None, export_parts=True, probe_map=None):
    cx, cy = P['pcb_width']/2, -P['pcb_depth']/2
    base = block(P['base_width'], P['base_depth'], P['floor_thickness'], cx, cy,
                 radius=P['base_radius'])
    rim = block(P['base_width'], P['base_depth'], P['rim_height'], cx, cy,
                radius=P['base_radius']).cut(
                    block(P['pcb_width']+2*P['pcb_edge_clearance'],
                          P['pcb_depth']+2*P['pcb_edge_clearance'],
                          P['rim_height']+2, cx, cy, -1))
    for x1,y1,x2,y2 in P['rim_openings']:
        rim = rim.cut(block(x2-x1,y2-y1,P['rim_height']+2,
                            (x1+x2)/2,-(y1+y2)/2,-1))
    base = base.union(rim)
    # Broad U relief: flat insertion corridor and tangent-continuous shoulders.
    ux=P['usb_relief_center_x']; uw=P['usb_relief_width']; rh=P['rim_height']
    flat=P['usb_relief_flat_width']; shoulder=(uw-flat)/2
    assert shoulder>0 and rh-P['usb_relief_depth']>P['floor_thickness']
    relief=(cq.Workplane('XZ').moveTo(ux-uw/2,rh)
            .bezier([(ux-uw/2+shoulder/2,rh),(ux-flat/2-shoulder/2,rh-P['usb_relief_depth']),(ux-flat/2,rh-P['usb_relief_depth'])],includeCurrent=True)
            .lineTo(ux+flat/2,rh-P['usb_relief_depth'])
            .bezier([(ux+flat/2+shoulder/2,rh-P['usb_relief_depth']),(ux+uw/2-shoulder/2,rh),(ux+uw/2,rh)],includeCurrent=True)
            .lineTo(ux+uw/2,rh+4).lineTo(ux-uw/2,rh+4).close().extrude(8,both=True))
    base=base.cut(relief)
    for x, y in P['holes']:
        base = base.union(cylinder(P['pillar_diameter'], P['pcb_bottom_z'], x, -y, 0))
        base = base.cut(cylinder(P['insert_pilot_diameter'], P['insert_pilot_depth']+1,
                                x, -y, P['pcb_bottom_z']-P['insert_pilot_depth']))
        base = base.cut(cylinder(P['foot_diameter'], P['foot_recess']+1, x, -y, -1))
    for x in [29, 35, 41, 47, 53, 80, 86, 92]:
        base = base.cut(block(2.5, 18, 5, x, -28, -1, 1.24))
    lid = block(P['base_width'], P['base_depth'], P['lid_thickness'], cx, cy,
                radius=P['base_radius'])
    for key in ['front_notch', 'external_input_notch']:
        lid = cut_window(lid, P[key], P['lid_thickness'])
    sx,sy = P['source_switch_center']
    lid = lid.cut(cylinder(P['source_switch_hole_diameter'],
                          P['lid_thickness']+2,sx,-sy,-1))
    for x, y in P['holes']:
        lid = lid.cut(cylinder(P['lid_hole_diameter'], P['lid_thickness']+2, x, -y, -1))
    pcb_top = P['pcb_bottom_z'] + P['pcb_thickness']
    lid_z = pcb_top + P['standoff_length']
    assembly = cq.Assembly(name='HSLink_LP_structure_C')
    assembly.add(base, name='Base_warm_ivory_PETG_prototype', color=cq.Color(.86,.81,.71))
    assembly.add(lid, name='Lid_PC_2mm_prototype', loc=cq.Location((0,0,lid_z)),
                 color=cq.Color(.94,.96,.97,.22))
    fastener_shapes=[]
    for i,(x,y) in enumerate(P['holes'],1):
        # Functional envelopes only: no helical threads/knurl. Fit requires a coupon.
        insert = cylinder(P['insert_nominal_outer_diameter'], P['insert_length'],
                          x,-y,P['pcb_bottom_z']-P['insert_length']).cut(cylinder(3,6,x,-y,4))
        stand = (cq.Workplane('XY').polygon(6,P['standoff_hex_af']/math.cos(math.pi/6))
                 .extrude(P['standoff_length']).translate((x,-y,pcb_top)))
        stand = stand.cut(cylinder(2.5,6,x,-y,lid_z-6))
        stand = stand.union(cylinder(3,P['standoff_male_thread_length'],x,-y,
                                    pcb_top-P['standoff_male_thread_length']))
        washer = cylinder(7,P['washer_thickness'],x,-y,lid_z+P['lid_thickness']).cut(
            cylinder(3.2,1,x,-y,lid_z+P['lid_thickness']))
        screw = cylinder(3,P['top_screw_length'],x,-y,
                         lid_z+P['lid_thickness']+P['washer_thickness']-P['top_screw_length'])
        screw = screw.union(cylinder(5.5,3,x,-y,lid_z+P['lid_thickness']+P['washer_thickness']))
        foot = cylinder(P['foot_diameter'],P['foot_thickness'],x,-y,
                        P['foot_recess']-P['foot_thickness'])
        for name,shape,color in [('Insert',insert,(.68,.51,.22)),('Standoff',stand,(.70,.57,.30)),
                                 ('Washer',washer,(.78,.80,.82)),('Screw',screw,(.78,.80,.82)),
                                 ('Foot',foot,(.08,.09,.1))]:
            assembly.add(shape,name=f'{name}_{i}',color=cq.Color(*color))
            if name in ['Standoff','Washer','Screw']:
                fastener_shapes.append((f'{name}_{i}',shape.val()))
    result={'status':'geometry_checked_not_physical_fit_tested','dimensions_mm':P,
            'lid_bottom_z':lid_z,'pcb_top_z':pcb_top,
            'base_valid':base.val().isValid(),'lid_valid':lid.val().isValid(),
            'base_solids':len(base.val().Solids()),'lid_solids':len(lid.val().Solids()),
            'base_volume_mm3':base.val().Volume(),'lid_volume_mm3':lid.val().Volume(),
            'checks':[],'limits':['尺寸模型含简化器件外形，不能覆盖厂商全公差或配套插头实际尺寸',
                                  '透明盖建议PC 2mm；底座建议PETG打印，尚无材料报价或实物样件',
                                  '热熔螺母孔需按实际螺母和打印机做试片，不含螺纹/滚花几何',
                                  '未验证温升、跌落、拔插力、绝缘污染及140nA漏电']}
    assert result['base_valid'] and result['lid_valid']
    assert result['base_solids']==1 and result['lid_solids']==1
    # Assumed straight plug-overmould sweep, not a vendor-qualified cable model.
    plug=block(14,25.5,8,ux,12.25,8.5).val()
    result['usb_plug_envelope']={'status':'假设包络检查，未指定实际线缆',
        'width_mm':14,'height_mm':8,'z_center_mm':12.5,
        'y_sweep_mm':[-.5,25],'base_collision_mm3':plug.intersect(base.val()).Volume(),
        'lid_collision_mm3':plug.intersect(lid.val().translate((0,0,lid_z))).Volume(),
        'limits':'仅直线插入与结构件；不覆盖弯头、加厚护套、倾斜及实际连接器配合'}
    assert result['usb_plug_envelope']['base_collision_mm3']<1e-5, result['usb_plug_envelope']
    assert result['usb_plug_envelope']['lid_collision_mm3']<1e-5
    if export_parts:
        for name,shape in [('hslink_lp_base',base),('hslink_lp_lid',lid)]:
            cq.exporters.export(shape,str(HERE/(name+'.step')))
            cq.exporters.export(shape,str(HERE/(name+'.stl')),tolerance=.03,angularTolerance=.1)
        cq.exporters.exportDXF(lid.faces('<Z').wires(),str(HERE/'hslink_lp_lid.dxf'))
    if pcb_step:
        raw=cq.importers.importStep(str(pcb_step)).val()
        board=max((s for s in raw.Solids() if s.BoundingBox().xlen>100 and s.BoundingBox().ylen>70),
                  key=lambda s:s.Volume())
        bb=board.BoundingBox()
        dz=P['pcb_bottom_z']-bb.zmin
        pcb=raw.translate((0,0,dz))
        # KiCad STEP repeats component product names; CadQuery's assembly importer
        # rejects duplicate names. Keep exact solids with unique display identifiers.
        for i,solid in enumerate(raw.Solids()):
            bb_s=solid.BoundingBox()
            if bb_s.xlen>100 and bb_s.ylen>70:
                color=cq.Color(.13,.44,.29)
            elif bb_s.zlen<.65:
                color=cq.Color(.65,.68,.70)
            elif 9.9<bb_s.xlen<10.4 and 10.4<bb_s.ylen<11 and bb_s.zlen>15:
                color=cq.Color(.23,.55,.12)
            elif bb_s.zlen>23 and 9<bb_s.xlen<9.4:
                color=cq.Color(.65,.67,.69)
            else:
                color=cq.Color(.25,.28,.31)
            assembly.add(solid, name=f'PCB_solid_{i:04d}',
                         loc=cq.Location((0,0,dz)), color=color)
        result['pcb_step_sha256']=hashlib.sha256(Path(pcb_step).read_bytes()).hexdigest()
        result['pcb_step_translation_z']=dz
        result['exported_board_body_top_z']=bb.zmax+dz
        result['board_body_note']='STEP板体不包含全部铜/阻焊厚度；机械安装仍按名义1.6mm板厚，需实物公差检查'
        for name,shape in [('base',base.val()),('lid',lid.val().translate((0,0,lid_z)))]+fastener_shapes:
            collisions=[]
            for i,s in enumerate(pcb.Solids()):
                a,b=s.BoundingBox(),shape.BoundingBox()
                if a.xmax<b.xmin or a.xmin>b.xmax or a.ymax<b.ymin or a.ymin>b.ymax or a.zmax<b.zmin or a.zmin>b.zmax:continue
                volume=s.intersect(shape).Volume()
                if volume>1e-5:collisions.append({'solid_index':i,'volume_mm3':volume})
            result['checks'].append({'test':'pcb_components_vs_'+name,'collisions':collisions})
    if pcb_step and probe_map:
        result['probe_access']={'assumption':'直径2mm竖直接近包络；未指定实际探头，不代表实物可达性验收','lid_removal_required':True,'points':[]}
        for point in json.loads(Path(probe_map).read_text()):
            x,y=point['position_mm']
            probe=cylinder(2,35,x,-y,pcb_top+.05).val()
            collisions=[]
            for i,solid in enumerate(pcb.Solids()):
                a,bbp=solid.BoundingBox(),probe.BoundingBox()
                if a.xmax<bbp.xmin or a.xmin>bbp.xmax or a.ymax<bbp.ymin or a.ymin>bbp.ymax or a.zmax<bbp.zmin:continue
                volume=solid.intersect(probe).Volume()
                if volume>1e-5:collisions.append({'solid_index':i,'volume_mm3':volume})
            result['probe_access']['points'].append({'ref':point['ref'],'xy_mm':[x,y],'component_collisions':collisions,'lid_intersection_mm3':lid.val().translate((0,0,lid_z)).intersect(probe).Volume()})
    if reports:
        reports.mkdir(parents=True,exist_ok=True)
        assembly.export(str(reports/'HSLink-LP-assembly.step'))
        assembly.export(str(reports/'HSLink-LP-assembly.glb'))
        (reports/'mechanical-checks.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps(result,ensure_ascii=False,indent=2))
    return base,lid,assembly

if __name__=='__main__':
    parser=argparse.ArgumentParser()
    parser.add_argument('--pcb-step',type=Path)
    parser.add_argument('--reports',type=Path,default=HERE.parent/'reports/pcb-structure-2026-11-12')
    parser.add_argument('--assembly-only',action='store_true',help='只更新装配与检查，不重写未变的结构单件')
    parser.add_argument('--probe-map',type=Path,help='KiCad导出的测试点位置JSON；仅检查假定接近包络')
    args=parser.parse_args()
    build(args.pcb_step,args.reports,not args.assembly_only,args.probe_map)
