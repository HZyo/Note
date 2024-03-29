# 8. 深度模型中的优化

## 8.1 学习和纯优化有什么不同

通常，代价函数可写为训练集上的平均，如 
$$
\mathbb { E } _ { \mathbf { x } , \mathbf { y } \sim \hat { p } _ { \mathrm { data } } } [ L ( f ( \boldsymbol { x } ; \boldsymbol { \theta } ) , y ) ] = \frac { 1 } { m } \sum _ { i = 1 } ^ { m } L \left( f \left( \boldsymbol { x } ^ { ( i ) } ; \boldsymbol { \theta } \right) , y ^ { ( i ) } \right)
\tag{8.1}
$$
其中 L 是每个样本的损失函数， $f(\boldsymbol{x}; \boldsymbol{\theta})$ 是输入$\boldsymbol{x}$ 时所预测的输出， $\hat{p}_\text{data}​$ 是经验分布。监督学习中， y 是目标输出。 

通常，我们更希望最小化取自数据生成分布 $p_\text{data}$ 的期望，而不仅仅是有限训练集上的对应目标函数 
$$
J ^ { * } ( \boldsymbol { \theta } ) = \mathbb { E } _ { ( \mathbf { x } , y ) \sim p _ { \text {data} } } L ( f ( x ; \boldsymbol { \theta } ) , y )
\tag{8.2}
$$

### 8.1.1 经验风险最小化

机器学习算法的目标是降低式 (8.2) 所示的期望泛化误差。这个数据量被称为 **风险**（ risk）。在这里，我们强调该期望取自真实的潜在分布 $p_\text{data}$。如果我们知道了真实分布 $p_\text{data}(\boldsymbol{x}; y)$，那么最小化风险变成了一个可以被优化算法解决的优化问题。然而，我们遇到的机器学习问题，通常是不知道 $p_\text{data}(\boldsymbol{x}; y)​$，只知道训练集中的样本。

 将机器学习问题转化回一个优化问题的最简单方法是最小化训练集上的期望损失。这意味着用训练集上的经验分布 $\hat{p}(\boldsymbol{x}; y)$ 替代真实分布 $p(\boldsymbol{x}; y)$。现在，我们将最小化 **经验风险**（ empirical risk）：
$$
\mathbb { E } _ { \mathbf { x } , \mathrm { y } \sim \hat { p } _ { \text {data} } } [ L ( f ( \boldsymbol { x } ; \boldsymbol { \theta } ) , y ) ] = \frac { 1 } { m } \sum _ { i = 1 } ^ { m } L \left( f \left( \boldsymbol { x } ^ { ( i ) } ; \boldsymbol { \theta } \right) , y ^ { ( i ) } \right)
$$
基于最小化这种平均训练误差的训练过程被称为 **经验风险最小化**（ empiricalrisk minimization）。 

然而，经验风险最小化很容易导致过拟合。最有效的现代优化算法是基于梯度下降的，但是很多有用的损失函数，如 0 - 1 损失，没有有效的导数。这两个问题说明，在深度学习中我们很少使用经验风险最小
化。反之，我们会使用一个稍有不同的方法，我们真正优化的目标会更加不同于我们希望优化的目标。 

### 8.1.2 代理损失函数和提前终止 

有时，我们真正关心的损失函数（比如分类误差）并不能被高效地优化。 在这种情况下，我们通常会优化 **代理损失函数**（ surrogate loss function）。 

> 例如，正确类别的负对数似然通常用作 0 - 1 损失的替代。 

一般的优化和我们用于训练算法的优化有一个重要不同：训练算法通常不会停止在局部极小点。反之，机器学习通常优化代理损失函数，但是在基于提前终止（第 7.8 节）的收敛条件满足时停止。通常，提前终止使用真实潜在损失函数，如验证集上的 0 - 1 损失，并设计为在过拟合发生之前终止。与纯优化不同的是，提前终止时代理损失函数仍然有较大的导数，而纯优化终止时导数较小。 

### 8.1.3 批量算法和小批量算法

机器学习算法的目标函数通常可以分解为训练样本上的求和。 机器学习中的优化算法在计算参数的每一次更新时通常仅使用整个代价函数中一部分项来估计代价函数的期望值。 

n 个样本均值的标准差是 $σ/\sqrt{n}$， 其中 σ 是样本值真实的标准差。分母 $\sqrt{n}$ 表明使用更多样本来估计梯度的方法的回报是低于线性的。比较两个假想的梯度计算，一个基于 100 个样本，另一个基于 10, 000 个样本。后者需要的计算量是前者的 100 倍，但却只降低了 10 倍的均值标准差。如果能够快速地计算出梯度估计值，而不是缓慢地计算准确值，那么大多数优化算法会收敛地更快（就总的计算量而言，而不是指更新次数）。 

