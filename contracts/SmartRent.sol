// SPDX-License-Identifier: MIT
pragma solidity ^0.8.19;

// Import OpenZeppelin Ownable for basic access control
import "@openzeppelin/contracts/access/Ownable.sol";

contract SmartRent is Ownable {

    // Event emitted when a rental is confirmed on-chain
    event RentalConfirmed(
        bytes32 indexed rentalId,       // Unique off-chain generated ID for the rental agreement
        uint256 indexed propertyId,     // Identifier for the property (can be off-chain ID initially)
        address indexed tenant,
        address landlord,
        string metadataURI             // URI pointing to off-chain rental details (e.g., IPFS)
    );

    // --- Functions --- 

    /**
     * @notice Confirms a rental agreement by emitting an event.
     * @dev Can only be called by the contract owner (initially the deployer/platform).
     *      Access control can be refined later (e.g., only landlord involved).
     *      Ensures a verifiable, timestamped record of the confirmation.
     * @param rentalId Unique identifier for the rental agreement (generated off-chain).
     * @param propertyId Identifier for the property being rented.
     * @param tenant The address of the tenant.
     * @param landlord The address of the landlord.
     * @param metadataURI URI pointing to detailed rental agreement metadata (e.g., IPFS hash).
     */
    function confirmRental(
        bytes32 rentalId,
        uint256 propertyId,
        address tenant,
        address landlord,
        string calldata metadataURI
    ) external onlyOwner { // Restriction: Only owner can call this for MVP
        require(tenant != address(0), "SmartRent: Tenant address cannot be zero");
        require(landlord != address(0), "SmartRent: Landlord address cannot be zero");
        require(bytes(metadataURI).length > 0, "SmartRent: Metadata URI cannot be empty");

        emit RentalConfirmed(
            rentalId,
            propertyId,
            tenant,
            landlord,
            metadataURI
        );
    }

    // Constructor to set the initial owner
    constructor() Ownable(msg.sender) {}

    // Note: The Property struct is removed as state is managed off-chain for MVP
    // struct Property {
    //     uint256 id;
    //     address landlord;
    //     string metadataURI;  
    // }
} 