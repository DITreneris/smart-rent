# Cryptographic Controls Policy

## Document Information
- **Document ID**: ISMS-POL-007
- **Version**: 1.0
- **Effective Date**: April 15, 2025
- **Review Date**: April 15, 2026
- **Status**: Draft

## 1. Purpose and Scope

### 1.1 Purpose
This Cryptographic Controls Policy establishes the requirements for the use of cryptographic controls within SmartRent to protect the confidentiality, integrity, authenticity, and non-repudiation of information. It provides direction for the proper selection, implementation, and management of cryptographic solutions to ensure adequate protection of sensitive information and compliance with relevant regulations and standards.

### 1.2 Scope
This policy applies to:
- All information systems, applications, and services owned or managed by SmartRent that require cryptographic controls
- All forms of data at rest, in use, or in transit that require protection through cryptographic means
- All employees, contractors, consultants, temporary staff, and third parties who implement or use cryptographic controls within SmartRent's environment
- All environments including production, test, development, and staging

## 2. Policy Statements

### 2.1 General Requirements

#### 2.1.1 Risk Assessment
- The need for cryptographic controls shall be determined based on a risk assessment
- The level of protection shall be commensurate with the classification of the information and identified risks
- Regulatory and contractual requirements shall be considered when implementing cryptographic controls

#### 2.1.2 Compliance with Standards
- All cryptographic implementations shall comply with:
  - Industry recognized standards and algorithms
  - Legal and regulatory requirements in applicable jurisdictions
  - SmartRent's Encryption Standard

#### 2.1.3 Approval Process
- All cryptographic solutions must be approved by the Information Security Team before implementation
- Exceptions to this policy must be documented and approved by the CISO

### 2.2 Cryptographic Algorithms and Protocols

#### 2.2.1 Approved Algorithms
- Only approved cryptographic algorithms and protocols shall be used
- The following types of algorithms are approved for specific uses:
  - Symmetric encryption: AES (256-bit minimum)
  - Asymmetric encryption: RSA (2048-bit minimum), ECC (256-bit minimum)
  - Hashing: SHA-256 or stronger
  - Message Authentication: HMAC with SHA-256 or stronger
  - Digital signatures: RSA (2048-bit minimum), ECDSA (256-bit minimum)

#### 2.2.2 Deprecated Algorithms
- The following algorithms are considered insecure and shall not be used in new implementations:
  - DES, 3DES, RC4, MD5, SHA-1, RSA (less than 2048 bits)
  - Any algorithm known to have significant vulnerabilities or weaknesses

#### 2.2.3 Algorithm Review
- Cryptographic algorithms shall be reviewed annually or when significant cryptographic vulnerabilities are discovered
- Transition plans shall be developed for algorithms and protocols that become deprecated

### 2.3 Key Management

#### 2.3.1 Key Generation
- Cryptographic keys shall be generated using secure methods
- Hardware Security Modules (HSMs) shall be used for generating and storing highly sensitive keys where appropriate
- Key generation shall occur in a secure environment

#### 2.3.2 Key Storage
- Private and secret keys shall be stored securely
- Critical cryptographic keys shall be stored in hardware security modules (HSMs) or other secure storage solutions
- Access to key storage systems shall be strictly controlled and logged

#### 2.3.3 Key Distribution
- Secure methods shall be used for key distribution
- Encryption keys shall be exchanged using secure protocols
- Keys shall be protected during transmission using secure channels

#### 2.3.4 Key Rotation
- Cryptographic keys shall be changed (rotated) at defined intervals:
  - Encryption keys for data at rest: At least every 2 years
  - Encryption keys for data in transit: At least annually
  - Signing keys: At least every 2 years
  - Authentication keys: At least annually
- Keys shall be rotated immediately if compromised or suspected of being compromised

#### 2.3.5 Key Backup and Recovery
- Critical cryptographic keys shall be backed up securely
- Key recovery procedures shall be documented and tested
- Key backup shall ensure both the security of the key material and its availability

#### 2.3.6 Key Destruction
- Cryptographic keys shall be securely destroyed when no longer needed
- Key destruction shall ensure the key material cannot be recovered

### 2.4 Use of Cryptographic Controls

#### 2.4.1 Data at Rest
- Sensitive data stored in databases, file systems, and storage media shall be encrypted using approved algorithms
- Full disk encryption shall be used for laptops and mobile devices
- Backup media containing sensitive information shall be encrypted

#### 2.4.2 Data in Transit
- Sensitive data transmitted over networks shall be encrypted using secure protocols
- Secure protocols (TLS 1.2 or higher) shall be used for web applications and services
- Secure file transfer protocols shall be used for transferring sensitive files
- VPN or other secure tunneling technologies shall be used for remote access

#### 2.4.3 Authentication and Authorization
- Strong authentication mechanisms shall be implemented for systems processing sensitive information
- Digital certificates shall be used to verify the identity of systems and services where appropriate
- Multi-factor authentication shall be implemented for access to critical systems

#### 2.4.4 Digital Signatures
- Digital signatures shall be used to ensure authenticity and non-repudiation where required
- Approved digital signature algorithms shall be used for signing code, documents, and transactions as appropriate

### 2.5 Public Key Infrastructure (PKI)

