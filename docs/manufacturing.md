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


## 本轮交付范围与当前完成度（2026-11-14）

用户已明确排线可以不考虑，因此排线选型/核价/插合/弯曲资料从本轮交付门槛中移出；前述调查保留，不把缺项写成验证通过。PCB布线/约束、完整DRC0/0/0、网表一致性、制造文件及回读、结构C的CAD单件/装配文件与当前尺寸模型的静态干涉检查均已完成。

“其余都完成”只适用于上述文件和CAD检查，不等于完整投产放行。材料/紧固件的最终采购型号与成本、拨杆全行程、样件公差/实际试装、工厂CAM与贴装接受以及40MHz/持续1A/140nA/20～30°C/VIO±1%实板验收仍未完成。本轮不改铜、叠层、接口、BOM、结构几何或指标，因此沿用对应未变源的检查结果，不重复运行相同检查。


## 首次打样订单与结构下单（2026-11-14）

用户确认本次PCB采用无铅OSP及±20%阻抗管控，不要求沉金/±10%；0.25mm最小钻孔由用户确认已设置，尚未独立从生产稿验证。铜层、叠层和尺寸保持。旧制造ZIP的`HSLink-LP-job.gbrjob`仍写ENIG，`fabrication-notes.txt`也沿用沉金说明；不可把它们当作本次用户坚持沉金。工厂须按本次订单OSP覆盖旧说明，层序仍为F.Cu(L1)→In1.Cu(L2)→In2.Cu(L3)→B.Cu(L4)，两内层均GND。ZIP已有完整FilesAttributes层序和MaterialStackup，不因网页层压顺序字段空白而认定Gerber缺层；仍需在CAM生产预览核对工厂实际映射。既有ZIP保留原哈希，不静默替换用户已上传文件。

PCB5片、电子散件10套；透明PC/亚克力各1片且均定制印刷。底座/紧固件1套仍是准备假设。当前无新的锁价/锁库/支付证据，不沿用SMT单价作为散件零售价。

### 底座建议填写（原方案，已被2026-11-15紧凑螺钉方案替代）

上传`hardware/design/mechanical/hslink_lp_base.stl`，可另附同名STEP作尺寸参考；不用装配STEP或上盖STL替代底座。模型毫米，外包络118×88×10mm，保持100%比例。建议FDM/ABS、白色或自然白、1件；保留原PETG为设计材料建议，ABS是结合嘉立创国内材料目录提出的本次采购建议，未写成用户已确认。不要将普通SLA树脂或“ABS-like”树脂当成热塑性ABS。热熔螺母预孔4.1mm/深5mm，按完整螺母料号和打印公差试装；底座平面朝平台、四柱朝上，支柱/孔周足够实心或高填充由工厂确认，切勿按普通装饰件缩放/掏空。没有对ABS收缩、翘曲、热熔或螺柱保持力进行样件验收。

嘉立创材料目录列ABS（https://www.jlc-3dp.cn/material/_1.html），此前PETG建议不代表该渠道当前必然可选。若报价页没有所需热塑料，不自动替换树脂。

### 2mm印刷盖板建议填写

面板类型亚克力面板、透明亚克力、基材2mm、118×88mm、单款1片、底面打印、常规遮光（白底）、不背胶、需要确认生产稿。白墨只覆盖有印刷内容的区域；中间透明区除白色接口字之外不印。图纸为正面俯视、可读方向；底面印刷镜像由工厂处理，不重复镜像。切割以DXF为准，PDF/SVG只规定印刷，不根据预览PNG切割。油墨增加总厚度（官网常规约0.1mm），尚未纳入原2mm纯板模型的完整公差验收。

本次将原SVG的14组文字转为Bezier路径，文本内容/颜色/位置中心和切割边界不改；1:1矢量PDF118×88mm无字体依赖。上传包为ignored reports中的`HSLink-LP-panel-order.zip`，含切割DXF、转曲SVG、1:1PDF、预览和加工说明；预览棋盘底纹不印。当前字样沿用HSLP；INT/EXT方向依据图纸推导，仍须样品导通确认，不能写成实际开关已验证。

PC是独立2mm透明聚碳酸酯板切割+同稿印刷，不用薄膜PC或透明光敏树脂替代。当前面板亚克力选项已确认，2mm厚PC支持/印刷附着与报价尚未核实，不能照亚克力金额代填PC。订单数量各1，分开记录材料和报价。

