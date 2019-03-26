# 02_01 模型与层

本章介绍如何使用TensorFlow快速搭建动态模型。

前置知识：

- [Python面向对象](http://www.runoob.com/python3/python3-class.html) （在Python内定义类和方法、类的继承、构造和析构函数，[使用super()函数调用父类方法](http://www.runoob.com/python/python-func-super.html) ，[使用__call__()方法对实例进行调用](https://www.liaoxuefeng.com/wiki/0014316089557264a6b348958f449949df42a6d3a2e542c000/0014319098638265527beb24f7840aa97de564ccc7f20f6000) 等）；
- 多层感知机、卷积神经网络、循环神经网络和强化学习（每节之前给出参考资料）。

```python
import tensorflow as tf

tf.enable_eager_execution()
```

## 1. 模型基础

如上一章所述，为了增强代码的可复用性，我们往往会将模型编写为类，然后在模型调用的地方使用 `y_pred = model(X)` 的形式进行调用。 **模型类** 的形式非常简单，主要包含 `__init__()` （构造函数，初始化）和 `call(input)` （模型调用）两个方法，但也可以根据需要增加自定义的方法。

```python
class MyModel(tf.keras.Model):
    def __init__(self):
        super().__init__()     # Python 2 下使用 super(MyModel, self).__init__()
        # 此处添加初始化代码（包含call方法中会用到的层）

    def call(self, inputs):
        # 此处添加模型调用的代码（处理输入并返回输出）
        return output
```

在这里，我们的模型类继承了 `tf.keras.Model` 。Keras是一个用Python编写的高级神经网络API，现已得到TensorFlow的官方支持和内置。继承 `tf.keras.Model` 的一个好处在于我们可以使用父类的若干方法和属性，例如在实例化类后可以通过 `model.variables` 这一属性直接获得模型中的所有变量，免去我们一个个显式指定变量的麻烦。

## 2. 线性模型

同时，我们引入 **“层”（Layer）** 的概念，层可以视为比模型粒度更细的组件单位，将计算流程和变量进行了封装。我们可以使用层来快速搭建模型。

上一章中简单的线性模型 `y_pred = tf.matmul(X, w) + b` ，我们可以通过模型类的方式编写如下：

```python
class Linear(tf.keras.Model):
    def __init__(self):
        super().__init__()
        self.dense = tf.keras.layers.Dense(units=1, kernel_initializer=tf.zeros_initializer(),
            bias_initializer=tf.zeros_initializer())

    def call(self, input):
        output = self.dense(input)
        return output
```

这里，我们没有显式地声明 `w` 和 `b` 两个变量并写出 `y_pred = tf.matmul(X, w) + b` 这一线性变换，而是在初始化部分实例化了一个全连接层（ `tf.keras.layers.Dense` ），并在call方法中对这个层进行调用。全连接层封装了 `output = activation(tf.matmul(input, kernel) + bias)` 这一线性变换+激活函数的计算操作，以及 `kernel` 和 `bias` 两个变量。当不指定激活函数时（即 `activation(x) = x` ），这个全连接层就等价于我们上述的线性变换。顺便一提，全连接层可能是我们编写模型时使用最频繁的层。

如果我们需要显式地声明自己的变量并使用变量进行自定义运算，请参考 [自定义层](https://tf.wiki/zh/models.html#custom-layer)。

```python
X = tf.constant([[1.0, 2.0, 3.0], [4.0, 5.0, 6.0]])
y = tf.constant([[10.0], [20.0]])

# 以下代码结构与前节类似
model = Linear()
optimizer = tf.train.GradientDescentOptimizer(learning_rate=0.01)

for i in range(100):
    with tf.GradientTape() as tape:
        y_pred = model(X)      # 调用模型
        loss = tf.reduce_mean(tf.square(y_pred - y))
    grads = tape.gradient(loss, model.variables)
    optimizer.apply_gradients(grads_and_vars=zip(grads, model.variables))
    
print(model.variables)
```

