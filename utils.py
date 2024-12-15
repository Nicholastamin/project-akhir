from keras.models import load_model
from PIL import Image, ImageOps
import numpy as np

def load_keras_model(model_path):
    """Fungsi untuk memuat model Keras."""
    model = load_model(model_path,compile=False)
    return model

def load_class_names(labels_path):
    """Fungsi untuk memuat label kelas dari file."""
    with open(labels_path, "r", encoding="utf-8") as f:
        class_names = f.readlines()
    return class_names

def predict_class(model, class_names, image_path):
    """Fungsi untuk melakukan prediksi kelas."""
    # Nonaktifkan notasi ilmiah
    np.set_printoptions(suppress=True)

    # Persiapkan gambar
    data = np.ndarray(shape=(1, 224, 224, 3), dtype=np.float32)
    image = Image.open(image_path).convert("RGB")
    size = (224, 224)
    image = ImageOps.fit(image, size, Image.Resampling.LANCZOS)
    image_array = np.asarray(image)
    normalized_image_array = (image_array.astype(np.float32) / 127.5) - 1
    data[0] = normalized_image_array

    # Prediksi
    prediction = model.predict(data)
    index = np.argmax(prediction)
    class_name = class_names[index].strip()  # Hapus spasi
    confidence_score = prediction[0][index]

    return class_name, confidence_score