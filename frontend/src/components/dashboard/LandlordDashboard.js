import React, { useState, useMemo, useCallback } from 'react';
import { useWeb3 } from '../../contexts/Web3Context';
import { FaHome, FaUser, FaFileContract, FaEthereum } from 'react-icons/fa';

// Property card component - memoized to prevent unnecessary re-renders
const PropertyCard = React.memo(({ property, onView, onEdit }) => (
  <tr>
    <td className="px-6 py-4 whitespace-nowrap">
      <div className="flex items-center">
        <div className="h-10 w-10 flex-shrink-0">
          <img 
            className="h-10 w-10 rounded-full object-cover" 
            src={property.imageUrl} 
            alt={property.title}
            loading="lazy" // Lazy load images
          />
        </div>
        <div className="ml-4">
          <div className="text-sm font-medium text-gray-900">{property.title}</div>
        </div>
      </div>
    </td>
    <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">{property.location}</td>
    <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900">{property.price} ETH</td>
    <td className="px-6 py-4 whitespace-nowrap">
      <span className={`px-2 py-1 inline-flex text-xs leading-5 font-semibold rounded-full ${
        property.status === 'Available' ? 'bg-green-100 text-green-800' : 'bg-blue-100 text-blue-800'
      }`}>
        {property.status}
      </span>
    </td>
    <td className="px-6 py-4 whitespace-nowrap text-right text-sm font-medium">
      <button 
        onClick={() => onView(property.id)} 
        className="text-indigo-600 hover:text-indigo-900 mr-3"
      >
        View
      </button>
      <button 
        onClick={() => onEdit(property.id)} 
        className="text-gray-600 hover:text-gray-900"
      >
        Edit
      </button>
    </td>
  </tr>
));

