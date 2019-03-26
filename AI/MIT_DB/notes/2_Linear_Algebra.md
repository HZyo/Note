# 2. 线性代数

## 2.1 标量、向量、矩阵和张量

张量 （tensor）：高维数组

## 2.2 矩阵和向量相乘

元素对应乘机（element-wise product）或者 **Hadamard乘积** (Hadamard product)，记为 $A \odot B$ 

## 2.3 单位矩阵和逆矩阵

## 2.4 线性相关和生成子空间

## 2.5 范数

**$L^p$ 范数** 

$L^p$ 范数定义如下
$$
||x||_p=(\sum_i{|x_i|^p})^\frac{1}{p}
$$
其中 $p\in\mathbb{R},p\ge 1$ 

$L^2$ 称为欧几里得范数，简化表示为 $||x||$ 和 $\mathbf{x}^T\mathbf{x}$ 

$L^\infty$ 范数，最大范数，$||\mathbf{x}||_\infty=\max\limits_i|x_i|$ 



**范数** 

范数是满足下列性质的任意函数

- $f(\mathbf{x})=0\Rightarrow\mathbf{x}=\mathbf{0}$ 
- $f(\mathbf{x}+\mathbf{y})\le f(\mathbf{x})+f(\mathbf{y})$ 
- $\forall \alpha\in\mathbb{R},f(\alpha\mathbf{x})=|\alpha|f(\mathbf{x})$ 



**Frobenius 范数** 

衡量矩阵大小的范数
$$
||\mathbf{A}||_F=\sqrt{\sum_{i,j}A^2_{i,j}}
$$
**点积** 
$$
\mathbf{x}^T\mathbf{y}=||\mathbf{x}||_2||\mathbf{y}||_2\cos\theta
$$

## 2.6 特殊类型的矩阵和向量

**正交矩阵** 
$$
\mathbf{A}^T\mathbf{A}=\mathbf{A}\mathbf{A}^T=\mathbf{I}\\
\mathbf{A}^{-1}=\mathbf{A}^T
$$

## 2.7 特征分解

每个实对称矩阵都可以分解成实特征向量和实特征值 
$$
A=Q\Lambda Q^T
$$
其中 Q 是 A 的特征向量组成的正交矩阵， Λ 是对角矩阵。 

特征值 $Λ_{i,i}$ 对应的特征向量是矩阵 Q 的第 i 列，记作 $Q_{:,i}$。因为 Q 是正交矩阵，我们可以将 A 看作沿方向 $v^{(i)}$ 延展 $λ_i$ 倍的空间。 

![1547096540844](assets/1547096540844.jpg)

## 2.8 奇异值分解

$$
A=UDV^T
$$

U，V 是正交矩阵

U的列向量为左奇异向量，是 $AA^T​$ 的特征向量

V的列向量为右奇异向量，是 $A^TA$ 的特征向量

## 2.9 Moore-Penrose 伪逆

$$
A^+=VD^+U^T
$$

$D^+​$ 是其非零元素取倒数之后再转置得到的

当矩阵 A 的列数多于行数时，使用伪逆求解线性方程是众多可能解法中的一种。特别地， $x = A^+y$ 是方程所有可行解中欧几里得范数 $||\mathbf{x}||_2​$ 最小的一个。 

当矩阵 A 的行数多于列数时，可能没有解。在这种情况下，通过伪逆得到的 x 使得 Ax 和 y 的欧几里得距离 $∥Ax - y∥_2​$ 最小。 

## 2.10 迹运算

$$
||A||_F=\sqrt{\text{Tr}(AA^T)}
$$

$$
\text{Tr}(ABC)=\text{Tr(CAB)}
$$

## 2.11 行列式

## 2.12 主成分分析

有损压缩
$$
\{\mathbf{x}^{(1)},...,\mathbf{x}^{(m)}\}\\
f(\mathbf{x})=\mathbf{c}\\
x\approx g(\mathbf{c})\\
g(\mathbf{c})=D\mathbf{c}\\
$$
f(x) 是编码器，g(x) 是解码器

为了简化才让 $g(\mathbf{c}) = D\mathbf{c}$ 

为了唯一解，D 的列向量都有单位范数

为了更简单，D 的列向量彼此正交

