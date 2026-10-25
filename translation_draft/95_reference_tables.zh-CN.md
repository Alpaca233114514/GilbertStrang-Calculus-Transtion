# 公式与单位速查表（书末）

> 来源：原书 PDF 第 704 页，印刷页 I-8 的公式表部分；该页上方索引见 `94_index.zh-CN.md`。状态：中文初译，未独立复审。物理常数和换算数值按原表照录，未更新为现行推荐值。

<!-- PDF 704 / 印刷页 I-8（公式表部分） -->

## 指数与对数

$$
y=b^x\ \Longleftrightarrow\ x=\log_b y,
\qquad y=e^x\ \Longleftrightarrow\ x=\ln y.
$$
$$
e=\lim_{n\to\infty}\left(1+\frac1n\right)^n
=\sum_{n=0}^{\infty}\frac1{n!}=2.71828\ldots,
$$
$$
e^x=\lim_{n\to\infty}\left(1+\frac xn\right)^n
=\sum_{n=0}^{\infty}\frac{x^n}{n!}.
$$
$$
\ln y=\int_1^y\frac{dx}{x},\qquad\ln1=0,\qquad\ln e=1.
$$
$$
\ln(xy)=\ln x+\ln y,\quad \ln x^n=n\ln x,
$$
$$
\log_a y=(\log_a b)(\log_b y),\qquad \log_a b=\frac1{\log_b a},
$$
$$
e^{x+y}=e^xe^y,\qquad b^x=e^{x\ln b},\qquad e^{\ln y}=y.
$$

## 向量与行列式

$$
\mathbf A=a_1\mathbf i+a_2\mathbf j+a_3\mathbf k,
\qquad |\mathbf A|^2=\mathbf A\cdot\mathbf A=a_1^2+a_2^2+a_3^2
\quad\text{（长度的平方）}.
$$
$$
\mathbf A\cdot\mathbf B=a_1b_1+a_2b_2+a_3b_3=|\mathbf A||\mathbf B|\cos\theta.
$$

施瓦茨不等式：$|\mathbf A\cdot\mathbf B|\le|\mathbf A||\mathbf B|$，因为 $|\cos\theta|\le1$。

三角不等式：$|\mathbf A+\mathbf B|\le|\mathbf A|+|\mathbf B|$。

叉积的长度：$|\mathbf A\times\mathbf B|=|\mathbf A||\mathbf B||\sin\theta|$。

$$
\mathbf A\times\mathbf B=
\begin{vmatrix}\mathbf i&\mathbf j&\mathbf k\\a_1&a_2&a_3\\b_1&b_2&b_3\end{vmatrix}
=(a_2b_3-a_3b_2)\mathbf i+(a_3b_1-a_1b_3)\mathbf j+(a_1b_2-a_2b_1)\mathbf k.
$$

右手法则：$\mathbf i\times\mathbf j=\mathbf k$，$\mathbf j\times\mathbf k=\mathbf i$，$\mathbf k\times\mathbf i=\mathbf j$。

平面平行四边形面积：$|a_1b_2-a_2b_1|=|\det|$。

平行六面体体积：$|\mathbf A\cdot(\mathbf B\times\mathbf C)|=|\text{行列式}|$。

## 国际单位制（SI）

| 物理量 | 单位 | 符号及关系 |
|---|---|---|
| 长度 | 米 | m |
| 质量 | 千克 | kg |
| 时间 | 秒 | s |
| 电流 | 安培 | A |
| 频率 | 赫兹 | Hz，$1/\mathrm s$ |
| 力 | 牛顿 | N，$\mathrm{kg\cdot m/s^2}$ |
| 压力 | 帕斯卡 | Pa，$\mathrm{N/m^2}$ |
| 能量、功 | 焦耳 | J，$\mathrm{N\cdot m}$ |
| 功率 | 瓦特 | W，$\mathrm{J/s}$ |
| 电荷 | 库仑 | C，$\mathrm{A\cdot s}$ |
| 温度 | 开尔文 | K |

原表数值：光速 $c=2.9979\times10^8\ \mathrm{m/s}$；引力常数 $G=6.6720\times10^{-11}\ \mathrm{N\,m^2/kg^2}$。

## 方程及其解

