import React, { useState } from 'react';
import { Link } from 'react-router-dom';
import { FaBell } from 'react-icons/fa'; // Optional: Bell icon for notification feel
import './Navbar.css';

function Navbar() {
  const [isOpen, setIsOpen] = useState(false);

  const toggleMenu = () => {
    setIsOpen(!isOpen);
  };

  return (
    <nav className="navbar">
      <div className="navbar-logo">
        <Link to="/">BeeSync</Link>
      </div>
      <div className="navbar-hamburger" onClick={toggleMenu}>
        <div className={`bar ${isOpen ? 'open' : ''}`}></div>
        <div className={`bar ${isOpen ? 'open' : ''}`}></div>
        <div className={`bar ${isOpen ? 'open' : ''}`}></div>
      </div>
      <ul className={`navbar-menu ${isOpen ? 'active' : ''}`}>
        <li>
          <Link to="/" onClick={() => setIsOpen(false)}>Home</Link>
        </li>
        <li>
          <Link to="/about" onClick={() => setIsOpen(false)}>About</Link>
          <li>
            <Link to="/monitoring" onClick={() => setIsOpen(false)}>Monitoring Dashboard</Link>
          </li>
        </li>
        <li>
          <Link to="/hive-management" onClick={() => setIsOpen(false)}>Manage Hives</Link>
        </li>
        <li>
          <Link to="/health-identification" onClick={() => setIsOpen(false)}>Health Analysis</Link>
        </li>
        <li>
          <Link to="/NewHivePlacement" onClick={() => setIsOpen(false)}>New Hive Placement</Link>
        </li>
        <li>

          <Link to="/threat-detection" onClick={() => setIsOpen(false)}>Threat Detection</Link>
        </li>
        <li>
          <Link to="/alerts">Threat Alerts</Link>
        </li>



      </ul>
    </nav>
  );
}

export default Navbar;