每次只使用单个样本的优化算法有时被称为 **随机**（ stochastic）或者 **在线**（ online）算法。 

> 术语 “在线’’ 通常是指从连续产生样本的数据流中抽取样本的情况，而不是从一个固定大小的训练集中遍历多次采样的情况。 
>
> 大多数用于深度学习的算法介于以上两者之间，使用一个以上，而又不是全部的训练样本。传统上，这些会被称为 **小批量**（ minibatch）或 **小批量随机**（ minibatch stochastic）方法，现在通常将它们简单地称为 **随机**（ stochastic）方法。 

我们可以从数据生成分布 $p_\text{data}$抽取小批量样本 $\left\{ x ^ { ( 1 ) } , \ldots , x ^ { ( m ) } \right\}$ 以及对应的目标 $y^{(i)}$，然后计算该小批量上损失函数关于对应参数的梯度
$$
\hat { \boldsymbol { g } } = \frac { 1 } { m } \nabla _ { \boldsymbol { \theta } } \sum _ { i } L \left( f \left( \boldsymbol { x } ^ { ( i ) } ; \boldsymbol { \theta } \right) , y ^ { ( i ) } \right)
$$
以此获得泛化误差准确梯度的无偏估计。最后，在泛化误差上使用 SGD 方法在方向$\hat{g}$ 上更新 $\boldsymbol{\theta}$。 

## 8.2 神经网络优化中的挑战

### 8.2.1 病态

在优化凸函数时，会遇到一些挑战。这其中最突出的是 Hessian 矩阵 H 的病态。 病态问题一般被认为存在于神经网络训练过程中。病态体现在随机梯度下降会‘‘卡’’ 在某些情况，此时即使很小的更新步长也会增加代价函数。 

代价函数的二阶泰勒级数展开预测梯度下降中的 -ϵg 会增加 
$$
\frac { 1 } { 2 } \epsilon ^ { 2 } g ^ { \top } H g - \epsilon g ^ { \top } g
$$
到代价中。当 $\frac { 1 } { 2 } \epsilon ^ { 2 } g ^ { \top } H g​$ 超过 $ϵ\boldsymbol{g}^⊤\boldsymbol{g}​$ 时，梯度的病态会成为问题。 

在很多情况中，梯度范数不会在训练过程中显著缩小，但是 $\boldsymbol{g}^⊤H\boldsymbol{g}$ 的增长会超过一个数量级。其结
果是尽管梯度很强，学习会变得非常缓慢，因为学习率必须收缩以弥补更强的曲率。 

### 8.2.2 局部极小值

由于 模型可辨识性（ model identifiability）问题，神经网络和任意具有多个等效参数化潜变量的模型都会具有多个局部极小值。 

如果局部极小值相比全局最小点拥有很大的代价，局部极小值会带来很大的隐患。 

对于实际中感兴趣的网络，是否存在大量代价很高的局部极小值，优化算法是否会碰到这些局部极小值，都是尚未解决的公开问题。 

学者们现在猜想，对于足够大的神经网络而言，大部分局部极小值都具有很小的代价函数，我们能不能找到真正的全局最小点并不重要，而是需要在参数空间中找到一个代价很小（但不是最小）的点。

一种能够排除局部极小值是主要问题的检测方法是画出梯度范数随时间的变化。如果梯度范数没有缩小到一个微小的值，那么该问题既不是局部极小值，也不是其他形式的临界点。 

### 8.2.3 高原、鞍点和其他平坦区域 

对于很多高维非凸函数而言，局部极小值（以及极大值）事实上都远少于另一类梯度为零的点：鞍点。 

在鞍点处， Hessian 矩阵同时具有正负特征值。位于正特征值对应的特征向量方向的点比鞍点有更大的代价，反之，位于负特征值对应的特征向量方向的点有更小的代价。 

在高维空间中，局部极小值很罕见，而鞍点则很常见。对于这类函数 $f : \mathbb { R } ^ { n } \rightarrow \mathbb { R }$ 而言，鞍点和局部极小值的数目比率的期望随 n 指数级增长。 

