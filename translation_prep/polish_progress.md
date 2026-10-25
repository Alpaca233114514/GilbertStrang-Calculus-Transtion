# 润色进度（语言灵动性与适度通俗性）

规范见 `translation_prep/polish_guide.md`；结构校验用 `translation_prep/tools/check_polish.py`。状态：`pending` 未润色，`polished` 已改待查，`checked` 结构与内容核对通过。

已完成并核对：全部 96 份译稿（前言、0–16 章正文、书前书后各表）；索引、积分表、公式速查表共 4 份按规范 skipped，不润色。

本轮补充口径（2026-10-26，用户指示）：只改灵动性不足的句子，不逐句重写。因此 43 号以后各节的改动行数多在 3%–10%，汉字数与基线相差在 ±3% 内；此前已入库的节（0–5 章部分）改动幅度较大，复核时按初译提交 9ab997d 比对。

注：26–29 号稿的润色已随提交 f3d0471 入库，核对时须用初译提交 9ab997d 作基线（`git show 9ab997d:路径 > tmp/x.md`，再 `check_polish.py --base tmp/x.md`）；其余未提交稿直接用默认的 HEAD 基线。

复核状态（2026-10-26）：96 份均已完成独立语义复核——逐段对照初译与 `translation_prep/source_text/` 英文页，专查信息增删、条件松动、术语混用、语义漂移、结构越权。复核共查出 88 处越界，已逐条改回（典型：量词加强「全看/最快/都要/之一」、条件句改陈述、第一人称被抹、新增原文没有的比喻、25 号稿公式被拆开并加记号）。改动只回收不新增，各稿仍为润色稿，reviewed 未动。

下一步：全书独立复审（各稿 reviewed 仍为 false）；本次登记在 `issues.json` 的初译/原书疑点（DRAFT-157～162 等）须在复审时定夺。

