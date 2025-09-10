// frontend/src/pages/ThreatDetection.jsx
import React, { useState, useEffect } from "react";
import axios from "axios";
import Navbar from "../components/Navbar";
import { RadialBarChart, RadialBar, ResponsiveContainer } from "recharts";
import { FaBug, FaExclamationTriangle, FaCheckCircle } from "react-icons/fa";
import "./ThreatDetection.css";

function ThreatDetection() {
  const [formData, setFormData] = useState({
    weather_temp_c: "",
    weather_humidity_pct: "",
    hive_sound_db: "",
    hive_sound_peak_freq: "",
    vibration_hz: "",
    vibration_var: ""
  });

  const [result, setResult] = useState(null);
  const [alerts, setAlerts] = useState([]);

  useEffect(() => {
    fetchAlerts();
    const id = setInterval(fetchAlerts, 7000);
    return () => clearInterval(id);
  }, []);

  const fetchAlerts = async () => {
    try {
      const res = await axios.get("http://127.0.0.1:5000/api/threat/alerts?limit=10");
      setAlerts(res.data || []);
    } catch (err) {
      console.error("Failed to load alerts:", err);
    }
  };

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData((prev) => ({ ...prev, [name]: value }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      const res = await axios.post("http://127.0.0.1:5000/api/threat/predict", formData, {
        headers: { "Content-Type": "application/json" }
      });
      setResult(res.data);
      fetchAlerts();
    } catch (err) {
      console.error("Prediction error:", err);
      alert("Prediction failed. Check backend logs.");
    }
  };

  const chartData = result
    ? [{ name: "Confidence", value: (result.probability * 100).toFixed(2) }]
    : [];

  return (
    <div className="threat-detection">
      <Navbar />
      <main className="td-main">
        <h1 className="page-title">🐝 Threat Detection & Prevention</h1>
        <div className="td-container">
          {/* Left side - form */}
          <div className="td-left">
            <div className="card form-card">
              <h2>Enter Hive Sensor Data</h2>
              <form onSubmit={handleSubmit} className="td-form">
                {Object.keys(formData).map((f) => (
                  <div key={f} className="form-group">
                    <label>{f.replace(/_/g, " ")}</label>
                    <input
                      name={f}
                      type="number"
                      step="any"
                      required
                      value={formData[f]}
                      onChange={handleChange}
                    />
                  </div>
                ))}
                <button type="submit" className="btn-predict">
                  Predict Threat
                </button>
              </form>
            </div>
          </div>

          {/* Right side - results & alerts */}
          <div className="td-right">
            {result && (
              <div className={`card result-card ${result.threat_type}`}>
                <h3>Prediction Result</h3>
                <p className="threat-type">
                  {result.threat_type === "No_Threat" ? (
                    <FaCheckCircle className="icon safe" />
                  ) : (
                    <FaExclamationTriangle className="icon danger" />
                  )}
                  {result.threat_type}
                </p>
                <div className="confidence">
                  Confidence: {(result.probability * 100).toFixed(1)}%
                </div>

                {result.recommendations && (
                  <div className="recommendations">
                    <h4>
                      Recommended Actions{" "}
                      <span className={`priority ${result.recommendations.priority}`}>
                        {result.recommendations.priority}
                      </span>
                    </h4>
                    <ul>
                      {result.recommendations.actions.map((a, i) => (
                        <li key={i}>✅ {a}</li>
                      ))}
                    </ul>
                    {result.recommendations.notes && (
                      <p className="notes">{result.recommendations.notes}</p>
                    )}
                  </div>
                )}

                <div className="chart-container">
                  <ResponsiveContainer width="100%" height={180}>
                    <RadialBarChart
                      innerRadius="80%"
                      outerRadius="100%"
                      data={chartData}
                      startAngle={180}
                      endAngle={0}
                    >
                      <RadialBar minAngle={15} dataKey="value" fill="#ff4c4c" />
                    </RadialBarChart>
                  </ResponsiveContainer>
                </div>
              </div>
            )}

            <div className="card alerts-card">
              <h3>📢 Live Alerts</h3>
              {alerts.length === 0 && <p>No alerts yet</p>}
              <ul className="alerts-list">
                {alerts.map((a, idx) => (
                  <li key={idx} className={`alert ${a.threat_type}`}>
                    <div className="alert-header">
                      <span className="type">{a.threat_type}</span>
                      <span className="prob">
                        {(a.probability * 100).toFixed(1)}%
                      </span>
                    </div>
                    <div className="time">
                      {new Date(a.timestamp).toLocaleString()}
                    </div>
                    {a.recommendations && (
                      <div className="mini-recs">
                        <ul>
                          {a.recommendations.actions
                            .slice(0, 2)
                            .map((act, i) => (
                              <li key={i}>👉 {act}</li>
                            ))}
                        </ul>
                      </div>
                    )}
                  </li>
                ))}
              </ul>
            </div>
          </div>
        </div>
      </main>
    </div>
  );
}

export default ThreatDetection;
