import React, { useState, useEffect, useRef } from "react";
import axios from "axios";

// import Navbar from "../components/Navbar";
import { PieChart, Pie, Cell, ResponsiveContainer, Legend, Tooltip } from "recharts";
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
        // Add timestamp if not present in the data
        const alertsWithTimestamps = res.data.map(alert => ({
          ...alert,
          timestamp: alert.timestamp || new Date().toISOString()
        }));
        setAlerts(alertsWithTimestamps);
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

  // Chart Data for threat distribution
  const pieData = alerts.reduce((acc, alert) => {
    const existing = acc.find(a => a.name === alert.threat_type);
    if (existing) existing.value++;
    else acc.push({ name: alert.threat_type, value: 1 });
    return acc;
  }, []);

  const COLORS = ["#F1C40F", "#F39C12", "#E67E22", "#D35400", "#F7DC6F", "#F4D03F"];

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
                    document.querySelector('.alerts-table-section').scrollIntoView({ 
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
        <h1>🐝 Real-Time Hive Threat Detection</h1>

        {/* Top Section: Live Alerts Table */}
        <section className="alerts-table-section">
          <div className="section-header">
            <h2>🚨 Live Threat Alerts</h2>
            <div className="alerts-count">{alerts.length} Active Alerts</div>
          </div>
          
          <div className="table-wrapper">
            <table className="modern-alerts-table">
              <thead>
                <tr>
                  <th>Timestamp</th>
                  <th>Threat Type</th>
                  <th>Probability</th>
                  <th>Recommendation</th>
                  <th>Status</th>
                </tr>
              </thead>
              <tbody>
                {alerts.length > 0 ? (
                  alerts.slice(0, 8).map((alert, idx) => (
                    <tr key={idx} className={`alert-row priority-${alert.threat_type !== 'No_Threat' ? 'high' : 'normal'}`}>
                      <td className="timestamp-cell">
                        {alert.timestamp
                          ? new Date(alert.timestamp).toLocaleString()
                          : "—"}
                      </td>
                      <td className="threat-cell">
                        <div className="threat-info">
                          <span className="threat-icon">
                            {getThreatIcon(alert.threat_type)}
                          </span>
                          <span className="threat-name">{alert.threat_type}</span>
                        </div>
                      </td>
                      <td className="probability-cell">
                        <div className="probability-bar">
                          <div 
                            className="probability-fill"
                            style={{ width: `${alert.probability * 100}%` }}
                          ></div>
                          <span className="probability-text">
                            {(alert.probability * 100).toFixed(1)}%
                          </span>
                        </div>
                      </td>
                      <td className="recommendation-cell">
                        <span className="recommendation-text">
                          {getRecommendation(alert.threat_type)}
                        </span>
                      </td>
                      <td className="status-cell">
                        <span className={`status-badge ${alert.threat_type !== 'No_Threat' ? 'active' : 'safe'}`}>
                          {alert.threat_type !== 'No_Threat' ? 'Active' : 'Safe'}
                        </span>
                      </td>
                    </tr>
                  ))
                ) : (
                  <tr>
                    <td colSpan="5" className="no-data">
                      <div className="no-data-content">
                        <div className="no-data-icon">📊</div>
                        <div className="no-data-text">No threat alerts detected</div>
                        <div className="no-data-subtext">Your hive is currently safe</div>
                      </div>
                    </td>
                  </tr>
                )}
              </tbody>
            </table>
          </div>
        </section>

        {/* Middle Section: Two Column Layout */}
        <div className="main-content-grid">
          {/* Left Column: Form */}
          <section className="form-section">
            <div className="section-header">
              <h2>📊 Analyze New Sensor Data</h2>
              <div className="section-subtitle">Enter real-time sensor readings</div>
            </div>
            
            <form onSubmit={handleSubmit} className="sensor-form">
              <div className="form-row">
                <div className="form-group">
                  <label htmlFor="weather_temp_c">
                    🌡️ Temperature (°C)
                  </label>
                  <input
                    id="weather_temp_c"
                    type="number"
                    name="weather_temp_c"
                    value={formData.weather_temp_c}
                    onChange={handleChange}
                    required
                    step="0.1"
                    placeholder="25.5"
                  />
                </div>

                <div className="form-group">
                  <label htmlFor="weather_humidity_pct">
                    💧 Humidity (%)
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
                    placeholder="65.0"
                  />
                </div>
              </div>

              <div className="form-row">
                <div className="form-group">
                  <label htmlFor="hive_sound_db">
                    🔊 Sound Level (dB)
                  </label>
                  <input
                    id="hive_sound_db"
                    type="number"
                    name="hive_sound_db"
                    value={formData.hive_sound_db}
                    onChange={handleChange}
                    required
                    step="0.1"
                    placeholder="45.2"
                  />
                </div>

                <div className="form-group">
                  <label htmlFor="hive_sound_peak_freq">
                    📳 Peak Frequency (Hz)
                  </label>
                  <input
                    id="hive_sound_peak_freq"
                    type="number"
                    name="hive_sound_peak_freq"
                    value={formData.hive_sound_peak_freq}
                    onChange={handleChange}
                    required
                    step="1"
                    placeholder="350"
                  />
                </div>
              </div>

              <div className="form-row">
                <div className="form-group">
                  <label htmlFor="vibration_hz">
                    📳 Vibration (Hz)
                  </label>
                  <input
                    id="vibration_hz"
                    type="number"
                    name="vibration_hz"
                    value={formData.vibration_hz}
                    onChange={handleChange}
                    required
                    step="1"
                    placeholder="15"
                  />
                </div>

                <div className="form-group">
                  <label htmlFor="vibration_var">
                    📊 Vibration Variance
                  </label>
                  <input
                    id="vibration_var"
                    type="number"
                    name="vibration_var"
                    value={formData.vibration_var}
                    onChange={handleChange}
                    required
                    step="0.1"
                    placeholder="2.5"
                  />
                </div>
              </div>

              <div className="form-actions">
                <button type="submit" className="analyze-btn">
                  <span className="btn-icon">🔍</span>
                  Analyze Threat
                </button>
              </div>
            </form>

            {/* Prediction Result */}
            {prediction && (
              <div className="result-section">
                <div className="result-header">
                  <h3>🎯 Analysis Result</h3>
                </div>
                <div className="result-card">
                  <div className="result-icon">
                    {getThreatIcon(prediction.threat_type)}
                  </div>
                  <div className="result-details">
                    <div className="result-threat">{prediction.threat_type}</div>
                    <div className="result-probability">
                      {(prediction.probability * 100).toFixed(1)}% Confidence
                    </div>
                    <div className="result-recommendation">
                      {getRecommendation(prediction.threat_type)}
                    </div>
                  </div>
                </div>
              </div>
            )}
          </section>

          {/* Right Column: Threat Distribution Chart */}
          <section className="chart-section">
            <div className="section-header">
              <h2>📈 Threat Distribution Analysis</h2>
              <div className="section-subtitle">Real-time threat overview</div>
            </div>
            
            <div className="chart-container">
              {pieData.length > 0 ? (
                <>
                  <ResponsiveContainer width="100%" height={300}>
                    <PieChart>
                      <Pie
                        data={pieData}
                        dataKey="value"
                        nameKey="name"
                        cx="50%"
                        cy="50%"
                        outerRadius={100}
                        innerRadius={40}
                        paddingAngle={5}
                      >
                        {pieData.map((entry, index) => (
                          <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
                        ))}
                      </Pie>
                      <Tooltip 
                        formatter={(value, name) => [`${value} alerts`, name]}
                        contentStyle={{
                          backgroundColor: '#fff',
                          border: '1px solid #f1c40f',
                          borderRadius: '8px',
                          boxShadow: '0 4px 12px rgba(0,0,0,0.1)'
                        }}
                      />
                      <Legend 
                        verticalAlign="bottom" 
                        height={36}
                        iconType="circle"
                      />
                    </PieChart>
                  </ResponsiveContainer>
                  
                  <div className="chart-stats">
                    <div className="stat-grid">
                      {pieData.map((item, index) => (
                        <div key={index} className="stat-item">
                          <div 
                            className="stat-color" 
                            style={{ backgroundColor: COLORS[index % COLORS.length] }}
                          ></div>
                          <div className="stat-info">
                            <div className="stat-type">{item.name}</div>
                            <div className="stat-count">{item.value} alerts</div>
                          </div>
                        </div>
                      ))}
                    </div>
                  </div>
                </>
              ) : (
                <div className="no-chart-data">
                  <div className="no-chart-icon">📊</div>
                  <div className="no-chart-text">No threat data available</div>
                  <div className="no-chart-subtext">Chart will appear when threats are detected</div>
                </div>
              )}
            </div>
          </section>
        </div>
      </main>
    </div>
  );
}

export default ThreatDetection;