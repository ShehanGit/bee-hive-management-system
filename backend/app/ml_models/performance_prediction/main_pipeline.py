# ===============================================================================
# 🐝 Hive Performance Prediction - Main Pipeline
# Location: Badulla District, Sri Lanka
# Research-based ML model for precision apiculture
# ===============================================================================

import os
import sys
import argparse
from datetime import datetime

# Add src directory to path
sys.path.append('src')

from data_preprocessing_performance import preprocess_data, get_feature_columns
from train_performance_model import train_pipeline
from evaluate_performance_model import main_evaluation
# Note: Prediction service will be available after training
# from prediction_service_performance import HivePerformancePredictor
from alert_store import HivePerformanceAlertStore

def setup_directories():
    """Create necessary directories for the project"""
    directories = ['data', 'models', 'outputs', 'src']
    
    for directory in directories:
        os.makedirs(directory, exist_ok=True)
        print(f"✅ Directory ready: {directory}/")

def full_training_pipeline(data_file):
    """Complete training pipeline from data to trained model"""
    print("🚀 STARTING FULL HIVE PERFORMANCE PREDICTION PIPELINE")
    print("=" * 80)

    try:
        # Setup directories
        setup_directories()

        # Step 1: Data Preprocessing
        print("\n📊 STEP 1: DATA PREPROCESSING")
        print("-" * 40)
        processed_data, feature_cols = preprocess_data(data_file)
        print(f"✅ Data preprocessing completed. Shape: {processed_data.shape}")

        # Step 2: Model Training
        print("\n🤖 STEP 2: MODEL TRAINING")
        print("-" * 40)
        training_results = train_pipeline(processed_data, feature_cols)

        if training_results is None:
            print("❌ Training failed!")
            return None

        # ✅ Fixed unpacking (now expects 8 values)
        best_model, scaler, results, X_test, y_test, best_model_name, label_mapping, le = training_results
        print(f"✅ Model training completed. Best model: {best_model_name}")

        # Step 3: Model Evaluation
        print("\n📊 STEP 3: MODEL EVALUATION")
        print("-" * 40)
        main_evaluation(results, X_test, y_test, best_model_name, best_model, feature_cols)

        print("✅ Model evaluation completed.")

        # Note: Prediction service testing skipped (model needs to be trained first)
        # Use the API endpoint /performance/predict for real-time predictions
        print("\n⚠️ NOTE: Prediction service will be available after model is trained")
        print("   Use the Flask API endpoint /performance/predict for predictions")

        print("\n🎉 PIPELINE COMPLETED SUCCESSFULLY!")
        print("=" * 60)
        print("Your hive performance prediction system is ready!")
        print(f"📁 Model files: models/performance_model.pkl")
        print(f"📊 Outputs: outputs/ directory")
        print(f"🚨 Alerts: outputs/alerts.json")

        return {
            'model': best_model,
            'scaler': scaler,
            'results': results,
            'model_name': best_model_name
        }

    except Exception as e:
        print(f"❌ Pipeline failed: {str(e)}")
        import traceback
        traceback.print_exc()
        return None

def predict_from_file(input_file, output_file=None):
    """Make predictions on new data from file"""
    print("🔮 MAKING PREDICTIONS FROM FILE")
    print("=" * 40)
    
    try:
        print("⚠️ Note: Batch prediction from file not yet implemented for weekly aggregation model")
        print("   Use the API endpoint /performance/predict for real-time predictions")
        print("   Or train the model first using: python main_pipeline.py train --data data/hive_data3.csv")
        
        return None, 0
        
    except Exception as e:
        print(f"❌ Prediction failed: {str(e)}")
        return None, 0

def monitor_hive_realtime():
    """Simulate real-time hive monitoring"""
    print("📡 REAL-TIME HIVE MONITORING SIMULATION")
    print("=" * 45)
    print("⚠️ Note: Real-time monitoring requires trained model")
    print("   Train the model first, then use the Flask API endpoint")
    print("   For monitoring, call: POST /performance/predict")

def main():
    """Main function with command line interface"""
    parser = argparse.ArgumentParser(description='🐝 Hive Performance Prediction System')
    
    parser.add_argument('command', choices=['train', 'predict', 'monitor', 'status'],
                       help='Command to execute')
    parser.add_argument('--data', type=str, help='Path to data file')
    parser.add_argument('--input', type=str, help='Input file for predictions')
    parser.add_argument('--output', type=str, help='Output file for predictions')
    
    args = parser.parse_args()
    
    if args.command == 'train':
        if not args.data:
            print("❌ --data argument required for training")
            return
        
        if not os.path.exists(args.data):
            print(f"❌ Data file not found: {args.data}")
            return
        
        result = full_training_pipeline(args.data)
        if result:
            print("✅ Training completed successfully!")
        else:
            print("❌ Training failed!")
    
    elif args.command == 'predict':
        if not args.input:
            print("❌ --input argument required for predictions")
            return
        
        if not os.path.exists(args.input):
            print(f"❌ Input file not found: {args.input}")
            return
        
        results, alerts = predict_from_file(args.input, args.output)
        if results is not None:
            print("✅ Predictions completed successfully!")
        else:
            print("❌ Prediction failed!")
    
    elif args.command == 'monitor':
        monitor_hive_realtime()
    
    elif args.command == 'status':
        print("📊 SYSTEM STATUS")
        print("=" * 30)
        
        # Check if model exists
        model_path = "models/performance_model.pkl"
        if os.path.exists(model_path):
            print("✅ Model: Available")
            stat = os.stat(model_path)
            print(f"   File size: {stat.st_size / 1024:.1f} KB")
            print(f"   Modified: {datetime.fromtimestamp(stat.st_mtime)}")
        else:
            print("❌ Model: Not found - run training first")
            print("   Command: python main_pipeline.py train --data data/hive_data3.csv")
        
        # Check alerts
        alert_store = HivePerformanceAlertStore()
        summary = alert_store.get_alert_summary()
        print(f"🚨 Alerts: {summary['active_alerts']} active, {summary['resolved_alerts']} resolved")
        
        # Check directories
        directories = ['data', 'models', 'outputs', 'src']
        for directory in directories:
            if os.path.exists(directory):
                files = len(os.listdir(directory))
                print(f"📁 {directory}/: {files} files")
            else:
                print(f"❌ {directory}/: Not found")

if __name__ == "__main__":
    # If no command line arguments, run demo
    if len(sys.argv) == 1:
        print("🐝 HIVE PERFORMANCE PREDICTION SYSTEM")
        print("=" * 50)
        print("Usage examples:")
        print("  python main_pipeline.py train --data data/hive_data.csv")
        print("  python main_pipeline.py predict --input data/new_data.csv")
        print("  python main_pipeline.py monitor")
        print("  python main_pipeline.py status")
        print("\nFor demo with sample data, ensure you have:")
        print("  - data/bee_performance_dataset_synthetic.csv")
        print("\nRunning status check...")
        
        import sys
        sys.argv = ['main_pipeline.py', 'status']
        main()
    else:
        main()
