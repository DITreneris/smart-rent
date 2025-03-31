import React, { useState, useEffect } from 'react';
import { useWeb3Context } from '../../contexts/Web3Context';
import { TransactionStatus as TxStatus } from '../../utils/transactionTracker';
import { TransactionStatus } from './TransactionStatus';
import LoadingSpinner from '../common/LoadingSpinner';

interface Transaction {
  id: string;
  hash: string;
  status
} 