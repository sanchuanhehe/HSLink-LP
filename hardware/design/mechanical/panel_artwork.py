"""面板矢量标识及装配薄层；不改PCB，不增加实体按钮或指示灯。"""
from pathlib import Path
import cadquery as cq

HERE=Path(__file__).resolve().parent
TEXT=[('HSLP',30,12,5.2),('DEBUG INSTRUMENT',33,19,1.8),
      ('INT',96,5.6,1.8),('EXT',96,18.3,1.8),('SOURCE',96,24,2),
      ('EXT IN',73.5,17.5,1.65),
      ('DEBUG',28,59,2.5),('ARM20 / JTAG / SWD',28,62.5,1.3),
      ('A',56,59,2.8),('UART A',56,62.5,1.4),
      ('B',76,59,2.8),('UART B',76,62.5,1.4),
      ('POWER',93,59,2.4),('DUT OUT',93,62.5,1.4)]

def add_artwork(assembly,lid,z):
    window=(cq.Workplane('XY').box(102,60,1,centered=(True,True,False))
            .edges('|Z').fillet(10).translate((63,-58,-.3)))
    s=(cq.Workplane('XY').box(140,110,.02,centered=(True,True,False))
       .translate((55,-40,0)).intersect(lid).cut(window))
    # STEP importers may discard a compound-level color; color each solid.
    for j, solid in enumerate(s.translate((0,0,z)).solids().vals()):
        assembly.add(solid,name=f'Print_C_ivory_mask_{j}',color=cq.Color(.941,.910,.855))
    for i,(t,x,y,size) in enumerate(TEXT):
        s=cq.Workplane('XY').text(t,size,.02,font='Arial',halign='center',valign='center').translate((x,-y,z+.025))
        for j, solid in enumerate(s.solids().vals()):
            assembly.add(solid,name=f'Print_text_{i}_{j}',color=cq.Color(1,1,1) if y>50 else cq.Color(.12,.16,.16))
    accent=cq.Workplane('XY').polyline([(57,-21),(57.45,-21),(60.45,-10),(60,-10)]).close().extrude(.02).translate((0,0,z+.025))
    assembly.add(accent,name='Print_vermilion_slash',color=cq.Color(.94,.22,.06))

def export_svg():
    a=['<svg xmlns="http://www.w3.org/2000/svg" width="118mm" height="88mm" viewBox="-4 -4 118 88">',
       '<title>HSLink-LP panel print / 1:1 mm / top side</title>']
    outline='M1 -4 H63.5 A2 2 0 0 1 65.5 -2 V11 A2 2 0 0 0 67.5 13 H79.5 A2 2 0 0 0 81.5 11 V-2 A2 2 0 0 1 83.5 -4 H109 A5 5 0 0 1 114 1 V79 A5 5 0 0 1 109 84 H103 A2 2 0 0 1 101 82 V67 A2 2 0 0 0 99 65 H10 A2 2 0 0 0 8 67 V82 A2 2 0 0 1 6 84 H1 A5 5 0 0 1 -4 79 V1 A5 5 0 0 1 1 -4 Z'
    holes=' '.join(f'M{x-1.7} {y} a1.7 1.7 0 1 0 3.4 0 a1.7 1.7 0 1 0 -3.4 0 Z' for x,y in [(4,4),(106,4),(4,76),(106,76)])
    holes+=' M92.75 12 a3.25 3.25 0 1 0 6.5 0 a3.25 3.25 0 1 0 -6.5 0 Z'
    a.append(f'<defs><clipPath id="lid"><path d="{outline} {holes}" clip-rule="evenodd"/></clipPath></defs><g clip-path="url(#lid)">')
    a.append('<path fill="#f0e8da" fill-rule="evenodd" d="M-4 -4 H114 V84 H-4 Z M22 28 H104 Q114 28 114 38 V78 Q114 88 104 88 H22 Q12 88 12 78 V38 Q12 28 22 28 Z"/>')
    a.append('<path fill="#ef380f" d="M57 21 L57.45 21 L60.45 10 L60 10 Z"/>')
    for t,x,y,size in TEXT:
        color='#ffffff' if y>50 else '#1f2929'
        a.append(f'<text x="{x}" y="{y}" font-family="Arial,sans-serif" font-size="{size}" text-anchor="middle" dominant-baseline="central" fill="{color}">{t}</text>')
    a.append('</g></svg>')
    (HERE/'hslink_lp_panel_print.svg').write_text('\n'.join(a)+'\n')