> 我们可以从直觉上理解这种现象
>
> Hessian 矩阵在局部极小点处只有正特征值。而在鞍点处， Hessian 矩阵则同时具有正负特征值。试想一下，每个特征值的正负号由抛硬币决定。在一维情况下，很容易抛硬币得到正面朝上一次而获取局部极小点。在 n-维空间中，要抛掷 n 次硬币都正面朝上的难度是指数级的。 

很多随机函数一个惊人性质是，当我们到达代价较低的区间时， Hessian 矩阵的特征值为正的可能性更大。这也意味着，局部极小值具有低代价的可能性比高代价要大得多。具有高代价的临界点更有可能是鞍点。具有极高代价的临界点就很可能是局部极大值了。

对于牛顿法而言，鞍点显然是一个问题。梯度下降旨在朝 ‘‘下坡’’ 移动，而非明确寻求临界点。而牛顿法的目标是寻求梯度为零的点。如果没有适当的修改，牛顿法就会跳进一个鞍点。高维空间中鞍点的激增或许解释了在神经网络训练中为什么二阶方法无法成功取代梯度下降。 

### 8.2.4 悬崖和梯度爆炸

多层神经网络通常存在像悬崖一样的斜率较大区域。遇到斜率极大的悬崖结构时，梯度更新会很大程度地改变参数值，通常会完全跳过这类悬崖结构。 

> ![1547463668571](assets/1547463668571.jpg)

不管我们是从上还是从下接近悬崖，情况都很糟糕，但幸运的是我们可以用使用第 10.11.1 节介绍的启发式 梯度截断（ gradient clipping）来避免其严重的后果。 

其基本想法源自梯度并没有指明最佳步长，只说明了在无限小区域内的最佳方向。当传统的梯度下降算法提议更新很大一步时，启发式梯度截断会干涉来减小步长，从而使其不太可能走出梯度近似为最陡下降方向的悬崖区域。 

### 8.2.5 长期依赖

因为循环网络要在很长时间序列的各个时刻重复应用相同操作来构建非常深的计算图，并且模型参数共享，这使长期依赖问题更加凸显。

例如，假设某个计算图中包含一条反复与矩阵 W 相乘的路径。那么 t 步后，相当于乘以 $W^t$。假设 W 有特征值分解 $W = V\text{diag}(λ)V^{-1}​$。在这种简单的情况下，很容易看出 
$$
\boldsymbol { W } ^ { t } = \left( \boldsymbol { V } \operatorname { diag } ( \boldsymbol { \lambda } ) \boldsymbol { V } ^ { - 1 } \right) ^ { t } = \boldsymbol { V } \operatorname { diag } ( \boldsymbol { \lambda } ) ^ { t } \boldsymbol { V } ^ { - 1 }
$$
当特征值 $λ_i$ 不在 1 附近时，若在量级上大于 1 则会爆炸；若小于 1 时则会消失。 **梯度消失**与**爆炸问题**（ vanishing and exploding gradient problem）是指该计算图上的梯度也会因为 $\text{diag}(λ)^t$ 大幅度变化。 

循环网络在各时间步上使用相同的矩阵 W，而前馈网络并没有。所以即使使用非常深层的前馈网络，也能很大程度上有效地避免梯度消失与爆炸问题 (Sussillo, 2014)。 

### 8.2.6 不精确的梯度

### 8.2.7 局部和全局结构间的弱一致性

如果该方向在局部改进很大，但并没有指向代价低得多的遥远区域，那么我们有可能在单点处克服以上所有困难，但仍然表现不佳。 

许多现有研究方法在求解具有困难全局结构的问题时，旨在寻求良好的初始点，而不是开发非局部范围更新的算法。 

### 8.2.8 优化的理论限制

## 8.3 基本算法

### 8.3.1 随机梯度下降

![1547465404350](assets/1547465404350.jpg)

### 8.3.2 动量

动量方法 (Polyak, 1964) 旨在加速学习，特别是处理高曲率、小但一致的梯度，或是带噪声的梯度。 

> 示例
>
> ![1547466017980](assets/1547466017980.jpg)

![1547465994797](assets/1547465994797.jpg)

超参数$α \in [0, 1)$ 决定了之前梯度的贡献衰减得有多快

如果动量算法总是观测到梯度 g，那么它会在方向 -g 上不停加速，直到达到最终速度，其中步长大小为， 
$$
\frac { \epsilon \| g \| } { 1 - \alpha }
$$
因此将动量的超参数视为 1-α 有助于理解。例如， α = 0.9 对应着最大速度 10 倍于梯度下降算法。 

### 8.3.3 Nesterov 动量

![1547466754207](assets/1547466754207.jpg)

