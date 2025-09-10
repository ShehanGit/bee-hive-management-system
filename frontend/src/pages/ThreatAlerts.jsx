import React, { useEffect, useState } from "react";
import { fetchAlerts } from "../services/threatApi";
import Navbar from "../components/Navbar";
import {
  LineChart, Line, XAxis, YAxis, Tooltip, CartesianGrid, Legend, ResponsiveContainer,
  PieChart, Pie, Cell
} from "recharts";
import "./ThreatAlerts.css";

function ThreatAlerts() {
  const [alerts, setAlerts] = useState([]);

  useEffect(() => {
    loadAlerts();
  }, []);

  const loadAlerts = async () => {
    try {
      const data = await fetchAlerts(10);
      setAlerts(data);
    } catch (error) {
      console.error("Error fetching alerts:", error);
    }
  };

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

        {/* Alerts Table */}
        <div className="alerts-table">
          <h2>📋 Recent Alerts</h2>
          <table>
            <thead>
              <tr>
                <th>Timestamp</th>
                <th>Threat Type</th>
                <th>Probability</th>
              </tr>
            </thead>
            <tbody>
              {alerts.map((alert, idx) => (
                <tr key={idx}>
                  <td>{alert.timestamp}</td>
                  <td>{alert.threat_type}</td>
                  <td>{(alert.probability * 100).toFixed(2)}%</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </main>
    </div>
  );
}

export default ThreatAlerts;
