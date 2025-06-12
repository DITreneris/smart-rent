# Encryption Standard

## Document Information
- **Document ID**: ISMS-STD-002
- **Version**: 1.0
- **Effective Date**: April 15, 2025
- **Review Date**: April 15, 2026
- **Status**: Draft

## 1. Purpose and Scope

### 1.1 Purpose
This standard defines the requirements for implementing and managing encryption to protect SmartRent's information assets. It establishes consistent practices for encryption across the organization to maintain the confidentiality, integrity, and authenticity of sensitive information during storage, processing, and transmission.

### 1.2 Scope
This standard applies to:
- All information systems storing, processing, or transmitting sensitive information
- All electronic communications containing sensitive information
- All portable devices and removable media used to store SmartRent data
- All cloud services and third-party systems storing or processing SmartRent data
- All employees, contractors, and third parties with access to SmartRent information assets

## 2. Encryption Requirements

### 2.1 Data Classification and Encryption

Encryption requirements are based on data classification:

| Data Classification | Data at Rest | Data in Transit | Example Data Types |
|---------------------|--------------|-----------------|-------------------|
| Public | Not Required | Not Required | Public website content, marketing materials |
| Internal | Not Required | Required | Internal communications, non-sensitive business documents |
| Confidential | Required | Required | Customer records, employee information, financial data |
| Restricted | Required | Required | Authentication credentials, encryption keys, payment card data |

### 2.2 Approved Encryption Algorithms

#### 2.2.1 Symmetric Encryption
- **Approved Algorithms**:
  - AES-256 (preferred)
  - AES-192
  - AES-128
- **Deprecated Algorithms** (not to be used for new implementations):
  - 3DES
  - DES
  - RC4
  - Blowfish
  - Any algorithm with key length less than 128 bits

#### 2.2.2 Asymmetric Encryption
- **Approved Algorithms**:
  - RSA (minimum 2048 bits, 4096 bits recommended)
  - ECC (minimum 256 bits)
  - Diffie-Hellman (minimum 2048 bits)
- **Deprecated Algorithms** (not to be used for new implementations):
  - RSA with less than 2048-bit keys
  - Diffie-Hellman with less than 2048-bit keys

#### 2.2.3 Hashing Algorithms
- **Approved Algorithms**:
  - SHA-256 (minimum)
  - SHA-384
  - SHA-512
  - BLAKE2
  - Argon2 (for password hashing)
  - bcrypt (for password hashing)
  - PBKDF2 (for password hashing, minimum 10,000 iterations)
- **Deprecated Algorithms** (not to be used for new implementations):
  - MD5
  - SHA-1
  - RIPEMD-160
  - Any hash algorithm with output less than 256 bits

#### 2.2.4 Transport Encryption
- **Approved Protocols**:
  - TLS 1.2 (minimum)
  - TLS 1.3 (preferred)
  - IPsec with IKEv2
- **Deprecated Protocols** (not to be used for new implementations):
  - SSL (all versions)
  - TLS 1.0
  - TLS 1.1
  - PPTP VPN
  - IKEv1

### 2.3 Encryption Implementation Requirements

#### 2.3.1 Encryption Mode and Padding
- **Symmetric Encryption Modes**:
  - GCM (Galois/Counter Mode) - preferred
  - CCM (Counter with CBC-MAC)
  - CBC (Cipher Block Chaining) with PKCS#7 padding
- **Avoid using**:
  - ECB (Electronic Codebook) mode
  - CBC without proper padding
  - Any mode without integrity protection

#### 2.3.2 Initialization Vectors (IVs) and Nonces
- Must be randomly generated for each encryption operation
- Must be at least as long as the block size
- Must never be reused with the same key
- Must be transmitted or stored alongside the ciphertext

#### 2.3.3 Authentication and Integrity
- HMAC or authenticated encryption modes (e.g., AES-GCM) should be used
- Encryption without integrity verification is not permitted for sensitive data
- Digital signatures must use approved algorithms (RSA, ECDSA) with appropriate key lengths

## 3. Key Management

### 3.1 Key Generation

- All cryptographic keys must be generated using approved random number generators
- Hardware-based random number generators should be used when available
- Key generation must be performed in a secure environment
- Keys must meet minimum length requirements specified in section 2.2
- Keys must never be based on easily guessable information (e.g., dictionary words)

### 3.2 Key Storage

- Private and symmetric keys must be protected with access controls
- Keys protecting confidential or restricted data must be stored in a secure key management system
- Hardware Security Modules (HSMs) or secure key vaults should be used for high-value keys
- Keys must never be stored in cleartext in application code, configuration files, or databases
- Keys must be stored separately from the data they protect

### 3.3 Key Usage

- Each key should have a defined purpose (e.g., encryption, signing, authentication)
- Keys should not be used for multiple unrelated purposes
- Key access should be restricted to authorized personnel and systems
- Key usage must be logged and monitored

### 3.4 Key Rotation

| Key Type | Maximum Key Lifetime |
|----------|----------------------|
| Encryption keys for data at rest | 2 years |
| TLS certificates | 1 year |
| VPN certificates | 1 year |
| Code signing keys | 3 years |
| Root CA certificates | 10 years |
| Intermediate CA certificates | 5 years |
| SSH keys | 1 year |
| User authentication keys | 1 year |

