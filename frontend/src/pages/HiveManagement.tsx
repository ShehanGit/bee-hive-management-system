// import React, { useEffect, useState } from 'react';
// import axios from 'axios';
// import Navbar from '../components/Navbar';
// import './HiveManagement.css';

// function HiveManagement() {
//   const [hives, setHives] = useState([]);
//   const [formData, setFormData] = useState({ name: '', location_lat: '', location_lng: '' });
//   const [editingHive, setEditingHive] = useState(null);

//   useEffect(() => {
//     fetchHives();
//   }, []);

//     // Fetch all hives from the backend using the correct endpoint.
//     const fetchHives = async () => {
//       try {
//         const res = await axios.get('http://127.0.0.1:5000/api/hives');
//         // Ensure we set an array, or default to an empty array.
//         setHives(Array.isArray(res.data) ? res.data : []);
//       } catch (error) {
//         console.error('Error fetching hives:', error);
//       }
//     };

//   // Handle form input changes
//   const handleInputChange = (e) => {
//     const { name, value } = e.target;
//     setFormData({ ...formData, [name]: value });
//   };

//   // Create or update a hive based on current state
//   const handleSubmit = async (e) => {
//     e.preventDefault();
//     if (editingHive) {
//       // Update existing hive
//       try {
//         await axios.put(`http://127.0.0.1:5000/api/hives/${editingHive.id}`, formData);
//         setEditingHive(null);
//         setFormData({ name: '', location_lat: '', location_lng: '' });
//         fetchHives();
//       } catch (error) {
//         console.error('Error updating hive:', error);
//       }
//     } else {
//       // Create a new hive
//       try {
//         await axios.post('http://127.0.0.1:5000/api/hives', formData);
//         setFormData({ name: '', location_lat: '', location_lng: '' });
//         fetchHives();
//       } catch (error) {
//         console.error('Error creating hive:', error);
//       }
//     }
//   };

//   // Prepare form for editing a hive
//   const handleEdit = (hive) => {
//     setEditingHive(hive);
//     setFormData({
//       name: hive.name,
//       location_lat: hive.location_lat,
//       location_lng: hive.location_lng,
//     });
//   };

//   // Delete a hive and refresh the list
//   const handleDelete = async (hiveId) => {
//     try {
//       await axios.delete(`http://127.0.0.1:5000/api/hives/${hiveId}`);
//       fetchHives();
//     } catch (error) {
//       console.error('Error deleting hive:', error);
//     }
//   };

//   // Cancel editing mode
//   const handleCancelEdit = () => {
//     setEditingHive(null);
//     setFormData({ name: '', location_lat: '', location_lng: '' });
//   };

//   return (
//     <div className="hive-management">
//       <Navbar />
//       <main>
//         <h1>Hive Management Dashboard</h1>
        
//         <section className="hive-form">
//           <h2>{editingHive ? 'Edit Hive' : 'Add New Hive'}</h2>
//           <form onSubmit={handleSubmit}>
//             <div>
//               <label>Name:</label>
//               <input 
//                 type="text" 
//                 name="name" 
//                 value={formData.name} 
//                 onChange={handleInputChange} 
//                 required 
//               />
//             </div>
//             <div>
//               <label>Location Latitude:</label>
//               <input 
//                 type="number" 
//                 name="location_lat" 
//                 value={formData.location_lat} 
//                 onChange={handleInputChange} 
//                 required 
//                 step="any"
//               />
//             </div>
//             <div>
//               <label>Location Longitude:</label>
//               <input 
//                 type="number" 
//                 name="location_lng" 
//                 value={formData.location_lng} 
//                 onChange={handleInputChange} 
//                 required 
//                 step="any"
//               />
//             </div>
//             <div className="form-buttons">
//               <button type="submit">
//                 {editingHive ? 'Update Hive' : 'Add Hive'}
//               </button>
//               {editingHive && (
//                 <button type="button" onClick={handleCancelEdit}>
//                   Cancel
//                 </button>
//               )}
//             </div>
//           </form>
//         </section>

//         <section className="hive-list">
//           <h2>Existing Hives</h2>
//           {Array.isArray(hives) && hives.length > 0 ? (
//             <table>
//               <thead>
//                 <tr>
//                   <th>ID</th>
//                   <th>Name</th>
//                   <th>Latitude</th>
//                   <th>Longitude</th>
//                   <th>Created At</th>
//                   <th>Actions</th>
//                 </tr>
//               </thead>
//               <tbody>
//                 {hives.map((hive) => (
//                   <tr key={hive.id}>
//                     <td>{hive.id}</td>
//                     <td>{hive.name}</td>
//                     <td>{hive.location_lat}</td>
//                     <td>{hive.location_lng}</td>
//                     <td>{new Date(hive.created_at).toLocaleString()}</td>
//                     <td>
//                       <button onClick={() => handleEdit(hive)}>Edit</button>
//                       <button onClick={() => handleDelete(hive.id)}>Delete</button>
//                     </td>
//                   </tr>
//                 ))}
//               </tbody>
//             </table>
//           ) : (
//             <p>No hives available.</p>
//           )}
//         </section>
//       </main>
//     </div>
//   );
// }

// export default HiveManagement;


import React, { useEffect, useState } from 'react';
import axios from 'axios';
// import Navbar from '../components/Navbar';
import './HiveManagement.css';

