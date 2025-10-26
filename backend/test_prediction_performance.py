"""Test prediction performance to find bottleneck"""
import sys
import os
import time
from datetime import datetime, timedelta

# Add the app directory to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'app'))

from app import create_app
from app.models.synchronized_data import SynchronizedData
from app.services.performance_prediction_service import predict_latest_performance

def test_prediction():
    print("=" * 70)
    print("🔍 TESTING PREDICTION PERFORMANCE")
    print("=" * 70)
    
    app = create_app()
    
    with app.app_context():
        # Test the actual prediction
        print("\n🚀 Testing actual prediction...")
        start = time.time()
        
        try:
            result = predict_latest_performance(hive_id=1)
            elapsed = time.time() - start
            
            print(f"\n✅ Prediction completed in {elapsed:.2f}s")
            print(f"Success: {result.get('success')}")
            
            if result.get('success'):
                pred = result.get('prediction', {})
                print(f"Predicted Level: {pred.get('predicted_level')}")
                print(f"Confidence: {pred.get('confidence', 0):.2%}")
                print(f"Data Points: {pred.get('data_points_used', 0)}")
            else:
                print(f"Error: {result.get('error')}")
                
        except Exception as e:
            elapsed = time.time() - start
            print(f"\n❌ Prediction failed after {elapsed:.2f}s")
            print(f"Error: {str(e)}")
            import traceback
            traceback.print_exc()
    
    print("\n" + "=" * 70)
    print("✅ Test complete")
    print("=" * 70)

if __name__ == "__main__":
    test_prediction()

