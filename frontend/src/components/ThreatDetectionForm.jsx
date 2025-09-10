// frontend/src/components/ThreatDetectionForm.jsx
import React, { useState } from "react";
import { predictThreat } from "../services/threatApi";
import { toast } from "react-toastify";

export default function ThreatDetectionForm({ onResult }) {
  const [form, setForm] = useState({
    weather_temp_c: 30,
    weather_humidity_pct: 65,
    hive_sound_db: 60,
    hive_sound_peak_freq: 200,
    vibration_hz: 220,
    vibration_var: 10,
    timestamp: new Date().toISOString(),
  });

  function updateField(e) {
    const { name, value } = e.target;
    setForm((s) => ({ ...s, [name]: value }));
  }

  async function handlePredict(e) {
    e?.preventDefault();
    try {
      const payload = {
        ...form,
        // ensure numeric types
        weather_temp_c: Number(form.weather_temp_c),
        weather_humidity_pct: Number(form.weather_humidity_pct),
        hive_sound_db: Number(form.hive_sound_db),
        hive_sound_peak_freq: Number(form.hive_sound_peak_freq),
        vibration_hz: Number(form.vibration_hz),
        vibration_var: Number(form.vibration_var),
        timestamp: new Date(form.timestamp).toISOString(),
      };
      const res = await predictThreat(payload);
      if (res?.threat_type && res.threat_type !== "No_Threat") {
        toast.error(`ALERT: ${res.threat_type} (${(res.probability*100 || 0).toFixed(1)}%)`);
      } else {
        toast.success(`No Threat (Confidence ${(res.probability*100 || 0).toFixed(1)}%)`);
      }
      if (onResult) onResult(res);
    } catch (err) {
      console.error("Prediction error", err);
      toast.error("Prediction failed");
    }
  }

  return (
    <form onSubmit={handlePredict} style={{ display: "grid", gap: 8 }}>
      <div>
        <label>Temperature (°C)</label><br />
        <input name="weather_temp_c" type="number" value={form.weather_temp_c} onChange={updateField} step="0.1" />
      </div>

      <div>
        <label>Humidity (%)</label><br />
        <input name="weather_humidity_pct" type="number" value={form.weather_humidity_pct} onChange={updateField} step="0.1" />
      </div>

      <div>
        <label>Sound (dB)</label><br />
        <input name="hive_sound_db" type="number" value={form.hive_sound_db} onChange={updateField} step="0.1" />
      </div>

      <div>
        <label>Sound peak freq (Hz)</label><br />
        <input name="hive_sound_peak_freq" type="number" value={form.hive_sound_peak_freq} onChange={updateField} step="1" />
      </div>

      <div>
        <label>Vibration (Hz)</label><br />
        <input name="vibration_hz" type="number" value={form.vibration_hz} onChange={updateField} step="1" />
      </div>

      <div>
        <label>Vibration var</label><br />
        <input name="vibration_var" type="number" value={form.vibration_var} onChange={updateField} step="0.1" />
      </div>

      <div style={{ marginTop: 8 }}>
        <button type="submit">Predict Threat</button>
      </div>
    </form>
  );
}
