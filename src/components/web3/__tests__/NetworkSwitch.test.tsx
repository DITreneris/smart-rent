import React from 'react';
import { render } from '@testing-library/react';
import { NetworkSwitch } from '../NetworkSwitch';
import { Web3Provider } from '../../../contexts/Web3Context';

// Mock the Network utils
jest.mock('../../../utils/networkUtils', () => ({
  SUPPORTED_NETWORKS: {
    1: 'Ethereum Mainnet',
    5: 'Goerli Testnet'
  }
}));

describe('NetworkSwitch', () => {
  it('renders without crashing', () => {
    render(
      <Web3Provider>
        <NetworkSwitch />
      </Web3Provider>
    );
  });
}); 