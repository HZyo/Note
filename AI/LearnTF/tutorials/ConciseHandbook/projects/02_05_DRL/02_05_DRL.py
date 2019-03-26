# -----------------------------------
#
# 02_05 深度强化学习
#
# -----------------------------------

import tensorflow as tf
import numpy as np

import random
from collections import deque

tf.enable_eager_execution()

# -----------------------------------
# 1. 游戏
# -----------------------------------

import gym

env = gym.make('CartPole-v1')       # 实例化一个游戏环境，参数为游戏名称

# -----------------------------------
# 2. 模型
# -----------------------------------

# Q-network用于拟合Q函数，和前节的多层感知机类似
# 输入state，输出各个action下的Q-value（CartPole下为2维）。
class QNetwork(tf.keras.Model):
    def __init__(self):
        super().__init__()
        self.dense1 = tf.keras.layers.Dense(units=24, activation=tf.nn.relu)
        self.dense2 = tf.keras.layers.Dense(units=24, activation=tf.nn.relu)
        self.dense3 = tf.keras.layers.Dense(units=2)

    def call(self, inputs):
        x = self.dense1(inputs)
        x = self.dense2(x)
        x = self.dense3(x)
        return x

    def predict(self, inputs):
        q_values = self(inputs)
        return tf.argmax(q_values, axis=-1)

# -----------------------------------
# 3. 训练
# -----------------------------------

num_episodes = 128
num_exploration_episodes = 64
max_len_episode = 1000
batch_size = 32
learning_rate = 1e-3
gamma = 1.
initial_epsilon = 1.
final_epsilon = 0.01

model = QNetwork()
optimizer = tf.train.AdamOptimizer(learning_rate=learning_rate)
replay_buffer = deque(maxlen=10000)

for episode_id in range(num_episodes):
    # 初始化环境，获得初始状态
    state = env.reset()
    epsilon = max(
        initial_epsilon * (num_exploration_episodes - episode_id) / num_exploration_episodes,
        final_epsilon)

    for t in range(max_len_episode):
        env.render()                # 对当前帧进行渲染，绘图到屏幕
        if random.random() < epsilon:               # epsilon-greedy探索策略
            action = env.action_space.sample()      # 以epsilon的概率选择随机动作
        else:
            action = model.predict(
                tf.constant(np.expand_dims(state, axis=0), dtype=tf.float32)).numpy()
            action = action[0]

        # 让环境执行动作，获得执行完动作的下一个状态，动作的奖励，游戏是否已结束以及额外信息
        next_state, reward, done, info = env.step(action)
        # 如果游戏Game Over，给予大的负奖励
        reward = -10. if done else reward
        # 将(state, action, reward, next_state)的四元组（外加done标签表示是否结束）放入经验重放池
        replay_buffer.append((state, action, reward, next_state, 1 if done else 0))
        state = next_state

        # 游戏结束则退出本轮循环，进行下一个episode
        if done:
            print("episode %d, epsilon %f, score %d" % (episode_id, epsilon, t))
            break

        if len(replay_buffer) >= batch_size:
            # 从经验回放池中随机取一个batch的四元组，并分别转换为NumPy数组
            batch_state, batch_action, batch_reward, batch_next_state, batch_done = zip(
                *random.sample(replay_buffer, batch_size))
            batch_state, batch_reward, batch_next_state, batch_done = \
                [np.array(a, dtype=np.float32) for a in [batch_state, batch_reward, batch_next_state, batch_done]]
            batch_action = np.array(batch_action, dtype=np.int32)

            q_value = model(tf.constant(batch_next_state, dtype=tf.float32))
            
            # 按照论文计算y值
            y = batch_reward + (gamma * tf.reduce_max(q_value, axis=1)) * (1 - batch_done)
            with tf.GradientTape() as tape:
                # 最小化y和Q-value的距离
                loss = tf.losses.mean_squared_error(
                    labels=y,
                    predictions=tf.reduce_sum(model(tf.constant(batch_state)) *
                                              tf.one_hot(batch_action, depth=2), axis=1)
                )

            # 计算梯度并更新参数
            grads = tape.gradient(loss, model.variables)
            optimizer.apply_gradients(grads_and_vars=zip(grads, model.variables))
