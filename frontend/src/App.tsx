// src/App.tsx (ensure all imports use .tsx for consistency)
import { Routes, Route } from 'react-router-dom';
import Home from './pages/Home.jsx';
import About from './pages/About.jsx';
import HiveManagement from './pages/HiveManagement.jsx';
import NewHivePlacement from './pages/HiveMap';
import ThreatDetection from "./pages/ThreatDetection.jsx";
import ThreatAlerts from "./pages/ThreatAlerts";
import Dashboard from './pages/Dashboard';
import HealthIdentification from './pages/HealthIdentification.js';


function App() {
  return (
    <Routes>
      <Route path="/" element={<Home />} />
      <Route path="/about" element={<About />} />
      <Route path="/hive-management" element={<HiveManagement />} />
      <Route path="/NewHivePlacement" element={<NewHivePlacement />} />
      <Route path="/threat-detection" element={<ThreatDetection />} />
      <Route path="/alerts" element={<ThreatAlerts />} />
      <Route path="/dashboard" element={<Dashboard />} />
      <Route path="/health" element={<HealthIdentification />} />
    </Routes>
  );
}

export default App;