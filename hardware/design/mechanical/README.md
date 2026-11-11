# 结构 C 工程样件

开放底座＋可拆盖板。此目录是唯一当前结构设计，版本使用Git；没有实物装配或生产放行。

- `parameters.json`：板框/孔位/高度/开口的毫米参数。
- `hslink_lp.py`：CadQuery参数化底座、盖板及装配。Python依赖通过用户已安装的uv工程运行。
- `component_envelopes.py`：六种缺少厂家STEP的器件外形模型源；输出到项目`libraries/models`。模型按已查尺寸图建立，但不覆盖完整公差、端子内部结构或所有活动位置。
- `hslink_lp_base.step/.stl`、`hslink_lp_lid.step/.stl/.dxf`：当前参数的导出件。STEP/STL可用FreeCAD打开；盖板DXF保持1:1毫米。文件随源参数一起更新，不作为独立版本副本。

底座118×88mm，底板3mm、低边框6mm；PCB底面距底座底面9mm。PCB110×80mm，四个M3孔与PCB坐标一致。16mm螺柱支承2mm盖板；盖板下表面名义高度26.6mm。接口/服务按钮/拨杆留避让口，前沿开放便于接线。尺寸、PETG底座与PC盖板均为工程建议，用户只确认了结构C形态。

装配建议件见`../../bom/mechanical.csv`：M3×16公母柱、公端6mm、4个M3×6上盖螺钉、垫圈、热熔螺母、脚垫。均尚未选定可采购的完整型号或核价。热熔螺母外径4.6/长度4mm和预孔4.1mm仅为试片起点，不能直接承诺热熔/打印配合。

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
