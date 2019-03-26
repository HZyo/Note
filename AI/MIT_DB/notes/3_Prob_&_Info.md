# 3. 概率与信息论

## 3.1 为什么要使用概率

## 3.2 随机变量

## 3.3 概率分布

### 3.3.1 离散型变量和概率质量函数

### 3.3.2 连续性变量和概率密度函数

## 3.4 边缘概率

## 3.5 条件概率

## 3.6 条件概率的链式法则

$$
P(X^{(1)},...,X^{(n)}) = P(X^{(1)})\prod^n_{i=2}P(X^{(i)}|X^{(1)},...,X^{(i−1)})
$$

## 3.7 独立性和条件独立性

**相互独立** 
$$
\forall x \in X, y \in Y, p(X = x, Y = y) = p(X = x)p(Y = y)
$$
简化表示为$X\perp Y$ 

**条件独立** 
$$
\forall x \in X, y \in Y, z\in Z, p(X = x, Y = y|Z=z) = p(X = x|Z=z)p(Y = y|Z=z)
$$
简化表示为 $X\perp Y\ |\ Z$ 

## 3.8 期望、方差和协方差

**协方差** 
$$
\text{Cov}(f(x),g(y))=E[(f(x)-E[f(x)])(g(y)-E[g(y)])]
$$
**协方差矩阵** 
$$
\text{Cov}(\mathbf{x})_{i,j}=\text{Cov}(\mathbf{x}_i,\mathbf{x}_j)
$$
协方差矩阵的对角元是方差 

## 3.9 常用概率分布

### 3.9.1 Bernoulli 分布

Bernoulli 分布（ Bernoulli distribution）是单个二值随机变量的分布。它由单个参数 $ϕ \in [0, 1]$ 控制， ϕ 给出了随机变量等于 1 的概率。 
$$
\begin{align}
P(X=1)&=\phi\\
P(X=0)&=1-\phi\\
P(X=x)&=\phi^x(1-\phi)^{1-x}\\
E_X[X&]=\phi\\
\text{Var}_X(X)&=\phi(1-\phi)\\
\end{align}
$$

### 3.9.2 Multinoulli 分布

Multinoulli 分布（ multinoulli distribution）或者 范畴分布（ categorical distribution）是指在具有 k 个不同状态的单个离散型随机变量上的分布，其中 k 是一个有限值。

Multinoulli 分布由向量 $\mathbf{p} \in [0, 1]^{k-1}$ 参数化，其中每一个分量 $p_i$ 表示第 i 个状态的概率。最后的第 k 个状态的概率可以通过 $1 - \mathbf{1}^⊤\mathbf{p}$ 给出。注意我们必须限制 $\mathbf{1}^⊤\mathbf{p} ≤ 1$。

### 3.9.3 高斯分布

**正态分布（高斯分布）** 
$$
\mathcal{N}(x;\mu,\sigma^2)=\sqrt{\frac{1}{2\pi\sigma^2}}\exp(-\frac{1}{2\sigma^2}(x-\mu)^2)
$$
一种更高效的参数化分布的方式是使用参数 $\beta\in(0,\infty)$，来控制分布的精度（或方差的倒数）
$$
\mathcal{N}(x;\mu,\beta^{-1})=\sqrt{\frac{\beta}{2\pi}}\exp(-\frac{\beta}{2}(x-\mu)^2)
$$
采用正态分布在很多应用中都是一个明智的选择。当我们由于缺乏关于某个实数上分布的先验知识而不知道该选择怎样的形式时，正态分布是默认的比较好的选择，其中有两个原因：

- 第一，我们想要建模的很多分布的真实情况是比较接近正态分布的。 **中心极限定理**（ central limit theorem）说明很多独立随机变量的和近似服从正态分布。 
- 第二，在具有相同方差的所有可能的概率分布中，正态分布在实数上具有最大的不确定性。 

**多维正态分布** 
$$
\mathcal{N}(\mathbf{x};\pmb\mu,\pmb\Sigma)=\sqrt{\frac{1}{(2\pi)^n|\pmb\Sigma|}}\exp(-\frac{1}{2}(\mathbf{x}-\pmb\mu)^T\pmb\Sigma^{-1}(\mathbf{x}-\pmb\mu))
$$
一种更高效的参数化分布的方式是使用**精度矩阵** $\pmb\beta$
$$
\mathcal{N}(\mathbf{x};\pmb\mu,\pmb\beta)=\sqrt{\frac{|\pmb\beta|}{(2\pi)^n}}\exp(-\frac{1}{2}(\mathbf{x}-\pmb\mu)^T\pmb\beta(\mathbf{x}-\pmb\mu))
$$
我们常常把协方差矩阵固定成一个对角阵。一个更简单的版本是 各向同性（ isotropic）高斯分布，它的协方差矩阵是一个标量乘以单位阵。 

### 3.9.4 指数分布和Laplace分布

**指数分布** 
$$
p(x;\lambda)=\lambda\mathbf{1}_{x\ge0}\exp(-\lambda x)
$$

> $\mathbf{1}_{x\ge0}$ 是指示函数(indicator function)

**Laplace分布** 
$$
\text{Laplace}(x;\mu,\gamma)=\frac{1}{2\gamma}\exp(-\frac{|x-\mu|}{\gamma})
$$
峰值在 $\mu$ 处

### 3.9.5 Dirac分布和经验分布

**Dirac分布** 
$$
p(x)=\delta(x-\mu)
$$
**经验分布** 
$$
\hat{p}(\mathbf{x})=\frac{1}{m}\sum_{i=1}^m\delta(\mathbf{x}-\mathbf{x}^{(i)})
$$

