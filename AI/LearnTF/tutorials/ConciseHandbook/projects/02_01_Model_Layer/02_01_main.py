# -----------------------------------
#
# 02_01 模型与层
#
# -----------------------------------

import tensorflow as tf

tf.enable_eager_execution()

# -----------------------------------
# 1. 模型基础
# -----------------------------------

class MyModel(tf.keras.Model):
    def __init__(self):
        super().__init__()     # Python 2 下使用 super(MyModel, self).__init__()
        # 此处添加初始化代码（包含call方法中会用到的层）

    def call(self, inputs):
        # 此处添加模型调用的代码（处理输入并返回输出）
        return output

# -----------------------------------
# 2. 线性模型
# -----------------------------------
   
class Linear(tf.keras.Model):
    def __init__(self):
        super().__init__()
        self.dense = tf.keras.layers.Dense(units=1, kernel_initializer=tf.zeros_initializer(),
            bias_initializer=tf.zeros_initializer())

    def call(self, input):
        output = self.dense(input)
        return output

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
