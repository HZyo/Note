# 14. 自编码器

**自编码器**（ autoencoder）是神经网络的一种，经过训练后能尝试**将输入复制到输出**。 

自编码器内部有一个隐藏层 $\boldsymbol{h}$，可以产生 **编码**（ code）表示输入。该网络可以看作由两部分组成：一个由函数 $\boldsymbol{h} = f(\boldsymbol{x})$ 表示的编码器和一个生成重构的解码器 $\boldsymbol{r} = g(\boldsymbol{h})$。

![1547811227611](assets/1547811227611.jpg)

如果一个自编码器只是简单地学会将处处设置为 $g(f(\boldsymbol{x})) = \boldsymbol{x}$，那么这个自编码器就没什么特别的用处。 

> 复读机

相反，我们不应该将自编码器设计成输入到输出完全相等。这通常需要向自编码器强加一些约束，使它只能近似地复制，并只能复制与训练数据相似的输入。**这些约束强制模型考虑输入数据的哪些部分需要被优先复制，因此它往往能学习到数据的有用特性**。 

现代自编码器将编码器和解码器的概念推而广之，将其中的确定函数推广为随机映射 $p_\text{encoder}(\boldsymbol{h} | \boldsymbol{x})$ 和 $p_\text{decoder}(\boldsymbol{x} | \boldsymbol{h})$。

##  14.1 欠完备自编码器

从自编码器获得有用特征的一种方法是限制 $\boldsymbol{h}$ 的维度比 $\boldsymbol{x}$ 小，这种编码维度小于输入维度的自编码器称为 **欠完备**（ undercomplete）自编码器。 学习欠完备的表示将**强制自编码器捕捉训练数据中最显著的特征**。 

学习过程可以简单地描述为最小化一个损失函数
$$
L(\boldsymbol{x},g(f(\boldsymbol{x})))
$$
当解码器是线性的且 L 是均方误差，欠完备的自编码器会学习出与 `PCA` 相同的生成子空间。这种情况下，自编码器在训练来执行复制任务的同时学到了训练数据的主元子空间。 

因此，拥有非线性编码器函数 f 和非线性解码器函数 g 的自编码器能够学习出更强大的 PCA 非线性推广。不幸的是，**如果编码器和解码器被赋予过大的容量，自编码器会执行复制任务而捕捉不到任何有关数据分布的有用信息**。从理论上说，我们可以设想这样一个自编码器，它只有一维编码，但它具有一个非常强大的非线性编码器，能够将每个训练数据 $\boldsymbol{x}^{(i)}$ 表示为编码 `i`。而解码器可以学习将这些整数索引映射回特定训练样本的值。这种特定情形不会在实际情况中发生，但它清楚地说明，如果自编码器的容量太大，那训练来执行复制任务的自编码器可能无法学习到数据集的任何有用信息。 

## 14.2 正则自编码器

正则自编码器**使用的损失函数可以鼓励模型学习其他特性**（除了将输入复制到输出），而不必限制使用浅层的编码器和解码器以及小的编码维数来限制模型的容量。 

### 14.2.1 稀疏自编码器

稀疏自编码器简单地在训练时结合编码层的稀疏惩罚 $Ω(\boldsymbol{h})$ 和重构误差： 
$$
L ( \boldsymbol { x } , g ( f ( \boldsymbol { x } ) ) ) + \Omega ( \boldsymbol { h } )
$$
其中 $g(\boldsymbol{h})$ 是解码器的输出，通常 $\boldsymbol{h}$ 是编码器的输出，即 $\boldsymbol{h} = f(\boldsymbol{h})$。

###  14.2.2 去噪自编码器

除了向代价函数增加一个惩罚项，我们也可以通过改变重构**误差项**来获得一个能学到有用信息的自编码器。 

