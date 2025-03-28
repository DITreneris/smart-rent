import React, { useState, useEffect, useMemo, useCallback } from 'react';
import { Link } from 'react-router-dom';
import { useWeb3 } from '../contexts/Web3Context';
import PropertyCard from '../components/PropertyCard';
import { FaSearch, FaFilter, FaSlidersH } from 'react-icons/fa';

// Virtualized list component for better performance
const VirtualizedPropertyList = React.memo(({ properties, visibleCount = 6 }) => {
  const [scrollPosition, setScrollPosition] = useState(0);
  const [containerHeight, setContainerHeight] = useState(0);
  
  const handleScroll = useCallback((e) => {
    setScrollPosition(e.target.scrollTop);
  }, []);

  useEffect(() => {
    const container = document.getElementById('property-list-container');
    if (container) {
      setContainerHeight(container.clientHeight);
      container.addEventListener('scroll', handleScroll);
    }
    
    return () => {
      const container = document.getElementById('property-list-container');
      if (container) {
        container.removeEventListener('scroll', handleScroll);
      }
    };
  }, [handleScroll]);

  // Calculate which items should be visible
  const itemHeight = 320; // Approximate height of each property card
  const startIndex = Math.max(0, Math.floor(scrollPosition / itemHeight) - 1);
  const endIndex = Math.min(
    properties.length - 1,
    Math.ceil((scrollPosition + containerHeight) / itemHeight) + 1
  );
  
  const visibleProperties = properties.slice(startIndex, startIndex + visibleCount);
  
  return (
    <div 
      id="property-list-container" 
      className="overflow-y-auto grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6"
      style={{ height: '70vh' }}
    >
      <div style={{ height: startIndex * itemHeight }} />
      {visibleProperties.map(property => (
        <PropertyCard key={property.id} property={property} />
      ))}
      <div style={{ height: (properties.length - endIndex - 1) * itemHeight }} />
    </div>
  );
});

