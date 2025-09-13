// frontend/src/components/ThreatAlertList.jsx
import React, { useEffect, useState, useRef } from "react";
import { fetchAlerts } from "../services/threatApi";

export default function ThreatAlertList({ pollInterval = 5000 }) {
  const [alerts, setAlerts] = useState([]);
  const isMounted = useRef(true);

  async function loadAlerts() {
    try {
      const data = await fetchAlerts(20);
      if (isMounted.current) setAlerts(data);
    } catch (err) {
      console.error("Failed to load alerts:", err);
    }
  }

  useEffect(() => {
    isMounted.current = true;
    loadAlerts();
    const t = setInterval(loadAlerts, pollInterval);
    return () => {
      isMounted.current = false;
      clearInterval(t);
    };
  }, [pollInterval]);

  return (
    <div className="threat-alert-list" style={{ maxHeight: 420, overflowY: "auto", border: "1px solid #ddd", padding: 10 }}>
      <h3>Recent Alerts</h3>
      {alerts.length === 0 && <div style={{ color: "#666" }}>No alerts yet.</div>}
      {alerts.map((a, i) => (
        <div key={i} style={{ padding: 8, borderBottom: "1px solid #eee" }}>
          <div style={{ fontWeight: 600 }}>
            {a.threat_type} <span style={{ fontWeight: 400, color: "#777" }}>({new Date(a.timestamp).toLocaleString()})</span>
          </div>
          <div style={{ fontSize: 13, color: "#444" }}>
            Prob: {(a.probability * 100 || 0).toFixed(1)}% — T: {a.used_features.weather_temp_c}°C, H: {a.used_features.weather_humidity_pct}%, S: {a.used_features.hive_sound_db}dB, V: {a.used_features.vibration_hz}Hz
          </div>
        </div>
      ))}
    </div>
  );
}
