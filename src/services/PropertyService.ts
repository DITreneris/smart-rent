import apiService from './ApiService';
import { ContractService } from '../utils/contractUtils';
import { Property, PropertyCreate, PropertyFilter } from '../types/property';
import { TransactionStatus } from '../utils/transactionTracker';
import { useWeb3Context } from '../contexts/Web3Context';

export class PropertyService {
  private contractService: ContractService;

  constructor(contractAddress: string, abi: any) {
    this.contractService = new ContractService(contractAddress, abi);
  }

  // Regular API methods
  async getProperties(filters?: PropertyFilter): Promise<Property[]> {
    return apiService.getProperties(filters);
  }

  async getPropertyById(id: string): Promise<Property> {
    return apiService.getPropertyById(id);
  }

  // Combined API + Blockchain methods
  async createProperty(propertyData: PropertyCreate): Promise<{ property: Property; txState: any }> {
    try {
      // First create in database
      const property = await apiService.createProperty(propertyData);
      
      // Then add to blockchain
      const metadataURI = propertyData.metadataURI || `ipfs://${property.id}`;
      const txState = await this.contractService.listProperty(
        metadataURI,
        propertyData.price,
        propertyData.price * 0.5 // Security deposit as 50% of monthly rent
      );
      
      // If transaction successful, update property with blockchain ID
      if (txState.status === TransactionStatus.COMPLETED) {
        const updatedProperty = await apiService.updateProperty(property.id, {
          blockchain_id: txState.blockchainPropertyId,
          metadataURI
        });
        return { property: updatedProperty, txState };
      }
      
      return { property, txState };
    } catch (error) {
      console.error('Error creating property:', error);
      throw new Error(`Failed to create property: ${error.message}`);
    }
  }

  async rentProperty(propertyId: string, duration: number): Promise<{ success: boolean; txState: any }> {
    try {
      // Get property from database
      const property = await apiService.getPropertyById(propertyId);
      
      if (!property.blockchain_id) {
        throw new Error('Property not available on blockchain');
      }
      
      // Calculate total payment (price * duration + security deposit)
      const totalPayment = property.price * duration + (property.price * 0.5);
      
      // Execute blockchain transaction
      const txState = await this.contractService.rentProperty(
        parseInt(property.blockchain_id),
        duration,
        totalPayment
      );
      
      return {
        success: txState.status === TransactionStatus.COMPLETED,
        txState
      };
    } catch (error) {
      console.error('Error renting property:', error);
      throw new Error(`Failed to rent property: ${error.message}`);
    }
  }
}

// Create a singleton using the hook
export const usePropertyService = () => {
  const { isConnected } = useWeb3Context();
  
  // Create service when Web3 is connected
  if (isConnected) {
    return new PropertyService(
      process.env.REACT_APP_CONTRACT_ADDRESS as string,
      CONTRACT_ABI
    );
  }
  
  // Fallback to API-only methods when Web3 is not connected
  return {
    getProperties: (filters?: PropertyFilter) => apiService.getProperties(filters),
    getPropertyById: (id: string) => apiService.getPropertyById(id),
    createProperty: async () => {
      throw new Error('Wallet connection required to create properties');
    },
    rentProperty: async () => {
      throw new Error('Wallet connection required to rent properties');
    }
  };
}; 