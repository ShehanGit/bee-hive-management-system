import os
import sys
from datetime import datetime, timedelta
from sqlalchemy import create_engine, text
from dotenv import load_dotenv
import pandas as pd
import numpy as np

load_dotenv()

def check_arima_readiness():
    """Check if data is suitable for ARIMA forecasting"""
    
    print("=" * 80)
    print("🔍 ARIMA FORECASTING READINESS CHECK")
    print("=" * 80)
    
    database_url = os.getenv('DATABASE_URL', 'mysql+pymysql://root:root@localhost/hive_db')
    
    try:
        engine = create_engine(database_url, pool_pre_ping=True)
        
        with engine.connect() as conn:
            
            # 1. Check data availability
            print("\n1️⃣ DATA AVAILABILITY")
            print("-" * 80)
            
            result = conn.execute(text("""
                SELECT 
                    COUNT(*) as total_records,
                    MIN(collection_timestamp) as first_record,
                    MAX(collection_timestamp) as last_record,
                    COUNT(DISTINCT DATE(collection_timestamp)) as days_of_data
                FROM synchronized_data
                WHERE weather_temperature IS NOT NULL 
                AND sensor_sound IS NOT NULL
            """))
            
            summary = result.fetchone()
            total_records = summary[0]
            days_of_data = summary[3]
            
            print(f"Total Records: {total_records}")
            print(f"First Record:  {summary[1]}")
            print(f"Last Record:   {summary[2]}")
            print(f"Days of Data:  {days_of_data}")
            
            if summary[1] and summary[2]:
                duration = summary[2] - summary[1]
                hours = duration.total_seconds() / 3600
                print(f"Duration:      {hours:.1f} hours ({days_of_data} days)")
                
                if total_records > 0:
                    freq = hours / total_records * 60
                    print(f"Avg Frequency: ~{freq:.1f} minutes between records")
            
            # ARIMA Requirements Check
            print("\n✅ ARIMA Requirements:")
            if total_records >= 50:
                print(f"   ✓ Minimum data points: {total_records} (need 50+)")
            else:
                print(f"   ✗ Insufficient data: {total_records} (need 50+)")
                print("   → Collect more data or use simple forecasting")
            
            if days_of_data >= 2:
                print(f"   ✓ Days of history: {days_of_data} (need 2+)")
            else:
                print(f"   ✗ Insufficient history: {days_of_data} days (need 2+)")
            
            # 2. Data continuity check
            print("\n2️⃣ DATA CONTINUITY (gaps in time series)")
            print("-" * 80)
            
            result = conn.execute(text("""
                SELECT 
                    collection_timestamp,
                    LAG(collection_timestamp) OVER (ORDER BY collection_timestamp) as prev_timestamp
                FROM synchronized_data
                WHERE collection_timestamp >= NOW() - INTERVAL 24 HOUR
                ORDER BY collection_timestamp
            """))
            
            timestamps = result.fetchall()
            gaps = []
            
            for row in timestamps[1:]:  # Skip first row
                if row[1]:  # If prev_timestamp exists
                    gap = (row[0] - row[1]).total_seconds() / 60
                    if gap > 10:  # Gaps larger than 10 minutes
                        gaps.append(gap)
            
            if gaps:
                print(f"⚠️  Found {len(gaps)} gaps > 10 minutes")
                print(f"   Largest gap: {max(gaps):.1f} minutes")
                print(f"   Average gap: {np.mean(gaps):.1f} minutes")
                print("   → ARIMA can handle small gaps, but large gaps reduce accuracy")
            else:
                print("✓ No significant gaps detected (good for ARIMA)")
            
            # 3. Statistical properties
            print("\n3️⃣ STATISTICAL PROPERTIES")
            print("-" * 80)
            
            # Get threat probability data
            result = conn.execute(text("""
                SELECT probability
                FROM threat_alerts
                WHERE timestamp >= NOW() - INTERVAL 7 DAY
                ORDER BY timestamp
            """))
            
            probabilities = [row[0] for row in result.fetchall()]
            
            if len(probabilities) >= 20:
                print(f"Threat Data Points: {len(probabilities)}")
                print(f"Mean Probability:   {np.mean(probabilities):.3f}")
                print(f"Std Deviation:      {np.std(probabilities):.3f}")
                print(f"Min Probability:    {np.min(probabilities):.3f}")
                print(f"Max Probability:    {np.max(probabilities):.3f}")
                
                # Check for stationarity (basic test)
                if np.std(probabilities) < 0.05:
                    print("⚠️  Low variance - data might be too stable for forecasting")
                else:
                    print("✓ Good variance for time series analysis")
                
            else:
                print(f"⚠️  Only {len(probabilities)} threat data points")
                print("   Need more data for accurate statistical analysis")
            
            # 4. Seasonality check
            print("\n4️⃣ SEASONALITY PATTERNS")
            print("-" * 80)
            
            result = conn.execute(text("""
                SELECT 
                    HOUR(collection_timestamp) as hour,
                    AVG(weather_temperature) as avg_temp,
                    COUNT(*) as records
                FROM synchronized_data
                WHERE collection_timestamp >= NOW() - INTERVAL 3 DAY
                GROUP BY HOUR(collection_timestamp)
                ORDER BY hour
            """))
            
            hourly = result.fetchall()
            
            if len(hourly) >= 12:
                temps = [row[1] for row in hourly if row[1]]
                temp_range = max(temps) - min(temps) if temps else 0
                
                print(f"Hourly data points: {len(hourly)}")
                print(f"Temperature range:  {temp_range:.1f}°C")
                
                if temp_range > 5:
                    print("✓ Clear daily patterns detected (good for ARIMA with seasonality)")
                else:
                    print("→ Weak daily patterns (might need more data)")
            else:
                print(f"⚠️  Only {len(hourly)} hours of data")
                print("   Need more data to detect patterns")
            
            # 5. Final recommendation
            print("\n" + "=" * 80)
            print("📊 FORECASTING RECOMMENDATION")
            print("=" * 80)
            
            if total_records >= 100 and days_of_data >= 3:
                print("✅ READY FOR ARIMA FORECASTING!")
                print("   Your data is suitable for:")
                print("   - ARIMA (AutoRegressive Integrated Moving Average)")
                print("   - SARIMA (Seasonal ARIMA) if patterns are strong")
                print("   - Prophet (if you have weekly/daily seasonality)")
                return True
                
            elif total_records >= 50 and days_of_data >= 2:
                print("⚠️  LIMITED DATA - Use Simple Forecasting")
                print("   Recommended methods:")
                print("   - Exponential Smoothing")
                print("   - Moving Average")
                print("   - Linear Regression")
                print("\n   Continue collecting data for better ARIMA forecasts")
                return False
                
            else:
                print("❌ INSUFFICIENT DATA")
                print(f"   Current: {total_records} records, {days_of_data} days")
                print("   Required: 50+ records, 2+ days")
                print("\n   Recommendations:")
                print("   1. Continue collecting data for at least 2-3 days")
                print("   2. Ensure data collection is continuous (no long gaps)")
                print("   3. Use dummy/simulated forecasts until then")
                return False
            
    except Exception as e:
        print(f"\n❌ Error: {e}")
        return False

if __name__ == "__main__":
    ready = check_arima_readiness()
    sys.exit(0 if ready else 1)