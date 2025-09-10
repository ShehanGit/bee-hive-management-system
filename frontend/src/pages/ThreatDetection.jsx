import React, { useState } from "react";
import axios from "axios";
import Navbar from "../components/Navbar";
import {
  RadialBarChart, RadialBar, Legend, ResponsiveContainer
} from "recharts";
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

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData((prev) => ({ ...prev, [name]: value }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      const res = await axios.post("http://127.0.0.1:5000/api/threat/predict", formData);
      setResult(res.data);
    } catch (error) {
      console.error("Prediction error:", error);
      alert("Failed to fetch prediction. Check backend.");
    }
  };

  // Prepare chart data
  const chartData = result
    ? [{ name: "Confidence", value: (result.probability * 100).toFixed(2), fill: "#FF4C4C" }]
    : [];

  return (
    <div className="threat-detection">
      <Navbar />
      <main>
        <h1>🐝 AI-Powered Threat Detection</h1>
        
        {/* Input Form */}
        <section className="form-section">
          <h2>Enter Hive Data</h2>
          <form onSubmit={handleSubmit}>
            {Object.keys(formData).map((field) => (
              <div className="form-group" key={field}>
                <label>{field.replace(/_/g, " ")}</label>
                <input
                  type="number"
                  step="any"
                  name={field}
                  value={formData[field]}
                  onChange={handleChange}
                  required
                />
              </div>
            ))}
            <button type="submit">🔍 Predict Threat</button>
          </form>
        </section>

        {/* Results Section */}
        {result && (
          <section className="result-section">
            <div className={`result-card ${result.threat_type}`}>
              <h2>Prediction Result</h2>
              <p><strong>Threat Type:</strong> {result.threat_type}</p>
              <p><strong>Confidence:</strong> {(result.probability * 100).toFixed(2)}%</p>
            </div>

            <div className="chart-container">
              <h3>Confidence Level</h3>
              <ResponsiveContainer width="100%" height={250}>
                <RadialBarChart
                  innerRadius="80%"
                  outerRadius="100%"
                  barSize={30}
                  data={chartData}
                  startAngle={180}
                  endAngle={0}
                >
                  <RadialBar minAngle={15} background clockWise dataKey="value" />
                  <Legend iconSize={10} layout="horizontal" verticalAlign="bottom" align="center" />
                </RadialBarChart>
              </ResponsiveContainer>
            </div>
          </section>
        )}
      </main>
    </div>
  );
}

export default ThreatDetection;
