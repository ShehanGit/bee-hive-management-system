import React from 'react';
import LandingNavbar from './LandingNavbar';
import './LandingLayout.css';

interface LandingLayoutProps {
  children: React.ReactNode;
  className?: string;
}

const LandingLayout: React.FC<LandingLayoutProps> = ({ children, className = '' }) => {
  return (
    <div className={`landing-layout ${className}`}>
      <LandingNavbar />
      <main className="landing-main">
        {children}
      </main>
    </div>
  );
};

export default LandingLayout;