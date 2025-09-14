# ===============================================================================
# 🐝 Hive Performance Model Evaluation
# Location: Badulla District, Sri Lanka
# Research-based ML model for precision apiculture
# ===============================================================================

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import json
from datetime import datetime
from sklearn.metrics import confusion_matrix, classification_report
import joblib
import os

def create_visualizations(results, X_test, y_test, best_model_name, best_model, feature_cols):
    """Create comprehensive visualizations"""
    print("\n📊 CREATING VISUALIZATIONS...")
    
    # Create outputs directory if it doesn't exist
    os.makedirs('outputs', exist_ok=True)
    
    fig, axes = plt.subplots(2, 2, figsize=(16, 12))
    
    # 1. Model Comparison
    comparison_data = []
    for model_name, metrics in results.items():
        comparison_data.append({
            'Model': model_name,
            'Accuracy': metrics['accuracy'],
            'F1-Score': metrics['f1_score'],
            'Critical Precision': metrics['critical_precision'],
            'Critical Recall': metrics['critical_recall']
        })
    
    df_comparison = pd.DataFrame(comparison_data)
    df_comparison.set_index('Model').plot(kind='bar', ax=axes[0, 0], width=0.8)
    axes[0, 0].set_title('🏆 Model Performance Comparison', fontsize=14, weight='bold')
    axes[0, 0].set_ylabel('Score')
    axes[0, 0].legend(bbox_to_anchor=(1.05, 1), loc='upper left')
    axes[0, 0].tick_params(axis='x', rotation=45)
    axes[0, 0].grid(True, alpha=0.3)
    
    # 2. Confusion Matrix
    cm = confusion_matrix(y_test, results[best_model_name]['predictions'])
    sns.heatmap(cm, annot=True, fmt='d', ax=axes[0, 1], cmap='Blues')
    axes[0, 1].set_title(f'🎯 Confusion Matrix - {best_model_name}', fontsize=14, weight='bold')
    axes[0, 1].set_xlabel('Predicted Performance Level')
    axes[0, 1].set_ylabel('Actual Performance Level')
    
    # 3. Performance Distribution
    performance_dist = pd.Series(y_test).value_counts().sort_index()
    colors = ['green', 'lightgreen', 'yellow', 'orange', 'red']
    bars = performance_dist.plot(kind='bar', ax=axes[1, 0],
                                color=colors[:len(performance_dist)])
    axes[1, 0].set_title('📊 Test Set Distribution', fontsize=14, weight='bold')
    axes[1, 0].set_xlabel('Performance Level')
    axes[1, 0].set_ylabel('Count')
    axes[1, 0].tick_params(axis='x', rotation=0)
    
    # Add count labels
    for bar in bars.patches:
        height = bar.get_height()
        axes[1, 0].text(bar.get_x() + bar.get_width()/2., height,
                       f'{int(height):,}', ha='center', va='bottom', weight='bold')
    
    # 4. Feature Importance
    if hasattr(best_model, 'feature_importances_'):
        importances = best_model.feature_importances_
        feature_imp = pd.DataFrame({
            'feature': feature_cols,
            'importance': importances
        }).sort_values('importance', ascending=False).head(10)
        
        y_pos = np.arange(len(feature_imp))
        axes[1, 1].barh(y_pos, feature_imp['importance'],
                       color=plt.cm.viridis(feature_imp['importance']/feature_imp['importance'].max()))
        axes[1, 1].set_yticks(y_pos)
        axes[1, 1].set_yticklabels(feature_imp['feature'])
        axes[1, 1].set_title(f'🔥 Top Features - {best_model_name}', fontsize=14, weight='bold')
        axes[1, 1].set_xlabel('Importance')
        
        # Add values on bars
        for i, v in enumerate(feature_imp['importance']):
            axes[1, 1].text(v + 0.001, i, f'{v:.3f}', va='center', weight='bold')
    
    plt.tight_layout()
    plt.savefig('outputs/model_evaluation.png', dpi=300, bbox_inches='tight')
    plt.show()
    
    # Save individual plots
    save_individual_plots(results, y_test, best_model_name, best_model, feature_cols)
    
    return fig

def save_individual_plots(results, y_test, best_model_name, best_model, feature_cols):
    """Save individual visualization plots"""
    
    # Confusion Matrix
    plt.figure(figsize=(8, 6))
    cm = confusion_matrix(y_test, results[best_model_name]['predictions'])
    sns.heatmap(cm, annot=True, fmt='d', cmap='Blues')
    plt.title(f'Confusion Matrix - {best_model_name}', fontsize=14, weight='bold')
    plt.xlabel('Predicted Performance Level')
    plt.ylabel('Actual Performance Level')
    plt.tight_layout()
    plt.savefig('outputs/confusion_matrix.png', dpi=300, bbox_inches='tight')
    plt.close()
    
    # Feature Importance
    if hasattr(best_model, 'feature_importances_'):
        plt.figure(figsize=(10, 8))
        importances = best_model.feature_importances_
        feature_imp = pd.DataFrame({
            'feature': feature_cols,
            'importance': importances
        }).sort_values('importance', ascending=False).head(15)
        
        plt.barh(range(len(feature_imp)), feature_imp['importance'],
                color=plt.cm.viridis(feature_imp['importance']/feature_imp['importance'].max()))
        plt.yticks(range(len(feature_imp)), feature_imp['feature'])
        plt.title('Feature Importances', fontsize=14, weight='bold')
        plt.xlabel('Importance')
        plt.gca().invert_yaxis()
        plt.tight_layout()
        plt.savefig('outputs/feature_importances.png', dpi=300, bbox_inches='tight')
        plt.close()

