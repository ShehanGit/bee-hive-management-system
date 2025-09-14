import React from 'react';
import LandingLayout from '../components/LandingLayout';
import { FaHive, FaUsers, FaAward, FaGlobe, FaHeart, FaLightbulb } from 'react-icons/fa';

const About: React.FC = () => {
  return (
    <LandingLayout>
      {/* Hero Section */}
      <section className="landing-section hero">
        <div className="landing-container">
          <div style={{ textAlign: 'center', maxWidth: '800px', margin: '0 auto' }}>
            <h1 className="landing-title">About <span className="landing-title highlight">BeeHive Pro</span></h1>
            <p className="landing-subtitle">
              Revolutionizing beekeeping through technology and innovation
            </p>
          </div>
        </div>
      </section>

      {/* Mission Section */}
      <section className="landing-section white">
        <div className="landing-container">
          <div className="hero-content">
            <div className="hero-text">
              <h2 className="landing-title" style={{ fontSize: '2.5rem', textAlign: 'left', marginBottom: '1.5rem' }}>Our <span className="landing-title highlight">Mission</span></h2>
              <p className="landing-description">
                At BeeHive Pro, we believe that technology can enhance traditional beekeeping practices 
                without replacing the essential knowledge and care that beekeepers bring to their craft. 
                Our mission is to provide beekeepers with intelligent tools that help them monitor, 
                protect, and optimize their hives for maximum health and productivity.
              </p>
              <div className="hero-stats">
                <div className="hero-stat">
                  <span className="stat-number">500+</span>
                  <span className="stat-label">Happy Beekeepers</span>
                </div>
                <div className="hero-stat">
                  <span className="stat-number">10,000+</span>
                  <span className="stat-label">Hives Monitored</span>
                </div>
                <div className="hero-stat">
                  <span className="stat-number">99%</span>
                  <span className="stat-label">Uptime</span>
                </div>
              </div>
            </div>
            <div className="hero-visual">
              <div style={{ width: '200px', height: '200px', background: 'linear-gradient(135deg, #f59e0b, #d97706)', borderRadius: '50%', display: 'flex', alignItems: 'center', justifyContent: 'center', boxShadow: '0 20px 40px rgba(245, 158, 11, 0.3)' }}>
                <FaHive style={{ fontSize: '4rem', color: 'white' }} />
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* Values Section */}
      <section className="landing-section gray">
        <div className="landing-container">
          <h2 className="landing-title">Our <span className="landing-title highlight">Values</span></h2>
          <div className="landing-grid four">
            <div className="landing-card">
              <div className="card-icon">
                <FaHeart />
              </div>
              <h3 className="card-title">Bee Welfare First</h3>
              <p className="card-description">
                Every feature we build prioritizes the health and well-being of your bee colonies.
              </p>
            </div>
            <div className="landing-card">
              <div className="card-icon">
                <FaUsers />
              </div>
              <h3 className="card-title">Beekeeper Community</h3>
              <p className="card-description">
                We're built by beekeepers, for beekeepers. Your feedback drives our innovation.
              </p>
            </div>
            <div className="landing-card">
              <div className="card-icon">
                <FaLightbulb />
              </div>
              <h3 className="card-title">Innovation</h3>
              <p className="card-description">
                We continuously push the boundaries of what's possible in smart beekeeping.
              </p>
            </div>
            <div className="landing-card">
              <div className="card-icon">
                <FaGlobe />
              </div>
              <h3 className="card-title">Sustainability</h3>
              <p className="card-description">
                Our technology helps protect pollinators and support ecosystem health.
              </p>
            </div>
          </div>
        </div>
      </section>

      {/* Team Section */}
      <section className="landing-section white">
        <div className="landing-container">
          <h2 className="landing-title">Meet Our <span className="landing-title highlight">Team</span></h2>
          <div className="landing-grid three">
            <div className="landing-card">
              <div style={{ width: '100px', height: '100px', background: 'linear-gradient(135deg, #f59e0b, #d97706)', borderRadius: '50%', display: 'flex', alignItems: 'center', justifyContent: 'center', margin: '0 auto 1.5rem' }}>
                <FaUsers style={{ fontSize: '2.5rem', color: 'white' }} />
              </div>
              <h3 className="card-title">Sarah Johnson</h3>
              <p style={{ color: '#f59e0b', fontWeight: '500', marginBottom: '1rem', textAlign: 'center' }}>CEO & Founder</p>
              <p className="card-description">
                A third-generation beekeeper with 15 years of experience and a passion for technology.
              </p>
            </div>
            <div className="landing-card">
              <div style={{ width: '100px', height: '100px', background: 'linear-gradient(135deg, #f59e0b, #d97706)', borderRadius: '50%', display: 'flex', alignItems: 'center', justifyContent: 'center', margin: '0 auto 1.5rem' }}>
                <FaAward style={{ fontSize: '2.5rem', color: 'white' }} />
              </div>
              <h3 className="card-title">Dr. Michael Chen</h3>
              <p style={{ color: '#f59e0b', fontWeight: '500', marginBottom: '1rem', textAlign: 'center' }}>Chief Technology Officer</p>
              <p className="card-description">
                AI researcher specializing in agricultural applications and bee health monitoring.
              </p>
            </div>
            <div className="landing-card">
              <div style={{ width: '100px', height: '100px', background: 'linear-gradient(135deg, #f59e0b, #d97706)', borderRadius: '50%', display: 'flex', alignItems: 'center', justifyContent: 'center', margin: '0 auto 1.5rem' }}>
                <FaHive style={{ fontSize: '2.5rem', color: 'white' }} />
              </div>
              <h3 className="card-title">Emily Rodriguez</h3>
              <p style={{ color: '#f59e0b', fontWeight: '500', marginBottom: '1rem', textAlign: 'center' }}>Head of Product</p>
              <p className="card-description">
                Product designer with expertise in IoT systems and user experience.
              </p>
            </div>
          </div>
        </div>
      </section>

      {/* CTA Section */}
      <section className="landing-section dark">
        <div className="landing-container">
          <div style={{ textAlign: 'center', maxWidth: '600px', margin: '0 auto' }}>
            <h2 className="landing-title" style={{ color: 'white', marginBottom: '1rem' }}>Ready to Join Our <span style={{ color: '#f59e0b' }}>Community</span>?</h2>
            <p className="landing-subtitle" style={{ color: '#cbd5e1', marginBottom: '2.5rem' }}>
              Start your journey with BeeHive Pro and experience the future of beekeeping.
            </p>
            <div style={{ display: 'flex', gap: '1rem', justifyContent: 'center' }}>
              <a href="/dashboard" className="landing-btn primary">
                <FaHive className="btn-icon" />
                <span>Start Free Trial</span>
              </a>
              <a href="/contact" className="landing-btn white">
                <span>Contact Us</span>
              </a>
            </div>
          </div>
        </div>
      </section>
    </LandingLayout>
  );
};

export default About;
  