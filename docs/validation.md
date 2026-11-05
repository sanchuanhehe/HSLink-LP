# 验证计划

下表为硬件验收项目，全部尚未执行。原理图文件检查摘要及源文件哈希记录在 [hardware/validation.json](../hardware/validation.json)；ERC 和网表比较不能代替硬件验收。版本使用 Git 提交定位，不复制工程目录。

## 原理图文件检查

在工程根目录使用 KiCad 10 的命令行重新导出：

```bash
mkdir -p hardware/design/reports
kicad-cli sch erc --format json --exit-code-violations -o hardware/design/reports/erc.json hardware/design/HSLink-LP.kicad_sch
kicad-cli sch export netlist --format kicadxml -o hardware/design/reports/netlist.xml hardware/design/HSLink-LP.kicad_sch
kicad-cli sch export pdf -o hardware/design/reports/HSLink-LP.pdf hardware/design/HSLink-LP.kicad_sch
```

`reports/` 为可再生成输出，Git 忽略。每次电路修改后，核对实际 XML 网表与 `hardware/design/connectivity.json` 中的器件及引脚网络集合，同时检查未连接引脚、缺失封装，并逐页查看实际图面。验证通过后更新摘要和文件哈希；临时检查脚本不保留在工作区。`connectivity.json` 是设计基线，不能代替实际导出网表。

版面修改也必须核对网表。对每个标签，检查文字是否被导线、引脚或符号边框穿过，移动后是否仍有明确接点；电源汇线应避开引脚编号。对自定义符号，核对引脚线内端与边框、脚名位置，并确认脚号、电气类型和外部连接端坐标未被排版操作改动。分别查看默认字体和实际阅读字体的导出图；过滤空白字符后的文本包围盒检测只能作为辅助。

2026-11-06 的检查通过标准 MCP 执行；服务调用 KiCad CLI 运行 ERC，原始 MCP 响应保存在 `reports/erc-mcp.json`，其余证据见 `hardware/validation.json`。上面的命令可重新生成完整 CLI ERC JSON。

## 硬件验收

| 项目 | 方法与通过条件 |
| --- | --- |
| 40 MHz | 在支持该频率的目标或测试夹具上检查实际时钟、双向时序、波形及错误；记录 1.8/3.3 V 信号电平、线长、负载和探头 |
| 双串口 | 两路 3 Mbaud / 8N1 同时收发并执行调试，使用序列号或 CRC 检查丢字节和串扰；检查两组 DTR/RTS |
| 内置供电 | 1.8/3.3/5.0 V 下检查空载、负载、瞬态、纹波、温升、过流保护及 USB 输入电流预算 |
| 外部路径 | 最高 5.5 V / 2 A 条件检查压降、温升、反向供电及关断 |
| 低功耗 | 25±5°C、保持相同目标端电压，比对物理拔线与软件断开，附加电流 ≤0.1 µA；记录仪器误差与环境条件 |
| 断开覆盖 | 逐项检查调试、复位、两路 UART、Vref、目标电压、放电、ESD 与备用接口 |
| 异常恢复 | USB 拔插、复位、Bootloader、外部电源掉电、断开时打开串口或发送 DAP，不能意外接通 |
| 重复性 | 至少 1000 次连接、隔离、恢复和电源循环，检查最终状态和数据一致性 |

## 前置验证

先制作“电平转换＋模拟开关”验证电路和电源路径验证电路，通过后再冻结整板原理图。

漏电测试使用可覆盖 0.1 µA 误差目标的仪器和接线。必须排除目标自身电压变化、USB 额外供电、低侧测量被共地旁路、接触污染等影响。

室温测量状态、掉电状态、电源关闭状态和高温状态分开记录。任何未达到的设计指标应明确标注，不静默降低验收目标。

## 报告字段

样板编号、硬件/固件版本、仪器型号及校准信息、温湿度、电源和信号电平、接线照片、测试步骤、原始数据路径、结果与限制。
