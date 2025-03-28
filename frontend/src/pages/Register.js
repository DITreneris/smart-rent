import React, { useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { useAuth } from '../contexts/AuthContext';
import WalletConnect from '../components/wallet/WalletConnect';

const Register = () => {
  const [formData, setFormData] = useState({
    email: '',
    password: '',
    confirmPassword: '',
    fullName: '',
    phone: '',
    walletAddress: '',
  });
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);
  const [step, setStep] = useState(1); // 1 = Personal info, 2 = Wallet connection
  
  const { register } = useAuth();
  const navigate = useNavigate();

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData((prev) => ({
      ...prev,
      [name]: value,
    }));
  };

  const handleWalletConnected = (walletData) => {
    setFormData((prev) => ({
      ...prev,
      walletAddress: walletData.address,
    }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    
    if (formData.password !== formData.confirmPassword) {
      return setError('Passwords do not match');
    }
    
    try {
      setError('');
      setLoading(true);
      
      const result = await register({
        email: formData.email,
        password: formData.password,
        full_name: formData.fullName,
        phone: formData.phone,
        wallet_address: formData.walletAddress,
      });
      
      if (result.success) {
        navigate('/dashboard');
      } else {
        setError(result.error || 'Failed to create an account. Please try again.');
      }
    } catch (err) {
      setError('An error occurred during registration. Please try again.');
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  const nextStep = () => {
    if (
      !formData.email || 
      !formData.password || 
      !formData.confirmPassword || 
      !formData.fullName
    ) {
      setError('Please fill in all required fields');
      return;
    }
    
    if (formData.password !== formData.confirmPassword) {
      setError('Passwords do not match');
      return;
    }
    
    setError('');
    setStep(2);
  };

  const prevStep = () => {
    setStep(1);
  };

  return (
    <div className="max-w-md mx-auto mt-10 mb-10">
      <div className="bg-white p-8 rounded-lg shadow-md">
        <h1 className="text-2xl font-bold text-center mb-6">Create an Account</h1>
        
        {error && (
          <div className="bg-red-100 border-l-4 border-red-500 text-red-700 p-4 mb-4" role="alert">
            <p>{error}</p>
          </div>
        )}
        
        {/* Progress indicator */}
        <div className="flex mb-8">
          <div className={`flex-1 text-center py-2 ${step === 1 ? 'bg-primary text-white' : 'bg-gray-200'}`}>
            Personal Info
          </div>
          <div className={`flex-1 text-center py-2 ${step === 2 ? 'bg-primary text-white' : 'bg-gray-200'}`}>
            Connect Wallet
          </div>
        </div>
        
        {step === 1 && (
          <form onSubmit={(e) => { e.preventDefault(); nextStep(); }}>
            <div className="mb-4">
              <label className="block text-gray-700 text-sm font-bold mb-2" htmlFor="fullName">
                Full Name
              </label>
              <input
                id="fullName"
                type="text"
                name="fullName"
                value={formData.fullName}
                onChange={handleChange}
                className="shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline"
                placeholder="Enter your full name"
                required
              />
            </div>
            
            <div className="mb-4">
              <label className="block text-gray-700 text-sm font-bold mb-2" htmlFor="email">
                Email Address
              </label>
              <input
                id="email"
                type="email"
                name="email"
                value={formData.email}
                onChange={handleChange}
                className="shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline"
                placeholder="Enter your email"
                required
              />
            </div>
            
            <div className="mb-4">
              <label className="block text-gray-700 text-sm font-bold mb-2" htmlFor="phone">
                Phone Number
              </label>
              <input
                id="phone"
                type="tel"
                name="phone"
                value={formData.phone}
                onChange={handleChange}
                className="shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline"
                placeholder="Enter your phone number"
              />
            </div>
            
            <div className="mb-4">
              <label className="block text-gray-700 text-sm font-bold mb-2" htmlFor="password">
                Password
              </label>
              <input
                id="password"
                type="password"
                name="password"
                value={formData.password}
                onChange={handleChange}
                className="shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline"
                placeholder="Create a password"
                required
                minLength="8"
              />
            </div>
            
            <div className="mb-6">
              <label className="block text-gray-700 text-sm font-bold mb-2" htmlFor="confirmPassword">
                Confirm Password
              </label>
              <input
                id="confirmPassword"
                type="password"
                name="confirmPassword"
                value={formData.confirmPassword}
                onChange={handleChange}
                className="shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline"
                placeholder="Confirm your password"
                required
                minLength="8"
              />
            </div>
            
            <div className="mb-6">
              <button
                type="submit"
                className="btn-primary w-full"
              >
                Next: Connect Wallet
              </button>
            </div>
          </form>
        )}
        
        {step === 2 && (
          <div>
            <div className="mb-6">
              <h3 className="text-lg font-semibold mb-4">Connect Your Crypto Wallet</h3>
              <p className="text-gray-600 mb-6">
                Connecting your wallet will allow you to make secure blockchain-based rental agreements and payments.
              </p>
              
              <WalletConnect onWalletConnected={handleWalletConnected} />
              
              {formData.walletAddress && (
                <div className="mt-4 p-3 bg-green-50 border border-green-200 rounded-md">
                  <p className="text-sm text-green-700">Wallet successfully connected!</p>
                </div>
              )}
            </div>
            
            <div className="flex gap-4 mt-8">
              <button
                onClick={prevStep}
                className="btn-secondary flex-1"
              >
                Back
              </button>
              
              <button
                onClick={handleSubmit}
                className={`btn-primary flex-1 ${loading ? 'opacity-70 cursor-not-allowed' : ''}`}
                disabled={loading}
              >
                {loading ? 'Creating Account...' : 'Create Account'}
              </button>
            </div>
            
            <div className="mt-3 text-xs text-gray-500 text-center">
              <p>You can also create an account without connecting a wallet now. You'll be able to connect later.</p>
            </div>
          </div>
        )}
        
        <hr className="my-6 border-gray-300" />
        
        <div className="text-center">
          <p className="text-gray-600">
            Already have an account?{' '}
            <Link to="/login" className="text-blue-600 hover:text-blue-800 font-semibold">
              Log In
            </Link>
          </p>
        </div>
      </div>
    </div>
  );
};

export default Register; 