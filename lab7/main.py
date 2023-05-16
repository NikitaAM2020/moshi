import tensorflow as tf
from tensorflow.keras.datasets import mnist

# Завантаження даних
(x_train, y_train), (x_test, y_test) = mnist.load_data()

# Перетворення та нормалізація даних
x_train = x_train.reshape(-1, 28*28) / 255.0
x_test = x_test.reshape(-1, 28*28) / 255.0

# Побудова моделі нейронної мережі
model = tf.keras.models.Sequential([
    tf.keras.layers.Dense(128, activation='relu', input_shape=(28*28,)),
    tf.keras.layers.Dropout(0.2),
    tf.keras.layers.Dense(10, activation='softmax')
])

# Компіляція моделі
model.compile(optimizer='adam',
              loss='sparse_categorical_crossentropy',
              metrics=['accuracy'])

# Навчання моделі
model.fit(x_train, y_train, epochs=5, batch_size=32, validation_split=0.1)

# Оцінка точності на тестових даних
test_loss, test_accuracy = model.evaluate(x_test, y_test)
print('Точність на тестових даних:', test_accuracy)
