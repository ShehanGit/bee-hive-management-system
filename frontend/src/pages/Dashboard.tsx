import React from 'react';
import ModernHiveDashboard from '../components/ModernHiveDashboard';
import Navbar from '../components/Navbar';
import './Dashboard.css';

const Dashboard: React.FC = () => {
  return (
    <div className="dashboard-page">
      <div className="dashboard-content">
        <Navbar />
        <ModernHiveDashboard />
      </div>
    </div>
  );
};

export default Dashboard;
