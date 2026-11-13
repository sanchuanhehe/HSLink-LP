# 制造数据与装配审阅

2026-11-14，当前为首板审阅数据，尚无生产放行。唯一工程仍是`hardware/design`，源版本以Git及`hardware/validation.json`哈希为准；生成文件在忽略的`hardware/design/reports/manufacturing-review-2026-11-14`。本轮不改电路、走线、接口或材料选型，不刷新11月7日价格/库存快照。

## 实际修复

U501自建BGA封装原为未指定放置类型，KiCad的仅SMD坐标导出会漏掉它；已将板上及库中类型改为SMD。SW601/K601的板上和库中类型一并明确为THT。放置属性通过标准MCP工具修改；旧服务没有库属性编辑工具，库文件经一次性MCP适配器调用KiCad原生对象模型保存。库焊盘UUID、编号、坐标、尺寸、图形与模型未变；字段UUID/模型块格式由KiCad规范化。适配器用完删除，标准服务未修改。

USB-C J101是SMT信号脚加四个通孔屏蔽固定脚，不能用`--exclude-fp-th`生成最终SMT坐标。最终保留`--smd-only --exclude-dnp`，与采购BOM逐位号核对为185个SMT、8个THT，共193采购器件。11个裸铜测试点、安装孔和定位点不进入采购贴装表；J101屏蔽脚焊接方式仍需装配方确认。

对`8b3c89b`的PCB差异只有三处`attr`：U501→smd，SW601/K601→through_hole。759个焊盘对象的网络/几何、全部走线/过孔、位置、接口、3D关联及其他PCB内容保持；`.pro/.dru`哈希不变。完整DRC重新加载/重铺铜后0一般违规、0未连接、0原理图parity，无新增忽略项。采购BOM增量¥0/板、¥0/10套；制造和结构未重新核价。

## 文件

|路径（相对此次reports目录）|用途与范围|
|---|---|
|`HSLink-LP-fabrication-review.zip`|11个Gerber、独立PTH/NPTH钻孔、Gerber Job及工艺说明；审阅包|
|`assembly/jlc-smt-bom.csv`|185个SMT位号，带完整MPN、封装和嘉立创编号；沿用既有选型|
|`assembly/jlc-smt-cpl.csv`|185行，T面、mm、原生位置/角度；需工厂预览复核旋转与吸取偏移|
|`assembly/kicad-smd-positions.csv`|KiCad原生坐标，作为格式转换来源|
|`assembly/through-hole-assembly.csv`|8个通孔采购器件的独立装配表|
|`HSLink-LP-ipc356.d356`|裸板电测数据，1524条记录，非硬件测试结果|
|`HSLink-LP-mechanical-review.zip`|底座STEP/STL、盖板STEP/STL/DXF、印刷SVG、参数与当前装配STEP|
|`manufacturing-readback.json`|独立Gerber/钻孔/IPC回读及BOM/CPL一致性|
|`metadata-only-proof.json`|原生焊盘/铜几何比较及三处元数据差异|
|`mechanical/mechanical-checks.json`|当前STEP的坐标、孔位、结构件与探针包络检查|
|`mechanical-access-envelope.json`|插头/刀杆工程包络及紧固堆叠计算；不是所选插头实测|
|`mechanical-part-readback.json`、`lid-dxf-readback.json`|既有单件STEP/STL与当前CAD一致、闭合网格及DXF毫米单位检查|

