import React from 'react';
import { Link } from 'react-router-dom';
import circuitImage from '../assets/circuit-board.js';

const Home = () => {
  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
      {/* Hero Section */}
      <div className="hero-grid">
        <div className="hero-left">
          <h1 className="section-title">Smart Rent: The Future of Rental Properties</h1>
          <p className="subheadline">
            A decentralized rental platform powered by blockchain technology that brings transparency, 
            security, and efficiency to property rentals.
          </p>
          <div className="flex flex-wrap gap-4 mt-6">
            <Link to="/properties" className="btn-primary">
              Browse Properties
            </Link>
            <Link to="/register" className="btn-secondary">
              Create Account
            </Link>
          </div>
        </div>
        
        <div className="hero-right">
          <img 
            src={circuitImage} 
            alt="Digital circuit board representing blockchain technology" 
            className="rounded-xl shadow-lg w-full h-auto"
          />
        </div>
      </div>

      {/* Features Section */}
      <div className="py-section">
        <div className="text-center mb-16">
          <h2 className="section-title mb-4">Why Choose Smart Rent?</h2>
          <p className="subheadline mx-auto">
            Our platform combines blockchain technology with traditional rental processes
            to create a secure, efficient, and transparent rental experience.
          </p>
        </div>
        
        <div className="features-container">
          <div className="feature-item">
            <div className="flex justify-center mb-6">
              <div className="w-16 h-16 bg-primary/10 rounded-full flex items-center justify-center">
                <svg className="w-8 h-8 text-primary" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M9 12l2 2 4-4m5.618-4.016A11.955 11.955 0 0112 2.944a11.955 11.955 0 01-8.618 3.04A12.02 12.02 0 003 9c0 5.591 3.824 10.29 9 11.622 5.176-1.332 9-6.03 9-11.622 0-1.042-.133-2.052-.382-3.016z" />
                </svg>
              </div>
            </div>
            <h3 className="text-xl font-semibold mb-3">Secure Transactions</h3>
            <p className="text-secondary-text">
              All rental agreements are secured by blockchain technology, ensuring
              transparency and security for both landlords and tenants.
            </p>
          </div>

          <div className="feature-item">
            <div className="flex justify-center mb-6">
              <div className="w-16 h-16 bg-primary/10 rounded-full flex items-center justify-center">
                <svg className="w-8 h-8 text-primary" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M12 8c-1.657 0-3 .895-3 2s1.343 2 3 2 3 .895 3 2-1.343 2-3 2m0-8c1.11 0 2.08.402 2.599 1M12 8V7m0 1v8m0 0v1m0-1c-1.11 0-2.08-.402-2.599-1M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
                </svg>
              </div>
            </div>
            <h3 className="text-xl font-semibold mb-3">No Middlemen</h3>
            <p className="text-secondary-text">
              Deal directly with property owners without paying extra fees to 
              intermediaries, saving both time and money.
            </p>
          </div>

          <div className="feature-item">
            <div className="flex justify-center mb-6">
              <div className="w-16 h-16 bg-primary/10 rounded-full flex items-center justify-center">
                <svg className="w-8 h-8 text-primary" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
                </svg>
              </div>
            </div>
            <h3 className="text-xl font-semibold mb-3">Smart Contracts</h3>
            <p className="text-secondary-text">
              Automated rental agreements handle rent payments, security deposits,
              and dispute resolution with precision and reliability.
            </p>
          </div>
        </div>
      </div>

      {/* CTA Section */}
      <div className="bg-primary/5 py-16 px-4 sm:px-6 rounded-xl my-section">
        <div className="text-center max-w-3xl mx-auto">
          <h2 className="text-2xl font-bold mb-4">Ready to transform your rental experience?</h2>
          <p className="text-secondary-text mb-8">
            Join thousands of landlords and tenants who are already benefiting from our 
            blockchain-powered rental platform.
          </p>
          <Link to="/register" className="btn-primary">
            Get Started Today
          </Link>
        </div>
      </div>
    </div>
  );
};

export default Home; 