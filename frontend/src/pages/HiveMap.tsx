import React, { useState, useEffect, useMemo } from "react";
import axios from "axios";
import Navbar from "../components/Navbar";
import mapImage from "../assets/images/map.png";
import "./HiveMap.css";

function HiveMap() {
  const [hives, setHives] = useState([]);
  const [potentialLocations, setPotentialLocations] = useState([]);
  const [selectedCell, setSelectedCell] = useState(null);
  const [predictions, setPredictions] = useState({});
  const [cellToLocation, setCellToLocation] = useState({});
  const [maxHoney, setMaxHoney] = useState(1);
  const [rows, setRows] = useState(0);
  const [cols, setCols] = useState(0);
  const [viewMode, setViewMode] = useState("grid");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const API_BASE = "http://127.0.0.1:5000/api";

  // Fetch hives
  const fetchHives = async () => {
    try {
      const res = await axios.get(`${API_BASE}/hives`);
      setHives(Array.isArray(res.data) ? res.data : []);
    } catch (error) {
      console.error("Error fetching hives:", error);
      setError("Failed to fetch hives.");
    }
  };

  // Fetch potential locations
  const fetchPotentialLocations = async () => {
    try {
      setLoading(true);
      const res = await axios.get(`${API_BASE}/potential-locations`);
      const locations = Array.isArray(res.data) ? res.data : [];
      setPotentialLocations(locations);
      processLocations(locations);
      setError(null);
    } catch (error) {
      console.error("Error fetching potential locations:", error);
      setError("Failed to fetch potential locations.");
    } finally {
      setLoading(false);
    }
  };

  // FIXED: Use Map + toFixed(6) to avoid floating-point mismatch
  const processLocations = (locations) => {
    if (locations.length === 0) {
      setRows(0);
      setCols(0);
      setPredictions({});
      setCellToLocation({});
      setMaxHoney(1);
      return;
    }

    const precision = 6;
    const round = (num) => Number(num.toFixed(precision));

    const latMap = new Map();
    const lngMap = new Map();
    const newPredictions = {};
    const newCellToLocation = {};

    locations.forEach((l) => {
      const lat = round(l.lat);
      const lng = round(l.lng);

      if (!latMap.has(lat)) latMap.set(lat, latMap.size);
      if (!lngMap.has(lng)) lngMap.set(lng, lngMap.size);

      const row = latMap.get(lat);
      const col = lngMap.get(lng);
      const cellId = `${row}-${col}`;

      // If duplicate lat/lng, take the one with honey_production if available, else last
      if (newCellToLocation[cellId] && newCellToLocation[cellId].honey_production !== null) {
        return; // Keep existing if has value
      }
      newPredictions[cellId] = l.honey_production;
      newCellToLocation[cellId] = l;
    });

    const sortedLats = Array.from(latMap.keys()).sort((a, b) => b - a);
    const sortedLngs = Array.from(lngMap.keys()).sort((a, b) => a - b);

    setPredictions(newPredictions);
    setCellToLocation(newCellToLocation);
    setRows(sortedLats.length);
    setCols(sortedLngs.length);

    const honeyValues = Object.values(newPredictions).filter(
      (v) => v !== null && v !== undefined && v > 0
    );
    setMaxHoney(honeyValues.length > 0 ? Math.max(...honeyValues) : 1);
  };

  // Generate grid
  const generateGrid = async () => {
    try {
      setLoading(true);
      await axios.get(`${API_BASE}/potential-locations/generate-grid`);
      console.log("Grid generated");
    } catch (error) {
      console.error("Error generating grid:", error);
      setError("Failed to generate grid.");
    } finally {
      setLoading(false);
    }
  };

  // Predict all
  const predictAll = async () => {
    try {
      setLoading(true);
      await axios.get(`${API_BASE}/ml/predict-all`);
      console.log("Predictions updated");
    } catch (error) {
      console.error("Error running predictions:", error);
      setError("Failed to run predictions.");
    } finally {
      setLoading(false);
    }
  };

  // Clear predictions
  const clearAllPredictions = async () => {
    if (!window.confirm("Clear all predicted honey values?")) return;
    try {
      setLoading(true);
      await axios.delete(`${API_BASE}/potential-locations/clear-predictions`);
      await fetchPotentialLocations();
    } catch (error) {
      console.error("Error clearing predictions:", error);
      setError("Failed to clear predictions.");
    } finally {
      setLoading(false);
    }
  };

  // Delete all locations
  const deleteAllLocations = async () => {
    if (!window.confirm("Delete ALL location data? This cannot be undone.")) return;
    try {
      setLoading(true);
      await axios.delete(`${API_BASE}/potential-locations`);
      await fetchPotentialLocations();
    } catch (error) {
      console.error("Error deleting locations:", error);
      setError("Failed to delete locations.");
    } finally {
      setLoading(false);
    }
  };

  // Load optimal
  const loadOptimalLocations = async () => {
    try {
      setLoading(true);
      await generateGrid();
      await predictAll();
      // Double fetch to ensure DB commit
      await fetchPotentialLocations();
      setTimeout(fetchPotentialLocations, 600);
    } catch (error) {
      console.error("Error loading optimal locations:", error);
      setError("Failed to load optimal locations.");
    } finally {
      setLoading(false);
    }
  };

  // Initial load
  useEffect(() => {
    fetchHives();
    fetchPotentialLocations();
  }, []);

  // Cell click
  const handleCellClick = (row, col) => {
    const cellId = `${row}-${col}`;
    if (cellToLocation[cellId]) {
      setSelectedCell(cellId);
    }
  };

  // FIXED: Safe color calculation
  const getCellColor = (cellId) => {
    const score = predictions[cellId];
    if (score === undefined || score === null || score <= 0) return "#ffffff";
    const normalized = maxHoney > 0 ? score / maxHoney : 0;
    if (normalized > 0.7) return "var(--green-color)";
    if (normalized > 0.4) return "var(--blue-color)";
    return "var(--red-color)";
  };

  // Toggle view
  const toggleViewMode = () => {
    setViewMode(viewMode === "grid" ? "map" : "grid");
  };

  // Memoized grid
  const grid = useMemo(() => {
    if (rows === 0 || cols === 0) {
      return <p style={{ padding: "2rem", textAlign: "center" }}>No location data available.</p>;
    }

    return Array.from({ length: rows }).map((_, row) => (
      <div key={row} className="grid-row">
        {Array.from({ length: cols }).map((_, col) => {
          const cellId = `${row}-${col}`;
          return (
            <div
              key={cellId}
              className="grid-cell"
              onClick={() => handleCellClick(row, col)}
              style={{ backgroundColor: getCellColor(cellId) }}
              title={cellToLocation[cellId] ? `Honey: ${cellToLocation[cellId].honey_production?.toFixed(2) || '—'}` : "No data"}
            />
          );
        })}
      </div>
    ));
  }, [rows, cols, predictions, cellToLocation, maxHoney]);

  return (
    <div className="hivemap-page">
      <Navbar />
      <div className="hive-map-container">
        <aside className="sidebar">
          <h2 className="sidebar-title">Hive Locations</h2>
          <div className="search-container">
            <input type="text" placeholder="Search hives..." className="search-input" />
          </div>

          {error && <p className="error-message">{error}</p>}
          {loading && <p style={{ color: "var(--primary-color)", fontWeight: 500 }}>Loading...</p>}

          <ul className="hive-list">
            {hives.length > 0 ? (
              hives.map((hive) => (
                <li key={hive.id} className="hive-list-item">
                  <h3>{hive.name}</h3>
                  <p>Lat: {hive.location_lat}, Lng: {hive.location_lng}</p>
                </li>
              ))
            ) : (
              <li className="hive-list-item">No hives found.</li>
            )}
          </ul>

          <div style={{ display: "flex", flexDirection: "column", gap: "0.5rem" }}>
            <button onClick={loadOptimalLocations} className="toggle-view-btn" disabled={loading}>
              {loading ? "Processing..." : "Load Optimal Locations"}
            </button>

            <button onClick={clearAllPredictions} className="toggle-view-btn delete-btn" disabled={loading}>
              {loading ? "Clearing..." : "Clear Predictions"}
            </button>

            <button onClick={deleteAllLocations} className="toggle-view-btn delete-btn" disabled={loading}>
              {loading ? "Deleting..." : "Delete All Locations"}
            </button>

            <button onClick={toggleViewMode} className="toggle-view-btn" disabled={loading}>
              Switch to {viewMode === "grid" ? "Map" : "Grid"} View
            </button>

            {/* DEBUG BUTTON */}
            <button
              onClick={() => {
                console.log("Raw Locations:", potentialLocations);
                console.log("Predictions Map:", predictions);
                console.log("Max Honey:", maxHoney);
              }}
              className="toggle-view-btn"
              style={{ background: "#666", fontSize: "0.8rem" }}
            >
              Debug Console
            </button>
          </div>
        </aside>

        <main className="map-section">
          <div
            className={`grid-container ${viewMode === "map" ? "map-view" : ""}`}
            style={viewMode === "map" ? { backgroundImage: `url(${mapImage})` } : {}}
          >
            {grid}
          </div>

          {/* Popup */}
          {selectedCell && cellToLocation[selectedCell] && (
            <div className="popup-overlay" onClick={() => setSelectedCell(null)}>
              <div className="popup-content" onClick={(e) => e.stopPropagation()}>
                <h3>Details for Cell {selectedCell}</h3>
                <div className="location-details">
                  <p><strong>Latitude:</strong> {cellToLocation[selectedCell].lat}</p>
                  <p><strong>Longitude:</strong> {cellToLocation[selectedCell].lng}</p>
                  <p><strong>Temperature:</strong> {cellToLocation[selectedCell].temperature} °C</p>
                  <p><strong>Humidity:</strong> {cellToLocation[selectedCell].humidity} %</p>
                  <p><strong>Sunlight Exposure:</strong> {cellToLocation[selectedCell].sunlight_exposure} hours/day</p>
                  <p><strong>Wind Speed:</strong> {cellToLocation[selectedCell].wind_speed} km/h</p>
                  <p><strong>Dist. to Water Source:</strong> {cellToLocation[selectedCell].dist_to_water_source.toFixed(3)} km</p>
                  <p><strong>Dist. to Flowering Area:</strong> {cellToLocation[selectedCell].dist_to_flowering_area.toFixed(3)} km</p>
                  <p><strong>Dist. to Feeding Station:</strong> {cellToLocation[selectedCell].dist_to_feeding_station.toFixed(3)} km</p>
                  <p>
                    <strong>Predicted Honey Production:</strong>{" "}
                    <span style={{ color: "var(--primary-color)", fontWeight: "bold" }}>
                      {cellToLocation[selectedCell].honey_production !== null && cellToLocation[selectedCell].honey_production > 0
                        ? cellToLocation[selectedCell].honey_production.toFixed(2)
                        : "Not predicted yet"}
                    </span>
                  </p>
                </div>
                <div className="form-buttons">
                  <button type="button" onClick={() => setSelectedCell(null)}>
                    Close
                  </button>
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