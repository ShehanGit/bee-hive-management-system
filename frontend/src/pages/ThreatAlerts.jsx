import React, { useEffect, useState } from "react";
import axios from "axios";
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

function ThreatAlerts() {
  const [alerts, setAlerts] = useState([]);
  const [currentPage, setCurrentPage] = useState(1);
  const alertsPerPage = 10;

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
    const interval = setInterval(fetchAlerts, 5000);
    return () => clearInterval(interval);
  }, []);

  // Pagination calculations
  const indexOfLast = currentPage * alertsPerPage;
  const indexOfFirst = indexOfLast - alertsPerPage;
  const currentAlerts = alerts.slice(indexOfFirst, indexOfLast);
  const totalPages = Math.ceil(alerts.length / alertsPerPage);

  // Prepare chart data
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
        <h1>🚨 Real-Time Hive Threat Alerts</h1>

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

        {/* Updated Alerts Table with Pagination */}
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
                        <button className="action-btn">View</button>
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

          {/* Pagination Controls */}
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
      </main>
    </div>
  );
}

export default ThreatAlerts;