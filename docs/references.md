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
| ADG4612 | [数据手册](https://www.analog.com/media/en/technical-documentation/data-sheets/adg4612_4613.pdf) | 实际供电下的信号范围、全温漏电、导通电阻及寄生电容；40 MHz 须实测 |
| TPS63811 | [TPS63810/TPS63811 数据手册](https://www.ti.com/lit/ds/symlink/tps63810.pdf) | 上电默认状态、输入能力、输出功率和热设计 |
| TUSB320LAI | [产品与资料](https://www.ti.com/product/TUSB320LAI) | Type-C 可用电流识别与系统限流的配合 |
| TLP3547 | [数据手册](https://toshiba-semicon-storage.com/info/docget.jsp?did=36853&prodName=TLP3547) | A 接法、导通压降、温度降额、关闭漏电与开关时间 |

器件典型值不构成整板指标保证。BOM 冻结时应保存所用数据手册版本，并逐项记录工作条件与验证结果。