在凸批量梯度的情况下， Nesterov 动量将额外误差收敛率从 $O(1/k)$（ k 步后）改进到 $O(1/k^2)$，如 Nesterov (1983) 所示。可惜，在随机梯度的情况下， Nesterov动量没有改进收敛率。 

## 8.4 参数初始化策略

## 8.5 自适应学习率算法

### 8.5.1 AdaGrad

![1547467443864](assets/1547467443864.jpg)

在凸优化背景中， AdaGrad 算法具有一些令人满意的理论性质。然而，经验上已经发现，对于训练深度神经网络模型而言， 从训练开始时积累梯度平方会导致有效学习率过早和过量的减小。 AdaGrad 在某些深度学习模型上效果不错，但不是全部。 

### 8.5.2 RMSProp

![1547467559391](assets/1547467559391.jpg)

RMSProp 算法 (Hinton, 2012) 修改 AdaGrad 以在非凸设定下效果更好，改变梯度积累为指数加权的移动平均。 AdaGrad 旨在应用于凸问题时快速收敛。当应用于非凸函数训练神经网络时，学习轨迹可能穿过了很多不同的结构，最终到达一个局部是凸碗的区域。 AdaGrad 根据平方梯度的整个历史收缩学习率，可能使得学习率在达到这样的凸结构前就变得太小了。 RMSProp 使用指数衰减平均以丢弃遥远过去的历史，使其能够在找到凸碗状结构后快速收敛，它就像一个初始化于该碗状结构的 AdaGrad 算法实例。 

经验上， RMSProp 已被证明是一种有效且实用的深度神经网络优化算法。目前它是深度学习从业者经常采用的优化方法之一。 

### 8.5.3 Adam

![1547467919482](assets/1547467919482.jpg)

### 8.5.4 选择正确的优化算法

### 8.5.5 其他方法

- 在每次迭代中调节不同的学习率。在每次迭代中去调整学习率的值是另一种很好的学习率自适应方法。此类方法的基本思路是当你离最优值越远，你需要朝最优值移动的就越多，即学习率就应该越大；反之亦反。例如：如果相对于上一次迭代，错误率减少了，就可以增大学习率，以5%的幅度；如果相对于上一次迭代，错误率增大了（意味着跳过了最优值），那么应该重新设置上一轮迭代ωj 的值，并且减少学习率到之前的50%。
- 当validation accuracy满足early stopping时，但是我们可以不stop，而是让learning rate减半之后让程序继续跑。下一次validation accuracy又满足no-improvement-in-n规则时，我们同样再将learning rate减半。继续这个过程，直到learning rate变为原来的1/1024再终止程序。（1/1024还是1/512还是其他可以根据实际确定）。

## 8.6 二阶近似方法

为表述简单起见，我们只考察目标函数为经验风险： 
$$
J ( \boldsymbol { \theta } ) = \mathbb { E } _ { \mathbf { x } , \mathbf { y } \sim \hat { p } _ { \text { data } } ( x , y ) } [ L ( f ( x ; \boldsymbol { \theta } ) , y ) ] = \frac { 1 } { m } \sum _ { i = 1 } ^ { m } L \left( f \left( \boldsymbol { x } ^ { ( i ) } ; \boldsymbol { \theta } \right) , y ^ { ( i ) } \right)
$$

### 8.6.1 牛顿法

牛顿法是基于二阶泰勒级数展开在某点 $\boldsymbol{\theta}_0$ 附近来近似 $J(\boldsymbol{\theta})$ 的优化方法，其忽略了高阶导数： 
$$
J ( \boldsymbol { \theta } ) \approx J \left( \boldsymbol { \theta } _ { 0 } \right) + \left( \boldsymbol { \theta } - \boldsymbol { \theta } _ { 0 } \right) ^ { \top } \nabla _ { \boldsymbol { \theta } } J \left( \boldsymbol { \theta } _ { 0 } \right) + \frac { 1 } { 2 } \left( \boldsymbol { \theta } - \boldsymbol { \theta } _ { 0 } \right) ^ { \top } \boldsymbol { H } \left( \boldsymbol { \theta } - \boldsymbol { \theta } _ { 0 } \right)
$$
如果我们再求解这个函数的临界点，我们将得到牛顿参数更新规则： 
$$
\boldsymbol { \theta } ^ { * } = \boldsymbol { \theta } _ { 0 } - \boldsymbol { H } ^ { - 1 } \nabla _ { \boldsymbol { \theta } } J \left( \boldsymbol { \theta } _ { 0 } \right)
$$
对于局部的二次函数（具有正定的 H ），用 $H^{-1}$ 重新调整梯度，牛顿法会直接跳到极小值。如果目标函数是凸的但非二次的（有高阶项），该更新将是迭代的，得到和牛顿法相关的算法，如下

