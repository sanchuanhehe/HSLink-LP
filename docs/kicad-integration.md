# KiCad 与 Codex 接入记录

更新：2026-11-05。Python 环境、依赖和执行统一使用 **uv**。

## 当前安装

| 项目 | 版本 / 状态 |
| --- | --- |
| KiCad | 本机 10.0.7，未升级到 11 |
| MCP | [mixelpixx/KiCAD-MCP-Server](https://github.com/mixelpixx/KiCAD-MCP-Server)，v2.8.3 |
| 固定提交 | `1d204fe3384eb73c890bbe531538a6e735c40fe0` |
| 用户工具目录 | `~/.local/share/kicad-mcp-server/`，保留上游 MIT 许可 |
| Codex 注册名 | `kicad_hslink`，stdio，通过安装目录的 `launch.sh` 启动 |
| Python | KiCad 自带 Python 3.9，依赖环境位于安装目录的 `runtime/python-env/`，由 `python-uv.sh` 通过 uv 启动 |
| 整理后复测 | 独立启动服务，列出 122 个工具；读取当前根页的 28 个符号；确认实际使用 uv 启动入口 |

MCP、Node 依赖、Python 环境、字体缓存都在用户工具目录，不放入工程或 Git。Codex 的注册配置位于用户自己的 `~/.codex/config.toml`，仓库不携带这份本机配置。

服务返回 `backend=swig`、`realtime=false`、`ipcConnected=false`。这是文件级 MCP 工作流。原理图 IPC 是外部程序通过进程间接口访问正在运行的 KiCad 编辑器；当前接入没有该实时编辑器能力。

启动配置通过 `KICAD_PYTHON` 指向 uv 包装入口。该版服务优先搜索安装目录中的 `venv/` 和 `.venv/`，因此依赖环境放在 `runtime/python-env/`，避免绕过 uv。`HSLINK_NODE` 可覆盖本机 Node 路径；不要用不兼容的系统 Python 加载 `pcbnew`。

## 已安装的社区 skills

以下三项已安装在 `~/.codex/skills/`：

- [kicad-schematic](https://github.com/mixelpixx/Konnect/blob/main/crates/konnect/assets/skills/kicad-schematic/SKILL.md)：功能分组、接线、渲染和验证。
- [kicad-library](https://github.com/mixelpixx/Konnect/blob/main/crates/konnect/assets/skills/kicad-library/SKILL.md)：符号、封装及物理引脚核对。
- [kicad-review](https://github.com/mixelpixx/Konnect/blob/main/crates/konnect/assets/skills/kicad-review/SKILL.md)：ERC、实际网表及图面复查。

它们来自同一作者的 Konnect 仓库，工具名称与 TypeScript MCP 不完全一致，需按当前工具清单映射使用，不能把不存在的工具当作已执行。

## 设计来源和工作区整理

当前 `hardware/design/HSLink-LP.kicad_pro` 基于锁定的 HSLink Pro 1.2.0 原图增改，共 9 页。设计期间实际使用了 MCP 的器件、连线、层次页、符号及字段工具；按 UUID 编辑、字段字号等上游能力不足的操作曾通过临时本地 MCP 扩展完成。

按工程整理要求，临时扩展、请求生成器、一次性检查脚本和本地调用客户端已删除，当前启动的是未修改的上游标准服务。若后续标准工具不能完成某项操作，应如实说明能力缺口；不能继续宣称旧扩展仍已安装。以保存的 KiCad 源文件为准，不依赖旧脚本重建原理图。

工程历史由 Git 管理，不再保留版本号目录副本。MCP 安装不随工程清理而卸载。新 Codex 会话会读取更新后的启动路径；已经运行的旧服务需要重载后使用新路径。

## 后续编辑与验证

- 先读取当前原理图，再调用 MCP 修改。对不支持的属性，不能只根据成功响应认定修改已生效。
- 移动器件后检查标签是否仍连接在线段或引脚上，重新导出实际网表并运行 ERC。
- 每次版面修改后查看实际 PDF 或渲染图，检查位号、数值、引脚名、说明与连线的重叠。
- 文件检查摘要及源文件哈希记录在 [hardware/validation.json](../hardware/validation.json)；命令见 [验证计划](validation.md)。可再生成的 PDF、网表与 ERC 输出放在被 Git 忽略的 `hardware/design/reports/`。

MCP 返回成功、ERC 通过和图面可读分别是不同检查，也都不能代替封装核对及硬件实测。
