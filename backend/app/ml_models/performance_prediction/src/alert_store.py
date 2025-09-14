# ===============================================================================
# 🐝 Hive Performance Alert Management System
# Location: Badulla District, Sri Lanka
# Research-based ML model for precision apiculture
# ===============================================================================

import json
import pandas as pd
from datetime import datetime, timedelta
from typing import List, Dict, Optional
import os

class HivePerformanceAlertStore:
    """Manage and store hive performance alerts"""
    
    def __init__(self, alerts_file="outputs/alerts.json"):
        """Initialize the alert store"""
        self.alerts_file = alerts_file
        self.alerts = []
        self.load_alerts()
        
        # Alert thresholds
        self.alert_thresholds = {
            'critical_level': 5,      # Alert when level reaches critical
            'poor_level': 4,          # Alert when level reaches poor
            'low_confidence': 0.6,    # Alert when confidence is low
            'consecutive_poor': 3,    # Alert after 3 consecutive poor readings
            'weight_drop_threshold': -5.0,  # Alert on significant weight drop
            'temp_variance_high': 5.0  # Alert on high temperature variance
        }
        
        # Alert priorities
        self.alert_priorities = {
            'CRITICAL': 1,
            'HIGH': 2, 
            'MEDIUM': 3,
            'LOW': 4,
            'INFO': 5
        }
    
    def load_alerts(self):
        """Load existing alerts from file"""
        try:
            if os.path.exists(self.alerts_file):
                with open(self.alerts_file, 'r') as f:
                    data = json.load(f)
                    self.alerts = data.get('alerts', [])
                print(f"✅ Loaded {len(self.alerts)} existing alerts")
            else:
                print("📝 No existing alerts file found - starting fresh")
                # Create directory if it doesn't exist
                os.makedirs(os.path.dirname(self.alerts_file), exist_ok=True)
        except Exception as e:
            print(f"⚠️ Error loading alerts: {str(e)}")
            self.alerts = []
    
    def save_alerts(self):
        """Save alerts to file"""
        try:
            alert_data = {
                'last_updated': datetime.now().isoformat(),
                'total_alerts': len(self.alerts),
                'alerts': self.alerts
            }
            
            with open(self.alerts_file, 'w') as f:
                json.dump(alert_data, f, indent=2, default=str)
            print(f"💾 Saved {len(self.alerts)} alerts to {self.alerts_file}")
        except Exception as e:
            print(f"❌ Error saving alerts: {str(e)}")
    
    def create_alert(self, hive_id: str, alert_type: str, message: str, 
                    priority: str = "MEDIUM", prediction_data: Dict = None,
                    metadata: Dict = None):
        """Create a new alert"""
        alert = {
            'alert_id': f"ALERT_{datetime.now().strftime('%Y%m%d_%H%M%S')}_{hive_id}",
            'hive_id': hive_id,
            'timestamp': datetime.now().isoformat(),
            'alert_type': alert_type,
            'priority': priority,
            'priority_score': self.alert_priorities.get(priority, 3),
            'message': message,
            'status': 'ACTIVE',
            'prediction_data': prediction_data or {},
            'metadata': metadata or {},
            'acknowledged': False,
            'resolved': False,
            'resolution_notes': None
        }
        
        self.alerts.append(alert)
        print(f"🚨 Created {priority} alert for {hive_id}: {message}")
        return alert
    
    def analyze_prediction_for_alerts(self, hive_id: str, prediction_result: Dict, 
                                    sensor_data: Dict = None):
        """Analyze prediction result and generate appropriate alerts"""
        alerts_generated = []
        
        try:
            predicted_level = prediction_result.get('predicted_level', 3)
            confidence = prediction_result.get('confidence', 1.0)
            interpretation = prediction_result.get('interpretation', '')
            
            # Critical performance level alert
            if predicted_level >= self.alert_thresholds['critical_level']:
                alert = self.create_alert(
                    hive_id=hive_id,
                    alert_type="CRITICAL_PERFORMANCE",
                    message=f"Critical performance detected (Level {predicted_level}): {interpretation}",
                    priority="CRITICAL",
                    prediction_data=prediction_result,
                    metadata={'trigger': 'critical_level_threshold'}
                )
                alerts_generated.append(alert)
            
            # Poor performance level alert
            elif predicted_level >= self.alert_thresholds['poor_level']:
                alert = self.create_alert(
                    hive_id=hive_id,
                    alert_type="POOR_PERFORMANCE", 
                    message=f"Poor performance detected (Level {predicted_level}): {interpretation}",
                    priority="HIGH",
                    prediction_data=prediction_result,
                    metadata={'trigger': 'poor_level_threshold'}
                )
                alerts_generated.append(alert)
            
            # Low confidence alert
            if confidence < self.alert_thresholds['low_confidence']:
                alert = self.create_alert(
                    hive_id=hive_id,
                    alert_type="LOW_CONFIDENCE",
                    message=f"Low prediction confidence ({confidence:.1%}) - sensor data may be unreliable",
                    priority="MEDIUM",
                    prediction_data=prediction_result,
                    metadata={'trigger': 'low_confidence', 'confidence': confidence}
                )
                alerts_generated.append(alert)
            
            # Sensor-based alerts
            if sensor_data:
                sensor_alerts = self._analyze_sensor_data_for_alerts(hive_id, sensor_data)
                alerts_generated.extend(sensor_alerts)
            
            # Check for consecutive poor performance
            consecutive_alerts = self._check_consecutive_poor_performance(hive_id)
            if consecutive_alerts:
                alerts_generated.extend(consecutive_alerts)
                
        except Exception as e:
            error_alert = self.create_alert(
                hive_id=hive_id,
                alert_type="SYSTEM_ERROR",
                message=f"Error analyzing prediction for alerts: {str(e)}",
                priority="MEDIUM",
                metadata={'error': str(e)}
            )
            alerts_generated.append(error_alert)
        
        if alerts_generated:
            self.save_alerts()
        
        return alerts_generated
    
    def _analyze_sensor_data_for_alerts(self, hive_id: str, sensor_data: Dict):
        """Analyze sensor data for specific alert conditions"""
        alerts = []
        
        # Temperature variance alert
        temp_variance = sensor_data.get('temp_variance_1h', 0)
        if temp_variance > self.alert_thresholds['temp_variance_high']:
            alert = self.create_alert(
                hive_id=hive_id,
                alert_type="HIGH_TEMPERATURE_VARIANCE",
                message=f"High temperature variance detected ({temp_variance:.2f}°C) - possible thermoregulation issues",
                priority="MEDIUM",
                metadata={'temp_variance': temp_variance, 'trigger': 'temp_variance_threshold'}
            )
            alerts.append(alert)
        
        # Weight drop alert
        if 'sensor_weight' in sensor_data and 'previous_weight' in sensor_data:
            weight_change = sensor_data['sensor_weight'] - sensor_data['previous_weight']
            weight_change_pct = (weight_change / sensor_data['previous_weight']) * 100
            
            if weight_change_pct < self.alert_thresholds['weight_drop_threshold']:
                alert = self.create_alert(
                    hive_id=hive_id,
                    alert_type="SIGNIFICANT_WEIGHT_DROP",
                    message=f"Significant weight drop detected ({weight_change_pct:.1f}%) - possible swarming or robbing",
                    priority="HIGH",
                    metadata={'weight_change_pct': weight_change_pct, 'trigger': 'weight_drop_threshold'}
                )
                alerts.append(alert)
        
        # Temperature extremes
        sensor_temp = sensor_data.get('sensor_temperature')
        if sensor_temp:
            if sensor_temp > 40:
                alert = self.create_alert(
                    hive_id=hive_id,
                    alert_type="HIGH_TEMPERATURE",
                    message=f"High hive temperature detected ({sensor_temp:.1f}°C) - overheating risk",
                    priority="HIGH",
                    metadata={'temperature': sensor_temp, 'trigger': 'high_temperature'}
                )
                alerts.append(alert)
            elif sensor_temp < 30:
                alert = self.create_alert(
                    hive_id=hive_id,
                    alert_type="LOW_TEMPERATURE", 
                    message=f"Low hive temperature detected ({sensor_temp:.1f}°C) - colony stress possible",
                    priority="MEDIUM",
                    metadata={'temperature': sensor_temp, 'trigger': 'low_temperature'}
                )
                alerts.append(alert)
        
        return alerts
    
    def _check_consecutive_poor_performance(self, hive_id: str):
        """Check for consecutive poor performance readings"""
        alerts = []
        
        # Get recent alerts for this hive
        recent_alerts = [a for a in self.alerts if a['hive_id'] == hive_id 
                        and a['alert_type'] in ['POOR_PERFORMANCE', 'CRITICAL_PERFORMANCE']
                        and a['status'] == 'ACTIVE']
        
        # Check if we have reached the threshold
        if len(recent_alerts) >= self.alert_thresholds['consecutive_poor']:
            # Check if these are within a reasonable time frame (e.g., last 24 hours)
            recent_time = datetime.now() - timedelta(hours=24)
            recent_alerts_24h = [a for a in recent_alerts 
                               if datetime.fromisoformat(a['timestamp'].replace('Z', '+00:00')) > recent_time]
            
            if len(recent_alerts_24h) >= self.alert_thresholds['consecutive_poor']:
                alert = self.create_alert(
                    hive_id=hive_id,
                    alert_type="CONSECUTIVE_POOR_PERFORMANCE",
                    message=f"Consecutive poor performance detected ({len(recent_alerts_24h)} readings in 24h) - urgent intervention needed",
                    priority="CRITICAL",
                    metadata={
                        'consecutive_count': len(recent_alerts_24h),
                        'trigger': 'consecutive_poor_threshold'
                    }
                )
                alerts.append(alert)
        
        return alerts
    
    def get_active_alerts(self, hive_id: Optional[str] = None, priority: Optional[str] = None):
        """Get active alerts, optionally filtered by hive_id and/or priority"""
        filtered_alerts = [a for a in self.alerts if a['status'] == 'ACTIVE']
        
        if hive_id:
            filtered_alerts = [a for a in filtered_alerts if a['hive_id'] == hive_id]
        
        if priority:
            filtered_alerts = [a for a in filtered_alerts if a['priority'] == priority]
        
        # Sort by priority score (lower = higher priority) then by timestamp
        filtered_alerts.sort(key=lambda x: (x['priority_score'], x['timestamp']))
        
        return filtered_alerts
    
    def acknowledge_alert(self, alert_id: str, acknowledged_by: str = "System"):
        """Acknowledge an alert"""
        for alert in self.alerts:
            if alert['alert_id'] == alert_id:
                alert['acknowledged'] = True
                alert['acknowledged_by'] = acknowledged_by
                alert['acknowledged_at'] = datetime.now().isoformat()
                self.save_alerts()
                print(f"✅ Alert {alert_id} acknowledged by {acknowledged_by}")
                return True
        
        print(f"⚠️ Alert {alert_id} not found")
        return False
    
    def resolve_alert(self, alert_id: str, resolution_notes: str, resolved_by: str = "System"):
        """Resolve an alert"""
        for alert in self.alerts:
            if alert['alert_id'] == alert_id:
                alert['resolved'] = True
                alert['status'] = 'RESOLVED'
                alert['resolution_notes'] = resolution_notes
                alert['resolved_by'] = resolved_by
                alert['resolved_at'] = datetime.now().isoformat()
                self.save_alerts()
                print(f"✅ Alert {alert_id} resolved by {resolved_by}")
                return True
        
        print(f"⚠️ Alert {alert_id} not found")
        return False
    
    def get_alert_summary(self):
        """Get summary statistics of alerts"""
        total_alerts = len(self.alerts)
        active_alerts = len([a for a in self.alerts if a['status'] == 'ACTIVE'])
        resolved_alerts = len([a for a in self.alerts if a['status'] == 'RESOLVED'])
        
        # Priority breakdown
        priority_counts = {}
        for alert in self.alerts:
            if alert['status'] == 'ACTIVE':
                priority = alert['priority']
                priority_counts[priority] = priority_counts.get(priority, 0) + 1
        
        # Hive breakdown
        hive_counts = {}
        for alert in self.alerts:
            if alert['status'] == 'ACTIVE':
                hive_id = alert['hive_id']
                hive_counts[hive_id] = hive_counts.get(hive_id, 0) + 1
        
        summary = {
            'total_alerts': total_alerts,
            'active_alerts': active_alerts,
            'resolved_alerts': resolved_alerts,
            'priority_breakdown': priority_counts,
            'hive_breakdown': hive_counts,
            'last_updated': datetime.now().isoformat()
        }
        
        return summary
    
    def export_alerts_csv(self, filename: Optional[str] = None):
        """Export alerts to CSV file"""
        if not filename:
            filename = f"outputs/alerts_export_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
        
        df = pd.DataFrame(self.alerts)
        df.to_csv(filename, index=False)
        print(f"📊 Exported {len(self.alerts)} alerts to {filename}")
        return filename

