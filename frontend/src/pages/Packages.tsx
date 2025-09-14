import React from 'react';
import LandingLayout from '../components/LandingLayout';
import { FaCheck, FaHive } from 'react-icons/fa';

function Packages() {
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
    const subject = `BeeSync Package Subscription - ${packageTitle}`;
    const body = `Hello,

I am interested in subscribing to the ${packageTitle} package at ${price}/month for my bee hive management system.

Please provide me with the next steps to get started.

Best regards`;
    
    const mailtoLink = `mailto:support@beesync.com?subject=${encodeURIComponent(subject)}&body=${encodeURIComponent(body)}`;
    
    window.location.href = mailtoLink;
  };

  return (
    <LandingLayout>
      {/* Hero Section */}
      <section className="landing-section hero">
        <div className="landing-container">
          <div style={{ textAlign: 'center', maxWidth: '800px', margin: '0 auto' }}>
            <h1 className="landing-title">Choose Your <span className="landing-title highlight">Package</span></h1>
            <p className="landing-subtitle">
              Select the perfect plan for your beekeeping operation
            </p>
          </div>
        </div>
      </section>

      {/* Packages Section */}
      <section className="landing-section white">
        <div className="landing-container">
          <div className="landing-grid three">
            {packages.map((pkg, index) => (
              <div key={index} className="landing-card" style={{ position: 'relative', overflow: 'hidden' }}>
                {index === 1 && (
                  <div style={{ 
                    position: 'absolute', 
                    top: '1rem', 
                    right: '1rem', 
                    background: 'linear-gradient(135deg, #f59e0b, #d97706)', 
                    color: 'white', 
                    padding: '0.5rem 1rem', 
                    borderRadius: '20px', 
                    fontSize: '0.875rem', 
                    fontWeight: '600',
                    zIndex: 1
                  }}>
                    Most Popular
                  </div>
                )}
                
                <div style={{ textAlign: 'center', marginBottom: '2rem' }}>
                  <h2 style={{ fontSize: '1.5rem', fontWeight: '700', color: '#1e293b', marginBottom: '1rem' }}>{pkg.title}</h2>
                  <div style={{ marginBottom: '0.5rem' }}>
                    <span style={{ fontSize: '3rem', fontWeight: '800', color: '#f59e0b', lineHeight: 1 }}>{pkg.price}</span>
                    <span style={{ fontSize: '1rem', color: '#64748b', marginLeft: '0.5rem' }}>/month</span>
                  </div>
                  <p style={{ color: '#64748b', fontSize: '0.9rem', margin: 0 }}>{pkg.billing}</p>
                </div>

                <button 
                  className="landing-btn primary"
                  style={{ width: '100%', marginBottom: '2rem' }}
                  onClick={() => handleGetStarted(pkg.title, pkg.price)}
                >
                  <FaHive className="btn-icon" />
                  <span>Get Started</span>
                </button>

                <div style={{ display: 'flex', flexDirection: 'column', gap: '1rem' }}>
                  {pkg.features.map((feature, idx) => (
                    <div key={idx} style={{ display: 'flex', alignItems: 'center', gap: '0.75rem' }}>
                      <div style={{ 
                        width: '20px', 
                        height: '20px', 
                        background: 'linear-gradient(135deg, #10b981, #059669)', 
                        borderRadius: '50%', 
                        display: 'flex', 
                        alignItems: 'center', 
                        justifyContent: 'center',
                        flexShrink: 0
                      }}>
                        <FaCheck style={{ color: 'white', fontSize: '0.75rem' }} />
                      </div>
                      <span style={{ color: '#64748b', fontSize: '0.95rem' }}>{feature}</span>
                    </div>
                  ))}
                </div>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* CTA Section */}
      <section className="landing-section dark">
        <div className="landing-container">
          <div style={{ textAlign: 'center', maxWidth: '600px', margin: '0 auto' }}>
            <h2 className="landing-title" style={{ color: 'white', marginBottom: '1rem' }}>Ready to Start <span style={{ color: '#f59e0b' }}>Monitoring</span>?</h2>
            <p className="landing-subtitle" style={{ color: '#cbd5e1', marginBottom: '2.5rem' }}>
              Join thousands of beekeepers who trust BeeHive Pro for their hive management
            </p>
            <div style={{ display: 'flex', gap: '1rem', justifyContent: 'center' }}>
              <a href="/dashboard" className="landing-btn primary">
                <FaHive className="btn-icon" />
                <span>Start Free Trial</span>
              </a>
              <a href="/contact" className="landing-btn white">
                <span>Contact Sales</span>
              </a>
            </div>
          </div>
        </div>
      </section>
    </LandingLayout>
  );
}

export default Packages;