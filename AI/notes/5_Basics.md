# 5. 机器学习基础

## 5.1 学习算法

对于某类任务 T 和性能度量 P，一个计算机程序被认为可以从经验 E 中学习是指，通过经验 E 改进后，它在任务 T 上由性能度量 P 衡量的性能有所提升。

### 5.1.1 任务 T

**样本**是指我们从某些希望机器学习系统处理的对象或事件中收集到的已经量化的 **特征**（ feature）的集合 

任务举例：分类、输入缺失分类、回归、转录、机器翻译、结构化输出、异常检测、合成和采样、缺失值填补、去噪、密度估计或概率质量函数估计

### 5.1.2 性能度量 P

准确率、错误率、测试集

### 5.1.3 经验 E

**无监督学习算法** 

训练含有很多特征的数据集，然后学习出这个数据集上有用的结构性质。 

观察随机向量 x 的好几个样本，试图显式或隐式地学习出概率分布 p(x)，或者是该分布一些有意思的性质 

**监督学习算法** 

训练含有很多特征的数据集，不过数据集中的样本都有一个 标签（ label）或 目标（ target）。 

观察随机向量 x 及其相关联的值或向量 y，然后从 x 预测 y，通常是估计 $p(\mathbf{y} | \mathbf{x})$。 

**界线** 

概率的链式法则表明对于向量 $\mathbf{x} \in \mathbb{R}^n$，联合分布可以分解成
$$
p(\mathbf{x})=\prod_{i=1}^n p(x_i|x_1,...,x_{i-1})
$$
该分解意味着我们可以将其拆分成 n 个监督学习问题，来解决表面上的无监督学习p(x)。 

另外，我们求解监督学习问题 $p(\mathbf{y} | \mathbf{x})$ 时，也可以使用传统的无监督学习策略学习联合分布 $p(\mathbf{x}, \mathbf{y})$，然后推断
$$
p(y|\mathbf{x})=\frac{p(\mathbf{x},y)}{\sum_{y'}p(\mathbf{x},y')}
$$

### 5.1.4 示例：线性回归

$$
\begin{align}
\hat{y}&=\mathbf{w}^T\mathbf{x}\\

\text{MSE}_\text{test}&=\frac{1}{m}||\hat{\mathbf{y}}^{(\text{test})}-\mathbf{y}^{(\text{test})}||_2^2\\

\nabla_\mathbf{w}\text{MSE}_\text{train}
&=\nabla_\mathbf{w}||\hat{\mathbf{y}}^{(\text{train})}-\mathbf{y}^{(\text{train})}||_2^2\\
&=\nabla_\mathbf{w}||X^{(\text{train})}\mathbf{w}-\mathbf{y}^{(\text{train})}||_2^2\\
&=\nabla_\mathbf{w}(X^{(\text{train})}\mathbf{w}-\mathbf{y}^{(\text{train})})^T
	(X^{(\text{train})}\mathbf{w}-\mathbf{y}^{(\text{train})})\\
&=\nabla_\mathbf{w}
	(\mathbf{w}^T X^{(\text{train})T} X^{(\text{train})}\mathbf{w}
	-2\mathbf{w}^T X^{(\text{train})T} \mathbf{y}^{(\text{train})}
	+\mathbf{y}^{(\text{train})T}\mathbf{y}^{(\text{train})})\\
&=2 X^{(\text{train})T} X^{(\text{train})}\mathbf{w} - 2 X^{(\text{train})T} \mathbf{y}^{(\text{train})}\\
\mathbf{w}&=(X^{(\text{train})T} X^{(\text{train})})^{-1}X^{(\text{train})T}\mathbf{y}^{(\text{train})}
\end{align}
$$

