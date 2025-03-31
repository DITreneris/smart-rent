import { renderHook, act } from '@testing-library/react-hooks';
import { useWeb3Context, Web3Provider } from '../Web3Context';
import { mockWeb3Provider } from '../../utils/test-utils';

describe('Web3Context', () => {
  beforeEach(() => {
    global.ethereum = mockWeb3Provider;
    jest.clearAllMocks();
  });

  it('should initialize with disconnected state', () => {
    const { result } = renderHook(() => useWeb3Context(), {
      wrapper: Web3Provider,
    });

    expect(result.current.isConnected).toBe(false);
    expect(result.current.account).toBeNull();
    expect(result.current.chainId).toBeNull();
  });

  it('should connect wallet successfully', async () => {
    mockWeb3Provider.request
      .mockResolvedValueOnce(['0x123'])  // eth_requestAccounts
      .mockResolvedValueOnce('0x1');     // eth_chainId

    const { result } = renderHook(() => useWeb3Context(), {
      wrapper: Web3Provider,
    });

    await act(async () => {
      await result.current.connect();
    });

    expect(result.current.isConnected).toBe(true);
    expect(result.current.account).toBe('0x123');
    expect(result.current.chainId).toBe(1);
  });

  it('should handle connection errors', async () => {
    mockWeb3Provider.request.mockRejectedValueOnce(new Error('User rejected'));

    const { result } = renderHook(() => useWeb3Context(), {
      wrapper: Web3Provider,
    });

    await act(async () => {
      try
}); 