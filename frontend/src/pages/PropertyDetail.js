import React, { useState, useEffect } from 'react';
import { useParams, Link } from 'react-router-dom';
import axios from 'axios';
import { useWeb3 } from '../contexts/Web3Context';
import { FaBed, FaBath, FaRulerCombined, FaMapMarkerAlt, FaEthereum } from 'react-icons/fa';

const PropertyDetail = () => {
  const { id } = useParams();
  const [property, setProperty] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [paymentMethod, setPaymentMethod] = useState('traditional');
  const [rentSubmitting, setRentSubmitting] = useState(false);
  const [rentSuccess, setRentSuccess] = useState(false);
  const [rentError, setRentError] = useState(null);

  const { isConnected, account, rentalContract, connectWallet } = useWeb3();

  // ETH conversion rate from environment variable
  const ethPrice = process.env.REACT_APP_ETH_USD_PRICE || 1800; // Default to $1800 if not set
  
  // Fetch property details
  useEffect(() => {
    const fetchProperty = async () => {
      try {
        setLoading(true);
        if (process.env.REACT_APP_ENABLE_TEST_MODE === 'true') {
          // Mock data for testing
          setTimeout(() => {
            setProperty({
              id: parseInt(id),
              title: 'Luxury Waterfront Apartment',
              description: 'This beautiful waterfront apartment offers stunning views of the bay. It has been recently renovated with high-end finishes throughout. The open concept living area features floor-to-ceiling windows, and the gourmet kitchen is equipped with state-of-the-art appliances. The spacious master bedroom includes a walk-in closet and en-suite bathroom with a soaking tub.',
              address: '123 Waterfront Ave',
              city: 'Bay City',
              state: 'CA',
              zip: '94111',
              price: 2500,
              bedrooms: 2,
              bathrooms: 2,
              area: 1200,
              property_type: 'apartment',
              available_from: '2023-08-01',
              is_favorite: false,
              landlord: {
                id: 1,
                name: 'John Smith',
                email: 'john@example.com',
                phone: '(555) 123-4567'
              },
              features: [
                'In-unit laundry',
                'Air conditioning',
                'Balcony',
                'Hardwood floors',
                'Gym access',
                'Swimming pool',
                'Covered parking',
                'Pet friendly'
              ],
              image_url: 'https://images.unsplash.com/photo-1512917774080-9991f1c4c750?w=800&auto=format&fit=crop',
              images: [
                'https://images.unsplash.com/photo-1512917774080-9991f1c4c750?w=800&auto=format&fit=crop',
                'https://images.unsplash.com/photo-1512917774080-9991f1c4c750?w=800&auto=format&fit=crop&q=80',
                'https://images.unsplash.com/photo-1512917774080-9991f1c4c750?w=800&auto=format&fit=crop&q=60'
              ]
            });
            setLoading(false);
          }, 1000);
        } else {
          const response = await axios.get(`${process.env.REACT_APP_API_URL}/properties/${id}`);
          setProperty(response.data);
          setLoading(false);
        }
      } catch (err) {
        console.error('Error fetching property details:', err);
        setError('Failed to load property details. Please try again later.');
        setLoading(false);
      }
    };

    fetchProperty();
  }, [id]);

  // Calculate ETH amount
  const calculateEthAmount = (usdAmount) => {
    return (usdAmount / ethPrice).toFixed(5);
  };

  // Handle rental payment
  const handleRentPayment = async () => {
    if (paymentMethod === 'ethereum' && !isConnected) {
      try {
        await connectWallet();
      } catch (err) {
        setRentError('Failed to connect wallet. Please try again.');
        return;
      }
    }

    setRentSubmitting(true);
    setRentError(null);

    try {
      if (paymentMethod === 'ethereum') {
        if (!rentalContract) {
          throw new Error('Smart contract not initialized. Please try again.');
        }

        // In a real app, this would interact with the rental smart contract
        // const ethAmount = calculateEthAmount(property.price);
        // const tx = await rentalContract.payRent(property.id, { value: ethers.parseEther(ethAmount) });
        // await tx.wait();
        
        // Mock successful payment for now
        await new Promise(resolve => setTimeout(resolve, 2000));
        
        setRentSuccess(true);
      } else {
        // Traditional payment flow
        // Redirect to payment processor or show form
        await new Promise(resolve => setTimeout(resolve, 2000));
        setRentSuccess(true);
      }
    } catch (err) {
      console.error('Payment error:', err);
      setRentError(err.message || 'Payment failed. Please try again.');
    } finally {
      setRentSubmitting(false);
    }
  };

  if (loading) return <div className="text-center py-10">Loading property details...</div>;
  if (error) return <div className="text-center py-10 text-red-600">{error}</div>;
  if (!property) return <div className="text-center py-10">Property not found</div>;

  const ethAmount = calculateEthAmount(property.price);

  return (
    <div>
      {/* Property Images */}
      <div className="relative mb-8">
        <div className="h-96 bg-gray-200 rounded-lg overflow-hidden">
          <img 
            src={property.image_url || property.images?.[0]} 
            alt={property.title}
            className="w-full h-full object-cover"
          />
        </div>
        
        {property.images && property.images.length > 1 && (
          <div className="flex overflow-x-auto gap-4 mt-4 pb-2">
            {property.images.map((image, index) => (
              <img 
                key={index}
                src={image} 
                alt={`${property.title} - view ${index + 1}`}
                className="h-24 w-40 object-cover rounded-md cursor-pointer flex-shrink-0"
                onClick={() => {
                  const updatedProperty = {...property};
                  updatedProperty.image_url = image;
                  setProperty(updatedProperty);
                }}
              />
            ))}
          </div>
        )}
      </div>
      
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
        {/* Property Details */}
        <div className="lg:col-span-2">
          <div className="bg-white rounded-lg shadow-md p-6 mb-8">
            <div className="flex justify-between items-start mb-4">
              <div>
                <h1 className="text-3xl font-bold text-gray-800 mb-2">{property.title}</h1>
                <div className="flex items-center text-gray-600 mb-1">
                  <FaMapMarkerAlt className="mr-2 text-red-500" />
                  <span>{property.address}, {property.city}, {property.state} {property.zip}</span>
                </div>
              </div>
              <div className="text-right">
                <div className="text-2xl font-bold text-blue-600">${property.price}/month</div>
                <div className="flex items-center text-blue-500 font-medium">
                  <FaEthereum className="mr-1" />
                  <span>{ethAmount} ETH/month</span>
                </div>
              </div>
            </div>
            
            <div className="grid grid-cols-3 gap-4 py-4 border-t border-b border-gray-200 my-4">
              <div className="flex flex-col items-center">
                <div className="flex items-center text-gray-700 mb-1">
                  <FaBed className="mr-2 text-blue-500" />
                  <span className="font-medium">{property.bedrooms}</span>
                </div>
                <span className="text-sm text-gray-500">Bedrooms</span>
              </div>
              <div className="flex flex-col items-center">
                <div className="flex items-center text-gray-700 mb-1">
                  <FaBath className="mr-2 text-blue-500" />
                  <span className="font-medium">{property.bathrooms}</span>
                </div>
                <span className="text-sm text-gray-500">Bathrooms</span>
              </div>
              <div className="flex flex-col items-center">
                <div className="flex items-center text-gray-700 mb-1">
                  <FaRulerCombined className="mr-2 text-blue-500" />
                  <span className="font-medium">{property.area}</span>
                </div>
                <span className="text-sm text-gray-500">Sq. Ft.</span>
              </div>
            </div>
            
            <h2 className="text-xl font-semibold text-gray-800 mb-3">Description</h2>
            <p className="text-gray-600 mb-6">{property.description}</p>
            
            {property.features && property.features.length > 0 && (
              <>
                <h2 className="text-xl font-semibold text-gray-800 mb-3">Features</h2>
                <ul className="grid grid-cols-2 gap-2 mb-6">
                  {property.features.map((feature, index) => (
                    <li key={index} className="flex items-center text-gray-600">
                      <span className="mr-2 text-green-500">✓</span>
                      {feature}
                    </li>
                  ))}
                </ul>
              </>
            )}
            
            {property.landlord && (
              <>
                <h2 className="text-xl font-semibold text-gray-800 mb-3">Landlord Information</h2>
                <div className="bg-gray-50 p-4 rounded-md">
                  <p className="font-medium text-gray-800">{property.landlord.name}</p>
                  <p className="text-gray-600">Email: {property.landlord.email}</p>
                  <p className="text-gray-600">Phone: {property.landlord.phone}</p>
                </div>
              </>
            )}
          </div>
        </div>
        
        {/* Sidebar */}
        <div>
          <div className="bg-white rounded-lg shadow-md p-6 mb-8">
            <h2 className="text-xl font-semibold text-gray-800 mb-4">Interested in this property?</h2>
            
            {/* Payment Options */}
            <div className="mb-6">
              <h3 className="font-medium text-gray-700 mb-2">Payment Method</h3>
              <div className="flex flex-col space-y-2">
                <label className="flex items-center cursor-pointer p-2 border rounded-md hover:bg-gray-50">
                  <input
                    type="radio"
                    name="paymentMethod"
                    value="traditional"
                    checked={paymentMethod === 'traditional'}
                    onChange={() => setPaymentMethod('traditional')}
                    className="mr-2"
                  />
                  <span>Traditional (Credit Card/Bank Transfer)</span>
                </label>
                <label className="flex items-center cursor-pointer p-2 border rounded-md hover:bg-gray-50">
                  <input
                    type="radio"
                    name="paymentMethod"
                    value="ethereum"
                    checked={paymentMethod === 'ethereum'}
                    onChange={() => setPaymentMethod('ethereum')}
                    className="mr-2"
                  />
                  <div className="flex items-center">
                    <FaEthereum className="mr-1 text-blue-500" />
                    <span>Pay with Ethereum ({ethAmount} ETH)</span>
                  </div>
                </label>
              </div>
            </div>
            
            {paymentMethod === 'ethereum' && !isConnected && (
              <div className="bg-blue-50 border border-blue-200 rounded-md p-3 mb-4">
                <p className="text-sm text-blue-800">
                  You need to connect your Ethereum wallet to proceed with payment.
                </p>
              </div>
            )}
            
            {rentSuccess ? (
              <div className="bg-green-50 border border-green-200 rounded-md p-4 mb-4">
                <p className="text-green-800 font-medium">Your rental request has been submitted successfully!</p>
                <p className="text-green-700 text-sm mt-1">The landlord will contact you soon with next steps.</p>
              </div>
            ) : (
              <button
                onClick={handleRentPayment}
                disabled={rentSubmitting}
                className={`w-full py-3 px-4 rounded-md font-medium text-white ${
                  rentSubmitting 
                    ? 'bg-gray-400 cursor-not-allowed' 
                    : paymentMethod === 'ethereum' 
                      ? 'bg-blue-600 hover:bg-blue-700' 
                      : 'bg-green-600 hover:bg-green-700'
                }`}
              >
                {rentSubmitting 
                  ? 'Processing...' 
                  : paymentMethod === 'ethereum' && !isConnected 
                    ? 'Connect Wallet to Pay' 
                    : `Submit Rental Application`
                }
              </button>
            )}
            
            {rentError && (
              <div className="mt-3 text-red-600 text-sm">
                Error: {rentError}
              </div>
            )}
            
            <div className="mt-6">
              <Link 
                to="/properties" 
                className="block text-center text-blue-600 hover:text-blue-800"
              >
                ← Back to all properties
              </Link>
            </div>
          </div>
          
          {/* Ethereum Information */}
          {paymentMethod === 'ethereum' && (
            <div className="bg-blue-50 rounded-lg shadow-md p-6">
              <h3 className="text-lg font-semibold text-blue-800 mb-3">
                <FaEthereum className="inline mr-1" /> Ethereum Payment
              </h3>
              <p className="text-blue-700 mb-3">
                Paying with cryptocurrency offers:
              </p>
              <ul className="text-blue-700 text-sm mb-4 space-y-2">
                <li className="flex items-start">
                  <span className="mr-2 font-bold">•</span>
                  Instant, secure transactions through smart contracts
                </li>
                <li className="flex items-start">
                  <span className="mr-2 font-bold">•</span>
                  No middlemen or bank fees
                </li>
                <li className="flex items-start">
                  <span className="mr-2 font-bold">•</span>
                  Automatic rental agreement generation
                </li>
                <li className="flex items-start">
                  <span className="mr-2 font-bold">•</span>
                  Transparent payment history on the blockchain
                </li>
              </ul>
              {isConnected && (
                <div className="bg-white rounded p-3 text-xs text-gray-600 break-all">
                  Connected Wallet: {account}
                </div>
              )}
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

export default PropertyDetail; 