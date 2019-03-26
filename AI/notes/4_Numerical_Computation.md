# 4. 数值计算

## 4.1 上溢和下溢

必须对上溢和下溢进行数值稳定的一个例子是 softmax 函数
$$
\text{softmax}(\mathbf{x})_i=\frac{\exp(x_i)}{\sum_{j=1}^n\exp(x_j)}
$$
令$\mathbf{z}=\mathbf{x}-\max\limits_i x_i$，则避免了溢出(分母大于1，分子小于等于1)，且 $\text{softmax}(\mathbf{z})=\text{softmax}(\mathbf{x})$ 

另外分子下溢时，计算 $\log\text{softmax}(\mathbf{x})$ 会错误的得到$-\infty$，必须实现一个单独的函数来数值稳定的计算 $\log\text{softmax}$。

## 4.2 病态条件

条件数表征函数相对于输入的微小变化而变化的快慢程度。输入被轻微扰动而迅速改变的函数对于科学计算来说可能是有问题的，因为输入中的舍入误差可能导致输出的巨大变化。 

## 4.3 基于梯度的优化方法

$$
\mathbf{x}'=\mathbf{x}-\epsilon\nabla_\mathbf{x}f(\mathbf{x})
$$

### 4.3.1 梯度之上：Jacobian 和 Hessian 矩阵

**Jacobian矩阵** 
$$
\mathbf{f}:\mathbb{R}^m\to\mathbb{R}^n\\
J_{i,j}=\frac{\part}{\part x_j}\mathbf{f}(\mathbf{x})_i
$$
**Hessian矩阵** 
$$
\mathbf{f}:\mathbb{R}^m\to\mathbb{R}\\
H_{i,j}=\frac{\part^2}{\part x_i\part x_j}f(\mathbf{x})
$$
微分算子在任何二阶偏导连续的点处可交换，故在深度学习背景下，Hessian矩阵大多是对称的

特定方向$\mathbf{d}$ 上的二阶导数可以写成 $\mathbf{d}^TH\mathbf{d}$。

> 当 $\mathbf{d}$ 是 H 的一个特征向量时，这个方向的二阶导数就是对应的特征值。对于其他的方向 $\mathbf{d}$，方向二阶导数是所有特征值的加权平均，权重在 0 和 1 之间，且与 $\mathbf{d}$ 夹角越小的特征向量的权重越大。最大特征值确定最
> 大二阶导数，最小特征值确定最小二阶导数 

**梯度下降与二阶导数** 
$$
\begin{align}
f(\mathbf{x})&\approx f(\mathbf{x}^{(0)})
+(\mathbf{x}-\mathbf{x}^{(0)})^T\mathbf{g}
+\frac{1}{2}(\mathbf{x}-\mathbf{x}^{(0)})^TH(\mathbf{x}-\mathbf{x}^{(0)})\\

f(\mathbf{x}^{(0)}-\epsilon \mathbf{g}) &\approx f(\mathbf{x}^{(0)})
-\epsilon \mathbf{g}^T \mathbf{g}
+\frac{1}{2} \epsilon^2 \mathbf{g}^T H \mathbf{g}\\

\end{align}
$$
其中有 3 项：函数的原始值、函数斜率导致的预期改善、函数曲率导致的校正。 

**牛顿法** 
$$
\begin{align}
\frac{\part}{\part\mathbf{x}}f(\mathbf{x})\approx \mathbf{g}+H(\mathbf{x-\mathbf{x}^{(0)}})\\

\mathbf{x}^*=\mathbf{x}^{(0)}-H^{-1}\mathbf{g}\\
\end{align}
$$
当 f 是一个正定二次函数时，牛顿法只要应用一次式 (4.12) 就能直接跳到函数的最小点。如果 f 不是一个真正二次但能在局部近似为正定二次，牛顿法则需要多次迭代 。迭代地更新近似函数和跳到近似函数的最小点可以比梯度下降更快地到达临界点。这在接近局部极小点时是一个特别有用的性质，但是在鞍点附近是有害的。

仅使用梯度信息的优化算法被称为**一阶优化算法** (first-order optimization algorithms)，如梯度下降。使用 Hessian 矩阵的优化算法被称为 **二阶最优化算法**(second-order optimization algorithms)(Nocedal and Wright, 2006)，如牛顿法。

**Lipschitz连续** 

Lipschitz 连续函数的变化速度以 Lipschitz常数（ Lipschitz constant） $\mathcal{L}$ 为界：
$$
\forall \mathbf{x},\forall \mathbf{y},|f(\mathbf{x})-f(\mathbf{y})|\le\mathcal{L}||\mathbf{x}-\mathbf{y}||_2
$$
这个属性允许我们量化我们的假设——梯度下降等算法导致的输入的微小变化将使输出只产生微小变化

## 4.4 约束优化

**广义Lagrangian/Lagrange函数** 

约束的形式描述
$$
\mathbb{S}=\{\mathbf{x}|\forall i,g^{(i)}(\mathbf{x})=0\text{ and }\forall j,h^{(j)}(\mathbf{x})\le0\}\\
$$
广义Lagrangian函数定义如下
$$
L(\mathbf{x},\pmb\lambda,\pmb\alpha)=
f(\mathbf{x})
+\sum_i\lambda_ig^{(i)}(\mathbf{x})
+\sum_j\alpha_jh^{(j)}(\mathbf{x})
$$
$\lambda_i$ 和$\alpha_j$ 称为 KKT 乘子

