# -----------------------------------
#
# 02_02 深度前馈网络
#
# -----------------------------------

import numpy as np

import tensorflow as tf

tf.enable_eager_execution()

# -----------------------------------
# 1. 数据
# -----------------------------------

class DataLoader():
    def __init__(self):
        (train_images, train_labels), (test_images, test_labels) = tf.keras.datasets.mnist.load_data()
        train_images = train_images.reshape(-1, 28 * 28) / 255.0
        test_images = test_images.reshape(-1, 28 * 28) / 255.0
        self.train_data = train_images                     # np.array [55000, 784]
        self.train_labels = train_labels.astype(int)       # np.array [55000] of int32
        self.eval_data = test_images                       # np.array [10000, 784]
        self.eval_labels = test_labels.astype(int)         # np.array [10000] of int32

    def get_batch(self, batch_size):
        index = np.random.randint(0, np.shape(self.train_data)[0], batch_size)
        return self.train_data[index, :], self.train_labels[index]

# -----------------------------------
# 2. 模型
# -----------------------------------

class MLP(tf.keras.Model):
    def __init__(self):
        super().__init__()
        self.dense1 = tf.keras.layers.Dense(units=100, activation=tf.nn.relu)
        self.dense2 = tf.keras.layers.Dense(units=10)

    def call(self, inputs):
        x = self.dense1(inputs)
        x = self.dense2(x)
        return x

    def predict(self, inputs):
        logits = self(inputs)
        return tf.argmax(logits, axis=-1)

# -----------------------------------
# 3. 训练
# -----------------------------------

num_batches = 1000
batch_size = 50
learning_rate = 0.001

model = MLP()
data_loader = DataLoader()
optimizer = tf.train.AdamOptimizer(learning_rate=learning_rate)

for batch_index in range(num_batches):
    X, y = data_loader.get_batch(batch_size)
    with tf.GradientTape() as tape:
        y_logit_pred = model(tf.convert_to_tensor(X))
        loss = tf.losses.sparse_softmax_cross_entropy(labels=y, logits=y_logit_pred)
        print("batch %d: loss %f" % (batch_index, loss.numpy()))
    grads = tape.gradient(loss, model.variables)
    optimizer.apply_gradients(grads_and_vars=zip(grads, model.variables))

# -----------------------------------
# 4. 预测
# -----------------------------------

num_eval_samples = np.shape(data_loader.eval_labels)[0]
y_pred = model.predict(data_loader.eval_data).numpy()
print("test accuracy: %f" % (sum(y_pred == data_loader.eval_labels) / num_eval_samples))
