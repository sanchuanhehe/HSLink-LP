# 固件工作区

上游 CherryDAP 基线：67fb4b5412772a6a435e5f02f694f1615f0b5030。
参考项目：projects/HSLink-Pro；HPM SDK：v1.9.0。
工具链基线：xPack RISC-V GCC 13.2.0-2，darwin-arm64，riscv-none-elf。

```bash
python3 tools/fetch_upstream.py firmware
python3 tools/fetch_upstream.py sdk
```

在工程根目录运行。工具链需单独安装，初始化阶段没有安装或编译。

后续改版创建独立板型，正式工作代码与上游参考分开管理。首先实现双 CDC、独立 DMA/缓冲、GPIO 扩展和 OFF/ACTIVE/MEASURE/FAULT 状态机。切勿把旧版 HSP_Loop 的 Vref 自动开启逻辑原样用于新板。

当前没有新的板级引脚表、编译目标或可烧录固件。原版板型仅用于参考，不代表适配了 HSLink-LP。
