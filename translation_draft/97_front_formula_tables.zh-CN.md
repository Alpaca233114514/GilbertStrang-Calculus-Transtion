# 公式速查表（书前）

> 来源：原书 PDF 第 12–13 页，无印刷页码。状态：中文初译，未独立复审。公式依原页分组；省略的适用条件与发现的疑误见末尾译注。不定积分均应补任意常数 $C$。

<!-- PDF 12 / 印刷页 无 -->

## 导数

$$
\begin{aligned}
\text{和：}\quad &(u+v)'=u'+v',\\
\text{乘积：}\quad &(uv)'=uv'+vu',\\
\text{商：}\quad &\left(\frac uv\right)'=\frac{vu'-uv'}{v^2},\\
\text{幂：}\quad &(u^n)'=nu^{n-1}u',\\
\text{链式：}\quad &\frac d{dx}z(y(x))=\frac{dz}{dy}\frac{dy}{dx},\\
\text{反函数：}\quad &\frac{dx}{dy}=\frac1{dy/dx}.
\end{aligned}
$$

| 函数 | 导数 | 函数 | 导数 |
|---|---|---|---|
| $\sin x$ | $\cos x$ | $e^{cx}$ | $ce^{cx}$ |
| $\cos x$ | $-\sin x$ | $b^x$ | $b^x\ln b$ |
| $\tan x$ | $\sec^2x$ | $\ln x$ | $1/x$ |
| $\cot x$ | $-\csc^2x$ | $\sin^{-1}x$ | $1/\sqrt{1-x^2}$ |
| $\sec x$ | $\sec x\tan x$ | $\tan^{-1}x$ | $1/(1+x^2)$ |
| $\csc x$ | $-\csc x\cot x$ | $\sec^{-1}x$ | $1/(\lvert x\rvert\sqrt{x^2-1})$ |

## 极限与连续性

当 $x\to0$ 时：

$$
\frac{\sin x}{x}\to1,\qquad\frac{1-\cos x}{x}\to0,\qquad\frac{1-\cos x}{x^2}\to\frac12.
$$

- $a_n\to0$：对任意 $\varepsilon>0$，存在 $N$，使所有 $n>N$ 满足 $|a_n|<\varepsilon$。
- $a_n\to L$：对任意 $\varepsilon>0$，存在 $N$，使所有 $n>N$ 满足 $|a_n-L|<\varepsilon$。
- $f(x)\to L$（$x\to a$）：对任意 $\varepsilon>0$，存在 $\delta>0$，使 $0<|x-a|<\delta$ 时 $|f(x)-L|<\varepsilon$。
- $f(x)\to f(a)$：当极限 $L=f(a)$ 时，函数在 $a$ 连续。
- $\displaystyle\frac{f(x)-f(a)}{x-a}\to f'(a)$：$a$ 处导数。
- $\displaystyle\frac{f(x)-f(a)}{x-a}=f'(c)$：中值定理。
- $\displaystyle\frac{f(x+\Delta x)-f(x)}{\Delta x}\to f'(x)$：$x$ 处导数。
- $\displaystyle\frac{f(x+\Delta x)-f(x-\Delta x)}{2\Delta x}\to f'(x)$：中心差分。
- $\displaystyle\lim\frac{f(x)}{g(x)}=\lim\frac{f'(x)}{g'(x)}$：用于 $0/0$ 型的洛必达法则。

## 极大值与极小值

候选位置：$f'(x)=0$、导数不存在处，或端点。

