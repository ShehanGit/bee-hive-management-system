import pandas as pd
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
import joblib
import numpy as np  # ✅ Import NumPy for RMSE calculation

def evaluate_model(df: pd.DataFrame, model_path: str = "random_forest_model.pkl"):
    """
    Loads a trained model and evaluates it on the given DataFrame.
    
    :param df: The DataFrame with features and target.
    :param model_path: Path to the trained model file.
    """
    # 1. Load trained model
    model = joblib.load(model_path)
    
    # 2. Prepare features (X) and target (y)
    X = df.drop(columns=['honey_production'])
    y = df['honey_production']
    
    # 3. Predict using the model
    predictions = model.predict(X)
    
    # 4. Compute metrics
    mae = mean_absolute_error(y, predictions)
    mse = mean_squared_error(y, predictions)
    rmse = np.sqrt(mse)  # ✅ FIXED: Compute RMSE manually
    r2 = r2_score(y, predictions)

    print(f"Model Evaluation Results:")
    print(f"Mean Absolute Error (MAE): {mae:.4f}")
    print(f"Root Mean Squared Error (RMSE): {rmse:.4f}")
    print(f"R² Score: {r2:.4f}")

if __name__ == "__main__":
    from data_preprocessing import load_and_clean_data
    from feature_engineering import engineer_features

    # ✅ FIX: Ensure proper file path format
    data = load_and_clean_data("../data/hive_data.xlsx")  # Fixed path
    data_fe = engineer_features(data)
    
    evaluate_model(data_fe, "random_forest_model.pkl")
