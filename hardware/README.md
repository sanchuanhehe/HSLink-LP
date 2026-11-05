# 硬件工作区

- `design/HSLink-LP.kicad_pro`：唯一的当前 KiCad 工程；基于上游原文件修改的原理图审阅稿，尚无 PCB。
- `design/reports/`：本机生成的 PDF、网表和 ERC 报告，Git 忽略。
- `validation.json`：检查摘要和源文件哈希，并分别记录原理图、PCB、固件和主机软件状态。
- `reference/`：上游 HSLink Pro 1.2.0 参考源码。
- `bom/candidates.csv`：候选器件，不可直接用于采购生产。

获取参考源码：

```bash
uv run --python 3.12 tools/fetch_upstream.py hardware
```

从工程根目录运行。随后打开 reference/HSLink-hardware/HSLinkPro_v1.2.0/HSLinkPro.kicad_pro 阅读原板。

新板只在 design/ 维护，历史版本通过 Git 回溯，不复制版本号目录。不要直接修改参考仓库。没有完成原理图、电路验证及 PCB 审查前，不生成“生产就绪”标记。
