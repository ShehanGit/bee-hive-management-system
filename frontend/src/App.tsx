// src/App.tsx (ensure all imports use .tsx for consistency)
import { Routes, Route } from 'react-router-dom';


import Home from './pages/Home.jsx';
import About from './pages/About.jsx';
import HiveManagement from './pages/HiveManagement.jsx';
import NewHivePlacement from './pages/HiveMap';
// @ts-ignore
import ThreatDetection from "./pages/ThreatDetection.jsx";
// @ts-ignore
import ThreatAlerts from "./pages/ThreatAlerts.jsx";
import HealthIdentification from './pages/HealthIdentification.tsx';
import Packages from './pages/Packages.tsx';
import RegisterHive from './pages/RegisterHive.tsx';



function App() {
  return (
    <Routes>
      <Route path="/" element={<Home />} />
      <Route path="/about" element={<About />} />
      <Route path="/packages" element={<Packages />} />
      <Route path="/register-hive" element={<RegisterHive />} />
      <Route path="/hive-management" element={<HiveManagement />} />
      <Route path="/NewHivePlacement" element={<NewHivePlacement />} />

      <Route path="/health-identification" element={<HealthIdentification />} />

      <Route path="/threat-detection" element={<ThreatDetection />} />
      <Route path="/alerts" element={<ThreatAlerts />} />
    </Routes>
  );
}

export default App;