def demo_alert_system():
    """Demonstrate the alert system"""
    print("🚨 HIVE PERFORMANCE ALERT SYSTEM DEMO")
    print("=" * 50)
    
    # Initialize alert store
    alert_store = HivePerformanceAlertStore()
    
    # Sample prediction results that would trigger alerts
    sample_predictions = [
        {
            'hive_id': 'HIVE_001',
            'prediction': {'predicted_level': 5, 'confidence': 0.85, 'interpretation': 'Critical - Colony collapse risk'},
            'sensor_data': {'sensor_temperature': 42.0, 'temp_variance_1h': 6.2}
        },
        {
            'hive_id': 'HIVE_002', 
            'prediction': {'predicted_level': 4, 'confidence': 0.45, 'interpretation': 'Poor - Consuming stored honey'},
            'sensor_data': {'sensor_weight': 38.5, 'previous_weight': 42.0}
        }
    ]
    
    # Process predictions and generate alerts
    for sample in sample_predictions:
        alerts = alert_store.analyze_prediction_for_alerts(
            hive_id=sample['hive_id'],
            prediction_result=sample['prediction'],
            sensor_data=sample['sensor_data']
        )
        print(f"Generated {len(alerts)} alerts for {sample['hive_id']}")
    
    # Show alert summary
    summary = alert_store.get_alert_summary()
    print(f"\n📊 ALERT SUMMARY:")
    print(f"Active Alerts: {summary['active_alerts']}")
    print(f"Priority Breakdown: {summary['priority_breakdown']}")
    
    # Show active alerts
    active_alerts = alert_store.get_active_alerts()
    print(f"\n🚨 ACTIVE ALERTS ({len(active_alerts)}):")
    for alert in active_alerts[:3]:  # Show first 3
        print(f"  {alert['priority']} - {alert['hive_id']}: {alert['message']}")
    
    return alert_store

if __name__ == "__main__":
    # Run demo
    demo_alert_system()