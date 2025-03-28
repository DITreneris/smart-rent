import React, { useState, useMemo, useCallback, Suspense, lazy } from 'react';
// Remove empty destructuring from useWeb3
// import { useWeb3 } from '../../contexts/Web3Context';
import { FaHome, FaUser, FaFileContract } from 'react-icons/fa';

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

// Memoized UserItem component to prevent unnecessary re-renders
const UserItem = React.memo(({ user, onVerify, onBan }) => (
  <tr>
    <td className="px-6 py-4 whitespace-nowrap">
      <div className="flex items-center">
        <div className="h-10 w-10 flex-shrink-0">
          <img 
            className="h-10 w-10 rounded-full object-cover" 
            src={`https://avatars.dicebear.com/api/initials/${user.username}.svg`} 
            alt={user.username}
            loading="lazy"
          />
        </div>
        <div className="ml-4">
          <div className="text-sm font-medium text-gray-900">{user.username}</div>
          <div className="text-sm text-gray-500">{user.address}</div>
        </div>
      </div>
    </td>
    <td className="px-6 py-4 whitespace-nowrap">
      <span className="text-sm text-gray-500">{user.role}</span>
    </td>
    <td className="px-6 py-4 whitespace-nowrap">
      <span className="text-sm text-gray-500">{user.joinDate}</span>
    </td>
    <td className="px-6 py-4 whitespace-nowrap">
      <span className={`px-2 py-1 inline-flex text-xs leading-5 font-semibold rounded-full ${
        user.verified ? 'bg-green-100 text-green-800' : 'bg-yellow-100 text-yellow-800'
      }`}>
        {user.verified ? 'Verified' : 'Pending'}
      </span>
    </td>
    <td className="px-6 py-4 whitespace-nowrap text-right text-sm font-medium">
      {!user.verified ? (
        <button
          onClick={() => onVerify(user.id)}
          className="text-indigo-600 hover:text-indigo-900 mr-3"
        >
          Verify
        </button>
      ) : null}
      {!user.banned ? (
        <button
          onClick={() => onBan(user.id)}
          className="text-red-600 hover:text-red-900"
        >
          Ban
        </button>
      ) : (
        <button
          onClick={() => onBan(user.id)}
          className="text-gray-600 hover:text-gray-900"
        >
          Unban
        </button>
      )}
    </td>
  </tr>
));

// Memoized PropertyItem component to prevent unnecessary re-renders
const PropertyItem = React.memo(({ property, onApprove, onReject }) => (
  <tr>
    <td className="px-6 py-4 whitespace-nowrap">
      <div className="flex items-center">
        <div className="h-10 w-10 flex-shrink-0">
          <img 
            className="h-10 w-10 rounded object-cover" 
            src={property.imageUrl} 
            alt={property.title}
            loading="lazy"
          />
        </div>
        <div className="ml-4">
          <div className="text-sm font-medium text-gray-900">{property.title}</div>
          <div className="text-sm text-gray-500">{property.location}</div>
        </div>
      </div>
    </td>
    <td className="px-6 py-4 whitespace-nowrap">
      <span className="text-sm text-gray-500">{property.landlord}</span>
    </td>
    <td className="px-6 py-4 whitespace-nowrap">
      <span className="text-sm text-gray-900">{property.price} ETH</span>
    </td>
    <td className="px-6 py-4 whitespace-nowrap">
      <span className={`px-2 py-1 inline-flex text-xs leading-5 font-semibold rounded-full ${
        property.status === 'Pending' ? 'bg-yellow-100 text-yellow-800' : 
        property.status === 'Approved' ? 'bg-green-100 text-green-800' : 
        'bg-red-100 text-red-800'
      }`}>
        {property.status}
      </span>
    </td>
    <td className="px-6 py-4 whitespace-nowrap text-right text-sm font-medium">
      {property.status === 'Pending' && (
        <>
          <button
            onClick={() => onApprove(property.id)}
            className="text-indigo-600 hover:text-indigo-900 mr-3"
          >
            Approve
          </button>
          <button
            onClick={() => onReject(property.id)}
            className="text-red-600 hover:text-red-900"
          >
            Reject
          </button>
        </>
      )}
    </td>
  </tr>
));

