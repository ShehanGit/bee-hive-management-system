import React from 'react';
import { Link } from 'react-router-dom';
import { FaHive, FaHome, FaInfoCircle, FaBox, FaEnvelope, FaSignInAlt } from 'react-icons/fa';
import './LandingNavbar.css';

const LandingNavbar: React.FC = () => {
  return (
    <nav className="landing-navbar">
      <div className="navbar-container">
        {/* Logo */}
        <div className="navbar-brand">
          <Link to="/" className="brand-link">
            <FaHive className="brand-icon" />
            <span className="brand-text">BeeHive Pro</span>
          </Link>
        </div>

        {/* Navigation Links */}
        <div className="navbar-nav">
          <Link to="/" className="nav-link">
            <FaHome className="nav-icon" />
            <span>Home</span>
          </Link>
          <Link to="/about" className="nav-link">
            <FaInfoCircle className="nav-icon" />
            <span>About Us</span>
          </Link>
          <Link to="/packages" className="nav-link">
            <FaBox className="nav-icon" />
            <span>Packages</span>
          </Link>
          <Link to="/contact" className="nav-link">
            <FaEnvelope className="nav-icon" />
            <span>Contact Us</span>
          </Link>
        </div>

        {/* Dashboard Button */}
        <div className="navbar-actions">
          <Link to="/dashboard" className="dashboard-btn">
            <FaSignInAlt className="btn-icon" />
            <span>My Dashboard</span>
          </Link>
        </div>
      </div>
    </nav>
  );
};

export default LandingNavbar;

