import React, { useState } from 'react';
import { 
    FiHome, 
    FiActivity, 
    FiMap, 
    FiBell, 
    FiShield, 
    FiSettings
} from 'react-icons/fi';
import './ModernSidebar.css';

const ModernSidebar: React.FC = () => {
    const [activeItem, setActiveItem] = useState('dashboard');

    const menuItems = [
        { id: 'dashboard', label: 'Dashboard', icon: FiHome, path: '/dashboard' },
        { id: 'hive-management', label: 'Hive Management', icon: FiActivity, path: '/hive-management' },
        { id: 'hive-map', label: 'Hive Map', icon: FiMap, path: '/hive-map' },
        { id: 'notifications', label: 'Notifications', icon: FiBell, path: '/notifications' },
        { id: 'threat-alerts', label: 'Threat Alerts', icon: FiShield, path: '/threat-alerts' },
        { id: 'settings', label: 'Settings', icon: FiSettings, path: '/settings' }
    ];

    return (
        <aside className="modern-sidebar">
            {/* Sidebar Header */}
            <div className="sidebar-header">
                <div className="sidebar-logo">
                    <FiActivity className="logo-icon" />
                    <span className="logo-text">BeeHive</span>
                </div>
            </div>

            {/* Navigation Menu */}
            <nav className="sidebar-nav">
                <ul className="nav-list">
                    {menuItems.map((item) => {
                        const IconComponent = item.icon;
                        return (
                            <li key={item.id} className="nav-item">
                                <a
                                    href={item.path}
                                    className={`nav-link ${activeItem === item.id ? 'active' : ''}`}
                                    onClick={() => setActiveItem(item.id)}
                                >
                                    <IconComponent className="nav-icon" />
                                    <span className="nav-label">{item.label}</span>
                                </a>
                            </li>
                        );
                    })}
                </ul>
            </nav>

            {/* Sidebar Footer */}
            <div className="sidebar-footer">
                <div className="user-info">
                    <div className="user-avatar">
                        <span className="avatar-text">MH</span>
                    </div>
                    <div className="user-details">
                        <div className="user-name">Malinda</div>
                        <div className="user-role">Beekeeper</div>
                    </div>
                </div>
            </div>
        </aside>
    );
};

export default ModernSidebar;
