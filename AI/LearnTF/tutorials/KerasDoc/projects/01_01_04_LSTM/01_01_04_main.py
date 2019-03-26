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
