# ===============================================================================
# 🐝 Hive Performance Model Training
# Location: Badulla District, Sri Lanka
# Research-based ML model for precision apiculture
# ===============================================================================

import pandas as pd
import numpy as np
import joblib
import json
from datetime import datetime
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import MinMaxScaler
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier, ExtraTreesClassifier
from sklearn.metrics import (accuracy_score, precision_score, recall_score, f1_score)

# Try importing XGBoost safely
try:
    import xgboost
    from xgboost import XGBClassifier
    XGBOOST_AVAILABLE = True
    print("✅ XGBoost imported successfully")
except ImportError:
    print("⚠️ XGBoost not available - using alternative models")
    XGBOOST_AVAILABLE = False

def train_models(data, feature_cols):
    """Train and compare multiple machine learning models"""
    print("\n🤖 TRAINING MACHINE LEARNING MODELS...")
    
    # Prepare features
    X = data[feature_cols].fillna(0)
    y = data['performance_level']
    
    # Fix: shift labels so they always start from 0 (needed for XGBoost)
    y = y - y.min()
    
    print(f"Features: {len(feature_cols)}")
    print(f"Samples: {len(X)}")
    print(f"Target distribution:\n{y.value_counts().sort_index()}")
    
    # Split data
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.15, random_state=42, stratify=y
    )
    
    # Scale features
    scaler = MinMaxScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)
    
    print(f"Training set: {X_train.shape[0]:,} samples")
    print(f"Test set: {X_test.shape[0]:,} samples")
    
    # Define models based on XGBoost availability
    if XGBOOST_AVAILABLE:
        models = {
            'Random Forest': RandomForestClassifier(
                n_estimators=200, max_depth=15, random_state=42, n_jobs=-1
            ),
            'XGBoost': XGBClassifier(
                n_estimators=200, max_depth=8, learning_rate=0.1,
                random_state=42, eval_metric='mlogloss', verbosity=0
            ),
            'Gradient Boosting': GradientBoostingClassifier(
                n_estimators=150, max_depth=6, learning_rate=0.1, random_state=42
            )
        }
    else:
        models = {
            'Random Forest': RandomForestClassifier(
                n_estimators=200, max_depth=15, random_state=42, n_jobs=-1
            ),
            'Extra Trees': ExtraTreesClassifier(
                n_estimators=200, max_depth=15, random_state=42, n_jobs=-1
            ),
            'Gradient Boosting': GradientBoostingClassifier(
                n_estimators=150, max_depth=6, learning_rate=0.1, random_state=42
            )
        }
    
    results = {}
    trained_models = {}
    
    # Train each model
    for model_name, model in models.items():
        print(f"\n🔧 Training {model_name}...")
        
        # Train model
        model.fit(X_train, y_train)
        
        # Make predictions
        y_pred = model.predict(X_test)
        y_pred_proba = model.predict_proba(X_test)
        
        # Calculate metrics
        accuracy = accuracy_score(y_test, y_pred)
        f1 = f1_score(y_test, y_pred, average='macro')
        precision = precision_score(y_test, y_pred, average='macro', zero_division=0)
        recall = recall_score(y_test, y_pred, average='macro', zero_division=0)
        
        # Critical levels performance (levels 4 & 5)
        critical_mask = y_test >= 3  # Adjusted for 0-based indexing
        if critical_mask.sum() > 0:
            critical_precision = precision_score(y_test >= 3, y_pred >= 3, zero_division=0)
            critical_recall = recall_score(y_test >= 3, y_pred >= 3, zero_division=0)
        else:
            critical_precision = critical_recall = 0.0
        
        results[model_name] = {
            'accuracy': accuracy,
            'f1_score': f1,
            'precision': precision,
            'recall': recall,
            'critical_precision': critical_precision,
            'critical_recall': critical_recall,
            'predictions': y_pred,
            'probabilities': y_pred_proba
        }
        
        trained_models[model_name] = model
        
        print(f"✅ {model_name} Results:")
        print(f"   Accuracy: {accuracy:.3f}")
        print(f"   F1-Score: {f1:.3f}")
        print(f"   Critical Precision: {critical_precision:.3f}")
        print(f"   Critical Recall: {critical_recall:.3f}")
    
    # Select best model
    best_model_name = max(results.keys(), key=lambda k: results[k]['f1_score'])
    best_model = trained_models[best_model_name]
    
    print(f"\n🏆 BEST MODEL: {best_model_name}")
    best_results = results[best_model_name]
    print(f"📊 Final Performance:")
    print(f"   🎯 Accuracy: {best_results['accuracy']:.1%}")
    print(f"   📈 F1-Score: {best_results['f1_score']:.1%}")
    print(f"   🚨 Critical Precision: {best_results['critical_precision']:.1%}")
    print(f"   🚨 Critical Recall: {best_results['critical_recall']:.1%}")
    
    return best_model, scaler, results, X_test, y_test, best_model_name

def save_model_artifacts(best_model, scaler, feature_cols, best_model_name):
    """Save trained model and associated artifacts"""
    print(f"\n💾 SAVING MODEL ARTIFACTS...")
    
    # Save model
    model_filename = "models/performance_model.pkl"
    joblib.dump(best_model, model_filename)
    
    # Save scaler
    scaler_filename = "models/scaler.pkl"  
    joblib.dump(scaler, scaler_filename)
    
    # Save model metadata
    model_info = {
        'model_name': best_model_name,
        'feature_columns': feature_cols,
        'performance_levels': {
            0: 'Excellent - Strong nectar flow, high activity',
            1: 'Good - Consistent foraging, stable growth',
            2: 'Moderate - Maintenance phase',
            3: 'Poor - Consuming stored honey, stress signs',
            4: 'Critical - Significant stress, intervention needed'
        },
        'model_files': {
            'model': model_filename,
            'scaler': scaler_filename
        },
        'training_date': datetime.now().isoformat(),
        'model_type': 'hive_performance_prediction'
    }
    
    with open('models/performance_model_meta.json', 'w') as f:
        json.dump(model_info, f, indent=2)
    
    print(f"✅ Model saved: {model_filename}")
    print(f"✅ Scaler saved: {scaler_filename}")
    print(f"✅ Metadata saved: models/performance_model_meta.json")
    
    return model_filename, scaler_filename

def train_pipeline(data, feature_cols):
    """Complete training pipeline"""
    print("🚀 STARTING HIVE PERFORMANCE MODEL TRAINING")
    print("=" * 60)
    
    try:
        # Train models
        best_model, scaler, results, X_test, y_test, best_model_name = train_models(data, feature_cols)
        
        # Save model artifacts
        model_file, scaler_file = save_model_artifacts(best_model, scaler, feature_cols, best_model_name)
        
        print("\n🎉 TRAINING COMPLETED SUCCESSFULLY!")
        print("=" * 50)
        print("Your hive performance prediction model is ready!")
        print(f"🤖 Best Model: {best_model_name}")
        print(f"📁 Model Files: {model_file}, {scaler_file}")
        
        return best_model, scaler, results, X_test, y_test, best_model_name
        
    except Exception as e:
        print(f"❌ Error in training pipeline: {str(e)}")
        import traceback
        traceback.print_exc()
        return None

if __name__ == "__main__":
    from data_preprocessing_performance import preprocess_data
    
    # Example usage
    file_path = "data/hive_data.csv"
    data, feature_cols = preprocess_data(file_path)
    
    # Train model
    results = train_pipeline(data, feature_cols)
    if results:
        print("Training completed successfully!")