官方面板流程（https://www.szlcmb.com/processGuidance.html）说明底面印刷、白底遮光、油墨厚度和生产稿；该流程资料不代表工厂已接受本工程DXF/SVG/PDF或承诺印刷公差。


## 2026-11-15 嵌件及面板工艺交付（历史，嵌件/平台已撤销；面板稿仍有效）

厂家《镶嵌螺母说明》（https://www.jlc-3dp.cn/technicalColumnsDetails/41455）规定M3*4*3为内M3/外径4/长3mm，预孔3.6mm深5mm，孔壁≥3mm及14×14mm工具平面。原底座4.1mm预孔/7mm支柱是通用自装假设，不能直接匹配下拉目录；现实施上述型号×4，位置PDF/PNG已生成。较长型号需要更深盲孔，本轮未选。

底座当前124×94×10mm、FDM ABS白色建议；原118×88mm STL须替换。四处14.2mm方平面向外偏移2.2mm，避免扩大平台与来源开关干涉，保留PCB孔位/板底Z9/盖板118×88×2及装配高度。预孔名义最小侧壁3.1mm、孔底至脚垫槽3.5mm。已完成更新模型的静态碰撞/工具平面/盖板实体差及STL回读；孔公差、热熔或其他工厂实际镶嵌工法、保持力、紧固扭矩和样件试装仍待工厂审核/实测。

底座改动增加材料体积，不能沿用用户截图旧模型ABS白色61元作为新报价。厂家公开2023服务说明按4颗×5元参考20元，不是当前订单锁价；底座、嵌件、运输分别以重传后实际报价为准。镶嵌服务若已含4颗螺母，不再重复购买4颗散件。

底座上传当前`hslink_lp_base.stl`，嵌件栏选M3*4*3、4处（整件底座数量1）；另传`insert-fit-2026-11-15/HSLink-LP-insert-installation.pdf`或同名PNG。底座参考包`HSLink-LP-base-order.zip`含STL/STEP/安装PDF/PNG和说明，3D主文件仍用单件STL。原机械审阅包保留为原哈希历史证据，不代表新底座。

按用户提供面板规范，盖板上传包已增加`GUIDE-HSLink-LP-panel-process.pdf/.png`：正面效果图、印刷图案1:1、外框118×88、红线只切割不印、黄色只标无色透明、白色接口文字要白墨、不背胶、无鼓包、RGB色号、字体全部转曲。实际PRINT文件不加红线/黄色，CUT-DXF几何保持。生产稿需确认一次底面镜像而非上传背面镜像稿；2mmPC加工渠道仍待核实。

既有PCB、原理图及约束源未变，沿用对应哈希的DRC/连接记录，不将结构适配写成新的电气或实板验证。


## 2026-11-15 当前底座：紧凑外观＋底部隐藏螺钉

本节覆盖上述嵌件/平台和旧公母螺柱说明。用户拒绝外扩方平台，底座恢复118×88×10mm、四个D7圆柱支承。取消嵌件和代镶嵌；网页“镶嵌螺母”选“不需要”，不再上传旧镶嵌位置图。PCB、四孔位置、板底Z9、盖板118×88×2与ARM20→UART A→UART B→DUT电源保持。透明盖切割/印刷包继续用原稿，无需因底部紧固方式重传盖板。

### 本轮紧固件尺寸方案

- 下方：4颗M3×12内六角平圆头（GB/T70.2），头径最大5.7mm、头高最大1.65mm、2mm内六角。不是普通高圆柱头；后者会顶脚垫。长度12mm的标准表界限11.65～12.35mm，仍须商品图确认。
- 中间：4颗M3双通黄铜柱，柱身长12mm，对边不超过5.5mm；优先贯通M3内螺纹，每端有效牙深至少5mm。原M3公母12+6柱及旧嵌件不能沿用。精确商品、有效螺纹与当前零售价未核实，BOM不填假价格。
- 上方保留4颗M3×6上盖螺钉和4片外径7/内径3.2/厚0.5mm垫圈；脚垫D10×2mm×4，选绝缘非导电材料、最后贴合。