const PropertyListing = () => {
  const { isConnected } = useWeb3();
  const [loading, setLoading] = useState(true);
  const [properties, setProperties] = useState([]);
  const [searchTerm, setSearchTerm] = useState('');
  const [filters, setFilters] = useState({
    priceMin: '',
    priceMax: '',
    bedrooms: '',
    bathrooms: '',
    propertyType: 'all'
  });
  const [showFilters, setShowFilters] = useState(false);

  // Fetch properties on component mount
  useEffect(() => {
    const fetchProperties = async () => {
      try {
        // Simulating API call with mock data
        setTimeout(() => {
          const mockProperties = [
            {
              id: '1',
              title: 'Modern Downtown Apartment',
              address: '123 Main St, New York, NY',
              price: '0.5',
              bedrooms: 2,
              bathrooms: 1,
              sqft: 850,
              propertyType: 'apartment',
              available: true,
              imageUrl: 'https://images.unsplash.com/photo-1522708323590-d24dbb6b0267',
              description: 'Beautiful modern apartment in the heart of downtown with stunning city views.'
            },
            {
              id: '2',
              title: 'Spacious Family Home',
              address: '456 Oak Ave, Los Angeles, CA',
              price: '1.2',
              bedrooms: 4,
              bathrooms: 2.5,
              sqft: 2200,
              propertyType: 'house',
              available: true,
              imageUrl: 'https://images.unsplash.com/photo-1510627498534-cf7e9002facc',
              description: 'Spacious family home with large backyard, perfect for entertaining.'
            },
            {
              id: '3',
              title: 'Cozy Studio Loft',
              address: '789 Pine St, Chicago, IL',
              price: '0.3',
              bedrooms: 0,
              bathrooms: 1,
              sqft: 500,
              propertyType: 'studio',
              available: true,
              imageUrl: 'https://images.unsplash.com/photo-1536376072261-38c75010e6c9',
              description: 'Cozy studio loft with modern amenities in a vibrant neighborhood.'
            },
            {
              id: '4',
              title: 'Luxury Waterfront Condo',
              address: '101 Ocean Dr, Miami, FL',
              price: '2.0',
              bedrooms: 3,
              bathrooms: 2,
              sqft: 1800,
              propertyType: 'condo',
              available: true,
              imageUrl: 'https://images.unsplash.com/photo-1515263487990-61b07816b324',
              description: 'Luxury waterfront condo with breathtaking ocean views and premium finishes.'
            },
            {
              id: '5',
              title: 'Charming Suburban Townhome',
              address: '222 Elm St, Austin, TX',
              price: '0.8',
              bedrooms: 3,
              bathrooms: 2.5,
              sqft: 1500,
              propertyType: 'townhouse',
              available: true,
              imageUrl: 'https://images.unsplash.com/photo-1512917774080-9991f1c4c750',
              description: 'Charming townhome in a quiet suburban neighborhood with community amenities.'
            },
            {
              id: '6',
              title: 'Rustic Mountain Cabin',
              address: '333 Pine Ln, Denver, CO',
              price: '0.7',
              bedrooms: 2,
              bathrooms: 1,
              sqft: 1200,
              propertyType: 'cabin',
              available: true,
              imageUrl: 'https://images.unsplash.com/photo-1518780664697-55e3ad937233',
              description: 'Rustic mountain cabin with stunning views, perfect for a peaceful getaway.'
            },
          ];
          setProperties(mockProperties);
          setLoading(false);
        }, 1000);
      } catch (error) {
        console.error('Error fetching properties:', error);
        setLoading(false);
      }
    };

    fetchProperties();
  }, []);

  const handleSearchChange = useCallback((e) => {
    setSearchTerm(e.target.value);
  }, []);

  const handleFilterChange = useCallback((e) => {
    const { name, value } = e.target;
    setFilters(prev => ({ ...prev, [name]: value }));
  }, []);

  const toggleFilters = useCallback(() => {
    setShowFilters(prev => !prev);
  }, []);

  const resetFilters = useCallback(() => {
    setFilters({
      priceMin: '',
      priceMax: '',
      bedrooms: '',
      bathrooms: '',
      propertyType: 'all'
    });
    setSearchTerm('');
  }, []);

  // Filter properties based on search and filters
  const filteredProperties = useMemo(() => {
    return properties.filter(property => {
      // Search term filter
      const matchesSearch = 
        property.title.toLowerCase().includes(searchTerm.toLowerCase()) ||
        property.address.toLowerCase().includes(searchTerm.toLowerCase()) ||
        property.description.toLowerCase().includes(searchTerm.toLowerCase());
      
      // Price range filter
      const matchesPrice = 
        (filters.priceMin === '' || parseFloat(property.price) >= parseFloat(filters.priceMin)) &&
        (filters.priceMax === '' || parseFloat(property.price) <= parseFloat(filters.priceMax));
      
      // Bedrooms filter
      const matchesBedrooms = 
        filters.bedrooms === '' || property.bedrooms >= parseInt(filters.bedrooms);
      
      // Bathrooms filter
      const matchesBathrooms = 
        filters.bathrooms === '' || property.bathrooms >= parseFloat(filters.bathrooms);
      
      // Property type filter
      const matchesType = 
        filters.propertyType === 'all' || property.propertyType === filters.propertyType;
      
      return matchesSearch && matchesPrice && matchesBedrooms && matchesBathrooms && matchesType;
    });
  }, [properties, searchTerm, filters]);

  return (
    <div className="container mx-auto px-4 py-8">
      <div className="flex flex-col md:flex-row justify-between items-center mb-8">
        <h1 className="text-3xl font-bold text-gray-900 mb-4 md:mb-0">Available Properties</h1>
        
        <div className="w-full md:w-auto flex flex-col md:flex-row space-y-2 md:space-y-0 md:space-x-2">
          <div className="relative">
            <input
              type="text"
              placeholder="Search properties..."
              className="pl-10 pr-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 w-full md:w-64"
              value={searchTerm}
              onChange={handleSearchChange}
            />
            <FaSearch className="absolute left-3 top-3 text-gray-400" />
          </div>
          
          <button
            onClick={toggleFilters}
            className="flex items-center justify-center px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition duration-300"
          >
            <FaFilter className="mr-2" />
            <span>Filters</span>
          </button>
        </div>
      </div>
      
      {showFilters && (
        <div className="bg-white p-4 mb-6 rounded-lg shadow-md">
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">Price (ETH)</label>
              <div className="flex space-x-2">
                <input
                  type="number"
                  placeholder="Min"
                  name="priceMin"
                  value={filters.priceMin}
                  onChange={handleFilterChange}
                  className="w-full p-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-1 focus:ring-blue-500"
                />
                <input
                  type="number"
                  placeholder="Max"
                  name="priceMax"
                  value={filters.priceMax}
                  onChange={handleFilterChange}
                  className="w-full p-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-1 focus:ring-blue-500"
                />
              </div>
            </div>
            
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">Bedrooms</label>
              <select
                name="bedrooms"
                value={filters.bedrooms}
                onChange={handleFilterChange}
                className="w-full p-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-1 focus:ring-blue-500"
              >
                <option value="">Any</option>
                <option value="0">Studio</option>
                <option value="1">1+</option>
                <option value="2">2+</option>
                <option value="3">3+</option>
                <option value="4">4+</option>
              </select>
            </div>
            
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">Bathrooms</label>
              <select
                name="bathrooms"
                value={filters.bathrooms}
                onChange={handleFilterChange}
                className="w-full p-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-1 focus:ring-blue-500"
              >
                <option value="">Any</option>
                <option value="1">1+</option>
                <option value="1.5">1.5+</option>
                <option value="2">2+</option>
                <option value="2.5">2.5+</option>
                <option value="3">3+</option>
              </select>
            </div>
            
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">Property Type</label>
              <select
                name="propertyType"
                value={filters.propertyType}
                onChange={handleFilterChange}
                className="w-full p-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-1 focus:ring-blue-500"
              >
                <option value="all">All Types</option>
                <option value="house">House</option>
                <option value="apartment">Apartment</option>
                <option value="condo">Condo</option>
                <option value="townhouse">Townhouse</option>
                <option value="studio">Studio</option>
                <option value="cabin">Cabin</option>
              </select>
            </div>
          </div>
          
          <div className="flex justify-end mt-4">
            <button
              onClick={resetFilters}
              className="px-4 py-2 border border-gray-300 rounded-lg mr-2 hover:bg-gray-50 transition duration-300"
            >
              Reset
            </button>
          </div>
        </div>
      )}
      
      {loading ? (
        <div className="flex justify-center items-center h-64">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600"></div>
        </div>
      ) : filteredProperties.length > 0 ? (
        <VirtualizedPropertyList properties={filteredProperties} />
      ) : (
        <div className="text-center py-12">
          <FaSlidersH className="mx-auto text-4xl text-gray-400 mb-4" />
          <h3 className="text-xl font-medium text-gray-700 mb-2">No properties found</h3>
          <p className="text-gray-500">Try adjusting your filters or search criteria</p>
        </div>
      )}

      {isConnected && (
        <div className="mt-8 text-center">
          <Link
            to="/dashboard"
            className="inline-block px-6 py-3 bg-green-600 text-white font-medium rounded-lg hover:bg-green-700 transition duration-300"
          >
            Manage Your Properties
          </Link>
        </div>
      )}
    </div>
  );
};

export default React.memo(PropertyListing); 