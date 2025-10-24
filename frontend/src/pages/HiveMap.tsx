import React, { useState, useEffect, useMemo } from "react";
import axios from "axios";
import Navbar from "../components/Navbar";
import mapImage from "../assets/images/map.png";
import "./HiveMap.css";

function HiveMap() {
  const [hives, setHives] = useState<any[]>([]);
  const [potentialLocations, setPotentialLocations] = useState<any[]>([]);
  const [selectedCell, setSelectedCell] = useState<string | null>(null);
  const [predictions, setPredictions] = useState<Record<string, number | null>>({});
  const [cellToLocation, setCellToLocation] = useState<Record<string, any>>({});
  const [maxHoney, setMaxHoney] = useState(1);
  const [rows, setRows] = useState(0);
  const [cols, setCols] = useState(0);
  const [viewMode, setViewMode] = useState<"grid" | "map">("grid");

  // UI state
  const [loading, setLoading] = useState(false);
  const [loadStep, setLoadStep] = useState<"grid" | "predict" | "done" | "">("");
  const [error, setError] = useState<string | null>(null);
  const [toast, setToast] = useState<string | null>(null);

  const API_BASE = "http://127.0.0.1:5000/api";

  const showToast = (msg: string) => {
    setToast(msg);
    setTimeout(() => setToast(null), 3000);
  };

  // === DATA FETCHING ===
  const fetchHives = async () => {
    try {
      const res = await axios.get(`${API_BASE}/hives`);
      setHives(Array.isArray(res.data) ? res.data : []);
    } catch (err) {
      console.error(err);
    }
  };

  const fetchPotentialLocations = async () => {
    try {
      setLoading(true);
      const res = await axios.get(`${API_BASE}/potential-locations`);
      const locs = Array.isArray(res.data) ? res.data : [];
      setPotentialLocations(locs);
      processLocations(locs);
    } catch (err) {
      setError("Failed to load locations.");
    } finally {
      setLoading(false);
    }
  };

  const processLocations = (locs: any[]) => {
    if (!locs.length) {
      setRows(0); setCols(0); return;
    }

    const lats = [...new Set(locs.map(l => l.lat))].sort((a, b) => b - a);
    const lngs = [...new Set(locs.map(l => l.lng))].sort((a, b) => a - b);

    const preds: Record<string, number | null> = {};
    const map: Record<string, any> = {};

    locs.forEach(l => {
      const row = lats.indexOf(l.lat);
      const col = lngs.indexOf(l.lng);
      const id = `${row}-${col}`;
      preds[id] = l.honey_production;
      map[id] = l;
    });

    setPredictions(preds);
    setCellToLocation(map);
    setRows(lats.length);
    setCols(lngs.length);

    const values = Object.values(preds).filter(v => v != null) as number[];
    setMaxHoney(values.length ? Math.max(...values) : 1);
  };

  // === LOAD OPTIMAL LOCATIONS (with animation) ===
  const generateGrid = async () => {
    setLoadStep("grid");
    await axios.get(`${API_BASE}/potential-locations/generate-grid`);
  };

  const predictAll = async () => {
    setLoadStep("predict");
    await axios.get(`${API_BASE}/ml/predict-all`);
  };

  const loadOptimalLocations = async () => {
    setLoading(true);
    setError(null);
    setLoadStep("grid");

    try {
      await generateGrid();
      await predictAll();
      await fetchPotentialLocations();
      setLoadStep("done");
      setTimeout(() => setLoadStep(""), 1500);
      showToast("Predictions loaded!");
    } catch (err: any) {
      setError(err.message || "Failed.");
      setLoadStep("");
    } finally {
      setLoading(false);
    }
  };

  // === CLEAR ALL PREDICTIONS ===
  const clearAllPredictions = async () => {
    if (!window.confirm("Delete ALL predicted honey values? This cannot be undone.")) return;

    try {
      setLoading(true);
      const res = await axios.delete(`${API_BASE}/potential-locations/clear-all-predictions`);
      const cleared = res.data.cleared_count || 0;

      // Update UI
      const newPreds = { ...predictions };
      const newMap = { ...cellToLocation };
      Object.keys(newPreds).forEach(id => {
        newPreds[id] = null;
        if (newMap[id]) newMap[id].honey_production = null;
      });
      setPredictions(newPreds);
      setCellToLocation(newMap);
      setMaxHoney(1);

      showToast(`Cleared ${cleared} prediction${cleared !== 1 ? 's' : ''}!`);
    } catch (err) {
      alert("Failed to clear predictions.");
    } finally {
      setLoading(false);
    }
  };

  // === INITIAL LOAD ===
  useEffect(() => {
    fetchHives();
    fetchPotentialLocations();
  }, []);

  // === GRID INTERACTION ===
  const handleCellClick = (row: number, col: number) => {
    const id = `${row}-${col}`;
    if (cellToLocation[id]) setSelectedCell(id);
  };

  const getCellColor = (id: string) => {
    const v = predictions[id];
    if (v == null) return "#fff";
    const r = v / maxHoney;
    if (r > 0.7) return "var(--green-color)";
    if (r > 0.4) return "var(--blue-color)";
    return "var(--red-color)";
  };

  const toggleViewMode = () => setViewMode(viewMode === "grid" ? "map" : "grid");

  // === MEMOIZED GRID ===
  const grid = useMemo(() => {
    if (rows === 0 || cols === 0) {
      return <p className="no-data">No location data.</p>;
    }
    return Array.from({ length: rows }).map((_, row) => (
      <div key={row} className="grid-row">
        {Array.from({ length: cols }).map((_, col) => {
          const id = `${row}-${col}`;
          return (
            <div
              key={id}
              className="grid-cell"
              onClick={() => handleCellClick(row, col)}
              style={{ backgroundColor: getCellColor(id) }}
            />
          );
        })}
      </div>
    ));
  }, [rows, cols, predictions, maxHoney]);

  // === CHECK IF ANY PREDICTION EXISTS ===
  const hasAnyPrediction = Object.values(predictions).some(v => v != null);

  return (
    <div className="hivemap-page">
      <Navbar />
      <div className="hive-map-container">

        {/* === SIDEBAR === */}
        <aside className="sidebar">
          <h2 className="sidebar-title">Hive Locations</h2>

          <div className="search-container">
            <input type="text" placeholder="Search hives..." className="search-input" />
          </div>

          {error && <p className="error-message">{error}</p>}

          {loading && (
            <div className="loading-animation">
              <div className="spinner"></div>
              <p>
                {loadStep === "grid" && "Generating grid..."}
                {loadStep === "predict" && "AI predicting honey..."}
                {loadStep === "done" && "All set!"}
              </p>
            </div>
          )}

          <ul className="hive-list">
            {hives.map(hive => (
              <li key={hive.id} className="hive-list-item">
                <h3>{hive.name}</h3>
                <p>Lat: {hive.location_lat}, Lng: {hive.location_lng}</p>
              </li>
            ))}
          </ul>

          {/* === ACTION BUTTONS === */}
          <button onClick={loadOptimalLocations} className="action-btn primary" disabled={loading}>
            {loading ? "Working..." : "Load Optimal Locations"}
          </button>

          {hasAnyPrediction && (
            <button onClick={clearAllPredictions} className="action-btn danger" disabled={loading}>
              Clear All Predictions
            </button>
          )}

          <button onClick={toggleViewMode} className="action-btn secondary" disabled={loading}>
            Switch to {viewMode === "grid" ? "Map" : "Grid"}
          </button>
        </aside>

        {/* === MAP === */}
        <main className="map-section">
          <div
            className={`grid-container ${viewMode === "map" ? "map-view" : ""}`}
            style={viewMode === "map" ? { backgroundImage: `url(${mapImage})` } : {}}
          >
            {grid}
          </div>

          {/* Toast */}
          {toast && <div className="toast">{toast}</div>}

          {/* === POPUP (optional single delete) === */}
          {selectedCell && cellToLocation[selectedCell] && (
            <div className="popup-overlay" onClick={() => setSelectedCell(null)}>
              <div className="popup-content" onClick={e => e.stopPropagation()}>
                <h3>Location Details</h3>
                <div className="location-details">
                  <p><strong>Lat:</strong> {cellToLocation[selectedCell].lat}</p>
                  <p><strong>Lng:</strong> {cellToLocation[selectedCell].lng}</p>
                  <p><strong>Temp:</strong> {cellToLocation[selectedCell].temperature} °C</p>
                  <p><strong>Humidity:</strong> {cellToLocation[selectedCell].humidity}%</p>
                  <p><strong>Sunlight:</strong> {cellToLocation[selectedCell].sunlight_exposure} h</p>
                  <p><strong>Wind:</strong> {cellToLocation[selectedCell].wind_speed} km/h</p>
                  <p><strong>Water:</strong> {cellToLocation[selectedCell].dist_to_water_source.toFixed(2)} km</p>
                  <p><strong>Flowers:</strong> {cellToLocation[selectedCell].dist_to_flowering_area.toFixed(2)} km</p>
                  <p><strong>Feed:</strong> {cellToLocation[selectedCell].dist_to_feeding_station.toFixed(2)} km</p>

                  <p className="honey-pred">
                    <strong>Honey:</strong>{" "}
                    {cellToLocation[selectedCell].honey_production !== null
                      ? `${cellToLocation[selectedCell].honey_production.toFixed(2)} kg`
                      : "Not predicted"}
                  </p>
                </div>

                <div className="form-buttons">
                  <button onClick={() => setSelectedCell(null)} className="btn-close">
                    Close
                  </button>
                  {cellToLocation[selectedCell].honey_production !== null && (
                    <button
                      onClick={async () => {
                        const id = cellToLocation[selectedCell].id;
                        await axios.delete(`${API_BASE}/potential-locations/${id}/honey-production`);
                        setCellToLocation(p => ({ ...p, [selectedCell]: { ...p[selectedCell], honey_production: null } }));
                        setPredictions(p => ({ ...p, [selectedCell]: null }));
                        const vals = Object.values(predictions).filter(v => v != null) as number[];
                        setMaxHoney(vals.length ? Math.max(...vals) : 1);
                        showToast("Prediction cleared!");
                      }}
                      className="btn-delete"
                    >
                      Clear This One
                    </button>
                  )}
                </div>
              </div>
            </div>
          )}
        </main>
      </div>
    </div>
  );
}

export default HiveMap;