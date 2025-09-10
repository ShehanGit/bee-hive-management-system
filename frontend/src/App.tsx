// src/App.tsx (ensure all imports use .tsx for consistency)
import { Routes, Route } from 'react-router-dom';
import Home from './pages/Home.tsx';  // Now .tsx
import About from './pages/About.tsx';
import HiveManagement from './pages/HiveManagement.tsx';
import NewHivePlacement from './pages/HiveMap.tsx';
import Notifications from './pages/Notifications.tsx';

function App() {
  return (
    <Routes>
      <Route path="/" element={<Home />} />
      <Route path="/about" element={<About />} />
      <Route path="/hive-management" element={<HiveManagement />} />
      <Route path="/NewHivePlacement" element={<NewHivePlacement />} />
      <Route path="/notifications" element={<Notifications />} />
    </Routes>
  );
}

export default App;