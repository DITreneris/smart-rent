import React, { useMemo, useCallback, useState } from 'react';
import { useWeb3 } from '../../contexts/Web3Context';
import { Link } from 'react-router-dom';
import { FaHome, FaCreditCard, FaEthereum, FaFileAlt, FaSearch, FaFileContract, FaCalendarAlt, FaFileInvoiceDollar } from 'react-icons/fa';

// Memoized StatCard component to prevent unnecessary re-renders
const StatCard = React.memo(({ icon: Icon, title, value, bgColor, iconColor }) => (
  <div className="bg-white rounded-lg shadow-md p-4">
    <div className="flex items-center">
      <div className={`flex-shrink-0 rounded-full p-3 ${bgColor}`}>
        <Icon className={`h-5 w-5 ${iconColor}`} />
      </div>
      <div className="ml-4">
        <h2 className="text-sm font-medium text-gray-500">{title}</h2>
        <p className="text-lg font-semibold text-gray-800">{value}</p>
      </div>
    </div>
  </div>
));

// Memoized PaymentHistoryItem component to prevent unnecessary re-renders
const PaymentHistoryItem = React.memo(({ payment }) => (
  <tr>
    <td className="px-6 py-4 whitespace-nowrap">
      <span className="text-sm text-gray-900">{payment.date}</span>
    </td>
    <td className="px-6 py-4 whitespace-nowrap">
      <span className="text-sm text-gray-900">{payment.amount} ETH</span>
    </td>
    <td className="px-6 py-4 whitespace-nowrap">
      <span className="text-sm text-gray-900">{payment.description}</span>
    </td>
    <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
      <a 
        href={`https://etherscan.io/tx/${payment.txHash}`} 
        target="_blank" 
        rel="noopener noreferrer"
        className="text-indigo-600 hover:text-indigo-900"
      >
        {payment.txHash.substring(0, 10)}...
      </a>
    </td>
    <td className="px-6 py-4 whitespace-nowrap">
      <span className={`px-2 py-1 inline-flex text-xs leading-5 font-semibold rounded-full ${
        payment.status === 'Completed' ? 'bg-green-100 text-green-800' : 'bg-yellow-100 text-yellow-800'
      }`}>
        {payment.status}
      </span>
    </td>
  </tr>
));

// Virtualized list for payment history
const VirtualizedPaymentHistory = React.memo(({ payments }) => {
  // In a real app, this would use react-window or react-virtualized
  // This is a simplified version for demonstration
  const [visibleRange, setVisibleRange] = useState({ start: 0, end: 5 });
  
  // Get only the payments that are currently visible
  const visiblePayments = useMemo(() => {
    return payments.slice(visibleRange.start, visibleRange.end);
  }, [payments, visibleRange]);
  
  return (
    <tbody className="bg-white divide-y divide-gray-200">
      {visiblePayments.map((payment, index) => (
        <PaymentHistoryItem key={payment.txHash || index} payment={payment} />
      ))}
      {payments.length > visibleRange.end && (
        <tr>
          <td colSpan="5" className="px-6 py-4 text-center">
            <button 
              onClick={() => setVisibleRange(prev => ({ 
                start: prev.start, 
                end: Math.min(prev.end + 5, payments.length) 
              }))}
              className="text-indigo-600 hover:text-indigo-900"
            >
              Load more
            </button>
          </td>
        </tr>
      )}
    </tbody>
  );
});

// Current Rental Card component - memoized to prevent unnecessary re-renders
const CurrentRentalCard = React.memo(({ rental, formatAddress, daysUntilNextPayment }) => (
  <div className="bg-white rounded-lg shadow-md overflow-hidden">
    <div className="md:flex">
      <div className="md:flex-shrink-0">
        <img 
          className="h-48 w-full object-cover md:w-48" 
          src={rental.imageUrl} 
          alt={rental.title} 
          loading="lazy"
        />
      </div>
      <div className="p-8">
        <div className="block mt-1 text-lg leading-tight font-medium text-black">{rental.title}</div>
        <p className="mt-2 text-gray-600">{rental.address}</p>
        <div className="mt-4 grid grid-cols-1 gap-4">
          <div>
            <span className="text-gray-500">Landlord:</span>
            <span className="ml-2">{formatAddress(rental.landlord)}</span>
          </div>
          <div>
            <span className="text-gray-500">Rental Period:</span>
            <span className="ml-2">{rental.rentalPeriod}</span>
          </div>
          <div>
            <span className="text-gray-500">Monthly Rent:</span>
            <span className="ml-2">{rental.monthlyRent} ETH</span>
          </div>
          <div>
            <span className="text-gray-500">Security Deposit:</span>
            <span className="ml-2">{rental.securityDeposit} ETH</span>
          </div>
          <div>
            <span className="text-gray-500">Next Payment:</span>
            <span className="ml-2">{rental.nextPaymentDate} ({daysUntilNextPayment} days)</span>
          </div>
        </div>
        <div className="mt-6">
          <button className="bg-blue-600 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded">
            Make Payment
          </button>
        </div>
      </div>
    </div>
  </div>
));

