import React from 'react';
import { FaHive, FaChartLine, FaBell, FaShieldAlt, FaHeartbeat } from 'react-icons/fa';
import './DashboardOverview.css';

interface DashboardOverviewProps {
  isSidebarCollapsed?: boolean;
}

const DashboardOverview: React.FC<DashboardOverviewProps> = ({ isSidebarCollapsed = false }) => {
  const stats = [
    {
      id: 'active-hives',
      label: 'Active Hives',
      value: '12',
      icon: FaHive,
      color: '#f59e0b',
      change: '+2 this month',
      changeType: 'positive'
    },
    {
      id: 'health-checks',
      label: 'Health Checks',
      value: '8',
      icon: FaHeartbeat,
      color: '#10b981',
      change: 'All healthy',
      changeType: 'positive'
    },
    {
      id: 'active-alerts',
      label: 'Active Alerts',
      value: '3',
      icon: FaBell,
      color: '#ef4444',
      change: '2 new today',
      changeType: 'warning'
    },
    {
      id: 'threats-blocked',
      label: 'Threats Blocked',
      value: '15',
      icon: FaShieldAlt,
      color: '#3b82f6',
      change: 'Last 7 days',
      changeType: 'neutral'
    }
  ];

  const recentActivities = [
    {
      id: 1,
      type: 'health-check',
      message: 'Health analysis completed for Hive #3',
      time: '2 minutes ago',
      status: 'success'
    },
    {
      id: 2,
      type: 'threat-detected',
      message: 'Environmental threat detected in Hive #7',
      time: '15 minutes ago',
      status: 'warning'
    },
    {
      id: 3,
      type: 'hive-added',
      message: 'New hive "Sunny Meadow" added successfully',
      time: '1 hour ago',
      status: 'success'
    },
    {
      id: 4,
      type: 'alert-resolved',
      message: 'Wax moth threat resolved in Hive #2',
      time: '2 hours ago',
      status: 'success'
    }
  ];

  return (
    <div className={`dashboard-overview ${isSidebarCollapsed ? 'collapsed' : ''}`}>
      <div className="dashboard-header">
        <h1>Welcome back, Beekeeper! 🐝</h1>
        <p>Here's what's happening with your hives today</p>
      </div>

      {/* Stats Grid */}
      <div className="stats-grid">
        {stats.map((stat) => {
          const Icon = stat.icon;
          return (
            <div key={stat.id} className="stat-card">
              <div className="stat-icon" style={{ color: stat.color }}>
                <Icon />
              </div>
              <div className="stat-content">
                <div className="stat-value">{stat.value}</div>
                <div className="stat-label">{stat.label}</div>
                <div className={`stat-change ${stat.changeType}`}>
                  {stat.change}
                </div>
              </div>
            </div>
          );
        })}
      </div>

      {/* Recent Activities */}
      <div className="activities-section">
        <h2>Recent Activities</h2>
        <div className="activities-list">
          {recentActivities.map((activity) => (
            <div key={activity.id} className={`activity-item ${activity.status}`}>
              <div className="activity-icon">
                {activity.type === 'health-check' && <FaHeartbeat />}
                {activity.type === 'threat-detected' && <FaShieldAlt />}
                {activity.type === 'hive-added' && <FaHive />}
                {activity.type === 'alert-resolved' && <FaBell />}
              </div>
              <div className="activity-content">
                <div className="activity-message">{activity.message}</div>
                <div className="activity-time">{activity.time}</div>
              </div>
            </div>
          ))}
        </div>
      </div>

      {/* Quick Actions */}
      <div className="quick-actions">
        <h2>Quick Actions</h2>
        <div className="actions-grid">
          <button className="action-btn primary">
            <FaHive />
            <span>Add New Hive</span>
          </button>
          <button className="action-btn secondary">
            <FaHeartbeat />
            <span>Health Check</span>
          </button>
          <button className="action-btn secondary">
            <FaShieldAlt />
            <span>Threat Scan</span>
          </button>
          <button className="action-btn secondary">
            <FaChartLine />
            <span>View Analytics</span>
          </button>
        </div>
      </div>
    </div>
  );
};

export default DashboardOverview;
