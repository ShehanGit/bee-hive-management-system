import React, { useState, useEffect, useRef } from "react";
import axios from "axios";
// import Navbar from "../components/Navbar";
import "./ThreatDetection.css";

// Map threat types to emojis
const getThreatIcon = (threatType) => {
  switch (threatType) {
    case "Wax_Moth":
      return "🦋";
    case "Predator":
      return "🦊";
    case "Environmental":
      return "🌡️";
    case "No_Threat":
      return "✅";
    default:
      return "⚠️";
  }
};

// Map threat types to recommendations
const getRecommendation = (threatType) => {
  switch (threatType) {
    case "Wax_Moth":
      return "Inspect hive frames and consider narrowing hive entrances.";
    case "Predator":
      return "Deploy protective barriers or ultrasonic deterrents.";
    case "Environmental":
      return "Check ventilation and temperature regulation.";
    case "No_Threat":
      return "Hive is stable. Keep monitoring.";
    default:
      return "No specific recommendation.";
  }
};

function ThreatDetection() {
  const [formData, setFormData] = useState({
    weather_temp_c: "",
    weather_humidity_pct: "",
    hive_sound_db: "",
    hive_sound_peak_freq: "",
    vibration_hz: "",
    vibration_var: "",
  });

  const [prediction, setPrediction] = useState(null);
  const [alerts, setAlerts] = useState([]);
  const [showNotifications, setShowNotifications] = useState(false);
  const notificationRef = useRef(null);

  // Fetch live alerts periodically
  useEffect(() => {
    const fetchAlerts = async () => {
      try {
        const res = await axios.get("http://127.0.0.1:5000/api/threat/alerts");
        setAlerts(res.data);
      } catch (error) {
        console.error("Error fetching alerts:", error);
      }
    };

    fetchAlerts();
    const interval = setInterval(fetchAlerts, 5000); // refresh every 5s
    return () => clearInterval(interval);
  }, []);

  // Close dropdown when clicking outside
  useEffect(() => {
    const handleClickOutside = (event) => {
      if (notificationRef.current && !notificationRef.current.contains(event.target)) {
        setShowNotifications(false);
      }
    };

    document.addEventListener('mousedown', handleClickOutside);
    return () => {
      document.removeEventListener('mousedown', handleClickOutside);
    };
  }, []);

  const handleChange = (e) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value,
    });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      const res = await axios.post(
        "http://127.0.0.1:5000/api/threat/predict",
        formData
      );
      setPrediction(res.data);
    } catch (error) {
      console.error("Error making prediction:", error);
      alert("Failed to connect to backend.");
    }
  };

  const toggleNotifications = () => {
    setShowNotifications(!showNotifications);
  };

  // Get first 5 alerts for notifications
  const notificationAlerts = alerts.slice(0, 5);
  const hasAlerts = alerts.length > 0;

  return (
    <div className="threat-detection-page">
      {/* <Navbar /> */}
      
      {/* Bell Notification Icon */}
      <div className="notification-container" ref={notificationRef}>
        <button 
          className={`notification-bell ${hasAlerts ? 'has-alerts' : ''}`}
          onClick={toggleNotifications}
        >
          🔔
          {hasAlerts && <span className="notification-badge">{alerts.length}</span>}
        </button>
        
        {showNotifications && (
          <div className="notification-dropdown">
            <div className="notification-header">
              <h3>Recent Alerts</h3>
              <span className="notification-count">{alerts.length} total</span>
            </div>
            <div className="notification-list">
              {notificationAlerts.length > 0 ? (
                notificationAlerts.map((alert, idx) => (
                  <div key={idx} className="notification-item">
                    <span className="notification-icon">
                      {getThreatIcon(alert.threat_type)}
                    </span>
                    <div className="notification-content">
                      <div className="notification-type">{alert.threat_type}</div>
                      <div className="notification-prob">
                        {(alert.probability * 100).toFixed(1)}% probability
                      </div>
                    </div>
                  </div>
                ))
              ) : (
                <div className="no-notifications">No recent alerts</div>
              )}
            </div>
            {alerts.length > 5 && (
              <div className="notification-footer">
                <button 
                  className="view-all-btn"
                  onClick={() => {
                    setShowNotifications(false);
                    // Scroll to alerts section
                    document.querySelector('.alerts-section').scrollIntoView({ 
                      behavior: 'smooth' 
                    });
                  }}
                >
                  View All Alerts
                </button>
              </div>
            )}
          </div>
        )}
      </div>

      <main className="content">
        <h1>🐝 Real-Time Threat Detection</h1>

        {/* Form Section */}
        <section className="form-section">
          <h2> Enter Hive Sensor Data</h2>
          <form onSubmit={handleSubmit} className="sensor-form">
            <div className="form-group">
              <label htmlFor="weather_temp_c">
                
                Weather Temperature (°C)
              </label>
              <input
                id="weather_temp_c"
                type="number"
                name="weather_temp_c"
                value={formData.weather_temp_c}
                onChange={handleChange}
                required
                step="0.1"
                placeholder="Enter temperature in Celsius"
              />
            </div>

            <div className="form-group">
              <label htmlFor="weather_humidity_pct">
                
                Weather Humidity (%)
              </label>
              <input
                id="weather_humidity_pct"
                type="number"
                name="weather_humidity_pct"
                value={formData.weather_humidity_pct}
                onChange={handleChange}
                required
                step="0.1"
                min="0"
                max="100"
                placeholder="Enter humidity percentage"
              />
            </div>

            <div className="form-group">
              <label htmlFor="hive_sound_db">
                
                Hive Sound (dB)
              </label>
              <input
                id="hive_sound_db"
                type="number"
                name="hive_sound_db"
                value={formData.hive_sound_db}
                onChange={handleChange}
                required
                step="0.1"
                placeholder="Enter sound level in decibels"
              />
            </div>

            <div className="form-group">
              <label htmlFor="hive_sound_peak_freq">
                
                Hive Sound Peak Frequency (Hz)
              </label>
              <input
                id="hive_sound_peak_freq"
                type="number"
                name="hive_sound_peak_freq"
                value={formData.hive_sound_peak_freq}
                onChange={handleChange}
                required
                step="1"
                placeholder="Enter peak frequency in Hz"
              />
            </div>

            <div className="form-group">
              <label htmlFor="vibration_hz">
                
                Vibration (Hz)
              </label>
              <input
                id="vibration_hz"
                type="number"
                name="vibration_hz"
                value={formData.vibration_hz}
                onChange={handleChange}
                required
                step="1"
                placeholder="Enter vibration frequency"
              />
            </div>

            <div className="form-group">
              <label htmlFor="vibration_var">
                
                Vibration Variance
              </label>
              <input
                id="vibration_var"
                type="number"
                name="vibration_var"
                value={formData.vibration_var}
                onChange={handleChange}
                required
                step="0.1"
                placeholder="Enter vibration variance"
              />
            </div>

            <div className="form-actions">
              <button type="submit" className="submit-btn">
                
                Analyze Threat
              </button>
            </div>
          </form>
        </section>

        {/* Prediction Result */}
        {prediction && (
          <section className="result-section">
            <h2>📋 Prediction Result</h2>
            <div className="result-card">
              <div className="result-icon">
                {getThreatIcon(prediction.threat_type)}
              </div>
              <div className="result-details">
                <p>
                  <strong>Threat Type:</strong> {prediction.threat_type}
                </p>
                <p>
                  <strong>Probability:</strong>{" "}
                  {(prediction.probability * 100).toFixed(1)}%
                </p>
                <p>
                  <strong>Recommendation:</strong>{" "}
                  {getRecommendation(prediction.threat_type)}
                </p>
              </div>
            </div>
          </section>
        )}

        {/* Live Alerts */}
        {/* <section className="alerts-section">
          <h2>🚨 Live Alerts</h2>
          <ul className="alerts-list">
            {alerts.length > 0 ? (
              alerts.map((alert, idx) => (
                <li key={idx} className="alert-item">
                  <span className="alert-icon">
                    {getThreatIcon(alert.threat_type)}
                  </span>
                  <span className="alert-type">{alert.threat_type}</span>
                  <span className="alert-prob">
                    {(alert.probability * 100).toFixed(1)}%
                  </span>
                </li>
              ))
            ) : (
              <p>No recent alerts</p>
            )}
          </ul>
        </section> */}
      </main>
    </div>
  );
}

export default ThreatDetection;