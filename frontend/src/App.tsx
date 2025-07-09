// App.jsx
import { Routes, Route } from 'react-router-dom';
import Home from './pages/Home.jsx';
import About from './pages/About.jsx';
import HiveManagement from './pages/HiveManagement.jsx';
import NewHivePlacement from './pages/HiveMap';

function App() {
  return (
    <Routes>
      <Route path="/" element={<Home />} />
      <Route path="/about" element={<About />} />
      <Route path="/hive-management" element={<HiveManagement />} />
      <Route path="/NewHivePlacement" element={<NewHivePlacement />} />
    </Routes>
  );
}

export default App;
