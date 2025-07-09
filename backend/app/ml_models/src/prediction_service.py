from flask import Flask, request, jsonify
from flask_cors import CORS  # Import CORS from flask_cors
import pandas as pd
import joblib
from feature_engineering import engineer_features  # Assuming this is in your project

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Load the model once when the app starts
model = joblib.load("random_forest_model.pkl")
expected_features = model.feature_names_in_  # Ensure your model supports this attribute

def prepare_input_data(input_data: dict) -> pd.DataFrame:
    """
    Convert JSON input data to a pandas DataFrame,
    apply feature engineering, and ensure all expected features are present.
    """
    df = pd.DataFrame(input_data)
    
    # Engineer features using your custom function
    df = engineer_features(df)
    
    # Add any missing features with a default value (e.g., 0)
    for col in expected_features:
        if col not in df.columns:
            df[col] = 0

    # Reorder columns to match the model's expectations
    df = df[expected_features]
    return df

@app.route('/predict', methods=['POST', 'OPTIONS'])
def predict():
    """
    Expects a JSON payload that can be converted to a pandas DataFrame.
    Returns predictions from the pre-loaded model.
    """
    if request.method == 'OPTIONS':
        return '', 200  # Handle CORS preflight request
    
    # Get JSON data from the request
    data = request.get_json(force=True)
    
    # Prepare the input data
    input_df = prepare_input_data(data)
    
    # Get predictions from the model
    predictions = model.predict(input_df)
    
    # Return the predictions as JSON
    return jsonify({'predictions': predictions.tolist()})

if __name__ == "__main__":
    # Run the Flask app on localhost, port 8080
    app.run(host='0.0.0.0', port=5002, debug=True)