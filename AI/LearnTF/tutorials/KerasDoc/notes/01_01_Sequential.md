# 01_01. Sequential

依赖项

```python
from keras.models import Sequential
from keras.layers import Dense, Activation
```

## 1. 搭建模型

你可以通过将网络层实例的列表传递给 `Sequential` 的构造器，来创建一个 `Sequential` 模型：

```python
model = Sequential([
    Dense(32, input_shape=(784,)),
    Activation('relu'),
    Dense(10),
    Activation('softmax'),
])
```

也可以简单地使用 `.add()` 方法将各层添加到模型中：

```python
model = Sequential()
model.add(Dense(32, input_shape=(784,)))
model.add(Activation('relu'))
# ...
```

## 2. 指定输入数据的尺寸

模型需要知道它所期望的输入的尺寸。出于这个原因，顺序模型中的**第一层**（且只有第一层，因为下面的层可以自动地推断尺寸）需要接收关于其输入尺寸的信息。

传递一个 `input_shape` 参数给第一层。它是一个表示尺寸的元组 (一个整数或 `None` 的元组，其中 `None` 表示可能为任何正整数)。在 `input_shape`中**不包含数据的 batch 大小**。

```python
model = Sequential()
model.add(Dense(32, input_shape=(784,)))
```

> **其他方式** 
>
> - 某些 2D 层，例如 `Dense`，支持通过参数 `input_dim` 指定输入尺寸，某些 3D 时序层支持 `input_dim` 和 `input_length` 参数。
> - 如果你需要为你的输入指定一个固定的 batch 大小（这对 stateful RNNs 很有用），你可以传递一个 `batch_size` 参数给一个层。如果你同时将 `batch_size=32` 和 `input_shape=(6, 8)` 传递给一个层，那么每一批输入的尺寸就为 `(32，6，8)`。
>
> ```python
> model = Sequential()
> model.add(Dense(32, input_dim=784))
> ```

## 3. 模型编译

在训练模型之前，您需要配置学习过程，这是通过 `compile` 方法完成的。它接收三个参数：

