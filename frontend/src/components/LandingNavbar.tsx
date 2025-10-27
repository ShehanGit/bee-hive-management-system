import { useState } from 'react';
import { Link, useLocation } from 'react-router-dom';
import './LandingNavbar.css';

const LandingNavbar = () => {
  const [isMenuOpen, setIsMenuOpen] = useState(false);
  const location = useLocation();

  const isActive = (path: string) => {
    return location.pathname === path ? 'active' : '';
  };

  return (
    <nav className="landing-navbar">
      <div className="landing-nav-container">
        <Link to="/" className="landing-nav-logo">
          <img 
            src="/BeeSyc-removebg-preview.png" 
            alt="BeeSyc Logo" 
            className="landing-logo-image"
          />
        </Link>

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

