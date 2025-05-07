from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import cv2
import numpy as np
import tensorflow as tf
from werkzeug.utils import secure_filename
import json
from datetime import datetime
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('E:/TeaXpert/backend/app.log'),
        logging.StreamHandler()
    ]
)

# Initialize Flask app
app = Flask(__name__)
CORS(app)

# Configuration
UPLOAD_FOLDER = "uploads"
ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg"}
MAX_FILE_SIZE = 5 * 1024 * 1024  # 5MB
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

# Ensure the upload folder exists
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

# Load trained AI model
MODEL_PATH = "E:/TeaXpert/backend/tea_model.h5"
try:
    model = tf.keras.models.load_model(MODEL_PATH)
    logging.info("Model loaded successfully")
    with open("class_info.json", "r") as f:
        class_info = json.load(f)
        CLASS_LABELS = class_info['class_names']
        CLASS_INDICES = class_info['class_indices']
    logging.info(f"Loaded class labels: {CLASS_LABELS}")
    logging.info(f"Loaded class indices: {CLASS_INDICES}")
except Exception as e:
    logging.error(f"Error loading model: {e}")
    CLASS_LABELS = ["Unknown Disease"]
    CLASS_INDICES = {}

def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS

def validate_image(file):
    """Validate image file."""
    if file.content_length > MAX_FILE_SIZE:
        return False, "File size exceeds 5MB limit"
    if not allowed_file(file.filename):
        return False, "Invalid file type. Allowed types: png, jpg, jpeg"
    return True, ""

@app.route("/ping")
def ping():
    return jsonify({"status": "success", "message": "pong", "timestamp": datetime.now().isoformat()})

@app.route("/")
def home():
    return jsonify({
        "status": "success",
        "message": "Tea Leaf Disease Detection Backend is Running!",
        "version": "1.0.0"
    })

@app.route("/upload", methods=["POST"])
def upload_file():
    """Handles image uploads and returns the detected disease."""
    try:
        if "image" not in request.files:
            return jsonify({
                "status": "error",
                "message": "No file uploaded",
                "timestamp": datetime.now().isoformat()
            }), 400

        file = request.files["image"]

        if file.filename == "":
            return jsonify({
                "status": "error",
                "message": "No selected file",
                "timestamp": datetime.now().isoformat()
            }), 400

        # Validate file
        is_valid, error_message = validate_image(file)
        if not is_valid:
            return jsonify({
                "status": "error",
                "message": error_message,
                "timestamp": datetime.now().isoformat()
            }), 400

        # Save file
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config["UPLOAD_FOLDER"], filename)
        file.save(filepath)

        # Process image and get disease prediction
        disease, percentage, confidence_scores = detect_disease(filepath)

        # Log prediction
        logging.info(f"Prediction - Disease: {disease}, Confidence: {percentage}%")

        return jsonify({
            "status": "success",
            "data": {
                "disease": disease,
                "confidence": percentage,
                "confidence_scores": confidence_scores,
                "timestamp": datetime.now().isoformat()
            }
        })

    except Exception as e:
        logging.error(f"Error processing request: {e}")
        return jsonify({
            "status": "error",
            "message": "Internal server error",
            "timestamp": datetime.now().isoformat()
        }), 500

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

        # Log detailed prediction information
        logging.info(f"Raw predictions: {predictions[0]}")
        logging.info(f"Predicted class index: {predicted_class}")
        logging.info(f"Predicted disease: {disease}")
        logging.info(f"Confidence scores: {confidence_scores}")

        # Check if confidence is too low
        if confidence < 30:
            logging.warning(f"Low confidence prediction: {confidence}%")
            return "Uncertain Prediction", confidence, confidence_scores

        return disease, confidence, confidence_scores
    except Exception as e:
        logging.error(f"Error in prediction: {e}")
        return "Error in Model", 0.0, {}

# ---- TIPS DATA ----
tips_data = {
    "anthracnose": [
        "Remove infected leaves and ensure proper air circulation.",
        "Use copper-based fungicides as a preventative measure.",
        "Maintain proper watering practices to avoid leaf diseases.",
        "Apply neem oil as a natural pesticide to combat pests.",
        "Ensure soil drainage to prevent fungal growth."
    ],
    "algal_leaf": [
        "Reduce watering frequency.",
        "Apply a suitable fungicide.",
        "Ensure good air circulation around the plants.",
        "Remove affected leaves promptly.",
        "Maintain proper soil pH levels."
    ],
    "bird_eye_spot": [
        "Use resistant plant varieties if available.",
        "Apply fungicides as recommended.",
        "Ensure proper spacing between plants.",
        "Remove fallen leaves and debris.",
        "Water plants in the morning to reduce humidity."
    ],
    "brown_blight": [
        "Prune infected areas of the plant.",
        "Avoid overhead watering.",
        "Apply fungicides as necessary.",
        "Ensure adequate sunlight for plants.",
        "Rotate crops to avoid soil-borne diseases."
    ]
}

@app.route('/api/tips/<disease_name>', methods=['GET'])
def get_tips(disease_name):
    """Fetch tips based on the disease name."""
    try:
        disease_name = disease_name.replace('_', ' ').lower()
        tips = tips_data.get(disease_name, ["No tips available for this disease."])
        return jsonify({
            "status": "success",
            "data": {
                "tips": tips,
                "timestamp": datetime.now().isoformat()
            }
        })
    except Exception as e:
        logging.error(f"Error fetching tips: {e}")
        return jsonify({
            "status": "error",
            "message": "Internal server error",
            "timestamp": datetime.now().isoformat()
        }), 500

if __name__ == "__main__":
    app.run(debug=True)
