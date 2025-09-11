// src/pages/Notifications.tsx
// Kept as list, but enhanced for more attention: Added auto-refresh, sorting by timestamp (newest first), per-item dismiss (simulates marking as read by removing locally), and bold for urgent threats.

import React, { useEffect, useState } from 'react';
import axios from 'axios';
import Navbar from '../components/Navbar';
import { FaBell, FaExclamationTriangle, FaTimesCircle, FaTrashAlt, FaTimes } from 'react-icons/fa'; // Added FaTimes for dismiss
import './Notifications.css';

interface Notification {
  id: number;
  hive_id: number;
  threat_type: 'wax_moth' | 'hornets' | 'mammals' | string;
  message: string;
  timestamp: string;
}

function Notifications() {
  const [notifications, setNotifications] = useState<Notification[]>([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const fetchNotifications = async () => {
    setLoading(true);
    setError(null);
    try {
      const res = await axios.get('http://127.0.0.1:5001/api/notifications');
      let data = Array.isArray(res.data) ? res.data : [];
      // Sort by timestamp descending (newest first)
      data.sort((a, b) => new Date(b.timestamp).getTime() - new Date(a.timestamp).getTime());
      setNotifications(data);
    } catch (err) {
      setError('Error fetching notifications. Please try again.');
      console.error('Error fetching notifications:', err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchNotifications();
    // Auto-refresh every 30 seconds for more attention
    const interval = setInterval(fetchNotifications, 30000);
    return () => clearInterval(interval);
  }, []);

  const handleClearNotifications = async () => {
    try {
      await axios.post('http://127.0.0.1:5001/api/notifications/clear');
      setNotifications([]);
    } catch (err) {
      console.error('Error clearing notifications:', err);
    }
  };

  const handleDismiss = (id: number) => {
    // Simulate dismiss by removing locally (could POST to backend if implemented)
    setNotifications((prev) => prev.filter((notif) => notif.id !== id));
  };

  // Function to get color and icon based on threat type, with urgency bold
  const getThreatStyle = (threat: string) => {
    let isUrgent = ['hornets', 'mammals'].includes(threat.toLowerCase()); // Example: hornets and mammals are urgent
    switch (threat.toLowerCase()) {
      case 'wax_moth':
        return { color: '#FF9800', icon: <FaExclamationTriangle />, urgent: isUrgent };
      case 'hornets':
        return { color: '#F44336', icon: <FaTimesCircle />, urgent: isUrgent };
      case 'mammals':
        return { color: '#2196F3', icon: <FaBell />, urgent: isUrgent };
      default:
        return { color: '#9E9E9E', icon: <FaBell />, urgent: false };
    }
  };

  return (
    <div className="notifications-page">
      <Navbar />
      <main className="notifications-main">
        <section className="notifications-header">
          <div className="header-content">
            <FaBell className="header-icon" />
            <h1>Hive Risk Notifications</h1>
            <p>Monitor threats like wax moths, hornets, and mammals in real-time. Auto-updates every 30 seconds.</p>
          </div>
          <button onClick={fetchNotifications} disabled={loading} className="check-button">
            {loading ? 'Checking...' : 'Refresh Now'}
          </button>
        </section>

        {error && <p className="error-message">{error}</p>}

        <section className="notifications-list">
          <h2>Current Notifications ({notifications.length})</h2>
          {notifications.length > 0 ? (
            <ul className="notification-list">
              {notifications.map((notif) => {
                const { color, icon, urgent } = getThreatStyle(notif.threat_type);
                return (
                  <li key={notif.id} className={`notification-item ${urgent ? 'urgent' : ''}`} style={{ borderLeft: `5px solid ${color}` }}>
                    <div className="item-icon" style={{ color }}>
                      {icon}
                    </div>
                    <div className="item-content">
                      <h3>{notif.threat_type.toUpperCase()} Threat</h3>
                      <p className="message">{notif.message}</p>
                      <p className="details">
                        Hive ID: {notif.hive_id} | {new Date(notif.timestamp).toLocaleString()}
                      </p>
                    </div>
                    <button className="dismiss-button" onClick={() => handleDismiss(notif.id)}>
                      <FaTimes /> Dismiss
                    </button>
                  </li>
                );
              })}
            </ul>
          ) : (
            <p className="no-notifications">No notifications available. Your hives are safe!</p>
          )}
          {notifications.length > 0 && (
            <button onClick={handleClearNotifications} className="clear-button">
              <FaTrashAlt /> Clear All
            </button>
          )}
        </section>
      </main>
    </div>
  );
}

export default Notifications;