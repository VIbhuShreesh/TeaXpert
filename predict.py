import sys
import cv2
import tensorflow as tf
import numpy as np
import logging

# Load model and other necessary variables
MODEL_PATH = "E:/TeaXpert/backend/tea_model.h5"
model = tf.keras.models.load_model(MODEL_PATH)

CLASS_LABELS = ['Anthracnose', 'algal leaf', 'bird eye spot', 'brown blight', 'gray light', 'healthy', 'red leaf spot', 'white spot']
logging.basicConfig(level=logging.INFO)

def preprocess_image(image_path):
    """Loads and preprocesses an image for model prediction."""
    try:
        image = cv2.imread(image_path)
        if image is None:
            raise ValueError("Could not read image")

        # Convert to RGB
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

        # Resize with aspect ratio preservation
        h, w = image.shape[:2]
        if h > w:
            new_h = 224
            new_w = int(w * (224 / h))
        else:
            new_w = 224
            new_h = int(h * (224 / w))

        image = cv2.resize(image, (new_w, new_h))

        # Pad to make square
        pad_h = (224 - new_h) // 2
        pad_w = (224 - new_w) // 2
        image = cv2.copyMakeBorder(image, pad_h, 224 - new_h - pad_h,
                                 pad_w, 224 - new_w - pad_w,
                                 cv2.BORDER_CONSTANT, value=[0, 0, 0])

        # Normalize
        image = image / 255.0
        image = np.expand_dims(image, axis=0)
        return image
    except Exception as e:
        logging.error(f"Error preprocessing image: {e}")
        return None

def detect_disease(image_path):
    """Predicts the disease using the trained model."""
    image = preprocess_image(image_path)
    if image is None:
        return "Invalid Image", 0.0, {}

    try:
        predictions = model.predict(image, verbose=0)
        predicted_class = np.argmax(predictions)
        disease = CLASS_LABELS[predicted_class]
        confidence = round(np.max(predictions) * 100, 2)

        # Get confidence scores for all classes
        confidence_scores = {
            CLASS_LABELS[i]: round(score * 100, 2)
            for i, score in enumerate(predictions[0])
        }

        logging.info(f"Predicted class: {disease} with {confidence}% confidence")
        return disease, confidence, confidence_scores
    except Exception as e:
        logging.error(f"Error in prediction: {e}")
        return "Error in Model", 0.0, {}

if __name__ == "__main__":
    # Ensure the script receives the image path as a command-line argument
    if len(sys.argv) < 2:
        print("Usage: python predict.py <image_path>")
        sys.exit(1)

    image_path = sys.argv[1]  # Get image path from command-line argument

    disease, confidence, all_scores = detect_disease(image_path)

    print(f"Disease: {disease}")
    print(f"Confidence: {confidence}%")
    print(f"All Scores: {all_scores}")
