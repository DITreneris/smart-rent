import { ethers } from 'ethers';
import { ISmartRent } from '../types/contracts';
import { TransactionTracker, TransactionState } from './transactionTracker';

export class ContractService {
  private contract: ISmartRent;
  private provider: ethers.providers.Web3Provider;

  constructor(contractAddress: string, abi: ethers.ContractInterface) {
    this.provider = new ethers.providers.Web3Provider(window.ethereum);
    this.contract = new ethers.Contract(
      contractAddress,
      abi,
      this.provider.getSigner()
    ) as ISmartRent;
  }

  async listProperty(
    metadataURI: string,
    pricePerMonth: number,
    securityDeposit: number
  ): Promise<TransactionState> {
    try {
      // Validate inputs
      if (!metadataURI || pricePerMonth <= 0 || securityDeposit <= 0) {
        throw new Error('Invalid property listing parameters');
      }

      const txPromise = this.contract.listProperty(
        metadataURI,
        ethers.utils.parseEther(pricePerMonth.toString()),
        ethers.utils.parseEther(securityDeposit.toString())
      );

      return await TransactionTracker.trackTransaction(txPromise);
    } catch (error) {
      console.error('Error listing property:', error);
      throw new Error(`Failed to list property: ${error.message}`);
    }
  }

  async rentProperty(
    propertyId: number,
    duration: number,
    value: number
  ): Promise<TransactionState> {
    try {
      // Validate inputs
      if (propertyId < 0 || duration <= 0 || value <= 0) {
        throw new Error('Invalid rental parameters');
      }

      const txPromise = this.contract.rentProperty(
        propertyId,
        duration,
        { value: ethers.utils.parseEther(value.toString()) }
      );

      return await TransactionTracker.trackTransaction(txPromise);
    } catch (error) {
      console.error('Error renting property:', error);
      throw new Error(`Failed to rent property: ${error.message}`);
    }
  }
} 