> 值得注意的是，术语 线性回归（ linear regression）通常用来指稍微复杂一些，附加额外参数（截距项 b）的模型。在这个模型中， 
> $$
> \hat{y}=\mathbf{w}^T\mathbf{x}+b
> $$
> 因此从参数到预测的映射仍是一个线性函数，而从特征到预测的映射是一个仿射函数。如此扩展到仿射函数意味着模型预测的曲线仍然看起来像是一条直线，只是这条直线没必要经过原点。除了通过添加偏置参数 b，我们还可以使用仅含权重的模型，但是 x 需要增加一项永远为 1 的元素。对应于额外 1 的权重起到了偏置参数的作用。当我们在本书中提到仿射函数时，我们会经常使用术语 ‘‘线性’’。 

## 5.2 容量、过拟合和欠拟合

欠拟合是指模型不能在训练集上获得足够低的误差。

过拟合是指训练误差和和测试误差之间的差距太大。 

通过调整模型的 容量（ capacity），我们可以控制模型是否偏向于过拟合或者欠拟合。 

统计学习理论中最重要的结论阐述了训练误差和泛化误差之间差异的上界随着模型容量增长而增长，但随着训练样本增多而下降。

我们必须记住虽然更简单的函数更可能泛化（训练误差和测试误差的差距小），但我们仍然需要选择一个充分复杂的假设以达到低的训练误差。通常，当模型容量上升时，训练误差会下降，直到其渐近最小可能误差（假设误差度量有最小值）。通常，泛化误差是一个关于模型容量的 U 形曲线函数。 

![1547029098290](assets/1547029098290.jpg)

### 5.2.1 没有免费午餐定理

没有免费午餐定理表明，在所有可能的数据生成分布上平均之后，每一个分类算法在未事先观测的点上都有相同的错误率。 

幸运的是，这些结论仅在我们考虑所有可能的数据生成分布时才成立。在真实世界应用中，如果我们对遇到的概率分布进行假设的话，那么我们可以设计在这些分布上效果良好的学习算法。 

### 5.2.2 正则化

更一般地，正则化一个学习函数 $f(\mathbf{x}; \pmb θ)$ 的模型，我们可以给代价函数添加被称为 正则化项（ regularizer）的惩罚。 如权重衰减
$$
J(\mathbf{w})=\text{MSE}_{\text{train}}+\lambda\mathbf{w}^T\mathbf{w}
$$

## 5.3 超参数和验证集

有时一个选项被设为学习算法不用学习的超参数，是因为它太难优化了。更多的情况是，该选项必须是超参数，因为它不适合在训练集上学习。这适用于控制模型容量的所有超参数。如果在训练集上学习超参数，这些超参数总是趋向于最大可能的模型容量，导致过拟合。

为了解决这个问题，我们需要一个训练算法观测不到的 验证集（ validation set）样本。 测试样本不能以任何形式参与到模型的选择中，包括设定超参数。 基于这个原因，测试集中的样本不能用于验证集。因此，我们总是从训练数据中构建验证集。 

### 5.3.1 交叉验证

![1547032447842](assets/1547032447842.jpg)

## 5.4 估计、偏差和方差

### 5.4.1 点估计

$$
\hat{\theta}_m=g(\mathbf{x}^{(1)},...，\mathbf{x}^{(m)})
$$

### 5.4.2 偏差

$$
\text{bias}(\hat{\pmb\theta}_m)=\mathbb{E}(\hat{\pmb\theta}_m)-\pmb\theta
$$

如果 $\text{bias}(\hat{\pmb θ}^m) = 0$，那么估计量 $\hat{\pmb θ}^m$ 被称为是 无偏（ unbiased），这意味着 $\mathbb{E}(\hat{\pmb θ}^m) = \pmb θ$ 

如果 $\lim\limits_{m\to\infty}\text{bias}(\hat{\pmb θ}^m) = 0$，那么估计量 $\hat{\pmb θ}^m$ 被称为是渐进无偏（ asymptotically unbiased），这意味着 $\lim\limits_{m\to\infty}\mathbb{E}(\hat{\pmb θ}^m) = \pmb θ$ 

### 5.4.3 方差和标准差