### 3.9.6 分布的混合

$$
P(X)=\sum_iP(c=i)P(X|c=i)
$$

## 3.10 常用函数的有用性质

**logistic sigmoid** 
$$
\sigma(x)=\frac{1}{1+e^{-x}}
$$
![sigmoid](assets/1546961695832.jpg)

**softplus** 
$$
\zeta(x)=\log(1+e^x)
$$
![softplus](assets/1546961921975.jpg)

名称来源于 $x^+=\max(0,x)$ 的软化

**性质** 
$$
\begin{align}
\frac{d}{dx}\sigma(x)&=\sigma(x)(1-\sigma(x))\\
\frac{d}{dx}\zeta(x)&=\sigma(x)\\
\end{align}
$$

## 3.11 贝叶斯规则

$$
P(X|Y)=\frac{P(X)P(Y|X)}{P(Y)}
$$

> $P(Y)$ 通常使用$P(Y)=\sum_xP(Y|x)P(x)$ 来计算 ，故不需要事先知道$P(Y)$ 的信息

## 3.12 连续性变量的技术细节

**测度论** 

**函数关系** 
$$
\begin{align}
\mathbf{y}&=g(\mathbf{x})\\
|p_y(g(x))dy|&=|p_x(x)dx|\\
p_x(x)&=p_y(g(x))\Big|\frac{\part g(x)}{\part x}\Big|\\
p_x(\mathbf{x})&=p_y(g(\mathbf{x}))\Big|\text{det}\Big(\frac{\part g(\mathbf{x})}{\part \mathbf{x}}\Big)\Big|\\
\end{align}
$$
其中 $g(\mathbf{x})$ 可逆、连续可微

## 3.13 信息论

信息论的基本想法是一个不太可能的事件居然发生了，要比一个非常可能的事件发生，能提供更多的信息。 

> 消息说： ‘‘今天早上太阳升起’’ 信息量是如此之少以至于没有必要发送
>
> 但一条消息说： ‘‘今天早上有日食’’ 信息量就很丰富。 



**自信息** 

性质

- 非常可能发生的事件信息量要比较少，并且极端情况下，确保能够发生的事件
  应该没有信息量。

- 较不可能发生的事件具有更高的信息量。

- 独立事件应具有增量的信息。

  > 例如，投掷的硬币两次正面朝上传递的信息量，应该是投掷一次硬币正面朝上的信息量的两倍。 

定义事件 $X=x$ 的自信息为
$$
I(x)=-\log(P(x))\ [\text{nats}]
$$

> 上式底数为 e，当底数为2时，单位为 比特或香农

![-log](assets/1547008966728.jpg)

**香农熵** 

用 香农熵（ Shannon entropy）来对整个概率分布中的不确定性总量进行量化： 
$$
H(X)=E_{X\sim P}[I(x)]=-E_{X\sim P}[\log P(x)]
$$
也记作 $H(P)$ 

> 那些接近确定性的分布 (输出几乎可以确定) 具有较低的熵；那些接近均匀分布的概率分布具有较高的熵。 

**KL散度** 

如果我们对于同一个随机变量 x 有两个单独的概率分布 P(x) 和 Q(x)，我们可以使用 KL 散度（ Kullback-Leibler (KL) divergence）来衡量这两个分布的差异 
$$
D_{KL}(P||Q)=E_{X\sim P}\Big[\log\frac{P(x)}{Q(x)}\Big]
$$

> 非负，相同分布时为0
>
> 非对称

**交叉熵** 
$$
H(P,Q)=-E_{X\sim P}[\log Q(x)]
$$

## 3.14 结构化概率模型

**有向** 

用条件概率分布来表示分解 

有向模型对于分布中的每一个随机变量 $x_i$ 都包含着一个影响因子，这个组成 $x_i$ 条件概率的影响因子被称为 $x_i$ 的父节点，记为 $Pa_\mathcal{G}(x_i)$ 
$$
P(\mathbf{x})=\prod p(x_i|Pa_\mathcal{G}(x_i))
$$

> 示例
>
> ![1547012187614](assets/1547012187614.jpg)
>
> $$
> p(a,b,c,d,e)=p(a)p(b|a)p(c|a,b)p(d|b)p(e|c)
> $$
>

**无向** 

$\mathcal{G}$ 中任何满足两两之间有边连接的顶点的集合被称为团。 无向模型中的每个团 $C^{(i)}$ 都伴随着一个因子
$ϕ^{(i)}(C^{(i)})$。这些因子仅仅是函数，并不是概率分布。 每个因子的输出都必须是非负的，但是并没有像概率分布中那样要求因子的和或者积分为 1。 

随机变量的联合概率与所有这些因子的乘积 成比例（ proportional）——意味着因子的值越大则可能性越大。当然，不能保证这种乘积的求和为 1。所以我们需要除以一个归一化常数 Z 来得到归一化的概率分布，归一化常数 Z 被定义为 ϕ 函数乘积的所有状态的求和或积分。概率分布为： 
$$
p(\mathbf{x})=\frac{1}{Z}\prod_i\phi^{(i)}(C^{(i)})
$$

> 示例
>
> ![1547012548481](assets/1547012548481.jpg)
> $$
> p(a,b,c,d,e)=\frac{1}{Z}\phi^{(1)}(a,b,c)\phi^{(2)}(b,d)\phi^{(3)}(c,e)
> $$
>