// Agreement card component - memoized to prevent unnecessary re-renders
const AgreementCard = React.memo(({ agreement, index, formatAddress }) => (
  <div className="border border-gray-200 rounded-lg p-4">
    <div className="flex justify-between items-start">
      <div>
        <h3 className="font-medium">Agreement #{agreement.id || index + 1}</h3>
        <p className="text-sm text-gray-600">Landlord: {formatAddress(agreement.landlord || "0x0")}</p>
        <p className="text-sm text-gray-600">
          Rent: {agreement.rent || "0"} ETH | Security Deposit: {agreement.securityDeposit || "0"} ETH
        </p>
      </div>
      <span className={`px-2 py-1 text-xs rounded-full ${
        agreement.active ? 'bg-green-100 text-green-800' : 'bg-red-100 text-red-800'
      }`}>
        {agreement.active ? 'Active' : 'Terminated'}
      </span>
    </div>
  </div>
));

const TenantDashboard = () => {
  const { 
    tenantAgreements,
    balance,
    formatAddress
  } = useWeb3();
  
  // Mock data for tenant's current rental - in production this would come from an API
  const currentRental = useMemo(() => ({
    id: 1,
    title: 'Modern Studio Apartment',
    address: '789 Tenant Lane, Cityville',
    landlord: '0x8ba1f109551bD432803012645Ac136ddd64DBA72',
    rentalPeriod: 'Jan 1, 2023 - Dec 31, 2023',
    monthlyRent: 0.5,
    securityDeposit: 1,
    nextPaymentDate: 'Oct 1, 2023',
    imageUrl: 'https://images.unsplash.com/photo-1522708323590-d24dbb6b0267?w=500'
  }), []);
  
  // Mock payment history data - in production this would come from an API or blockchain
  const paymentHistory = useMemo(() => [
    { date: 'Sep 1, 2023', amount: 0.5, description: 'Monthly Rent', txHash: '0x8b7989435b9323244e83fcb25d4140d9f6dd8d4ba46b3a8f6b4e76a2148aa50f', status: 'Completed' },
    { date: 'Aug 1, 2023', amount: 0.5, description: 'Monthly Rent', txHash: '0x9a4988995b93232d9e83fcb25d4140d9f6dd8d4ba46b3a8f6b4e76a2148bb61a', status: 'Completed' },
    { date: 'Jul 1, 2023', amount: 0.5, description: 'Monthly Rent', txHash: '0x7c6977775b93232d9e83fcb25d4140d9f6dd8d4ba46b3a8f6b4e76a2148cc72b', status: 'Completed' },
    { date: 'Jun 1, 2023', amount: 0.5, description: 'Monthly Rent', txHash: '0x6d5866665b93232d9e83fcb25d4140d9f6dd8d4ba46b3a8f6b4e76a2148dd83c', status: 'Completed' },
    { date: 'May 1, 2023', amount: 0.5, description: 'Monthly Rent', txHash: '0x5e4755555b93232d9e83fcb25d4140d9f6dd8d4ba46b3a8f6b4e76a2148ee94d', status: 'Completed' },
    { date: 'Apr 1, 2023', amount: 0.5, description: 'Monthly Rent', txHash: '0x4f3644445b93232d9e83fcb25d4140d9f6dd8d4ba46b3a8f6b4e76a2148ff05e', status: 'Completed' },
    { date: 'Mar 1, 2023', amount: 0.5, description: 'Monthly Rent', txHash: '0x3a2533335b93232d9e83fcb25d4140d9f6dd8d4ba46b3a8f6b4e76a2148aa16f', status: 'Completed' },
    { date: 'Feb 1, 2023', amount: 0.5, description: 'Monthly Rent', txHash: '0x2b1422225b93232d9e83fcb25d4140d9f6dd8d4ba46b3a8f6b4e76a2148bb27a', status: 'Completed' },
    { date: 'Jan 1, 2023', amount: 1.5, description: 'First Month + Security Deposit', txHash: '0x1c0311115b93232d9e83fcb25d4140d9f6dd8d4ba46b3a8f6b4e76a2148cc38b', status: 'Completed' },
  ], []);
  
  // Calculate statistics using useMemo to prevent recalculation on each render
  const statistics = useMemo(() => {
    const totalSpent = paymentHistory.reduce((sum, payment) => sum + payment.amount, 0);
    const activeLeases = tenantAgreements?.filter(a => a.active)?.length || 1;
    
    return {
      totalSpent,
      activeLeases
    };
  }, [paymentHistory, tenantAgreements]);
  
  // Calculate days until next payment using useMemo
  const daysUntilNextPayment = useMemo(() => {
    const today = new Date();
    const nextPaymentDate = new Date(currentRental.nextPaymentDate);
    const diffTime = Math.abs(nextPaymentDate - today);
    return Math.ceil(diffTime / (1000 * 60 * 60 * 24));
  }, [currentRental.nextPaymentDate]);
  
  // Memoize the stats cards to prevent unnecessary re-renders
  const statsCards = useMemo(() => (
    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
      <StatCard 
        icon={FaHome} 
        title="Active Leases" 
        value={statistics.activeLeases}
        bgColor="bg-blue-100"
        iconColor="text-blue-600"
      />
      <StatCard 
        icon={FaEthereum} 
        title="Wallet Balance" 
        value={`${balance || '0'} ETH`}
        bgColor="bg-green-100"
        iconColor="text-green-600"
      />
      <StatCard 
        icon={FaCalendarAlt} 
        title="Next Payment" 
        value={`${daysUntilNextPayment} days`}
        bgColor="bg-yellow-100"
        iconColor="text-yellow-600"
      />
      <StatCard 
        icon={FaFileInvoiceDollar} 
        title="Total Spent" 
        value={`${statistics.totalSpent} ETH`}
        bgColor="bg-purple-100"
        iconColor="text-purple-600"
      />
    </div>
  ), [statistics, balance, daysUntilNextPayment]);
  
  // Search box state and handler (using useCallback to prevent recreation on each render)
  const [searchQuery, setSearchQuery] = useState('');
  const handleSearchChange = useCallback((e) => {
    setSearchQuery(e.target.value);
  }, []);
  
  return (
    <div className="space-y-6">
      {/* Tenant Header */}
      <div className="bg-white rounded-lg shadow-md p-6">
        <div className="flex flex-col md:flex-row md:items-center md:justify-between">
          <div>
            <h1 className="text-2xl font-bold text-gray-800">Tenant Dashboard</h1>
            <p className="text-gray-600">Manage your rentals and payments</p>
          </div>
          <div className="mt-4 md:mt-0 bg-blue-50 p-4 rounded-lg">
            <div className="flex items-center">
              <FaCalendarAlt className="text-blue-600 mr-2" />
              <div>
                <div className="text-sm text-gray-600">Next Payment</div>
                <div className="font-medium">{currentRental.nextPaymentDate}</div>
                <div className="text-xs text-gray-500">({daysUntilNextPayment} days left)</div>
              </div>
            </div>
          </div>
        </div>
      </div>
      
      {/* Stats Overview */}
      {statsCards}
      
      {/* Current Rental */}
      <div className="bg-white rounded-lg shadow-md p-6">
        <h2 className="text-lg font-semibold text-gray-800 mb-4">Your Current Rental</h2>
        <CurrentRentalCard 
          rental={currentRental} 
          formatAddress={formatAddress} 
          daysUntilNextPayment={daysUntilNextPayment} 
        />
      </div>
      
      {/* Payment History */}
      <div className="bg-white rounded-lg shadow-md overflow-hidden">
        <div className="p-6 border-b border-gray-200">
          <h2 className="text-lg font-semibold text-gray-800">Payment History</h2>
        </div>
        <div className="overflow-x-auto">
          <table className="min-w-full divide-y divide-gray-200">
            <thead className="bg-gray-50">
              <tr>
                <th scope="col" className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Date</th>
                <th scope="col" className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Amount</th>
                <th scope="col" className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Description</th>
                <th scope="col" className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Transaction</th>
                <th scope="col" className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Status</th>
              </tr>
            </thead>
            <VirtualizedPaymentHistory payments={paymentHistory} />
          </table>
        </div>
      </div>
      
      {/* Blockchain Agreements */}
      <div className="bg-white rounded-lg shadow-md overflow-hidden">
        <div className="p-6 border-b border-gray-200">
          <h2 className="text-lg font-semibold text-gray-800">Blockchain Agreements</h2>
        </div>
        <div className="p-6">
          {!tenantAgreements || tenantAgreements.length === 0 ? (
            <p className="text-gray-500 text-center">No blockchain rental agreements found.</p>
          ) : (
            <div className="space-y-4">
              {tenantAgreements.map((agreement, index) => (
                <AgreementCard 
                  key={agreement.id || index} 
                  agreement={agreement} 
                  index={index}
                  formatAddress={formatAddress}
                />
              ))}
            </div>
          )}
        </div>
      </div>
      
      {/* Property Search */}
      <div className="bg-white rounded-lg shadow-md p-6">
        <h2 className="text-lg font-semibold text-gray-800 mb-4">Find New Properties</h2>
        <div className="mb-4">
          <input
            type="text"
            placeholder="Search by location, price, or features..."
            className="w-full px-4 py-2 border border-gray-300 rounded-md"
            value={searchQuery}
            onChange={handleSearchChange}
          />
        </div>
        <div className="text-center text-gray-500">
          <p>Property search feature coming soon!</p>
        </div>
      </div>
    </div>
  );
};

export default React.memo(TenantDashboard); 