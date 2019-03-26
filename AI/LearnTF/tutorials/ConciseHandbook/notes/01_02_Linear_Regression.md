# 01_02 线性回归

考虑一个实际问题，某城市在2013年-2017年的房价如下表所示：

| 年份 | 2013  | 2014  | 2015  | 2016  | 2017  |
| ---- | ----- | ----- | ----- | ----- | ----- |
| 房价 | 12000 | 14000 | 15000 | 16500 | 17500 |

现在，我们希望通过对该数据进行线性回归，即使用线性模型 $y=wx+b$ 来拟合上述数据，此处 `a` 和 `b` 是待求的参数。

```python
import numpy as np

import tensorflow as tf

tf.enable_eager_execution()
```

## 1. 数据

首先，我们定义数据，进行基本的归一化操作。

```python
X_raw = np.array([2013, 2014, 2015, 2016, 2017], dtype=np.float32)
y_raw = np.array([12000, 14000, 15000, 16500, 17500], dtype=np.float32)

X = (X_raw - X_raw.mean()) / X_raw.std()
y = (y_raw - y_raw.mean()) / y_raw.std()
```

## 2. 理论

接下来，我们使用梯度下降方法来求线性模型中两个参数 `w` 和 `b` 的值 。

回顾机器学习的基础知识，对于多元函数 $f(x)​$ 求局部极小值，梯度下降的过程如下：

- 初始化自变量为 $x_0$ ， $k=0$ 

- 迭代进行下列步骤直到满足收敛条件：

  > - 求函数 $f(x)$ 关于自变量的梯度 $\nabla_x f(x_k)​$ 
  > - 更新自变量： $x_{k+1}=x_k-\alpha\nabla_x f(x_k)$ 。这里 $\alpha​$ 是学习率（也就是梯度下降一次迈出的“步子”大小）
  > - $k\gets k+1​$ 

接下来，我们考虑如何使用程序来实现梯度下降方法，求得线性回归的解
$$
\begin{align}
\min _ { w , b } L ( w , b ) 
&= \min _ { w , b } \sum _ { i = 1 } ^ { n } \left( w x ^ { ( i ) } + b - y ^ { ( i ) } \right) ^ { 2 } \\
&= \min _ { w , b } \| X w + b - Y \|_2^2\\
\end{align}
$$
偏导为
$$
\begin{align}
\frac{\part L}{\part w}&=X^\top(Xw+b-Y)\\
\frac{\part L}{\part b}&=1_{n \times 1}^\top(Xw+b-Y)\\
\end{align}
$$

## 3. Numpy

机器学习模型的实现并不是TensorFlow的专利。事实上，对于简单的模型，即使使用常规的科学计算库或者工具也可以求解。在这里，我们使用NumPy这一通用的科学计算库来实现梯度下降方法。NumPy提供了多维数组支持，可以表示向量、矩阵以及更高维的张量。同时，也提供了大量支持在多维数组上进行操作的函数（比如下面的 `np.dot()` 是求内积， `np.sum()` 是求和）。在这方面，NumPy和MATLAB比较类似。在以下代码中，我们手工求损失函数关于参数 `a` 和 `b` 的偏导数，并使用梯度下降法反复迭代，最终获得 `w` 和 `b` 的值。

```python
w, b = 0, 0

num_epoch = 1000
learning_rate = 1e-3
for e in range(num_epoch):
    # 手动计算损失函数关于自变量（模型参数）的梯度
    y_pred = w * X + b
    grad_w, grad_b = (y_pred - y).dot(X), (y_pred - y).sum()

    # 更新参数
    w, b = w - learning_rate * grad_w, b - learning_rate * grad_b

print(w, b)
```

然而，你或许已经可以注意到，使用常规的科学计算库实现机器学习模型有两个痛点：

- 经常需要手工求函数关于参数的偏导数。如果是简单的函数或许还好，但一旦函数的形式变得复杂（尤其是深度学习模型），手工求导的过程将变得非常痛苦，甚至不可行。
- 经常需要手工根据求导的结果更新参数。这里使用了最基础的梯度下降方法，因此参数的更新还较为容易。但如果使用更加复杂的参数更新方法（例如Adam或者Adagrad），这个更新过程的编写同样会非常繁杂。

而TensorFlow等深度学习框架的出现很大程度上解决了这些痛点，为机器学习模型的实现带来了很大的便利。

## 4. TensorFlow

TensorFlow的 **Eager Execution（动态图）模式** 与上述NumPy的运行方式十分类似，然而提供了更快速的运算（GPU支持）、自动求导、优化器等一系列对深度学习非常重要的功能。以下展示了如何使用TensorFlow计算线性回归。可以注意到，程序的结构和前述NumPy的实现非常类似。这里，TensorFlow帮助我们做了两件重要的工作：

```python
X = tf.constant(X)
y = tf.constant(y)

w = tf.get_variable('w', dtype=tf.float32, shape=[], initializer=tf.zeros_initializer)
b = tf.get_variable('b', dtype=tf.float32, shape=[], initializer=tf.zeros_initializer)
variables = [w, b]

num_epoch = 1000
optimizer = tf.train.GradientDescentOptimizer(learning_rate=1e-3)
for e in range(num_epoch):
    # 使用tf.GradientTape()记录损失函数的梯度信息
    with tf.GradientTape() as tape:
        y_pred = w * X + b
        loss = 0.5 * tf.reduce_sum(tf.square(y_pred - y))
    # TensorFlow自动计算损失函数关于自变量（模型参数）的梯度
    grads = tape.gradient(loss, variables)
    # TensorFlow自动根据梯度更新参数
    optimizer.apply_gradients(grads_and_vars=zip(grads, variables))
```

在这里，我们使用了前文的方式计算了损失函数关于参数的偏导数。同时，使用 `tf.train.GradientDescentOptimizer(learning_rate=1e-3)` 声明了一个梯度下降 **优化器** （Optimizer），其学习率为1e-3。优化器可以帮助我们根据计算出的求导结果更新模型参数，从而最小化某个特定的损失函数，具体使用方式是调用其 `apply_gradients()` 方法。

注意到这里，更新模型参数的方法 `optimizer.apply_gradients()` 需要提供参数 `grads_and_vars`，即待更新的变量（如上述代码中的 `variables` ）及损失函数关于这些变量的偏导数（如上述代码中的 `grads` ）。具体而言，这里需要传入一个Python列表（List），列表中的每个元素是一个（变量的偏导数，变量）对。比如这里是 `[(grad_w, w), (grad_b, b)]` 。我们通过 `grads = tape.gradient(loss, variables)` 求出tape中记录的 `loss` 关于 `variables = [w, b]` 中每个变量的偏导数，也就是 `grads = [grad_w, grad_b]`，再使用Python的 `zip()` 函数将 `grads = [grad_w, grad_b]` 和 `vars = [w, b]` 拼装在一起，就可以组合出所需的参数了。

在实际应用中，我们编写的模型往往比这里一行就能写完的线性模型 `y_pred = tf.matmul(X, w) + b`要复杂得多。所以，我们往往会编写一个模型类，然后在需要调用的时候使用 `y_pred = model(X)` 进行调用。关于模型类的编写方式可见 [下章](https://tf.wiki/zh/models.html)。

