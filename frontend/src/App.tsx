// src/App.tsx (ensure all imports use .tsx for consistency)
import { Routes, Route } from 'react-router-dom';
import { useState, useEffect } from 'react';
import Navbar from './components/Navbar';
import Sidebar from './components/Sidebar';

import LandingPage from './pages/LandingPage';
import Home from './pages/Home.jsx';
import About from './pages/About.jsx';
import HiveManagement from './pages/HiveManagement.jsx';
import NewHivePlacement from './pages/HiveMap';
import ThreatDetection from "./pages/ThreatDetection.jsx";
import ThreatAlerts from "./pages/ThreatAlerts.jsx";
import HealthIdentification from './pages/HealthIdentification.tsx';
import Packages from './pages/Packages.tsx';

import './App.css';

function App() {
  const [sidebarCollapsed, setSidebarCollapsed] = useState(false);
  const [sidebarOpen, setSidebarOpen] = useState(false);

  // Handle sidebar toggle
  const handleSidebarToggle = () => {
    setSidebarCollapsed(!sidebarCollapsed);
  };

  // Handle mobile sidebar toggle
  const handleMobileSidebarToggle = () => {
    setSidebarOpen(!sidebarOpen);
  };

  // Close mobile sidebar when clicking outside
  useEffect(() => {
    const handleResize = () => {
      if (window.innerWidth > 1024) {
        setSidebarOpen(false);
      }
    };

    const handleClickOutside = (event: MouseEvent) => {
      if (window.innerWidth <= 1024 && sidebarOpen) {
        const sidebar = document.querySelector('.sidebar');
        const navbar = document.querySelector('.navbar');
        if (sidebar && !sidebar.contains(event.target as Node) && 
            navbar && !navbar.contains(event.target as Node)) {
          setSidebarOpen(false);
        }
      }
    };

    window.addEventListener('resize', handleResize);
    document.addEventListener('mousedown', handleClickOutside);

    return () => {
      window.removeEventListener('resize', handleResize);
      document.removeEventListener('mousedown', handleClickOutside);
    };
  }, [sidebarOpen]);

  return (
    <Routes>
      {/* Landing Page Routes */}
      <Route path="/" element={<LandingPage />} />
      <Route path="/about" element={<LandingPage />} />
      <Route path="/packages" element={<LandingPage />} />
      <Route path="/contact" element={<LandingPage />} />
      
      {/* Dashboard Routes - Direct access for existing links */}
      <Route path="/dashboard" element={
        <div className="app-container">
          <Sidebar 
            isCollapsed={sidebarCollapsed} 
            onToggle={handleSidebarToggle}
            isOpen={sidebarOpen}
          />
          <div className={`main-content ${sidebarCollapsed ? 'sidebar-collapsed' : ''} ${sidebarOpen ? 'sidebar-open' : ''}`}>
            <Home />
          </div>
        </div>
      } />
      
      {/* Individual Dashboard Routes */}
      <Route path="/hive-management" element={
        <div className="app-container">
          <Sidebar 
            isCollapsed={sidebarCollapsed} 
            onToggle={handleSidebarToggle}
            isOpen={sidebarOpen}
          />
          <div className={`main-content ${sidebarCollapsed ? 'sidebar-collapsed' : ''} ${sidebarOpen ? 'sidebar-open' : ''}`}>
            <HiveManagement />
          </div>
        </div>
      } />
      
      <Route path="/NewHivePlacement" element={
        <div className="app-container">
          <Sidebar 
            isCollapsed={sidebarCollapsed} 
            onToggle={handleSidebarToggle}
            isOpen={sidebarOpen}
          />
          <div className={`main-content ${sidebarCollapsed ? 'sidebar-collapsed' : ''} ${sidebarOpen ? 'sidebar-open' : ''}`}>
            <NewHivePlacement />
          </div>
        </div>
      } />
      
      <Route path="/health-identification" element={
        <div className="app-container">
          <Sidebar 
            isCollapsed={sidebarCollapsed} 
            onToggle={handleSidebarToggle}
            isOpen={sidebarOpen}
          />
          <div className={`main-content ${sidebarCollapsed ? 'sidebar-collapsed' : ''} ${sidebarOpen ? 'sidebar-open' : ''}`}>
            <HealthIdentification />
          </div>
        </div>
      } />
      
      <Route path="/threat-detection" element={
        <div className="app-container">
          <Sidebar 
            isCollapsed={sidebarCollapsed} 
            onToggle={handleSidebarToggle}
            isOpen={sidebarOpen}
          />
          <div className={`main-content ${sidebarCollapsed ? 'sidebar-collapsed' : ''} ${sidebarOpen ? 'sidebar-open' : ''}`}>
            <ThreatDetection />
          </div>
        </div>
      } />
      
      <Route path="/alerts" element={
        <div className="app-container">
          <Sidebar 
            isCollapsed={sidebarCollapsed} 
            onToggle={handleSidebarToggle}
            isOpen={sidebarOpen}
          />
          <div className={`main-content ${sidebarCollapsed ? 'sidebar-collapsed' : ''} ${sidebarOpen ? 'sidebar-open' : ''}`}>
            <ThreatAlerts />
          </div>
        </div>
      } />
    </Routes>
  );
}

export default App;