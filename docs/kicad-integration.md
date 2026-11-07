# KiCad 与 Codex 接入记录

更新：2026-11-07。Python 环境、依赖和执行统一使用 **uv**。

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

2026-11-06 的标签与符号修正全部使用标准 MCP 工具完成。实测发现 `batch_set_schematic_property_positions` 的括号匹配不忽略字符串：遇到 `TLP3547(TP1,F` 等型号，可能将后续多个器件的字段一起移动。该处改用能正确处理字符串括号的 `edit_schematic_component.fieldPositions`，按 Git 基线恢复受影响字段后重新检查了导出图。未修改已安装服务，也未留下临时扩展。移动旋转器件的字段时还需显式保留原 `angle`，否则工具默认设为 0。

MCP 返回成功、ERC 通过和图面可读分别是不同检查，也都不能代替封装核对及硬件实测。

2026-11-07 降本修改使用标准 MCP 完成器件、接线、字段、符号与封装。自由文字和图签缺少编辑接口，本次使用临时 MCP 注释工具，仅允许精确匹配的顶层文字／图签编辑并验证其他对象逐字节不变；完成后删除。项目封装的查询缓存存在缺陷，回读验证时临时注册全局库 `HSLinkLP_PinCheck_Temporary`，最终通过 MCP 删除。正式工程使用 `${KIPRJMOD}/libraries/HSLinkLP.pretty`，不依赖临时全局项。

本轮移除 TCA9543A、合并 I2C 和替换 MCP4726 均通过标准 MCP 完成。一次性注释工具还按唯一 UUID 删除了删除器件后遗留的孤立 NC 标记，校验其余对象逐字节一致；随后全项目 ERC 为零，实际网表与预先定义意图一致。标准服务未修改；临时客户端、检查脚本、扩展和验证工程均在记录证据后清理。

本轮 `open_project` 在仅有原理图的正式项目上返回 SWIG/缺少 PCB 会话错误，没有据此调用 `save_project` 或创建空白 PCB。文件级原理图工具已经保存修改，随后独立 MCP 进程导出的网表、双字体 PDF 和 ERC 读取的是这些已保存文件。

12 颗 DBVR 实施使用标准 MCP 放置/接线/字段和导出检查。A3 页面设置、旧对象清理及保留复位电路整体移动，由临时 MCP 适配器调用安装环境中的 kicad-skip 完成；清除该 API 删除最后一个 NC 后残留的空标记。大批量放置超时后先回读已写入位号，再分批补全，未重复放置。临时适配器、客户端与验证工程在证据保存后删除，正式服务未改动。

本轮单Vref修改：器件、精确连线/标签删除、接线、字段及导出/ERC使用标准MCP；新符号通过create_symbol建立。标准删除会自动清理无效结点；剩余两个旧NC和新增NC、自由文字由仅接受已核对UUID的临时MCP适配器处理。曾计划的坐标范围批量清理被自动审批拒绝，未执行，改为逐段标准MCP精确删除。适配器还用pcbnew完成临时封装回读，并对语义完全不变的对象恢复Git原始格式。标准list_symbol_pins的项目库查询失败，以临时/正式实例get_schematic_pin_locations及导出XML的六脚记录交叉验证；不伪称缺失工具执行成功。客户端/适配器/缓存用后删除。

格式检查中，进一步重排顶层对象以减小Git差异的操作被自动审批拒绝，未执行；最终只通过MCP逐行清除行尾空白，并验证解析对象与顺序完全不变。

## KiCad 10 原生格式统一（2026-11-07）

使用本机 KiCad 10.0.7 的原生 `sch upgrade`、`sym upgrade`、`fp upgrade` 原地保存，未手工改文件头。标准 MCP v2.8.3 无格式升级工具，本次由临时 stdio MCP 适配器调用原生命令；标准 MCP 完成转换前后的 ERC、完整层次网表和 PDF 导出。适配器、客户端和检查脚本在完成后删除，常驻服务未修改。

- 9 页原理图分别升级；`sch upgrade` 不递归升级子页，全部逐页执行。当前原理图格式为 `20260306`。
- 2 个工程内符号库（27 个符号）升级为 `20251024`。`UpstreamCache` 是新板自己的缓存；`hardware/reference` 内上游不改。
- 6 个本地封装检查/升级为 `20260206`；其中 4 个原本已是此格式，保持字节不变。
- `.kicad_pro`、库表已被 KiCad 10 正常使用，原样保留。文件类型的内部格式编号各不相同，不把项目 JSON 或库表的 schema 数字强行改为 10。当前没有 PCB 文件。

完整网表的器件属性、库引脚和网络内容在转换前后完全一致：194 个物理位号、117 个连接网络、675 个连接引脚、45 个独立 NC；同时与 `connectivity.json` 的引脚集合核对一致。两次 ERC 均为 0 错误、0 告警，未增加忽略规则。27 个符号仅有原生默认字段/空值/排序规范化；6 个封装的焊盘编号、坐标、尺寸、钻孔及图形未变。

九页 PDF 的全部矢量图形、文字内容、位置与样式均一致；原生对象排序造成局部叠画/抗锯齿像素差异，因此不宣称 PDF 二进制或所有像素相同。已查看九页总览并放大复查主控、供电和检测页。证据保存在忽略目录 `hardware/design/reports/kicad10-format-2026-11-07/`，摘要及源文件哈希进入 `hardware/validation.json`。本轮仅转换文件格式，既有电气审查缺项和三处过时注释继续保留记录，不代表实板验收。

若转换时编辑器已打开，关闭旧窗口时不要用旧内存内容覆盖磁盘文件，再从当前 `hardware/design/HSLink-LP.kicad_pro` 重新打开。继续只保留一份工作设计，历史使用 Git。

2026-11-07 VIO余量修改：标准MCP批量改R58/R59/R60与电源符号，保持封装；标准工具重排R60字段、把反馈回线改为同页标签，完整网表核对仅U502.6/C43.1换到USB_5V。原生MCP导出/ERC，临时只读MCP适配器补充Arial Unicode MS PDF（普通Arial缺中文字形，已换字体重导出）。未修改常驻服务，无临时CAD工程副本；客户端、适配器和核查脚本用后删除。
