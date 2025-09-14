import React, { useState } from 'react';
import LandingLayout from '../components/LandingLayout';
import { FaEnvelope, FaPhone, FaMapMarkerAlt, FaHive, FaPaperPlane } from 'react-icons/fa';

const Contact: React.FC = () => {
  const [formData, setFormData] = useState({
    name: '',
    email: '',
    subject: '',
    message: ''
  });

  const handleChange = (e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement>) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value
    });
  };

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    // Handle form submission here
    console.log('Form submitted:', formData);
    alert('Thank you for your message! We will get back to you soon.');
    setFormData({ name: '', email: '', subject: '', message: '' });
  };

  return (
    <LandingLayout>
      {/* Hero Section */}
      <section className="landing-section hero">
        <div className="landing-container">
          <div style={{ textAlign: 'center', maxWidth: '800px', margin: '0 auto' }}>
            <h1 className="landing-title">Get In <span className="landing-title highlight">Touch</span></h1>
            <p className="landing-subtitle">
              Have questions about BeeHive Pro? We're here to help!
            </p>
          </div>
        </div>
      </section>

      {/* Contact Section */}
      <section className="landing-section white">
        <div className="landing-container">
          <div className="hero-content">
            <div className="hero-text">
              <h2 className="landing-title" style={{ fontSize: '2.5rem', textAlign: 'left', marginBottom: '1rem' }}>Contact <span className="landing-title highlight">Information</span></h2>
              <p className="landing-description">
                Reach out to us through any of the channels below, and we'll get back to you as soon as possible.
              </p>
              
              <div style={{ display: 'flex', flexDirection: 'column', gap: '1.5rem', marginTop: '2rem' }}>
                <div style={{ display: 'flex', alignItems: 'flex-start', gap: '1rem', padding: '1.5rem', background: '#f8fafc', borderRadius: '12px', border: '1px solid #e2e8f0' }}>
                  <div style={{ width: '50px', height: '50px', background: 'linear-gradient(135deg, #f59e0b, #d97706)', borderRadius: '12px', display: 'flex', alignItems: 'center', justifyContent: 'center', fontSize: '1.25rem', color: 'white', flexShrink: 0 }}>
                    <FaEnvelope />
                  </div>
                  <div style={{ flex: 1 }}>
                    <h3 style={{ fontSize: '1.25rem', fontWeight: '600', color: '#1e293b', marginBottom: '0.5rem' }}>Email</h3>
                    <p style={{ color: '#64748b', fontSize: '0.95rem', lineHeight: '1.5', margin: '0 0 0.25rem 0' }}>support@beehivepro.com</p>
                    <p style={{ color: '#64748b', fontSize: '0.95rem', lineHeight: '1.5', margin: 0 }}>sales@beehivepro.com</p>
                  </div>
                </div>
                
                <div style={{ display: 'flex', alignItems: 'flex-start', gap: '1rem', padding: '1.5rem', background: '#f8fafc', borderRadius: '12px', border: '1px solid #e2e8f0' }}>
                  <div style={{ width: '50px', height: '50px', background: 'linear-gradient(135deg, #f59e0b, #d97706)', borderRadius: '12px', display: 'flex', alignItems: 'center', justifyContent: 'center', fontSize: '1.25rem', color: 'white', flexShrink: 0 }}>
                    <FaPhone />
                  </div>
                  <div style={{ flex: 1 }}>
                    <h3 style={{ fontSize: '1.25rem', fontWeight: '600', color: '#1e293b', marginBottom: '0.5rem' }}>Phone</h3>
                    <p style={{ color: '#64748b', fontSize: '0.95rem', lineHeight: '1.5', margin: '0 0 0.25rem 0' }}>+1 (555) 123-4567</p>
                    <p style={{ color: '#64748b', fontSize: '0.95rem', lineHeight: '1.5', margin: 0 }}>Mon-Fri 9AM-6PM EST</p>
                  </div>
                </div>
                
                <div style={{ display: 'flex', alignItems: 'flex-start', gap: '1rem', padding: '1.5rem', background: '#f8fafc', borderRadius: '12px', border: '1px solid #e2e8f0' }}>
                  <div style={{ width: '50px', height: '50px', background: 'linear-gradient(135deg, #f59e0b, #d97706)', borderRadius: '12px', display: 'flex', alignItems: 'center', justifyContent: 'center', fontSize: '1.25rem', color: 'white', flexShrink: 0 }}>
                    <FaMapMarkerAlt />
                  </div>
                  <div style={{ flex: 1 }}>
                    <h3 style={{ fontSize: '1.25rem', fontWeight: '600', color: '#1e293b', marginBottom: '0.5rem' }}>Address</h3>
                    <p style={{ color: '#64748b', fontSize: '0.95rem', lineHeight: '1.5', margin: '0 0 0.25rem 0' }}>123 Hive Street</p>
                    <p style={{ color: '#64748b', fontSize: '0.95rem', lineHeight: '1.5', margin: 0 }}>Beekeeping City, BC 12345</p>
                  </div>
                </div>
              </div>
            </div>

            <div style={{ background: '#f8fafc', padding: '2rem', borderRadius: '16px', border: '1px solid #e2e8f0' }}>
              <h2 className="landing-title" style={{ fontSize: '2.5rem', textAlign: 'left', marginBottom: '1.5rem' }}>Send us a <span className="landing-title highlight">Message</span></h2>
              <form style={{ display: 'flex', flexDirection: 'column', gap: '1.5rem' }} onSubmit={handleSubmit}>
                <div style={{ display: 'flex', flexDirection: 'column', gap: '0.5rem' }}>
                  <label htmlFor="name" style={{ fontWeight: '600', color: '#374151', fontSize: '0.95rem' }}>Name</label>
                  <input
                    type="text"
                    id="name"
                    name="name"
                    value={formData.name}
                    onChange={handleChange}
                    style={{ padding: '0.75rem 1rem', border: '2px solid #e5e7eb', borderRadius: '8px', fontSize: '1rem', transition: 'all 0.3s ease', background: 'white' }}
                    required
                  />
                </div>
                
                <div style={{ display: 'flex', flexDirection: 'column', gap: '0.5rem' }}>
                  <label htmlFor="email" style={{ fontWeight: '600', color: '#374151', fontSize: '0.95rem' }}>Email</label>
                  <input
                    type="email"
                    id="email"
                    name="email"
                    value={formData.email}
                    onChange={handleChange}
                    style={{ padding: '0.75rem 1rem', border: '2px solid #e5e7eb', borderRadius: '8px', fontSize: '1rem', transition: 'all 0.3s ease', background: 'white' }}
                    required
                  />
                </div>
                
                <div style={{ display: 'flex', flexDirection: 'column', gap: '0.5rem' }}>
                  <label htmlFor="subject" style={{ fontWeight: '600', color: '#374151', fontSize: '0.95rem' }}>Subject</label>
                  <input
                    type="text"
                    id="subject"
                    name="subject"
                    value={formData.subject}
                    onChange={handleChange}
                    style={{ padding: '0.75rem 1rem', border: '2px solid #e5e7eb', borderRadius: '8px', fontSize: '1rem', transition: 'all 0.3s ease', background: 'white' }}
                    required
                  />
                </div>
                
                <div style={{ display: 'flex', flexDirection: 'column', gap: '0.5rem' }}>
                  <label htmlFor="message" style={{ fontWeight: '600', color: '#374151', fontSize: '0.95rem' }}>Message</label>
                  <textarea
                    id="message"
                    name="message"
                    value={formData.message}
                    onChange={handleChange}
                    style={{ padding: '0.75rem 1rem', border: '2px solid #e5e7eb', borderRadius: '8px', fontSize: '1rem', transition: 'all 0.3s ease', background: 'white', resize: 'vertical', minHeight: '120px' }}
                    rows={5}
                    required
                  />
                </div>
                
                <button type="submit" className="landing-btn primary" style={{ marginTop: '1rem' }}>
                  <FaPaperPlane className="btn-icon" />
                  <span>Send Message</span>
                </button>
              </form>
            </div>
          </div>
        </div>
      </section>

      {/* FAQ Section */}
      <section className="landing-section gray">
        <div className="landing-container">
          <h2 className="landing-title">Frequently Asked <span className="landing-title highlight">Questions</span></h2>
          <div className="landing-grid two">
            <div className="landing-card">
              <h3 style={{ fontSize: '1.25rem', fontWeight: '600', color: '#1e293b', marginBottom: '1rem', display: 'flex', alignItems: 'center', gap: '0.75rem' }}>
                <span style={{ width: '30px', height: '30px', background: 'linear-gradient(135deg, #f59e0b, #d97706)', color: 'white', borderRadius: '50%', display: 'flex', alignItems: 'center', justifyContent: 'center', fontWeight: '700', fontSize: '0.9rem', flexShrink: 0 }}>?</span>
                How does BeeHive Pro work?
              </h3>
              <p style={{ color: '#64748b', lineHeight: '1.6', paddingLeft: '2.5rem' }}>
                BeeHive Pro uses IoT sensors to monitor your hives 24/7. The data is analyzed by our AI system 
                to provide health insights, threat detection, and optimization recommendations.
              </p>
            </div>
            
            <div className="landing-card">
              <h3 style={{ fontSize: '1.25rem', fontWeight: '600', color: '#1e293b', marginBottom: '1rem', display: 'flex', alignItems: 'center', gap: '0.75rem' }}>
                <span style={{ width: '30px', height: '30px', background: 'linear-gradient(135deg, #f59e0b, #d97706)', color: 'white', borderRadius: '50%', display: 'flex', alignItems: 'center', justifyContent: 'center', fontWeight: '700', fontSize: '0.9rem', flexShrink: 0 }}>?</span>
                What sensors are included?
              </h3>
              <p style={{ color: '#64748b', lineHeight: '1.6', paddingLeft: '2.5rem' }}>
                Each hive monitoring kit includes temperature, humidity, weight, and sound sensors. 
                Additional sensors for air quality and weather monitoring are available as add-ons.
              </p>
            </div>
            
            <div className="landing-card">
              <h3 style={{ fontSize: '1.25rem', fontWeight: '600', color: '#1e293b', marginBottom: '1rem', display: 'flex', alignItems: 'center', gap: '0.75rem' }}>
                <span style={{ width: '30px', height: '30px', background: 'linear-gradient(135deg, #f59e0b, #d97706)', color: 'white', borderRadius: '50%', display: 'flex', alignItems: 'center', justifyContent: 'center', fontWeight: '700', fontSize: '0.9rem', flexShrink: 0 }}>?</span>
                Is there a mobile app?
              </h3>
              <p style={{ color: '#64748b', lineHeight: '1.6', paddingLeft: '2.5rem' }}>
                Yes! Our mobile app is available for both iOS and Android, allowing you to monitor 
                your hives from anywhere and receive instant alerts.
              </p>
            </div>
            
            <div className="landing-card">
              <h3 style={{ fontSize: '1.25rem', fontWeight: '600', color: '#1e293b', marginBottom: '1rem', display: 'flex', alignItems: 'center', gap: '0.75rem' }}>
                <span style={{ width: '30px', height: '30px', background: 'linear-gradient(135deg, #f59e0b, #d97706)', color: 'white', borderRadius: '50%', display: 'flex', alignItems: 'center', justifyContent: 'center', fontWeight: '700', fontSize: '0.9rem', flexShrink: 0 }}>?</span>
                What's included in the free trial?
              </h3>
              <p style={{ color: '#64748b', lineHeight: '1.6', paddingLeft: '2.5rem' }}>
                The free trial includes access to all dashboard features, basic monitoring for up to 3 hives, 
                and email alerts. Premium features like AI health analysis require a subscription.
              </p>
            </div>
          </div>
        </div>
      </section>
    </LandingLayout>
  );
};

export default Contact;
