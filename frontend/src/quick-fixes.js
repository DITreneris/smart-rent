// Quick fixes for Web3Context and WalletManagement

// Fix 1: Format address helper
export const formatWalletAddress = (address) => {
  if (!address || typeof address !== 'string') return '';
  return `${address.substring(0, 6)}...${address.substring(address.length - 4)}`;
};

// Fix 2: Balance formatting helper 
export const formatEthBalance = (balanceInEth) => {
  if (!balanceInEth) return '0.0000';
  return parseFloat(balanceInEth).toFixed(4);
};

// Fix 3: Mock transaction generator for testing
export const generateMockTransaction = () => {
  return {
    hash: '0x' + Array(64).fill(0).map(() => Math.floor(Math.random() * 16).toString(16)).join(''),
    success: true,
    timestamp: new Date().toISOString()
  };
};

// Fix 4: Utility to safely get balance
export const safeGetBalance = async (provider, address) => {
  try {
    if (!provider || !address) return null;
    const balanceWei = await provider.getBalance(address);
    return balanceWei.toString();
  } catch (error) {
    console.error("Error getting balance:", error);
    return null;
  }
}; 