估计量的方差
$$
\text{Var}(\hat{\theta})
$$
标准差
$$
\text{SE}(\hat{\theta})
$$
均值的标准差
$$
\text{SE}(\hat{\mu}_m)=\sqrt{\text{Var}\Big[\frac{1}{m}\sum_{i=1}^mx^{(i)}\Big]}=\frac{\sigma}{\sqrt m}
$$
以均值 $\hat{µ}^m$ 为中心的 95% 置信区间是 
$$
(\hat{\mu}_m-1.96\text{SE}(\hat{\mu}_m),
\hat{\mu}_m+1.96\text{SE}(\hat{\mu}_m))
$$
在机器学习实验中，我们通常说算法 A 比算法 B 好，是指算法 A 的误差的 95% 置信区间的上界小于算法 B
的误差的 95% 置信区间的下界。 

### 5.4.4 权衡偏差和方差以最小化均方误差

均方误差
$$
\begin{align}
\text{MSE}
&=\mathbb{E}[(\hat{\theta}_m-\theta)^2]\\
&=\text{Bias}(\hat\theta_m)^2+\text{Var}(\hat{\theta}_m)
\end{align}
$$
偏差和方差的关系和机器学习容量、欠拟合和过拟合的概念紧密相联。用MSE 度量泛化误差（偏差和方差对于泛化误差都是有意义的）时，增加容量会增加方差，降低偏差。

![1547034314147](assets/1547034314147.jpg)

### 5.4.5 一致性

$$
\text{plim}_{m\to\infty}\hat{\theta}_m=\theta
$$

plim表示依概率收敛，即对于任意的 ϵ > 0，当 $m\to\infty$ 时，有 $P(|\hat{θ}_m - θ| >ϵ) \to 0$。 

几乎必然收敛指当$p(\lim_{m\to\infty}\mathbf{x}^{(m)}=\mathbf{x})=1$ ，随机变量序列$\mathbf{x}^{(1)},\mathbf{x}^{(2)},...$ 收敛到$\mathbf{x}$ 

## 5.5 最大似然估计

考虑一组含有 m 个样本的数据集 $\mathbb{X} = \{\mathbf{x}^{(1)},...,\mathbf{x}^{(m)}\}$，独立地由未知的真实数据生成分布 $p_\text{data}(\mathbf{x})$ 生成。 

令 $p_\text{model}(\mathbf{x}; \pmb θ)$ 是一族由 θ 确定在相同空间上的概率分布。换言之， $p_\text{model}(\mathbf{x}; \pmb θ)$将任意输入 x 映射到实数来估计真实概率 $p_\text{data}(\mathbf{x})$。 

对 θ 的最大似然估计被定义为： 
$$
\begin{align}
\pmb\theta_\text{ML}
&=\arg\max\limits_{\pmb\theta}p_\text{model}(\mathbb{X};\pmb\theta)\\
&=\arg\max\limits_{\pmb\theta}\prod_{i=1}^m p_\text{model}(\mathbf{x}^{(i)};\pmb\theta)\\
&=\arg\max\limits_{\pmb\theta}\sum_{i=1}^m\log p_\text{model}(\mathbf{x}^{(i)};\pmb\theta)\\
&=\arg\max\limits_{\pmb\theta}\mathbb{E}_{\mathbf{x}\sim \hat{p}_\text{data}}\log p_\text{model}(\mathbf{x};\pmb\theta)\\
\end{align}\\
$$

