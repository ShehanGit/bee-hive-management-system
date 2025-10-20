import React from 'react';
import CleanHiveDashboard from '../components/CleanHiveDashboard';
import Navbar from '../components/Navbar';
import './Dashboard.css';

const Dashboard: React.FC = () => {
  return (
    <div className="dashboard-page">
      <Navbar />
      <CleanHiveDashboard />
    </div>
  );
};

export default Dashboard;
