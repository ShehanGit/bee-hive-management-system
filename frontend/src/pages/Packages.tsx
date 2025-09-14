import React from 'react';
import { useNavigate } from 'react-router-dom';
import Navbar from '../components/Navbar';
import './Packages.css';

function Packages() {
  const navigate = useNavigate();
  
  const packages = [
    {
      title: '1-3 Hives',
      price: '£4.99',
      billing: 'Billed monthly, cancel anytime.',
      features: [
        'Cloud Dashboard',
        'Seasonal Monitoring',
        'Real-time Alerts',
        'Email/SMS Notifications',
        'Hive Locations',
        '£1.66 per hive'
      ]
    },
    {
      title: '4-6 Hives',
      price: '£7.99',
      billing: 'Billed monthly, cancel anytime.',
      features: [
        'Cloud Dashboard',
        'Seasonal Monitoring',
        'Real-time Alerts',
        'Email/SMS Notifications',
        'Hive Locations',
        '£1.33 per hive'
      ]
    },
    {
      title: '7-10 Hives',
      price: '£9.99',
      billing: 'Billed monthly, cancel anytime.',
      features: [
        'Cloud Dashboard',
        'Seasonal Monitoring',
        'Real-time Alerts',
        'Email/SMS Notifications',
        'Hive Locations',
        '£1.00 per hive'
      ]
    }
  ];

  const handleGetStarted = (packageTitle: string, price: string) => {
    navigate('/register-hive', {
      state: {
        title: packageTitle,
        price: price
      }
    });
  };

  return (
    <div className="packages">
      <Navbar />
      
      <div className="packages-container">
        <header className="packages-header">
          <h1>Choose Your Package</h1>
          <p>Select the perfect plan for your beekeeping operation</p>
        </header>

        <div className="packages-grid">
          {packages.map((pkg, index) => (
            <div key={index} className="package-card">
              <div className="package-header">
                <h2>{pkg.title}</h2>
                <div className="package-price">
                  <span className="price">{pkg.price}</span>
                </div>
                <p className="billing-info">{pkg.billing}</p>
              </div>

              <button 
                className="get-started-btn"
                onClick={() => handleGetStarted(pkg.title, pkg.price)}
              >
                Get started
              </button>

              <div className="package-features">
                {pkg.features.map((feature, idx) => (
                  <div key={idx} className="feature-item">
                    <span className="checkmark">✓</span>
                    <span className="feature-text">{feature}</span>
                  </div>
                ))}
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}

export default Packages;