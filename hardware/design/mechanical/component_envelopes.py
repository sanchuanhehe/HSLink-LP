"""用于装配审查的尺寸模型；不是厂家 STEP、模具图或电气模型。"""
from pathlib import Path
import cadquery as cq

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'libraries' / 'models'


def block(x, y, z, cx=0, cy=0, bottom=0):
    return cq.Workplane('XY').box(x,y,z,centered=(True,True,False)).translate((cx,cy,bottom))


def build():
    OUT.mkdir(parents=True,exist_ok=True)
    parts={}
    # Hongfa HFD2 single-stable drawing p4: 20.2 x 10.2 x 10.6; leads 3 mm.
    r=block(20.2,10.2,10.6)
    for x,y in [(-8.89,3.81),(-1.27,3.81),(3.81,3.81),(8.89,3.81),
                (8.89,-3.81),(3.81,-3.81),(-1.27,-3.81),(-8.89,-3.81)]:
        r=r.union(block(.5,.25,3,x,y,-3))
    parts['HFD2_envelope']=r
    # KF128: two positions, 5.08 pitch, 10.7 depth, 14 high, 4.3 mm tails.
    r=block(10.16,10.7,14,2.54)
    for x in (0,5.08):
        r=r.cut(cq.Workplane('XY').center(x,0).circle(1.8).extrude(3).translate((0,0,11.2)))
        r=r.cut(block(3.2,3.5,4,x,-4.5,2.5))
        r=r.union(block(.9,.8,4.3,x,0,-4.3))
    parts['KF128_2P_envelope']=r
    # Dailywell DWG 2MDP0428 Rev A; plain bushing, no functional thread model.
    r=block(9.14,8.13,8.64)
    r=r.union(cq.Workplane('XY').circle(2.5).extrude(5.59).translate((0,0,8.64)))
    r=r.union(cq.Workplane('XY').circle(1.27).extrude(9.4).translate((0,0,14.23)))
    for x in (-2.54,2.54):
        for y in (-2.54,0,2.54):r=r.union(block(.76,.51,3.3,x,y,-3.3))
    parts['Dailywell_2MD_envelope']=r
    # Small packages only need conservative body-clearance envelopes here.
    parts['SPH4018_envelope']=block(4.2,4.2,2.0)
    parts['WUSB3801_envelope']=block(1.7,1.7,1.0)
    parts['TPS63810_YFF_envelope']=block(1.344,2.255,1.0)
    for name,part in parts.items():
        assert part.val().isValid(),name
        cq.exporters.export(part,str(OUT/(name+'.step')))
    return parts

if __name__=='__main__':
    print('Saved dimension envelopes:', ', '.join(build()))
