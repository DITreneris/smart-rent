export enum TransactionStatus {
  PENDING = 'PENDING',
  MINING = 'MINING',
  COMPLETED = 'COMPLETED',
  FAILED = 'FAILED'
}

interface TransactionState {
  status: TransactionStatus;
  hash: string;
  error?: string;
  confirmations: number;
}

export class TransactionTracker {
  private static readonly REQUIRED_CONFIRMATIONS = 2;

  static async trackTransaction(
    txPromise: Promise<ethers.ContractTransaction>
  ): Promise<TransactionState> {
    try {
      // Initial state
      const state: TransactionState = {
        status: TransactionStatus.PENDING,
        hash: '',
        confirmations: 0
      };

      // Wait for transaction submission
      const tx = await txPromise;
      state.hash = tx.hash;
      state.status = TransactionStatus.MINING;

      // Wait for confirmations
      const receipt = await tx.wait(this.REQUIRED_CONFIRMATIONS);
      
      state.status = TransactionStatus.COMPLETED;
      state.confirmations = receipt.confirmations;
      
      return state;
    } catch (error) {
      return {
        status: TransactionStatus.FAILED,
        hash: '',
        error: error.message,
        confirmations: 0
      };
    }
  }
} 