// Agreement card component - memoized to prevent unnecessary re-renders
const AgreementCard = React.memo(({ agreement, index, formatAddress }) => (
  <div className="border border-gray-200 rounded-lg p-4">
    <div className="flex justify-between items-start">
      <div>
        <h3 className="font-medium">Agreement #{agreement.id || index + 1}</h3>
        <p className="text-sm text-gray-600">Tenant: {formatAddress(agreement.tenant || "0x0")}</p>
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

// Stat card component - memoized to prevent unnecessary re-renders
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

// Virtualized list for properties - only renders visible items
const VirtualizedPropertyList = React.memo(({ properties, onView, onEdit }) => {
  // In a real app, this would use react-window or react-virtualized
  // This is a simplified version for demonstration
  const [visibleRange, setVisibleRange] = useState({ start: 0, end: 20 });
  
  // Get only the properties that are currently visible
  const visibleProperties = useMemo(() => {
    return properties.slice(visibleRange.start, visibleRange.end);
  }, [properties, visibleRange]);
  
  return (
    <tbody className="bg-white divide-y divide-gray-200">
      {visibleProperties.map((property) => (
        <PropertyCard 
          key={property.id} 
          property={property} 
          onView={onView}
          onEdit={onEdit}
        />
      ))}
      {properties.length > visibleRange.end && (
        <tr>
          <td colSpan="5" className="px-6 py-4 text-center">
            <button 
              onClick={() => setVisibleRange(prev => ({ 
                start: prev.start, 
                end: Math.min(prev.end + 10, properties.length) 
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

const LandlordDashboard = () => {
  const { formatAddress, landlordAgreements } = useWeb3();
  
  const [showAddPropertyForm, setShowAddPropertyForm] = useState(false);
  const [newProperty, setNewProperty] = useState({
    title: '',
    location: '',
    price: '',
    description: ''
  });

  // Mock property data for display - in production, this would come from an API
  const [properties] = useState([
    { id: 1, title: 'Modern Apartment', location: '123 Main St, Anytown', price: 0.5, status: 'Rented', imageUrl: 'https://images.unsplash.com/photo-1522708323590-d24dbb6b0267?w=500' },
    { id: 2, title: 'Downtown Loft', location: '456 Urban Ave, Cityville', price: 0.7, status: 'Available', imageUrl: 'https://images.unsplash.com/photo-1493809842364-78817add7ffb?w=500' },
    { id: 3, title: 'Suburban House', location: '789 Quiet Ln, Suburbtown', price: 0.9, status: 'Available', imageUrl: 'https://images.unsplash.com/photo-1580587771525-78b9dba3b914?w=500' },
  ]);

  // Calculate statistics with useMemo to prevent recalculation on each render
  const statistics = useMemo(() => {
    const totalProperties = properties.length;
    const activeTenants = properties.filter(p => p.status === 'Rented').length;
    const activeAgreements = landlordAgreements?.length || 0;
    const monthlyIncome = properties.filter(p => p.status === 'Rented').reduce((total, p) => total + p.price, 0);

    return { totalProperties, activeTenants, activeAgreements, monthlyIncome };
  }, [properties, landlordAgreements]);

  // Event handlers with useCallback to prevent recreation on each render
  const toggleAddPropertyForm = useCallback(() => {
    setShowAddPropertyForm(prev => !prev);
  }, []);

  const handlePropertyInputChange = useCallback((e, field) => {
    setNewProperty(prev => ({
      ...prev,
      [field]: e.target.value
    }));
  }, []);

  const handlePropertySubmit = useCallback((e) => {
    e.preventDefault();
    // Here you would add the property to your database/blockchain
    console.log('New property submitted:', newProperty);
    // Reset form and hide it
    setNewProperty({ title: '', location: '', price: '', description: '' });
    setShowAddPropertyForm(false);
  }, [newProperty]);

  const handleViewProperty = useCallback((id) => {
    console.log('View property:', id);
    // Navigation would go here
  }, []);

  const handleEditProperty = useCallback((id) => {
    console.log('Edit property:', id);
    // Navigation would go here
  }, []);

  // Memoize stats cards to prevent unnecessary re-renders
  const statsCards = useMemo(() => (
    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
      <StatCard 
        icon={FaHome} 
        title="Properties" 
        value={statistics.totalProperties}
        bgColor="bg-blue-100"
        iconColor="text-blue-600"
      />
      <StatCard 
        icon={FaUser} 
        title="Active Tenants" 
        value={statistics.activeTenants}
        bgColor="bg-green-100"
        iconColor="text-green-600"
      />
      <StatCard 
        icon={FaFileContract} 
        title="Agreements" 
        value={statistics.activeAgreements}
        bgColor="bg-yellow-100"
        iconColor="text-yellow-600"
      />
      <StatCard 
        icon={FaEthereum} 
        title="Monthly Income" 
        value={`${statistics.monthlyIncome} ETH`}
        bgColor="bg-purple-100"
        iconColor="text-purple-600"
      />
    </div>
  ), [statistics]);

  // Memoize property form to prevent unnecessary re-renders
  const propertyForm = useMemo(() => {
    if (!showAddPropertyForm) return null;
    
    return (
      <div className="mt-6 border-t border-gray-200 pt-4">
        <form onSubmit={handlePropertySubmit}>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">Property Title</label>
              <input
                type="text"
                className="w-full px-3 py-2 border border-gray-300 rounded-md"
                value={newProperty.title}
                onChange={(e) => handlePropertyInputChange(e, 'title')}
                required
              />
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">Location</label>
              <input
                type="text"
                className="w-full px-3 py-2 border border-gray-300 rounded-md"
                value={newProperty.location}
                onChange={(e) => handlePropertyInputChange(e, 'location')}
                required
              />
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">Monthly Rent (ETH)</label>
              <input
                type="number"
                step="0.01"
                className="w-full px-3 py-2 border border-gray-300 rounded-md"
                value={newProperty.price}
                onChange={(e) => handlePropertyInputChange(e, 'price')}
                required
              />
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">Description</label>
              <textarea
                className="w-full px-3 py-2 border border-gray-300 rounded-md"
                value={newProperty.description}
                onChange={(e) => handlePropertyInputChange(e, 'description')}
                required
              ></textarea>
            </div>
          </div>
          <div className="mt-4 flex justify-end">
            <button
              type="submit"
              className="bg-green-600 hover:bg-green-700 text-white px-4 py-2 rounded-md"
            >
              Save Property
            </button>
          </div>
        </form>
      </div>
    );
  }, [showAddPropertyForm, newProperty, handlePropertyInputChange, handlePropertySubmit]);

  // Memoize agreements section to prevent unnecessary re-renders
  const agreementsSection = useMemo(() => (
    <div className="bg-white rounded-lg shadow-md overflow-hidden">
      <div className="p-6 border-b border-gray-200">
        <h2 className="text-lg font-semibold text-gray-800">Recent Agreements</h2>
      </div>
      <div className="p-6">
        {!landlordAgreements || landlordAgreements.length === 0 ? (
          <p className="text-gray-500 text-center">No rental agreements found.</p>
        ) : (
          <div className="space-y-4">
            {landlordAgreements.map((agreement, index) => (
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
  ), [landlordAgreements, formatAddress]);

  return (
    <div className="space-y-6">
      {/* Landlord Header */}
      <div className="bg-white rounded-lg shadow-md p-6">
        <div className="flex flex-col md:flex-row md:items-center md:justify-between">
          <div>
            <h1 className="text-2xl font-bold text-gray-800">Landlord Dashboard</h1>
            <p className="text-gray-600">Manage your properties and rental agreements</p>
          </div>
          <div className="mt-4 md:mt-0">
            <button 
              onClick={toggleAddPropertyForm}
              className="bg-blue-600 hover:bg-blue-700 text-white px-4 py-2 rounded-md"
            >
              {showAddPropertyForm ? 'Cancel' : '+ Add New Property'}
            </button>
          </div>
        </div>

        {/* Add Property Form */}
        {propertyForm}
      </div>
      
      {/* Stats Overview */}
      {statsCards}
      
      {/* Properties Table */}
      <div className="bg-white rounded-lg shadow-md overflow-hidden">
        <div className="p-6 border-b border-gray-200">
          <h2 className="text-lg font-semibold text-gray-800">Manage Properties</h2>
        </div>
        <div className="overflow-x-auto">
          <table className="min-w-full divide-y divide-gray-200">
            <thead className="bg-gray-50">
              <tr>
                <th scope="col" className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Property</th>
                <th scope="col" className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Location</th>
                <th scope="col" className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Price (ETH)</th>
                <th scope="col" className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Status</th>
                <th scope="col" className="px-6 py-3 text-right text-xs font-medium text-gray-500 uppercase tracking-wider">Actions</th>
              </tr>
            </thead>
            <VirtualizedPropertyList 
              properties={properties} 
              onView={handleViewProperty}
              onEdit={handleEditProperty}
            />
          </table>
        </div>
      </div>
      
      {/* Recent Agreements */}
      {agreementsSection}
    </div>
  );
};

export default React.memo(LandlordDashboard); 