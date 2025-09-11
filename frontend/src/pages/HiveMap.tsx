import React, { useState, useEffect } from "react";
import axios from "axios";
import Navbar from "../components/Navbar";
import mapImage from "../assets/images/map.png"; // Import the map image
import "./HiveMap.css";

function HiveMap() {
  const [hives, setHives] = useState([]);
  const [selectedCell, setSelectedCell] = useState(null);
  const [formData, setFormData] = useState({
    hive_lat: "",
    hive_lng: "",
    dist_to_water_source: "",
    dist_to_feeding_station: "",
    dist_to_flowering_area: "",
    humidity: "",
    temperature: "",
  });
  const [predictions, setPredictions] = useState({});
  const [viewMode, setViewMode] = useState("grid"); // Default to grid view

  const fetchHives = async () => {
    try {
      const res = await axios.get("http://127.0.0.1:5000/api/hives");
      setHives(Array.isArray(res.data) ? res.data : []);
    } catch (error) {
      console.error("Error fetching hives:", error);
    }
  };

  useEffect(() => {
    fetchHives();
  }, []);

  const handleCellClick = (row, col) => {
    setSelectedCell(`${row}-${col}`);
  };

  const handleInputChange = (e) => {
    const { name, value } = e.target;
    setFormData((prev) => ({ ...prev, [name]: value }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    const data = {
      hive_lat: [parseFloat(formData.hive_lat)],
      hive_lng: [parseFloat(formData.hive_lng)],
      dist_to_water_source: [parseFloat(formData.dist_to_water_source)],
      dist_to_feeding_station: [parseFloat(formData.dist_to_feeding_station)],
      dist_to_flowering_area: [parseFloat(formData.dist_to_flowering_area)],
      humidity: [parseFloat(formData.humidity)],
      temperature: [parseFloat(formData.temperature)],
    };

    try {
      const res = await axios.post("http://localhost:5002/predict", data, {
        headers: { "Content-Type": "application/json" },
      });
      const prediction = res.data.predictions[0];
      setPredictions((prev) => ({ ...prev, [selectedCell]: prediction }));
      setSelectedCell(null);
      setFormData({
        hive_lat: "",
        hive_lng: "",
        dist_to_water_source: "",
        dist_to_feeding_station: "",
        dist_to_flowering_area: "",
        humidity: "",
        temperature: "",
      });
    } catch (error) {
      console.error("Error getting prediction:", error);
    }
  };

  const getCellColor = (cellId) => {
    const score = predictions[cellId];
    if (score === undefined) return "#fff";
    if (score > 0.7) return "green";
    if (score > 0.4) return "blue";
    return "red";
  };

  const toggleViewMode = () => {
    setViewMode(viewMode === "grid" ? "map" : "grid");
  };

  const rows = 50; // Increased from 10 for more cells
  const cols = 50; // Increased from 10 for more cells

  return (
    <div className="hivemap-page">
      <Navbar />
      <div className="hive-map-container">
        <aside className="sidebar">
          <h2 className="sidebar-title">Hive Locations</h2>
          <div className="search-container">
            <input type="text" placeholder="Search hives..." className="search-input" />
          </div>
          <ul className="hive-list">
            {hives.map((hive) => (
              <li key={hive.id} className="hive-list-item">
                <h3>{hive.name}</h3>
                <p>Lat: {hive.location_lat}, Lng: {hive.location_lng}</p>
              </li>
            ))}
          </ul>
          <button onClick={toggleViewMode} className="toggle-view-btn">
            Switch to {viewMode === "grid" ? "Map" : "Grid"} View
          </button>
        </aside>
        <main className="map-section">
          <div
            className={`grid-container ${viewMode === "map" ? "map-view" : ""}`}
            style={viewMode === "map" ? { backgroundImage: `url(${mapImage})` } : {}}
          >
            {Array.from({ length: rows }).map((_, row) => (
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
            ))}
          </div>
          {selectedCell && (
            <div className="popup-overlay">
              <div className="popup-content">
                <h3>Enter Details for Cell {selectedCell}</h3>
                <form onSubmit={handleSubmit} className="prediction-form">
                  <input
                    type="number"
                    name="hive_lat"
                    placeholder="Hive Latitude"
                    value={formData.hive_lat}
                    onChange={handleInputChange}
                    step="any"
                    required
                  />
                  <input
                    type="number"
                    name="hive_lng"
                    placeholder="Hive Longitude"
                    value={formData.hive_lng}
                    onChange={handleInputChange}
                    step="any"
                    required
                  />
                  <input
                    type="number"
                    name="dist_to_water_source"
                    placeholder="Dist. to Water (km)"
                    value={formData.dist_to_water_source}
                    onChange={handleInputChange}
                    step="any"
                    required
                  />
                  <input
                    type="number"
                    name="dist_to_feeding_station"
                    placeholder="Dist. to Feeding (km)"
                    value={formData.dist_to_feeding_station}
                    onChange={handleInputChange}
                    step="any"
                    required
                  />
                  <input
                    type="number"
                    name="dist_to_flowering_area"
                    placeholder="Dist. to Flowers (km)"
                    value={formData.dist_to_flowering_area}
                    onChange={handleInputChange}
                    step="any"
                    required
                  />
                  <input
                    type="number"
                    name="humidity"
                    placeholder="Humidity (%)"
                    value={formData.humidity}
                    onChange={handleInputChange}
                    step="any"
                    required
                  />
                  <input
                    type="number"
                    name="temperature"
                    placeholder="Temperature (°C)"
                    value={formData.temperature}
                    onChange={handleInputChange}
                    step="any"
                    required
                  />
                  <div className="form-buttons">
                    <button type="submit">Submit</button>
                    <button type="button" onClick={() => setSelectedCell(null)}>
                      Cancel
                    </button>
                  </div>
                </form>
              </div>
            </div>
          )}
        </main>
      </div>
    </div>
  );
}

export default HiveMap;