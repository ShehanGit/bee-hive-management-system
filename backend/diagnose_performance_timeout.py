"""
Diagnostic script to identify why performance prediction is timing out.
Run this to check database performance and identify bottlenecks.
"""
import sys
import os
import time
from datetime import datetime, timedelta

# Add the app directory to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'app'))

from app import create_app
from app.models.synchronized_data import SynchronizedData

def check_database_performance():
    """Diagnose database query performance"""
    print("=" * 70)
    print("🔍 PERFORMANCE PREDICTION TIMEOUT DIAGNOSTICS")
    print("=" * 70)
    
    app = create_app()
    
    with app.app_context():
        # 1. Check total records
        print("\n📊 Checking database size...")
        start = time.time()
        total = SynchronizedData.query.count()
        elapsed = time.time() - start
        print(f"   Total records: {total:,}")
        print(f"   Query time: {elapsed:.2f}s")
        
        if elapsed > 1:
            print("   ⚠️ WARNING: Counting records is slow!")
        
        # 2. Check records per hive
        print("\n🐝 Checking records per hive...")
        hive_counts = {}
        for hive_id in range(1, 6):
            start = time.time()
            count = SynchronizedData.query.filter_by(hive_id=hive_id).count()
            elapsed = time.time() - start
            hive_counts[hive_id] = count
            print(f"   Hive {hive_id}: {count:,} records ({elapsed:.2f}s)")
        
        # 3. Simulate the actual query
        print("\n🔍 Simulating performance prediction query...")
        since_time = datetime.now() - timedelta(days=7)
        hive_id = 1
        
        # Time the query
        start = time.time()
        records = SynchronizedData.query.filter(
            SynchronizedData.hive_id == hive_id,
            SynchronizedData.collection_timestamp >= since_time
        ).order_by(SynchronizedData.collection_timestamp.asc()).limit(1000).all()
        elapsed = time.time() - start
        
        print(f"   Hive: {hive_id}")
        print(f"   Time window: Last 7 days")
        print(f"   Records found: {len(records)}")
        print(f"   Query time: {elapsed:.2f}s")
        
        # 4. Check if database has indexes
        print("\n📑 Checking database indexes...")
        try:
            from sqlalchemy import inspect, text
            from app import db
            inspector = inspect(db.engine)
            indexes = inspector.get_indexes('synchronized_data')
            
            index_names = [idx['name'] for idx in indexes]
            required_indexes = ['idx_hive_timestamp', 'idx_hive_id', 'idx_collection_timestamp']
            
            print(f"   Found indexes: {index_names}")
            
            missing = [idx for idx in required_indexes if idx not in index_names]
            if missing:
                print(f"   ⚠️ MISSING INDEXES: {missing}")
                print("   👉 Run the migration to add indexes!")
            else:
                print("   ✅ All required indexes exist")
                
        except Exception as e:
            print(f"   ❌ Could not check indexes: {e}")
        
        # 5. Diagnose the problem
        print("\n" + "=" * 70)
        print("📋 DIAGNOSIS")
        print("=" * 70)
        
        problems = []
        recommendations = []
        
        if elapsed > 10:
            problems.append(f"Query is VERY SLOW ({elapsed:.2f}s)")
            recommendations.append("❌ URGENT: Add database indexes")
        elif elapsed > 5:
            problems.append(f"Query is SLOW ({elapsed:.2f}s)")
            recommendations.append("⚠️ Add database indexes")
        
        if len(records) == 0:
            problems.append("No data found for last 7 days")
            recommendations.append("⚠️ Check if data collection is working")
        
        if total > 100000:
            problems.append(f"Database is large ({total:,} records)")
            recommendations.append("💡 Consider archiving old data")
        
        if problems:
            print("\n❌ Problems found:")
            for problem in problems:
                print(f"   • {problem}")
        else:
            print("\n✅ No obvious problems detected")
        
        if recommendations:
            print("\n💡 Recommendations:")
            for rec in recommendations:
                print(f"   {rec}")
    
    print("\n" + "=" * 70)
    print("✅ Diagnostic complete")
    print("=" * 70)

if __name__ == "__main__":
    check_database_performance()

