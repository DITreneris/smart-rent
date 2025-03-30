// SPDX-License-Identifier: MIT
pragma solidity ^0.8.19;

contract SmartRent {
    // Contract owner
    address public owner;
    
    // Property struct
    struct Property {
        uint256 id;
        address landlord;
        string metadataURI;  
    }
} 