from flask import Flask, request, render_template, jsonify
import numpy as np
import tensorflow as tf
from PIL import Image
from flask_cors import CORS 
import os
import io

app = Flask(__name__)
CORS(app)

# Configuration
BEE_THRESHOLD = 0.6  # Confidence threshold for bee classification
DISEASE_CLASSES = ['healthy', 'varroa', 'wax moth']  # Update with your actual classes

# Disease recommendations
disease_recommendations = {
    'healthy': "The bee is healthy. No action needed.",
    'varroa': "Varroa mite detected. Recommendation: Use miticides like Apivar or formic acid treatment.",
    'wax moth': "Wax moth detected. Recommendation: Remove affected combs and freeze them to kill larvae."
}

# Load models
try:
    # Load bee detection model
    bee_interpreter = tf.lite.Interpreter(model_path='bee_model_improved_quant.tflite')
    bee_interpreter.allocate_tensors()
    bee_input_size = tuple(bee_interpreter.get_input_details()[0]['shape'][1:3])
    print("Bee model loaded successfully.")
    
    # Load disease classification model
    disease_interpreter = tf.lite.Interpreter(model_path='high_accuracy_model.tflite')
    disease_interpreter.allocate_tensors()
    disease_input_size = tuple(disease_interpreter.get_input_details()[0]['shape'][1:3])
    print("Disease model loaded successfully.")
except Exception as e:
    print(f"Error loading models: {e}")
    bee_interpreter = None
    disease_interpreter = None

def preprocess_image(file_stream, target_size):
    """Load and preprocess image for model prediction"""
    try:
        img = Image.open(io.BytesIO(file_stream)).convert('RGB')
        img = img.resize(target_size)
        img_array = np.array(img, dtype=np.float32) / 255.0
        img_array = np.expand_dims(img_array, axis=0)  # Add batch dimension
        return img_array
    except Exception as e:
        print(f"Error preprocessing image: {e}")
        return None

def run_inference(interpreter, input_data):
    """Run inference using TFLite model"""
    input_details = interpreter.get_input_details()
    output_details = interpreter.get_output_details()
    interpreter.set_tensor(input_details[0]['index'], input_data)
    interpreter.invoke()
    return interpreter.get_tensor(output_details[0]['index'])

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    if 'file' not in request.files:
        return jsonify({'error': 'No file uploaded'}), 400
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No file selected'}), 400
    
    try:
        # Read file into memory
        file_stream = file.read()
        
        # First run bee detection
        img_data = preprocess_image(file_stream, bee_input_size)
        if img_data is None:
            return jsonify({'error': 'Error processing image'}), 500
            
        bee_output = run_inference(bee_interpreter, img_data)
        
        # Interpret bee detection results
        if bee_output.shape[-1] == 2:  # Binary classification output
            is_bee = bee_output[0][1] > BEE_THRESHOLD
            bee_confidence = bee_output[0][1] if is_bee else bee_output[0][0]
        else:  # Single output (assuming < threshold = bee)
            is_bee = bee_output[0][0] < BEE_THRESHOLD
            bee_confidence = 1 - bee_output[0][0] if is_bee else bee_output[0][0]
        
        # Initialize result structure
        result = {
            'bee_detection': {
                'is_bee': bool(is_bee),
                'confidence': float(bee_confidence)
            },
            'disease_detection': None
        }
        
        # If bee is detected, run disease classification
        if is_bee and disease_interpreter:
            # Preprocess image for disease model if different size
            if bee_input_size != disease_input_size:
                img_data = preprocess_image(file_stream, disease_input_size)
                
            disease_output = run_inference(disease_interpreter, img_data)
            
            if len(disease_output[0]) == len(DISEASE_CLASSES):
                predicted_class = np.argmax(disease_output[0])
                disease_result = DISEASE_CLASSES[predicted_class]
                disease_confidence = float(np.max(disease_output[0]))
                
                result['disease_detection'] = {
                    'disease': disease_result,
                    'confidence': disease_confidence,
                    'recommendation': disease_recommendations.get(disease_result, "No specific recommendation available.")
                }
        
        return jsonify(result)
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)