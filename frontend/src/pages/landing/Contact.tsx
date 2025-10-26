import React, { useState } from 'react';
import LandingNavbar from '../../components/LandingNavbar';
import './Contact.css';

const Contact: React.FC = () => {
  const [formData, setFormData] = useState({
    name: '',
    email: '',
    subject: '',
    message: ''
  });

  const handleChange = (e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement | HTMLSelectElement>) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value
    });
  };

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    // Here you would typically send the form data to your backend
    console.log('Form submitted:', formData);
    alert('Thank you for your message! We will get back to you soon.');
    setFormData({ name: '', email: '', subject: '', message: '' });
  };

  return (
    <div className="landing-contact">
      <LandingNavbar />
      
      {/* Hero Section */}
      <section className="contact-hero">
        <div className="container">
          <h1>Get in Touch</h1>
          <p className="hero-subtitle">We'd love to hear from you. Send us a message and we'll respond as soon as possible.</p>
        </div>
      </section>

      {/* Contact Section */}
      <section className="contact-section">
        <div className="container">
          <div className="contact-grid">
            {/* Contact Info */}
            <div className="contact-info">
              <h2>Contact Information</h2>
              <p className="contact-intro">Have questions? We're here to help! Reach out through any of the channels below.</p>
              
              <div className="contact-item">
                <div className="contact-icon">📧</div>
                <div className="contact-details">
                  <h3>Email Us</h3>
                  <p>support@beehivepro.com</p>
                  <p>sales@beehivepro.com</p>
                </div>
              </div>
              
              <div className="contact-item">
                <div className="contact-icon">📞</div>
                <div className="contact-details">
                  <h3>Call Us</h3>
                  <p>+1 (555) 123-4567</p>
                  <p>Mon-Fri 9am-6pm EST</p>
                </div>
              </div>
              
              <div className="contact-item">
                <div className="contact-icon">📍</div>
                <div className="contact-details">
                  <h3>Visit Us</h3>
                  <p>123 Apiary Road</p>
                  <p>Honeyville, Bee State 12345</p>
                </div>
              </div>
            </div>

            {/* Contact Form */}
            <div className="contact-form-container">
              <h2>Send us a Message</h2>
              <form onSubmit={handleSubmit} className="contact-form">
                <div className="form-group">
                  <label htmlFor="name">Full Name</label>
                  <input
                    type="text"
                    id="name"
                    name="name"
                    value={formData.name}
                    onChange={handleChange}
                    required
                    placeholder="John Doe"
                  />
                </div>
                
                <div className="form-group">
                  <label htmlFor="email">Email Address</label>
                  <input
                    type="email"
                    id="email"
                    name="email"
                    value={formData.email}
                    onChange={handleChange}
                    required
                    placeholder="john@example.com"
                  />
                </div>
                
                <div className="form-group">
                  <label htmlFor="subject">Subject</label>
                  <select
                    id="subject"
                    name="subject"
                    value={formData.subject}
                    onChange={handleChange}
                    required
                  >
                    <option value="">Select a subject</option>
                    <option value="general">General Inquiry</option>
                    <option value="support">Technical Support</option>
                    <option value="sales">Sales Question</option>
                    <option value="feature">Feature Request</option>
                    <option value="other">Other</option>
                  </select>
                </div>
                
                <div className="form-group">
                  <label htmlFor="message">Message</label>
                  <textarea
                    id="message"
                    name="message"
                    value={formData.message}
                    onChange={handleChange}
                    required
                    rows={6}
                    placeholder="Tell us how we can help..."
                  />
                </div>
                
                <button type="submit" className="btn btn-primary btn-full">
                  Send Message
                </button>
              </form>
            </div>
          </div>
        </div>
      </section>

      {/* Social Media Section */}
      <section className="social-section">
        <div className="container">
          <h2>Follow Us</h2>
          <p>Stay connected with us on social media for updates, tips, and community discussions.</p>
          <div className="social-links">
            <a href="#" className="social-link">
              <span>📘</span>
              <span>Facebook</span>
            </a>
            <a href="#" className="social-link">
              <span>🐦</span>
              <span>Twitter</span>
            </a>
            <a href="#" className="social-link">
              <span>📸</span>
              <span>Instagram</span>
            </a>
            <a href="#" className="social-link">
              <span>💼</span>
              <span>LinkedIn</span>
            </a>
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

export default Contact;

