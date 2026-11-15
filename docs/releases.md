# 打样产物归档

## prototype-2026-11-15

[GitHub Release](https://github.com/sanchuanhehe/HSLink-LP/releases/tag/prototype-2026-11-15)，设计源基线`0fe1c4ef0dfc469ad659218d97282f4c92a202f9`。这是首板打样预发布，不代表生产/实板性能放行。当前工作工程仍只有`hardware/design`；归档是已生成的不可编辑交付快照，不作为工程版本副本。

|附件|用途|
|---|---|
|HSLink-LP-Prototype-2026-11-15.zip|完整总包，含证据/许可/已上传旧包的追溯副本|
|HSLink-LP-PCB-Gerber.zip|当前OSP工艺说明＋未改变的11层Gerber和2份钻孔|
|HSLink-LP-Top-Stencil.zip|顶面钢网及定位板框，1:1不镜像|
|HSLink-LP-Mechanical.zip|紧凑底座、盖板切割/印刷稿、装配STEP/GLB/预览|
|HSLink-LP-BOM.zip|原商城模板、5套散件CSV和结构紧固件清单|
|manifest.json、SHA256SUMS.txt|逐文件来源/哈希及Release附件哈希|

生成文件放ignored `hardware/design/reports/prototype-2026-11-15`；Git只登记本说明、`hardware/releases/prototype-2026-11-15.json`索引与validation摘要。PCB/钢网采用既有独立回读结果，结构核对来源哈希，原XLSX只读复制；本轮无电路/走线/模型/采购变更。原始报价XLS、订单截图、缓存及临时脚本不进入Release。

当前PCB下单包不含旧ENIG Gerber Job/旧加工说明，层序/叠层详见包内READ-ME；原始已上传包只放总包provenance供追溯，不静默覆盖。结构1套、PC/PMMA各1片，脚垫/嵌件不采购；装配参考的脚垫包络只是预留。BOM价格库存为既有快照，未重新核价或锁库。

已有0一般DRC/0未连接，保留U301/U302/U303的6项Value/Specification属性差异；本轮源未改，不重复ERC/DRC。40MHz、持续1A、140nA/20～30°C、VIO±1%、打印/切割/紧固公差、工厂CAM与实板验收仍待完成，详见需求/制造/验证记录。重新产生设计变更后必须生成新标签/归档，不覆盖本标签产物。
