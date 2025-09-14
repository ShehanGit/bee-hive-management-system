import React from 'react';
import { useLocation } from 'react-router-dom';
import LandingLayout from '../components/LandingLayout';
import About from './About';
import Contact from './Contact';
import Packages from './Packages';
import { FaHive, FaChartLine, FaShieldAlt, FaHeartbeat, FaMapMarkerAlt, FaBell, FaArrowRight, FaStar, FaQuoteLeft } from 'react-icons/fa';

const LandingPage: React.FC = () => {
  const location = useLocation();
  
  // Route to different components based on path
  if (location.pathname === '/about') {
    return <About />;
  }
  
  if (location.pathname === '/contact') {
    return <Contact />;
  }
  
  if (location.pathname === '/packages') {
    return <Packages />;
  }

  // Default home page
  return (
    <LandingLayout>
      {/* Hero Section */}
      <section className="landing-section hero">
        <div className="landing-container">
          <div className="hero-content">
            <div className="hero-text">
              <h1 className="hero-title">
                Smart Bee Hive Management
                <span className="hero-highlight"> Made Simple</span>
              </h1>
              <p className="hero-description">
                Monitor your bee colonies with advanced IoT sensors, AI-powered health analysis, 
                and real-time threat detection. Keep your bees healthy and maximize honey production.
              </p>
              <div className="hero-actions">
                <a href="/dashboard" className="landing-btn primary">
                  <FaHive className="btn-icon" />
                  <span>Start Managing</span>
                  <FaArrowRight className="btn-arrow" />
                </a>
                <a href="/packages" className="landing-btn secondary">
                  <span>View Packages</span>
                </a>
              </div>
              <div className="hero-stats">
                <div className="hero-stat">
                  <span className="stat-number">500+</span>
                  <span className="stat-label">Happy Beekeepers</span>
                </div>
                <div className="hero-stat">
                  <span className="stat-number">10K+</span>
                  <span className="stat-label">Hives Monitored</span>
                </div>
                <div className="hero-stat">
                  <span className="stat-number">99%</span>
                  <span className="stat-label">Uptime</span>
                </div>
              </div>
            </div>
            <div className="hero-visual">
              <div className="dashboard-preview">
                <div className="preview-header">
                  <div className="preview-dots">
                    <span></span>
                    <span></span>
                    <span></span>
                  </div>
                  <span className="preview-title">BeeHive Dashboard</span>
                </div>
                <div className="preview-content">
                  <div className="preview-stats">
                    <div className="preview-stat">
                      <FaHive className="preview-icon" />
                      <div>
                        <span className="preview-value">12</span>
                        <span className="preview-label">Active Hives</span>
                      </div>
                    </div>
                    <div className="preview-stat">
                      <FaHeartbeat className="preview-icon healthy" />
                      <div>
                        <span className="preview-value">98%</span>
                        <span className="preview-label">Health</span>
                      </div>
                    </div>
                  </div>
                  <div className="preview-chart">
                    <div className="chart-bars">
                      <div className="bar" style={{ height: '60%' }}></div>
                      <div className="bar" style={{ height: '80%' }}></div>
                      <div className="bar" style={{ height: '45%' }}></div>
                      <div className="bar" style={{ height: '90%' }}></div>
                      <div className="bar" style={{ height: '70%' }}></div>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* Features Section */}
      <section className="landing-section white">
        <div className="landing-container">
          <h2 className="landing-title">Why Choose <span className="landing-title highlight">BeeHive Pro</span>?</h2>
          <p className="landing-subtitle">
            Advanced technology meets traditional beekeeping wisdom
          </p>
          <div className="landing-grid three">
            <div className="landing-card">
              <div className="card-icon">
                <FaChartLine />
              </div>
              <h3 className="card-title">Real-time Monitoring</h3>
              <p className="card-description">
                Track temperature, humidity, weight, and activity 24/7 with IoT sensors
              </p>
            </div>
            <div className="landing-card">
              <div className="card-icon">
                <FaHeartbeat />
              </div>
              <h3 className="card-title">Health Analysis</h3>
              <p className="card-description">
                AI-powered bee health identification and disease detection
              </p>
            </div>
            <div className="landing-card">
              <div className="card-icon">
                <FaShieldAlt />
              </div>
              <h3 className="card-title">Threat Detection</h3>
              <p className="card-description">
                Early warning system for pests, predators, and environmental threats
              </p>
            </div>
            <div className="landing-card">
              <div className="card-icon">
                <FaMapMarkerAlt />
              </div>
              <h3 className="card-title">Location Optimization</h3>
              <p className="card-description">
                Find the best locations for new hives using environmental data
              </p>
            </div>
            <div className="landing-card">
              <div className="card-icon">
                <FaBell />
              </div>
              <h3 className="card-title">Smart Alerts</h3>
              <p className="card-description">
                Get instant notifications about critical events and recommendations
              </p>
            </div>
            <div className="landing-card">
              <div className="card-icon">
                <FaHive />
              </div>
              <h3 className="card-title">Production Insights</h3>
              <p className="card-description">
                Analyze honey production patterns and optimize yield
              </p>
            </div>
          </div>
        </div>
      </section>

      {/* Testimonials Section */}
      <section className="landing-section gray">
        <div className="landing-container">
          <h2 className="landing-title">What Our <span className="landing-title highlight">Beekeepers</span> Say</h2>
          <p className="landing-subtitle">
            Join hundreds of successful beekeepers worldwide
          </p>
          <div className="landing-grid three">
            <div className="landing-card">
              <div className="testimonial-content">
                <FaQuoteLeft className="quote-icon" style={{ color: '#f59e0b', fontSize: '1.5rem', marginBottom: '1rem' }} />
                <p className="testimonial-text" style={{ fontStyle: 'italic', color: '#64748b', lineHeight: '1.6', marginBottom: '1.5rem' }}>
                  "BeeHive Pro transformed my beekeeping. I can monitor all my hives remotely 
                  and get alerts before problems become serious. My honey production increased by 40%!"
                </p>
              </div>
              <div className="testimonial-author" style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                <div className="author-info">
                  <h4 className="author-name" style={{ fontWeight: '600', color: '#1e293b', marginBottom: '0.25rem' }}>Sarah Johnson</h4>
                  <p className="author-title" style={{ color: '#64748b', fontSize: '0.9rem' }}>Commercial Beekeeper</p>
                </div>
                <div className="author-rating" style={{ display: 'flex', gap: '0.25rem' }}>
                  {[...Array(5)].map((_, i) => (
                    <FaStar key={i} className="star filled" style={{ color: '#f59e0b', fontSize: '1rem' }} />
                  ))}
                </div>
              </div>
            </div>
            <div className="landing-card">
              <div className="testimonial-content">
                <FaQuoteLeft className="quote-icon" style={{ color: '#f59e0b', fontSize: '1.5rem', marginBottom: '1rem' }} />
                <p className="testimonial-text" style={{ fontStyle: 'italic', color: '#64748b', lineHeight: '1.6', marginBottom: '1.5rem' }}>
                  "The AI health analysis caught a disease outbreak early. Without BeeHive Pro, 
                  I would have lost half my colonies. This technology is a game-changer!"
                </p>
              </div>
              <div className="testimonial-author" style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                <div className="author-info">
                  <h4 className="author-name" style={{ fontWeight: '600', color: '#1e293b', marginBottom: '0.25rem' }}>Michael Chen</h4>
                  <p className="author-title" style={{ color: '#64748b', fontSize: '0.9rem' }}>Hobby Beekeeper</p>
                </div>
                <div className="author-rating" style={{ display: 'flex', gap: '0.25rem' }}>
                  {[...Array(5)].map((_, i) => (
                    <FaStar key={i} className="star filled" style={{ color: '#f59e0b', fontSize: '1rem' }} />
                  ))}
                </div>
              </div>
            </div>
            <div className="landing-card">
              <div className="testimonial-content">
                <FaQuoteLeft className="quote-icon" style={{ color: '#f59e0b', fontSize: '1.5rem', marginBottom: '1rem' }} />
                <p className="testimonial-text" style={{ fontStyle: 'italic', color: '#64748b', lineHeight: '1.6', marginBottom: '1.5rem' }}>
                  "The location optimization feature helped me find the perfect spots for new hives. 
                  My bees are healthier and more productive than ever before."
                </p>
              </div>
              <div className="testimonial-author" style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                <div className="author-info">
                  <h4 className="author-name" style={{ fontWeight: '600', color: '#1e293b', marginBottom: '0.25rem' }}>Emily Rodriguez</h4>
                  <p className="author-title" style={{ color: '#64748b', fontSize: '0.9rem' }}>Urban Beekeeper</p>
                </div>
                <div className="author-rating" style={{ display: 'flex', gap: '0.25rem' }}>
                  {[...Array(5)].map((_, i) => (
                    <FaStar key={i} className="star filled" style={{ color: '#f59e0b', fontSize: '1rem' }} />
                  ))}
                </div>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* CTA Section */}
      <section className="landing-section dark">
        <div className="landing-container">
          <div style={{ textAlign: 'center', maxWidth: '600px', margin: '0 auto' }}>
            <h2 className="landing-title" style={{ color: 'white', marginBottom: '1rem' }}>Ready to Transform Your <span style={{ color: '#f59e0b' }}>Beekeeping</span>?</h2>
            <p className="landing-subtitle" style={{ color: '#cbd5e1', marginBottom: '2.5rem' }}>
              Join thousands of beekeepers who trust BeeHive Pro for their hive management
            </p>
            <div style={{ display: 'flex', gap: '1rem', justifyContent: 'center' }}>
              <a href="/dashboard" className="landing-btn primary">
                <FaHive className="btn-icon" />
                <span>Start Your Free Trial</span>
                <FaArrowRight className="btn-arrow" />
              </a>
              <a href="/contact" className="landing-btn white">
                <span>Contact Sales</span>
              </a>
            </div>
          </div>
        </div>
      </section>

      {/* Footer */}
      <footer style={{ background: '#1e293b', color: 'white', padding: '2rem 0' }}>
        <div className="landing-container">
          <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '1rem' }}>
            <div style={{ display: 'flex', alignItems: 'center', gap: '0.75rem' }}>
              <FaHive style={{ fontSize: '1.5rem', color: '#f59e0b' }} />
              <span style={{ fontSize: '1.25rem', fontWeight: '700' }}>BeeHive Pro</span>
            </div>
            <div style={{ display: 'flex', gap: '2rem' }}>
              <a href="/about" style={{ color: '#cbd5e1', textDecoration: 'none', transition: 'color 0.3s ease' }} onMouseEnter={(e) => (e.target as HTMLElement).style.color = '#f59e0b'} onMouseLeave={(e) => (e.target as HTMLElement).style.color = '#cbd5e1'}>About Us</a>
              <a href="/packages" style={{ color: '#cbd5e1', textDecoration: 'none', transition: 'color 0.3s ease' }} onMouseEnter={(e) => (e.target as HTMLElement).style.color = '#f59e0b'} onMouseLeave={(e) => (e.target as HTMLElement).style.color = '#cbd5e1'}>Packages</a>
              <a href="/contact" style={{ color: '#cbd5e1', textDecoration: 'none', transition: 'color 0.3s ease' }} onMouseEnter={(e) => (e.target as HTMLElement).style.color = '#f59e0b'} onMouseLeave={(e) => (e.target as HTMLElement).style.color = '#cbd5e1'}>Contact</a>
              <a href="/dashboard" style={{ color: '#cbd5e1', textDecoration: 'none', transition: 'color 0.3s ease' }} onMouseEnter={(e) => (e.target as HTMLElement).style.color = '#f59e0b'} onMouseLeave={(e) => (e.target as HTMLElement).style.color = '#cbd5e1'}>Dashboard</a>
            </div>
          </div>
          <div style={{ textAlign: 'center', paddingTop: '1rem', borderTop: '1px solid #374151' }}>
            <p style={{ color: '#9ca3af', fontSize: '0.9rem', margin: 0 }}>
              © 2024 BeeHive Pro. All rights reserved.
            </p>
          </div>
        </div>
      </footer>
    </LandingLayout>
  );
};

export default LandingPage;