- 极小值判据：$f'(x)=0$ 且 $f''(x)>0$。
- 极大值判据：$f'(x)=0$ 且 $f''(x)<0$。
- 拐点候选条件：$f''(x)=0$，还需检查凹凸性改变。
- 牛顿法：$\displaystyle x_{n+1}=x_n-\frac{f(x_n)}{f'(x_n)}$。
- 迭代 $x_{n+1}=F(x_n)$：若不动点 $x^*=F(x^*)$ 满足 $|F'(x^*)|<1$，在适当邻域内具有吸引性。

二维驻点：$f_x=f_y=0$。在驻点处，

$$
\begin{array}{ll}
\text{极小值：}&f_{xx}>0,\quad f_{xx}f_{yy}>f_{xy}^2;\\
\text{极大值：}&f_{xx}<0,\quad f_{xx}f_{yy}>f_{xy}^2;\\
\text{鞍点：}&f_{xx}f_{yy}<f_{xy}^2.
\end{array}
$$

二维牛顿法求增量：

$$
\begin{cases}
g+g_x\Delta x+g_y\Delta y=0,\\
h+h_x\Delta x+h_y\Delta y=0.
\end{cases}
$$

## 代数

$$
\frac{x/a}{y/b}=\frac{bx}{ay},\qquad x^{-n}=\frac1{x^n},\qquad\sqrt[n]x=x^{1/n},
$$
$$
(x^2)(x^3)=x^5,\qquad(x^2)^3=x^6,\qquad x^2/x^3=x^{-1}.
$$

二次方程与根：

$$
ax^2+bx+c=0\quad\Rightarrow\quad x=\frac{-b\pm\sqrt{b^2-4ac}}{2a},
$$
$$
x^2+2Bx+C=0\quad\Rightarrow\quad x=-B\pm\sqrt{B^2-C}.
$$

配方：

$$
ax^2+bx+c=a\left(x+\frac b{2a}\right)^2+c-\frac{b^2}{4a}.
$$

部分分式：

$$
\frac{cx+d}{(x-a)(x-b)}=\frac A{x-a}+\frac B{x-b}.
$$

常见错误——下列并非一般成立的恒等式：

$$
\frac a{b+c}\ne\frac ab+\frac ac,\qquad\sqrt{x^2+a^2}\ne x+a.
$$

## 微积分基本定理

$$
\frac d{dx}\int_a^xv(t)\,dt=v(x),\qquad
\int_a^b\frac{df}{dx}\,dx=f(b)-f(a).
$$
$$
\frac d{dx}\int_{a(x)}^{b(x)}v(t)\,dt
=v(b(x))b'(x)-v(a(x))a'(x).
$$
$$
\int_0^by(x)\,dx=\lim_{\Delta x\to0}\Delta x[y(\Delta x)+y(2\Delta x)+\cdots+y(b)].
$$

## 圆、直线与平面

$$
x=r\cos\omega t,\qquad y=r\sin\omega t,\qquad\text{速率 }|\omega|r.
$$

直线：$y=mx+b$，或 $y-y_0=m(x-x_0)$。

平面：$ax+by+cz=d$，或 $a(x-x_0)+b(y-y_0)+c(z-z_0)=0$。法向量为 $a\mathbf i+b\mathbf j+c\mathbf k$，平面到原点距离为 $|d|/\sqrt{a^2+b^2+c^2}$。

空间直线：

$$
(x,y,z)=(x_0,y_0,z_0)+t(v_1,v_2,v_3),
\qquad
\frac{x-x_0}{v_1}=\frac{y-y_0}{v_2}=\frac{z-z_0}{v_3}.
$$

投影：

$$
\mathbf p=\frac{\mathbf b\cdot\mathbf a}{\mathbf a\cdot\mathbf a}\mathbf a,
\qquad |\mathbf p|=|\mathbf b|\,|\cos\theta|.
$$

<!-- PDF 13 / 印刷页 无 -->

## 三角恒等式

$$
\begin{aligned}
\sin^2x+\cos^2x&=1,\\
\tan^2x+1&=\sec^2x\quad\text{（除以 $\cos^2x$）},\\
1+\cot^2x&=\csc^2x\quad\text{（除以 $\sin^2x$）},\\
\sin2x&=2\sin x\cos x\quad\text{（倍角）},\\
\cos2x&=\cos^2x-\sin^2x=2\cos^2x-1=1-2\sin^2x,\\
\sin(s\pm t)&=\sin s\cos t\pm\cos s\sin t,\\
\cos(s\pm t)&=\cos s\cos t\mp\sin s\sin t,\\
\tan(s+t)&=\frac{\tan s+\tan t}{1-\tan s\tan t}.
\end{aligned}
$$

余弦定理：$c^2=a^2+b^2-2ab\cos\theta$。正弦定理：$a/\sin A=b/\sin B=c/\sin C$。

$$
a\cos\theta+b\sin\theta=\sqrt{a^2+b^2}\cos\left(\theta-\tan^{-1}\frac ba\right).
$$
$$
\begin{aligned}
\cos(-x)&=\cos x,&\sin(-x)&=-\sin x,\\
\sin(\pi/2\pm x)&=\cos x,&\cos(\pi/2\pm x)&=\mp\sin x,\\
\sin(\pi\pm x)&=\mp\sin x,&\cos(\pi\pm x)&=-\cos x.
\end{aligned}
$$

## 三角积分

$$
\int\sin^2x\,dx=\frac{x-\sin x\cos x}{2}
=\int\frac{1-\cos2x}{2}\,dx=\frac x2-\frac{\sin2x}{4},
$$
$$
\int\cos^2x\,dx=\frac{x+\sin x\cos x}{2}
=\int\frac{1+\cos2x}{2}\,dx=\frac x2+\frac{\sin2x}{4}.
$$
$$
\int\tan^2x\,dx=\tan x-x,\qquad
\int\cot^2x\,dx=-\cot x-x.
$$
$$
\int\sin^nx\,dx=-\frac{\sin^{n-1}x\cos x}{n}+\frac{n-1}{n}\int\sin^{n-2}x\,dx,
$$
$$
\int\cos^nx\,dx=\frac{\cos^{n-1}x\sin x}{n}+\frac{n-1}{n}\int\cos^{n-2}x\,dx,
$$
$$
\int\tan^nx\,dx=\frac{\tan^{n-1}x}{n-1}-\int\tan^{n-2}x\,dx,
$$
$$
\int\sec^nx\,dx=\frac{\sec^{n-2}x\tan x}{n-1}+\frac{n-2}{n-1}\int\sec^{n-2}x\,dx.
$$
$$
\begin{aligned}
\int\tan x\,dx&=-\ln|\cos x|,\\
\int\cot x\,dx&=\ln|\sin x|,\\
\int\sec x\,dx&=\ln|\sec x+\tan x|,\\
\int\csc x\,dx&=\ln|\csc x-\cot x|=-\ln|\csc x+\cot x|,\\
\int\sec^3x\,dx&=\tfrac12\sec x\tan x+\tfrac12\ln|\sec x+\tan x|.
\end{aligned}
$$
$$
\int\sin(px)\sin(qx)\,dx=\frac{\sin((p-q)x)}{2(p-q)}-\frac{\sin((p+q)x)}{2(p+q)},
$$
$$
\int\cos(px)\cos(qx)\,dx=\frac{\sin((p-q)x)}{2(p-q)}+\frac{\sin((p+q)x)}{2(p+q)},
$$
$$
\int\sin(px)\cos(qx)\,dx=-\frac{\cos((p-q)x)}{2(p-q)}-\frac{\cos((p+q)x)}{2(p+q)}.
$$

## 分部积分

$$
\begin{aligned}
\int\ln x\,dx&=x\ln x-x,\\
\int x^n\ln x\,dx&=\frac{x^{n+1}\ln x}{n+1}-\frac{x^{n+1}}{(n+1)^2},\\
\int x^ne^x\,dx&=x^ne^x-n\int x^{n-1}e^x\,dx,\\
\int e^{cx}\sin kx\,dx&=\frac{e^{cx}}{c^2+k^2}(c\sin kx-k\cos kx),\\
\int e^{cx}\cos kx\,dx&=\frac{e^{cx}}{c^2+k^2}(c\cos kx+k\sin kx),\\
\int x\sin x\,dx&=\sin x-x\cos x,\\
\int x\cos x\,dx&=\cos x+x\sin x,\\
\int x^n\sin x\,dx&=-x^n\cos x+n\int x^{n-1}\cos x\,dx,\\
\int x^n\cos x\,dx&=x^n\sin x-n\int x^{n-1}\sin x\,dx,\\
\int\sin^{-1}x\,dx&=x\sin^{-1}x+\sqrt{1-x^2},\\
\int\tan^{-1}x\,dx&=x\tan^{-1}x-\tfrac12\ln(1+x^2).
\end{aligned}
$$

## 含 $x^2,a^2$ 的积分及判别式 $D=b^2-4ac$

$$
\int\frac{dx}{x^2+a^2}=\frac1a\tan^{-1}\frac xa,
\qquad
\int\frac{dx}{a^2-x^2}=\frac1{2a}\ln\left|\frac{x+a}{x-a}\right|=\frac1a\tanh^{-1}\frac xa.
$$
$$
\int\frac{dx}{\sqrt{x^2+a^2}}=\ln|x+\sqrt{x^2+a^2}|,
\qquad
\int\frac{dx}{\sqrt{a^2-x^2}}=\sin^{-1}\frac xa.
$$
$$
\int\sqrt{x^2+a^2}\,dx=\frac x2\sqrt{x^2+a^2}+\frac{a^2}{2}\ln|x+\sqrt{x^2+a^2}|,
$$
$$
\int\sqrt{a^2-x^2}\,dx=\frac x2\sqrt{a^2-x^2}+\frac{a^2}{2}\sin^{-1}\frac xa.
$$
$$
\int\frac{dx}{x\sqrt{x^2-a^2}}=\frac1a\cos^{-1}\frac ax,
\qquad
\int\frac{dx}{x\sqrt{x^2+a^2}}=\frac1a\ln\left|\frac{\sqrt{x^2+a^2}-a}{x}\right|.
$$
$$
\int\frac{dx}{ax^2+bx+c}=
\begin{cases}
\dfrac1{\sqrt D}\ln\left|\dfrac{2ax+b-\sqrt D}{2ax+b+\sqrt D}\right|,&D>0,\\[6pt]
\dfrac2{\sqrt{-D}}\tan^{-1}\dfrac{2ax+b}{\sqrt{-D}},&D<0,\\[6pt]
-\dfrac2{2ax+b},&D=0.
\end{cases}
$$
$$
\int\frac{dx}{\sqrt{ax^2+bx+c}}
=\frac1{\sqrt a}\ln|2ax+b+2\sqrt a\sqrt{ax^2+bx+c}|\quad(a>0),
$$
$$
\int\frac{dx}{\sqrt{ax^2+bx+c}}
=\frac1{\sqrt{-a}}\sin^{-1}\frac{-2ax-b}{\sqrt D}\quad(a<0).
$$

## 定积分

$$
\int_0^\infty x^ne^{-x}\,dx=n!=\Gamma(n+1),\qquad
\int_0^\infty e^{-a^2x^2}\,dx=\frac{\sqrt\pi}{2a},
$$
$$
\int_0^1x^m(1-x)^n\,dx=\frac{m!n!}{(m+n+1)!},
$$
$$
\int_0^\infty\frac{\sin^2x}{x^2}\,dx
=\int_0^\infty\frac{\sin x}{x}\,dx=\frac\pi2.
$$
$$
\int_0^{\pi/2}\sin^nx\,dx=\int_0^{\pi/2}\cos^nx\,dx=
\begin{cases}
\dfrac12\dfrac34\cdots\dfrac{n-1}{n}\dfrac\pi2,&n\text{ 为正偶数},\\[6pt]
\dfrac23\dfrac45\cdots\dfrac{n-1}{n},&n>1\text{ 为奇数}.
\end{cases}
$$

## 译注与待复审事项

- 本表为速查，不替代正文定理条件。极限定义的“任意 $\varepsilon$、存在 $N$ 或 $\delta$”在原表中省略，译文为避免误读补全量词。洛必达、中值定理、基本定理与二阶判别均须满足正文假设。
- 原表把 $f''(x)=0$ 直接列为拐点，已明确为候选条件；它不是充分条件，二阶导数不存在的点也可能为拐点。原圆周速率 $\omega r$ 与投影长度 $|\mathbf b|\cos\theta$ 在一般情形需绝对值，已补。
- 相位公式使用 $\arctan(b/a)$ 时隐含正确象限；一般应选 $\alpha$ 满足 $\cos\alpha=a/\sqrt{a^2+b^2},\sin\alpha=b/\sqrt{a^2+b^2}$，不能对 $a<0$ 无条件取反正切主值。
- 原表最后一个三角积的原函数第二项漏写自变量 $x$，已补为 $\cos((p+q)x)$。$p=\pm q$ 时需另算或取极限。各递推式分母为零的情形不适用。
- 实数积分中常取 $a>0$；$\operatorname{artanh}(x/a)$ 的实分支要求 $|x|<a$。含 $\arccos(a/x)$ 的公式按原式保留，取 $x>a>0$；负半轴须调整分支。二次根式积分须根号内为正；$a<0$ 的反正弦式还要求 $D>0$。
- 阶乘形式取非负整数 $m,n$；高斯积分取 $a>0$。黎曼和默认 $b=N\Delta x$ 的等分，空间直线对称式默认相应 $v_i\ne0$，分量为零时应单列常坐标。
- 初译逐式对照原页，尚未对全部公式进行独立符号验证或最终版式校验。
