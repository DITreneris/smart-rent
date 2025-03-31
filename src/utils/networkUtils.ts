export const SUPPORTED_NETWORKS = {
  1: 'Ethereum Mainnet',
  5: 'Goerli Testnet',
  11155111: 'Sepolia Testnet'
};

export class NetworkValidator {
  static async validateNetwork(provider: ethers.providers.Web3Provider): Promise<boolean> {
    const network = await provider.getNetwork();
    const chainId = network.chainId;

    if (!SUPPORTED_NETWORKS[chainId]) {
      throw new Error(`Unsupported network. Please connect to: ${Object.values(SUPPORTED_NETWORKS).join(', ')}`);
    }

    return true;
  }

  static async switchNetwork(provider: ethers.providers.Web3Provider, targetChainId: number): Promise<void> {
    try {
      await provider.send('wallet_switchEthereumChain', [
        { chainId: ethers.utils.hexValue(targetChainId) }
      ]);
    } catch (error) {
      throw new Error(`Failed to switch network: ${error.message}`);
    }
  }
} 