**去噪自编码器**（ denoising autoencoder, DAE）最小化 
$$
L(\boldsymbol{x},g(f(\tilde{\boldsymbol{x}})))
$$
其中 $\tilde{\boldsymbol{x}}$ 是被某种**噪声**损坏的 $\boldsymbol{x}​$ 的副本。因此去噪自编码器必须撤消这些损坏，而不是简单地复制输入。 

Alain and Bengio (2013) 和 Bengio et al. (2013c) 指出去噪训练过程强制 f 和 g 隐式地学习 $p_\text{data}(\boldsymbol{x})$ 的结构。 

### 14.2.3 惩罚导数作为正则

另一正则化自编码器的策略是使用一个类似稀疏自编码器中的惩罚项 Ω， 
$$
L ( \boldsymbol{x} , g ( f ( \boldsymbol{x} ) ) ) + \Omega ( \boldsymbol{h} , \boldsymbol{x} )
$$
但 Ω 的形式不同： 
$$
\Omega ( \boldsymbol { h } , \boldsymbol { x } ) = \lambda \sum _ { i } \left\| \nabla _ { \boldsymbol { x } } h _ { i } \right\| ^ { 2 }
$$
这迫使模型学习一个在 $\boldsymbol{x}$ 变化小时目标也没有太大变化的函数。因为这个惩罚只对训练数据适用，它迫使自编码器学习可以反映训练数据分布信息的特征。 

这样正则化的自编码器被称为 **收缩自编码器**（ contractive autoencoder, CAE）。这种方法与去噪自编码器、流形学习和概率模型存在一定理论联系。 

## 14.3 表示能力、层的大小和深度

自编码器通常只有单层的编码器和解码器，但这不是必然的。实际上深度编码器和解码器能提供更多优势。 

深度可以指数地降低表示某些函数的计算成本。深度也能指数地减少学习一些函数所需的训练数据量。

## 14.4 随机编码器和解码器 

![1547814300660](assets/1547814300660.jpg)

## 14.5 去噪自编码器

**去噪自编码器**（ denoising autoencoder, DAE）是一类接受损坏数据作为输入，并训练来预测原始未被损坏数据作为输出的自编码器。 

DAE 的训练过程如下

![1547815188544](assets/1547815188544.jpg)

我们引入一个损坏过程 $C(\tilde{\boldsymbol{x}} | \boldsymbol{x})​$，这个条件分布代表给定数据样本 $\boldsymbol{x}​$ 产生损坏样本 $\tilde{\boldsymbol{x}}​$ 的概率。自编码器则根据以下过程，从训练数据对 $(\boldsymbol{x}; \tilde{\boldsymbol{x}})​$ 中学习**重构分布** (reconstruction distribution) $p_\text{reconstruct}(\boldsymbol{x} | \tilde{\boldsymbol{x}})​$：

1. 从训练数据中采一个训练样本 $\boldsymbol{x}$。
2. 从 $C(\tilde{\boldsymbol{x}} | \boldsymbol{x})$ 采一个损坏样本 $\tilde{\boldsymbol{x}}$。
3. 将 $(\boldsymbol{x}; \tilde{\boldsymbol{x}})$ 作为训练样本来估计自编码器的重构分布 $p_\text{reconstruct}(\boldsymbol{x} | \tilde{\boldsymbol{x}}) =p_\text{decoder}(\boldsymbol{x} | \boldsymbol{h})$，其中 $\boldsymbol{h}$ 是编码器 $f(\tilde{\boldsymbol{x}})$ 的输出， $p_\text{decoder}$ 根据解码函数 $g(\boldsymbol{h})$ 定义。 

我们可以认为 DAE 是在以下期望下进行随机梯度下降： 
$$
- \mathbb { E } _ { \mathbf { x } \sim \hat { p } _ { \text { data } } ( \mathbf { x } ) } \mathbb { E } _ { \tilde { \mathbf { x } } \sim C ( \tilde { \mathbf { x } } | \boldsymbol{x} ) } \log p _ { \text { decoder } } ( \boldsymbol { x } | \boldsymbol { h } = f ( \tilde { \boldsymbol { x } } ) )
$$
