# SPICE功能测试输入

该目录是当前设计的可复用仿真源文件，不是另一份原理图或版本副本。原理图只在上级目录保留一份，历史使用Git。

| 输入 | 模型及范围 |
| --- | --- |
| vio.cir | 未修改的TI TLV75801P_TRANS宏模型＋实际反馈网络；DAC为理想电压源；10→100mA测试负载含0.5V低压顺从特性 |
| vref.cir | U901为假设Ron/Roff的SPDT，完整68k/68k/1n分压；0/40nA人为注入示例，不能证明真实漏电 |
| discharge.cir | K601 COM/NO/NC与R57/Q902拓扑；触点/FET用有限电导行为模型，延迟、转换时间均为假设 |
| safety.cir | 从最终导出网表的U301～U304引脚分组生成逻辑连接；512组稳定输入组合，非传播延迟或固件仿真 |

`safety.cir`中`POWER_OFF`是实际自动网络`Net-(U303-1B)`的SPICE安全别名，未改真实网络。其他边界信号与原理图一致。`.save`限制保存的节点，`.tran`给出默认测试时长。变更电路后必须重新核对映射，不能只重跑旧测试台。

## 模型与重跑

模型出处、SHA256、端口顺序和局限在`models.json`。TI原文件保留版权头；未修改，放入忽略目录`../reports/spice-models/`，不在本仓库重新分发。需从TI官方SBVM926下载并解压`TLV75801P_TRANS.lib`至该位置，再核对哈希。SLVMDI3仅用于适用性审查，未用作TPS22950C验证。

已安装独立ngspice的环境可在本目录运行，例如（输出目录需先存在）：

```sh
ngspice -b -r ../reports/vio.raw -o ../reports/vio.log vio.cir
ngspice -b -r ../reports/vref.raw -o ../reports/vref.log vref.cir
ngspice -b -r ../reports/discharge.raw -o ../reports/discharge.log discharge.cir
ngspice -b -r ../reports/safety.raw -o ../reports/safety.log safety.cir
```

`.spiceinit`启用PSpice兼容模式；需要正常安装的XSPICE模型。当前Mac没有独立ngspice命令，本轮通过uv运行一次性ctypes适配器调用KiCad的`Contents/Frameworks/libngspice.0.dylib`，并加载`Contents/PlugIns/sim/ngspice/`下的analog、digital、spice2poly和xtradev代码模型。运行参数、每个实际测试台、ngspice日志与ASCII原始波形保存在`../reports/spice-2026-11-11/`；临时适配器删除，不作为项目运行依赖。

默认VIO采用Gear、reltol=1e-3、最大步长0.5µs。3.3V高输入和DAC零码另以reltol=1e-4、最大步长0.25µs复查；零码异常启动对数值设置仍敏感，不能据此决定故障钳位。未进行完整温度、生产容差、DAC误差和校准仿真。

结果、未覆盖部分及工程变化见[仿真记录](../../../docs/spice-validation.md)。求解完成不等于整板验收；140nA、40MHz、1A及±1%目标仍待实测。

## 2026-11-12 专项测试台

- `vio-sequencing.cir`：外部DAC反馈跳变、EN顺序、容量/ESR参数；默认含12×100nF远端去耦的集中等效。TI模型在此动态反馈场景出现非物理吸收/源电流，不可使用微秒建立时间或启动峰值作器件保证；零码和轻载关机存在数值敏感性。
- `vref-acquisition.cir`：U901在完整分压之前，ADC采样保持Cs=4pF/Ron=300Ω仅典型；采样前电荷预置是压力模型，可扫采样窗、容量、阻抗、前一通道电压。
- `discharge-faults.cir`：复位、旧放电请求、触点延迟/抖动与持续外部能源；R37/R62双100k下拉已纳入当前测试台。实际门欠压行为、继电器线圈/触点和MOS模型缺项仍需实测。

新增27份波形对应输入和参数变化详见忽略目录`../reports/prefab-2026-11-11/case-index.json`及各目录`case.cir`；当前通用测试台包含本轮查出的完整去耦/双下拉，早期诊断用例仍原样保留以便审计，不冒称其覆盖所有真实负载。两份轻载22ms用例关机处超时，失败日志另存；18ms结果只评价关机前部分。模型文件未修改。数值、计算和流程边界见[专项分析](../../../docs/prefab-analysis.md)。
