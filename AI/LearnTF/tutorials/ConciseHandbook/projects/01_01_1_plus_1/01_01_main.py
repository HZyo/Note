# -----------------------------------
#
# 01_01 1+1
#
# -----------------------------------

import tensorflow as tf

tf.enable_eager_execution()

# -----------------------------------
# 1. 科学计算库
# -----------------------------------

a = tf.constant(1)
b = tf.constant(1)
c = tf.add(a, b)    # 也可以直接写 c = a + b，两者等价

# tf.Tensor(2, shape=(), dtype=int32)
print(c)

A = tf.constant([[1, 2], [3, 4]])
B = tf.constant([[5, 6], [7, 8]])
C = tf.matmul(A, B)

# tf.Tensor(
#[[19 22]
# [43 50]], shape=(2, 2), dtype=int32)
print(C)

# -----------------------------------
# 2. 自动求导
# -----------------------------------

x = tf.get_variable('x', shape=[1], initializer=tf.constant_initializer(3.))

# 在 tf.GradientTape() 的上下文内，所有计算步骤都会被记录以用于求导
with tf.GradientTape() as tape : y = tf.square(x)

y_grad = tape.gradient(y, x)        # 计算y关于x的导数
# 9, 6
print([y.numpy(), y_grad.numpy()])

X = tf.constant([[1., 2.], [3., 4.]])
y = tf.constant([[1.], [2.]])
w = tf.get_variable('w', shape=[2, 1], initializer=tf.constant_initializer([[1.], [2.]]))
b = tf.get_variable('b', shape=[1], initializer=tf.constant_initializer([1.]))

with tf.GradientTape() as tape : L = 0.5 * tf.reduce_sum(tf.square(tf.matmul(X, w) + b - y))

w_grad, b_grad = tape.gradient(L, [w, b])        # 计算L(w, b)关于w, b的偏导数
print([L.numpy(), w_grad.numpy(), b_grad.numpy()])
