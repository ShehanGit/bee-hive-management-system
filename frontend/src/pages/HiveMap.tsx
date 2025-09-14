// frontend/src/HiveMap.js (updated for multiple views and resource colors)

import React, { useState, useEffect, useMemo } from "react";
import axios from "axios";
import Navbar from "../components/Navbar";
import mapImage from "../assets/images/map.png"; // Restore image map
import { MapContainer, TileLayer, Marker, Popup, Circle } from 'react-leaflet';
import 'leaflet/dist/leaflet.css';
import "./HiveMap.css";

function HiveMap() {
  const [hives, setHives] = useState([]);
  const [potentialLocations, setPotentialLocations] = useState([]);
  const [resources, setResources] = useState([]);
  const [selectedCell, setSelectedCell] = useState(null);
  const [predictions, setPredictions] = useState({});
  const [cellToLocation, setCellToLocation] = useState({});
  const [maxHoney, setMaxHoney] = useState(1);
  const [rows, setRows] = useState(0);
  const [cols, setCols] = useState(0);
  const [viewMode, setViewMode] = useState("grid"); // grid, image-map, real-map
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [resourceType, setResourceType] = useState('');

  const API_BASE = "http://127.0.0.1:5000/api";
  const CENTER = [6.9271, 79.8612];
  const ZOOM = 13;

  const fetchHives = async () => {
    try {
      const res = await axios.get(`${API_BASE}/hives`);
      setHives(Array.isArray(res.data) ? res.data : []);
    } catch (error) {
      console.error("Error fetching hives:", error);
      setError("Failed to fetch hives.");
    }
  };

  const fetchResources = async () => {
    try {
      const res = await axios.get(`${API_BASE}/resources`);
      setResources(Array.isArray(res.data) ? res.data : []);
    } catch (error) {
      console.error("Error fetching resources:", error);
      setError("Failed to fetch resources.");
    }
  };

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

  const processLocations = (locations) => {
    if (locations.length === 0) {
      setRows(0);
      setCols(0);
      return;
    }

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

    const honeyValues = Object.values(newPredictions).filter(
      (v) => v !== null && v !== undefined
    );
    setMaxHoney(honeyValues.length > 0 ? Math.max(...honeyValues) : 1);
  };

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

  const recalculateDistances = async () => {
    try {
      setLoading(true);
      await axios.get(`${API_BASE}/potential-locations/recalculate-distances`);
      console.log("Distances recalculated successfully");
      setError(null);
    } catch (error) {
      console.error("Error recalculating distances:", error);
      setError("Failed to recalculate distances.");
    } finally {
      setLoading(false);
    }
  };

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

  const loadOptimalLocations = async () => {
    try {
      setLoading(true);
      await generateGrid();
      await recalculateDistances();
      await predictAll();
      await fetchPotentialLocations();
    } catch (error) {
      console.error("Error loading optimal locations:", error);
      setError("Failed to load optimal locations.");
    } finally {
      setLoading(false);
    }
  };

  const addResource = async (lat, lng, type) => {
    try {
      await axios.post(`${API_BASE}/resources`, { lat, lng, type });
      console.log("Resource added successfully");
      await fetchResources();
      await recalculateDistances();
      await predictAll();
      await fetchPotentialLocations();
      setError(null);
    } catch (error) {
      console.error("Error adding resource:", error);
      setError("Failed to add resource.");
    }
  };

  useEffect(() => {
    fetchHives();
    fetchResources();
    fetchPotentialLocations();
  }, []);

  const handleCellClick = (row, col) => {
    const cellId = `${row}-${col}`;
    if (cellToLocation[cellId]) {
      setSelectedCell(cellId);
      setResourceType('');
    }
  };

  const handleAddResource = () => {
    if (resourceType && selectedCell) {
      const loc = cellToLocation[selectedCell];
      addResource(loc.lat, loc.lng, resourceType);
      setSelectedCell(null);
    }
  };

  const getCellColor = (cellId) => {
    const score = predictions[cellId];
    if (score === undefined || score === null) return "#fff";
    const normalized = score / maxHoney;
    if (normalized > 0.7) return "green";
    if (normalized > 0.4) return "blue";
    return "red";
  };

  const switchViewMode = (mode) => {
    setViewMode(mode);
  };

  // Memoize grid for grid/image-map view
  const grid = useMemo(() => {
    if (rows === 0 || cols === 0) {
      return <p>No location data available.</p>;
    }
    return Array.from({ length: rows }).map((_, row) => (
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
    ));
  }, [rows, cols, predictions, cellToLocation, maxHoney]);

  // Image map view with fixed background
  const imageMapView = (
    <div 
      className="grid-container" 
      style={{ 
        backgroundImage: `url(${mapImage})`,
        backgroundSize: 'cover',
        backgroundPosition: 'center',
        backgroundRepeat: 'no-repeat',
        position: 'relative'
      }}
    >
      <div style={{ position: 'absolute', top: 0, left: 0, width: '100%', height: '100%', opacity: 0.5 }}>  {/* Reduced opacity */}
        {grid}
      </div>
    </div>
  );

  // Real map view with Leaflet
  const realMapView = (
    <MapContainer center={CENTER} zoom={ZOOM} style={{ height: "100%", width: "100%" }}>
      <TileLayer
        url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
        attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
      />
      {potentialLocations.map((loc) => {
        const normalized = (loc.honey_production || 0) / maxHoney;
        let color = 'red';
        if (normalized > 0.7) color = 'green';
        else if (normalized > 0.4) color = 'blue';
        return (
          <Circle
            key={loc.id}
            center={[loc.lat, loc.lng]}
            radius={250}
            pathOptions={{ color: color, fillColor: color, fillOpacity: 0.5 }}
          >
            <Popup>
              <h3>Potential Location</h3>
              <p>Lat: {loc.lat}, Lng: {loc.lng}</p>
              <p>Honey Production: {loc.honey_production?.toFixed(2) || 'N/A'}</p>
            </Popup>
          </Circle>
        );
      })}
      {hives.map((hive) => (
        <Marker key={hive.id} position={[hive.location_lat, hive.location_lng]}>
          <Popup>
            <h3>Hive: {hive.name}</h3>
            <p>Lat: {hive.location_lat}, Lng: {hive.location_lng}</p>
          </Popup>
        </Marker>
      ))}
      {resources.map((res) => (
        <Circle
          key={res.id}
          center={[res.lat, res.lng]}
          radius={100}
          pathOptions={{ color: 'purple', fillColor: 'purple', fillOpacity: 0.7 }}
        >
          <Popup>
            <h3>Resource: {res.type}</h3>
            <p>Lat: {res.lat}, Lng: {res.lng}</p>
          </Popup>
        </Circle>
      ))}
    </MapContainer>
  );

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
          <h3>Resources</h3>
          <ul className="hive-list">
            {resources.map((res) => (
              <li key={res.id} className="hive-list-item">
                <h3>{res.type}</h3>
                <p>Lat: {res.lat}, Lng: {res.lng}</p>
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
            onClick={() => switchViewMode("grid")}
            className="toggle-view-btn"
            disabled={loading}
          >
            Grid View
          </button>
          <button
            onClick={() => switchViewMode("image-map")}
            className="toggle-view-btn"
            disabled={loading}
          >
            Image Map View
          </button>
          <button
            onClick={() => switchViewMode("real-map")}
            className="toggle-view-btn"
            disabled={loading}
          >
            Real Map View
          </button>
        </aside>
        <main className="map-section">
          <div className="grid-container">
            {viewMode === "grid" ? grid : viewMode === "image-map" ? imageMapView : realMapView}
          </div>
          {selectedCell && (viewMode === "grid" || viewMode === "image-map") && (
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
                {/* Add Resource Form */}
                <div className="add-resource-form">
                  <h4>Add Resource</h4>
                  <select
                    value={resourceType}
                    onChange={(e) => setResourceType(e.target.value)}
                  >
                    <option value="">Select Type</option>
                    <option value="water">Water Source</option>
                    <option value="flowering">Flowering Area</option>
                    <option value="feeding">Feeding Station</option>
                  </select>
                  <button onClick={handleAddResource} disabled={!resourceType}>
                    Add
                  </button>
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