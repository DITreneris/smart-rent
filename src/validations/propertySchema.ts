import { z } from 'zod';

export const addressSchema = z.object({
  street: z.string().min(1, 'Street is required'),
  city: z.string().min(1, 'City is required'),
  state: z.string().min(1, 'State is required'),
  postalCode: z.string().min(1, 'Postal code is required'),
  country: z.string().min(1, 'Country is required'),
});

export const propertyCreateSchema = z.object({
  title: z.string().min(3, 'Title must be at least 3 characters'),
  description: z.string().min(10, 'Description must be at least 10 characters'),
  price: z.number().positive('Price must be positive'),
  bedrooms: z.number().int().nonnegative('Bedrooms must be a non-negative integer'),
  bathrooms: z.number().nonnegative('Bathrooms must be a non-negative number'),
  area: z.number().positive('Area must be positive'),
  address: addressSchema,
  amenities: z.array(z.string()),
  images: z.array(z.string().url('Invalid image URL')),
  metadataURI: z.string().optional(),
});

export type PropertyCreateSchema = z.infer<typeof propertyCreateSchema>; 