**KKT方法** 

> Karush-Kuhn-Tucker

通过优化无约束的广义Lagrangian解决约束最小化问题

只要存在至少一个可行点且$f(\mathbf{x})$ 不允许取$\infty$ ，那么
$$
\min_\mathbf{x}\max_{\pmb\lambda}\max_{\pmb\alpha,\pmb\alpha\ge0}
L(\mathbf{x,\pmb\lambda,\pmb\alpha})
$$
与如下函数有相同的最优目标函数值和最优点集
$$
\min_{\mathbf{x}\in\mathbb{S}}f(\mathbf{x})
$$
因为当约束满足时，
$$
\max_{\pmb\lambda}\max_{\pmb\alpha,\pmb\alpha\ge0}
L(\mathbf{x,\pmb\lambda,\pmb\alpha})
=
f(\mathbf{x})
$$
而违反任意约束时，
$$
\max_{\pmb\lambda}\max_{\pmb\alpha,\pmb\alpha\ge0}
L(\mathbf{x,\pmb\lambda,\pmb\alpha})=\infty
$$
这些性质保证不可行点不会是最佳的，并且可行点范围内的最优点不变。

要解决约束最大化问题，我们可以构造 -f(x) 的广义 Lagrange 函数，从而导致以下优化问题  
$$
\min_\mathbf{x}\max_{\pmb\lambda}\max_{\pmb\alpha,\pmb\alpha\ge0}
-f(\mathbf{x})
+\sum_i\lambda_ig^{(i)}(\mathbf{x})
+\sum_j\alpha_jh^{(j)}(\mathbf{x})
$$
满足 $\pmb\alpha\odot\mathbf{h}(\mathbf{x})=0$ 

> 为了获得关于这个想法的一些直观解释，我们可以说这个解是由不等式强加的边界，我们必须通过对应的 KKT 乘子影响 x的解，或者不等式对解没有影响，我们则归零 KKT 乘子。 

我们可以使用一组简单的性质来描述约束优化问题的最优点。这些性质称为 **Karush–Kuhn–Tucker（ KKT）条件**。这些是确定一个点是最优点的必要条件，但不一定是充分条件。这些条件是： 

- 广义 Lagrangian 的梯度为零 
- 所有关于 x 和 KKT 乘子的约束都满足 
- 不等式约束显示的 ‘‘互补松弛性’’： $\pmbα \odot \mathbf{h}(\mathbf{x}) = 0$ 

## 4.5 实例：线性最小二乘

### 4.5.1 无约束

$$
\begin{align}
f(\mathbf{x})
&=\frac{1}{2}||A\mathbf{x}-\mathbf{b}||_2^2\\
&=\frac{1}{2}(A\mathbf{x}-\mathbf{b})^T(A\mathbf{x}-\mathbf{b})\\
&=\frac{1}{2}(\mathbf{x}^T A^T A\mathbf{x}-\mathbf{b}^T A\mathbf{x}-\mathbf{x}^T A^T \mathbf{b}+\mathbf{b}^T\mathbf{b})\\
\nabla_\mathbf{x}f(\mathbf{x})
&=A^TA\mathbf{x}-A^T\mathbf{b}
\end{align}
$$

**梯度下降** 

将步长 (ϵ) 和容差 (δ) 设为小的正数。
$$
\begin{align}
&\text{while  } ||A^⊤A\mathbf{x} - A^⊤\mathbf{b}||_2 > δ \text{ do}\\
&\ \ \ \ \mathbf{x}\gets\mathbf{x}-\epsilon(A^TA\mathbf{x}-A^T\mathbf{b})\\
&\text{end while}
\end{align}
$$
我们也可以使用牛顿法解决这个问题。因为在这个情况下，真实函数是二次的，牛顿法所用的二次近似是精确的，该算法会在一步后收敛到全局最小点。 

### 4.5.1 有约束

$$
\mathbf{x}^T\mathbf{x}\le1\\
L(\mathbf{x},\lambda)=f(\mathbf{x})+\lambda(\mathbf{x}^T\mathbf{x}-1)\\
\min_\mathbf{x}\max_{\lambda,\lambda\ge0}L(\mathbf{x},\lambda)
$$

使用Moore-Penrose伪逆$\mathbf{x}=A^+\mathbf{b}$ 找到无约束最小二乘问题的最小范数解，如果范数小于等于1，则这也是约束问题的解。否则必须找到约束是活跃的解。
$$
\frac{\part L}{\part \mathbf{x}}=A^TA\mathbf{x}-A^T\mathbf{b}+2\lambda\mathbf{x}\\
\mathbf{x}=(A^TA+2\lambda I)^{-1}A^T\mathbf{b}\\
\frac{\part L}{\part \lambda}=\mathbf{x}^T\mathbf{x}-1\\
$$
当 x 的范数超过 1 时，该导数是正的，所以为了跟随导数上坡并相对 λ 增加 Lagrangian，我们需要增加 λ。因为 $\mathbf{x}^⊤\mathbf{x}$ 的惩罚系数增加了，求解关于 x 的线性方程现在将得到具有较小范数的解。求解线性方程和调整 λ 的过程将一直持续到 x 具有正确的范数并且关于 λ 的导数是 0。 

