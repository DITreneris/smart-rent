import React from 'react';
import { Link } from 'react-router-dom';
import { FaHeart, FaBed, FaBath, FaRulerCombined } from 'react-icons/fa';

const PropertyCard = ({ property, onFavorite }) => {
  // ETH conversion rate from environment variable
  const ethPrice = process.env.REACT_APP_ETH_USD_PRICE || 1800; // Default to $1800 if not set
  const ethAmount = (property.price / ethPrice).toFixed(3);

  return (
    <div className="bg-white rounded-lg shadow-md overflow-hidden transition-transform hover:scale-[1.02]">
      <div className="relative">
        <img 
          src={property.imageUrl || 'https://via.placeholder.com/400x250?text=Property'} 
          alt={property.title}
          className="w-full h-64 object-cover"
        />
        <div className="absolute top-0 right-0 bg-blue-600 text-white py-1 px-3 rounded-bl-lg font-bold">
          <div>${property.price}/month</div>
          <div className="text-sm font-medium text-blue-100">{ethAmount} ETH/month</div>
        </div>
      </div>
      <div className="p-4">
        <h3 className="text-xl font-bold text-gray-800">{property.title}</h3>
        <p className="text-gray-600 mb-3">{property.address}, {property.city}</p>
        
        <div className="flex justify-between mb-4">
          <div className="flex items-center text-gray-700">
            <FaBed className="mr-1" />
            <span>{property.bedrooms} Beds</span>
          </div>
          <div className="flex items-center text-gray-700">
            <FaBath className="mr-1" />
            <span>{property.bathrooms} Baths</span>
          </div>
          <div className="flex items-center text-gray-700">
            <FaRulerCombined className="mr-1" />
            <span>{property.sqft} sqft</span>
          </div>
        </div>
        
        <div className="flex justify-between items-center">
          <Link 
            to={`/properties/${property.id}`}
            className="bg-blue-600 hover:bg-blue-700 text-white py-2 px-4 rounded-md font-medium"
          >
            View Details
          </Link>
          {onFavorite && (
            <button 
              onClick={() => onFavorite(property.id)}
              className="text-gray-400 hover:text-red-500"
              aria-label="Favorite"
            >
              <FaHeart className={property.is_favorite ? "text-red-500" : ""} />
            </button>
          )}
        </div>
      </div>
    </div>
  );
};

// Memoize the component to prevent unnecessary re-renders
export default React.memo(PropertyCard, (prevProps, nextProps) => {
  return prevProps.property.id === nextProps.property.id && 
         prevProps.property.is_favorite === nextProps.property.is_favorite;
}); 