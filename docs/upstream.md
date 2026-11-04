# 上游工程管理

记录日期：2026-11-04。

本项目使用 Git 子模块保存上游源码，主仓库只记录子模块地址与提交，不将上游文件复制成普通文件。`upstream.lock.json` 与 Git 子模块提交必须一致。上游保留各自许可证，改版工作与参考源码分开。

## 固定版本与入口

| 上游 | 本地路径 | 固定提交 |
| --- | --- | --- |
| HSLink-hardware | `hardware/reference/HSLink-hardware` | `c315927df32c9de4cd2d5447a6e171fc19618024` |
| CherryDAP | `firmware/upstream/CherryDAP` | `67fb4b5412772a6a435e5f02f694f1615f0b5030` |
| HPM SDK v1.9.0 | `firmware/sdk/hpm_sdk` | `d64c133d0626a6986125f33c2e3f9283c7088e88` |

- 硬件参考：`hardware/reference/HSLink-hardware/HSLinkPro_v1.2.0/HSLinkPro.kicad_pro`。
- 固件应用：`firmware/upstream/CherryDAP/projects/HSLink-Pro/src/`。
- Bootloader：`firmware/upstream/CherryDAP/projects/HSLink-Pro/bootloader/`。
- 原版板级定义：`firmware/upstream/CherryDAP/projects/HSLink-Pro/common/hslinkpro/`。
- SDK 中文说明：`firmware/sdk/hpm_sdk/README_zh.md`。

CherryDAP 包含 13 个递归子模块，包括 CherryUSB、CherryRB 和 HSLink-Pro 的第三方依赖；它们的提交由各自父仓库记录。当前固定版本的硬件仓库与 HPM SDK 没有子模块。

## 获取与检查

在本工程根目录执行：

```bash
git submodule update --init --recursive --depth=1
python3 tools/fetch_upstream.py --check
```

辅助工具支持按需初始化或补齐缺失的嵌套依赖：

```bash
python3 tools/fetch_upstream.py hardware
python3 tools/fetch_upstream.py firmware
python3 tools/fetch_upstream.py sdk
```

初始化前，工具检查 `.gitmodules`、Git 索引中的子模块提交与锁文件；已有上游工作区如有本地修改或处于不同版本，会报错并保留现场。下载失败后不要直接删除目录，先查看错误与 `git submodule status --recursive`，确认现场后再恢复。

只读检查不会下载或改变版本。命令不带依赖名时检查全部依赖，也可执行 `python3 tools/fetch_upstream.py firmware --check` 检查单个依赖。

本次下载使用浅克隆，只包含固定提交所需的历史。后续需要查阅更早提交时，在对应子模块内按需执行 `git fetch --unshallow`。

## 版本升级

有意升级时，先检查目标上游版本与兼容性，再更新对应子模块提交和 `upstream.lock.json`；涉及 SDK 时保留其来源标签。重新检查递归依赖后，将 Git 子模块指针、锁文件和验证记录一起提交到主仓库。日常恢复不使用 `git submodule update --remote`，避免意外跟随上游最新分支。

新板改动放在 `hardware/design/`；后续固件需创建独立板型，并明确工作分支或补丁的管理方式。当前子模块作为基线，不直接修改。

## 接入验证与边界

- 已下载上述三个固定版本，并恢复 CherryDAP 的 13 个递归子模块。
- 已核对主仓库子模块指针、锁文件、工作区 HEAD、来源 URL 及递归子模块状态。
- 三个上游仓库的 `LICENSE` 文件随源码保留。
- 本次只接入与检查源码；未安装 RISC-V 工具链、编译固件或进行硬件验证。