- Key rotation must be performed before the maximum lifetime is reached
- Key rotation must be performed immediately if compromise is suspected
- Procedures must be in place to ensure business continuity during key rotation
- Old keys must be securely archived for data recovery purposes

### 3.5 Key Backup and Recovery

- Critical keys must be backed up to enable recovery in case of loss
- Key backups must be secured with the same level of protection as the original keys
- Recovery procedures must be documented and tested
- Split knowledge and dual control procedures should be implemented for critical keys
- Recovery of archived keys must follow formal authorization procedures

### 3.6 Key Destruction

- Keys must be securely destroyed when no longer needed
- Destruction must render the key irrecoverable
- Key destruction must be documented and verified
- All copies of the key must be identified and destroyed
- Hardware containing non-extractable keys must be securely decommissioned

## 4. Specific Implementation Requirements

### 4.1 Database Encryption

- Sensitive data in databases must be encrypted using column-level or cell-level encryption
- Database encryption keys must be stored separately from the database
- Database backup files containing sensitive data must be encrypted
- Transparent Data Encryption (TDE) may be used in addition to application-level encryption
- Database connection strings containing credentials must be encrypted in configuration files

### 4.2 File Encryption

- Files containing sensitive data must be encrypted when stored outside of secured environments
- Encrypted file systems or volumes should be used where appropriate
- File encryption keys must not be stored in the same location as the encrypted files
- Folder and file names should not reveal sensitive information about the contents

### 4.3 Email Encryption

- Emails containing confidential or restricted information must be encrypted
- S/MIME or PGP should be used for email encryption
- Encryption keys or certificates for email must follow the same management requirements
- Automatic email forwarding to external addresses should be prohibited or restricted

### 4.4 Mobile Devices and Removable Media

- Mobile devices storing sensitive data must implement full-disk encryption
- Removable media containing sensitive data must be encrypted
- Hardware-based encryption should be used where available
- Encryption must be verified before sensitive data is stored on the device

### 4.5 Cloud Services

- Data stored in cloud services must be encrypted in accordance with its classification
- Customer-managed encryption keys should be used where supported by the cloud provider
- Secure key management services provided by the cloud vendor may be used if they meet requirements
- Cloud backup and snapshot data must maintain the same encryption requirements as the source data

### 4.6 Network Encryption

- All web applications must use TLS 1.2 or higher
- Internal network traffic containing sensitive data should be encrypted
- Wireless networks must use WPA2-Enterprise or WPA3-Enterprise with AES encryption
- VPN connections must use approved encryption protocols
- Remote access to systems must use encrypted protocols

### 4.7 Application Encryption

- Applications handling sensitive data must implement encryption at the application layer
- Encryption libraries must be from trusted sources and kept updated
- Applications must validate the integrity of encrypted data before processing
- Applications must implement secure key management practices

## 5. Compliance and Exceptions

### 5.1 Compliance Verification

- Regular reviews of encryption implementation must be conducted
- Automated scanning tools should be used to detect non-compliant encryption
- Penetration testing should include validation of encryption implementations
- Encryption key management procedures should be audited annually

### 5.2 Exceptions

- Exceptions to this standard may be granted only when:
  - Technical limitations prevent compliance
  - Business requirements necessitate a deviation
  - Compensating controls provide equivalent security
- All exceptions must be:
  - Documented with a clear business justification
  - Approved by the CISO or designated security authority
  - Reviewed at least annually
  - Accompanied by compensating controls where possible

## 6. Roles and Responsibilities

### 6.1 Information Security Team
- Defines and maintains encryption standards
- Reviews and approves exceptions
- Conducts periodic reviews of encryption implementations
- Provides guidance on encryption technologies

### 6.2 IT Operations
- Implements encryption for infrastructure systems
- Manages encryption key lifecycle
- Maintains encryption systems and tools
- Monitors for encryption failures or issues

### 6.3 Development Teams
- Implements encryption in applications
- Ensures proper key management in application code
- Follows secure coding practices for cryptographic implementations

### 6.4 System Administrators
- Enables encryption on systems and services
- Configures encryption settings according to standards
- Implements key rotation procedures

### 6.5 All Employees
- Follows procedures for protecting encrypted data
- Reports suspected encryption failures or issues
- Uses encryption tools provided by the organization

## 7. Related Documents
- ISMS-POL-001 Information Security Policy
- ISMS-POL-007 Cryptographic Controls Policy
- ISMS-POL-004 Data Classification Policy
- ISMS-POL-006 Access Control Policy
- ISMS-STD-001 Password Standard

## 8. Definitions
- **Encryption**: The process of converting information or data into a code to prevent unauthorized access
- **Symmetric Encryption**: Encryption that uses the same key for both encryption and decryption
- **Asymmetric Encryption**: Encryption that uses a public key for encryption and a private key for decryption
- **Hashing**: A one-way function that maps data of arbitrary size to a fixed-size string
- **Key**: A parameter that determines the output of a cryptographic algorithm
- **Initialization Vector (IV)**: A random value used with a cryptographic algorithm to ensure unique encryption results
- **Transport Layer Security (TLS)**: A cryptographic protocol designed to provide communications security over a computer network

## 9. Document History

| Version | Date | Description of Changes | Author | Approved By |
|---------|------|------------------------|--------|------------|
| 1.0 | April 15, 2025 | Initial version | Security Team | [APPROVER] | 