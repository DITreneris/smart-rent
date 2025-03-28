import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { useAuth } from '../../contexts/AuthContext';
import { useWeb3 } from '../../contexts/Web3Context';
import axios from 'axios';

const ContractForm = ({ propertyId, propertyDetails }) => {
  const [formData, setFormData] = useState({
    startDate: '',
    endDate: '',
    monthlyRent: propertyDetails?.price || 0,
    securityDeposit: (propertyDetails?.price || 0) * 2,
  });
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [success, setSuccess] = useState('');
  
  const { token } = useAuth();
  const { isConnected, connectWallet } = useWeb3();
  const navigate = useNavigate();

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData({
      ...formData,
      [name]: value,
    });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    
    if (!isConnected) {
      setError('Please connect your wallet before creating a contract');
      return;
    }
    
    setLoading(true);
    setError('');
    
    try {
      // Convert dates to timestamps
      const startDate = new Date(formData.startDate).getTime() / 1000;
      const endDate = new Date(formData.endDate).getTime() / 1000;
      
      // Create contract in the backend
      const response = await axios.post(
        `${process.env.REACT_APP_API_URL}/api/v1/contracts`,
        {
          property_id: propertyId,
          start_date: new Date(formData.startDate).toISOString(),
          end_date: new Date(formData.endDate).toISOString(),
          monthly_rent: Number(formData.monthlyRent),
          security_deposit: Number(formData.securityDeposit),
        },
        {
          headers: { Authorization: `Bearer ${token}` },
        }
      );
      
      setSuccess('Rental request submitted successfully! The landlord will be notified.');
      
      // Redirect to contracts list after a delay
      setTimeout(() => {
        navigate('/dashboard');
      }, 3000);
    } catch (err) {
      console.error('Error creating contract:', err);
      setError(err.response?.data?.detail || 'Failed to create contract. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="bg-white shadow sm:rounded-lg p-6">
      <h2 className="text-xl font-semibold mb-6">Request to Rent This Property</h2>
      
      {!isConnected && (
        <div className="mb-6 bg-yellow-50 p-4 rounded-md">
          <div className="flex">
            <div className="flex-shrink-0">
              <svg className="h-5 w-5 text-yellow-400" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="currentColor">
                <path fillRule="evenodd" d="M8.257 3.099c.765-1.36 2.722-1.36 3.486 0l5.58 9.92c.75 1.334-.213 2.98-1.742 2.98H4.42c-1.53 0-2.493-1.646-1.743-2.98l5.58-9.92zM11 13a1 1 0 11-2 0 1 1 0 012 0zm-1-8a1 1 0 00-1 1v3a1 1 0 002 0V6a1 1 0 00-1-1z" clipRule="evenodd" />
              </svg>
            </div>
            <div className="ml-3">
              <h3 className="text-sm font-medium text-yellow-800">Wallet Connection Required</h3>
              <div className="mt-2 text-sm text-yellow-700">
                <p>To create a rental contract, you need to connect your crypto wallet first.</p>
              </div>
              <div className="mt-4">
                <button
                  type="button"
                  onClick={connectWallet}
                  className="inline-flex items-center px-4 py-2 border border-transparent text-sm font-medium rounded-md shadow-sm text-white bg-primary-600 hover:bg-primary-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-primary-500"
                >
                  Connect Wallet
                </button>
              </div>
            </div>
          </div>
        </div>
      )}
      
      {error && (
        <div className="mb-4 p-4 text-red-700 bg-red-100 rounded-md">
          {error}
        </div>
      )}
      
      {success && (
        <div className="mb-4 p-4 text-green-700 bg-green-100 rounded-md">
          {success}
        </div>
      )}
      
      <form onSubmit={handleSubmit} className="space-y-6">
        <div>
          <label htmlFor="startDate" className="block text-sm font-medium text-gray-700">
            Start Date
          </label>
          <input
            type="date"
            id="startDate"
            name="startDate"
            required
            value={formData.startDate}
            onChange={handleChange}
            className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-primary-500 focus:ring-primary-500 sm:text-sm"
          />
        </div>
        
        <div>
          <label htmlFor="endDate" className="block text-sm font-medium text-gray-700">
            End Date
          </label>
          <input
            type="date"
            id="endDate"
            name="endDate"
            required
            value={formData.endDate}
            onChange={handleChange}
            className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-primary-500 focus:ring-primary-500 sm:text-sm"
          />
        </div>
        
        <div>
          <label htmlFor="monthlyRent" className="block text-sm font-medium text-gray-700">
            Monthly Rent (in cents)
          </label>
          <input
            type="number"
            id="monthlyRent"
            name="monthlyRent"
            required
            value={formData.monthlyRent}
            onChange={handleChange}
            className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-primary-500 focus:ring-primary-500 sm:text-sm"
          />
          <p className="mt-1 text-sm text-gray-500">
            ${(formData.monthlyRent / 100).toFixed(2)}/month
          </p>
        </div>
        
        <div>
          <label htmlFor="securityDeposit" className="block text-sm font-medium text-gray-700">
            Security Deposit (in cents)
          </label>
          <input
            type="number"
            id="securityDeposit"
            name="securityDeposit"
            required
            value={formData.securityDeposit}
            onChange={handleChange}
            className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-primary-500 focus:ring-primary-500 sm:text-sm"
          />
          <p className="mt-1 text-sm text-gray-500">
            ${(formData.securityDeposit / 100).toFixed(2)}
          </p>
        </div>
        
        <div className="flex items-center justify-between pt-4">
          <button
            type="button"
            onClick={() => navigate(-1)}
            className="inline-flex justify-center py-2 px-4 border border-gray-300 shadow-sm text-sm font-medium rounded-md text-gray-700 bg-white hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-primary-500"
          >
            Cancel
          </button>
          <button
            type="submit"
            disabled={loading || !isConnected}
            className="inline-flex justify-center py-2 px-4 border border-transparent shadow-sm text-sm font-medium rounded-md text-white bg-primary-600 hover:bg-primary-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-primary-500 disabled:opacity-50"
          >
            {loading ? 'Creating Contract...' : 'Create Rental Contract'}
          </button>
        </div>
      </form>
    </div>
  );
};

export default ContractForm; 