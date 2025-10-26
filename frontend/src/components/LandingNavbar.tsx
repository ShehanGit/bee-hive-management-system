import React, { useState } from 'react';
import { Link, useLocation } from 'react-router-dom';
import './LandingNavbar.css';

const LandingNavbar: React.FC = () => {
  const [isMenuOpen, setIsMenuOpen] = useState(false);
  const location = useLocation();

  const isActive = (path: string) => {
    return location.pathname === path ? 'active' : '';
  };

  return (
    <nav className="landing-navbar">
      <div className="landing-nav-container">
        <div className="landing-nav-logo">
          <span className="logo-icon">🍯</span>
          <span className="logo-text">BeeHive Pro</span>
        </div>

        <button 
          className={`mobile-menu-toggle ${isMenuOpen ? 'active' : ''}`}
          onClick={() => setIsMenuOpen(!isMenuOpen)}
          aria-label="Toggle menu"
        >
          <span></span>
          <span></span>
          <span></span>
        </button>

        <ul className={`landing-nav-links ${isMenuOpen ? 'active' : ''}`}>
          <li><Link to="/landing" className={isActive('/landing')}>Home</Link></li>
          <li><Link to="/landing/about" className={isActive('/landing/about')}>About</Link></li>
          <li><Link to="/landing/pricing" className={isActive('/landing/pricing')}>Pricing</Link></li>
          <li><Link to="/landing/contact" className={isActive('/landing/contact')}>Contact</Link></li>
          <li><Link to="/dashboard" className="nav-cta">Dashboard</Link></li>
        </ul>
      </div>
    </nav>
  );
};

export default LandingNavbar;

