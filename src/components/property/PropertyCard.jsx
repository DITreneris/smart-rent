import React from 'react';
import { Link } from 'react-router-dom';
import { shortenAddress } from '../../utils/addressUtils';

const PropertyCard = ({ property }) => {
  return (
    <div className="bg-white rounded-lg shadow-md overflow-hidden transition-transform hover:scale-[1.02]">
      <img 
        src={property.image_urls ? JSON.parse(property.image_urls)[0] : 'https://via.placeholder.com/300x200?text=No+Image'} 
        alt={property.title}
        className="w-full h-48 object-cover"
      />
      
      <div className="p-4">
        <h3 className="text-xl font-semibold mb-2">{property.title}</h3>
        
        <div className="flex justify-between mb-2">
          <span className="text-lg font-bold text-blue-600">{property.price} ETH/month</span>
          <span className="text-gray-600">{property.bedrooms} bd | {property.bathrooms} ba</span>
        </div>
        
        <p className="text-gray-600 mb-2 truncate">{property.address}, {property.city}, {property.state}</p>
        
        <p className="text-gray-500 mb-3 line-clamp-2">{property.description}</p>
        
        {property.blockchain_id && (
          <div className="mb-2 text-xs text-gray-500">
            Blockchain ID: {property.blockchain_id}
          </div>
        )}
        
        {property.owner_id && (
          <div className="mb-3 text-xs text-gray-500">
            Owner: {shortenAddress(property.owner_address || property.owner_id)}
          </div>
        )}
        
        <div className="flex justify-between">
          <Link 
            to={`/properties/${property.id}`}
            className="text-blue-600 hover:text-blue-800 font-medium"
          >
            View Details
          </Link>
          
          <span className={`px-2 py-1 rounded-full text-xs font-semibold ${
            property.available 
              ? 'bg-green-100 text-green-800' 
              : 'bg-red-100 text-red-800'
          }`}>
            {property.available ? 'Available' : 'Rented'}
          </span>
        </div>
      </div>
    </div>
  );
};

export default PropertyCard; 