export const formatAddress = (address: string | null | undefined): string => {
  if (!address) return '';
  return `${address.substring(0, 6)}...${address.substring(address.length - 4)}`;
};

export const isValidEthereumAddress = (address: string | null | undefined): boolean => {
  if (!address) return false;
  return /^0x[a-fA-F0-9]{40}$/.test(address);
};

export const formatEther = (wei: string | null | undefined): string => {
  if (!wei) return '0';
  const etherValue = Number(wei) / 1e18;
  return etherValue.toFixed(2);
};

export const parseEther = (ether: string | null | undefined): string => {
  if (!ether) return '0';
  const weiValue = Number(ether) * 1e18;
  return weiValue.toString();
}; 