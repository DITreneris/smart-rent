import { TransactionStatus } from '../utils/transactionTracker';

/**
 * Represents a blockchain transaction in the application
 */
export interface Transaction {
  id: string;          // Unique identifier for the transaction
  hash: string;        // Transaction hash from the blockchain
  status: TransactionStatus;  // Current status of the transaction
  timestamp: number;   // When the transaction was created
  description: string; // Human-readable description
  type: TransactionType; // Type of transaction
  amount?: string;     // Amount involved (if applicable)
  from?: string;       // Sender address
  to?: string;         // Recipient address
  confirmations?: number; // Number of confirmations
  error?: string;      // Error message if transaction failed
  receipt?: any;       // Transaction receipt data
  metadata?: Record<string, any>; // Additional transaction data
}

/**
 * Types of transactions in the system
 */
export enum TransactionType {
  PROPERTY_LISTING = 'PROPERTY_LISTING',
  PROPERTY_RENTAL = 'PROPERTY_RENTAL',
  RENTAL_PAYMENT = 'RENTAL_PAYMENT',
  RENTAL_COMPLETION = 'RENTAL_COMPLETION',
  CONTRACT_INTERACTION = 'CONTRACT_INTERACTION',
  WALLET_TRANSFER = 'WALLET_TRANSFER'
}

/**
 * Receipts generated for transactions
 */
export interface TransactionReceipt {
  transactionId: string;
  transactionHash: string;
  timestamp: number;
  amount?: string;
  description: string;
  from: string;
  to: string;
  status: TransactionStatus;
  metadata?: Record<string, any>;
  pdfUrl?: string;
} 