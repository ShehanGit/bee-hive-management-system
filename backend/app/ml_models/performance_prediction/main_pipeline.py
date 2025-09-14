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
from prediction_service_performance import HivePerformancePredictor
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
        
        best_model, scaler, results, X_test, y_test, best_model_name = training_results
        print(f"✅ Model training completed. Best model: {best_model_name}")
        
        # Step 3: Model Evaluation
        print("\n📊 STEP 3: MODEL EVALUATION")
        print("-" * 40)
        main_evaluation(results, X_test, y_test, best_model_name, best_model, feature_cols)
        print("✅ Model evaluation completed.")
        
        # Step 4: Test Prediction Service
        print("\n🔮 STEP 4: TESTING PREDICTION SERVICE")
        print("-" * 40)
        predictor = HivePerformancePredictor()
        
        # Create sample prediction
        sample_data = {
            'collection_timestamp': '2024-12-01 14:30:00',
            'hive_id': 'HIVE_001',
            'weather_temperature': 28.5,
            'weather_humidity': 65.0,
            'weather_wind_speed': 12.0,
            'weather_light_intensity': 45000.0,
            'weather_rainfall': 0.0,
            'sensor_temperature': 35.2,
            'sensor_humidity': 55.0,
            'sensor_sound': 75.0,
            'sensor_weight': 45.2
        }
        
        prediction = predictor.predict_single(sample_data)
        print(f"✅ Prediction service test: Level {prediction.get('predicted_level', 'Error')}")
        
        # Step 5: Test Alert System
        print("\n🚨 STEP 5: TESTING ALERT SYSTEM")
        print("-" * 40)
        alert_store = HivePerformanceAlertStore()
        alerts = alert_store.analyze_prediction_for_alerts('HIVE_001', prediction, sample_data)
        print(f"✅ Alert system test: {len(alerts)} alerts generated")
        
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
            'predictor': predictor,
            'alert_store': alert_store
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
        import pandas as pd
        
        # Load data
        data = pd.read_csv(input_file)
        print(f"📊 Loaded {len(data)} observations from {input_file}")
        
        # Initialize predictor
        predictor = HivePerformancePredictor()
        
        # Make predictions
        predictions = predictor.predict_batch(data)
        
        # Convert to DataFrame
        results_df = pd.DataFrame(predictions)
        
        # Save results
        if output_file is None:
            output_file = f"outputs/predictions_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
        
        results_df.to_csv(output_file, index=False)
        print(f"💾 Predictions saved to: {output_file}")
        
        # Summary
        level_counts = results_df['predicted_level'].value_counts().sort_index()
        print(f"\n📊 PREDICTION SUMMARY:")
        for level, count in level_counts.items():
            print(f"   Level {level}: {count} hives")
        
        # Alert analysis
        alert_store = HivePerformanceAlertStore()
        total_alerts = 0
        
        for prediction in predictions:
            if 'error' not in prediction:
                alerts = alert_store.analyze_prediction_for_alerts(
                    prediction.get('hive_id', f"HIVE_{prediction.get('observation_id', 0)}"),
                    prediction
                )
                total_alerts += len(alerts)
        
        print(f"🚨 Generated {total_alerts} alerts")
        
        return results_df, total_alerts
        
    except Exception as e:
        print(f"❌ Prediction failed: {str(e)}")
        return None, 0

def monitor_hive_realtime():
    """Simulate real-time hive monitoring"""
    print("📡 REAL-TIME HIVE MONITORING SIMULATION")
    print("=" * 45)
    
    import time
    import random
    import numpy as np
    
    predictor = HivePerformancePredictor()
    alert_store = HivePerformanceAlertStore()
    
    hives = ['HIVE_001', 'HIVE_002', 'HIVE_003']
    
    print("Starting monitoring... (Press Ctrl+C to stop)")
    
    try:
        iteration = 0
        while iteration < 10:  # Limited for demo
            iteration += 1
            print(f"\n📊 Monitoring Cycle {iteration}")
            
            for hive_id in hives:
                # Simulate sensor data
                sensor_data = {
                    'collection_timestamp': datetime.now().isoformat(),
                    'hive_id': hive_id,
                    'weather_temperature': np.random.normal(27, 3),
                    'weather_humidity': np.random.normal(70, 10),
                    'weather_wind_speed': np.random.normal(15, 5),
                    'weather_light_intensity': np.random.normal(40000, 10000),
                    'weather_rainfall': 0 if random.random() > 0.2 else np.random.exponential(2),
                    'sensor_temperature': np.random.normal(35, 2),
                    'sensor_humidity': np.random.normal(60, 8),
                    'sensor_sound': np.random.normal(70, 15),
                    'sensor_weight': 40 + np.random.normal(0, 2)
                }
                
                # Make prediction
                prediction = predictor.predict_single(sensor_data)
                
                if 'error' not in prediction:
                    print(f"   {hive_id}: Level {prediction['predicted_level']} ({prediction['confidence']:.1%})")
                    
                    # Generate alerts if needed
                    alerts = alert_store.analyze_prediction_for_alerts(hive_id, prediction, sensor_data)
                    if alerts:
                        print(f"      🚨 {len(alerts)} new alerts")
                else:
                    print(f"   {hive_id}: Error - {prediction['error']}")
            
            time.sleep(2)  # Wait 2 seconds between cycles
        
        # Show final summary
        summary = alert_store.get_alert_summary()
        print(f"\n📊 MONITORING SUMMARY:")
        print(f"   Total Alerts: {summary['total_alerts']}")
        print(f"   Active Alerts: {summary['active_alerts']}")
        print(f"   Hives with Alerts: {len(summary.get('hive_breakdown', {}))}")
        
    except KeyboardInterrupt:
        print("\n⏹️ Monitoring stopped by user")
    except Exception as e:
        print(f"❌ Monitoring error: {str(e)}")

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
            try:
                predictor = HivePerformancePredictor()
                info = predictor.get_model_info()
                print(f"   Model: {info['model_name']}")
                print(f"   Features: {info['feature_count']}")
                print(f"   Trained: {info['training_date']}")
            except:
                print("⚠️ Model exists but cannot be loaded")
        else:
            print("❌ Model: Not found - run training first")
        
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