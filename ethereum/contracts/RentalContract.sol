// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

/**
 * @title RentalContract
 * @dev Smart contract for managing property rental agreements on Smart Rent Platform
 */
contract RentalContract {
    // Status options for a rental agreement
    enum AgreementStatus { Pending, Active, Completed, Cancelled }
    
    // Structure to store rental agreement details
    struct RentalAgreement {
        string propertyId;          // Unique identifier for the property
        address tenant;             // Address of the tenant
        address landlord;           // Address of the landlord
        uint256 startDate;          // Start date as Unix timestamp
        uint256 endDate;            // End date as Unix timestamp
        uint256 monthlyRent;        // Monthly rent amount in Wei
        uint256 securityDeposit;    // Security deposit amount in Wei
        uint256 lastPaymentDate;    // Last payment date as Unix timestamp
        AgreementStatus status;     // Current status of the agreement
    }
    
    // Storage for agreements, mapped by agreement ID
    mapping(uint256 => RentalAgreement) public agreements;
    
    // Track agreements by tenant
    mapping(address => uint256[]) public tenantAgreements;
    
    // Track agreements by landlord
    mapping(address => uint256[]) public landlordAgreements;
    
    // Agreement ID counter
    uint256 public nextAgreementId = 1;
    
    // Events
    event AgreementCreated(uint256 indexed agreementId, address indexed tenant, address indexed landlord);
    event RentPaid(uint256 indexed agreementId, address indexed tenant, uint256 amount);
    event AgreementStatusChanged(uint256 indexed agreementId, AgreementStatus status);
    event SecurityDepositPaid(uint256 indexed agreementId, address indexed tenant, uint256 amount);
    event SecurityDepositReturned(uint256 indexed agreementId, address indexed tenant, uint256 amount);
    
    /**
     * @dev Create a new rental agreement
     * @param propertyId ID of the property
     * @param landlord Address of the landlord
     * @param startDate Start date as Unix timestamp
     * @param endDate End date as Unix timestamp
     * @param monthlyRent Monthly rent amount in Wei
     * @param securityDeposit Security deposit amount in Wei
     * @return ID of the created agreement
     */
    function createAgreement(
        string memory propertyId,
        address landlord,
        uint256 startDate,
        uint256 endDate,
        uint256 monthlyRent,
        uint256 securityDeposit
    ) public returns (uint256) {
        // Validate inputs
        require(startDate < endDate, "Start date must be before end date");
        require(monthlyRent > 0, "Monthly rent must be greater than zero");
        require(landlord != address(0), "Invalid landlord address");
        require(landlord != msg.sender, "Landlord cannot be the tenant");
        
        // Assign agreement ID and increment counter
        uint256 agreementId = nextAgreementId++;
        
        // Create agreement in storage
        agreements[agreementId] = RentalAgreement({
            propertyId: propertyId,
            tenant: msg.sender,
            landlord: landlord,
            startDate: startDate,
            endDate: endDate,
            monthlyRent: monthlyRent,
            securityDeposit: securityDeposit,
            lastPaymentDate: 0,
            status: AgreementStatus.Pending
        });
        
        // Track agreement under both tenant and landlord
        tenantAgreements[msg.sender].push(agreementId);
        landlordAgreements[landlord].push(agreementId);
        
        // Emit creation event
        emit AgreementCreated(agreementId, msg.sender, landlord);
        
        return agreementId;
    }
    
    /**
     * @dev Pay security deposit to activate agreement
     * @param agreementId ID of the agreement
     */
    function paySecurityDeposit(uint256 agreementId) public payable {
        // Get agreement from storage
        RentalAgreement storage agreement = agreements[agreementId];
        
        // Validate
        require(agreement.tenant == msg.sender, "Only tenant can pay security deposit");
        require(agreement.status == AgreementStatus.Pending, "Agreement not in pending status");
        require(msg.value == agreement.securityDeposit, "Incorrect security deposit amount");
        
        // Transfer security deposit to contract (held in escrow)
        // Security deposit remains in contract until agreement is completed or cancelled
        
        // Emit event
        emit SecurityDepositPaid(agreementId, msg.sender, msg.value);
    }
    
    /**
     * @dev Pay rent for an agreement
     * @param agreementId ID of the agreement
     */
    function payRent(uint256 agreementId) public payable {
        // Get agreement from storage
        RentalAgreement storage agreement = agreements[agreementId];
        
        // Validate
        require(agreement.tenant == msg.sender, "Only tenant can pay rent");
        require(agreement.status == AgreementStatus.Pending || agreement.status == AgreementStatus.Active, "Agreement not active");
        require(msg.value == agreement.monthlyRent, "Incorrect rent amount");
        
        // Update status if first payment
        if (agreement.status == AgreementStatus.Pending) {
            agreement.status = AgreementStatus.Active;
            emit AgreementStatusChanged(agreementId, AgreementStatus.Active);
        }
        
        // Update last payment date
        agreement.lastPaymentDate = block.timestamp;
        
        // Transfer payment to landlord
        (bool success, ) = agreement.landlord.call{value: msg.value}("");
        require(success, "Payment failed");
        
        // Emit payment event
        emit RentPaid(agreementId, msg.sender, msg.value);
    }
    
    /**
     * @dev Terminate an active agreement
     * @param agreementId ID of the agreement
     */
    function terminateAgreement(uint256 agreementId) public {
        // Get agreement from storage
        RentalAgreement storage agreement = agreements[agreementId];
        
        // Validate
        require(agreement.tenant == msg.sender || agreement.landlord == msg.sender, "Not authorized");
        require(agreement.status == AgreementStatus.Active, "Agreement not active");
        
        // Update status
        agreement.status = AgreementStatus.Completed;
        
        // Emit status change event
        emit AgreementStatusChanged(agreementId, AgreementStatus.Completed);
    }
    
    /**
     * @dev Return security deposit to tenant
     * @param agreementId ID of the agreement
     */
    function returnSecurityDeposit(uint256 agreementId) public {
        // Get agreement from storage
        RentalAgreement storage agreement = agreements[agreementId];
        
        // Only landlord can return security deposit
        require(agreement.landlord == msg.sender, "Only landlord can return security deposit");
        require(agreement.status == AgreementStatus.Completed, "Agreement not completed");
        
        // Transfer security deposit back to tenant
        (bool success, ) = agreement.tenant.call{value: agreement.securityDeposit}("");
        require(success, "Security deposit return failed");
        
        // Emit event
        emit SecurityDepositReturned(agreementId, agreement.tenant, agreement.securityDeposit);
    }
    
    /**
     * @dev Get a specific agreement details
     * @param agreementId ID of the agreement
     * @return Complete rental agreement details
     */
    function getAgreement(uint256 agreementId) public view returns (RentalAgreement memory) {
        require(agreementId < nextAgreementId, "Agreement does not exist");
        return agreements[agreementId];
    }
    
    /**
     * @dev Get all agreement IDs for a tenant
     * @param tenant Address of the tenant
     * @return Array of agreement IDs
     */
    function getAgreementsByTenant(address tenant) public view returns (uint256[] memory) {
        return tenantAgreements[tenant];
    }
    
    /**
     * @dev Get all agreement IDs for a landlord
     * @param landlord Address of the landlord
     * @return Array of agreement IDs
     */
    function getAgreementsByLandlord(address landlord) public view returns (uint256[] memory) {
        return landlordAgreements[landlord];
    }
    
    /**
     * @dev Check if an agreement is active
     * @param agreementId ID of the agreement
     * @return True if active, false otherwise
     */
    function isAgreementActive(uint256 agreementId) public view returns (bool) {
        return agreements[agreementId].status == AgreementStatus.Active;
    }
    
    /**
     * @dev Get current agreement count
     * @return Total number of agreements created
     */
    function getAgreementCount() public view returns (uint256) {
        return nextAgreementId - 1;
    }
} 