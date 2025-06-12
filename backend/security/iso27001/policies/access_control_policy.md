# Access Control Policy

## Document Information
- **Document ID**: ISMS-POL-006
- **Version**: 1.0
- **Effective Date**: April 15, 2025
- **Review Date**: April 15, 2026
- **Status**: Draft

## 1. Purpose and Scope

### 1.1 Purpose
This Access Control Policy establishes the requirements for controlling access to SmartRent's information systems, applications, and data. It defines how access rights are granted, managed, and revoked to ensure that only authorized individuals can access information assets according to business needs and security requirements.

### 1.2 Scope
This policy applies to:
- All information systems, applications, databases, and services owned or managed by SmartRent
- All employees, contractors, consultants, temporary staff, and third parties with access to SmartRent information assets
- All access methods including physical access, network access, remote access, and application access
- All environments including production, test, development, and staging

## 2. Policy Statements

### 2.1 Access Control Principles

#### 2.1.1 Need-to-Know
Access to information shall be restricted based on the principle of need-to-know, providing users with the minimum privileges required to perform their job functions.

#### 2.1.2 Least Privilege
Users shall be granted the minimum level of access rights necessary to perform their authorized tasks.

#### 2.1.3 Segregation of Duties
Conflicting duties and responsibilities shall be segregated to reduce the risk of unauthorized or unintentional modification or misuse of assets.

#### 2.1.4 Default Deny
Access control systems shall implement a default "deny all" setting so that access rights must be explicitly granted.

### 2.2 User Access Management

#### 2.2.1 User Registration and Deregistration
- A formal user registration and deregistration process shall be implemented for granting and revoking access to systems and services
- Each user shall be assigned a unique identifier (user ID)
- Generic, shared, or group user IDs shall not be permitted except where required for business or operational reasons, and must be approved by the CISO
- Access requests must be formally documented and approved by the appropriate authority

#### 2.2.2 User Provisioning
- Access rights shall be provisioned using a formal process
- All access requests must be approved by the relevant information owner or system owner
- Elevated privilege accounts shall require additional approval from the CISO or delegate
- All access rights shall be documented and reviewed periodically

#### 2.2.3 Review of Access Rights
- Information owners shall review user access rights at regular intervals:
  - General access rights: at least annually
  - Privileged access rights: at least quarterly
  - Critical systems access: at least quarterly
- Changes to user roles, responsibilities, or employment status shall trigger an immediate review of access rights

#### 2.2.4 Removal or Adjustment of Access Rights
- Access rights shall be removed or adjusted upon:
  - Termination of employment or contract
  - Change in role or responsibility
  - Extended leave of absence
  - Contractor or third-party engagement completion
- A formal offboarding process shall be followed to ensure all access rights are properly revoked

### 2.3 User Responsibilities

#### 2.3.1 Password Management
- Users shall follow the requirements defined in the Password Policy
- Temporary passwords shall be changed at first login
- Users shall not share their passwords with any other person
- Multi-factor authentication shall be used for all remote access and privileged account access

#### 2.3.2 Unattended Equipment
- Users shall ensure that unattended equipment has appropriate protection through:
  - Logging off systems or applications when finished
  - Activating password-protected screen savers or screen locks
  - Securing physical documents and removable media

### 2.4 Network Access Control

#### 2.4.1 Network Segmentation
- The network shall be segmented to isolate systems based on sensitivity and function
- Appropriate controls shall be implemented at network boundaries to restrict unauthorized traffic

#### 2.4.2 Remote Access
- Remote access to SmartRent systems shall:
  - Require multi-factor authentication
  - Use encrypted communication channels (e.g., VPN, TLS)
  - Be subject to session timeout after a period of inactivity
  - Be limited to authorized devices where possible
- All remote access sessions shall be logged and monitored

#### 2.4.3 Wireless Network Access
- Wireless networks shall be secured using industry-standard encryption protocols
- Corporate and guest wireless networks shall be segregated
- Authentication shall be required for all wireless network access

### 2.5 Application and Information Access Control

#### 2.5.1 Information Access Restriction
- Access to information and application system functions shall be restricted in accordance with the need-to-know principle
- Information shall be classified according to the Data Classification Policy
- Access controls shall be appropriate to the sensitivity of the information

#### 2.5.2 Secure Log-on Procedures
- Access to systems and applications shall be controlled by a secure log-on procedure
- Multi-factor authentication shall be implemented for access to sensitive systems
- Failed login attempts shall be limited and recorded
- Password management systems shall enforce strong passwords

