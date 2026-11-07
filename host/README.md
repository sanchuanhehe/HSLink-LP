# Mac / Python 工具骨架

Python 3.10+。当前仅提供本地工程信息命令，尚未实现设备发现、HID、串口控制或仪器适配。

从项目根目录运行：

```bash
uv run --project host hslink-lp --help
uv run --project host hslink-lp info
```

需要安装开发入口时，在独立虚拟环境内执行：

```bash
uv sync --project host --python 3.12
uv run --project host hslink-lp info
```

后续加入真实传输层前先冻结固件 HID 协议。未来 power_on、power_off、isolate、reconnect、power_cycle 等方法不得返回模拟的“成功”。

本板已取消DUT_OUT电压回读，U1.26留NC；仅保留U1.27的隔离Vref ADC。不得上报设定值作为实测电压，也不能在板内完成输出掉压或放电完成的电压判断。读Vref不得解除MEASURE锁。能力/状态字段与控制时序是待实现约束，见[接口语义](../docs/control-interface.md)；当前没有新增真实HID或仪器功能。