![1547468298902](assets/1547468298902.jpg)

在深度学习中，目标函数的表面通常非凸（有很多特征），如鞍点。因此使用牛顿法是有问题的。如果Hessian 矩阵的特征值并不都是正的，例如，靠近鞍点处，牛顿法实际上会导致更新朝错误的方向移动。这种情况可以通过正则化Hessian 矩阵来避免。常用的正则化策略包括在 Hessian 矩阵对角线上增加常数 α。正则化更新变为 
$$
\boldsymbol { \theta } ^ { * } = \boldsymbol { \theta } _ { 0 } - \left[ H \left( f \left( \boldsymbol { \theta } _ { 0 } \right) \right) + \alpha \boldsymbol { I } \right] ^ { - 1 } \nabla _ { \boldsymbol { \theta } } f \left( \boldsymbol { \theta } _ { 0 } \right)
$$
这个正则化策略用于牛顿法的近似，例如 Levenberg-Marquardt 算法 (Levenberg, 1944; Marquardt, 1963)，只要 Hessian 矩阵的负特征值仍然相对接近零，效果就会很好。在曲率方向更极端的情况下， α 的值必须足够大，以抵消负特征值。然而，如果 α 持续增加， Hessian 矩阵会变得由对角矩阵 αI 主导，通过牛顿法所选择的方向会收敛到普通梯度除以 α。当很强的负曲率存在时， α 可能需要特别大，以致于牛顿法比选择合适学习率的梯度下降的步长更小。 

除了目标函数的某些特征带来的挑战， 如鞍点，牛顿法用于训练大型神经网络还受限于其显著的计算负担。 Hessian 矩阵中元素数目是参数数量的平方，因此，如果参数数目为 k（甚至是在非常小的神经网络中 k 也可能是百万级别），牛顿法需要计算 k × k 矩阵的逆，计算复杂度为 O(k3)。另外，由于参数将每次更新都会改变， 每次训练迭代都需要计算 Hessian 矩阵的逆。其结果是，只有参数很少的网络才能在实际中用牛顿法训练。在本节的剩余部分，我们将讨论一些试图保持牛顿法优点，同时避免计算障碍的替代算法。 

### 8.6.2 共轭矩阵

共轭梯度是一种通过迭代下降的 共轭方向（ conjugate directions）以有效避免 Hessian 矩阵求逆计算的方法。 这种方法的灵感来自于对最速下降方法弱点的仔细研究，其中线搜索迭代地用于与梯度相关的方向上。 

假设上一个搜索方向是 $\boldsymbol{d}_{t-1}$。在极小值处，线搜索终止，方向 $\boldsymbol{d}_{t-1}$ 处的方向导数为零： $∇_{\boldsymbol{\theta}}J(\boldsymbol{\theta}) · \boldsymbol{d}_{t-1} = 0$。因为该点的梯度定义了当前的搜索方向， $d _ { t } = \nabla _ { \boldsymbol { \theta } } J ( \boldsymbol { \theta } )$将不会贡献于方向$\boldsymbol{d}_{t-1}$。因此方向 $\boldsymbol{d}_{t}$ 正交于 $\boldsymbol{d}_{t-1}$。最速下降多次迭代中，方向 $\boldsymbol{d}_{t-1}$和 $\boldsymbol{d}_{t}$ 之间的关系如下图所示。如图展示的，下降正交方向的选择不会保持前一搜索方向上的最小值。这产生了锯齿形的过程。在当前梯度方向下降到极小值，我们必须重新最小化之前梯度方向上的目标。因此，通过遵循每次线搜索结束时的梯度，我们在某种程度上撤销了在之前线搜索的方向上取得的进展。共轭梯度试图解决这个问题。 

![1547469535926](assets/1547469535926.jpg)

在共轭梯度法中，我们寻求一个和先前线搜索方向 共轭（ conjugate）的搜索方向，即它不会撤销该方向上的进展。在训练迭代 t 时，下一步的搜索方向 $\boldsymbol{d}_t​$ 的形式如下： 
$$
d _ { t } = \nabla _ { \boldsymbol { \theta } } J ( \boldsymbol { \theta } ) + \beta _ { t } \boldsymbol { d } _ { t - 1 }
$$
如果 $\boldsymbol { d } _ { t } ^ { \top } \boldsymbol { H } \boldsymbol { d } _ { t - 1 } = 0$，其中 H 是 Hessian 矩阵，则两个方向 $\boldsymbol{d}_t$ 和 $\boldsymbol{d}_{t-1}$ 被称为共轭的。 

