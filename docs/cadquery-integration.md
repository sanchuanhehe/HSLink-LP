# CadQuery 安装与使用

2026-11-11，按用户要求使用 uv 安装。环境位于用户工具目录，不进入硬件工程或 Git。

| 项目 | 当前状态 |
| --- | --- |
| 环境目录 | `~/.local/share/cadquery` |
| CadQuery | 2.8.0 |
| Python | uv 管理的 CPython 3.12.14，arm64；`.python-version` 固定 3.12 |
| 几何内核绑定 | cadquery-ocp 7.9.3.1.1 |
| 依赖管理 | 环境内 `pyproject.toml`、`uv.lock`、`.venv`；使用 `--locked` 按锁文件运行 |
| 图形界面 | 本次安装建模库；FreeCAD、CQ-editor 尚未安装 |

从任意工作目录运行模型文件：

```sh
uv run --project "$HOME/.local/share/cadquery" --locked python /绝对路径/model.py
```

交互使用：

```sh
uv run --project "$HOME/.local/share/cadquery" --locked python
```

在 Python 中可直接 `import cadquery as cq`。结构模型源文件后续放入正式工程并用 Git 管理；不要将模型源文件放进工具的 `.venv`。新增建模依赖也使用此环境的 uv，不复用 KiCad 的 Python 或主机软件环境。

已执行的安装检查：建立30×20×4mm测试实体、四个通孔和圆角；检查实体有效且只有一个实体；体积与解析计算相符；导出STEP/STL/SVG，再导入STEP检查有效性与体积一致。`uv pip check`报告44个依赖均兼容。测试几何使用临时目录并已自动删除，未保留一次性脚本。

检查摘要放入忽略的 `hardware/design/reports/tool-check-2026-11-11/cadquery.json`，环境配置和锁文件哈希记录到 `hardware/validation.json`。这是工具安装检查，不是结构C的装配或强度验收；本轮没有改变原理图、PCB或BOM。

参考：[CadQuery 官方安装说明](https://cadquery.readthedocs.io/en/latest/installation.html)。
