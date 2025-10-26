import React from 'react';
import ModernHiveDashboard from '../components/ModernHiveDashboard';
import ModernSidebar from '../components/ModernSidebar';
import Navbar from '../components/Navbar';
import './Dashboard.css';

const Dashboard: React.FC = () => {
  return (
    <div className="dashboard-page">
      <ModernSidebar />
      <div className="dashboard-content">
        <Navbar />
        <ModernHiveDashboard />
      </div>
    </div>
  );
};

export default Dashboard;