最优编码为
$$
\begin{aligned}
c^*
&=\arg\min\limits_{\mathbf{c}}||\mathbf{x}-g(\mathbf{c})||^2_2\\
&=\arg\min\limits_{\mathbf{c}}\ 
(\mathbf{x}-g(\mathbf{c})^T)(\mathbf{x}-g(\mathbf{c}))\\
&=\arg\min\limits_{\mathbf{c}}\ 
\mathbf{x}^T\mathbf{x}-2\mathbf{x}^Tg(\mathbf{c})+g(\mathbf{c})^Tg(\mathbf{c})\\
&=\arg\min\limits_{\mathbf{c}}\ 
-2\mathbf{x}^Tg(\mathbf{c})+g(\mathbf{c})^Tg(\mathbf{c})\\
&=\arg\min\limits_{\mathbf{c}}\ 
-2\mathbf{x}^TD\mathbf{c}+\mathbf{c}^TD^TD\mathbf{c}\\
&=\arg\min\limits_{\mathbf{c}}\ 
-2\mathbf{x}^TD\mathbf{c}+\mathbf{c}^T\mathbf{c}\\
\end{aligned}
$$
用向量微积分求解这个最优化问题
$$
\begin{aligned}
\nabla_\mathbf{c}(-2\mathbf{x}^TD\mathbf{c}+\mathbf{c}^T\mathbf{c})&=0\\
-2D^T\mathbf{x}+2\mathbf{c}&=0\\
\mathbf{c}&=D^T\mathbf{x}
\end{aligned}
$$
故有
$$
r(\mathbf{x})=g(f(\mathbf{x}))=DD^T\mathbf{x}
$$
需要挑选 D
$$
D^*=\arg\min\limits_D\sqrt{\sum_{i,j}(\mathbf{x}_j^{(i)}-r(\mathbf{x}^{(i)})_j)}\ \text{subject to }D^TD=I
$$
考虑 D 为单一向量 $\mathbf{d}$ 
$$
\mathbf{d}^*=\arg\min\limits_\mathbf{d}\sqrt{\sum_{i}(\mathbf{x}^{(i)}-\mathbf{x}^{(i)}\mathbf{d}\mathbf{d}^T)}\ \text{subject to }\mathbf{d}^T\mathbf{d}=1
$$
将各点向量 $\{\mathbf{x}^{(1)},...,\mathbf{x}^{(m)}\}$ 堆叠成一个矩阵 $X$ 
$$
\begin{aligned}
\mathbf{d}^*
&=\arg\min\limits_\mathbf{d}||X-X\mathbf{d}\mathbf{d}^T||^2_F\ 
\text{subject to }\mathbf{d}^T\mathbf{d}=1\\
&=arg\min\limits_\mathbf{d}\ \text{Tr}((X-X\mathbf{d}\mathbf{d}^T)^T(X-X\mathbf{d}\mathbf{d}^T))\\
&=arg\min\limits_\mathbf{d}\ -2\text{Tr}(X^TX\mathbf{d}\mathbf{d}^T)+\text{Tr}(\mathbf{d}\mathbf{d}^TX^TX\mathbf{d}\mathbf{d}^T)\\
&=arg\min\limits_\mathbf{d}\ -2\text{Tr}(X^TX\mathbf{d}\mathbf{d}^T)+\text{Tr}(X^TX\mathbf{d}\mathbf{d}^T\mathbf{d}\mathbf{d}^T)\\
&=arg\min\limits_\mathbf{d}\ -\text{Tr}(X^TX\mathbf{d}\mathbf{d}^T)\\
&=arg\max\limits_\mathbf{d}\ \text{Tr}(\mathbf{d}^TX^TX\mathbf{d})\\
\end{aligned}
$$
这个优化问题可以通过特征分解来求解。具体来讲，最优的 $\mathbf{d}$ 是 $X^TX$ 最大特征值对应的特征向量。 

以上推导特定于矩阵 D 为单列向量的情况，仅得到了第一个主成分。更一般地，当我们希望得到主成分的基时，矩阵 D 由前 $l​$ 个最大的特征值对应的特征向量组成。这个结论可以通过归纳法证明。

> 这里表达下我个人理解的关于PCA的几何描述
>
> 先对数据进行预处理，使其均值为0
>
> 对于一个维度来说，数据在一个以原点为中心的对称区间内
>
> 对于两个维度来说，数据在一个以原点为中心的椭圆区域内
>
> 对于三个维度来说，数据在一个以原点为中心的椭球区域内
>
> 如果某一维度的区间大小比较小，那么在高维视角里，数据的区域在那一个的维度比较扁。
>
> 为了压缩数据，我们应该尽量保留那些区间比较大的维度，舍弃那些区间比较小的维度。
>
> 而区间的大小就取决于特征值的大小

## 2.13 矩阵求导

### 2.13.1 求导

**标量求导** 

设$y$ 为一个元素，$\mathbf{x}^T=[x_1...x_n]$ 是$n$ 维行向量，则：
$$
\frac{\part y}{\part \mathbf{x}^T}=\Big[\frac{\part y}{\part x_1}...\frac{\part y}{\part x_n}\Big]
$$
**向量求导** 

设$\mathbf{y}^T=[y_1...y_n]$ 是 $n$ 维行向量，$\mathbf{x}=[x_1...x_m]$ 是$m​$ 维列向量，则
$$
\begin{align}
\frac{\part \mathbf{y}^T}{\part \mathbf{x}}
&=\Big[\frac{\part y_1}{\part \mathbf{x}}...\frac{\part y_n}{\part \mathbf{x}}\Big]\\
&=
\begin
{bmatrix}
\frac{\part y_1}{\part x_1}&...&\frac{\part y_n}{\part x_1}\\
...&...&...\\
\frac{\part y_1}{\part x_m}&...&\frac{\part y_n}{\part x_m}\\
\end
{bmatrix}
\end{align}
$$
**矩阵求导** 

设$Y$ 是 $m\times n$ 的矩阵，$\mathbf{x}=[x_1...x_p]$ 是$p$ 维列向量
$$
\frac{\part Y}{\part \mathbf{x}}=\Big[\frac{\part Y}{\part x_1}...\frac{\part Y}{\part x_n}\Big]
$$

### 2.13.2 常见性质

$$
\begin{align}
\frac{\part(A\mathbf{x})}{\part \mathbf{x}^T}&=A\\
\frac{\part(\mathbf{x}^T A\mathbf{x})}{\part \mathbf{x}}&=A\mathbf{x}+A^T\mathbf{x}\\
\frac{\part(\mathbf{x}^T \mathbf{x})}{\part \mathbf{x}}&=2\mathbf{x}\\
\frac{\part(\mathbf{a}^T\mathbf{x})}{\part \mathbf{x}}&=\mathbf{a}\\
\frac{\part(\mathbf{x}^T A\mathbf{y})}{\part \mathbf{x}}&=A\mathbf{y}\\
\frac{\part(\mathbf{x}^T A\mathbf{y})}{\part A}&=\mathbf{x}\mathbf{y}^T\\
\end{align}
$$

