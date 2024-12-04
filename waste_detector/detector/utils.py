import numpy as np
import cv2
from tensorflow.keras.models import load_model

# Load the waste detection model once when the server starts
model = load_model('detector/models/waste_model.keras')

# Map of predictions to waste categories
WASTE_MAP = {
    0: 'PLASTC',
    1: 'PLASTIC_BOTTLE',
    2: 'DISPOSABLE_CUP',
    3: 'PAPER'
}

def preprocess_image(image_path, target_size=(64, 64)):
    """
    Preprocesses an image for the waste detection model.
    :param image_path: Path to the input image.
    :param target_size: Target size for resizing the image.
    :return: Preprocessed image ready for prediction.
    """
    # Read the image in RGB format
    image = cv2.imread(image_path)
    if image is None:
        raise ValueError("Error reading the image. Please check the file path.")
    
    # Resize the image
    image_resized = cv2.resize(image, target_size)

    # Normalize pixel values to [0, 1]
    image_normalized = image_resized / 255.0

    # Expand dimensions to match model input (1, height, width, 3)
    preprocessed_image = np.expand_dims(image_normalized, axis=0)
    return preprocessed_image

def predict_waste(image_path):
    """
    Predicts the waste category of an image.
    :param image_path: Path to the input image.
    :return: Predicted waste category.
    """
    try:
        # Preprocess the image
        preprocessed_image = preprocess_image(image_path)

        # Predict using the model
        predictions = model.predict(preprocessed_image)
        predicted_class = np.argmax(predictions)

        # Map the predicted class to a waste category
        waste_category = WASTE_MAP.get(predicted_class, "Unknown")

        return waste_category
    except Exception as e:
        return f"Prediction error: {str(e)}"
