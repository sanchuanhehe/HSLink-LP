# 硬件工作区

- `design/`：新板 KiCad 工程。当前尚未绘制。
- `reference/`：上游 HSLink Pro 1.2.0 参考源码。
- `bom/candidates.csv`：候选器件，不可直接用于采购生产。

获取参考源码：

```bash
python3 tools/fetch_upstream.py hardware
```

从工程根目录运行。随后打开 reference/HSLink-hardware/HSLinkPro_v1.2.0/HSLinkPro.kicad_pro 阅读原板。

新板必须另存至 design/，不要直接修改参考仓库。没有完成原理图、电路验证及 PCB 审查前，不生成“生产就绪”标记。
