# Smart Rent Contract Form Component

The ContractForm component is a key part of the Smart Rent platform, allowing users to create new rental contracts backed by blockchain smart contracts.

## Overview

This component provides a form interface for users to input contract details like start/end dates, monthly rent amount, and security deposit. Upon submission, it:

1. Verifies the user has a connected crypto wallet
2. Creates a blockchain-backed rental agreement
3. Stores the agreement details in the platform's database
4. Provides feedback on success or failure

## Component Structure

```jsx
<ContractForm propertyId={123} propertyDetails={{...}} />
```

### Props

| Prop | Type | Description |
|------|------|-------------|
| `propertyId` | Number | ID of the property to create a contract for |
| `propertyDetails` | Object | Property information (optional, for display purposes) |

### State Variables

- `formData`: Tracks form field values (start date, end date, rent amount, deposit)
- `loading`: Boolean for loading state during submission
- `error`: String for any error messages
- `success`: Boolean for successful submissions

## Integration with Blockchain

The component interacts with the blockchain in these ways:

1. Checks if the user has a connected wallet via `useWeb3` hook
2. Creates a smart contract on the blockchain when the form is submitted
3. Stores the contract address in the database for future reference

## Usage Example

```jsx
import ContractForm from '../components/contracts/ContractForm';

const PropertyPage = ({ property }) => {
  return (
    <div>
      <h1>{property.title}</h1>
      <PropertyDetails property={property} />
      
      {/* Rental Contract Form */}
      <div className="mt-8">
        <h2>Create Rental Agreement</h2>
        <ContractForm 
          propertyId={property.id} 
          propertyDetails={property}
        />
      </div>
    </div>
  );
};
```

## Form Validation

The component validates several aspects:
- All required fields must be filled
- Start date must be before end date
- End date must be at least 30 days after start date
- Rent amount and security deposit must be positive values

## Responsive Design

The form is designed to be responsive:
- Full-width on mobile devices
- Two-column layout on tablets and desktop
- Accessible input fields with proper labels

## Future Enhancements

Planned improvements for this component:
- Support for additional contract terms (late fees, utilities included)
- Preview of the contract before submission
- Template selection for different types of rental agreements
- Document attachment support for supplementary materials 