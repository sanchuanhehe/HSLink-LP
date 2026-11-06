# 降本器件物理引脚核对

日期：2026-11-07。范围仅为原理图符号与封装引脚映射；不代表 PCB、额定负载、寿命或漏电验证通过。

通过 MCP 创建／查询符号和封装，临时工程放置后回读全部焊盘并导出原理图与 PCB 图面检查。项目库查询存在缓存缺陷，验证时临时注册全局库，完成后删除；正式工程仅引用项目库。坐标为元件面顶视图，X 向右、Y 向下，以封装原点为基准。定制封装以方形 1 脚焊盘和其外侧丝印短条标记方向，主体在 F.Fab，院落留 ≥0.25 mm。

## HFD2/005-S

来源：[宏发 HFD2 2026 Rev.1.00](https://source.hongfa.com/Uploads/Product/PDF/HFD2_en.pdf)，PDF 第 4 页；底视图沿水平中轴翻转为顶视图，定位标记在左，顶视 1 脚左下。

符号 `HSLinkLP:HFD2_005_S`；封装 `HSLinkLP:Relay_Hongfa_HFD2`。引脚／符号脚／电气焊盘均为 8，无重复焊盘、散热焊盘或机械孔。映射核对：通过；非整板硬件签核。

| 实物端子 | 功能 | 符号脚／类型 | 焊盘 | 顶视 X / Y（mm） | 孔径 / 尺寸（mm） |
|---|---|---|---|---|---|
| 1 | COIL+ | 1 / passive | 1 | -8.8900 / 3.8100 | 1 / 1.8×1.8 |
| 4 | COM1 | 4 / passive | 4 | -1.2700 / 3.8100 | 1 / 1.8×1.8 |
| 6 | NC1 | 6 / passive | 6 | 3.8100 / 3.8100 | 1 / 1.8×1.8 |
| 8 | NO1 | 8 / passive | 8 | 8.8900 / 3.8100 | 1 / 1.8×1.8 |
| 16 | COIL− | 16 / passive | 16 | -8.8900 / -3.8100 | 1 / 1.8×1.8 |
| 13 | COM2 | 13 / passive | 13 | -1.2700 / -3.8100 | 1 / 1.8×1.8 |
| 11 | NC2 | 11 / passive | 11 | 3.8100 / -3.8100 | 1 / 1.8×1.8 |
| 9 | NO2 | 9 / passive | 9 | 8.8900 / -3.8100 | 1 / 1.8×1.8 |


## 2MD1T1B1M2QES-5

来源：[Dailywell 图号 2MDP0428 Rev.A](https://www.thonk.co.uk/wp-content/uploads/2017/05/DW3-DPDT-ON-ON-2MD1T1B1M2QES.pdf)，第 1 页 PC MOUNTING 元件面，与端子视图左右镜像；1 脚左下。

符号 `HSLinkLP:Dailywell_2MD1T1B1M2QES_5`；封装 `HSLinkLP:SW_Dailywell_2MD1T1B1M2QES_5`。引脚／符号脚／电气焊盘均为 6，无重复焊盘、散热焊盘或机械孔。映射核对：通过；非整板硬件签核。

| 实物端子 | 功能 | 符号脚／类型 | 焊盘 | 顶视 X / Y（mm） | 孔径 / 尺寸（mm） |
|---|---|---|---|---|---|
| 1 | INT | 1 / passive | 1 | -2.5400 / 2.5400 | 1.1 / 1.9×1.9 |
| 2 | COM | 2 / passive | 2 | -2.5400 / 0.0000 | 1.1 / 1.9×1.9 |
| 3 | EXT | 3 / passive | 3 | -2.5400 / -2.5400 | 1.1 / 1.9×1.9 |
| 4 | INT_ID | 4 / passive | 4 | 2.5400 / 2.5400 | 1.1 / 1.9×1.9 |
| 5 | ID_COM | 5 / passive | 5 | 2.5400 / 0.0000 | 1.1 / 1.9×1.9 |
| 6 | EXT_ID | 6 / passive | 6 | 2.5400 / -2.5400 | 1.1 / 1.9×1.9 |


## TLV75801PDBVR

来源：[TI SBVS351D](https://www.ti.com/lit/ds/symlink/tlv758p.pdf)，第 3 页图 4-2，DBV 顶视图，1 脚左上，左列向下编号。

符号 `Regulator_Linear:TLV75801PDBV`；封装 `Package_TO_SOT_SMD:SOT-23-5`。引脚／符号脚／电气焊盘均为 5，无重复焊盘、散热焊盘或机械孔。映射核对：通过；非整板硬件签核。

| 实物端子 | 功能 | 符号脚／类型 | 焊盘 | 顶视 X / Y（mm） | 孔径 / 尺寸（mm） |
|---|---|---|---|---|---|
| 1 | IN | 1 / power_in | 1 | -1.1375 / -0.9500 | None / 1.325×0.6 |
| 2 | GND | 2 / power_in | 2 | -1.1375 / 0.0000 | None / 1.325×0.6 |
| 3 | EN | 3 / input | 3 | -1.1375 / 0.9500 | None / 1.325×0.6 |
| 4 | FB | 4 / input | 4 | 1.1375 / 0.9500 | None / 1.325×0.6 |
| 5 | OUT | 5 / power_out | 5 | 1.1375 / -0.9500 | None / 1.325×0.6 |


## MCP4725A0T-E/CH

来源：[Microchip DS20002039F](https://ww1.microchip.com/downloads/aemDocuments/documents/APID/ProductDocuments/DataSheets/MCP4725-12-Bit-Digital-to-Analog-Converter-with-EEPROM-Memory-DS20002039.pdf)，第 2 页 CH/SOT-23-6 顶视图，1 脚左上；不是 DFN 引脚图。

符号 `Analog_DAC:MCP4725xxx-xCH`；封装 `Package_TO_SOT_SMD:SOT-23-6`。引脚／符号脚／电气焊盘均为 6，无重复焊盘、散热焊盘或机械孔。映射核对：通过；非整板硬件签核。

| 实物端子 | 功能 | 符号脚／类型 | 焊盘 | 顶视 X / Y（mm） | 孔径 / 尺寸（mm） |
|---|---|---|---|---|---|
| 1 | VOUT | 1 / output | 1 | -1.1375 / -0.9500 | None / 1.325×0.6 |
| 2 | VSS | 2 / power_in | 2 | -1.1375 / 0.0000 | None / 1.325×0.6 |
| 3 | VDD | 3 / power_in | 3 | -1.1375 / 0.9500 | None / 1.325×0.6 |
| 4 | SDA | 4 / bidirectional | 4 | 1.1375 / 0.9500 | None / 1.325×0.6 |
| 5 | SCL | 5 / input | 5 | 1.1375 / 0.0000 | None / 1.325×0.6 |
| 6 | A0 | 6 / input | 6 | 1.1375 / -0.9500 | None / 1.325×0.6 |


## AO3400A

来源：[AOS AO3400A Rev.3.1](https://www.aosmd.com/sites/default/files/res/datasheets/AO3400A.pdf)，第 1 页 SOT-23 Top View，点标所在 G 端为 1；旋转到库顶视图为左上 G、左下 S、右侧 D。

符号 `Transistor_FET:AO3400A`；封装 `Package_TO_SOT_SMD:SOT-23`。引脚／符号脚／电气焊盘均为 3，无重复焊盘、散热焊盘或机械孔。映射核对：通过；非整板硬件签核。

| 实物端子 | 功能 | 符号脚／类型 | 焊盘 | 顶视 X / Y（mm） | 孔径 / 尺寸（mm） |
|---|---|---|---|---|---|
| 1 | G | 1 / input | 1 | -0.9375 / -0.9500 | None / 1.475×0.6 |
| 2 | S | 2 / passive | 2 | -0.9375 / 0.9500 | None / 1.475×0.6 |
| 3 | D | 3 / passive | 3 | 0.9375 / 0.0000 | None / 1.475×0.6 |


## 1N4148W-7-F

来源：[Diodes DS30086 Rev.32-2](https://www.diodes.com/assets/Datasheets/ds30086.pdf)，第 1 页 SOD123 顶视及阴极条纹，第 4 页封装；厂家未标数字，工程明确规定条纹 K 为焊盘 1，A 为焊盘 2。

符号 `Device:D`；封装 `Diode_SMD:D_SOD-123`。引脚／符号脚／电气焊盘均为 2，无重复焊盘、散热焊盘或机械孔。映射核对：通过；非整板硬件签核。

| 实物端子 | 功能 | 符号脚／类型 | 焊盘 | 顶视 X / Y（mm） | 孔径 / 尺寸（mm） |
|---|---|---|---|---|---|
| 1 | K | 1 / passive | 1 | -1.6500 / 0.0000 | None / 0.9×1.2 |
| 2 | A | 2 / passive | 2 | 1.6500 / 0.0000 | None / 0.9×1.2 |

## 需实板／供应商确认

- 来源开关的 3 A / 28 VDC 来自 [2M 系列手册第 6 页](https://static.chipdip.ru/lib/866/DOC027866893.pdf) Q 银触点额定值；准确 -5 型号的 BBM 转换次序未获得保证，生产前必须确认，运行要求先关闭输出再切换来源。
- HFD2 的最小负载 10 mV / 10 µA 为厂家参考值，需按实际负载确认。检测分压改为 68k + 68k；供电触点低电流接触可靠性、2 A 压降、寿命、浪涌与温升均待测。
- 元件封装已提供，PCB 尚未设计，焊盘可制造性与板级间距仍需 DRC／DFM。