两种用于计算 $β_t$ 的流行方法是： 

- Fletcher-Reeves
  $$
  \beta _ { t } = \frac { \nabla _ { \boldsymbol { \theta } } J \left( \boldsymbol { \theta } _ { t } \right) ^ { \top } \nabla _ { \boldsymbol { \theta } } J \left( \boldsymbol { \theta } _ { t } \right) } { \nabla _ { \boldsymbol { \theta } } J \left( \boldsymbol { \theta } _ { t - 1 } \right) ^ { \top } \nabla _ { \boldsymbol { \theta } } J \left( \boldsymbol { \theta } _ { t - 1 } \right) }
  $$

- Polak-Ribière 
  $$
  \beta _ { t } = \frac { \left( \nabla _ { \boldsymbol { \theta } } J \left( \boldsymbol { \theta } _ { t } \right) - \nabla _ { \boldsymbol { \theta } } J \left( \boldsymbol { \theta } _ { t - 1 } \right) \right) ^ { \top } \nabla _ { \boldsymbol { \theta } } J \left( \boldsymbol { \theta } _ { t } \right) } { \nabla _ { \boldsymbol { \theta } } J \left( \boldsymbol { \theta } _ { t - 1 } \right) ^ { \top } \nabla _ { \boldsymbol { \theta } } J \left( \boldsymbol { \theta } _ { t - 1 } \right) }
  $$

![1547469727577](assets/1547469727577.jpg)

对于二次曲面而言，共轭方向确保梯度沿着前一方向大小不变。因此，我们在前一方向上仍然是极小值。其结果是，在 k-维参数空间中， 共轭梯度只需要至多 k 次线搜索就能达到极小值。 

> 目前，我们已经讨论了用于二次目标函数的共轭梯度法。当然，本章我们主要关注于探索训练神经网络和其他相关深度学习模型的优化方法，其对应的目标函数比二次函数复杂得多。或许令人惊讶，共轭梯度法在这种情况下仍然是适用的，尽管需要作一些修改。没有目标是二次的保证，共轭方向也不再保证在以前方向上的目标仍是极小值。其结果是， 非线性共轭梯度 算法会包括一些偶尔的重设，共轭梯度法沿未修改的梯度重启线搜索。 

### 8.6.3 BFGS

Broyden-Fletcher-Goldfarb-Shanno（ BFGS）算法具有牛顿法的一些优点，但没有牛顿法的计算负担。 

运用牛顿法的主要计算难点在于计算 Hessian 逆 $H^{-1}$。拟牛顿法所采用的方法（ BFGS 是其中最突出的）是使用矩阵 $M_t$ 近似逆，迭代地低秩更新精度以更好地近似 $H^{-1}$。 

当 Hessian 逆近似 $M_t$ 更新时，下降方向 $\boldsymbol{\rho}_t$ 为 $\boldsymbol{\rho} _ { t } = M _ { t } \boldsymbol{g} _ { t }$。该方向上的线搜索用于决定该方向上的步长 $ϵ^∗$。参数的最后更新为： 
$$
\boldsymbol { \theta } _ { t + 1 } = \boldsymbol { \theta } _ { t } + \epsilon ^ { * } \boldsymbol { \rho } _ { t }
$$
**存储受限的BFGS**（或 L-BFGS） 通过避免存储完整的 Hessian 逆近似 M，BFGS 算法的存储代价可以显著降低。 L-BFGS 算法使用和 BFGS 算法相同的方法计算 M 的近似，但起始假设是 $M^{(t-1)}$ 是单位矩阵，而不是一步一步都要存储近似。 

## 8.7 优化策略和元算法

### 8.7.1 批标准化

> Batch Normalization

批标准化 (Ioffe and Szegedy, 2015) 是优化深度神经网络中最激动人心的最新创新之一。实际上它并不是一个优化算法，而是一个自适应的重参数化的方法，试图解决训练非常深的模型的困难。

非常深的模型会涉及多个函数或层组合。在其他层不改变的假设下，梯度用于如何更新每一个参数。在实践中，我们同时更新所有层。当我们进行更新时，可能会发生一些意想不到的结果，这是因为许多组合在一起的函数同时改变时，计算更新的假设是其他函数保持不变（偏导数）。

