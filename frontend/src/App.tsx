// src/App.tsx (ensure all imports use .tsx for consistency)
import { Routes, Route } from 'react-router-dom';
import Home from './pages/Home.jsx';
import About from './pages/About.jsx';
import HiveManagement from './pages/HiveManagement.jsx';
import NewHivePlacement from './pages/HiveMap';
import ThreatDetection from "./pages/ThreatDetection.jsx";
import ThreatAlerts from "./pages/ThreatAlerts";
import Dashboard from './pages/Dashboard';

// Landing pages
import LandingHomepage from './pages/landing/Homepage';
import LandingAbout from './pages/landing/About';
import LandingPricing from './pages/landing/Pricing';
import LandingContact from './pages/landing/Contact';


function App() {
  return (
    <Routes>
      {/* Application Routes */}
      <Route path="/" element={<Home />} />
      <Route path="/about" element={<About />} />
      <Route path="/hive-management" element={<HiveManagement />} />
      <Route path="/NewHivePlacement" element={<NewHivePlacement />} />
      <Route path="/threat-detection" element={<ThreatDetection />} />
      <Route path="/alerts" element={<ThreatAlerts />} />
      <Route path="/dashboard" element={<Dashboard />} />
      
      {/* Landing Page Routes */}
      <Route path="/landing" element={<LandingHomepage />} />
      <Route path="/landing/about" element={<LandingAbout />} />
      <Route path="/landing/pricing" element={<LandingPricing />} />
      <Route path="/landing/contact" element={<LandingContact />} />
    </Routes>
  );
}

export default App;