# 参考资料与版本

上游代码版本见 `upstream.lock.json`。三个上游仓库均使用提交 SHA；SDK 的 `v1.9.0` 标签已解析为 `d64c133d0626a6986125f33c2e3f9283c7088e88`。Git 子模块固定同一提交，维护方式见 [上游工程](upstream.md)。

## 上游工程

- [HSLink 硬件仓库](https://github.com/cherry-embedded/HSLink-hardware)，使用 `HSLinkPro_v1.2.0` 子目录。
- [原版 1.2.0 原理图固定版本](https://github.com/cherry-embedded/HSLink-hardware/blob/c315927df32c9de4cd2d5447a6e171fc19618024/HSLinkPro_v1.2.0/HSLinkPro.kicad_sch)。
- [CherryDAP 固件仓库](https://github.com/cherry-embedded/CherryDAP)，使用 `projects/HSLink-Pro`。
- [原版板级定义固定版本](https://github.com/cherry-embedded/CherryDAP/blob/67fb4b5412772a6a435e5f02f694f1615f0b5030/projects/HSLink-Pro/common/hslinkpro/board.h)。
- [HPM SDK](https://github.com/hpmicro/hpm_sdk/tree/v1.9.0)。

## 候选器件原厂资料

| 器件 | 资料 | 设计前必须核查 |
| --- | --- | --- |
| FSA2466 | [数据手册](https://www.onsemi.com/download/data-sheet/pdf/fsa2466-d.pdf) | 1.8～3.3 V 信号、3.6 V 供电、漏电预算、USB 掉电风险；40 MHz 须实测 |
| HFD2/005-S | [数据手册](https://source.hongfa.com/Uploads/Product/PDF/HFD2_en.pdf) | 触点最小负载、2 A 压降与热、带续流的释放时间 |
| TPS63811 | [TPS63810/TPS63811 数据手册](https://www.ti.com/lit/ds/symlink/tps63810.pdf) | 上电默认状态、输入能力、输出功率和热设计 |
| TUSB320LAI | [产品与资料](https://www.ti.com/product/TUSB320LAI) | Type-C 可用电流识别与系统限流的配合 |
| TLV75801 / MCP4725 | [完整引脚与资料索引](costdown-pinmap.md) | 反馈注入公式、默认关闭、DAC 写入顺序和 VIO 热设计 |
| Dailywell 2MD1T1B1M2QES-5 | [引脚与资料索引](costdown-pinmap.md) | 准确后缀、BBM 和 DC 额定值确认 |

器件典型值不构成整板指标保证。BOM 冻结时应保存所用数据手册版本，并逐项记录工作条件与验证结果。
