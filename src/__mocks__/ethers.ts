// Mock implementation for ethers
const mockEthers = {
  providers: {
    Web3Provider: jest.fn().mockImplementation(() => ({
      getSigner: jest.fn().mockReturnValue({
        getAddress: jest.fn().mockResolvedValue('0x1234567890123456789012345678901234567890'),
        getChainId: jest.fn().mockResolvedValue(1),
        getBalance: jest.fn().mockResolvedValue('1000000000000000000')
      }),
      getNetwork: jest.fn().mockResolvedValue({ chainId: 1, name: 'Mainnet' })
    }))
  },
  Contract: jest.fn().mockImplementation(() => ({
    listProperty: jest.fn().mockResolvedValue({
      wait: jest.fn().mockResolvedValue({ status: 1 })
    }),
    rentProperty: jest.fn().mockResolvedValue({
      wait: jest.fn().mockResolvedValue({ status: 1 })
    }),
    connect: jest.fn().mockReturnThis()
  })),
  utils: {
    parseEther: jest.fn().mockImplementation(value => value + '000000000000000000'),
    formatEther: jest.fn().mockImplementation(value => value.replace('000000000000000000', ''))
  }
};

module.exports = mockEthers; 