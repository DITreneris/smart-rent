// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

/**
 * @title RentalAgreement
 * @dev Smart contract for managing rental agreements between landlords and tenants
 */
contract RentalAgreement {
    // Enum for different states of the rental agreement
    enum Status { 
        Active,     // Agreement is active
        Terminated, // Agreement is terminated early
        Completed   // Agreement reached its end date
    }
    
    // Rental agreement struct
    struct Agreement {
        address landlord;
        address tenant;
        uint256 propertyId;
        uint256 startDate;
        uint256 endDate;
        uint256 monthlyRent;
        uint256 securityDeposit;
        Status status;
        bool securityDepositReturned;
    }
    
    // Contract details
    Agreement public agreement;
    
    // Events
    event AgreementCreated(address landlord, address tenant, uint256 propertyId);
    event RentPaid(address tenant, uint256 amount, uint256 timestamp);
    event AgreementTerminated(uint256 timestamp, Status status);
    event SecurityDepositReturned(address tenant, uint256 amount, uint256 timestamp);
    
    // Modifiers
    modifier onlyLandlord() {
        require(msg.sender == agreement.landlord, "Only landlord can call this function");
        _;
    }
    
    modifier onlyTenant() {
        require(msg.sender == agreement.tenant, "Only tenant can call this function");
        _;
    }
    
    modifier agreementActive() {
        require(agreement.status == Status.Active, "Agreement is not active");
        _;
    }
    
    /**
     * @dev Constructor to create a new rental agreement
     * @param _tenant Address of the tenant
     * @param _propertyId ID of the property being rented
     * @param _startDate Start date of the rental period (Unix timestamp)
     * @param _endDate End date of the rental period (Unix timestamp)
     * @param _monthlyRent Monthly rent amount in wei
     */
    constructor(
        address _tenant,
        uint256 _propertyId,
        uint256 _startDate,
        uint256 _endDate,
        uint256 _monthlyRent
    ) {
        require(_tenant != address(0), "Invalid tenant address");
        require(_startDate < _endDate, "End date must be after start date");
        require(_monthlyRent > 0, "Monthly rent must be greater than 0");
        
        agreement.landlord = msg.sender;
        agreement.tenant = _tenant;
        agreement.propertyId = _propertyId;
        agreement.startDate = _startDate;
        agreement.endDate = _endDate;
        agreement.monthlyRent = _monthlyRent;
        agreement.securityDeposit = _monthlyRent * 2; // Security deposit is 2 months' rent
        agreement.status = Status.Active;
        agreement.securityDepositReturned = false;
        
        emit AgreementCreated(msg.sender, _tenant, _propertyId);
    }
    
    /**
     * @dev Function for tenant to pay rent
     */
    function payRent() external payable onlyTenant agreementActive {
        require(msg.value == agreement.monthlyRent, "Amount should equal monthly rent");
        
        // Transfer rent to landlord
        (bool success, ) = agreement.landlord.call{value: msg.value}("");
        require(success, "Transfer to landlord failed");
        
        emit RentPaid(msg.sender, msg.value, block.timestamp);
    }
    
    /**
     * @dev Function for tenant to pay security deposit
     */
    function paySecurityDeposit() external payable onlyTenant agreementActive {
        require(msg.value == agreement.securityDeposit, "Amount should equal security deposit");
        
        emit RentPaid(msg.sender, msg.value, block.timestamp);
    }
    
    /**
     * @dev Function for landlord to terminate the agreement
     */
    function terminateAgreement() external onlyLandlord agreementActive {
        agreement.status = Status.Terminated;
        
        emit AgreementTerminated(block.timestamp, Status.Terminated);
    }
    
    /**
     * @dev Function for landlord to mark agreement as completed
     */
    function completeAgreement() external onlyLandlord agreementActive {
        require(block.timestamp >= agreement.endDate, "Agreement end date not reached");
        
        agreement.status = Status.Completed;
        
        emit AgreementTerminated(block.timestamp, Status.Completed);
    }
    
    /**
     * @dev Function for landlord to return security deposit to tenant
     */
    function returnSecurityDeposit() external payable onlyLandlord {
        require(agreement.status != Status.Active, "Agreement must be terminated or completed");
        require(!agreement.securityDepositReturned, "Security deposit already returned");
        require(address(this).balance >= agreement.securityDeposit, "Contract doesn't have enough balance");
        
        agreement.securityDepositReturned = true;
        
        // Transfer security deposit to tenant
        (bool success, ) = agreement.tenant.call{value: agreement.securityDeposit}("");
        require(success, "Transfer to tenant failed");
        
        emit SecurityDepositReturned(agreement.tenant, agreement.securityDeposit, block.timestamp);
    }
    
    /**
     * @dev Function to get the current agreement details
     */
    function getAgreementDetails() external view returns (
        address landlord,
        address tenant,
        uint256 propertyId,
        uint256 startDate,
        uint256 endDate,
        uint256 monthlyRent,
        uint256 securityDeposit,
        Status status,
        bool securityDepositReturned
    ) {
        return (
            agreement.landlord,
            agreement.tenant,
            agreement.propertyId,
            agreement.startDate,
            agreement.endDate,
            agreement.monthlyRent,
            agreement.securityDeposit,
            agreement.status,
            agreement.securityDepositReturned
        );
    }
    
    /**
     * @dev Function to get the contract balance
     */
    function getContractBalance() external view returns (uint256) {
        return address(this).balance;
    }
} 