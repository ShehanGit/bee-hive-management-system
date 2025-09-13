import React from 'react';
import Navbar from '../components/Navbar'; // Add this import
import CleanHiveDashboard from '../components/CleanHiveDashboard';
import './MonitoringDashboard.css';

const MonitoringDashboard = () => {
    return (
        <>
            <Navbar /> {/* Add Navbar here */}
            <CleanHiveDashboard />
        </>
    );
};

export default MonitoringDashboard;
