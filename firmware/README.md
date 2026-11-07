# 固件工作区

上游 CherryDAP 基线：67fb4b5412772a6a435e5f02f694f1615f0b5030。
参考项目：projects/HSLink-Pro；HPM SDK：v1.9.0。
工具链基线：xPack RISC-V GCC 13.2.0-2，darwin-arm64，riscv-none-elf。

```bash
uv run --python 3.12 tools/fetch_upstream.py firmware
uv run --python 3.12 tools/fetch_upstream.py sdk
```

在工程根目录运行。CherryDAP 与 HPM SDK 均通过 Git 子模块管理，嵌套依赖按各自仓库记录的提交恢复。执行 `uv run --python 3.12 tools/fetch_upstream.py --check` 可核对全部版本与工作区。维护方法见 [上游工程](../docs/upstream.md)。

工具链需单独安装，当前没有安装或编译。

后续改版创建独立板型，正式工作代码与上游参考分开管理。首先实现双 CDC、独立 DMA/缓冲、GPIO 扩展和 OFF/ACTIVE/MEASURE/FAULT 状态机。切勿把旧版 HSP_Loop 的 Vref 自动开启逻辑原样用于新板。

当前没有新的板级引脚表、编译目标或可烧录固件。原版板型仅用于参考，不代表适配了 HSLink-LP。

本板已取消DUT_OUT电压回读，U1.26留NC；仅保留U1.27的隔离Vref ADC。不得上报设定值作为实测电压，也不能在板内完成输出掉压或放电完成的电压判断。读Vref不得解除MEASURE锁。能力/状态字段与控制时序是待实现约束，见[接口语义](../docs/control-interface.md)；当前没有新增真实HID或仪器功能。