| 方程 | 原表列出的解或基本解 |
|---|---|
| $y'=cy$ | $y_0e^{ct}$ |
| $y'=cy+s$ | $y_0e^{ct}+\dfrac sc(e^{ct}-1)$ |
| $y'=cy-by^2$ | $\dfrac c{b+de^{-ct}}$，其中 $d=\dfrac{c-by_0}{y_0}$ |
| $y''=-\lambda^2y$ | $\cos\lambda t$ 与 $\sin\lambda t$ |
| $my''+dy'+ky=0$ | $e^{\lambda_1t}$ 与 $e^{\lambda_2t}$；重根时为 $e^{\lambda_1t}$ 与 $te^{\lambda_1t}$ |
| $y_{n+1}=ay_n+s$ | $a^ny_0+s\dfrac{a^n-1}{a-1}$ |

## 矩阵与逆矩阵

$A\mathbf x$ 是矩阵各列的线性组合，方程为 $A\mathbf x=\mathbf b$。若 $A^{-1}A=I$，则解为 $\mathbf x=A^{-1}\mathbf b$。

最小二乘的正规方程：$A^{\mathsf T}A\mathbf x=A^{\mathsf T}\mathbf b$。

特征值方程：$A\mathbf x=\lambda\mathbf x$，其中 $\lambda$ 为特征值。

$$
\begin{pmatrix}a&b\\c&d\end{pmatrix}^{-1}
=\frac1{ad-bc}\begin{pmatrix}d&-b\\-c&a\end{pmatrix},
$$
$$
(AB)^{-1}=B^{-1}A^{-1},\qquad (AB)^{\mathsf T}=B^{\mathsf T}A^{\mathsf T}.
$$

以列向量 $\mathbf a,\mathbf b,\mathbf c$ 构成矩阵时：

$$
\begin{pmatrix}|&|&|\\\mathbf a&\mathbf b&\mathbf c\\|&|&|\end{pmatrix}^{-1}
=\frac1D\begin{pmatrix}(\mathbf b\times\mathbf c)^{\mathsf T}\\
(\mathbf c\times\mathbf a)^{\mathsf T}\\(\mathbf a\times\mathbf b)^{\mathsf T}\end{pmatrix},
\qquad D=\mathbf a\cdot(\mathbf b\times\mathbf c).
$$
$$
\begin{vmatrix}a_1&a_2&a_3\\b_1&b_2&b_3\\c_1&c_2&c_3\end{vmatrix}
=a_1b_2c_3+a_2b_3c_1+a_3b_1c_2-a_1b_3c_2-a_2b_1c_3-a_3b_2c_1.
$$

## 单位换算

将原单位的数值乘以下表系数，得到目标单位的数值（系数按原表精度）。

| 原单位 | 目标单位 | 乘数 |
|---|---|---:|
| 度 | 弧度 | 0.01745 |
| 卡路里 | 焦耳 | 4.1868 |
| 英热单位（BTU） | 焦耳 | 1055.1 |
| 英尺磅 | 焦耳 | 1.3558 |
| 英尺 | 米 | 0.3048 |
| 英里 | 千米 | 1.609 |
| 英尺／秒 | 千米／小时 | 1.0973 |
| 磅 | 千克 | 0.45359 |
| 盎司 | 千克 | 0.02835 |
| 加仑 | 升 | 3.785 |
| 马力 | 瓦特 | 745.7 |

原表地球赤道半径：$R=6378\ \mathrm{km}=3964$ 英里。

原表重力加速度：$g=9.8067\ \mathrm{m/s^2}=32.174\ \mathrm{ft/s^2}$。

## 译注与待复审事项

- 对数公式采用实数定义域：真数正、底数正且不等于1。逆矩阵须存在，行列式分母非零；特征向量必须非零。
- 方程解表按原书给出典型形式，分母参数为零或初值为零等退化情况须另算；二阶方程的两个基本解应作任意线性组合，$\lambda_i$ 是特征方程的根。符号 $d$ 在两行有不同用途。
- 原表没有注明卡路里、BTU、加仑、马力的具体制式；这里只保留其数值，不能当作所有同名单位的通用精确换算。物理常数属于原书资料，未更新或核定。
- 原矩阵简写以列向量并列、叉积作行；译文补转置符号和 $D$ 的定义以明确形状，不改变公式含义。
