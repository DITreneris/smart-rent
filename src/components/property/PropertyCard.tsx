import React from 'react';

interface Property {
  id: string;
  title: string;
  description: string;
  price: string;
  image?: string;
  owner: string;
}

interface PropertyCardProps {
  property: Property;
  onClick?: (property: Property) => void;
}

const PropertyCard: React.FC<PropertyCardProps> = ({ property, onClick }) => {
  const handleClick = () => {
    if (onClick) {
      onClick(property);
    }
  };

  const handleImageError = (e: React.SyntheticEvent<HTMLImageElement, Event>) => {
    e.currentTarget.src = '/images/default-property.jpg';
  };

  return (
    <div className="property-card" onClick={handleClick} data-testid="property-card">
      <div className="property-image">
        <img 
          src={property.image || '/images/default-property.jpg'}
          alt={property.title}
          onError={handleImageError}
        />
      </div>
    </div>
  );
};

export default PropertyCard; 