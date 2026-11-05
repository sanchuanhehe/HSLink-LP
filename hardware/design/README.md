# HSLink-LP 原理图审阅稿

打开 `HSLink-LP.kicad_pro`。本版以锁定的 HSLink Pro 1.2.0 原文件为基础增改，原参考仓库未修改。历史版本通过 Git 提交回溯，不保留版本号目录副本。当前没有 PCB 或生产文件。

## 本次排版

- 主控根页、晶振、启动电阻、复位 RC、主控电源单元和去耦沿用上游布局；34 个符号单元（33 个物理位号）的坐标、旋转与上游一致，核对结果见 [验证记录](../validation.json)。
- 新增电路按功能紧凑分组。主控仍分信号/电源两个单元；原四页基础上增加五页，共 9 页。
- 位号和数值分开固定位置，显示短型号/数值，完整规格保留在属性及 BOM；扩展自定义符号的引脚间距，避开页框和标题栏。
- 用 MCP 修改原理图、符号及字段；设计期间的对象级操作曾使用临时 MCP 扩展，整理后已移除；已安装的标准 MCP 服务保留在用户工具目录，见 [接入记录](../../docs/kicad-integration.md)。
- R1/R2 对应上游串行调试支路的位号重新映射；R1/R2/R5/L1 的非极性引脚方向按上游保留，差异明确记录在 `upstream-layout.json`。J101 保留位置，使用当前候选 USB4105 的 16P/SH 符号。其余逻辑网络与 Git 中的初版基线等价。

## 阅读顺序

| 页 | 文件 | 电路 |
| --- | --- | --- |
| 1 | HSLink-LP | 主控、晶振、BOOT/RESET、服务口和子页入口 |
| 2 | Power | 上游主控电源与去耦，USB 辅助 3.3/3.6/12 V |
| 3 | Interface | USB-C、CC、ESD、输入限流 |
| 4 | LogicTranslation | 电平转换与开漏复位 |
| 5 | Control | I2C GPIO、总线多路器与默认下拉 |
| 6 | Safety | 硬件禁能与放电互锁 |
| 7 | TargetPower | 内置可调输出、VIO、来源选择、输出开关 |
| 8 | Disconnect | FSA2466、调试和双串口目标接口 |
| 9 | Sense | Vref/目标电压可断开采样、可断开放电 |

## 文件检查

2026-11-05：ERC **0 错误、0 告警**。实际 KiCad XML 网表与基线的 172 个物理位号、129 个逻辑网络和 643 个已连接引脚一致；未连接引脚没有意外短接。此结果不证明物理封装或硬件性能。

本次整理前，已分别检查 KiCad 默认字体和 Arial Unicode MS 导出的 9 页 PDF，包括文本包围盒辅助检测和逐页渲染检查；自动检测不覆盖所有文字/图形相交。整理只移动原理图，源文件 SHA-256 保持一致；检查记录见 [验证记录](../validation.json)。PDF、网表和 ERC 原始输出统一生成到 `reports/`，由 Git 忽略。

一次性生成与排版脚本已删除。以保存的 KiCad 原理图为准。后续修改需重新导出、检查网表与 ERC，并查看实际图面。

## 关键选型与原因

- 数字断开：4×FSA2466UMX，参考 Nordic nRF54L15 DK 同款，B1 接目标、B0 悬空，选择 0 为断开。USB 侧独立 3.6 V 供电。
- 检测/放电断开：ADG4612BRUZ，USB 辅助 12 V 供电，覆盖最高 5.5 V 电源检测。二分之一分压和放电电阻全部放在可断开支路之后。
- VIO：第二颗 TPS63811 从 USB 侧供电并跟随目标 Vref；不从被测目标取电。软件限制到 1.8～3.3 V。
- 内置输出：TPS63811，后接 TPS22950，仅此支路提供板上限流；外部路径的限流由仪器负责。
- 来源选择：NKK M2022SS1W03 候选 DPDT，第二极只报告来源。输出开关：TLP3547 A 接法，LED 驱动来自 USB 侧。
- USB 侧 ESD：TPD2E2U06DCKR；未在 DUT 侧加常接 TVS，以免未计入的漏电污染测量。接口 ESD/误插能力因此仍需单独验证。

## 尚未关闭的问题

| 项目 | 状态 / 下一步 |
| --- | --- |
| 100 nA 附加电流 | FSA 25°C 每通道关断漏电最大值按 10 nA 预算，14 路即 140 nA，尚未计检测、PCB 和连接器；当前不能作整板保证，需试验与方案取舍 |
| USB 掉电隔离 | FSA 不具备保证的掉电隔离；目标独立上电时可能反灌；不得宣称支持该工况 |
| 40 MHz | 需验证电平转换、模拟开关、往返延迟、走线和实际目标；不是已实现速率 |
| 输出能力 | 1 A/2 A 均为目标。TPS22950 1 A 名义限流有容差，不能承诺持续完整 1 A；TLP 热降额、压降和外部 2 A 要实测 |
| USB 预算 | 默认约 0.44 A 硬件限流并不等于枚举前允许取 0.44 A；固件须执行 CC、枚举及挂起功率规则 |
| 未绑定封装 | U501/U502、L4/L5、U601、SW601 共 6 个位号。必须按准确 MPN/后缀完成数据表视图、符号脚号、焊盘号对照和渲染签核 |
| 已绑定封装 | 也只是候选；HPM QFN48+EP、FSA UQFN、连接器朝向等仍需逐项物理映射复核 |
| 恢复与日志 | UART_B 与 ISP 服务口共用；应用禁用该 UART 日志，验证 BOOT/JTAG 恢复流程 |
| 被动器件 | 晶体负载、电源电感饱和/温升、电容直流偏压降容、USB 启动电流待验证 |
| 固件和主机 | 独立板型、双 CDC、HID 协议及 MEASURE 锁定尚未实现；不可烧录原版固件作为成品使用 |

没有因为文件 ERC 通过就冻结硬件。目标供电与信号连接状态分离；MEASURE 保持目标电源而关闭所有调试、复位、双串口握手、Vref、采样和放电支路。默认保留共地，不是电气隔离。

## 资料与许可

- [Nordic nRF54L15 DK 硬件指南](https://docs-be.nordicsemi.com/bundle/nRF54L15_DK/raw/resource/enus/nRF54L15_DK_HW_User_Guide_v0.9.1.pdf)：参考 FSA2466 选型，不等于套用其整板性能。
- [FSA2466 数据表](https://www.onsemi.com/download/data-sheet/pdf/fsa2466-d.pdf)、[ADG4612 数据表](https://www.analog.com/media/en/technical-documentation/data-sheets/adg4612_4613.pdf)、[TPS63811 数据表](https://www.ti.com/lit/ds/symlink/tps63810.pdf)、[TLP3547 数据表](https://toshiba-semicon-storage.com/info/docget.jsp?did=36853&prodName=TLP3547)。
- 每个元件的数据表路径保留在原理图属性、`connectivity.json` 和候选 BOM 中。
- HPM5301 及晶体符号从锁定上游原图的缓存经 MCP 导出至 UpstreamCache 库；符号来源于上游 HSLink 硬件工程，原 Apache-2.0 许可保留为 `libraries/HSLink-upstream-LICENSE`。未修改 `hardware/reference/` 内的上游工程。
