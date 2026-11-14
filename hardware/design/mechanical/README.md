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

- PCB110×80×名义1.6mm，四孔(4,4)/(106,4)/(4,76)/(106,76)mm；底座已为嘉立创镶嵌服务适配为124×94mm，外角R5；盖板仍118×88mm。
- 底板3mm、围边高10mm，PCB下表面Z9mm；围边单边离板0.8mm，不承托焊点。仅USB处有22mm宽、4mm深的圆滑U形避让，中间14mm平底与两侧三次Bezier相切过渡。
- 12mm螺柱支承2mm盖，盖板下表面Z22.6mm、上表面24.6mm。前沿开口X8～101、Y65向外开放；外部电源开口X65.5～81.5、向内至Y13mm，八处开口转角R2。切割边仍需去毛刺。
- 来源拨杆圆孔中心(96,12)mm、直径6.5mm，围绕模型5mm轴套留0.75mm径向间隙，盖板不夹持开关。当前只建直立拨杆，完整动作/倾斜及样品公差未验证。
- 所有新增TP2～TP11拆盖后探测，不增加盖板探针孔。D2mm竖直探针包络仅用于布局筛查。

基于厂家图纸和现有引脚推导，拨杆朝后为INT、朝前为EXT；印刷放行前须样品导通确认。没有新增实体MEASURE键/状态灯；参考效果图的这些功能不作为已确认电路。

装配显示采用米白底座、透明2mm盖板、黄铜柱、银色螺钉及黑色脚垫；本次底座采购建议FDM ABS白色，透明PC/亚克力各一片，均定制印刷。紧固件建议尺寸见`../../bom/mechanical.csv`，尚无完整供应商型号及价格。现按嘉立创M3*4*3采用3.6mm预孔、深5mm；四处14.2mm方平台。实际镶嵌、保持力与打印公差待工厂/样件确认。

面板SVG与装配0.02mm薄层表达印刷，不能当作加工凸字。白色/米白需印厂确认白墨工艺，本次SVG的14组文字已转曲，并生成118×88mm的1:1矢量PDF；1:1纸样对位、色差和实际开关方向仍需确认。SVG裁切边界不替代DXF切割轮廓。

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


## 排线范围更新（2026-11-14）

用户已明确排线可以不考虑，本轮不继续排线资料调查、也不以排线插合/弯曲验证作为交付门槛；前述排线不确定性作为未验证历史事实保留，不写成通过。底座/盖板和装配CAD、当前静态尺寸模型干涉检查已完成；材料/紧固件最终选型、拨杆全行程及样件公差/实物试装仍未完成，不与CAD文件完成混为一谈。


## 首板下单补充

用户接受PCB首板OSP和±20%阻抗管控；不改变铜层/叠层。PC和亚克力2mm各1片，均印刷。底座下单推荐FDM/ABS白色，属于渠道适配建议，未替代用户材料确认；原PETG不是已核实在嘉立创可选。具体填写项、印刷镜像/透明白墨和旧制造包ENIG说明覆盖见`docs/manufacturing.md`的首板下单节。底座/盖板CAD几何未改，不重复静态干涉检查。


## 2026-11-15 嘉立创嵌件适配（覆盖先前通用嵌件假设）

当前采用工厂目录M3*4*3（内M3、外径4、长3mm）×4。预孔3.6mm、深5mm，预孔至平台侧壁名义最小3.1mm、孔底至脚垫槽3.5mm；四处14.2×14.2mm工具平面，顶面Z9mm。旧4.1mm预孔/4.6×4mm通用嵌件不适配此目录，不可用旧STL直接下镶嵌服务。

扩大平台原会碰来源开关，改为向外移2.2mm并将底座扩至124×94×10mm；围边在平台处降至支承面，保留完整工具平面。PCB110×80mm、四孔坐标、板底Z9mm、盖板118×88×2mm及装配高度保持。`lid_width/lid_depth/lid_radius`独立于底座，已用双向实体差确认现有盖板几何未变，DXF未改。

对当前PCB STEP与十个探针模型重做静态干涉检查通过，14.2mm平面材料完整；更新STL闭合/非流形及STEP体积比较通过。名义螺纹啮合3mm，公端尖端至盲孔底0.6mm；不宣称FDM公差、保持力、扭矩和实物装配已经通过。最新装配、示意图和检查在`../reports/insert-fit-2026-11-15`；旧机械审阅ZIP不代表本次更新底座。

面板加工包增加带118×88mm外框尺寸、红色切割线、黄色透明区和无背胶标注的正面1:1工艺图；全部文字转曲，工艺图颜色/边框不印，实际印刷仍用PRINT稿，切割用CUT-DXF。底座和盖板本次改动均为工程实施，未将具体尺寸方案伪写为用户逐项确认。
