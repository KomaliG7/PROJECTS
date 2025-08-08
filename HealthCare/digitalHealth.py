import os
import cv2
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import pickle

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder, StandardScaler
from tensorflow.keras.utils import to_categorical
from tensorflow.keras.models import Model
from tensorflow.keras.layers import Input, Dense, Dropout, Flatten, Conv2D, MaxPooling2D, Concatenate
from tensorflow.keras.optimizers import Adam

# === Load Structured Data ===
input_cols = ['Name', 'Age', 'Gender', 'Blood Type', 'Medical Condition', 'Medication']
target_col = 'Test Results'

data = pd.read_csv('healthcare_dataset.csv')

# Encode target column
label_encoder_target = LabelEncoder()
data[target_col] = label_encoder_target.fit_transform(data[target_col])

# Separate input and output
x_structured = data[input_cols].copy()
y_structured = data[target_col].copy()

# Encode categorical columns
label_encoders = {}
for col in x_structured.select_dtypes(include=['object']).columns:
    le = LabelEncoder()
    x_structured.loc[:, col] = le.fit_transform(x_structured[col])
    label_encoders[col] = le

# Scale numerical columns
scaler = StandardScaler()
x_structured = scaler.fit_transform(x_structured)

# === Load Image Data ===
IMG_SIZE = 128

def loaddataset(basepath):
    X, Y = [], []
    for label, folder in enumerate(['no', 'yes']):
        folder_path = os.path.join(basepath, folder)
        for file in os.listdir(folder_path):
            path = os.path.join(folder_path, file)
            img = cv2.imread(path, 0)
            if img is None:
                continue
            img = cv2.resize(img, (IMG_SIZE, IMG_SIZE))
            img = img.reshape(IMG_SIZE, IMG_SIZE, 1)
            X.append(img)
            Y.append(label)
    return np.array(X), np.array(Y)

image_path = r"C:\Users\KOMALIG\OneDrive\future dealer\OneDrive\Internship\TRAINING\25.Medical Diagnosis of Brain Tumour\dataset"
X_image, Y_image = loaddataset(image_path)
X_image = X_image.astype("float32") / 255.0
Y_image = to_categorical(Y_image)

# === Align structured & image data lengths ===
min_samples = min(len(X_image), len(x_structured))
X_image = X_image[:min_samples]
Y_image = Y_image[:min_samples]
x_structured = x_structured[:min_samples]
y_structured = y_structured[:min_samples]

# === Train-test split together for alignment ===
X_train_image, X_test_image, x_train_structured, x_test_structured, y_train_image, y_test_image = train_test_split(
    X_image, x_structured, Y_image, test_size=0.2, random_state=2
)

# === Build Multimodal Model ===
image_input = Input(shape=(128, 128, 1))
x = Conv2D(32, (3, 3), activation="relu")(image_input)
x = MaxPooling2D(pool_size=(2, 2))(x)
x = Conv2D(32, (3, 3), activation="relu")(x)
x = MaxPooling2D(pool_size=(2, 2))(x)
x = Flatten()(x)

structured_input = Input(shape=(x_train_structured.shape[1],))
y = Dense(64, activation='relu')(structured_input)

combined = Concatenate()([x, y])
z = Dense(128, activation='relu')(combined)
z = Dropout(0.3)(z)
z = Dense(2, activation='softmax')(z)

model = Model(inputs=[image_input, structured_input], outputs=z)
model.compile(optimizer=Adam(), loss='categorical_crossentropy', metrics=['accuracy'])

# === Train Model ===
hist = model.fit(
    [X_train_image, x_train_structured],
    y_train_image,
    batch_size=16,
    epochs=10,
    validation_split=0.2,
    shuffle=True,
    verbose=2
)

# === Save Model and Preprocessors ===
os.makedirs('Model', exist_ok=True)
model.save_weights('Model/model_weights.h5')

with open("Model/model.json", "w") as json_file:
    json_file.write(model.to_json())

with open('Model/history.pckl', 'wb') as f:
    pickle.dump(hist.history, f)

with open('Model/label_encoders.pkl', 'wb') as f:
    pickle.dump(label_encoders, f)

with open('Model/scaler.pkl', 'wb') as f:
    pickle.dump(scaler, f)

# === Evaluate Model ===
loss, accuracy = model.evaluate([X_test_image, x_test_structured], y_test_image, verbose=0)
print(f"Test Loss: {loss:.4f}")
print(f"Test Accuracy: {accuracy:.4f}")

# === Plot Performance ===
acc = hist.history['accuracy']
val_acc = hist.history['val_accuracy']
losses = hist.history['loss']
val_losses = hist.history['val_loss']

plt.figure(figsize=(12, 5))
plt.subplot(1, 2, 1)
plt.plot(acc, label='Train Accuracy')
plt.plot(val_acc, label='Val Accuracy')
plt.title('Model Accuracy')
plt.legend()

plt.subplot(1, 2, 2)
plt.plot(losses, label='Train Loss')
plt.plot(val_losses, label='Val Loss')
plt.title('Model Loss')
plt.legend()
plt.show()