BOM/CPL字段参照[嘉立创国内格式规范](https://www.jlc.com/portal/server_guide_48022.html)；单行表头、完整列出位号、同一毫米原点，BOM与CPL集合一致。坐标是KiCad封装原点/旋转，未替工厂确认具体MPN的吸取中心、零度定义及极性；不能将CSV格式正确当作实际贴装方向通过。

## 原点、叠层与数据检查

辅助原点(88,61)mm；Gerber、钻孔、CPL、IPC均减去它。X向右、Y向上，因此当前板多为负Y；结构源使用同一PCB原点，CadQuery Y负值朝前。不得单独平移/反射CPL或钻孔。板轮廓中心线110×80mm；原生Gerber Job尺寸110.1×80.1mm包含0.1mm边框笔宽，不是改变板框。原生Job的`rev?`占位仅在生成数据中改为PCB文件SHA前12位，几何、层及材料字段不变，精确身份见manifest。

Gerber Job回读确认F.Cu/In1.Cu/In2.Cu/B.Cu四层，外铜35µm、内铜15.2µm；两侧7628介质各0.2104mm，中心core1.065mm，名义成品1.6mm、ENIG。订单前仍需嘉立创国内确认同一叠层和阻抗公差。USB主段W0.2474/S0.1524mm为90Ω工程选择，细引脚出口不是恒定阻抗线；两内层保持GND。

Gerbonara1.6.3独立读入11层Gerber及两份钻孔。842个孔（PTH836、NPTH6，含4个槽）逐一核对中心和尺寸；Excellon坐标量化0.001mm，本次最大单轴舍入约0.0005mm，非实际加工精度。IPC的1524条记录=746个铜/机械焊盘记录+778个过孔，与原生物理端点和162个网络分组对应；759个PCB焊盘对象中的13个纯锡膏开口不作电测点。IPC坐标量化0.0001inch，最大位置差约0.001754mm；ASCII描述中中文变问号、部分长名截断，但按物理端点确认网络对应唯一，原中文网名映射在回读JSON中。该数据核对不等于已经完成裸板电测。

保留两条关于G90所在段的解析告警；所有孔坐标/尺寸已独立对应，语法仍由工厂CAM接收确认。Job中的PadToPad/PadToTrack摘要0.1016mm不能代替当前0.127mm DRC：原生查询仅六个无网络NPTH的OwnClearance为0.1016，其余≥0.127，全局和DRU均保持0.127。未因导出改制造约束。已查看独立Gerber回读的正反铜和两内层；这些图来自实际制造文件，不是PCB SVG替代。

## 再生成核心命令

在工程根目录运行，`kicad-cli`指本机KiCad10.0.7。输出路径可统一选择当前审阅reports，避免混用其他源哈希；先完整DRC，再导出。所有生成后处理记录源哈希，更新Job身份、CPL字段和BOM集合检查。

```sh
kicad-cli pcb export gerbers --layers F.Cu,In1.Cu,In2.Cu,B.Cu,F.Mask,B.Mask,F.Silkscreen,B.Silkscreen,F.Paste,B.Paste,Edge.Cuts --use-drill-file-origin --precision 6 --no-protel-ext --check-zones -o hardware/design/reports/manufacturing-review-2026-11-14/fabrication/ hardware/design/HSLink-LP.kicad_pcb
kicad-cli pcb export drill --format excellon --drill-origin plot --excellon-units mm --excellon-zeros-format decimal --excellon-oval-format route --excellon-separate-th -o hardware/design/reports/manufacturing-review-2026-11-14/fabrication/ hardware/design/HSLink-LP.kicad_pcb
kicad-cli pcb export pos --side both --format csv --units mm --use-drill-file-origin --exclude-dnp --smd-only -o hardware/design/reports/manufacturing-review-2026-11-14/assembly/kicad-smd-positions.csv hardware/design/HSLink-LP.kicad_pcb
kicad-cli pcb export ipcd356 -o hardware/design/reports/manufacturing-review-2026-11-14/HSLink-LP-ipc356.d356 hardware/design/HSLink-LP.kicad_pcb
```

## 未关闭的设计/生产门槛

- CBL801资料缺少插头最大外形、插合总高和排线弯曲参数。34×12mm的ARM20工程包络、13×4mm的UART包络可从当前开口竖直进入而不碰底座/盖板；不能据此保证所选线束已匹配。实际料/可靠尺寸图仍需补齐。
- D4mm竖直刀杆在四个电源端子螺丝位置对底座/盖板无干涉，不包括手柄、斜插及真实槽型。USB14×8mm护套仍为工程假设；拨杆全行程、手指空间和热熔/打印/板厚/紧固件公差待实物。
- 当前上盖螺丝名义啮合3.5mm，螺柱公端穿过PCB后4.4mm，热熔螺母4mm、预孔深5mm，公端尖端距孔底约0.6mm。只是名义堆叠，非强度/扭矩保证；材料与完整紧固件料号/报价仍未闭合。
- 工厂CAM/DFM、DSBGA钢网与贴装/X-ray、过孔盖油、J101固定脚焊接、实际零件/封装映射及机器旋转须审核；未上传下单或取得工厂接受结论。
- 40MHz、持续1A、140nA/20～30°C、逐板校准VIO±1%及长控制/Vref动态保留实板门槛；FSA漏电温区上限预算问题仍未关闭。固件/HID/测量锁实现为其他交付，不能由制造文件证明已实现。


## 2026-11-14 国内阻抗计算器复核

已实际操作[国内计算器](https://tools.jlc.com/jlcTools/index.html#/impedanceCalculatenew)：4层、名义1.6mm、外1oz/内0.5oz、外层非共面差分、L1/L2参考、90Ω、6mil线距。通用`JLC04161H-7628`结果为成品1.59mm±10%，两侧7628各0.2104mm、core1.065mm、外铜0.035/内铜0.0152mm，与本PCB导出的Gerber Job逐层相同。不是工厂已经接受订单。

线宽显示9.7mil；9.7和9.8mil反算分别约90.126Ω和89.916Ω。当前0.2474mm=9.74015748mil位于两者之间，因此保留现有主段，不为页面显示精度重布USB。输入精确值时页面仍显示9.7、反算仍90.126，不能把它记为精确线宽的计算结果；这里只用相邻显示值做局部敏感性检查，不作为整板或制造公差界限。动态页面没有列Er/损耗角，既有4.4/4.6/0.02记录未改，尤其不把2018年网页参数混用。

本次仅补资料及哈希，PCB/叠层/规则文件未变，当前完整DRC结果仍适用。输入、结果DOM与截图、实际Job叠层比对放在当前reports的`domestic-stack/`。下单指定同一结构、阻抗公差及工厂CAM/贴装预览仍待确认；细焊盘出口、实物线宽和USB性能均未由该计算验收。
