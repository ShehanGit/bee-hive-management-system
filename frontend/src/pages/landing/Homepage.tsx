import React from 'react';
import { Link } from 'react-router-dom';
import LandingNavbar from '../../components/LandingNavbar';
import './Homepage.css';

const Homepage: React.FC = () => {
  return (
    <div className="landing-homepage">
      <LandingNavbar />
      
      {/* Hero Section */}
      <section className="hero-landing">
        <div className="hero-content-landing">
          <div className="hero-text">
            <h1 className="hero-title">
              Smart Bee Hive Management
              <span className="title-highlight"> Made Simple</span>
            </h1>
            <p className="hero-description">
              Monitor your hives with AI-powered insights, real-time threat detection, 
              and automated performance tracking. Boost honey production and keep your bees healthy.
            </p>
            <div className="hero-buttons">
              <Link to="/dashboard" className="btn btn-primary">
                Get Started Free
              </Link>
              <Link to="/landing/about" className="btn btn-secondary">
                Learn More
              </Link>
            </div>
            <div className="hero-stats">
              <div className="stat-item">
                <div className="stat-number">1000+</div>
                <div className="stat-label">Hives Monitored</div>
              </div>
              <div className="stat-item">
                <div className="stat-number">99.9%</div>
                <div className="stat-label">Uptime</div>
              </div>
              <div className="stat-item">
                <div className="stat-number">50K+</div>
                <div className="stat-label">Data Points/Day</div>
              </div>
            </div>
          </div>
          <div className="hero-image">
            <div className="floating-card card-1">
              <div className="card-icon">🌡️</div>
              <div className="card-info">
                <div className="card-label">Temperature</div>
                <div className="card-value">32°C</div>
              </div>
            </div>
            <div className="floating-card card-2">
              <div className="card-icon">💧</div>
              <div className="card-info">
                <div className="card-label">Humidity</div>
                <div className="card-value">65%</div>
              </div>
            </div>
            <div className="floating-card card-3">
              <div className="card-icon">🔊</div>
              <div className="card-info">
                <div className="card-label">Sound Level</div>
                <div className="card-value">72 dB</div>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* Features Section */}
      <section className="features-landing">
        <div className="container">
          <div className="section-header">
            <h2 className="section-title">Powerful Features</h2>
            <p className="section-subtitle">
              Everything you need to manage your apiary with confidence
            </p>
          </div>
          
          <div className="features-grid">
            <div className="feature-card">
              <div className="feature-icon">🚨</div>
              <h3>AI Threat Detection</h3>
              <p>Advanced machine learning algorithms detect diseases, parasites, and environmental threats in real-time before they become critical.</p>
            </div>
            
            <div className="feature-card">
              <div className="feature-icon">📊</div>
              <h3>Performance Prediction</h3>
              <p>Predict hive productivity and health trends using weather patterns, historical data, and AI-powered analytics.</p>
            </div>
            
            <div className="feature-card">
              <div className="feature-icon">📍</div>
              <h3>Optimal Placement</h3>
              <p>Find the best hive locations based on environmental factors, proximity to resources, and predicted performance.</p>
            </div>
            
            <div className="feature-card">
              <div className="feature-icon">🌡️</div>
              <h3>IoT Monitoring</h3>
              <p>24/7 temperature, humidity, sound, and weight monitoring with instant alerts and data visualization.</p>
            </div>
            
            <div className="feature-card">
              <div className="feature-icon">☁️</div>
              <h3>Weather Integration</h3>
              <p>Real-time weather data synchronization to understand how environmental conditions affect your hives.</p>
            </div>
            
            <div className="feature-card">
              <div className="feature-icon">📱</div>
              <h3>Real-Time Dashboard</h3>
              <p>Beautiful, responsive dashboard with live updates, charts, and comprehensive hive health metrics.</p>
            </div>
          </div>
        </div>
      </section>

      {/* How It Works */}
      <section className="how-it-works">
        <div className="container">
          <div className="section-header">
            <h2 className="section-title">How It Works</h2>
            <p className="section-subtitle">Simple setup, powerful results</p>
          </div>
          
          <div className="steps-container">
            <div className="step-item">
              <div className="step-number">1</div>
              <h3>Install Sensors</h3>
              <p>Set up IoT sensors in your hives to monitor temperature, humidity, sound, and weight.</p>
            </div>
            
            <div className="step-connector"></div>
            
            <div className="step-item">
              <div className="step-number">2</div>
              <h3>Connect to Platform</h3>
              <p>Sensors automatically sync data via Adafruit IO cloud to our secure platform.</p>
            </div>
            
            <div className="step-connector"></div>
            
            <div className="step-item">
              <div className="step-number">3</div>
              <h3>Get Insights</h3>
              <p>AI analyzes your data and provides actionable insights, predictions, and alerts.</p>
            </div>
          </div>
        </div>
      </section>

      {/* CTA Section */}
      <section className="cta-landing">
        <div className="container">
          <div className="cta-content">
            <h2>Ready to Transform Your Beekeeping?</h2>
            <p>Join thousands of beekeepers using AI to optimize their hives</p>
            <Link to="/dashboard" className="btn btn-primary btn-large">
              Start Free Trial
            </Link>
          </div>
        </div>
      </section>

      {/* Footer */}
      <footer className="landing-footer">
        <div className="container">
          <div className="footer-content">
            <div className="footer-col">
              <div className="footer-logo">
                <span className="logo-icon">🍯</span>
                <span className="logo-text">BeeHive Pro</span>
              </div>
              <p>Smart beekeeping management for the modern age.</p>
            </div>
            
            <div className="footer-col">
              <h4>Product</h4>
              <ul>
                <li><Link to="/landing">Features</Link></li>
                <li><Link to="/landing/pricing">Pricing</Link></li>
                <li><Link to="/dashboard">Dashboard</Link></li>
              </ul>
            </div>
            
            <div className="footer-col">
              <h4>Company</h4>
              <ul>
                <li><Link to="/landing/about">About</Link></li>
                <li><Link to="/landing/contact">Contact</Link></li>
                <li><a href="#">Blog</a></li>
              </ul>
            </div>
            
            <div className="footer-col">
              <h4>Support</h4>
              <ul>
                <li><a href="#">Documentation</a></li>
                <li><a href="#">FAQs</a></li>
                <li><a href="#">Support Center</a></li>
              </ul>
            </div>
          </div>
          
          <div className="footer-bottom">
            <p>&copy; 2024 BeeHive Pro. All rights reserved.</p>
          </div>
        </div>
      </footer>
    </div>
  );
};

export default Homepage;

