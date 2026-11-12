# 结构 C 工程样件

## 本轮围边与面板标识

2026-11-13：按用户指图删除盖板左侧原service_button_notch大U形开槽，恢复连续板面。覆盖区域服务操作需拆盖；未改PCB、原理图和USB底座避让口。装配检查仍基于既有PCB STEP快照，不能替代主线程最新布局复核。

USB过渡曲线最终采用三次Bezier精确相切构造。早期余弦采样插值出现微小越界并导致布尔切削未清除预期区域，已替换；最终假设插头包络与底座、盖板相交体积均为0。请打开重新导出的STEP，不沿用旧截图。

下围边恢复连续，仅USB保留总宽22mm、深4mm的圆滑U形下凹，中间14mm平底、左右各4mm三次Bezier相切过渡；肩部与底部斜率连续，底面Z=6mm，底板厚3mm保持。其他接口模型未与围边干涉。以宽14mm、高8mm、中心Z=12.5mm、Y=-0.5～25mm的假设插头护套直线扫掠检查底座与盖板；这是工程包络，不是已选线缆的尺寸保证，不覆盖弯头、加厚护套、斜插或实际配合。下文先前“接口处避让”的描述由本段取代，上盖开口保持原样。

PCB STEP经普通实体导入后原颜色未保留；本轮绿色端子、银灰开关为尺寸分类示意配色，其他器件仍有简化显示。六类自建模型不是厂家精细模型。旧原生检查快照无模型项仅含安装孔、定位点及TP1，新增裸铜测试点也不需要实体。尚不能据此证明主线程最新PCB的全部模型覆盖。

开放底座＋可拆盖板。此目录是唯一当前结构设计，版本使用Git；没有实物装配或生产放行。

- `parameters.json`：板框/孔位/高度/开口的毫米参数。
- `hslink_lp.py`：CadQuery参数化底座、盖板及装配。Python依赖通过用户已安装的uv工程运行。
- `component_envelopes.py`：六种缺少厂家STEP的器件外形模型源；输出到项目`libraries/models`。模型按已查尺寸图建立，但不覆盖完整公差、端子内部结构或所有活动位置。
- `hslink_lp_base.step/.stl`、`hslink_lp_lid.step/.stl/.dxf`：当前参数的导出件。STEP/STL可用FreeCAD打开；盖板DXF保持1:1毫米。文件随源参数一起更新，不作为独立版本副本。

底座118×88mm，底板3mm、围边高10mm；PCB底面距底座底面9mm。PCB110×80mm，四个M3孔与PCB坐标一致。12mm螺柱支承2mm盖板；盖板下表面22.6mm、顶面24.6mm，与简化电源端子顶面名义齐平。围边单边距板边0.8mm，不承托焊点；围边仅USB处保留圆滑避让。尺寸仍需公差和样品验证。

装配建议件见`../../bom/mechanical.csv`：M3×12黄铜公母柱、公端6mm、4个M3×6上盖螺钉、垫圈、热熔螺母、脚垫。均尚未选定可采购的完整型号或核价。热熔螺母外径4.6/长度4mm和预孔4.1mm仅为试片起点，不能直接承诺热熔/打印配合。

本轮外观：暖米白PETG底座、近无色透明PC盖板、黄铜柱、银色金属螺钉和垫圈、黑色脚垫。颜色是显示属性，不构成材料采购认证；透明板保留既有PC建议，未自动改为PMMA亚克力。拨杆开口改为中心(96,12)mm、直径6.5mm圆孔，围绕模型直径5mm轴套留0.75mm径向间隙，不夹持PCB开关。模型轴套顶面比盖板顶面高约0.23mm；现有模型仅含直立拨杆，全行程、倾斜装配及样品公差必须复核。

降低盖板后装配导出与干涉报告见`../reports/structure-compact-2026-11-12`。本轮使用既有布局快照`layout-ux-2026-11-12/pcb.step`，没有修改PCB或原理图。主线程仍在布线，最新布局若变化需重新导出PCB并检查；既有旧装配报告不能代表本轮结构。

## 重新生成

先使用KiCad MCP导出当前PCB STEP（原点0,0mm、替换模型启用），放入忽略的`../reports/pcb-structure-2026-11-12/pcb.step`。在工程根目录运行：

```bash
uv run --project /Users/sanchuanhehe/.local/share/cadquery --locked --offline python \
  hardware/design/mechanical/hslink_lp.py \
  --pcb-step hardware/design/reports/pcb-structure-2026-11-12/pcb.step
```

用户工具路径可按本机CadQuery安装目录修改。无PCB参数时仅生成结构单件；包含PCB时还输出忽略的装配STEP/GLB及几何检查JSON。渲染颜色用于辨识，不表示实际材料或PCB已布完。

## 检查边界

底座和盖板各为一个有效实体；导入PCB器件与底座/盖板/四组螺柱、垫圈、螺钉未发现超过1e-5mm³的体积干涉。板体STEP厚度不完全包含铜/阻焊，安装高度仍按名义1.6mm，必须计入板厚和模型公差。没有用无干涉结果替代实物插拔和装配验证。

ARM20排线资料未给出准确插头外包络；当前开口不是经实测确认的插头模型。还需检查排线出线/弯曲、端子螺丝刀可达、拨杆全行程、USB插头、打印收缩、螺柱/螺母采购公差、透明盖挠曲、通风与温升。6个简化外形不是厂家原始STEP。整夹具140nA漏电仍需包括线束、PCB污染和结构材料进行实测。

## 接口重排与测试点检查（2026-11-12）

当前前沿顺序为ARM20、UART A、UART B、DUT电源。板框、安装孔及结构开口未改变，继续使用本目录唯一单件STEP/STL/DXF；按新PCB重新导出的装配位于忽略目录`../reports/layout-ux-2026-11-12`，未发现当前简化器件与底座/盖板/紧固件体积干涉。

TP2～TP11均需要拆下透明盖板后使用。按直径2mm、竖直向上35mm的探针包络检查，未与PCB器件模型相交；这个假设不能代替实际探头外形/公差/手持角度和试针行程检查。盖板不为这些点增加孔；保持可拆即可进行首板调试和外部校准。

只更新装配而不重写未变单件，可增加`--assembly-only`。使用KiCad原生位置JSON（列表，每项含`ref`和`position_mm:[x,y]`）可增加`--probe-map PATH`进行上述包络检查，例：

```bash
uv run --project /Users/sanchuanhehe/.local/share/cadquery --locked --offline python \
  hardware/design/mechanical/hslink_lp.py --assembly-only \
  --pcb-step hardware/design/reports/layout-ux-2026-11-12/pcb.step \
  --probe-map hardware/design/reports/layout-ux-2026-11-12/testpoint-connectivity.json \
  --reports hardware/design/reports/layout-ux-2026-11-12
```
