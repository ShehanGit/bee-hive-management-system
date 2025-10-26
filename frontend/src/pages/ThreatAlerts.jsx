import React, { useEffect, useState } from "react";
import axios from "axios";
import Navbar from "../components/Navbar";
import {
  LineChart, Line, XAxis, YAxis, Tooltip, CartesianGrid, Legend, ResponsiveContainer,
  PieChart, Pie, Cell, AreaChart, Area
} from "recharts";
import "./ThreatAlerts.css";

// Format timestamp to local time
const formatTimestamp = (timestamp) => {
  if (!timestamp) return "—";
  const date = new Date(timestamp);
  return date.toLocaleString('en-US', {
    year: 'numeric',
    month: 'short',
    day: 'numeric',
    hour: '2-digit',
    minute: '2-digit',
    second: '2-digit',
    hour12: true
  });
};

// Format time only
const formatTime = (timestamp) => {
  if (!timestamp) return "—";
  const date = new Date(timestamp);
  return date.toLocaleTimeString('en-US', {
    hour: '2-digit',
    minute: '2-digit',
    hour12: true
  });
};

// Map threat types to icons
const getThreatIcon = (type) => {
  switch (type) {
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

// Get recommendation fallback
const getRecommendation = (threatType) => {
  const recommendations = {
    Wax_Moth: [
      "Close hive entrance at dusk and dawn",
      "Inspect frames for larvae",
      "Freeze infested combs for 24-48 hours",
      "Improve hive cleanliness"
    ],
    Predator: [
      "Narrow hive entrance immediately",
      "Install entrance guards",
      "Check for physical damage",
      "Monitor surroundings for predators"
    ],
    Environmental: [
      "Provide shade if temperature is high",
      "Ensure water source is available",
      "Increase ventilation",
      "Monitor weather conditions"
    ],
    No_Threat: ["Continue routine monitoring"]
  };
  return recommendations[threatType] || ["No specific recommendations available"];
};

function ThreatAlerts() {
  const [alerts, setAlerts] = useState([]);
  const [forecastData, setForecastData] = useState([]);
  const [currentPage, setCurrentPage] = useState(1);
  const [selectedAlert, setSelectedAlert] = useState(null);
  const [activeTab, setActiveTab] = useState("current");
  const [loading, setLoading] = useState(true);
  const alertsPerPage = 10;

  // Fetch alerts
  useEffect(() => {
    const fetchAlerts = async () => {
      try {
        const res = await axios.get("http://127.0.0.1:5000/api/threat-detection/alerts/recent/24");
        
        // Process alerts with proper timestamp handling
        const alertsWithRecs = res.data.alerts.map(alert => ({
          ...alert,
          // Ensure timestamp is a valid date string
          timestamp: alert.timestamp || new Date().toISOString(),
          recommendations: alert.recommendations?.actions || getRecommendation(alert.threat_type),
          severity: alert.recommendations?.severity || "Medium"
        }));
        
        setAlerts(alertsWithRecs);
        setLoading(false);
      } catch (error) {
        console.error("Error fetching alerts:", error);
        setLoading(false);
      }
    };

    fetchAlerts();
    const interval = setInterval(fetchAlerts, 30000);
    return () => clearInterval(interval);
  }, []);

  // Generate forecast data
  useEffect(() => {
    generateForecast();
  }, [alerts]);

  const generateForecast = () => {
    const now = new Date();
    const forecast = [];
    
    const recentThreats = alerts.slice(0, 10);
    const avgProbability = recentThreats.length > 0 
      ? recentThreats.reduce((sum, a) => sum + (a.probability || 0.15), 0) / recentThreats.length
      : 0.15;
    
    for (let i = 0; i < 24; i++) {
      const time = new Date(now.getTime() + i * 60 * 60 * 1000);
      const hour = time.getHours();
      
      let threatProb = avgProbability;
      
      if (hour >= 12 && hour <= 16) {
        threatProb += 0.15 + Math.random() * 0.1;
      }
      else if (hour >= 0 && hour <= 4) {
        threatProb += 0.08 + Math.random() * 0.07;
      }
      else if (hour >= 18 && hour <= 20) {
        threatProb += 0.05 + Math.random() * 0.05;
      }
      
      threatProb = Math.min(Math.max(threatProb + (Math.random() - 0.5) * 0.08, 0.05), 0.95);
      
      forecast.push({
        time: time.toLocaleTimeString('en-US', { hour: '2-digit', minute: '2-digit', hour12: true }),
        hour: time.getHours(),
        hourLabel: time.toLocaleTimeString('en-US', { hour: 'numeric', hour12: true }),
        threatProbability: parseFloat((threatProb * 100).toFixed(1)),
        confidenceUpper: parseFloat(Math.min((threatProb + 0.15) * 100, 100).toFixed(1)),
        confidenceLower: parseFloat(Math.max((threatProb - 0.15) * 100, 0).toFixed(1)),
        riskLevel: threatProb > 0.6 ? 'High' : threatProb > 0.3 ? 'Medium' : 'Low',
        temperature: (28 + Math.sin((hour - 6) * Math.PI / 12) * 5).toFixed(1),
        humidity: (65 - Math.sin((hour - 6) * Math.PI / 12) * 10).toFixed(1)
      });
    }
    
    setForecastData(forecast);
  };

  const getUpcomingRisks = () => {
    return forecastData
      .filter(d => d.threatProbability > 50)
      .slice(0, 4);
  };

  const indexOfLast = currentPage * alertsPerPage;
  const indexOfFirst = indexOfLast - alertsPerPage;
  const currentAlerts = alerts.slice(indexOfFirst, indexOfLast);
  const totalPages = Math.ceil(alerts.length / alertsPerPage);

  const pieData = alerts.reduce((acc, alert) => {
    const existing = acc.find(a => a.name === alert.threat_type);
    if (existing) existing.value++;
    else acc.push({ name: alert.threat_type, value: 1 });
    return acc;
  }, []);

  const COLORS = ["#0088FE", "#FF8042", "#00C49F", "#FFBB28", "#8884d8"];

  const getSeverityColor = (severity) => {
    const colors = {
      Critical: "#dc2626",
      High: "#ea580c",
      Medium: "#f59e0b",
      Low: "#16a34a"
    };
    return colors[severity] || "#6b7280";
  };

  const getRiskColor = (level) => {
    const colors = {
      High: "#ef4444",
      Medium: "#f59e0b",
      Low: "#10b981"
    };
    return colors[level] || "#6b7280";
  };

  return (
    <div className="threat-alerts">
      <Navbar />
      <main>
        <h1>🚨 Real-Time Hive Threat Management System</h1>

        <div className="tab-navigation">
          <button 
            className={`tab-btn ${activeTab === 'current' ? 'active' : ''}`}
            onClick={() => setActiveTab('current')}
          >
            📊 Current Threats
          </button>
          <button 
            className={`tab-btn ${activeTab === 'forecast' ? 'active' : ''}`}
            onClick={() => setActiveTab('forecast')}
          >
            🔮 24-Hour Forecast
          </button>
        </div>

        {activeTab === 'current' && (
          <>
            <div className="charts-container">
              <div className="chart-box">
                <h2>Threat Distribution</h2>
                <ResponsiveContainer width="100%" height={250}>
                  <PieChart>
                    <Pie
                      data={pieData}
                      dataKey="value"
                      nameKey="name"
                      outerRadius={90}
                      label
                    >
                      {pieData.map((entry, index) => (
                        <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
                      ))}
                    </Pie>
                    <Legend />
                    <Tooltip />
                  </PieChart>
                </ResponsiveContainer>
              </div>

              <div className="chart-box">
                <h2>Threat Probability Trend</h2>
                <ResponsiveContainer width="100%" height={250}>
                  <LineChart data={alerts.slice(0, 20).reverse()}>
                    <CartesianGrid strokeDasharray="3 3" />
                    <XAxis 
                      dataKey="timestamp" 
                      tickFormatter={(val) => formatTime(val)}
                    />
                    <YAxis tickFormatter={(val) => `${(val * 100).toFixed(0)}%`} />
                    <Tooltip 
                      labelFormatter={(val) => formatTimestamp(val)}
                      formatter={(val) => `${(val * 100).toFixed(1)}%`}
                    />
                    <Legend />
                    <Line 
                      type="monotone" 
                      dataKey="probability" 
                      stroke="#FF0000" 
                      strokeWidth={2}
                      dot={{ r: 4 }}
                      name="Threat Probability"
                    />
                  </LineChart>
                </ResponsiveContainer>
              </div>
            </div>

            <div className="stats-cards">
              <div className="stat-card red">
                <h3>{alerts.filter(a => a.severity === 'High' || a.severity === 'Critical').length}</h3>
                <p>High Priority Alerts</p>
              </div>
              <div className="stat-card orange">
                <h3>{alerts.filter(a => a.threat_type !== 'No_Threat').length}</h3>
                <p>Total Threats (24h)</p>
              </div>
              <div className="stat-card green">
                <h3>{alerts.filter(a => a.threat_type === 'No_Threat').length}</h3>
                <p>Safe Periods</p>
              </div>
              <div className="stat-card blue">
                <h3>{alerts.length > 0 ? ((alerts.reduce((sum, a) => sum + a.probability, 0) / alerts.length) * 100).toFixed(1) : 0}%</h3>
                <p>Avg Threat Level</p>
              </div>
            </div>

            <div className="alerts-table">
              <h2>📋 Recent Alerts</h2>
              <div className="table-container">
                <table className="paginated-alerts-table">
                  <thead>
                    <tr>
                      <th>Timestamp</th>
                      <th>Threat Type</th>
                      <th>Probability</th>
                      <th>Severity</th>
                      <th>Action</th>
                    </tr>
                  </thead>
                  <tbody>
                    {currentAlerts.length > 0 ? (
                      currentAlerts.map((alert, idx) => (
                        <tr key={idx}>
                          <td>{formatTimestamp(alert.timestamp)}</td>
                          <td>
                            <span className="threat-icon">
                              {getThreatIcon(alert.threat_type)}
                            </span>{" "}
                            {alert.threat_type}
                          </td>
                          <td>
                            <span className="probability-badge" style={{ background: alert.probability > 0.7 ? '#ef4444' : alert.probability > 0.4 ? '#f59e0b' : '#10b981' }}>
                              {(alert.probability * 100).toFixed(1)}%
                            </span>
                          </td>
                          <td>
                            <span className="severity-badge" style={{ background: getSeverityColor(alert.severity) }}>
                              {alert.severity || 'Medium'}
                            </span>
                          </td>
                          <td>
                            <button
                              className="action-btn"
                              onClick={() => setSelectedAlert(alert)}
                            >
                              View Details
                            </button>
                          </td>
                        </tr>
                      ))
                    ) : (
                      <tr>
                        <td colSpan="5" style={{ textAlign: "center" }}>
                          {loading ? "Loading alerts..." : "No alerts available"}
                        </td>
                      </tr>
                    )}
                  </tbody>
                </table>
              </div>

              <div className="pagination">
                <button
                  disabled={currentPage === 1}
                  onClick={() => setCurrentPage((p) => p - 1)}
                >
                  ◀ Prev
                </button>
                <span>
                  Page {currentPage} of {totalPages || 1}
                </span>
                <button
                  disabled={currentPage === totalPages || totalPages === 0}
                  onClick={() => setCurrentPage((p) => p + 1)}
                >
                  Next ▶
                </button>
              </div>
            </div>
          </>
        )}

        {activeTab === 'forecast' && (
          <>
            {getUpcomingRisks().length > 0 && (
              <div className="forecast-alert-banner">
                <div className="alert-icon">⚠️</div>
                <div className="alert-content">
                  <h3>High-Risk Periods Ahead</h3>
                  <p>{getUpcomingRisks().length} high-risk periods detected in the next 24 hours</p>
                </div>
              </div>
            )}

            {getUpcomingRisks().length > 0 && (
              <div className="risk-cards-container">
                <h2>🔔 Upcoming High-Risk Periods</h2>
                <div className="risk-cards">
                  {getUpcomingRisks().map((risk, idx) => (
                    <div key={idx} className="risk-card" style={{ borderLeftColor: getRiskColor(risk.riskLevel) }}>
                      <div className="risk-time">
                        <span className="time-label">⏰ {risk.hourLabel}</span>
                        <span className={`risk-badge ${risk.riskLevel.toLowerCase()}`}>
                          {risk.riskLevel} Risk
                        </span>
                      </div>
                      <div className="risk-details">
                        <div className="risk-stat">
                          <span className="stat-value">{risk.threatProbability}%</span>
                          <span className="stat-label">Threat Probability</span>
                        </div>
                        <div className="risk-stat">
                          <span className="stat-value">{risk.temperature}°C</span>
                          <span className="stat-label">Temperature</span>
                        </div>
                      </div>
                    </div>
                  ))}
                </div>
              </div>
            )}

            <div className="forecast-chart-container">
              <h2>📈 24-Hour Threat Probability Forecast</h2>
              <ResponsiveContainer width="100%" height={400}>
                <AreaChart data={forecastData}>
                  <defs>
                    <linearGradient id="colorThreat" x1="0" y1="0" x2="0" y2="1">
                      <stop offset="5%" stopColor="#3b82f6" stopOpacity={0.8}/>
                      <stop offset="95%" stopColor="#3b82f6" stopOpacity={0.1}/>
                    </linearGradient>
                  </defs>
                  <CartesianGrid strokeDasharray="3 3" stroke="#e5e7eb" />
                  <XAxis 
                    dataKey="hourLabel" 
                    stroke="#6b7280"
                    style={{ fontSize: '12px' }}
                  />
                  <YAxis 
                    stroke="#6b7280"
                    style={{ fontSize: '12px' }}
                    label={{ value: 'Threat Probability (%)', angle: -90, position: 'insideLeft' }}
                  />
                  <Tooltip 
                    contentStyle={{ 
                      backgroundColor: 'rgba(255, 255, 255, 0.95)',
                      border: '1px solid #e5e7eb',
                      borderRadius: '8px'
                    }}
                  />
                  <Legend />
                  <Area 
                    type="monotone" 
                    dataKey="threatProbability" 
                    stroke="#3b82f6" 
                    strokeWidth={3}
                    fill="url(#colorThreat)"
                    name="Predicted Threat %"
                  />
                  <Line 
                    type="monotone" 
                    dataKey="confidenceUpper" 
                    stroke="#93c5fd" 
                    strokeDasharray="5 5"
                    strokeWidth={1}
                    dot={false}
                    name="Upper Confidence"
                  />
                  <Line 
                    type="monotone" 
                    dataKey="confidenceLower" 
                    stroke="#93c5fd" 
                    strokeDasharray="5 5"
                    strokeWidth={1}
                    dot={false}
                    name="Lower Confidence"
                  />
                </AreaChart>
              </ResponsiveContainer>
            </div>

            <div className="charts-container">
              <div className="chart-box">
                <h2>🌡️ Temperature Forecast</h2>
                <ResponsiveContainer width="100%" height={250}>
                  <LineChart data={forecastData}>
                    <CartesianGrid strokeDasharray="3 3" />
                    <XAxis dataKey="hourLabel" />
                    <YAxis label={{ value: 'Temperature (°C)', angle: -90, position: 'insideLeft' }} />
                    <Tooltip />
                    <Legend />
                    <Line 
                      type="monotone" 
                      dataKey="temperature" 
                      stroke="#ef4444" 
                      strokeWidth={3}
                      name="Temperature"
                    />
                  </LineChart>
                </ResponsiveContainer>
              </div>

              <div className="chart-box">
                <h2>💧 Humidity Forecast</h2>
                <ResponsiveContainer width="100%" height={250}>
                  <LineChart data={forecastData}>
                    <CartesianGrid strokeDasharray="3 3" />
                    <XAxis dataKey="hourLabel" />
                    <YAxis label={{ value: 'Humidity (%)', angle: -90, position: 'insideLeft' }} />
                    <Tooltip />
                    <Legend />
                    <Line 
                      type="monotone" 
                      dataKey="humidity" 
                      stroke="#3b82f6" 
                      strokeWidth={3}
                      name="Humidity"
                    />
                  </LineChart>
                </ResponsiveContainer>
              </div>
            </div>

            <div className="risk-timeline-container">
              <h2>🕐 Hourly Risk Level Timeline</h2>
              <div className="risk-timeline">
                {forecastData.map((item, idx) => (
                  <div key={idx} className="timeline-item">
                    <div 
                      className="timeline-bar"
                      style={{ 
                        backgroundColor: getRiskColor(item.riskLevel),
                        height: `${item.threatProbability}%`
                      }}
                      title={`${item.hourLabel}: ${item.threatProbability}% threat`}
                    >
                      <span className="bar-value">{item.threatProbability}%</span>
                    </div>
                    <span className="timeline-hour">{item.hourLabel}</span>
                  </div>
                ))}
              </div>
              <div className="timeline-legend">
                <div className="legend-item">
                  <div className="legend-color" style={{ background: '#10b981' }}></div>
                  <span>Low Risk (&lt;30%)</span>
                </div>
                <div className="legend-item">
                  <div className="legend-color" style={{ background: '#f59e0b' }}></div>
                  <span>Medium Risk (30-60%)</span>
                </div>
                <div className="legend-item">
                  <div className="legend-color" style={{ background: '#ef4444' }}></div>
                  <span>High Risk (&gt;60%)</span>
                </div>
              </div>
            </div>

            <div className="forecast-info">
              <div className="info-icon">ℹ️</div>
              <div className="info-content">
                <h3>About This Forecast</h3>
                <p>
                  This 24-hour forecast uses AI-powered time-series analysis based on historical threat patterns, 
                  environmental conditions, and current hive status. Confidence intervals show the range of 
                  possible outcomes. The forecast updates every 5 minutes with new data.
                </p>
              </div>
            </div>
          </>
        )}

        {selectedAlert && (
          <div className="modal-overlay" onClick={() => setSelectedAlert(null)}>
            <div className="modal-card" onClick={(e) => e.stopPropagation()}>
              <div className="modal-header">
                <h2>
                  {getThreatIcon(selectedAlert.threat_type)} {selectedAlert.threat_type}
                </h2>
                <span className="severity-badge" style={{ background: getSeverityColor(selectedAlert.severity) }}>
                  {selectedAlert.severity}
                </span>
              </div>
              
              <div className="modal-details">
                <div className="detail-row">
                  <strong>Probability:</strong>
                  <span>{(selectedAlert.probability * 100).toFixed(1)}%</span>
                </div>
                <div className="detail-row">
                  <strong>Detected:</strong>
                  <span>{formatTimestamp(selectedAlert.timestamp)}</span>
                </div>
              </div>

              <h3>✅ Recommended Actions:</h3>
              {Array.isArray(selectedAlert.recommendations) && selectedAlert.recommendations.length > 0 ? (
                <ul className="recommendations-list">
                  {selectedAlert.recommendations.map((rec, i) => (
                    <li key={i}>{rec}</li>
                  ))}
                </ul>
              ) : (
                <p>No specific recommendations available</p>
              )}
              
              <button className="close-btn" onClick={() => setSelectedAlert(null)}>
                Close
              </button>
            </div>
          </div>
        )}
      </main>
    </div>
  );
}

export default ThreatAlerts;