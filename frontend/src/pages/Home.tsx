import React from 'react';
import { Link } from 'react-router-dom';
import Navbar from '../components/Navbar';
import './Home.css';

function Home() {
  return (
    <div className="home">
      <Navbar />

      {/* Hero Section */}
      <header className="hero-section">
        <div className="hero-overlay"></div>
        <div className="hero-content">
          <h1>Welcome to Bee Hive Management System</h1>
          <p>Effortlessly manage your hives with real-time data and insights.</p>
          <Link to="/packages" className="hero-btn">Get Started</Link>
        </div>
      </header>

      {/* Features Section */}
      <section className="features-section">
        <h2>Our Features</h2>
        <div className="features-container">
          <div className="feature-card">
            <div className="feature-icon">🐝</div>
            <h3>Hive Monitoring</h3>
            <p>Track hive health and activity with live updates.</p>
          </div>
          <div className="feature-card">
            <div className="feature-icon">📊</div>
            <h3>Detailed Analytics</h3>
            <p>Gain insights into honey production and hive performance.</p>
          </div>
          <div className="feature-card">
            <div className="feature-icon">🔔</div>
            <h3>Alerts & Notifications</h3>
            <p>Receive alerts for any critical changes in your hive status.</p>
          </div>
        </div>
      </section>

      {/* Testimonials Section */}
      <section className="testimonials-section">
        <h2>What Our Users Say</h2>
        <div className="testimonials-container">
          <div className="testimonial-card">
            <p>"This system transformed how I manage my hives. The live monitoring is a game-changer!"</p>
            <h4>- Alex, Beekeeper</h4>
          </div>
          <div className="testimonial-card">
            <p>"I love the detailed analytics—it really helps me optimize my production."</p>
            <h4>- Jamie, Honey Producer</h4>
          </div>
        </div>
      </section>

      {/* Footer Section */}
      <footer className="footer-section">
        <p>© {new Date().getFullYear()} Bee Hive Management. All Rights Reserved.</p>
      </footer>
    </div>
  );
}

export default Home;
