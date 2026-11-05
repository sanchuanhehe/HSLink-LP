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