> 示例
>
> $l​$ 层链式无激活一个单元的深度神经网络，有
> $$
> \hat{y}=xw_1w_2...w_l
> $$
> 计算出$\boldsymbol{g}=\nabla_\boldsymbol{w}\hat{y}$，则$\hat{y}$ 的更新值为
> $$
> x(w_1-\epsilon g_1)(w_2-\epsilon g_2)...(w_l-\epsilon g_l)
> $$
> 这个更新中所产生的一个二阶项示例是 $\epsilon ^ { 2 } g _ { 1 } g _ { 2 } \prod _ { i = 3 } ^ { l } w _ { i }$。如果 $\prod _ { i = 3 } ^ { l } w _ { i }$ 很小，那么该项可以忽略不计。而如果层 3 到层 $l$ 的权重都比 1 大时，该项可能会指数级大。 

批标准化提出了一种几乎可以重参数化所有深度网络的优雅方法。重参数化显著减少了多层之间协调更新的问题。批标准化可应用于网络的任何输入层或隐藏层。 

设 $H$ 是需要标准化的某层的小批量激活函数，排布为设计矩阵，每个样本的激活出现在矩阵的每一行中。为了标准化 $H$，我们将其替换为 
$$
H ^ { \prime } = \frac { H - \boldsymbol{\mu} } { \boldsymbol{\sigma} }
$$
其中 $\boldsymbol{\mu}$ 是包含每个单元均值的向量， $\boldsymbol{\sigma}$ 是包含每个单元标准差的向量。

> 此处的算术是基于广播向量 $\boldsymbol{\mu}$ 和向量 $\boldsymbol{\sigma}$ 应用于矩阵 H 的每一行。在每一行内，运算是逐元素的，因此 $H_{i,j}$ 标准化为减去 $\mu_j$ 再除以 $σ_j$。网络的其余部分操作 H′ 的方式和原网络操作 H 的方式一样。 

在训练阶段， 
$$
\boldsymbol{\mu} = \frac { 1 } { m } \sum _ { i } \boldsymbol { H } _ { i , : }\\
\boldsymbol{\sigma} = \sqrt { \delta + \frac { 1 } { m } \sum _ { i } ( \boldsymbol { H } - \boldsymbol { \mu } ) _ { i } ^ { 2 } }
$$
其中 δ 是个很小的正值，比如 $10^{-8}$，以强制避免遇到 $\sqrt{z}$ 的梯度在 z = 0 处未定义的问题。 

标准化一个单元的均值和标准差会降低包含该单元的神经网络的表达能力。为了保持网络的表现力，通常会将批量隐藏单元激活 H 替换为 $γH′ + β$，而不是简单地使用标准化的 H′。变量 γ 和 β 是允许新变量有任意均值和标准差的学习参数。 

大多数神经网络层会采取 $ϕ(XW + \boldsymbol{b})$ 的形式，其中 ϕ 是某个固定的非线性激活函数，如整流线性变换。自然想到我们应该将批标准化应用于输入 X 还是变换后的值 $XW + \boldsymbol{b}$。 Ioffe and Szegedy (2015) 推荐后者。更具体地， $XW + \boldsymbol{b}​$ 应替换为XW 的标准化形式。偏置项应被忽略，因为参数 β 会加入批标准化重参数化，它是冗余的。 

### 8.7.2 坐标下降

在某些情况下，将一个优化问题分解成几个部分，可以更快地解决原问题。如果我们相对于某个单一变量 $x_i$ 最小化 $f(\boldsymbol{x})$，然后相对于另一个变量 $x_j$ 等等，反复循环所有的变量，我们会保证到达（局部）极小值。这种做法被称为 **坐标下降**（ coordinate descent），因为我们一次优化一个坐标。更一般地， **块坐标下降**（ block coordinate descent）是指对于某个子集的变量同时最小化。

当优化问题中的不同变量能够清楚地分成相对独立的组，或是当优化一组变量明显比优化所有变量效率更高时，坐标下降最有意义。 

> 示例
>
> 稀疏编码学习问题
> $$
> J ( \boldsymbol { H } , \boldsymbol { W } ) = \sum _ { i , j } \left| H _ { i , j } \right| + \sum _ { i , j } \left( \boldsymbol { X } - \boldsymbol { W } ^ { \top } \boldsymbol { H } \right) _ { i , j } ^ { 2 }
> $$
> 函数 J 不是凸的。然而，我们可以将训练算法的输入分成两个集合：字典参数W 和编码表示 H。最小化关于这两者之一的任意一组变量的目标函数都是凸问题。因此，块坐标下降允许我们使用高效的凸优化算法，交替固定 H 优化 W 和固定 W优化 H。 