| 文件 | 主题 | 状态 |
| --- | --- | --- |
| [00_preface.zh-CN.md](../translation_draft/00_preface.zh-CN.md) | 前言 | checked |
| [01_ch00_sec01.zh-CN.md](../translation_draft/01_ch00_sec01.zh-CN.md) | 第 0 章　微积分要点 | checked |
| [02_ch00_sec02.zh-CN.md](../translation_draft/02_ch00_sec02.zh-CN.md) | 0.2 $y=x^2$ 与 $y=x^n$ 的变化斜率 | checked |
| [03_ch00_sec03.zh-CN.md](../translation_draft/03_ch00_sec03.zh-CN.md) | 0.3 指数函数 $y=e^x$ | checked |
| [04a_ch00_sec04.zh-CN.md](../translation_draft/04a_ch00_sec04.zh-CN.md) | 0.4 视频讲座概要与练习题（上） | checked |
| [04b_ch00_sec04.zh-CN.md](../translation_draft/04b_ch00_sec04.zh-CN.md) | 0.4 视频讲座概要与练习题（下） | checked |
| [05_ch00_sec05.zh-CN.md](../translation_draft/05_ch00_sec05.zh-CN.md) | 0.5 函数图像与图形计算器 | checked |
| [06_ch01_sec01.zh-CN.md](../translation_draft/06_ch01_sec01.zh-CN.md) | 第 1 章　微积分导论 | checked |
| [07_ch01_sec02.zh-CN.md](../translation_draft/07_ch01_sec02.zh-CN.md) | 1.2 暂不使用极限的微积分 | checked |
| [08_ch01_sec03.zh-CN.md](../translation_draft/08_ch01_sec03.zh-CN.md) | 1.3 瞬时速度 | checked |
| [09_ch01_sec04.zh-CN.md](../translation_draft/09_ch01_sec04.zh-CN.md) | 1.4 圆周运动 | checked |
| [10_ch01_sec05.zh-CN.md](../translation_draft/10_ch01_sec05.zh-CN.md) | 1.5 三角学复习 | checked |
| [11_ch01_sec06.zh-CN.md](../translation_draft/11_ch01_sec06.zh-CN.md) | 1.6 千点光芒 | checked |
| [12_ch02_sec01.zh-CN.md](../translation_draft/12_ch02_sec01.zh-CN.md) | 第2章 导数 | checked |
| [13_ch02_sec02.zh-CN.md](../translation_draft/13_ch02_sec02.zh-CN.md) | 2.2 幂函数与多项式 | checked |
| [14_ch02_sec03.zh-CN.md](../translation_draft/14_ch02_sec03.zh-CN.md) | 2.3 斜率与切线 | checked |
| [15_ch02_sec04.zh-CN.md](../translation_draft/15_ch02_sec04.zh-CN.md) | 2.4 正弦函数与余弦函数的导数 | checked |
| [16_ch02_sec05.zh-CN.md](../translation_draft/16_ch02_sec05.zh-CN.md) | 2.5 乘积、商与幂的求导法则 | checked |
| [17_ch02_sec06.zh-CN.md](../translation_draft/17_ch02_sec06.zh-CN.md) | 2.6 极限 | checked |
| [18_ch02_sec07.zh-CN.md](../translation_draft/18_ch02_sec07.zh-CN.md) | 2.7 连续函数 | checked |
| [19_ch03_sec01.zh-CN.md](../translation_draft/19_ch03_sec01.zh-CN.md) | 第3章 导数的应用 | checked |
| [20_ch03_sec02.zh-CN.md](../translation_draft/20_ch03_sec02.zh-CN.md) | 3.2 最大值与最小值问题 | checked |
| [21_ch03_sec03.zh-CN.md](../translation_draft/21_ch03_sec03.zh-CN.md) | 3.3 二阶导数：弯曲与加速度 | checked |
| [22_ch03_sec04.zh-CN.md](../translation_draft/22_ch03_sec04.zh-CN.md) | 3.4 函数图像 | checked |
| [23_ch03_sec05.zh-CN.md](../translation_draft/23_ch03_sec05.zh-CN.md) | 3.5 抛物线、椭圆和双曲线 | checked |
| [24_ch03_sec06.zh-CN.md](../translation_draft/24_ch03_sec06.zh-CN.md) | 3.6 迭代 $x_{n+1}=F(x_n)$ | checked |
| [25_ch03_sec07.zh-CN.md](../translation_draft/25_ch03_sec07.zh-CN.md) | 3.7 牛顿法（及混沌） | checked |
| [26_ch03_sec08.zh-CN.md](../translation_draft/26_ch03_sec08.zh-CN.md) | 3.8 中值定理与洛必达法则 | checked |
| [27_ch04_sec01.zh-CN.md](../translation_draft/27_ch04_sec01.zh-CN.md) | 第4章 用链式法则求导 | checked |
| [28_ch04_sec02.zh-CN.md](../translation_draft/28_ch04_sec02.zh-CN.md) | 4.2 隐函数求导与相关变化率 | checked |
| [29_ch04_sec03.zh-CN.md](../translation_draft/29_ch04_sec03.zh-CN.md) | 4.3 反函数及其导数 | checked |
| [30_ch04_sec04.zh-CN.md](../translation_draft/30_ch04_sec04.zh-CN.md) | 4.4 反三角函数 | checked |
| [31_ch05_sec01.zh-CN.md](../translation_draft/31_ch05_sec01.zh-CN.md) | 第5章 积分 | checked |
| [32_ch05_sec02.zh-CN.md](../translation_draft/32_ch05_sec02.zh-CN.md) | 5.2 原函数 | checked |
| [33_ch05_sec03.zh-CN.md](../translation_draft/33_ch05_sec03.zh-CN.md) | 5.3 求和与积分 | checked |
| [34_ch05_sec04.zh-CN.md](../translation_draft/34_ch05_sec04.zh-CN.md) | 5.4 不定积分与换元法 | checked |
| [35_ch05_sec05.zh-CN.md](../translation_draft/35_ch05_sec05.zh-CN.md) | 5.5 定积分 | checked |
| [36_ch05_sec06.zh-CN.md](../translation_draft/36_ch05_sec06.zh-CN.md) | 5.6 积分的性质与平均值 | checked |
| [37_ch05_sec07.zh-CN.md](../translation_draft/37_ch05_sec07.zh-CN.md) | 5.7 微积分基本定理及其应用 | checked |
| [38_ch05_sec08.zh-CN.md](../translation_draft/38_ch05_sec08.zh-CN.md) | 5.8 数值积分 | checked |
| [39_ch06_sec01.zh-CN.md](../translation_draft/39_ch06_sec01.zh-CN.md) | 第6章 指数函数与对数函数 | checked |
| [40_ch06_sec02.zh-CN.md](../translation_draft/40_ch06_sec02.zh-CN.md) | 6.2 指数函数 $e^x$ | checked |
| [41_ch06_sec03.zh-CN.md](../translation_draft/41_ch06_sec03.zh-CN.md) | 6.3 科学与经济学中的增长和衰减 | checked |
| [42_ch06_sec04.zh-CN.md](../translation_draft/42_ch06_sec04.zh-CN.md) | 6.4 对数函数 | checked |
| [43_ch06_sec05.zh-CN.md](../translation_draft/43_ch06_sec05.zh-CN.md) | 6.5 可分离变量方程与逻辑斯谛方程 | checked |
| [44_ch06_sec06.zh-CN.md](../translation_draft/44_ch06_sec06.zh-CN.md) | 6.6 以幂代替指数函数 | checked |
| [45_ch06_sec07.zh-CN.md](../translation_draft/45_ch06_sec07.zh-CN.md) | 6.7 双曲函数 | checked |
| [46_ch07_sec01.zh-CN.md](../translation_draft/46_ch07_sec01.zh-CN.md) | 第7章 积分方法 | checked |
| [47_ch07_sec02.zh-CN.md](../translation_draft/47_ch07_sec02.zh-CN.md) | 7.2 三角函数的积分 | checked |
| [48_ch07_sec03.zh-CN.md](../translation_draft/48_ch07_sec03.zh-CN.md) | 7.3 三角换元 | checked |
| [49_ch07_sec04.zh-CN.md](../translation_draft/49_ch07_sec04.zh-CN.md) | 7.4 部分分式 | checked |
| [50_ch07_sec05.zh-CN.md](../translation_draft/50_ch07_sec05.zh-CN.md) | 7.5 反常积分 | checked |
| [51_ch08_sec01.zh-CN.md](../translation_draft/51_ch08_sec01.zh-CN.md) | 第8章　积分的应用 | checked |
| [52_ch08_sec02.zh-CN.md](../translation_draft/52_ch08_sec02.zh-CN.md) | 8.2　平面曲线的弧长 | checked |
| [53_ch08_sec03.zh-CN.md](../translation_draft/53_ch08_sec03.zh-CN.md) | 8.3　旋转曲面的面积 | checked |
| [54_ch08_sec04.zh-CN.md](../translation_draft/54_ch08_sec04.zh-CN.md) | 8.4 概率与微积分 | checked |
| [55_ch08_sec05.zh-CN.md](../translation_draft/55_ch08_sec05.zh-CN.md) | 8.5 质量与矩 | checked |
| [56_ch08_sec06.zh-CN.md](../translation_draft/56_ch08_sec06.zh-CN.md) | 8.6 力、功和能量 | checked |
| [57_ch09_sec01.zh-CN.md](../translation_draft/57_ch09_sec01.zh-CN.md) | 第9章　极坐标与复数 | checked |
| [58_ch09_sec02.zh-CN.md](../translation_draft/58_ch09_sec02.zh-CN.md) | 9.2 极坐标方程与图像 | checked |
| [59_ch09_sec03.zh-CN.md](../translation_draft/59_ch09_sec03.zh-CN.md) | 9.3 极坐标曲线的斜率、弧长与面积 | checked |
| [60_ch09_sec04.zh-CN.md](../translation_draft/60_ch09_sec04.zh-CN.md) | 9.4 复数 | checked |
| [61_ch10_sec01.zh-CN.md](../translation_draft/61_ch10_sec01.zh-CN.md) | 第10章　无穷级数 | checked |
| [62_ch10_sec02.zh-CN.md](../translation_draft/62_ch10_sec02.zh-CN.md) | 10.2 收敛判别法：正项级数 | checked |
| [63_ch10_sec03.zh-CN.md](../translation_draft/63_ch10_sec03.zh-CN.md) | 10.3 收敛判别法：一般级数 | checked |
| [64_ch10_sec04.zh-CN.md](../translation_draft/64_ch10_sec04.zh-CN.md) | 10.4　$e^x$、$\sin x$ 与 $\cos x$ 的泰勒级数 | checked |
| [65_ch10_sec05.zh-CN.md](../translation_draft/65_ch10_sec05.zh-CN.md) | 10.5　幂级数 | checked |
| [66_ch11_sec01.zh-CN.md](../translation_draft/66_ch11_sec01.zh-CN.md) | 第11章　向量与矩阵 | checked |
| [67_ch11_sec02.zh-CN.md](../translation_draft/67_ch11_sec02.zh-CN.md) | 11.2　平面与投影 | checked |
| [68_ch11_sec03.zh-CN.md](../translation_draft/68_ch11_sec03.zh-CN.md) | 11.3　叉积与行列式 | checked |
| [69_ch11_sec04.zh-CN.md](../translation_draft/69_ch11_sec04.zh-CN.md) | 11.4　矩阵与线性方程 | checked |
| [70_ch11_sec05.zh-CN.md](../translation_draft/70_ch11_sec05.zh-CN.md) | 11.5 线性代数 | checked |
| [71_ch12_sec01.zh-CN.md](../translation_draft/71_ch12_sec01.zh-CN.md) | 第12章　沿曲线的运动 | checked |
| [72_ch12_sec02.zh-CN.md](../translation_draft/72_ch12_sec02.zh-CN.md) | 12.2 平面运动：抛体与摆线 | checked |
| [73_ch12_sec03.zh-CN.md](../translation_draft/73_ch12_sec03.zh-CN.md) | 12.3 曲率与法向量 | checked |
| [74_ch12_sec04.zh-CN.md](../translation_draft/74_ch12_sec04.zh-CN.md) | 12.4 极坐标与行星运动 | checked |
| [75_ch13_sec01.zh-CN.md](../translation_draft/75_ch13_sec01.zh-CN.md) | 第13章　偏导数 | checked |
| [76_ch13_sec02.zh-CN.md](../translation_draft/76_ch13_sec02.zh-CN.md) | 13.2 偏导数 | checked |
| [77_ch13_sec03.zh-CN.md](../translation_draft/77_ch13_sec03.zh-CN.md) | 13.3 切平面与线性近似 | checked |
| [78_ch13_sec04.zh-CN.md](../translation_draft/78_ch13_sec04.zh-CN.md) | 13.4 方向导数与梯度 | checked |
| [79_ch13_sec05.zh-CN.md](../translation_draft/79_ch13_sec05.zh-CN.md) | 13.5 链式法则 | checked |
| [80_ch13_sec06.zh-CN.md](../translation_draft/80_ch13_sec06.zh-CN.md) | 13.6 极大值、极小值与鞍点 | checked |
| [81_ch13_sec07.zh-CN.md](../translation_draft/81_ch13_sec07.zh-CN.md) | 13.7 约束与拉格朗日乘子 | checked |
| [82_ch14_sec01.zh-CN.md](../translation_draft/82_ch14_sec01.zh-CN.md) | 第 14 章 重积分 | checked |
| [83_ch14_sec02.zh-CN.md](../translation_draft/83_ch14_sec02.zh-CN.md) | 14.2 换用更合适的坐标 | checked |
| [84_ch14_sec03.zh-CN.md](../translation_draft/84_ch14_sec03.zh-CN.md) | 14.3 三重积分 | checked |
| [85_ch14_sec04.zh-CN.md](../translation_draft/85_ch14_sec04.zh-CN.md) | 14.4 柱坐标与球坐标 | checked |
| [86_ch15_sec01.zh-CN.md](../translation_draft/86_ch15_sec01.zh-CN.md) | 第 15 章　向量微积分 | checked |
| [87_ch15_sec02.zh-CN.md](../translation_draft/87_ch15_sec02.zh-CN.md) | 15.2 曲线积分 | checked |
| [88_ch15_sec03.zh-CN.md](../translation_draft/88_ch15_sec03.zh-CN.md) | 15.3 格林定理 | checked |
| [89_ch15_sec04.zh-CN.md](../translation_draft/89_ch15_sec04.zh-CN.md) | 15.4 曲面积分 | checked |
| [90_ch15_sec05.zh-CN.md](../translation_draft/90_ch15_sec05.zh-CN.md) | 15.5 散度定理 | checked |
| [91_ch15_sec06.zh-CN.md](../translation_draft/91_ch15_sec06.zh-CN.md) | 15.6 斯托克斯定理与场的旋度 | checked |
| [92_ch16_intro.zh-CN.md](../translation_draft/92_ch16_intro.zh-CN.md) | 第 16 章　微积分之后的数学 | checked |
| [93_integral_table.zh-CN.md](../translation_draft/93_integral_table.zh-CN.md) | 积分表 | skipped |
| [94_index.zh-CN.md](../translation_draft/94_index.zh-CN.md) | 索引 | skipped |
| [95_reference_tables.zh-CN.md](../translation_draft/95_reference_tables.zh-CN.md) | 公式与单位速查表（书末） | skipped |
| [96_front_matter.zh-CN.md](../translation_draft/96_front_matter.zh-CN.md) | 封面、扉页、目录与致读者 | checked |
| [97_front_formula_tables.zh-CN.md](../translation_draft/97_front_formula_tables.zh-CN.md) | 公式速查表（书前） | skipped |
| [98_source_notice.zh-CN.md](../translation_draft/98_source_notice.zh-CN.md) | MIT 开放课程来源说明 | checked |
