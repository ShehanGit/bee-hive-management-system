import { useState } from 'react';
import { Link, useLocation, useNavigate } from 'react-router-dom';
import { 
  FiBarChart2, 
  FiLayers, 
  FiMapPin, 
  FiActivity, 
  FiAlertTriangle,
  FiLogOut
} from 'react-icons/fi';
import './Navbar.css';

function Navbar() {
  const [isOpen, setIsOpen] = useState(false);
  const [hoveredItem, setHoveredItem] = useState<string | null>(null);
  const location = useLocation();
  const navigate = useNavigate();

  const toggleMenu = () => {
    setIsOpen(!isOpen);
  };

  const handleLogout = () => {
    console.log('Logging out...');
    // Navigate to landing page
    navigate('/');
  };

  const menuItems = [
    { path: '/dashboard', icon: FiBarChart2, label: 'Dashboard', name: 'dashboard' },
    { path: '/hive-management', icon: FiLayers, label: 'Manage Hives', name: 'hive-management' },
    { path: '/NewHivePlacement', icon: FiMapPin, label: 'New Hive Placement', name: 'new-placement' },
    { path: '/health', icon: FiActivity, label: 'Health', name: 'health' },
    { path: '/alerts', icon: FiAlertTriangle, label: 'Threat Alerts', name: 'alerts' },
  ];

  return (
    <nav className="navbar">
      <div className="navbar-container">
        {/* Logo Icon - Left Side */}
        <div className="navbar-logo-icon">
          <Link to="/" className="logo-link-wrapper">
            <div className="logo-icon-wrapper">
              <img 
                src="/BeeSyc-removebg-preview.png" 
                alt="BeeSyc Logo" 
                className="logo-image"
              />
            </div>
          </Link>
        </div>
        
        {/* Hamburger Menu */}
        <div className="navbar-hamburger" onClick={toggleMenu}>
          <div className={`bar ${isOpen ? 'open' : ''}`}></div>
          <div className={`bar ${isOpen ? 'open' : ''}`}></div>
          <div className={`bar ${isOpen ? 'open' : ''}`}></div>
        </div>
        
        {/* Navigation Menu */}
        <ul className={`navbar-menu ${isOpen ? 'active' : ''}`}>
          {menuItems.map((item) => {
            const Icon = item.icon;
            const isActive = location.pathname === item.path;
            
            return (
              <li 
                key={item.name}
                onMouseEnter={() => setHoveredItem(item.name)}
                onMouseLeave={() => setHoveredItem(null)}
              >
                <Link 
                  to={item.path} 
                  onClick={() => setIsOpen(false)}
                  className={isActive ? 'active' : ''}
                  data-tooltip={hoveredItem === item.name ? item.label : ''}
                >
                  <Icon className="nav-icon" />
                  <span className="tooltip">{item.label}</span>
                </Link>
              </li>
            );
          })}
        </ul>
        
        {/* Logout Button - Right Side */}
        <div className="navbar-logout">
          <button 
            onClick={handleLogout}
            className="logout-button"
            title="Logout"
            onMouseEnter={() => setHoveredItem('logout')}
            onMouseLeave={() => setHoveredItem(null)}
          >
            <FiLogOut className="logout-icon" />
            <span className="tooltip">Logout</span>
          </button>
        </div>
      </div>
    </nav>
  );
}

export default Navbar;