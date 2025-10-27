import React, { useEffect, useState } from 'react';
import axios from 'axios';
import Navbar from '../components/Navbar';
import { FiPlus, FiEdit3, FiTrash2, FiX, FiMapPin, FiLayers } from 'react-icons/fi';
import './HiveManagement.css';

function HiveManagement() {
  const [hives, setHives] = useState([]);
  const [formData, setFormData] = useState({ name: '', location_lat: '', location_lng: '' });
  const [editingHive, setEditingHive] = useState(null);
  const [showModal, setShowModal] = useState(false);

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

  useEffect(() => {
    fetchHives();
  }, []);

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
        setShowModal(false);
        fetchHives();
      } catch (error) {
        console.error('Error updating hive:', error);
      }
    } else {
      // Create a new hive
      try {
        await axios.post('http://127.0.0.1:5000/api/hives', formData);
        setFormData({ name: '', location_lat: '', location_lng: '' });
        setShowModal(false);
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
    setShowModal(true);
  };

  // Open modal for new hive
  const handleAddNew = () => {
    setEditingHive(null);
    setFormData({ name: '', location_lat: '', location_lng: '' });
    setShowModal(true);
  };

  // Close modal
  const handleCloseModal = () => {
    setShowModal(false);
    setEditingHive(null);
    setFormData({ name: '', location_lat: '', location_lng: '' });
  };

  // Delete a hive and refresh the list
  const handleDelete = async (hiveId) => {
    if (window.confirm('Are you sure you want to delete this hive?')) {
      try {
        await axios.delete(`http://127.0.0.1:5000/api/hives/${hiveId}`);
        fetchHives();
      } catch (error) {
        console.error('Error deleting hive:', error);
      }
    }
  };

  return (
    <div className="hive-management">
      <Navbar />
      <main className="hive-management-main">
        <div className="page-header">
          <div className="header-content">
            <FiLayers className="header-icon" />
            <h1>Hive Management</h1>
          </div>
          <button className="add-button" onClick={handleAddNew}>
            <FiPlus className="button-icon" />
            Add New Hive
          </button>
        </div>

        <section className="hive-list">
          <h2 className="section-title">
            <FiMapPin className="section-icon" />
            Existing Hives
          </h2>
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
                      <button className="action-button edit-button" onClick={() => handleEdit(hive)}>
                        <FiEdit3 />
                      </button>
                      <button className="action-button delete-button" onClick={() => handleDelete(hive.id)}>
                        <FiTrash2 />
                      </button>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          ) : (
            <div className="empty-state">
              <FiLayers className="empty-icon" />
              <p>No hives available. Create your first hive!</p>
            </div>
          )}
        </section>
      </main>

      {/* Modal for Add/Edit Hive */}
      {showModal && (
        <div className="modal-overlay" onClick={handleCloseModal}>
          <div className="modal-content" onClick={(e) => e.stopPropagation()}>
            <div className="modal-header">
              <h2>{editingHive ? 'Edit Hive' : 'Add New Hive'}</h2>
              <button className="close-button" onClick={handleCloseModal}>
                <FiX />
              </button>
            </div>
            
            <form className="modal-form" onSubmit={handleSubmit}>
              <div className="form-group">
                <label htmlFor="name">
                  <FiLayers className="label-icon" />
                  Hive Name
                </label>
                <input 
                  id="name"
                  type="text" 
                  name="name" 
                  value={formData.name} 
                  onChange={handleInputChange} 
                  placeholder="Enter hive name"
                  required 
                />
              </div>
              
              <div className="form-group">
                <label htmlFor="location_lat">
                  <FiMapPin className="label-icon" />
                  Latitude
                </label>
                <input 
                  id="location_lat"
                  type="number" 
                  name="location_lat" 
                  value={formData.location_lat} 
                  onChange={handleInputChange} 
                  placeholder="e.g., 6.9271"
                  required 
                  step="any"
                />
              </div>
              
              <div className="form-group">
                <label htmlFor="location_lng">
                  <FiMapPin className="label-icon" />
                  Longitude
                </label>
                <input 
                  id="location_lng"
                  type="number" 
                  name="location_lng" 
                  value={formData.location_lng} 
                  onChange={handleInputChange} 
                  placeholder="e.g., 79.8612"
                  required 
                  step="any"
                />
              </div>
              
              <div className="modal-actions">
                <button type="button" className="cancel-button" onClick={handleCloseModal}>
                  Cancel
                </button>
                <button type="submit" className="submit-button">
                  {editingHive ? 'Update Hive' : 'Create Hive'}
                </button>
              </div>
            </form>
          </div>
        </div>
      )}
    </div>
  );
}

export default HiveManagement;
