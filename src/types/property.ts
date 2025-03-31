export interface PropertyCreate {
  title: string;
  description: string;
  price: number;
  bedrooms: number;
  bathrooms: number;
  area: number;
  address: {
    street: string;
    city: string;
    state: string;
    postalCode: string;
    country: string;
  };
  amenities: string[];
  images: string[];
  metadataURI?: string;
  blockchain_id?: string;
}

export interface Property extends PropertyCreate {
  id: string;
  owner_id: string;
  createdAt: string;
  updatedAt: string;
  status: 'available' | 'rented' | 'pending';
}

export interface PropertyFilter {
  minPrice?: number;
  maxPrice?: number;
  minBedrooms?: number;
  maxBedrooms?: number;
  city?: string;
  state?: string;
  status?: 'available' | 'rented' | 'pending';
} 