// Improved virtualized list with dynamic rendering thresholds for performance
const VirtualizedUserList = React.memo(({ users, onVerify, onBan }) => {
  // Use a more memory-efficient approach for larger lists
  const pageSize = useMemo(() => Math.min(10, Math.ceil(users.length / 5)), [users.length]);
  const [visibleRange, setVisibleRange] = useState({ start: 0, end: pageSize });
  
  // Optimize visible item calculation with useMemo
  const visibleUsers = useMemo(() => {
    return users.slice(visibleRange.start, visibleRange.end);
  }, [users, visibleRange.start, visibleRange.end]);
  
  // Optimize load more handler with useCallback
  const loadMore = useCallback(() => {
    setVisibleRange(prev => ({ 
      start: prev.start, 
      end: Math.min(prev.end + pageSize, users.length) 
    }));
  }, [pageSize, users.length]);
  
  return (
    <tbody className="bg-white divide-y divide-gray-200">
      {visibleUsers.map((user) => (
        <UserItem 
          key={user.id} 
          user={user} 
          onVerify={onVerify}
          onBan={onBan}
        />
      ))}
      {users.length > visibleRange.end && (
        <tr>
          <td colSpan="5" className="px-6 py-4 text-center">
            <button 
              onClick={loadMore}
              className="text-indigo-600 hover:text-indigo-900"
            >
              Load more ({users.length - visibleRange.end} remaining)
            </button>
          </td>
        </tr>
      )}
    </tbody>
  );
});

// Improved virtualized list for properties with dynamic rendering thresholds for performance
const VirtualizedPropertyList = React.memo(({ properties, onApprove, onReject }) => {
  // Use a more memory-efficient approach for larger lists
  const pageSize = useMemo(() => Math.min(10, Math.ceil(properties.length / 5)), [properties.length]);
  const [visibleRange, setVisibleRange] = useState({ start: 0, end: pageSize });
  
  // Optimize visible item calculation with useMemo
  const visibleProperties = useMemo(() => {
    return properties.slice(visibleRange.start, visibleRange.end);
  }, [properties, visibleRange.start, visibleRange.end]);
  
  // Optimize load more handler with useCallback
  const loadMore = useCallback(() => {
    setVisibleRange(prev => ({ 
      start: prev.start, 
      end: Math.min(prev.end + pageSize, properties.length) 
    }));
  }, [pageSize, properties.length]);
  
  return (
    <tbody className="bg-white divide-y divide-gray-200">
      {visibleProperties.map((property) => (
        <PropertyItem 
          key={property.id} 
          property={property} 
          onApprove={onApprove}
          onReject={onReject}
        />
      ))}
      {properties.length > visibleRange.end && (
        <tr>
          <td colSpan="5" className="px-6 py-4 text-center">
            <button 
              onClick={loadMore}
              className="text-indigo-600 hover:text-indigo-900"
            >
              Load more ({properties.length - visibleRange.end} remaining)
            </button>
          </td>
        </tr>
      )}
    </tbody>
  );
});

// Use dynamic import with prefetching hint for better loading performance
const PlatformStatisticsChart = lazy(() => {
  // Add a small delay to ensure main content loads first
  return Promise.all([
    import('../charts/PlatformStatisticsChart'),
    new Promise(resolve => setTimeout(resolve, 100))
  ]).then(([moduleExports]) => moduleExports);
});

// Loading fallback component - memoized to prevent unnecessary re-renders
const ChartLoadingFallback = React.memo(() => (
  <div className="text-center py-10">
    <div className="inline-block animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600 mb-2"></div>
    <p className="text-gray-600">Loading chart data...</p>
  </div>
));

