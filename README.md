# HSLink-LP

基于 HSLink Pro 1.2.0 / HPM5301 的双串口调试与低功耗测试工程。

**当前状态：上游布局的降本原理图审阅稿、完整嘉立创 BOM 核价记录及 ARM20 接口。** 已安装 KiCad MCP 和三项社区 skills，原理图由上游原文件复制后，通过 MCP 增改电路和整理文字。上游源码通过 Git 子模块管理。尚无 PCB、新板固件或真实设备通信；器件清单不是生产 BOM。

## 已确定的目标

- 新整板，单 USB-C，保留 CMSIS-DAP / SWD / JTAG。
- 两路 USB CDC 串口，各带 TX/RX、DTR/RTS；首版信号电平 1.8～3.3 V。
- 目标接口为带键 ARM 20 针，nTRST 第3针、nRESET 第15针；目标供电走独立接口。
- 40 MHz 调试链路验收目标，实际速率受目标芯片及连接条件限制。
- 内置可调供电 1.8～5.0 V / 最高 1 A；外部供电 1.8～5.5 V / 最高 2 A。
- 保留隔离Vref检测；取消DUT_OUT实测电压回读，供电范围不变。
- 外部供电测量仪负责电流测量；测量状态保持目标供电、断开信号及检测支路。
- 25±5°C 条件下，夹具附加电流目标 ≤0.14 µA，必须以整板实测确认。
- Mac 命令行工具和 Python 库；暂不包含图形界面。

电源来源按用户选择采用板上手动切换。电脑控制目标板电源通断，与来源选择分开。

打开 [HSLink-LP.kicad_pro](hardware/design/HSLink-LP.kicad_pro)。接入方式见 [KiCad MCP 与 skills](docs/kicad-integration.md)，降本方案见 [设计说明](docs/cost-down.md)，板上材料 ¥124.5295/板，加配套排线 ¥128.3725/套（10 套材料 ¥1,283.7250，不含制造、运输与采购余料），见 [成本评估](docs/cost.md)，未关闭的设计问题见 [设计审查](hardware/design/README.md)。Python 环境、依赖与执行统一使用 uv。

工作区只保留一份当前设计，历史通过 Git 提交回溯，不再使用版本号目录副本。原理图、符号库、候选 BOM 和验证摘要纳入 Git；KiCad 本机设置、备份、锁文件、导出报告和缓存由 `.gitignore` 排除。临时生成、排版脚本已删除；已安装的 MCP 服务放在用户工具目录。

## 目录

| 目录 | 用途 |
| --- | --- |
| `docs/` | 需求、架构、验收与实施阶段 |
| `hardware/design/` | 唯一的当前 KiCad 工程和项目符号库 |
| `hardware/validation.json` | 原理图文件检查、源文件哈希及各部分验证状态 |
| `hardware/reference/` | 固定版本的上游硬件参考 |
| `hardware/bom/` | 候选器件及验证状态 |
| `firmware/` | 改版固件及板级配置的工作目录 |
| `host/` | Mac / Python 控制工具骨架 |
| `tools/` | 获取固定版本上游源码的辅助工具 |
| `upstream.lock.json` | 上游仓库、版本和本地路径 |

## 开始使用

先阅读 [需求](docs/requirements.md)、[架构](docs/architecture.md) 和 [验证计划](docs/validation.md)。

通过 uv 运行命令行骨架：

```bash
uv run --project host hslink-lp info
```

该命令只显示工程状态，不连接设备。查看上游依赖：

```bash
uv run --python 3.12 tools/fetch_upstream.py --list
```

克隆本工程后，在工程根目录恢复全部上游源码及其嵌套子模块：

```bash
git submodule update --init --recursive --depth=1
uv run --python 3.12 tools/fetch_upstream.py --check
```

也可按需初始化单个上游工程：

```bash
uv run --python 3.12 tools/fetch_upstream.py hardware
uv run --python 3.12 tools/fetch_upstream.py firmware
uv run --python 3.12 tools/fetch_upstream.py sdk
```

SDK 和固件子模块下载可能较大。辅助工具会核对锁文件与 Git 子模块提交，拒绝覆盖已有修改或不同版本的工作区。它不执行上游构建脚本、不安装编译器或全局依赖。维护方法见 [上游工程](docs/upstream.md)，器件资料见 [参考资料](docs/references.md)。

## 当前边界

- 不存在可直接投板的改版电路或可烧录的新固件。
- 40 MHz、1 A/2 A 和低漏电都是设计与验收目标，尚未验证。
- FSA2466 14路在25°C的上限求和已占满140 nA整夹具目标；覆盖20～30°C的全温表值筛选为700 nA，另有U901、线束及PCB，预算仍未闭合。目标信号连接期间必须保持调试器USB供电；USB掉电而目标仍供电的FSA保护不在首版支持范围，未实现掉电保护。
- 不使用原版固件自动识别逻辑驱动改版电源电路。
- 新板需要独立板型、硬件身份和启动时默认关闭的输出控制。

ARM20 针脚、封装和线束见 [接口说明](docs/arm20-interface.md)，[板上 BOM](hardware/bom/candidates.csv)与[配件 BOM](hardware/bom/accessories.csv)分列。现货 20 cm 排线仅作为打样配套，手册绝缘下限不足以保证 0.14 µA，必须通过整夹具漏电及 40 MHz 实测后放行。

2026-11-07侧线程结论已同步：[边界、漏电与电源余量](docs/electrical-margins.md)。R42/VIO候选仅完成条件计算，未改阻值或宣称硬件通过。
