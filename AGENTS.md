# HSLink-LP 工程约定

- 以 docs/requirements.md 为需求基线；“默认假设”和“待确认”不得写成用户已确认。
- 使用中文撰写设计说明；代码标识符使用英文。
- Python 环境、依赖与执行统一使用 uv；KiCad 的 pcbnew 绑定使用 KiCad 自带 Python。MCP 安装和运行环境放在用户工具目录，见 docs/kicad-integration.md。
- 当前是初始化工程，禁止把占位、模拟结果或候选 BOM 宣称为硬件验证结果。
- 上游版本记录在 upstream.lock.json；外部仓库分别放在指定目录，保留原许可。
- hardware/design 是新板工作区；hardware/reference 内的上游参考不直接修改。
- 当前设计只保留 hardware/design 一份，版本历史使用 Git；不创建 rev0.x 等工程副本目录。
- 临时脚本、排版工具与一次性缓存用完删除；PDF、网表、ERC 输出放在已忽略的 hardware/design/reports，检查摘要和源文件哈希记录在 hardware/validation.json。
- 固件新增独立板型，不以原版 HSLink 固件身份发布改版。
- 低功耗断开必须覆盖 Vref、电压采样、放电、复位及串口握手线。
- 电源来源选择与输出开关分离；测量状态不得被串口打开、DTR/RTS 或 DAP 命令隐式解除。
- 主机软件当前没有真实 HID 传输协议；新增真实控制前先对齐固件协议。
- 原理图、PCB、固件和主机软件分别记录版本与验证结果。
- 不把供应商典型值当作整板保证值；记录温度、接线、电平和仪器条件。