- 优化器 `optimizer`。它可以是**现有优化器的字符串标识符**，如 `rmsprop` 或 `adagrad`，也可以是 `Optimizer` **类**的实例。详见：[optimizers](https://keras-zh.readthedocs.io/optimizers)。
- 损失函数 `loss`，模型试图最小化的**目标函数**。它可以是**现有损失函数的字符串标识符**，如 `categorical_crossentropy` 或 `mse`，也可以是一个目标**函数**。详见：[losses](https://keras-zh.readthedocs.io/losses)。
- 评估标准 `metrics`。对于任何分类问题，你都希望将其设置为 `metrics = ['accuracy']`。评估标准可以是**现有的标准的字符串标识符**，也可以是自定义的评估标准**函数**。

> 示例
>
> ```python
> # 多分类问题
> model.compile(optimizer='rmsprop',
>               loss='categorical_crossentropy',
>               metrics=['accuracy'])
> 
> # 二分类问题
> model.compile(optimizer='rmsprop',
>               loss='binary_crossentropy',
>               metrics=['accuracy'])
> 
> # 均方误差回归问题
> model.compile(optimizer='rmsprop',
>               loss='mse')
> 
> # 自定义评估标准函数
> import keras.backend as K
> 
> def mean_pred(y_true, y_pred):
>     return K.mean(y_pred)
> 
> model.compile(optimizer='rmsprop',
>               loss='binary_crossentropy',
>               metrics=['accuracy', mean_pred])
> ```

## 4. 模型训练

Keras 模型在输入数据和标签的 Numpy 矩阵上进行训练。为了训练一个模型，你通常会使用 `fit` 函数。[文档详见此处](https://keras-zh.readthedocs.io/models/sequential)。

> 示例
>
> ```python
> model.fit(data, labels, epochs=10, batch_size=32)
> ```

## 5. 样例

在 [examples 目录](https://github.com/keras-team/keras/tree/master/examples) 中，可以找到**真实数据集**的示例模型

以下都是**非真实数据集**的样例

### 5.1 基于 MLP 的 softmax 多分类

```python
import numpy as np
from keras.models import Sequential
from keras.layers import Dense, Dropout
from keras.optimizers import SGD

# 生成虚拟数据
x_train = np.random.random((1000, 20))
# y_train.shape : (1000, 10), one-hot
y_train = keras.utils.to_categorical(np.random.randint(10, size=(1000, 1)), num_classes=10)
x_test = np.random.random((100, 20))
y_test = keras.utils.to_categorical(np.random.randint(10, size=(100, 1)), num_classes=10)

model = Sequential()
model.add(Dense(64, activation='relu', input_dim=20))
model.add(Dropout(0.5))
model.add(Dense(64, activation='relu'))
model.add(Dropout(0.5))
model.add(Dense(10, activation='softmax'))

model.summary()

sgd = SGD(lr=0.01, decay=1e-6, momentum=0.9, nesterov=True)
model.compile(loss='categorical_crossentropy',
              optimizer=sgd,
              metrics=['accuracy'])

model.fit(x_train, y_train,
          epochs=20,
          batch_size=128)
score = model.evaluate(x_test, y_test, batch_size=128)
print("loss: {0}, acc: {1}".format(*score))
```

### 5.2 基于 MLP 的 sigmoid 二分类

```python
import numpy as np
from keras.models import Sequential
from keras.layers import Dense, Dropout

# 生成虚拟数据
x_train = np.random.random((1000, 20))
y_train = np.random.randint(2, size=(1000, 1))
x_test = np.random.random((100, 20))
y_test = np.random.randint(2, size=(100, 1))

model = Sequential()
model.add(Dense(64, activation='relu', input_dim=20))
model.add(Dropout(0.5))
model.add(Dense(64, activation='relu'))
model.add(Dropout(0.5))
model.add(Dense(1, activation='sigmoid'))

model.summary()

model.compile(loss='binary_crossentropy',
              optimizer='rmsprop',
              metrics=['accuracy'])

model.fit(x_train, y_train,
          epochs=20,
          batch_size=128)
score = model.evaluate(x_test, y_test, batch_size=128)
print("loss: {0}, acc: {1}".format(*score))
```

### 5.3 类似 VGG 的 CNN

```python
import numpy as np
import keras
from keras.models import Sequential
from keras.layers import Dense, Dropout, Flatten
from keras.layers import Conv2D, MaxPooling2D
from keras.optimizers import SGD

# 生成虚拟数据
# 100 x [ width 100, height 100, channel 3 ]
x_train = np.random.random((100, 100, 100, 3))
y_train = keras.utils.to_categorical(np.random.randint(10, size=(100, 1)), num_classes=10)
x_test = np.random.random((20, 100, 100, 3))
y_test = keras.utils.to_categorical(np.random.randint(10, size=(20, 1)), num_classes=10)

model.summary()

model = Sequential()
# 输入: 3 通道 100x100 像素图像 -> (100, 100, 3) 张量。
# 使用 32 个大小为 3x3 的卷积滤波器。
model.add(Conv2D(32, (3, 3), activation='relu', input_shape=(100, 100, 3)))
model.add(Conv2D(32, (3, 3), activation='relu'))
model.add(MaxPooling2D(pool_size=(2, 2)))
model.add(Dropout(0.25))

model.add(Conv2D(64, (3, 3), activation='relu'))
model.add(Conv2D(64, (3, 3), activation='relu'))
model.add(MaxPooling2D(pool_size=(2, 2)))
model.add(Dropout(0.25))

model.add(Flatten())
model.add(Dense(256, activation='relu'))
model.add(Dropout(0.5))
model.add(Dense(10, activation='softmax'))

sgd = SGD(lr=0.01, decay=1e-6, momentum=0.9, nesterov=True)
model.compile(loss='categorical_crossentropy', optimizer=sgd, metrics=['accuracy'])

model.fit(x_train, y_train, batch_size=32, epochs=10)
score = model.evaluate(x_test, y_test, batch_size=32)
print("loss: {0}, acc: {1}".format(*score))
```

### 5.4 基于 LSTM 的序列分类

数据生成是我自己写的，仅供参考

```python
import numpy as np
from keras.models import Sequential
from keras.layers import Dense, Dropout
from keras.layers import Embedding
from keras.layers import LSTM
from keras.preprocessing import sequence

max_features = 1024

len_train = np.random.randint(20, size=(1000, 1))
x_train = np.array([np.random.randint(10, size=(len_train[i])).tolist() for i in range(1000)])
x_train = sequence.pad_sequences(x_train, maxlen = 20, padding = 'post', value = 10)
y_train = np.random.randint(2, size=(1000, 1))

len_test = np.random.randint(20, size=(100, 1))
x_test = np.array([np.random.randint(10, size=(len_test[i])).tolist() for i in range(100)])
x_test = sequence.pad_sequences(x_test, maxlen = 20, padding = 'post', value = 10)
y_test = np.random.randint(2, size=(100, 1))

model = Sequential()
model.add(Embedding(max_features, output_dim=256))
model.add(LSTM(128))
model.add(Dropout(0.5))
model.add(Dense(1, activation='sigmoid'))

model.summary()

model.compile(loss='binary_crossentropy',
              optimizer='rmsprop',
              metrics=['accuracy'])

model.fit(x_train, y_train, batch_size=16, epochs=10)
score = model.evaluate(x_test, y_test, batch_size=16)
print("loss: {0}, acc: {1}".format(*score))
```