def generate_classification_report(results, y_test, best_model_name):
    """Generate and save detailed classification report"""
    print(f"\n📋 CLASSIFICATION REPORT - {best_model_name}:")
    print("=" * 60)
    
    target_names = ['Excellent', 'Good', 'Moderate', 'Poor', 'Critical']
    unique_levels = sorted(y_test.unique())
    
    # Adjust target names based on available levels
    if len(unique_levels) < len(target_names):
        report_names = [target_names[i] for i in unique_levels]
    else:
        report_names = target_names[:len(unique_levels)]
    
    report = classification_report(y_test, results[best_model_name]['predictions'],
                                 target_names=report_names, output_dict=True)
    
    # Print report
    print(classification_report(y_test, results[best_model_name]['predictions'],
                               target_names=report_names))
    
    # Save report to JSON
    report_data = {
        'model_name': best_model_name,
        'evaluation_date': datetime.now().isoformat(),
        'classification_report': report,
        'performance_summary': {
            'accuracy': results[best_model_name]['accuracy'],
            'f1_score': results[best_model_name]['f1_score'],
            'precision': results[best_model_name]['precision'],
            'recall': results[best_model_name]['recall'],
            'critical_precision': results[best_model_name]['critical_precision'],
            'critical_recall': results[best_model_name]['critical_recall']
        }
    }
    
    with open('outputs/classification_report.json', 'w') as f:
        json.dump(report_data, f, indent=2)
    
    print(f"\n✅ Classification report saved to: outputs/classification_report.json")
    
    return report

def evaluate_model_performance(model_path, scaler_path, test_data, feature_cols):
    """Load and evaluate saved model"""
    print("\n🔍 EVALUATING SAVED MODEL...")
    
    # Load model and scaler
    model = joblib.load(model_path)
    scaler = joblib.load(scaler_path)
    
    # Prepare test data
    X_test = test_data[feature_cols].fillna(0)
    y_test = test_data['performance_level'] - test_data['performance_level'].min()  # Adjust for 0-based
    
    # Scale features
    X_test_scaled = scaler.transform(X_test)
    
    # Make predictions
    y_pred = model.predict(X_test_scaled)
    y_pred_proba = model.predict_proba(X_test_scaled)
    
    # Calculate metrics
    from sklearn.metrics import accuracy_score, f1_score, precision_score, recall_score
    
    accuracy = accuracy_score(y_test, y_pred)
    f1 = f1_score(y_test, y_pred, average='macro')
    precision = precision_score(y_test, y_pred, average='macro', zero_division=0)
    recall = recall_score(y_test, y_pred, average='macro', zero_division=0)
    
    results = {
        'accuracy': accuracy,
        'f1_score': f1,
        'precision': precision,
        'recall': recall,
        'predictions': y_pred,
        'probabilities': y_pred_proba
    }
    
    print(f"✅ Model Evaluation Results:")
    print(f"   Accuracy: {accuracy:.3f}")
    print(f"   F1-Score: {f1:.3f}")
    print(f"   Precision: {precision:.3f}")
    print(f"   Recall: {recall:.3f}")
    
    return results, y_test

def main_evaluation(results=None, X_test=None, y_test=None, best_model_name=None, 
                   best_model=None, feature_cols=None):
    """Main evaluation pipeline"""
    print("📊 STARTING MODEL EVALUATION")
    print("=" * 50)
    
    try:
        if all(param is not None for param in [results, X_test, y_test, best_model_name, best_model, feature_cols]):
            # Use provided results from training
            print("Using results from training pipeline...")
        else:
            # Load saved model for evaluation
            print("Loading saved model for evaluation...")
            model_path = "models/performance_model.pkl"
            scaler_path = "models/scaler.pkl"
            
            if not os.path.exists(model_path):
                raise FileNotFoundError(f"Model file not found: {model_path}")
            
            # You would need to provide test data here
            # results, y_test = evaluate_model_performance(model_path, scaler_path, test_data, feature_cols)
            print("⚠️ Please provide test data for evaluation")
            return
        
        # Create visualizations
        create_visualizations(results, X_test, y_test, best_model_name, best_model, feature_cols)
        
        # Generate classification report
        generate_classification_report(results, y_test, best_model_name)
        
        print("\n🎉 EVALUATION COMPLETED SUCCESSFULLY!")
        print("📁 Output files saved to outputs/ directory")
        
    except Exception as e:
        print(f"❌ Error in evaluation pipeline: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    # Example usage - evaluate saved model
    main_evaluation()