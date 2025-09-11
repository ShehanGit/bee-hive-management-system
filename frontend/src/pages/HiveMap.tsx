import React, { useState, useEffect } from "react";
import axios from "axios";
import Navbar from "../components/Navbar";
import mapImage from "../assets/images/map.png"; // Ensure this image exists
import "./HiveMap.css";

function HiveMap() {
  const [hives, setHives] = useState([]);
  const [potentialLocations, setPotentialLocations] = useState([]);
  const [selectedCell, setSelectedCell] = useState(null);
  const [predictions, setPredictions] = useState({});
  const [cellToLocation, setCellToLocation] = useState({});
  const [maxHoney, setMaxHoney] = useState(1); // Default to avoid division by zero
  const [rows, setRows] = useState(5); // Dynamic based on data
  const [cols, setCols] = useState(5);
  const [viewMode, setViewMode] = useState("grid"); // grid or map
  const [loading, setLoading] = useState(false); // Loading state
  const [error, setError] = useState(null); // Error state

  const API_BASE = "http://127.0.0.1:5000/api"; // Matches backend prefix

  // Fetch hives
  const fetchHives = async () => {
    try {
      const res = await axios.get(`${API_BASE}/hives`);
      setHives(Array.isArray(res.data) ? res.data : []);
    } catch (error) {
      console.error("Error fetching hives:", error);
      setError("Failed to fetch hives. Please try again.");
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

  // Process locations to create grid and predictions
  const processLocations = (locations) => {
    if (locations.length === 0) {
      setRows(0);
      setCols(0);
      return;
    }

    // Get unique sorted lats (descending for row 0 = highest lat) and lngs (ascending)
    const uniqueLats = [...new Set(locations.map((l) => l.lat))].sort((a, b) => b - a);
    const uniqueLngs = [...new Set(locations.map((l) => l.lng))].sort((a, b) => a - b);

    const newPredictions = {};
    const newCellToLocation = {};
    locations.forEach((l) => {
      const row = uniqueLats.indexOf(l.lat);
      const col = uniqueLngs.indexOf(l.lng);
      const cellId = `${row}-${col}`;
      newPredictions[cellId] = l.honey_production;
      newCellToLocation[cellId] = l;
    });

    setPredictions(newPredictions);
    setCellToLocation(newCellToLocation);
    setRows(uniqueLats.length);
    setCols(uniqueLngs.length);

    // Calculate max honey_production for normalization
    const honeyValues = Object.values(newPredictions).filter(
      (v) => v !== null && v !== undefined
    );
    if (honeyValues.length > 0) {
      setMaxHoney(Math.max(...honeyValues));
    } else {
      setMaxHoney(1); // Fallback
    }
  };

  // Generate grid
  const generateGrid = async () => {
    try {
      setLoading(true);
      await axios.get(`${API_BASE}/potential-locations/generate-grid`);
      console.log("Grid generated successfully");
      setError(null);
    } catch (error) {
      console.error("Error generating grid:", error);
      setError("Failed to generate grid.");
    } finally {
      setLoading(false);
    }
  };

  // Run predictions
  const predictAll = async () => {
    try {
      setLoading(true);
      await axios.get(`${API_BASE}/ml/predict-all`);
      console.log("Predictions updated successfully");
      setError(null);
    } catch (error) {
      console.error("Error running predictions:", error);
      setError("Failed to run predictions.");
    } finally {
      setLoading(false);
    }
  };

  // Load optimal locations (generate grid, predict, fetch)
  const loadOptimalLocations = async () => {
    try {
      setLoading(true);
      await generateGrid();
      await predictAll();
      await fetchPotentialLocations();
    } catch (error) {
      console.error("Error loading optimal locations:", error);
      setError("Failed to load optimal locations.");
    } finally {
      setLoading(false);
    }
  };

  // Initial data fetch
  useEffect(() => {
    fetchHives();
    fetchPotentialLocations();
  }, []);

  // Handle cell click
  const handleCellClick = (row, col) => {
    const cellId = `${row}-${col}`;
    if (cellToLocation[cellId]) {
      setSelectedCell(cellId);
    }
  };

  // Determine cell color based on honey production
  const getCellColor = (cellId) => {
    const score = predictions[cellId];
    if (score === undefined || score === null) return "#fff"; // No prediction
    const normalized = score / maxHoney;
    if (normalized > 0.7) return "var(--green-color)";
    if (normalized > 0.4) return "var(--blue-color)";
    return "var(--red-color)";
  };

  // Toggle between grid and map view
  const toggleViewMode = () => {
    setViewMode(viewMode === "grid" ? "map" : "grid");
  };

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
          {loading && <p>Loading...</p>}
          <ul className="hive-list">
            {hives.map((hive) => (
              <li key={hive.id} className="hive-list-item">
                <h3>{hive.name}</h3>
                <p>Lat: {hive.location_lat}, Lng: {hive.location_lng}</p>
              </li>
            ))}
          </ul>
          <button
            onClick={loadOptimalLocations}
            className="toggle-view-btn"
            disabled={loading}
          >
            {loading ? "Loading..." : "Load Optimal Locations"}
          </button>
          <button
            onClick={toggleViewMode}
            className="toggle-view-btn"
            disabled={loading}
          >
            Switch to {viewMode === "grid" ? "Map" : "Grid"} View
          </button>
        </aside>
        <main className="map-section">
          <div
            className={`grid-container ${viewMode === "map" ? "map-view" : ""}`}
            style={viewMode === "map" ? { backgroundImage: `url(${mapImage})` } : {}}
          >
            {rows > 0 && cols > 0 ? (
              Array.from({ length: rows }).map((_, row) => (
                <div key={row} className="grid-row">
                  {Array.from({ length: cols }).map((_, col) => (
                    <div
                      key={`${row}-${col}`}
                      className="grid-cell"
                      onClick={() => handleCellClick(row, col)}
                      style={{ backgroundColor: getCellColor(`${row}-${col}`) }}
                    ></div>
                  ))}
                </div>
              ))
            ) : (
              <p>No location data available.</p>
            )}
          </div>
          {selectedCell && (
            <div className="popup-overlay">
              <div className="popup-content">
                <h3>Details for Cell {selectedCell}</h3>
                {cellToLocation[selectedCell] ? (
                  <div className="location-details">
                    <p><strong>Latitude:</strong> {cellToLocation[selectedCell].lat}</p>
                    <p><strong>Longitude:</strong> {cellToLocation[selectedCell].lng}</p>
                    <p><strong>Temperature:</strong> {cellToLocation[selectedCell].temperature} °C</p>
                    <p><strong>Humidity:</strong> {cellToLocation[selectedCell].humidity} %</p>
                    <p><strong>Sunlight Exposure:</strong> {cellToLocation[selectedCell].sunlight_exposure} hours/day</p>
                    <p><strong>Wind Speed:</strong> {cellToLocation[selectedCell].wind_speed} km/h</p>
                    <p><strong>Dist. to Water Source:</strong> {cellToLocation[selectedCell].dist_to_water_source} km</p>
                    <p><strong>Dist. to Flowering Area:</strong> {cellToLocation[selectedCell].dist_to_flowering_area} km</p>
                    <p><strong>Dist. to Feeding Station:</strong> {cellToLocation[selectedCell].dist_to_feeding_station} km</p>
                    <p>
                      <strong>Predicted Honey Production:</strong>{" "}
                      {cellToLocation[selectedCell].honey_production !== null
                        ? cellToLocation[selectedCell].honey_production.toFixed(2)
                        : "Not predicted yet"}
                    </p>
                  </div>
                ) : (
                  <p>No data available for this cell.</p>
                )}
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