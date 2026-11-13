# 结构 C 当前设计

2026-11-14。开放底座＋可拆透明盖，前沿ARM20→UART A→UART B→DUT电源。形态C已确认；以下具体尺寸、材料与颜色为工程方案，未实物装配或生产放行。版本历史使用Git，当前仅本目录一份设计。

## 源与交付

|文件|用途|
|---|---|
|`parameters.json`|毫米参数、孔位与开口|
|`hslink_lp.py`|CadQuery底座、盖板、装配及几何检查|
|`component_envelopes.py`|十类有资料出处的简化器件外形；不是厂家精细STEP|
|`panel_artwork.py`|统一的面板SVG及装配印刷示意|
|`hslink_lp_base.step/.stl`|底座单件|
|`hslink_lp_lid.step/.stl/.dxf`|2mm盖板；DXF单位毫米、1:1|
|`hslink_lp_panel_print.svg`|118×88mm正面印刷稿；透明区域不印|

当前PCB、装配STEP/GLB、PNG及检查记录在忽略的`../reports/manufacturing-review-2026-11-14`，包名`HSLink-LP-mechanical-review.zip`。可用FreeCAD打开其中`mechanical/HSLink-LP-assembly.step`；旧reports中的FCStd只属历史快照。精确源与输出哈希见`hardware/validation.json`。

## 尺寸及使用

- PCB110×80×名义1.6mm，四孔(4,4)/(106,4)/(4,76)/(106,76)mm；底座118×88mm，外角R5。
- 底板3mm、围边高10mm，PCB下表面Z9mm；围边单边离板0.8mm，不承托焊点。仅USB处有22mm宽、4mm深的圆滑U形避让，中间14mm平底与两侧三次Bezier相切过渡。
- 12mm螺柱支承2mm盖，盖板下表面Z22.6mm、上表面24.6mm。前沿开口X8～101、Y65向外开放；外部电源开口X65.5～81.5、向内至Y13mm，八处开口转角R2。切割边仍需去毛刺。
- 来源拨杆圆孔中心(96,12)mm、直径6.5mm，围绕模型5mm轴套留0.75mm径向间隙，盖板不夹持开关。当前只建直立拨杆，完整动作/倾斜及样品公差未验证。
- 所有新增TP2～TP11拆盖后探测，不增加盖板探针孔。D2mm竖直探针包络仅用于布局筛查。

基于厂家图纸和现有引脚推导，拨杆朝后为INT、朝前为EXT；印刷放行前须样品导通确认。没有新增实体MEASURE键/状态灯；参考效果图的这些功能不作为已确认电路。

当前显示为暖米白PETG底座、透明PC2mm盖板、黄铜柱、银色螺钉及黑色脚垫；均为工程外观/材料建议。紧固件建议尺寸见`../../bom/mechanical.csv`，尚无完整供应商型号及价格。热熔预孔4.1mm是试片起点，需按实际螺母和打印机确定。

面板SVG与装配0.02mm薄层表达印刷，不能当作加工凸字。白色/米白需印厂确认白墨工艺，生产前字体转曲、1:1纸样对位和色差确认。SVG裁切边界不替代DXF切割轮廓。

## 再生成

从PCB原生辅助原点(88,61)mm导出，不能使用绝对原点(0,0)mm。在工程根目录运行：

```sh
kicad-cli pcb export step --force --subst-models --no-optimize-step --user-origin 88x61mm -o hardware/design/reports/manufacturing-review-2026-11-14/pcb.step hardware/design/HSLink-LP.kicad_pcb
uv run --project /Users/sanchuanhehe/.local/share/cadquery --locked --offline python hardware/design/mechanical/hslink_lp.py --assembly-only --pcb-step hardware/design/reports/manufacturing-review-2026-11-14/pcb.step --probe-map hardware/design/reports/final-control-routing-2026-11-13/probe-map.json --reports hardware/design/reports/manufacturing-review-2026-11-14/mechanical
```

`--assembly-only`保留未变的单件STEP/STL/DXF；需要重生成单件时去掉它。探针位置必须来自当前PCB原生导出；变更布局时不可盲用旧map。Python统一uv，CadQuery运行环境在用户工具目录。

检查器现在拒绝偏离板局部原点的STEP、缺少安装孔及器件/探针碰撞。3.19mm净空柱用于确认孔位，不代替3.2mm孔径公差；无PCB输入时只报告结构单件检查，不能宣称已检查装配。源码和参数哈希随报告记录。故意平移STEP、缺孔板体及把探针放入K601的反例均被拒绝。

## 已完成检查及边界

当前原生PCB中211封装、759焊盘对象保持；本轮仅三处放置属性变化，全部几何不变。当前STEP的110×80mm边界与四安装孔通过新增检查。底座/盖板各一个有效实体，器件与底座、盖板及螺柱/垫圈/螺丝没有超过1e-5mm³的体积干涉；10个探针包络无器件干涉，使用时需拆盖。

既有单件STEP体积与当前CadQuery源一致，STL闭合、无边界/非流形边，体积误差<0.1%、边界差<0.04mm（网格逼近，非加工精度）；盖板DXF读回为毫米及四孔/拨杆孔正确。已查看当前装配俯视/透视和制造数据铜层。

ARM20的34×12mm、UART的13×4mm插头包络以及D4mm竖直螺丝刀杆对结构件无干涉，**均为工程试探包络**。CBL801图纸只给针距/线长，缺少插头外形及最小弯曲半径，不能称所选排线匹配通过；USB护套14×8mm同样未指定真实线缆。实际插拔/手指/刀柄、拨杆全行程、板厚/模型/打印/紧固件公差、盖板挠曲、材料采购、温升和140nA污染漏电仍待验证。

十类包络的尺寸与资料线索在`component_envelopes.py`，PDF来源哈希保留在`hardware/validation.json`的模型记录中；装配假设、工艺导出和未关闭项见[制造审阅说明](../../../docs/manufacturing.md)。资料/几何检查不代替实物验证。
