import { PropertyService } from '../PropertyService';
import { mockContractCalls } from '../../utils/test-utils';

describe('PropertyService', () => {
  let propertyService: PropertyService;

  beforeEach(() => {
    propertyService = new PropertyService(
      'test-contract-address',
      mockContractCalls
    );
  });

  it('should list property successfully', async () => {
    const propertyData = {
      title: 'Test Property',
      description: 'Test Description',
      price: 1,
      bedrooms: 2,
      bathrooms: 1,
      area: 100,
      images: ['image1.jpg'],
      amenities: ['wifi'],
      address: {
        street: '123 Test St',
        city: 'Test City',
        state: 'TS',
        postalCode: '12345',
        country: 'Test Country'
      }
    };

    mockContractCalls.listProperty.mockResolvedValueOnce({
      wait: () => Promise.resolve({ status: 1 }),
      hash: '0x123'
    });

    const result = await propertyService.listProperty(propertyData);

    expect(result.txState.status).toBe('COMPLETED');
    expect(mockContractCalls.listProperty).toHaveBeenCalledWith(
      expect.any(String),
      expect.any(Number),
      expect.any(Number)
    );
  });

  it('should handle listing errors', async () => {
    mockContractCalls.listProperty.mockRejectedValueOnce(
      new Error('Transaction failed')
    );

    await expect(propertyService.listProperty({} as any)).rejects.toThrow(
      'Transaction failed'
    );
  });
}); 