> $\hat{p}_\text{data}(\mathbf{x})=\frac{\#\{\mathbf{x}=\mathbb{X}\}}{m}$ 
>
> 一种解释最大似然估计的观点是将它看作最小化训练集上的经验分布 $\hat{p}_\text{data}$ 和模型分布之间的差异，用KL散度度量，定义如下
> $$
> D_{KL}(\hat{p}_\text{data}||p_\text{model})=\mathbb{E}_{\mathbf{x}\sim\hat{p}_\text{data}}[\log\hat{p}_\text{data}(\mathbf{x})-\log p_\text{model}(\mathbf{x})]\\
> \arg\min\limits_{\pmb\theta}D_{KL}(\hat{p}_\text{data}||p_\text{model})=\arg\max\limits_{\pmb\theta}\mathbb{E}_{\mathbf{x}\sim \hat{p}_\text{data}}\log p_\text{model}(\mathbf{x};\pmb\theta)
> $$
>

### 5.5.1 条件对数似然和均方误差

$$
\begin{align}
\pmb\theta_\text{ML}
&=\arg\max\limits_{\pmb\theta}p(Y|X;\pmb\theta)\\
&=\arg\max\limits_{\pmb\theta}\sum_{i=1}^m \log p(\mathbf{y}^{(i)}|\mathbf{x}^{(i)};\pmb\theta)
\end{align}
$$

**示例：线性回归作为最大似然** 
$$
p(y|\mathbf{x})=\mathcal{N}(y;\hat{y}(\mathbf{x};\mathbf{w}),\sigma^2)\\
\sum_{i=1}^m\log p(y^{(i)}|\mathbf{x}^{(i)};\mathbf{w})
=-m\log\sigma-\frac{m}{2}\log(2\pi)-\sum_{i=1}^m\frac{(\hat{y}^{(i)}-y^{(i)})^2}{2\sigma^2}\\
\text{MSE}_\text{train}=\frac{1}{m}\sum_{i=1}^m(\hat{y}^{(i)}-y^{(i)})^2
$$
可以看出最大化关于 w 的对数似然和最小化均方误差会得到相同的参数估计 w。 这验证了 MSE 可以用于最大似然估计。 

### 5.5.2 最大似然的性质

在合适的条件下，最大似然估计具有一致性，意味着训练样本数目趋向于无穷大时，参数的最大似然估计会收敛到参数的真实值。这些条件是 ：

- 真实分布$p_\text{data}$ 必须在模型族 $p_\text{model}(\cdot;\pmb\theta)$ 中。否则，没有估计可以还原$p_\text{data}$ 
- 真实分布 $p_\text{data}$ 必须刚好对应一个 θ 值。否则，最大似然估计恢复出真实分布$p_\text{data}$ 后，也不能决定数据生成过程使用哪个 θ。 

## 5.6 贝叶斯统计

在观察到数据前，我们将 θ 的已知知识表示成 先验概率分布（ prior probabilitydistribution）， p(θ)（有时简单地称为 ‘‘先验’’）。一般而言，机器学习实践者会选择一个相当宽泛的（即，高熵的）先验分布，反映在观测到任何数据前参数 θ 的高度不确定性。 

现在假设我们有一组数据样本 $\{x^{(1)},...,x^{(m)}\}$。通过贝叶斯规则结合数据似然$p(x^{(1)},...,x^{(m)}| \pmb\theta)$ 和先验，我们可以恢复数据对我们关于 θ 信念的影响： 
$$
p(\pmb\theta|x^{(1)},...,x^{(m)})=\frac{p(x^{(1)},...,x^{(m)}|\pmb\theta)p(\pmb\theta)}{p(x^{(1)},...,x^{(m)})}
$$
相对于最大似然估计，贝叶斯估计有两个重要区别。

第一，不像最大似然方法预测时使用 θ 的点估计，贝叶斯方法使用 θ 的全分布。例如，在观测到 m 个样本后，下一个数据样本 $x^{(m+1)}$ 的预测分布如下： 
$$
p(x^{(m+1)}| x^{(1)},...,x^{(m)}) = \int p(x^{(m+1)}|\pmb\theta)p(\pmb\theta|x^{(1)},...,x^{(m)})\ d\pmbθ
$$
第二个最大区别是由贝叶斯先验分布造成的。 先验能够影响概率质量密度朝参数空间中偏好先验的区域偏移。实践中，先验通常表现为偏好更简单或更光滑的模型。对贝叶斯方法的批判认为先验是人为主观判断影响预测的来源。 

**示例：贝叶斯线性回归** 

记 $\mathbf{y}^{(\text{train})}$ 为$\mathbf{y}$，$X^{(\text{train})}$ 为$X$ ，$\mathbf{y}$ 表示为高斯条件分布，有
$$
\begin{align}
p(\mathbf{y}|X,\mathbf{w})
&= \mathcal{N}(\mathbf{y};X\mathbf{w},I)\\
&\varpropto \exp\Big(-\frac{1}{2}(\mathbf{y}-X\mathbf{w})^T(\mathbf{y}-X\mathbf{w})\Big)
\end{align}
$$
使用高斯作为先验分布
$$
\begin{align}
p(\mathbf{w})
&= \mathcal{N}(\mathbf{w};\pmb\mu_0,\pmb\Lambda_0)\\
&\varpropto \exp\Big(-\frac{1}{2}(\mathbf{w}-\pmb\mu_0)^T\pmb\Lambda_0^{-1}(\mathbf{w}-\pmb\mu_0)\Big)
\end{align}
$$
后验分布
$$
\begin{align}
p(\mathbf{w}|X,\mathbf{y})
&\varpropto p(\mathbf{y}|X,\mathbf{w})p(\mathbf{w})\\
&\varpropto \exp\Big(-\frac{1}{2}(\mathbf{y}-X\mathbf{w})^T(\mathbf{y}-X\mathbf{w})\Big) \exp\Big(-\frac{1}{2}(\mathbf{w}-\pmb\mu_0)^T\pmb\Lambda_0^{-1}(\mathbf{w}-\pmb\mu_0)\Big)\\
&\varpropto \exp\Big(-\frac{1}{2}(-2\mathbf{y}^TX\mathbf{w}+\mathbf{w}^TX^TX\mathbf{w}+\mathbf{w}^T\pmb\Lambda_0^{-1}\mathbf{w}-2\pmb\mu_0^T\pmb\Lambda_0^{-1}\mathbf{w})\Big)\\
&\varpropto \exp\Big(-\frac{1}{2}(\mathbf{w}-\pmb\mu_m)^T\pmb\Lambda_m^{-1}(\mathbf{w}-\pmb\mu_m)+\frac{1}{2}\pmb\mu_m^T\pmb\Lambda_m^{-1}\pmb\mu_m\Big)\\
&\varpropto \exp\Big(-\frac{1}{2}(\mathbf{w}-\pmb\mu_m)^T\pmb\Lambda_m^{-1}(\mathbf{w}-\pmb\mu_m)\Big)\\
\end{align}
$$
其中
$$
\begin{align}
\pmb\Lambda_m&=(X^TX+\pmb\Lambda_0^{-1})^{-1}\\
\pmb\mu_m&=\pmb\Lambda_m(X^T\mathbf{y}+\pmb\Lambda_0^{-1}\pmb\mu_0)\\
\end{align}
$$
大多数情况下，我们设置 $\pmb µ_0 = 0$。如果我们设置 $\pmb\Lambda_0 = \frac{1}{\alpha} I$， 那么 $\pmb\mu_m$ 对 w 的估计就和频率派带权重衰减惩罚 $\alpha\mathbf{w}^⊤\mathbf{w}$ 的线性回归的估计是一样的。一个区别是若 α 设为 0 则贝叶斯估计是未定义的——我们不能将贝叶斯学习过程初始化为一个无限宽的 w 先验。更重要的区别是贝叶斯估计会给出一个协方差矩阵，表示 w 所有不同值的可能范围，而不仅是估计 $\pmb\mu_m$。 

### 5.6.1 最大后验（MAP）估计

希望使用点估计的一个常见原因是，对于大多数有意义的模型而言，大多数涉及到贝叶斯后验的计算是非常棘手的，点估计提供了一个可行的近似解。我们仍然可以让先验影响点估计的选择来利用贝叶斯方法的优点，而不是简单地回到最大似然估计。一种能够做到这一点的合理方式是选择 最大后验（ MaximumA Posteriori, MAP）点估计。 MAP 估计选择后验概率最大的点（或在 θ 是连续值的更常见情况下，概率密度最大的点）： 
$$
\begin{align}
\pmb\theta_\text{MAP}
&= \arg\max\limits_{\pmb\theta}\ p(\pmb\theta|\mathbf{x})\\
&= \arg\max\limits_{\pmb\theta}\ \log p(\mathbf{x}|\pmb\theta)+\log p(\pmb\theta)
\end{align}
$$
考虑具有高斯先验权重 w 的线性回归模型。如果先验是 $\mathcal{N}(\mathbf{w}; \mathbf{0}; \frac{1}{\lambda} I^2)$，那么上式的对数先验项正比于熟悉的权重衰减惩罚 $\lambda\mathbf{w}^⊤\mathbf{w}$，加上一个不依赖于w 也不会影响学习过程的项。因此，具有高斯先验权重的MAP 贝叶斯推断对应着权重衰减。

MAP 贝叶斯推断提供了一个直观的方法来设计复杂但可解释的正则化项。

## 5.7 监督学习算法

### 5.7.1 概率监督学习

**逻辑回归** 
$$
p(y=1|\mathbf{x};\pmb\theta)=\sigma(\pmb\theta^T\mathbf{x})
$$

### 5.7.2 支持向量机

类似于逻辑回归，这个模型也是基于线性函数 $\mathbf{w}^⊤\mathbf{x} + b$ 的。不同于逻辑回归的是，支持向量机不输出概率，只输出类别。当 $\mathbf{w}^⊤\mathbf{x} + b$ 为正时，支持向量机预测属于正类。类似地，当 $\mathbf{w}^⊤\mathbf{x} + b$ 为负时，支持向量机预测属于负类。 

**核技巧** 

支持向量机中的线性函数可以重写为 
$$
\mathbf{w}^T\mathbf{x}+b=b+\sum_{i=1}^m\alpha_i\mathbf{x}^T\mathbf{x}^{(i)}
$$
点积替换为被称为 核函数（ kernel function）的函数$k(\mathbf{x}, \mathbf{x}^{(i)}) = ϕ(\mathbf{x}) · ϕ(\mathbf{x}^{(i)})$。

> $\phi(\mathbf{x})\cdot\phi(\mathbf{x}^{(i)})=\phi(\mathbf{x})^T\phi(\mathbf{x}^{(i)})$ 

使用核估计替换点积之后，我们可以使用如下函数进行预测 
$$
f(\mathbf{x})=b+\sum_i \alpha_i k(\mathbf{x},\mathbf{x}^{(i)})
$$
核函数完全等价于用 ϕ(x) 预处理所有的输入，然后在新的转换空间学习线性模型 

最常用的核函数是 **高斯核**（ Gaussian kernel） 
$$
k(\mathbf{u},\mathbf{v})=\mathcal{N}(\mathbf{u}-\mathbf{v};\mathbf{0},\sigma^2I)
$$
这个核也被称为 **径向基函数**（ radial basis function, RBF）核，因为其值沿 v 中从 u 向外辐射的方向减小。 

> 我们可以认为高斯核在执行一种模板匹配 (template matching)。训练标签 y 相关的训练样本 x 变成了类别 y 的模版。当测试点 x′ 到 x 的欧几里得距离很小，对应的高斯核响应很大时，表明 x′ 和模版 x 非常相似。该模型进而会赋予相对应的训练标签 y 较大的权重。总的来说，预测将会组合很多这种通过训练样本相似度加权的训练标签。 

### 5.7.3 其他简单的监督学习算法

k-最近邻、决策树

## 5.8 无监督学习算法

一个经典的无监督学习任务是找到数据的 ‘‘最佳’’ 表示。 ‘‘最佳’’ 可以是不同的表示，但是一般来说，是指该表示在比本身表示的信息更简单或更易访问而受到一些惩罚或限制的情况下，尽可能地保存关于 x 更多的信息。 

有很多方式定义较简单的表示。最常见的三种包括低维表示、稀疏表示和独立表示。 

> - 低维表示尝试将 x 中的信息尽可能压缩在一个较小的表示中。 
>
> - 稀疏表示将数据集嵌入到输入项(entry)大多数为零的表示中 
>
> - 独立表示试图分开数据分布中变化的来源，使得表示的维度是统计独立的。 

### 5.8.1 主成分分析

假设有一个 m × n 的设计矩阵 X，数据的均值为零， E[x ] = 0。若非如此，通过预处理步骤使所有样本减去均值，数据可以很容易地中心化。 

X 对应的无偏样本协方差矩阵给定如下 
$$
\text{Var}[\mathbf{x}]=\frac{1}{m-1}X^\top X
$$
PCA 通过线性变换找到一个 Var[z] 是对角矩阵的表示 $\mathbf{z} = W^⊤ \mathbf{x}$。 

设计矩阵 X 的主成分由 $X^⊤X$ 的特征向量给定。 
$$
X^\top X=W\Lambda W^\top
$$
主成分也可以通过奇异值分解 (SVD) 得到。具体来说，它们是 X 的右奇异向量。 
$$
X=U\Sigma W^\top\\
X^\top X=(U\Sigma W^\top)^\top (U\Sigma W^\top)=W\Sigma^2 W^\top
$$
使用 X 的 SVD 分解， X 的方差可以表示为 
$$
\begin{align}
\text{Var}[\mathbf{x}]
&=\frac{1}{m-1}X^\top X\\
&=\frac{1}{m-1}W\Sigma^2 W^\top\\
\end{align}
$$
$\mathbf{z}$ 的协方差满足对角的要求
$$
\begin{align}
\text{Var}[\mathbf{z}]
&=\frac{1}{m-1}Z^\top Z\\
&=\frac{1}{m-1}W^\top X^\top X W\\
&=\frac{1}{m-1}W^\top W\Sigma^2 W^\top W\\
&=\frac{1}{m-1}\Sigma^2\\
\end{align}
$$

> 协方差矩阵为对角矩阵说明元素之间彼此线性无关

PCA 这种将数据变换为元素之间彼此不相关表示的能力是PCA 的一个重要性质。它是消除数据中未知变化因素的简单表示示例。在 PCA 中，这个消除是通过寻找输入空间的一个旋转（由 W 确定），使得方差的主坐标和 z 相关的新表示空间的基对齐。 

### 5.8.2 k-均值聚类

k-均值聚类算法将训练集分成 k个靠近彼此的不同样本聚类。因此我们可以认为该算法提供了 k-维的 one-hot 编码向量 $\mathbf{h}$ 以表示输入 $\mathbf{x}$。当  属于聚类 i 时，有 $h_i$ = 1， $\mathbf{h}$ 的其他项为零。

## 5.9 随机梯度下降

> stochastic gradient descent, SGD 

$$
J(\pmb\theta)
=\mathbb{E}_{\mathbf{x},y\sim\hat{p}_\text{data}}L(\mathbf{x},y,\pmb\theta)
=\frac{1}{m}\sum_{i=1}^mL(\mathbf{x}^{(i)},y^{(i)},\pmb\theta)\\
L(\mathbf{x},y,\pmb\theta)=-\log p(y|\mathbf{x};\pmb\theta)\\
\nabla_{\pmb\theta}J(\pmb\theta)=\frac{1}{m}\sum_{i=1}^m\nabla_{\pmb\theta}L(\mathbf{x}^{(i)},y^{(i)},\pmb\theta)
$$

这个运算的计算代价是 O(m)。随着训练集规模增长为数十亿的样本，计算一步梯度也会消耗相当长的时间。 

随机梯度下降的核心是，梯度是期望。期望可使用小规模的样本近似估计。 

在算法的每一步，我们从训练集中均匀抽出一 小批量（ minibatch）样本
$\mathbb{B} = \{x^{(1)},...,x^{(m′)}\}$。小批量的数目 m′ 通常是一个相对较小的数，从一到几百。重
要的是，当训练集大小 m 增长时， m′ 通常是固定的。我们可能在拟合几十亿的样
本时，每次更新计算只用到几百个样本。 

梯度的估计可以表示成 
$$
\mathbf{g}=\frac{1}{m'}\nabla_{\pmb\theta}\sum_{i=1}^{m'}L(\mathbf{x}^{(i)},y^{(i)},\pmb\theta)\\
\pmb\theta\gets\pmb\theta-\epsilon\mathbf{g}
$$

## 5.10 构建机器学习算法

几乎所有的深度学习算法都可以被描述为一个相当简单的配方：特定的数据集、代价函数、优化过程和模型。 

> 例如，线性回归算法由以下部分组成：  
>
> - 数据集：X 和 $\mathbf{y}$ 
> - 代价函数：$J(\mathbf{w},b)=-\mathbb{E}_{\mathbf{x},y\sim\hat{p}_\text{data}}\log p_\text{model}(y|\mathbf{x})$ 
> - 模型：$p_\text{model}(y|\mathbf{x})=\mathcal{N}(y;\mathbf{x}^\top\mathbf{w}+b,1)$ 
> - 优化算法 ：求解代价函数梯度为零的正规方程

## 5.11 促使深度学习发展的挑战

深度学习发展动机的一部分原因是传统学习算法在这类人工智能问题上泛化能力不足。 

### 5.11.1 维数灾难

![1547101888140](assets/1547101888140.jpg)

### 5.11.2 局部不变性和平滑正则化

> 这部分内容基本看不懂，o(╥﹏╥)o

为了更好地泛化，机器学习算法需要由先验信念引导应该学习什么类型的函数。 

**局部不变形先验** 
$$
f(\mathbf{x})\approx f(\mathbf{x}+\pmb\epsilon)
$$

### 5.11.3 流形学习

流形（ manifold）指连通的区域。 

每个点周围邻域的定义暗示着存在变换能够从一个位置移动到其邻域位置。 

尽管术语 “流形’’ 有正式的数学定义，但是机器学习倾向于更松散地定义一组点，只需要考虑少数嵌入在高维空间中的自由度或维数就能很好地近似。 

> 示例
>
> 训练数据位于二维空间中的一维流形中 
>
> ![1547102762268](assets/1547102762268.jpg)

如果我们希望机器学习算法学习整个 $\mathbb{R}^n$ 上有趣变化的函数，那么很多机器学习问题看上去都是无望的。  

流形学习（ manifold learning）算法通过一个假设来克服这个障碍，该假设认为 Rn 中大部分区域都是无效的输入，有意义的输入只分布在包含少量数据点的子集构成的一组流形中，而学习函数的输出中，有意义的变化都沿着流形的方向或仅发生在我们切换到另一流形时。 

数据位于低维流形的假设并不总是对的或者有用的。我们认为在人工智能的一些场景中，如涉及到处理图像、声音或者文本时，流形假设至少是近似对的。这个假设的支持证据包含两类观察结果。 

- 第一个支持 流形假设（ manifold hypothesis）的观察是现实生活中的图像、文本、声音的概率分布都是高度集中的。 

- 支持流形假设的第二个论点是，我们至少能够非正式地想象这些邻域和变换。 

  > 在图像中，我们当然会认为有很多可能的变换仍然允许我们描绘出图片空间的流形：我们可以逐渐变暗或变亮光泽、逐步移动或旋转图中对象、逐渐改变对象表面的颜色等等。 

当数据位于低维流形中时，使用流形中的坐标而非 Rn 中的坐标表示机器学习数据更为自然。 

> 日常生活中，我们可以认为道路是嵌入在三维空间的一维流形。我们用一维道路中的地址号码确定地址，而非三维空间中的坐标。 

