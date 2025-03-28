import React, { useState, useEffect } from 'react';
import axios from 'axios';
import PropertyCard from '../components/PropertyCard';
import { useWeb3 } from '../contexts/Web3Context';

const PropertyList = () => {
  const [properties, setProperties] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [filters, setFilters] = useState({
    minPrice: '',
    maxPrice: '',
    bedrooms: 'Any',
    propertyType: 'Any'
  });

  const { isConnected } = useWeb3();

  // Fetch properties
  useEffect(() => {
    const fetchProperties = async () => {
      try {
        setLoading(true);
        setError(null);
        
        // Always load mock data for demo purposes
        // In a production app, this would be conditional based on the environment
        const testData = [
          {
            id: 1,
            title: 'Luxury Apartment',
            address: '123 Main St',
            city: 'City',
            price: 2200,
            bedrooms: 2,
            bathrooms: 2,
            area: 1100,
            property_type: 'apartment',
            image_url: 'https://images.unsplash.com/photo-1512917774080-9991f1c4c750?w=800&auto=format&fit=crop'
          },
          {
            id: 2,
            title: 'Modern Townhouse',
            address: '456 Oak Ave',
            city: 'Town',
            price: 1500,
            bedrooms: 3,
            bathrooms: 2.5,
            area: 1800,
            property_type: 'townhouse',
            image_url: 'https://images.unsplash.com/photo-1580587771525-78b9dba3b914?w=800&auto=format&fit=crop'
          },
          {
            id: 3,
            title: 'Cozy Studio',
            address: '789 Pine St',
            city: 'City',
            price: 800,
            bedrooms: 0,
            bathrooms: 1,
            area: 500,
            property_type: 'studio',
            image_url: 'https://images.unsplash.com/photo-1522708323590-d24dbb6b0267?w=800&auto=format&fit=crop'
          },
          {
            id: 4,
            title: 'Waterfront Villa',
            address: '101 Beach Dr',
            city: 'Coast',
            price: 3200,
            bedrooms: 4,
            bathrooms: 3,
            area: 2200,
            property_type: 'house',
            image_url: 'https://images.unsplash.com/photo-1564013799919-ab600027ffc6?w=800&auto=format&fit=crop'
          }
        ];
        
        setProperties(testData);
        setLoading(false);

        // Try to fetch from API only if not in test mode
        if (process.env.REACT_APP_ENABLE_TEST_MODE !== 'true') {
          try {
            const response = await axios.get(`${process.env.REACT_APP_API_URL}/properties`);
            if (response.data && response.data.length > 0) {
              setProperties(response.data);
            }
          } catch (apiErr) {
            console.warn('Could not fetch from API, using test data:', apiErr);
            // We already set test data, so no need to show error to user
          }
        }
      } catch (err) {
        console.error('Error in property loading:', err);
        setError('Failed to load properties. Please try again later.');
        setLoading(false);
      }
    };

    fetchProperties();
  }, []);

  // Handle filter changes
  const handleFilterChange = (e) => {
    const { name, value } = e.target;
    setFilters({
      ...filters,
      [name]: value
    });
  };

  // Apply filters
  const applyFilters = () => {
    // In a real app, this would call API with filters
    console.log('Applying filters:', filters);
    
    // For demo, filter the local data
    const filtered = [
      {
        id: 1,
        title: 'Luxury Apartment',
        address: '123 Main St',
        city: 'City',
        price: 2200,
        bedrooms: 2,
        bathrooms: 2,
        area: 1100,
        property_type: 'apartment',
        image_url: 'https://images.unsplash.com/photo-1512917774080-9991f1c4c750?w=800&auto=format&fit=crop'
      },
      {
        id: 2,
        title: 'Modern Townhouse',
        address: '456 Oak Ave',
        city: 'Town',
        price: 1500,
        bedrooms: 3,
        bathrooms: 2.5,
        area: 1800,
        property_type: 'townhouse',
        image_url: 'https://images.unsplash.com/photo-1580587771525-78b9dba3b914?w=800&auto=format&fit=crop'
      },
      {
        id: 3,
        title: 'Cozy Studio',
        address: '789 Pine St',
        city: 'City',
        price: 800,
        bedrooms: 0,
        bathrooms: 1,
        area: 500,
        property_type: 'studio',
        image_url: 'https://images.unsplash.com/photo-1522708323590-d24dbb6b0267?w=800&auto=format&fit=crop'
      },
      {
        id: 4,
        title: 'Waterfront Villa',
        address: '101 Beach Dr',
        city: 'Coast',
        price: 3200,
        bedrooms: 4,
        bathrooms: 3,
        area: 2200,
        property_type: 'house',
        image_url: 'https://images.unsplash.com/photo-1564013799919-ab600027ffc6?w=800&auto=format&fit=crop'
      }
    ].filter(property => {
      // Filter by price
      if (filters.minPrice && property.price < parseInt(filters.minPrice)) return false;
      if (filters.maxPrice && property.price > parseInt(filters.maxPrice)) return false;
      
      // Filter by bedrooms
      if (filters.bedrooms !== 'Any') {
        if (filters.bedrooms === '0' && property.bedrooms !== 0) return false;
        if (filters.bedrooms === '1' && property.bedrooms !== 1) return false;
        if (filters.bedrooms === '2' && property.bedrooms !== 2) return false;
        if (filters.bedrooms === '3' && property.bedrooms < 3) return false;
      }
      
      // Filter by property type
      if (filters.propertyType !== 'Any' && property.property_type !== filters.propertyType.toLowerCase()) return false;
      
      return true;
    });
    
    setProperties(filtered);
  };

  // Handle favorite toggle
  const handleFavoriteToggle = (propertyId) => {
    setProperties(properties.map(property => 
      property.id === propertyId 
        ? { ...property, is_favorite: !property.is_favorite } 
        : property
    ));
  };

  if (loading) return <div className="text-center py-10">Loading properties...</div>;
  if (error) return <div className="text-center py-10 text-red-600">{error}</div>;

  return (
    <div>
      <h1 className="text-3xl font-bold text-gray-800 mb-8">Available Properties</h1>
      
      {/* Filters */}
      <div className="bg-white p-6 rounded-lg shadow-sm mb-8">
        <h2 className="text-xl font-semibold mb-4">Filters</h2>
        <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">Min Price</label>
            <input
              type="number"
              name="minPrice"
              value={filters.minPrice}
              onChange={handleFilterChange}
              placeholder="Min $"
              className="w-full p-2 border border-gray-300 rounded-md"
            />
          </div>
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">Max Price</label>
            <input
              type="number"
              name="maxPrice"
              value={filters.maxPrice}
              onChange={handleFilterChange}
              placeholder="Max $"
              className="w-full p-2 border border-gray-300 rounded-md"
            />
          </div>
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">Bedrooms</label>
            <select
              name="bedrooms"
              value={filters.bedrooms}
              onChange={handleFilterChange}
              className="w-full p-2 border border-gray-300 rounded-md"
            >
              <option value="Any">Any</option>
              <option value="0">Studio</option>
              <option value="1">1</option>
              <option value="2">2</option>
              <option value="3">3+</option>
            </select>
          </div>
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">Property Type</label>
            <select
              name="propertyType"
              value={filters.propertyType}
              onChange={handleFilterChange}
              className="w-full p-2 border border-gray-300 rounded-md"
            >
              <option value="Any">Any</option>
              <option value="apartment">Apartment</option>
              <option value="house">House</option>
              <option value="townhouse">Townhouse</option>
              <option value="studio">Studio</option>
            </select>
          </div>
        </div>
        <button
          onClick={applyFilters}
          className="mt-4 bg-blue-600 hover:bg-blue-700 text-white py-2 px-4 rounded-md"
        >
          Apply Filters
        </button>
      </div>
      
      {/* Property Listings */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        {properties.map(property => (
          <PropertyCard 
            key={property.id} 
            property={property} 
            onFavorite={handleFavoriteToggle}
          />
        ))}
      </div>
      
      {properties.length === 0 && (
        <div className="text-center py-10 text-gray-600">
          No properties match your search criteria.
        </div>
      )}

      {!isConnected && (
        <div className="mt-8 bg-blue-50 border border-blue-200 p-4 rounded-md">
          <p className="text-blue-800">
            Connect your Ethereum wallet to enable direct rental payments in ETH and access to smart contract features.
          </p>
        </div>
      )}
    </div>
  );
};

export default PropertyList; 