// Import your default hive image here
import defaultHiveImage from '../assets/hiveImage.png';
// For now, using a placeholder - replace with your actual image import
// const defaultHiveImage = "/path/to/your/default-hive-image.png";

function HiveManagement() {
  const [hives, setHives] = useState([]);
  const [formData, setFormData] = useState({ name: '', location_lat: '', location_lng: '' });
  const [editingHive, setEditingHive] = useState(null);
  const [showForm, setShowForm] = useState(false);

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
        setShowForm(false);
        fetchHives();
      } catch (error) {
        console.error('Error updating hive:', error);
      }
    } else {
      // Create a new hive
      try {
        await axios.post('http://127.0.0.1:5000/api/hives', formData);
        setFormData({ name: '', location_lat: '', location_lng: '' });
        setShowForm(false);
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
    setShowForm(true);
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
    setShowForm(false);
  };

  return (
    <div className="hive-management">
      {/* <Navbar /> */}
      <main className="hive-main">
        <div className="header-section">
          <h1>Hive Management Dashboard</h1>
          <button className="add-hive-btn" onClick={() => setShowForm(true)}>
            <span className="btn-icon">+</span>
            Add New Hive
          </button>
        </div>
        
        <section className="hive-cards-container">
          {Array.isArray(hives) && hives.length > 0 ? (
            <div className="hive-cards">
              {hives.map((hive) => (
                <div key={hive.id} className="hive-card">
                  <div className="hive-card-left">
                    <div className="hive-image-container">
                      <img 
                        src={defaultHiveImage} 
                        alt="Hive" 
                        className="hive-image"
                        onError={(e) => {
                          // Fallback to a simple colored div if image fails to load
                          e.target.style.display = 'none';
                          e.target.nextSibling.style.display = 'flex';
                        }}
                      />
                      <div className="hive-image-fallback" style={{display: 'none', width: '200px', height: '200px', borderRadius: '12px', background: '#FFD700', alignItems: 'center', justifyContent: 'center', fontSize: '48px'}}>🍯</div>
                      <div className="hive-image-name">{hive.name}</div>
                    </div>
                    <div className="hive-info">
                      <span className="hive-id">ID: {hive.id}</span>
                    </div>
                  </div>
                  
                  <div className="hive-card-middle">
                    <div className="location-info">
                      <div className="location-item">
                        <span className="location-label">Latitude:</span>
                        <span className="location-value">{hive.location_lat}</span>
                      </div>
                      <div className="location-item">
                        <span className="location-label">Longitude:</span>
                        <span className="location-value">{hive.location_lng}</span>
                      </div>
                      <div className="created-date">
                        Created: {new Date(hive.created_at).toLocaleDateString()}
                      </div>
                    </div>
                  </div>
                  
                  <div className="hive-card-right">
                    <button className="edit-btn" onClick={() => handleEdit(hive)}>
                      Edit
                    </button>
                    <button className="delete-btn" onClick={() => handleDelete(hive.id)}>
                      Delete
                    </button>
                  </div>
                </div>
              ))}
            </div>
          ) : (
            <div className="no-hives">
              <p>No hives available. Click "Add New Hive" to get started!</p>
            </div>
          )}
        </section>

        {/* Popup Form */}
        {showForm && (
          <div className="popup-overlay" onClick={(e) => {
            if (e.target.className === 'popup-overlay') {
              handleCancelEdit();
            }
          }}>
            <div className="popup-form">
              <div className="popup-header">
                <h2>{editingHive ? 'Edit Hive' : 'Add New Hive'}</h2>
                <button className="close-btn" onClick={handleCancelEdit}>×</button>
              </div>
              
              <form onSubmit={handleSubmit} className="hive-form">
                <div className="form-group">
                  <label>Hive Name:</label>
                  <input 
                    type="text" 
                    name="name" 
                    value={formData.name} 
                    onChange={handleInputChange} 
                    required 
                    placeholder="Enter hive name"
                  />
                </div>
                
                <div className="form-row">
                  <div className="form-group">
                    <label>Latitude:</label>
                    <input 
                      type="number" 
                      name="location_lat" 
                      value={formData.location_lat} 
                      onChange={handleInputChange} 
                      required 
                      step="any"
                      placeholder="0.000000"
                    />
                  </div>
                  
                  <div className="form-group">
                    <label>Longitude:</label>
                    <input 
                      type="number" 
                      name="location_lng" 
                      value={formData.location_lng} 
                      onChange={handleInputChange} 
                      required 
                      step="any"
                      placeholder="0.000000"
                    />
                  </div>
                </div>
                
                <div className="form-buttons">
                  <button type="button" className="cancel-btn" onClick={handleCancelEdit}>
                    Cancel
                  </button>
                  <button type="submit" className="submit-btn">
                    {editingHive ? 'Update Hive' : 'Add Hive'}
                  </button>
                </div>
              </form>
            </div>
          </div>
        )}

        {/* Hide the old form and table sections */}
        <section className="hive-form" style={{display: 'none'}}>
          {/* Original form content - hidden */}
        </section>

        <section className="hive-list" style={{display: 'none'}}>
          {/* Original table content - hidden */}
        </section>
      </main>
    </div>
  );
}

export default HiveManagement;