### 8.7.3 Polyak 平均

Polyak 平均 (Polyak and Juditsky, 1992) 会平均优化算法在参数空间访问轨迹中的几个点。如果 t 次迭代梯度下降访问了点 $\boldsymbol{\theta}^{(1)},...,\boldsymbol{\theta}^{(t)}$，那么 Polyak 平均算法的输出是 $\hat { \boldsymbol { \theta } } ^ { ( t ) } = \frac { 1 } { t } \sum _ { i } \boldsymbol { \theta } ^ { ( i ) }$。

在某些问题中，如梯度下降应用于凸问题时，这种方法具有较强的收敛保证。当应用于神经网络时，其验证更多是启发式的，但在实践中表现良好。基本想法是，优化算法可能会来回穿过山谷好几次而没经过山谷底部附近的点。尽管两边所有位置的均值应比较接近谷底。 

在非凸问题中，优化轨迹的路径可以非常复杂，并且经过了许多不同的区域。包括参数空间中遥远过去的点，可能与当前点在代价函数上相隔很大的障碍，看上去不像一个有用的行为。其结果是，当应用 Polyak 平均于非凸问题时，通常会使用指数衰减计算平均值： 
$$
\hat { \boldsymbol { \theta } } ^ { ( t ) } = \alpha \hat { \boldsymbol { \theta } } ^ { ( t - 1 ) } + ( 1 - \alpha ) \boldsymbol { \theta } ^ { ( t ) }
$$

### 8.7.4 监督预训练

在直接训练目标模型求解目标问题之前，训练简单模型求解简化问题的方法统称为 **预训练**（ pretraining）。 

**贪心算法**（ greedy algorithm）将问题分解成许多部分，然后独立地在每个部分求解最优值。 

贪心算法也可以紧接一个 **精调**（ fine-tuning）阶段，联合优化算法搜索全问题的最优解。使用贪心解初始化联合优化算法，可以极大地加速算法，并提高寻找到的解的质量。 这种方法被称为 **贪心监督预训练**（ greedy supervised pretraining）。 

在贪心监督预训练的原始版本 (Bengio et al., 2007c) 中，每个阶段包括一个仅涉及最终神经网络的子集层的监督学习训练任务。 

> 示例
>
> ![1547474130435](assets/1547474130435.jpg)
>
> (a) 我们从训练一个足够浅的架构开始。 (b) 同一个架构的另一描绘。 (c) 我们只保留原始网络的输入到隐藏层，并丢弃隐藏到输出层。我们将第一层隐藏层的输出作为输入发送到另一监督单隐层 MLP（使用与第一个网络相同的目标训练），从而可以添加第二层隐藏层。这可以根据需要重复多层。 (d) 所得架构的另一种描绘，可视为前馈网络。为了进一步改进优化，我们可以联合地精调所有层（仅在该过程的结束或者该过程的每个阶段）。 

Simonyan and Zisserman (2015) 预训练深度卷积网络（ 11 层权重），然后使用该网络前四层和最后三层初始化更深的网络（多达 19 层 权重），并非一次预训练一层。非常深的新网络的中间层是随机初始化的。然后联合训练新网络。 

还有一种选择，由Yu et al. (2010) 提出，将先前训练多层感知机的输出，以及原始输入，作为每个附加阶段的输入。 

### 8.7.5 设计有助于优化的模型

在实践中， 选择一族容易优化的模型比使用一个强大的优化算法更重要。 

### 8.7.6 延拓法和课程学习

延拓法（ continuation method）是一族通过挑选初始点使优化更容易的方法，以确保局部优化花费大部分时间在表现良好的空间。延拓法的背后想法是构造一系列具有相同参数的目标函数。为了最小化代价函数 $J(\boldsymbol{\theta})$，我们构建新的代价函数$\{J^{(0)},...,J^{(n)}\}$。这些代价函数的难度逐步提高，其中 $J^{(0)}$ 是最容易最小化的， $J^{(n)}$是最难的，真正的代价函数驱动整个过程。 

Bengio et al. (2009) 指出被称为 **课程学习**（ curriculum learning）或者 **塑造**（ shaping）的方法可以被解释为延拓法。课程学习基于规划学习过程的想法，首先学习简单的概念，然后逐步学习依赖于这些简化概念的复杂概念。 

