import axios from "axios";

const API_BASE = import.meta.env.VITE_API_BASE || "http://127.0.0.1:5000/api";

export async function predictThreat(payload) {
  const res = await axios.post(`${API_BASE}/threat/predict`, payload, {
    headers: { "Content-Type": "application/json" },
  });
  return res.data;
}

export async function fetchAlerts(limit = 20) {
  const res = await axios.get(`${API_BASE}/threat/alerts?limit=${limit}`);
  return res.data;
}

export async function getModelInfo() {
  const res = await axios.get(`${API_BASE}/threat/model_info`);
  return res.data;
}