const AdminDashboard = () => {
  // Tab state
  const [activeTab, setActiveTab] = useState('users');
  
  // Filter state
  const [userFilter, setUserFilter] = useState('all');
  const [propertyFilter, setPropertyFilter] = useState('pending');
  
  // Mock data for users - use lazy initialization function for useState
  const [users] = useState(() => [
    { id: 1, username: 'alice', address: '0x1234...5678', role: 'Landlord', joinDate: '2023-01-15', verified: true, banned: false },
    { id: 2, username: 'bob', address: '0x5678...9012', role: 'Tenant', joinDate: '2023-02-20', verified: true, banned: false },
    { id: 3, username: 'charlie', address: '0x9012...3456', role: 'Landlord', joinDate: '2023-03-10', verified: false, banned: false },
    { id: 4, username: 'dave', address: '0x3456...7890', role: 'Tenant', joinDate: '2023-03-25', verified: true, banned: true },
    { id: 5, username: 'eve', address: '0x7890...1234', role: 'Landlord', joinDate: '2023-04-05', verified: false, banned: false },
    { id: 6, username: 'frank', address: '0xabcd...efgh', role: 'Tenant', joinDate: '2023-04-20', verified: true, banned: false },
    { id: 7, username: 'grace', address: '0xefgh...ijkl', role: 'Landlord', joinDate: '2023-05-10', verified: true, banned: false },
  ]);
  
  // Mock data for properties - use lazy initialization function for useState
  const [properties] = useState(() => [
    { id: 1, title: 'Downtown Loft', location: '123 Main St, Cityville', landlord: 'alice', price: 0.5, status: 'Approved', imageUrl: 'https://images.unsplash.com/photo-1522708323590-d24dbb6b0267?w=500' },
    { id: 2, title: 'Suburban House', location: '456 Oak Ave, Suburbtown', landlord: 'alice', price: 0.7, status: 'Pending', imageUrl: 'https://images.unsplash.com/photo-1580587771525-78b9dba3b914?w=500' },
    { id: 3, title: 'City Apartment', location: '789 Urban Blvd, Metropolis', landlord: 'eve', price: 0.6, status: 'Pending', imageUrl: 'https://images.unsplash.com/photo-1493809842364-78817add7ffb?w=500' },
    { id: 4, title: 'Beach House', location: '101 Ocean Dr, Beachside', landlord: 'grace', price: 1.2, status: 'Rejected', imageUrl: 'https://images.unsplash.com/photo-1499793983690-e29da59ef1c2?w=500' },
  ]);
  
  // Calculate statistics with useMemo and optimized dependencies
  const statistics = useMemo(() => {
    const totalUsers = users.length;
    const verifiedUsers = users.filter(user => user.verified).length;
    const totalProperties = properties.length;
    const approvedProperties = properties.filter(prop => prop.status === 'Approved').length;
    
    return { totalUsers, verifiedUsers, totalProperties, approvedProperties };
  }, [users, properties]);
  
  // Filter users with useMemo and explicit dependencies
  const filteredUsers = useMemo(() => {
    switch (userFilter) {
      case 'verified':
        return users.filter(user => user.verified);
      case 'pending':
        return users.filter(user => !user.verified);
      case 'banned':
        return users.filter(user => user.banned);
      default:
        return users;
    }
  }, [users, userFilter]);
  
  // Filter properties with useMemo and explicit dependencies
  const filteredProperties = useMemo(() => {
    switch (propertyFilter) {
      case 'approved':
        return properties.filter(prop => prop.status === 'Approved');
      case 'pending':
        return properties.filter(prop => prop.status === 'Pending');
      case 'rejected':
        return properties.filter(prop => prop.status === 'Rejected');
      default:
        return properties;
    }
  }, [properties, propertyFilter]);
  
  // Event handlers with useCallback
  const handleTabChange = useCallback((tab) => {
    setActiveTab(tab);
  }, []);
  
  const handleUserFilterChange = useCallback((filter) => {
    setUserFilter(filter);
  }, []);
  
  const handlePropertyFilterChange = useCallback((filter) => {
    setPropertyFilter(filter);
  }, []);
  
  const handleVerifyUser = useCallback((userId) => {
    console.log('Verify user:', userId);
    // Implementation would set user.verified = true
  }, []);
  
  const handleBanUser = useCallback((userId) => {
    console.log('Ban/unban user:', userId);
    // Implementation would toggle user.banned
  }, []);
  
  const handleApproveProperty = useCallback((propertyId) => {
    console.log('Approve property:', propertyId);
    // Implementation would set property.status = 'Approved'
  }, []);
  
  const handleRejectProperty = useCallback((propertyId) => {
    console.log('Reject property:', propertyId);
    // Implementation would set property.status = 'Rejected'
  }, []);
  
  // Memoize stats cards
  const statsCards = useMemo(() => (
    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
      <StatCard 
        icon={FaUser} 
        title="Total Users" 
        value={statistics.totalUsers}
        bgColor="bg-blue-100"
        iconColor="text-blue-600"
      />
      <StatCard 
        icon={FaUser} 
        title="Verified Users" 
        value={`${statistics.verifiedUsers}/${statistics.totalUsers}`}
        bgColor="bg-green-100"
        iconColor="text-green-600"
      />
      <StatCard 
        icon={FaHome} 
        title="Total Properties" 
        value={statistics.totalProperties}
        bgColor="bg-purple-100"
        iconColor="text-purple-600"
      />
      <StatCard 
        icon={FaFileContract} 
        title="Approved Properties" 
        value={`${statistics.approvedProperties}/${statistics.totalProperties}`}
        bgColor="bg-yellow-100"
        iconColor="text-yellow-600"
      />
    </div>
  ), [statistics]);
  
  // Memoize tab buttons
  const tabButtons = useMemo(() => (
    <div className="flex border-b border-gray-200 mb-4">
      <button
        onClick={() => handleTabChange('users')}
        className={`px-4 py-2 font-medium ${
          activeTab === 'users'
            ? 'text-blue-600 border-b-2 border-blue-600'
            : 'text-gray-500 hover:text-gray-700'
        }`}
      >
        User Management
      </button>
      <button
        onClick={() => handleTabChange('properties')}
        className={`px-4 py-2 font-medium ${
          activeTab === 'properties'
            ? 'text-blue-600 border-b-2 border-blue-600'
            : 'text-gray-500 hover:text-gray-700'
        }`}
      >
        Property Approval
      </button>
      <button
        onClick={() => handleTabChange('stats')}
        className={`px-4 py-2 font-medium ${
          activeTab === 'stats'
            ? 'text-blue-600 border-b-2 border-blue-600'
            : 'text-gray-500 hover:text-gray-700'
        }`}
      >
        Platform Statistics
      </button>
    </div>
  ), [activeTab, handleTabChange]);
  
  // Memoize user filter controls
  const userFilterControls = useMemo(() => (
    <div className="flex space-x-2 mb-4">
      <button
        onClick={() => handleUserFilterChange('all')}
        className={`px-3 py-1 rounded-md text-sm ${
          userFilter === 'all'
            ? 'bg-blue-600 text-white'
            : 'bg-gray-100 text-gray-800 hover:bg-gray-200'
        }`}
      >
        All Users
      </button>
      <button
        onClick={() => handleUserFilterChange('verified')}
        className={`px-3 py-1 rounded-md text-sm ${
          userFilter === 'verified'
            ? 'bg-blue-600 text-white'
            : 'bg-gray-100 text-gray-800 hover:bg-gray-200'
        }`}
      >
        Verified
      </button>
      <button
        onClick={() => handleUserFilterChange('pending')}
        className={`px-3 py-1 rounded-md text-sm ${
          userFilter === 'pending'
            ? 'bg-blue-600 text-white'
            : 'bg-gray-100 text-gray-800 hover:bg-gray-200'
        }`}
      >
        Pending
      </button>
      <button
        onClick={() => handleUserFilterChange('banned')}
        className={`px-3 py-1 rounded-md text-sm ${
          userFilter === 'banned'
            ? 'bg-blue-600 text-white'
            : 'bg-gray-100 text-gray-800 hover:bg-gray-200'
        }`}
      >
        Banned
      </button>
    </div>
  ), [userFilter, handleUserFilterChange]);
  
  // Memoize property filter controls
  const propertyFilterControls = useMemo(() => (
    <div className="flex space-x-2 mb-4">
      <button
        onClick={() => handlePropertyFilterChange('all')}
        className={`px-3 py-1 rounded-md text-sm ${
          propertyFilter === 'all'
            ? 'bg-blue-600 text-white'
            : 'bg-gray-100 text-gray-800 hover:bg-gray-200'
        }`}
      >
        All Properties
      </button>
      <button
        onClick={() => handlePropertyFilterChange('pending')}
        className={`px-3 py-1 rounded-md text-sm ${
          propertyFilter === 'pending'
            ? 'bg-blue-600 text-white'
            : 'bg-gray-100 text-gray-800 hover:bg-gray-200'
        }`}
      >
        Pending
      </button>
      <button
        onClick={() => handlePropertyFilterChange('approved')}
        className={`px-3 py-1 rounded-md text-sm ${
          propertyFilter === 'approved'
            ? 'bg-blue-600 text-white'
            : 'bg-gray-100 text-gray-800 hover:bg-gray-200'
        }`}
      >
        Approved
      </button>
      <button
        onClick={() => handlePropertyFilterChange('rejected')}
        className={`px-3 py-1 rounded-md text-sm ${
          propertyFilter === 'rejected'
            ? 'bg-blue-600 text-white'
            : 'bg-gray-100 text-gray-800 hover:bg-gray-200'
        }`}
      >
        Rejected
      </button>
    </div>
  ), [propertyFilter, handlePropertyFilterChange]);
  
  // Memoize users table
  const usersTable = useMemo(() => (
    <div className="overflow-x-auto">
      <table className="min-w-full divide-y divide-gray-200">
        <thead className="bg-gray-50">
          <tr>
            <th scope="col" className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">User</th>
            <th scope="col" className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Role</th>
            <th scope="col" className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Join Date</th>
            <th scope="col" className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Status</th>
            <th scope="col" className="px-6 py-3 text-right text-xs font-medium text-gray-500 uppercase tracking-wider">Actions</th>
          </tr>
        </thead>
        <VirtualizedUserList 
          users={filteredUsers} 
          onVerify={handleVerifyUser}
          onBan={handleBanUser}
        />
      </table>
    </div>
  ), [filteredUsers, handleVerifyUser, handleBanUser]);
  
  // Memoize properties table
  const propertiesTable = useMemo(() => (
    <div className="overflow-x-auto">
      <table className="min-w-full divide-y divide-gray-200">
        <thead className="bg-gray-50">
          <tr>
            <th scope="col" className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Property</th>
            <th scope="col" className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Landlord</th>
            <th scope="col" className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Price</th>
            <th scope="col" className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Status</th>
            <th scope="col" className="px-6 py-3 text-right text-xs font-medium text-gray-500 uppercase tracking-wider">Actions</th>
          </tr>
        </thead>
        <VirtualizedPropertyList 
          properties={filteredProperties} 
          onApprove={handleApproveProperty}
          onReject={handleRejectProperty}
        />
      </table>
    </div>
  ), [filteredProperties, handleApproveProperty, handleRejectProperty]);

  // Conditionally render tab content to avoid unnecessary rendering of inactive tabs
  const activeTabContent = useMemo(() => {
    switch (activeTab) {
      case 'users':
        return (
          <div>
            {userFilterControls}
            {usersTable}
          </div>
        );
      case 'properties':
        return (
          <div>
            {propertyFilterControls}
            {propertiesTable}
          </div>
        );
      case 'stats':
        return (
          <div>
            <h2 className="text-lg font-semibold text-gray-800 mb-4">Platform Statistics</h2>
            <Suspense fallback={<ChartLoadingFallback />}>
              <PlatformStatisticsChart />
            </Suspense>
          </div>
        );
      default:
        return null;
    }
  }, [
    activeTab, 
    userFilterControls, 
    propertyFilterControls, 
    usersTable, 
    propertiesTable
  ]);

  return (
    <div className="space-y-6">
      {/* Admin Header */}
      <div className="bg-white rounded-lg shadow-md p-6">
        <h1 className="text-2xl font-bold text-gray-800">Admin Dashboard</h1>
        <p className="text-gray-600">Manage users, properties, and monitor platform activity</p>
      </div>
      
      {/* Stats Overview */}
      {statsCards}
      
      {/* Main Content */}
      <div className="bg-white rounded-lg shadow-md p-6">
        {/* Tab navigation */}
        {tabButtons}
        
        {/* Active tab content */}
        {activeTabContent}
      </div>
    </div>
  );
};

export default React.memo(AdminDashboard); 