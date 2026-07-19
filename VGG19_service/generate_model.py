import tensorflow as tf
from tensorflow.keras.applications import VGG19
from tensorflow.keras.models import Model
from tensorflow.keras.layers import Dense, GlobalAveragePooling2D
import os

model_path = 'VGG19.keras'
if os.path.exists(model_path):
    print("Model already exists.")
    exit(0)

print("Building VGG19 model for music genre classification...")
base = VGG19(weights='imagenet', include_top=False, input_shape=(288, 432, 3))
x = GlobalAveragePooling2D()(base.output)
x = Dense(256, activation='relu')(x)
output = Dense(10, activation='softmax', name='genre')(x)
model = Model(inputs=base.input, outputs=output)
model.compile(optimizer='adam', loss='categorical_crossentropy')
model.save(model_path)
print(f"Model saved to {model_path}")
