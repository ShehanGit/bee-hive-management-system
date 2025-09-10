import React, { useEffect, useState } from 'react';
import axios from 'axios';
import Navbar from '../components/Navbar';
import './HiveManagement.css';

function HiveManagement() {
  const [hives, setHives] = useState([]);
  const [formData, setFormData] = useState({ name: '', location_lat: '', location_lng: '' });
  const [editingHive, setEditingHive] = useState(null);

  useEffect(() => {
    fetchHives();
  }, []);

    // Fetch all hives from the backend using the correct endpoint.
    const fetchHives = async () => {
      try {
        const res = await axios.get('http://127.0.0.1:5000/api/hives');
        // Ensure we set an array, or default to an empty array.
        setHives(Array.isArray(res.data) ? res.data : []);
      } catch (error) {
        console.error('Error fetching hives:', error);
      }
    };

  // Handle form input changes
  const handleInputChange = (e) => {
    const { name, value } = e.target;
    setFormData({ ...formData, [name]: value });
  };

  // Create or update a hive based on current state
  const handleSubmit = async (e) => {
    e.preventDefault();
    if (editingHive) {
      // Update existing hive
      try {
        await axios.put(`http://127.0.0.1:5000/api/hives/${editingHive.id}`, formData);
        setEditingHive(null);
        setFormData({ name: '', location_lat: '', location_lng: '' });
        fetchHives();
      } catch (error) {
        console.error('Error updating hive:', error);
      }
    } else {
      // Create a new hive
      try {
        await axios.post('http://127.0.0.1:5000/api/hives', formData);
        setFormData({ name: '', location_lat: '', location_lng: '' });
        fetchHives();
      } catch (error) {
        console.error('Error creating hive:', error);
      }
    }
  };

  // Prepare form for editing a hive
  const handleEdit = (hive) => {
    setEditingHive(hive);
    setFormData({
      name: hive.name,
      location_lat: hive.location_lat,
      location_lng: hive.location_lng,
    });
  };

  // Delete a hive and refresh the list
  const handleDelete = async (hiveId) => {
    try {
      await axios.delete(`http://127.0.0.1:5000/api/hives/${hiveId}`);
      fetchHives();
    } catch (error) {
      console.error('Error deleting hive:', error);
    }
  };

  // Cancel editing mode
  const handleCancelEdit = () => {
    setEditingHive(null);
    setFormData({ name: '', location_lat: '', location_lng: '' });
  };

  return (
    <div className="hive-management">
      <Navbar />
      <main>
        <h1>Hive Management Dashboard</h1>
        
        <section className="hive-form">
          <h2>{editingHive ? 'Edit Hive' : 'Add New Hive'}</h2>
          <form onSubmit={handleSubmit}>
            <div>
              <label>Name:</label>
              <input 
                type="text" 
                name="name" 
                value={formData.name} 
                onChange={handleInputChange} 
                required 
              />
            </div>
            <div>
              <label>Location Latitude:</label>
              <input 
                type="number" 
                name="location_lat" 
                value={formData.location_lat} 
                onChange={handleInputChange} 
                required 
                step="any"
              />
            </div>
            <div>
              <label>Location Longitude:</label>
              <input 
                type="number" 
                name="location_lng" 
                value={formData.location_lng} 
                onChange={handleInputChange} 
                required 
                step="any"
              />
            </div>
            <div className="form-buttons">
              <button type="submit">
                {editingHive ? 'Update Hive' : 'Add Hive'}
              </button>
              {editingHive && (
                <button type="button" onClick={handleCancelEdit}>
                  Cancel
                </button>
              )}
            </div>
          </form>
        </section>

        <section className="hive-list">
          <h2>Existing Hives</h2>
          {Array.isArray(hives) && hives.length > 0 ? (
            <table>
              <thead>
                <tr>
                  <th>ID</th>
                  <th>Name</th>
                  <th>Latitude</th>
                  <th>Longitude</th>
                  <th>Created At</th>
                  <th>Actions</th>
                </tr>
              </thead>
              <tbody>
                {hives.map((hive) => (
                  <tr key={hive.id}>
                    <td>{hive.id}</td>
                    <td>{hive.name}</td>
                    <td>{hive.location_lat}</td>
                    <td>{hive.location_lng}</td>
                    <td>{new Date(hive.created_at).toLocaleString()}</td>
                    <td>
                      <button onClick={() => handleEdit(hive)}>Edit</button>
                      <button onClick={() => handleDelete(hive.id)}>Delete</button>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          ) : (
            <p>No hives available.</p>
          )}
        </section>
      </main>
    </div>
  );
}

export default HiveManagement;