#### 2.5.1 Certificate Authorities
- Trusted certificate authorities (CAs) shall be used for issuing digital certificates
- Internal CAs shall follow industry best practices for operation and maintenance
- The use of self-signed certificates shall be restricted to test environments or internal non-critical systems

#### 2.5.2 Certificate Management
- Digital certificates shall be managed through their entire lifecycle
- Certificate expiration dates shall be monitored
- Procedures shall be in place for certificate renewal and revocation
- Certificate revocation lists (CRLs) and Online Certificate Status Protocol (OCSP) shall be used where appropriate

#### 2.5.3 Certificate Validation
- Certificate validation shall be performed before trusting a certificate
- Certificate path validation shall be implemented in accordance with X.509 standards
- Certificate validation shall include expiration checking and revocation status verification

### 2.6 Cryptographic Implementation

#### 2.6.1 Secure Development
- Cryptographic implementations shall follow secure development practices
- Only validated cryptographic modules and libraries shall be used
- Custom cryptographic implementations should be avoided unless validated by qualified personnel

#### 2.6.2 Testing and Validation
- Cryptographic implementations shall be tested to ensure proper operation
- Cryptographic operations shall be verified using known test vectors where available
- Penetration testing shall be performed on systems implementing cryptographic controls

#### 2.6.3 Documentation
- Cryptographic implementations shall be documented
- Documentation shall include algorithm selection, key management procedures, and configuration settings

### 2.7 Third-Party Cryptographic Services

#### 2.7.1 Cloud Cryptographic Services
- Cloud-based cryptographic services shall be evaluated and approved before use
- Contractual agreements shall address security requirements for cryptographic services
- Key management responsibilities shall be clearly defined between SmartRent and the service provider

#### 2.7.2 Supplier Cryptographic Controls
- Suppliers shall adhere to SmartRent's cryptographic requirements when processing SmartRent data
- Supplier cryptographic implementations shall be assessed for compliance with this policy

### 2.8 Incident Response

#### 2.8.1 Compromise Response
- Procedures shall be in place to respond to cryptographic compromises
- Key revocation and rotation shall be performed immediately following a confirmed or suspected compromise
- Crypto-agility planning shall be implemented to enable rapid response to cryptographic emergencies

#### 2.8.2 Reporting
- Cryptographic incidents shall be reported to the Information Security Team
- Regulatory requirements for reporting cryptographic breaches shall be followed

## 3. Roles and Responsibilities

### 3.1 Chief Information Security Officer (CISO)
- Owning and maintaining this policy
- Approving exceptions to this policy
- Ensuring compliance with this policy
- Approving cryptographic solutions for use within SmartRent

### 3.2 Information Security Team
- Implementing and maintaining cryptographic controls
- Reviewing and approving cryptographic implementations
- Monitoring compliance with this policy
- Providing guidance on cryptographic solutions

### 3.3 IT Operations
- Implementing approved cryptographic controls
- Managing cryptographic infrastructure
- Monitoring the status of cryptographic systems

### 3.4 Development Teams
- Implementing approved cryptographic controls in applications
- Following secure development practices for cryptographic implementations
- Documenting cryptographic implementations

### 3.5 All Employees
- Following this policy when using cryptographic controls
- Reporting suspected cryptographic incidents or vulnerabilities

## 4. Compliance

### 4.1 Measurement
The CISO will verify compliance with this policy through:
- Regular reviews of cryptographic implementations
- Security assessments and audits
- Automated monitoring tools
- Penetration testing

### 4.2 Exceptions
Any exception to this policy must be approved by the CISO in advance and documented in the exception register.

### 4.3 Non-Compliance
An employee found to have violated this policy may be subject to disciplinary action, up to and including termination of employment.

## 5. Related Documents
- ISMS-POL-001 Information Security Policy
- ISMS-STD-002 Encryption Standard
- ISMS-POL-006 Access Control Policy
- ISMS-POL-005 Incident Response Policy
- ISMS-STD-003 Secure Coding Standard

## 6. Definitions

- **Cryptography**: The practice and study of techniques for secure communication in the presence of adversaries.
- **Encryption**: The process of converting plaintext into ciphertext to prevent unauthorized access.
- **Decryption**: The process of converting ciphertext back into plaintext.
- **Symmetric Encryption**: Encryption method using the same key for both encryption and decryption.
- **Asymmetric Encryption**: Encryption method using a pair of keys (public and private) where one key encrypts and the other decrypts.
- **Public Key Infrastructure (PKI)**: A framework of policies, procedures, and technologies used to manage digital certificates and public key encryption.
- **Digital Signature**: A mathematical technique used to validate the authenticity and integrity of a message, document, or software.
- **Hardware Security Module (HSM)**: A physical device that safeguards and manages cryptographic keys and provides cryptographic operations.
- **Transport Layer Security (TLS)**: A cryptographic protocol designed to provide secure communication over a computer network.
- **Certificate Authority (CA)**: An entity that issues digital certificates.
- **Hash Function**: A function that converts data of arbitrary size to a fixed-size value, used for data integrity verification.
- **Key Management**: The management of cryptographic keys, including generation, exchange, storage, use, destruction, and replacement.

## 7. Document History

| Version | Date | Description of Changes | Author | Approved By |
|---------|------|------------------------|--------|------------|
| 1.0 | April 15, 2025 | Initial version | Security Team | [APPROVER] | 