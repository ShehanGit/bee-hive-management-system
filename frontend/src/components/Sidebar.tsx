import React from 'react';
import { Link, useLocation } from 'react-router-dom';
import { 
  FaHome, 
  FaCog, 
  FaMapMarkerAlt, 
  FaHeartbeat, 
  FaShieldAlt, 
  FaBell,
  FaChevronLeft,
  FaChevronRight,
  FaHive,
  FaSignOutAlt
} from 'react-icons/fa';
import './Sidebar.css';

interface SidebarProps {
  isCollapsed: boolean;
  onToggle: () => void;
  isOpen?: boolean;
}

const Sidebar: React.FC<SidebarProps> = ({ isCollapsed, onToggle, isOpen = false }) => {
  const location = useLocation();
  
  const menuItems = [
    {
      id: 'dashboard',
      label: 'Dashboard',
      icon: FaHome,
      path: '/dashboard',
      description: 'Overview and analytics'
    },
    {
      id: 'hive-management',
      label: 'Hive Management',
      icon: FaCog,
      path: '/hive-management',
      description: 'Manage your bee hives'
    },
    {
      id: 'hive-map',
      label: 'Hive Placement',
      icon: FaMapMarkerAlt,
      path: '/NewHivePlacement',
      description: 'Find optimal locations'
    },
    {
      id: 'health-check',
      label: 'Health Analysis',
      icon: FaHeartbeat,
      path: '/health-identification',
      description: 'AI-powered health check'
    },
    {
      id: 'threat-detection',
      label: 'Threat Detection',
      icon: FaShieldAlt,
      path: '/threat-detection',
      description: 'Monitor hive threats'
    },
    {
      id: 'alerts',
      label: 'Threat Alerts',
      icon: FaBell,
      path: '/alerts',
      description: 'View active alerts'
    }
  ];

  const isActive = (path: string) => {
    if (path === '/dashboard') {
      return location.pathname === '/dashboard';
    }
    return location.pathname.startsWith(path);
  };

  const handleLogout = () => {
    // Navigate to landing page
    window.location.href = '/';
  };

  return (
    <div className={`sidebar ${isCollapsed ? 'collapsed' : ''} ${isOpen ? 'open' : ''}`}>
      {/* Sidebar Header */}
      <div className="sidebar-header">
        <div className="sidebar-logo">
          <FaHive className="logo-icon" />
          {!isCollapsed && (
            <div className="logo-text">
              <span className="brand-name">BeeHive Pro</span>
              <span className="brand-subtitle">Dashboard</span>
            </div>
          )}
        </div>
        <button 
          className="sidebar-toggle"
          onClick={onToggle}
          aria-label={isCollapsed ? 'Expand sidebar' : 'Collapse sidebar'}
        >
          {isCollapsed ? <FaChevronRight /> : <FaChevronLeft />}
        </button>
      </div>

      {/* Navigation Menu */}
      <nav className="sidebar-nav">
        <div className="nav-section">
          <div className="nav-section-title">
            {!isCollapsed && <span>Main Menu</span>}
          </div>
          <ul className="nav-list">
            {menuItems.map((item) => {
              const Icon = item.icon;
              const active = isActive(item.path);
              
              return (
                <li key={item.id} className="nav-item">
                  <Link
                    to={item.path}
                    className={`nav-link ${active ? 'active' : ''}`}
                    title={isCollapsed ? `${item.label} - ${item.description}` : ''}
                  >
                    <Icon className="nav-icon" />
                    {!isCollapsed && (
                      <div className="nav-content">
                        <span className="nav-label">{item.label}</span>
                        <span className="nav-description">{item.description}</span>
                      </div>
                    )}
                    {active && <div className="nav-indicator"></div>}
                  </Link>
                </li>
              );
            })}
          </ul>
        </div>
      </nav>

      {/* Sidebar Footer */}
      <div className="sidebar-footer">
        <div className="footer-content">
          {!isCollapsed && (
            <div className="footer-text">
              <p>Keep your bees healthy and productive</p>
            </div>
          )}
          <button 
            className="logout-btn"
            onClick={handleLogout}
            title="Logout to Landing Page"
          >
            <FaSignOutAlt className="logout-icon" />
            {!isCollapsed && <span className="logout-text">Logout</span>}
          </button>
        </div>
      </div>
    </div>
  );
};

export default Sidebar;
