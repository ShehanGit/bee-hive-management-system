// src/App.tsx (ensure all imports use .tsx for consistency)
import { Routes, Route } from 'react-router-dom';

import HiveManagement from './pages/HiveManagement.jsx';
import NewHivePlacement from './pages/HiveMap';
import ThreatDetection from "./pages/ThreatDetection.jsx";
import ThreatAlerts from "./pages/ThreatAlerts";
import Dashboard from './pages/Dashboard';
import HealthIdentification from './pages/HealthIdentification.js';

// Landing pages
import LandingHomepage from './pages/landing/Homepage';
import LandingAbout from './pages/landing/About';
import LandingPricing from './pages/landing/Pricing';
import LandingContact from './pages/landing/Contact';


function App() {
  return (
    <Routes>
     
      <Route path="/hive-management" element={<HiveManagement />} />
      <Route path="/NewHivePlacement" element={<NewHivePlacement />} />
      <Route path="/threat-detection" element={<ThreatDetection />} />
      <Route path="/alerts" element={<ThreatAlerts />} />
      <Route path="/dashboard" element={<Dashboard />} />
      
      {/* Landing Page Routes */}
      <Route path="/" element={<LandingHomepage />} />
      <Route path="/landing/about" element={<LandingAbout />} />
      <Route path="/landing/pricing" element={<LandingPricing />} />
      <Route path="/landing/contact" element={<LandingContact />} />
      <Route path="/health" element={<HealthIdentification />} />
    </Routes>
  );
}

export default App;