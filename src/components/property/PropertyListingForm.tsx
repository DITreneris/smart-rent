import React, { useState } from 'react';
import { useWeb3Context } from '../../contexts/Web3Context';
import { useAuth } from '../../contexts/AuthContext';
import { usePropertyService } from '../../services/PropertyService';
import { TransactionStatus } from '../web3/TransactionStatus';
import { NetworkSwitch } from '../web3/NetworkSwitch';
import LoadingSpinner from '../common/LoadingSpinner';
import { PropertyCreate } from '../../types/property';
import { useForm } from 'react-hook-form';
import { zodResolver } from '@hookform/resolvers/zod';
import { propertyCreateSchema, PropertyCreateSchema } from '../../validations/propertySchema';

export const PropertyListingForm: React.FC = () => {
  const { isConnected } = useWeb3Context();
  const { user } = useAuth();
  const propertyService = usePropertyService();
  
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [txState, setTxState] = useState(null);
  const [error, setError] = useState<string | null>(null);
  
  const { 
    register, 
    handleSubmit, 
    formState: { errors }, 
    reset 
  } = useForm<PropertyCreateSchema>({
    resolver: zodResolver(propertyCreateSchema),
    defaultValues: {
      title: '',
      description: '',
      price: 0,
      bedrooms: 1,
      bathrooms: 1,
      area: 0,
      address: {
        street: '',
        city: '',
        state: '',
        postalCode: '',
        country: '',
      },
      amenities: [],
      images: [],
    },
  });

  const handleChange = (e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement>) => {
    const { name, value } = e.target;
    
    if (name.includes('.')) {
      const [parent, child] = name.split('.');
      reset(prev => ({
        ...prev,
        [parent]: {
          ...prev[parent],
          [child]: value
        }
      }));
    } else {
      reset(prev => ({
        ...prev,
        [name]: value
      }));
    }
  };

  const handleSubmitForm = async (e: React.FormEvent) => {
    e.preventDefault();
    setIsSubmitting(true);
    setError(null);
    setTxState(null);

    try {
      const { property, txState } = await propertyService.createProperty(reset());
      setTxState(txState);
    } catch (error) {
      setError(error.message || 'Failed to create property');
    } finally {
      setIsSubmitting(false);
    }
  };

  return (
    <div>
      {/* Render your form components here */}
    </div>
  );
}; 