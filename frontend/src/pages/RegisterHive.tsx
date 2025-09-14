import React, { useState, useEffect } from 'react';
import { useLocation, useNavigate } from 'react-router-dom';
import Navbar from '../components/Navbar';
import './RegisterHive.css';

interface PackageInfo {
  title: string;
  price: string;
}

interface FormData {
  fullName: string;
  displayName: string;
  phoneNumber: string;
  email: string;
  password: string;
  confirmPassword: string;
  company: string;
  country: string;
}

function RegisterHive() {
  const location = useLocation();
  const navigate = useNavigate();
  const packageInfo = location.state as PackageInfo;

  const [formData, setFormData] = useState<FormData>({
    fullName: '',
    displayName: '',
    phoneNumber: '',
    email: '',
    password: '',
    confirmPassword: '',
    company: '',
    country: ''
  });

  const [errors, setErrors] = useState<Partial<FormData>>({});
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [progress, setProgress] = useState(0);

  const countries = [
    'United Kingdom', 'United States', 'Canada', 'Australia', 'Germany', 
    'France', 'Netherlands', 'Belgium', 'Switzerland', 'Austria',
    'Ireland', 'Denmark', 'Sweden', 'Norway', 'Finland', 'Other'
  ];

  // Redirect to packages if no package info
  useEffect(() => {
    if (!packageInfo) {
      navigate('/packages');
    }
  }, [packageInfo, navigate]);

  // Calculate form completion progress
  useEffect(() => {
    const requiredFields = ['fullName', 'displayName', 'phoneNumber', 'email', 'password', 'confirmPassword', 'country'];
    const completedFields = requiredFields.filter(field => formData[field as keyof FormData]?.trim()).length;
    setProgress((completedFields / requiredFields.length) * 100);
  }, [formData]);

  const handleInputChange = (e: React.ChangeEvent<HTMLInputElement | HTMLSelectElement>) => {
    const { name, value } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: value
    }));

    // Clear error when user starts typing
    if (errors[name as keyof FormData]) {
      setErrors(prev => ({
        ...prev,
        [name]: ''
      }));
    }
  };

  const validateForm = (): boolean => {
    const newErrors: Partial<FormData> = {};

    if (!formData.fullName.trim()) {
      newErrors.fullName = 'Full name is required';
    }

    if (!formData.displayName.trim()) {
      newErrors.displayName = 'Display name is required';
    }

    if (!formData.phoneNumber.trim()) {
      newErrors.phoneNumber = 'Phone number is required';
    }

    if (!formData.email.trim()) {
      newErrors.email = 'Email is required';
    } else if (!/\S+@\S+\.\S+/.test(formData.email)) {
      newErrors.email = 'Email is invalid';
    }

    if (!formData.password) {
      newErrors.password = 'Password is required';
    } else if (formData.password.length < 6) {
      newErrors.password = 'Password must be at least 6 characters';
    }

    if (!formData.confirmPassword) {
      newErrors.confirmPassword = 'Please confirm your password';
    } else if (formData.password !== formData.confirmPassword) {
      newErrors.confirmPassword = 'Passwords do not match';
    }

    if (!formData.country) {
      newErrors.country = 'Please select a country';
    }

    setErrors(newErrors);
    return Object.keys(newErrors).length === 0;
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    
    if (!validateForm()) {
      return;
    }

    setIsSubmitting(true);

    try {
      // Prepare registration data
      const registrationData = {
        fullName: formData.fullName,
        displayName: formData.displayName,
        phoneNumber: formData.phoneNumber,
        email: formData.email,
        password: formData.password,
        company: formData.company,
        country: formData.country,
        packageTitle: packageInfo?.title,
        packagePrice: packageInfo?.price
      };

      // Send registration data to backend
      const response = await fetch('http://127.0.0.1:5001/api/hive-register', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(registrationData)
      });

      const result = await response.json();

      if (response.ok && result.success) {
        // Show success message
        alert(`🎉 Registration Successful!

Hi ${formData.fullName},

Thank you for choosing BeeSync!

Your registration for the ${packageInfo?.title} package has been completed successfully.

Emails have been sent automatically to both you and our support team.

Our team will contact you shortly at ${formData.email} to complete your subscription setup.

Welcome to the BeeSync family! 🐝`);
        
        // Redirect to packages page
        navigate('/packages');
      } else {
        // Show error message
        alert(`❌ Registration failed: ${result.message || 'Please try again.'}`);
      }

    } catch (error) {
      console.error('Registration error:', error);
      alert('❌ Registration failed. Please check your internet connection and try again.');
    } finally {
      setIsSubmitting(false);
    }
  };

  if (!packageInfo) {
    return null; // Will redirect via useEffect
  }

  return (
    <div className="register-hive">
      <Navbar />
      
      <div className="register-hive-container">
        <div className="register-hive-content">
          <header className="register-hive-header">
            <div className="header-icon">🐝</div>
            <h1>Register</h1>
            <div className="package-info-card">
              <div className="package-info-content">
                <h3>📦 Selected Package</h3>
                <p><strong>{packageInfo.title}</strong></p>
                <p className="price">{packageInfo.price}/month</p>
              </div>
              <div className="package-info-badge">
                <span>✨ Premium</span>
              </div>
            </div>
            
            {/* Progress Indicator */}
            <div className="progress-container">
              <div className="progress-label">
                <span>Form Completion</span>
                <span>{Math.round(progress)}%</span>
              </div>
              <div className="progress-bar">
                <div 
                  className="progress-fill"
                  style={{ width: `${progress}%` }}
                ></div>
              </div>
            </div>
          </header>

          <form className="register-hive-form" onSubmit={handleSubmit}>
            <div className="form-section">
              <h3 className="section-title">👤 Personal Information</h3>
              
              <div className="form-row">
                <div className="form-group">
                  <label htmlFor="fullName">Full Name</label>
                  <input
                    id="fullName"
                    type="text"
                    name="fullName"
                    placeholder="Enter your full name"
                    value={formData.fullName}
                    onChange={handleInputChange}
                    className={errors.fullName ? 'error' : ''}
                  />
                  {errors.fullName && <span className="error-message">{errors.fullName}</span>}
                </div>

                <div className="form-group">
                  <label htmlFor="displayName">Display Name</label>
                  <input
                    id="displayName"
                    type="text"
                    name="displayName"
                    placeholder="Enter your display name"
                    value={formData.displayName}
                    onChange={handleInputChange}
                    className={errors.displayName ? 'error' : ''}
                  />
                  {errors.displayName && <span className="error-message">{errors.displayName}</span>}
                </div>
              </div>

              <div className="form-row">
                <div className="form-group">
                  <label htmlFor="phoneNumber">Phone Number</label>
                  <input
                    id="phoneNumber"
                    type="tel"
                    name="phoneNumber"
                    placeholder="Enter your phone number"
                    value={formData.phoneNumber}
                    onChange={handleInputChange}
                    className={errors.phoneNumber ? 'error' : ''}
                  />
                  {errors.phoneNumber && <span className="error-message">{errors.phoneNumber}</span>}
                </div>

                <div className="form-group">
                  <label htmlFor="email">Email Address</label>
                  <input
                    id="email"
                    type="email"
                    name="email"
                    placeholder="Enter your email address"
                    value={formData.email}
                    onChange={handleInputChange}
                    className={errors.email ? 'error' : ''}
                  />
                  {errors.email && <span className="error-message">{errors.email}</span>}
                </div>
              </div>
            </div>

            <div className="form-section">
              <h3 className="section-title">🔒 Security Information</h3>
              
              <div className="form-row">
                <div className="form-group">
                  <label htmlFor="password">Password</label>
                  <input
                    id="password"
                    type="password"
                    name="password"
                    placeholder="Create a password"
                    value={formData.password}
                    onChange={handleInputChange}
                    className={errors.password ? 'error' : ''}
                  />
                  {errors.password && <span className="error-message">{errors.password}</span>}
                </div>

                <div className="form-group">
                  <label htmlFor="confirmPassword">Confirm Password</label>
                  <input
                    id="confirmPassword"
                    type="password"
                    name="confirmPassword"
                    placeholder="Confirm your password"
                    value={formData.confirmPassword}
                    onChange={handleInputChange}
                    className={errors.confirmPassword ? 'error' : ''}
                  />
                  {errors.confirmPassword && <span className="error-message">{errors.confirmPassword}</span>}
                </div>
              </div>
            </div>

            <div className="form-section">
              <h3 className="section-title">🏢 Additional Information</h3>
              
              <div className="form-row">
                <div className="form-group">
                  <label htmlFor="company">Company (Optional)</label>
                  <input
                    id="company"
                    type="text"
                    name="company"
                    placeholder="Enter your company name"
                    value={formData.company}
                    onChange={handleInputChange}
                  />
                </div>

                <div className="form-group">
                  <label htmlFor="country">Country</label>
                  <select
                    id="country"
                    name="country"
                    value={formData.country}
                    onChange={handleInputChange}
                    className={errors.country ? 'error' : ''}
                  >
                    <option value="">Select your country...</option>
                    {countries.map((country) => (
                      <option key={country} value={country}>
                        {country}
                      </option>
                    ))}
                  </select>
                  {errors.country && <span className="error-message">{errors.country}</span>}
                </div>
              </div>
            </div>

            <div className="form-actions">
              <button 
                type="submit" 
                className="register-hive-btn"
                disabled={isSubmitting}
              >
                {isSubmitting ? (
                  <>
                    <div className="loading-spinner"></div>
                    <span>Registering...</span>
                  </>
                ) : (
                  <>
                    <span>🚀</span>
                    <span>Register Now</span>
                  </>
                )}
              </button>
              
              <p className="terms-text">
                By registering, you agree to our Terms of Service and Privacy Policy
              </p>
            </div>
          </form>
        </div>
      </div>
    </div>
  );
}

export default RegisterHive;