尺寸资料：[嘉立创FA GB/T70.2-2015手册](https://www.jlc-jdgf.com/mcbook/GBT70-2.htm?navbar=off)。标准头部/长度不是已锁定的具体库存商品证明。下螺钉从塑料底部穿过底座和PCB，拧入双通柱；用小扳手扶柱，禁止借PCB或焊点强扭。上盖独立从上方拆卸，底螺钉保留；需要全拆时先揭脚垫。

### 沉孔及名义堆叠

四处安装孔D3.4mm贯穿支柱；底面D10脚垫凹槽深0.5mm。头部沉孔D6.6mm，从脚垫凹槽面再向上深2.0mm，即螺钉承压面Z2.5mm（总深度从外底面算2.5mm），不是从底面再加2.5mm。该承压面在3mm底板以内，支柱不留镶嵌盲孔。

名义PCB上表面10.6mm；下螺钉尖端14.5mm，几何插入柱长3.9mm。盖板下表面22.6mm；上螺钉几何插入3.5mm，两端尖端间隔4.6mm。平圆头与脚垫上表面间隙0.35mm，径向沉孔余量0.45mm。几何插入深度包括端部倒角/不完整牙，并非完整牙有效啮合保证；须用实际铜柱与螺钉检查能可靠夹紧且不顶底，再轻紧，扭矩待样件确认。

公差筛查仅是参数扫描：取下螺钉长度±0.35mm（上述标准表）、柱下支承面至螺钉座的塑料有效厚度6.5±0.4mm、PCB1.6±0.16mm，下端几何插入2.99～4.81mm。上螺钉±0.24mm、盖板±0.2mm、垫圈±0.1mm、铜柱长±0.2mm作为工程筛查输入，两尖端最小间隔约2.95mm。除标准列明螺钉长度外，其余不是采购方已承诺的公差，且未覆盖打印形变、牙口倒角、预紧与蠕变。到货检查完整牙、孔通畅、头部不顶脚垫、PCB不翘曲，不能把本计算当作强度验收。

### 当前上传与成本边界

上传单件`hardware/design/mechanical/hslink_lp_base.stl`，毫米/100%比例；建议FDM/ABS白色、1件。不要上传装配STEP代替单件，不选镶嵌，不再用124×94mm平台STL或旧镶嵌PDF。当前底座包和装配示意见`reports/compact-fastening-2026-11-15/HSLink-LP-base-order.zip`，包含STL/STEP与PDF/PNG。上盖继续使用`reports/procurement-2026-11-14/HSLink-LP-panel-order.zip`。

取消4处镶嵌和服务；历史公开4×5元服务参考不再适用，但它并非当前订单锁价，不能称已节省20元。新增4颗底部螺钉，公母柱换双通柱；底座缩小后需重传报价，原截图61元也不能保证沿用。本轮未变电子BOM/PCB成本；新的结构件净差额须等底座与散件报价核齐，不把10套SMT元件口径套到零售紧固件。

当前完成的是CAD静态装配/沉孔/头部/脚垫间隙、盖板实体不变和网格回读检查；结果及哈希见`hardware/validation.json`。FDM尺寸/收缩、铜柱有效牙深与扭矩、盖板挠曲、拨杆全行程、实际试装及40MHz/持续1A/140nA/VIO精度仍需实物；既有PCB/原理图/规则未变，沿用对应源的完整DRC0/0/0与连接记录。


## 2026-11-15 商城模板 BOM

已按用户提供的立创商城模板生成`hardware/bom/HSLink-LP-立创商城BOM.xlsx`。Sheet1电子采购57种/193件每板，与当前PCB原生采购位号集合相同；导入该页后商城套数设10，单套用量不再乘10。Sheet2为结构件1套准备清单、PC/亚克力各1片，不自动套用10套；无准确商品编号项须另选实物核图。Sheet3记录使用边界。模板示例/原说明行删除，原列序和工作表名保持；TP/孔/定位点、已排除排线及嵌件不进入电子采购。

此次修正SN74LVC1T45原BOM通用参数中的误导性OE/Mbps描述，明确无独立OE；未换料、未改变数量/连接或历史价格字段，材料增量0。数据/整数数量/文本C编码/完整位号已回读，四处表格预览已查看。没有重新锁库或核定商城散件价、MOQ、备损及运费，不把此次模板整理写成已完成采购报价。详见`hardware/bom/README.md`和validation记录。
