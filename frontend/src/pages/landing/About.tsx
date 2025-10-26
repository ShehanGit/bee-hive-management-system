import React from 'react';
import LandingNavbar from '../../components/LandingNavbar';
import './About.css';

const About: React.FC = () => {
  return (
    <div className="landing-about">
      <LandingNavbar />
      
      {/* Hero Section */}
      <section className="about-hero">
        <div className="container">
          <h1>About BeeHive Pro</h1>
          <p className="hero-subtitle">Revolutionizing Beekeeping with AI and IoT Technology</p>
        </div>
      </section>

      {/* Mission Section */}
      <section className="mission-section">
        <div className="container">
          <div className="mission-content">
            <div className="mission-text">
              <h2>Our Mission</h2>
              <p>
                At BeeHive Pro, we're dedicated to helping beekeepers worldwide achieve healthier colonies, 
                higher honey yields, and sustainable apiary management through cutting-edge technology.
              </p>
              <p>
                Our AI-powered platform combines IoT sensors, machine learning, and real-time analytics 
                to provide unprecedented insights into hive health and productivity.
              </p>
            </div>
            <div className="mission-visual">
              <div className="mission-card">
                <div className="card-icon">🎯</div>
                <h3>Our Vision</h3>
                <p>To become the global standard for intelligent beekeeping management</p>
              </div>
              <div className="mission-card">
                <div className="card-icon">🌍</div>
                <h3>Global Impact</h3>
                <p>Supporting beekeepers in 50+ countries with reliable, data-driven insights</p>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* Technology Section */}
      <section className="tech-section">
        <div className="container">
          <h2>Powered by Advanced Technology</h2>
          <div className="tech-grid">
            <div className="tech-item">
              <div className="tech-icon">🤖</div>
              <h3>Machine Learning</h3>
              <p>Deep learning algorithms analyze millions of data points to detect patterns and predict hive health issues before they become critical.</p>
            </div>
            
            <div className="tech-item">
              <div className="tech-icon">☁️</div>
              <h3>IoT Integration</h3>
              <p>Real-time sensor monitoring via ESP32 devices connected through Adafruit IO cloud infrastructure for seamless data collection.</p>
            </div>
            
            <div className="tech-item">
              <div className="tech-icon">📊</div>
              <h3>Data Analytics</h3>
              <p>Comprehensive data synchronization between weather APIs and sensor networks for holistic environmental understanding.</p>
            </div>
            
            <div className="tech-item">
              <div className="tech-icon">🔬</div>
              <h3>Threat Detection</h3>
              <p>Advanced anomaly detection models identify diseases, parasites, and environmental threats with 95%+ accuracy.</p>
            </div>
          </div>
        </div>
      </section>

      {/* Team Section */}
      <section className="team-section">
        <div className="container">
          <h2>Key Capabilities</h2>
          <div className="capabilities-grid">
            <div className="capability-card">
              <div className="capability-number">24/7</div>
              <h3>Continuous Monitoring</h3>
              <p>Never miss a critical change in your hive conditions. Our system provides round-the-clock surveillance.</p>
            </div>
            
            <div className="capability-card">
              <div className="capability-number">99.9%</div>
              <h3>System Uptime</h3>
              <p>Reliable cloud infrastructure ensures your data is always accessible when you need it most.</p>
            </div>
            
            <div className="capability-card">
              <div className="capability-number">50K+</div>
              <h3>Data Points/Day</h3>
              <p>Collect and analyze thousands of measurements daily to ensure comprehensive hive health assessment.</p>
            </div>
            
            <div className="capability-card">
              <div className="capability-number">AI</div>
              <h3>Predictive Insights</h3>
              <p>Anticipate issues before they occur with AI-powered prediction models trained on historical data.</p>
            </div>
          </div>
        </div>
      </section>

      {/* Values Section */}
      <section className="values-section">
        <div className="container">
          <h2>What We Stand For</h2>
          <div className="values-grid">
            <div className="value-item">
              <h3>🐝 Bee Welfare First</h3>
              <p>Every feature we build prioritizes the health and wellbeing of your bees above all else.</p>
            </div>
            
            <div className="value-item">
              <h3>📊 Data-Driven Decisions</h3>
              <p>Make informed choices based on accurate, real-time data and AI-powered insights.</p>
            </div>
            
            <div className="value-item">
              <h3>🌱 Sustainability</h3>
              <p>Supporting sustainable beekeeping practices that benefit both beekeepers and the environment.</p>
            </div>
            
            <div className="value-item">
              <h3>🤝 Community</h3>
              <p>Building a global network of beekeepers sharing knowledge and best practices.</p>
            </div>
          </div>
        </div>
      </section>

      {/* CTA Section */}
      <section className="about-cta">
        <div className="container">
          <h2>Ready to Get Started?</h2>
          <p>Join thousands of beekeepers using BeeHive Pro to optimize their apiaries</p>
          <a href="/dashboard" className="btn btn-primary btn-large">Start Free Trial</a>
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
                <li><a href="/landing">Features</a></li>
                <li><a href="/landing/pricing">Pricing</a></li>
                <li><a href="/dashboard">Dashboard</a></li>
              </ul>
            </div>
            
            <div className="footer-col">
              <h4>Company</h4>
              <ul>
                <li><a href="/landing/about">About</a></li>
                <li><a href="/landing/contact">Contact</a></li>
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

export default About;