#### 2.5.3 Session Management
- Inactive sessions shall time out after a defined period of inactivity
- Concurrent sessions shall be restricted where necessary
- Session termination shall be enforced for high-risk applications

### 2.6 Privileged Access Management

#### 2.6.1 Privileged Account Control
- Privileged account access shall be strictly controlled and monitored
- Administrative accounts shall be used only for administrative tasks
- Standard user accounts shall be used for routine activities
- Privileged accounts shall require multi-factor authentication

#### 2.6.2 Review of Privileged Access Rights
- Privileged access rights shall be reviewed at least quarterly
- Privileged account usage shall be monitored and logged
- Privileged account passwords shall be changed more frequently than standard accounts

### 2.7 Physical Access Control

#### 2.7.1 Secure Areas
- Access to areas where sensitive information is processed or stored shall be restricted
- Physical access controls shall be appropriate to the sensitivity of the information
- Visitor access shall be controlled and logged

#### 2.7.2 Equipment Security
- Equipment shall be physically protected from unauthorized access and environmental threats
- Removal of equipment, information, or software shall be authorized and logged

## 3. Access Control Procedures

### 3.1 User Access Provisioning Procedure
- Access requests must be submitted using the approved request form or system
- Requests must include:
  - User's name and position
  - Systems, applications, or information requiring access
  - Level of access required
  - Business justification
  - Duration (for temporary access)
  - Approver's name and position
- Access shall be provisioned only after approval by the appropriate authority
- Temporary access shall include an expiration date

### 3.2 Access Termination Procedure
- A formal process shall be followed when a user's access rights need to be terminated
- HR shall notify IT of all terminations with sufficient lead time when possible
- Access shall be removed or disabled on the user's last working day at the latest
- Shared credentials shall be changed when team members leave

### 3.3 Password Management Procedure
- Initial passwords shall be securely communicated and set to expire upon first use
- Password reset procedures shall verify the identity of the user before issuing a new password
- Self-service password reset systems shall implement appropriate security controls

### 3.4 Privileged Access Request Procedure
- Requests for privileged access shall require additional approval
- Privileged access shall be time-limited where appropriate
- Privileged access usage shall be logged and reviewed

## 4. Roles and Responsibilities

### 4.1 Chief Information Security Officer (CISO)
- Overseeing the implementation of this policy
- Approving exceptions to this policy
- Reviewing access control effectiveness

### 4.2 IT Department
- Implementing technical access controls
- Managing user accounts and access rights
- Reviewing access logs and reports

### 4.3 Information Owners
- Approving access to their information assets
- Reviewing access rights periodically
- Defining access requirements based on sensitivity

### 4.4 Human Resources Department
- Notifying IT of personnel changes that affect access rights
- Supporting the user registration and deregistration process
- Ensuring access control requirements are included in job descriptions

### 4.5 All Employees, Contractors, and Third Parties
- Complying with access control requirements
- Protecting authentication credentials
- Reporting suspected access control violations

## 5. Policy Compliance

### 5.1 Compliance Measurement
The CISO will verify compliance with this policy through:
- Periodic access reviews
- Automated monitoring tools
- Internal and external audits
- Access control testing

### 5.2 Exceptions
Any exception to this policy must be approved by the CISO in advance and documented in the exception register.

### 5.3 Non-Compliance
An employee found to have violated this policy may be subject to disciplinary action, up to and including termination of employment.

## 6. Related Documents
- ISMS-POL-001 Information Security Policy
- ISMS-POL-003 Acceptable Use Policy
- ISMS-POL-004 Data Classification Policy
- ISMS-STD-001 Password Standard
- ISMS-PRO-007 User Access Management Procedure
- ISMS-PRO-008 Privileged Access Management Procedure

## 7. Definitions
- **Access Control**: The means of ensuring that access to information assets is authorized and restricted based on business and security requirements.
- **Least Privilege**: The principle of providing users with the minimum access rights necessary to perform their job functions.
- **Need-to-Know**: The principle that users should only have access to the information they need to perform their job functions.
- **Privileged Account**: An account with elevated permissions beyond those of a standard user account.
- **Multi-Factor Authentication (MFA)**: Authentication method that requires two or more verification factors.

## 8. Document History

| Version | Date | Description of Changes | Author | Approved By |
|---------|------|------------------------|--------|------------|
| 1.0 | April 15, 2025 | Initial version | Security Team | [APPROVER] | 