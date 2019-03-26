# -----------------------------------
#
# 01_02 线性回归
#
# -----------------------------------

import numpy as np

import tensorflow as tf

tf.enable_eager_execution()

# -----------------------------------
# 1. 数据
# -----------------------------------

X_raw = np.array([2013, 2014, 2015, 2016, 2017], dtype=np.float32)
y_raw = np.array([12000, 14000, 15000, 16500, 17500], dtype=np.float32)

X = (X_raw - X_raw.mean()) / X_raw.std()
y = (y_raw - y_raw.mean()) / y_raw.std()

# -----------------------------------
# 2. 理论
# -----------------------------------

# -----------------------------------
# 3. Numpy
# -----------------------------------

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

# -----------------------------------
# 4. TensorFlow
# -----------------------------------

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

print(w, b)
