# 上游硬件参考

`HSLink-hardware` 通过 Git 子模块固定到 `upstream.lock.json` 中的提交，使用 `HSLinkPro_v1.2.0` 子目录，保留上游许可证。

在工程根目录执行 `uv run --python 3.12 tools/fetch_upstream.py hardware` 可初始化或补齐未下载的依赖；执行 `uv run --python 3.12 tools/fetch_upstream.py hardware --check` 可只读核对版本和工作区。

参考原理图：`HSLink-hardware/HSLinkPro_v1.2.0/HSLinkPro.kicad_sch`。

参考 PCB：`HSLink-hardware/HSLinkPro_v1.2.0/HSLinkPro.kicad_pcb`。

改版文件放在 `hardware/design/`，不直接修改本目录中的上游参考。
