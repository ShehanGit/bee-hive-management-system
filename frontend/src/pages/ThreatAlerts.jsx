import React, { useEffect, useState } from "react";
import axios from "axios";
import io from "socket.io-client";
import Navbar from "../components/Navbar";
import {
  LineChart, Line, XAxis, YAxis, Tooltip, CartesianGrid, Legend, ResponsiveContainer,
  PieChart, Pie, Cell
} from "recharts";
import "./ThreatAlerts.css";

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

// Get recommendations for threat types
const getRecommendation = (threatType) => {
  switch (threatType) {
    case "Wax_Moth":
      return [
        "Inspect hive for wax moth larvae",
        "Remove infested frames immediately",
        "Apply Bacillus thuringiensis treatment",
        "Improve hive ventilation"
      ];
    case "Predator":
      return [
        "Check hive entrance reducer",
        "Install predator guards",
        "Secure hive stand",
        "Monitor for signs of attack"
      ];
    case "Environmental":
      return [
        "Check weather conditions",
        "Provide additional ventilation",
        "Monitor temperature and humidity",
        "Consider hive relocation if severe"
      ];
    case "No_Threat":
      return ["Continue regular monitoring"];
    default:
      return ["Monitor hive conditions"];
  }
};

function ThreatAlerts() {
  const [alerts, setAlerts] = useState([]);
  const [currentPage, setCurrentPage] = useState(1);
  const [selectedAlert, setSelectedAlert] = useState(null); // for popup
  const [socket, setSocket] = useState(null);
  const [realTimeData, setRealTimeData] = useState(null);
  const [threatLevel, setThreatLevel] = useState("unknown");
  const [isConnected, setIsConnected] = useState(false);
  const alertsPerPage = 10;

  // Initialize Socket.IO connection
  useEffect(() => {
    const newSocket = io("http://127.0.0.1:5000");
    setSocket(newSocket);

    // Connection event handlers
    newSocket.on("connect", () => {
      console.log("Connected to threat detection server");
      setIsConnected(true);
    });

    newSocket.on("disconnect", () => {
      console.log("Disconnected from threat detection server");
      setIsConnected(false);
    });

    // Real-time threat detection updates
    newSocket.on("threat_detection_update", (data) => {
      console.log("Real-time threat detection update:", data);
      setRealTimeData(data);
      
      // Update threat level
      if (data.threat_trend && data.threat_trend.current_threat_level) {
        const level = data.threat_trend.current_threat_level;
        if (level >= 0.8) setThreatLevel("critical");
        else if (level >= 0.6) setThreatLevel("high");
        else if (level >= 0.4) setThreatLevel("moderate");
        else if (level >= 0.2) setThreatLevel("low");
        else setThreatLevel("minimal");
      }
    });

    // Real-time threat alerts
    newSocket.on("threat_alert", (alertData) => {
      console.log("🚨 REAL-TIME THREAT ALERT:", alertData);
      
      // Add new alert to the beginning of the list
      setAlerts(prevAlerts => [alertData.alert_data, ...prevAlerts]);
      
      // Show browser notification if permission granted
      if (Notification.permission === "granted") {
        new Notification(`Threat Alert: ${alertData.threat_type}`, {
          body: `Probability: ${(alertData.probability * 100).toFixed(1)}%`,
          icon: "/favicon.ico"
        });
      }
    });

    return () => {
      newSocket.close();
    };
  }, []);

  // Request notification permission
  useEffect(() => {
    if (Notification.permission === "default") {
      Notification.requestPermission();
    }
  }, []);

  // Fetch initial alerts and set up polling
  useEffect(() => {
    const fetchAlerts = async () => {
      try {
        const res = await axios.get("http://127.0.0.1:5000/api/threat/alerts");
        // Attach recommendations if missing
        const alertsWithRecs = res.data.map(alert => ({
          ...alert,
          recommendations:
            alert.recommendations || getRecommendation(alert.threat_type),
        }));
        setAlerts(alertsWithRecs);
      } catch (error) {
        console.error("Error fetching alerts:", error);
      }
    };

    fetchAlerts();
    const interval = setInterval(fetchAlerts, 10000); // Poll every 10 seconds
    return () => clearInterval(interval);
  }, []);


  // Pagination
  const indexOfLast = currentPage * alertsPerPage;
  const indexOfFirst = indexOfLast - alertsPerPage;
  const currentAlerts = alerts.slice(indexOfFirst, indexOfLast);
  const totalPages = Math.ceil(alerts.length / alertsPerPage);

  // Chart Data
  const pieData = alerts.reduce((acc, alert) => {
    const existing = acc.find(a => a.name === alert.threat_type);
    if (existing) existing.value++;
    else acc.push({ name: alert.threat_type, value: 1 });
    return acc;
  }, []);

  const COLORS = ["#0088FE", "#FF8042", "#00C49F", "#FFBB28"];

  return (
    <div className="threat-alerts">
      <Navbar />
      <main>
        <div className="header-section">
          <h1>🚨 Real-Time Hive Threat Alerts</h1>
          
          {/* Real-time Status */}
          <div className="real-time-status">
            <div className={`connection-status ${isConnected ? 'connected' : 'disconnected'}`}>
              <div className="status-indicator"></div>
              <span>{isConnected ? 'Connected' : 'Disconnected'}</span>
            </div>
            
            <div className={`threat-level ${threatLevel}`}>
              <span className="threat-label">Threat Level:</span>
              <span className="threat-value">{threatLevel.toUpperCase()}</span>
            </div>
            
            {realTimeData && (
              <div className="latest-prediction">
                <span className="prediction-label">Latest:</span>
                <span className="prediction-value">
                  {getThreatIcon(realTimeData.prediction?.threat_type)} {realTimeData.prediction?.threat_type}
                </span>
                <span className="prediction-prob">
                  ({(realTimeData.prediction?.probability * 100).toFixed(1)}%)
                </span>
              </div>
            )}
          </div>
        </div>

        <div className="charts-container">
          {/* Pie Chart */}
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
              </PieChart>
            </ResponsiveContainer>
          </div>

          {/* Line Chart */}
          <div className="chart-box">
            <h2>Threat Probability Trend</h2>
            <ResponsiveContainer width="100%" height={250}>
              <LineChart data={alerts}>
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis dataKey="timestamp" />
                <YAxis />
                <Tooltip />
                <Line type="monotone" dataKey="probability" stroke="#FF0000" dot />
              </LineChart>
            </ResponsiveContainer>
          </div>
        </div>

        {/* Alerts Table */}
        <div className="alerts-table">
          <h2>📋 Recent Alerts</h2>
          <div className="table-container">
            <table className="paginated-alerts-table">
              <thead>
                <tr>
                  <th>Timestamp</th>
                  <th>Threat Type</th>
                  <th>Probability</th>
                  <th>Action</th>
                </tr>
              </thead>
              <tbody>
                {currentAlerts.length > 0 ? (
                  currentAlerts.map((alert, idx) => (
                    <tr key={idx}>
                      <td>
                        {alert.timestamp
                          ? new Date(alert.timestamp).toLocaleString()
                          : "—"}
                      </td>
                      <td>
                        <span className="threat-icon">
                          {getThreatIcon(alert.threat_type)}
                        </span>{" "}
                        {alert.threat_type}
                      </td>
                      <td>{(alert.probability * 100).toFixed(1)}%</td>
                      <td>
                        <button
                          className="action-btn"
                          onClick={() => setSelectedAlert(alert)}
                        >
                          View
                        </button>
                      </td>
                    </tr>
                  ))
                ) : (
                  <tr>
                    <td colSpan="4" style={{ textAlign: "center" }}>
                      No alerts available
                    </td>
                  </tr>
                )}
              </tbody>
            </table>
          </div>

          {/* Pagination */}
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

        {/* Recommendation Modal */}
        {selectedAlert && (
          <div className="modal-overlay">
            <div className="modal-card">
              <h2>
                {getThreatIcon(selectedAlert.threat_type)} {selectedAlert.threat_type}
              </h2>
              <p><b>Probability:</b> {(selectedAlert.probability * 100).toFixed(1)}%</p>
              <h3>Recommended Actions:</h3>
              {selectedAlert.recommendations && selectedAlert.recommendations.length > 0 ? (
                <ul>
                  {selectedAlert.recommendations.map((rec, i) => (
                    <li key={i}>✅ {rec}</li>
                  ))}
                </ul>
              ) : (
                <p>No recommendations available</p>
              )}
              <button className="close-btn" onClick={() => setSelectedAlert(null)}>Close</button>
            </div>
          </div>
        )}
      </main>
    </div>
  );
}

export default ThreatAlerts;
