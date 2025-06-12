# Password Standard

## Document Information
- **Document ID**: ISMS-STD-001
- **Version**: 1.0
- **Effective Date**: April 15, 2025
- **Review Date**: April 15, 2026
- **Status**: Draft

## 1. Purpose and Scope

### 1.1 Purpose
This standard defines the requirements for creating, managing, and securing passwords used to access SmartRent information systems, applications, and services. It establishes consistent password practices across the organization to protect against unauthorized access.

### 1.2 Scope
This standard applies to:
- All employees, contractors, consultants, temporary staff, and other workers at SmartRent
- All passwords used to access SmartRent systems, applications, networks, and services
- All authentication methods that use passwords or passphrases as a factor
- All systems and applications that require password authentication

## 2. Password Creation Requirements

### 2.1 Password Complexity

All passwords must meet the following minimum requirements:

#### 2.1.1 Standard User Accounts
- Minimum length: 12 characters
- Complexity: Must include at least one character from three of the following four categories:
  - Uppercase letters (A-Z)
  - Lowercase letters (a-z)
  - Numbers (0-9)
  - Special characters (e.g., !@#$%^&*()_+=-[]{}|;:'",.<>?/`~)
- Must not contain the user's username, first name, last name, or email address
- Must not contain dictionary words
- Must not be a commonly used password

#### 2.1.2 Privileged Accounts
- Minimum length: 16 characters
- Complexity: Must include at least one character from all four of the following categories:
  - Uppercase letters (A-Z)
  - Lowercase letters (a-z)
  - Numbers (0-9)
  - Special characters (e.g., !@#$%^&*()_+=-[]{}|;:'",.<>?/`~)
- Must not contain the user's username, first name, last name, or email address
- Must not contain dictionary words
- Must not be a commonly used password

#### 2.1.3 Service Accounts
- Minimum length: 20 characters
- Must be randomly generated
- Must include a mix of uppercase letters, lowercase letters, numbers, and special characters
- Must be stored securely in an approved password management system

#### 2.1.4 Passphrases
Where supported, passphrases may be used as an alternative to complex passwords:
- Minimum length: 20 characters
- Must include at least 4 words
- Words must be separated by spaces, hyphens, or other characters
- Should not be a common phrase, quote, or lyric

### 2.2 Password History

- Users must not reuse any of their previous 12 passwords
- New passwords must differ from previous passwords by at least 5 characters

### 2.3 Password Expiration

#### 2.3.1 Standard User Accounts
- Maximum password age: 90 days
- Minimum password age: 1 day (to prevent immediate reuse)
- Users will be prompted to change their passwords 14 days before expiration

#### 2.3.2 Privileged Accounts
- Maximum password age: 60 days
- Minimum password age: 1 day (to prevent immediate reuse)
- Users will be prompted to change their passwords 14 days before expiration

#### 2.3.3 Service Accounts
- Maximum password age: 180 days
- Password changes must be coordinated with application owners to prevent service disruption

### 2.4 Account Lockout

- Accounts will be locked after 5 consecutive failed login attempts
- Lockout duration: 15 minutes
- Alternatively, requiring progressively longer delays between login attempts is acceptable
- Privileged accounts may be subject to immediate notification to security personnel upon lockout

## 3. Multi-Factor Authentication (MFA)

### 3.1 MFA Requirements

Multi-factor authentication is required for:
- All remote access to SmartRent networks and systems
- All privileged account access
- All access to systems containing sensitive or confidential information
- All cloud service accounts
- All administrative interfaces

### 3.2 Approved MFA Methods

The following MFA methods are approved for use:
- Hardware authentication tokens (e.g., YubiKey, smartcards)
- Software authentication applications (e.g., Microsoft Authenticator, Google Authenticator)
- Push notifications to registered mobile devices
- Biometric authentication (when available and appropriate)

### 3.3 Prohibited MFA Methods

The following methods are not approved for use as a second factor:
- SMS text messages (unless no other option is available)
- Voice calls
- Email messages to the same account being authenticated

## 4. Password Management

### 4.1 Password Storage

- Passwords must be stored in a secure, hashed format using industry-standard algorithms (e.g., Argon2, bcrypt, PBKDF2)
- Plain text passwords must never be stored in any system, application, or database
- Password hashes must be protected with appropriate access controls
- Salt values must be used in conjunction with hashing algorithms
- Where possible, hardware security modules (HSMs) should be used for cryptographic operations

### 4.2 Password Transmission

- Passwords must be transmitted only over encrypted channels (e.g., TLS/SSL)
- Passwords must never be transmitted via email, instant messaging, or other unencrypted communications
- Passwords must never be included in logs, debugging information, or error messages

### 4.3 Default Passwords

- All default passwords must be changed before a system is put into production
- Systems must be configured to force a password change at first login when default credentials exist
- Default passwords must be changed on all network devices, IoT devices, and appliances before deployment

### 4.4 Shared Accounts

- Shared accounts should be avoided whenever possible
- When shared accounts are necessary, passwords must be:
  - Changed whenever a person with knowledge of the password leaves the organization
  - Reviewed at least quarterly
  - Stored in an approved password management solution
  - Changed regularly according to the service account schedule

### 4.5 Password Managers

- An approved enterprise password management solution must be used to store passwords
- The master password for password managers must meet the privileged account complexity requirements
- Multi-factor authentication must be enabled for access to password managers
- Password manager vaults must be backed up regularly
- Emergency access procedures must be documented for password manager accounts

## 5. User Responsibilities

### 5.1 Password Protection

Users must:
- Keep passwords confidential and not share them with anyone, including IT support staff
- Not write down passwords or store them in an insecure manner
- Not use the "remember password" feature in applications or browsers unless approved
- Not use the same password for multiple accounts, especially mixing personal and work accounts
- Lock their workstation when unattended
- Report suspected password compromise immediately

### 5.2 Password Creation

Users should:
- Create passwords that are easy to remember but difficult to guess
- Consider using passphrases where supported
- Not include personal information in passwords
- Not use patterns or predictable character substitutions

## 6. System Administration Requirements

### 6.1 System Configuration

System administrators must ensure:
- Password complexity and management settings are enforced technically where possible
- Password hashing uses approved algorithms with appropriate work factors
- Failed login attempts are logged and monitored
- Password change history is maintained
- Password age is enforced according to policy
- Default credentials are changed before production deployment

### 6.2 Exceptions

Exceptions to this standard may be granted only when:
- Technical limitations prevent compliance
- Business requirements necessitate a deviation
- Compensating controls provide equivalent security

All exceptions must be:
- Documented with a clear business justification
- Approved by the CISO or designated security authority
- Reviewed at least annually
- Accompanied by compensating controls where possible

## 7. Password Reset Procedures

### 7.1 Self-Service Password Reset

- Self-service password reset functionality should be available where possible
- Identity verification for self-service reset must use:
  - Pre-registered security questions, AND
  - Email verification to a pre-registered address, AND
  - Another factor such as mobile app notification or phone call

### 7.2 Helpdesk-Assisted Reset

- Helpdesk staff must verify the identity of the requestor using at least two verification methods
- Temporary passwords provided during reset must:
  - Be randomly generated
  - Expire within 24 hours
  - Require immediate change upon first login
- Password reset requests must be logged and periodically reviewed

## 8. Compliance Monitoring

- Automated tools should be used to audit password compliance
- Regular password strength audits should be conducted
- Users with weak passwords should be required to change them immediately
- System administrators should review account lockout events and failed login attempts

## 9. Related Documents
- ISMS-POL-001 Information Security Policy
- ISMS-POL-006 Access Control Policy
- ISMS-POL-008 Acceptable Use Policy
- ISMS-PRO-007 User Access Management Procedure

## 10. Definitions
- **Authentication**: The process of verifying the identity of a user, process, or device
- **Multi-Factor Authentication (MFA)**: Authentication using two or more factors: something you know (password), something you have (token), or something you are (biometric)
- **Password**: A secret string of characters used for authentication
- **Passphrase**: A sequence of words used for authentication
- **Privileged Account**: An account with elevated permissions beyond those of a standard user
- **Service Account**: An account used by an application or service rather than a person

## 11. Document History

| Version | Date | Description of Changes | Author | Approved By |
|---------|------|------------------------|--------|------------|
| 1.0 | April 15, 2025 | Initial version | Security Team | [APPROVER] | 