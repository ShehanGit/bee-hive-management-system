import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error
import joblib
import numpy as np  # ✅ Import numpy for manual RMSE computation

def train_and_save_model(df: pd.DataFrame, model_path: str = "random_forest_model.pkl"):
    """
    Trains a Random Forest Regressor on the provided DataFrame and saves the model.
    
    :param df: DataFrame containing features and target variable.
    :param model_path: File path to save the trained model.
    """
    # 1. Prepare features (X) and target (y)
    X = df.drop(columns=['honey_production'])  # drop target column from features
    y = df['honey_production']
    
    # 2. Train-Test split
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    # 3. Train Random Forest
    rf = RandomForestRegressor(n_estimators=100, random_state=42)
    rf.fit(X_train, y_train)
    
    # 4. Evaluate Model (Fix `squared` argument issue)
    y_pred = rf.predict(X_test)
    
    # Compute Mean Squared Error
    mse = mean_squared_error(y_test, y_pred)
    rmse = np.sqrt(mse)  # ✅ FIXED: Compute RMSE manually
    print(f"Test RMSE: {rmse:.2f}")  # Output RMSE
    
    # 5. Save Model
    joblib.dump(rf, model_path)
    print(f"Model saved to {model_path}")

if __name__ == "__main__":
    from data_preprocessing import load_and_clean_data
    from feature_engineering import engineer_features
    
    # 1. Load and clean data
    data = load_and_clean_data(".\data\hive_data.xlsx")
    # 2. Engineer features
    data_fe = engineer_features(data)
    # 3. Train and save model
    train_and_save_model(data_fe, "random_forest_model.pkl")



