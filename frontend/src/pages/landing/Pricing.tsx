import React from 'react';
import LandingNavbar from '../../components/LandingNavbar';
import './Pricing.css';

const Pricing: React.FC = () => {
  return (
    <div className="landing-pricing">
      <LandingNavbar />
      
      {/* Hero Section */}
      <section className="pricing-hero">
        <div className="container">
          <h1>Simple, Transparent Pricing</h1>
          <p className="hero-subtitle">Choose the plan that's right for your operation</p>
        </div>
      </section>

      {/* Pricing Tiers */}
      <section className="pricing-section">
        <div className="container">
          <div className="pricing-grid">
            {/* Starter Plan */}
            <div className="pricing-card">
              <div className="plan-badge">Basic</div>
              <div className="plan-header">
                <h3>Starter</h3>
                <div className="plan-price">
                  <span className="currency">$</span>
                  <span className="amount">29</span>
                  <span className="period">/month</span>
                </div>
                <p className="plan-description">Perfect for hobbyist beekeepers</p>
              </div>
              
              <ul className="plan-features">
                <li><span className="check-icon">✓</span> Up to 5 hives</li>
                <li><span className="check-icon">✓</span> Real-time monitoring</li>
                <li><span className="check-icon">✓</span> Basic alerts</li>
                <li><span className="check-icon">✓</span> Weather integration</li>
                <li><span className="check-icon">✓</span> Mobile dashboard</li>
                <li><span className="check-icon">✓</span> Email support</li>
              </ul>
              
              <a href="/dashboard" className="btn btn-outline">Start Free Trial</a>
            </div>

            {/* Pro Plan - Featured */}
            <div className="pricing-card featured">
              <div className="plan-badge popular">Most Popular</div>
              <div className="plan-header">
                <h3>Professional</h3>
                <div className="plan-price">
                  <span className="currency">$</span>
                  <span className="amount">79</span>
                  <span className="period">/month</span>
                </div>
                <p className="plan-description">For serious beekeepers and small operations</p>
              </div>
              
              <ul className="plan-features">
                <li><span className="check-icon">✓</span> Up to 25 hives</li>
                <li><span className="check-icon">✓</span> AI threat detection</li>
                <li><span className="check-icon">✓</span> Performance prediction</li>
                <li><span className="check-icon">✓</span> Advanced analytics</li>
                <li><span className="check-icon">✓</span> Optimal placement AI</li>
                <li><span className="check-icon">✓</span> Priority support</li>
                <li><span className="check-icon">✓</span> Historical data (1 year)</li>
              </ul>
              
              <a href="/dashboard" className="btn btn-primary">Start Free Trial</a>
            </div>

            {/* Enterprise Plan */}
            <div className="pricing-card">
              <div className="plan-badge">Enterprise</div>
              <div className="plan-header">
                <h3>Enterprise</h3>
                <div className="plan-price">
                  <span className="currency">$</span>
                  <span className="amount">199</span>
                  <span className="period">/month</span>
                </div>
                <p className="plan-description">For commercial apiaries and large operations</p>
              </div>
              
              <ul className="plan-features">
                <li><span className="check-icon">✓</span> Unlimited hives</li>
                <li><span className="check-icon">✓</span> All Pro features</li>
                <li><span className="check-icon">✓</span> Custom integrations</li>
                <li><span className="check-icon">✓</span> API access</li>
                <li><span className="check-icon">✓</span> Advanced reporting</li>
                <li><span className="check-icon">✓</span> 24/7 phone support</li>
                <li><span className="check-icon">✓</span> Dedicated account manager</li>
                <li><span className="check-icon">✓</span> On-site training</li>
              </ul>
              
              <a href="/landing/contact" className="btn btn-outline">Contact Sales</a>
            </div>
          </div>
        </div>
      </section>

      {/* Features Comparison */}
      <section className="features-comparison">
        <div className="container">
          <h2>Compare Plans</h2>
          <div className="comparison-table">
            <table>
              <thead>
                <tr>
                  <th>Feature</th>
                  <th>Starter</th>
                  <th>Professional</th>
                  <th>Enterprise</th>
                </tr>
              </thead>
              <tbody>
                <tr>
                  <td>Number of Hives</td>
                  <td>5</td>
                  <td>25</td>
                  <td>Unlimited</td>
                </tr>
                <tr>
                  <td>Real-time Monitoring</td>
                  <td>✓</td>
                  <td>✓</td>
                  <td>✓</td>
                </tr>
                <tr>
                  <td>AI Threat Detection</td>
                  <td>-</td>
                  <td>✓</td>
                  <td>✓</td>
                </tr>
                <tr>
                  <td>Performance Prediction</td>
                  <td>-</td>
                  <td>✓</td>
                  <td>✓</td>
                </tr>
                <tr>
                  <td>Optimal Placement AI</td>
                  <td>-</td>
                  <td>✓</td>
                  <td>✓</td>
                </tr>
                <tr>
                  <td>Historical Data</td>
                  <td>30 days</td>
                  <td>1 year</td>
                  <td>Unlimited</td>
                </tr>
                <tr>
                  <td>Support</td>
                  <td>Email</td>
                  <td>Priority</td>
                  <td>24/7 Phone</td>
                </tr>
                <tr>
                  <td>API Access</td>
                  <td>-</td>
                  <td>-</td>
                  <td>✓</td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>
      </section>

      {/* FAQ Section */}
      <section className="pricing-faq">
        <div className="container">
          <h2>Frequently Asked Questions</h2>
          <div className="faq-grid">
            <div className="faq-item">
              <h3>Is there a free trial?</h3>
              <p>Yes! All plans include a 14-day free trial. No credit card required.</p>
            </div>
            
            <div className="faq-item">
              <h3>Can I upgrade or downgrade later?</h3>
              <p>Absolutely! You can change your plan at any time. Changes take effect immediately.</p>
            </div>
            
            <div className="faq-item">
              <h3>What payment methods do you accept?</h3>
              <p>We accept all major credit cards, PayPal, and bank transfers for Enterprise plans.</p>
            </div>
            
            <div className="faq-item">
              <h3>Do you offer refunds?</h3>
              <p>Yes, we offer a 30-day money-back guarantee on all annual subscriptions.</p>
            </div>
          </div>
        </div>
      </section>

      {/* CTA Section */}
      <section className="pricing-cta">
        <div className="container">
          <h2>Still not sure?</h2>
          <p>Try all features free for 14 days. No credit card required.</p>
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

export default Pricing;

