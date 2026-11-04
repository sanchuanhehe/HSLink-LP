# HSLink-LP

基于 HSLink Pro 1.2.0 / HPM5301 的双串口调试与低功耗测试工程。

**当前状态：工程初始化。** 已保存需求、架构、验收计划和软件目录；尚未完成改版原理图、PCB、固件或真实设备通信。器件清单是待验证候选，不是生产 BOM。

## 已确定的目标

- 新整板，单 USB-C，保留 CMSIS-DAP / SWD / JTAG。
- 两路 USB CDC 串口，各带 TX/RX、DTR/RTS；信号电平 1.8～5.0 V。
- 40 MHz 调试链路验收目标，实际速率受目标芯片及连接条件限制。
- 内置可调供电 1.8～5.0 V / 最高 1 A；外部供电 1.8～5.5 V / 最高 2 A。
- 外部供电测量仪负责电流测量；测量状态保持目标供电、断开信号及检测支路。
- 25±5°C 条件下，夹具附加电流目标 ≤0.1 µA，必须以整板实测确认。
- Mac 命令行工具和 Python 库；暂不包含图形界面。

电源来源目前暂按板上拨动选择设计，**该项尚未由用户确认**。电脑控制目标板电源通断，与来源选择分开。

## 目录

| 目录 | 用途 |
| --- | --- |
| `docs/` | 需求、架构、验收与实施阶段 |
| `hardware/design/` | 后续 KiCad 改版工程 |
| `hardware/reference/` | 固定版本的上游硬件参考 |
| `hardware/bom/` | 候选器件及验证状态 |
| `firmware/` | 改版固件及板级配置的工作目录 |
| `host/` | Mac / Python 控制工具骨架 |
| `tools/` | 获取固定版本上游源码的辅助工具 |
| `upstream.lock.json` | 上游仓库、版本和本地路径 |

## 开始使用

先阅读 [需求](docs/requirements.md)、[架构](docs/architecture.md) 和 [验证计划](docs/validation.md)。

无需安装第三方依赖即可检查命令行骨架：

```bash
PYTHONPATH=host/src python3 -m hslink_lp info
```

该命令只显示工程状态，不连接设备。查看上游依赖：

```bash
python3 tools/fetch_upstream.py --list
```

按需下载固定版本源码：

```bash
python3 tools/fetch_upstream.py hardware
python3 tools/fetch_upstream.py firmware
python3 tools/fetch_upstream.py sdk
```

SDK 和固件子模块下载可能较大。工具不会修改任何已有目标目录，也不会执行上游构建脚本。初始化阶段不自动安装 SDK、编译器或全局依赖。上游与器件资料见 [参考资料](docs/references.md)。

## 当前边界

- 不存在可直接投板的改版电路或可烧录的新固件。
- 40 MHz、1 A/2 A 和低漏电都是设计与验收目标，尚未验证。
- 不使用原版固件自动识别逻辑驱动改版电源电路。
- 新板需要独立板型、硬件身份和启动时默认关闭的输出控制。
