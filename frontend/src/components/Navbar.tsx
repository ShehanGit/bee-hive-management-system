import React, { useState } from 'react';
import { Link } from 'react-router-dom';
import { FaBell, FaBars } from 'react-icons/fa'; // Optional: Bell icon for notification feel
import './Navbar.css';

interface NavbarProps {
  onMobileSidebarToggle?: () => void;
}

function Navbar({ onMobileSidebarToggle }: NavbarProps) {
  const [isOpen, setIsOpen] = useState(false);

  const toggleMenu = () => {
    setIsOpen(!isOpen);
  };

  const handleMobileSidebarToggle = () => {
    if (onMobileSidebarToggle) {
      onMobileSidebarToggle();
    }
  };

  return (
    <nav className="navbar">
      <div className="navbar-left">
        <button 
          className="mobile-sidebar-toggle"
          onClick={handleMobileSidebarToggle}
          aria-label="Toggle sidebar"
        >
          <FaBars />
        </button>
        <div className="navbar-logo">
          <Link to="/">BeeSync</Link>
        </div>
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
        </li>
        <li>
          <Link to="/packages" onClick={() => setIsOpen(false)}>Pricing</Link>
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