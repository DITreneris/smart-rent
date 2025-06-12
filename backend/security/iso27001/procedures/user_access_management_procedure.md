# User Access Management Procedure

## Document Information
- **Document ID**: ISMS-PRO-007
- **Version**: 1.0
- **Effective Date**: April 15, 2025
- **Review Date**: April 15, 2026
- **Status**: Draft

## 1. Purpose and Scope

### 1.1 Purpose
This User Access Management Procedure establishes the processes and responsibilities for managing user access to SmartRent's information systems and services. It provides detailed guidance on how to implement the requirements of the Access Control Policy, ensuring that access rights are granted, reviewed, and revoked in a controlled, secure, and consistent manner.

### 1.2 Scope
This procedure applies to:
- All information systems, applications, databases, and network infrastructure owned or managed by SmartRent
- All employees, contractors, consultants, temporary staff, and third parties requiring access to SmartRent systems
- All types of user accounts including standard user accounts, privileged accounts, service accounts, and temporary accounts
- All environments including production, test, development, and staging

## 2. Roles and Responsibilities

### 2.1 System Owner
- Approving access requests for their systems
- Defining access requirements for their systems
- Reviewing access rights periodically
- Ensuring segregation of duties is maintained

### 2.2 Information Security Team
- Maintaining this procedure
- Auditing compliance with this procedure
- Providing guidance on access management issues
- Reviewing and approving privileged access requests

### 2.3 IT Operations
- Implementing access controls as specified in approved requests
- Maintaining access control systems
- Executing technical procedures for user provisioning and deprovisioning
- Performing periodic access reviews

### 2.4 Human Resources
- Notifying IT of personnel changes that impact access rights
- Initiating the user access provisioning process for new employees
- Initiating the user access termination process for departing employees
- Maintaining accurate employee records

### 2.5 Line Managers
- Requesting and approving access for their team members
- Ensuring access requests are based on business need
- Reviewing team members' access rights periodically
- Notifying IT of role changes within their team

### 2.6 Users
- Following the requirements in this procedure
- Using their access rights appropriately
- Reporting suspected unauthorized access or security incidents
- Completing required access management training

## 3. User Access Lifecycle Management

### 3.1 User Registration and Onboarding

#### 3.1.1 New Employee Onboarding
1. HR initiates the onboarding workflow when a new employee is hired
2. The workflow includes an Access Request Form completed by the hiring manager
3. The Access Request Form specifies:
   - User details (name, employee ID, job title, department)
   - Required systems and applications
   - Access level needed for each system
   - Start date and, if applicable, end date
   - Business justification
4. System owners approve access requests for their respective systems
5. The Information Security Team reviews and approves requests for privileged access
6. IT Operations creates user accounts and assigns access rights as approved
7. Initial credentials are provided securely to the user
8. The user must change temporary passwords upon first login

#### 3.1.2 Contractor/Third-Party Onboarding
1. The sponsoring manager submits an Access Request Form for the contractor
2. The request must include:
   - Contractor details
   - Company information
   - Contract duration
   - Required access and justification
   - Confidentiality agreements status
3. System owners and Information Security review and approve the request
4. IT Operations creates temporary accounts with appropriate expiration dates
5. Contractor accounts are clearly identified with a "C-" prefix
6. All contractor access is documented in the third-party access register

#### 3.1.3 Creation of Special Account Types
1. Service accounts:
   - Require special approval from the system owner and Information Security
   - Must be documented in the service account register
   - Must have a designated responsible person
   - Are reviewed quarterly

2. Shared accounts:
   - Are generally prohibited except where technically necessary
   - Require CISO approval
   - Must have enhanced logging and monitoring
   - Password changes when a member with knowledge leaves

3. Temporary accounts:
   - Must have a specific expiration date
   - Are reviewed weekly
   - Are automatically disabled when no longer needed

### 3.2 User Access Provisioning

#### 3.2.1 Standard Access Request Process
1. Requestor submits an Access Request Form via the IT Service Management system
2. The request routes to the appropriate approvers based on the access requested
3. Approvers review the request for:
   - Business need
   - Appropriate access level
   - Compliance with segregation of duties
   - Security implications
4. Upon approval, IT Operations implements the requested access
5. The requestor is notified when access is granted
6. All access requests and approvals are logged for audit purposes

#### 3.2.2 Emergency Access Process
1. For urgent access needs outside business hours or in emergencies:
   - The requestor contacts the on-call IT support
   - The on-call support follows the emergency access procedure
   - Temporary access is granted with limited duration
2. Post-emergency review:
   - All emergency access grants are reviewed the next business day
   - Proper documentation and approvals are obtained retrospectively
   - Access is adjusted as necessary

#### 3.2.3 Privileged Access Provisioning
1. Privileged access requires:
   - Detailed justification
   - Manager approval
   - System owner approval
   - Information Security Team approval
2. Privileged access is:
   - Granted for limited time periods where possible
   - Granted with the minimum level necessary
   - Subject to enhanced monitoring and logging
   - Reviewed more frequently than standard access

#### 3.2.4 Role-Based Access Control
1. Standard role profiles are defined for common job functions
2. Role profiles define the standard set of access rights for that role
3. Users are assigned to appropriate roles based on job function
4. Roles are reviewed and updated when system changes occur
5. Exceptions to standard roles are documented and approved

### 3.3 User Access Changes

#### 3.3.1 Role Change Process
1. When an employee changes roles:
   - HR or the employee's manager submits a role change notification
   - The notification includes the new role and effective date
   - Previously required access that is no longer needed is identified
2. IT Operations:
   - Adjusts access rights according to the new role requirements
   - Removes access rights no longer needed
   - Documents all changes made

#### 3.3.2 Temporary Access Changes
1. For temporary projects or assignments:
   - The manager submits a temporary access request
   - The request includes a clear end date
   - Approvals are obtained as per standard process
2. IT Operations:
   - Implements temporary access with an expiration date
   - Monitors approaching expiration dates
   - Automatically removes temporary access on the end date unless extended

### 3.4 User Access Review

#### 3.4.1 Periodic Access Review Process
1. User access reviews are conducted:
   - For standard systems: at least annually
   - For critical systems: at least quarterly
   - For systems with regulatory requirements: as required by regulations
2. The review process:
   - System owners receive access reports for their systems
   - Managers receive access reports for their team members
   - Reviewers validate the continued business need for access
   - Reviewers approve or reject each access right
3. IT Operations implements changes resulting from the review
4. Review results are documented for audit purposes

#### 3.4.2 Privileged Access Review
1. Privileged access is reviewed:
   - At least quarterly
   - After major system changes
   - When security incidents occur
2. The Information Security Team leads the privileged access review
3. All unnecessary privileged access is promptly removed
4. Privileged account usage logs are reviewed as part of the process

#### 3.4.3 Dormant Account Review
1. Dormant account reports are generated monthly
2. Accounts inactive for 90 days are disabled
3. Accounts inactive for 180 days are scheduled for deletion
4. Exceptions must be approved by the system owner and Information Security

### 3.5 User Access Termination

#### 3.5.1 Employee Termination Process
1. HR initiates the offboarding workflow when an employee leaves
2. For planned departures:
   - HR provides at least one week's notice when possible
   - Access removal is scheduled for the last working day
3. For immediate terminations:
   - HR notifies IT Operations immediately
   - Access is revoked immediately
4. IT Operations:
   - Disables all user accounts
   - Removes all access rights
   - Archives mailboxes as required
   - Documents all actions taken

#### 3.5.2 Contractor Termination Process
1. The sponsoring manager notifies IT Operations when contractor engagements end
2. IT Operations:
   - Disables contractor accounts on the specified end date
   - Returns any physical access tokens
   - Updates the third-party access register
3. Contractor accounts are kept in disabled state for 90 days before deletion

#### 3.5.3 Involuntary Termination Process
1. For high-risk terminations:
   - HR and manager coordinate with IT Operations and Security before the termination
   - Access is revoked at the exact time of termination
   - Additional monitoring is implemented as needed
2. Post-termination review is conducted to ensure all access is removed

## 4. Technical Procedures

### 4.1 Active Directory User Management

#### 4.1.1 AD Account Creation
1. Create the user in the appropriate Organizational Unit
2. Set account properties according to the standard template
3. Assign to appropriate security groups based on approved access
4. Set password expiration according to policy
5. Enable account when ready for use

#### 4.1.2 AD Account Modification
1. Update user attributes as needed
2. Add or remove group memberships as approved
3. Document all changes in the ticket system
4. Notify user of changes made

#### 4.1.3 AD Account Disablement
1. Remove all group memberships
2. Move account to Disabled Users OU
3. Document disablement date and reason
4. Retain disabled accounts for audit purposes

### 4.2 Application Access Management

#### 4.2.1 Application Account Creation
1. Follow application-specific procedures for account creation
2. Use role-based access controls where available
3. Document all application access in the access management system
4. Verify access works as expected

#### 4.2.2 Application Access Review
1. Generate access reports from each application
2. Distribute reports to system owners and managers
3. Track review completion and resulting actions
4. Implement approved changes

#### 4.2.3 Application Account Termination
1. Remove application permissions
2. Disable application accounts
3. Archive user data as required
4. Document termination actions

### 4.3 Database Access Management

#### 4.3.1 Database Account Management
1. Create database accounts according to approved access requests
2. Assign minimum necessary permissions based on job role
3. Use database roles where possible
4. Monitor database account usage

#### 4.3.2 Database Privileged Access
1. Limit database administrator accounts
2. Use separate accounts for administrative and regular activities
3. Implement enhanced logging for administrative actions
4. Review administrative access regularly

### 4.4 Remote Access Management

#### 4.4.1 VPN Access Provisioning
1. Process VPN access requests with appropriate approvals
2. Configure VPN accounts with appropriate access profiles
3. Ensure multi-factor authentication is enabled
4. Provide secure delivery of VPN credentials

#### 4.4.2 Remote Access Monitoring
1. Monitor VPN usage patterns
2. Review access logs for unusual activity
3. Implement session timeout controls
4. Disable inactive VPN accounts

## 5. Access Control Implementation

### 5.1 Authentication Controls

#### 5.1.1 Password Management
1. Implement password controls according to the Password Standard
2. Configure password expiration, history, and complexity requirements
3. Implement secure password reset procedures
4. Provide guidance to users on password management

#### 5.1.2 Multi-Factor Authentication
1. Implement MFA for:
   - Remote access connections
   - Privileged account access
   - Critical system access
   - Administrator interfaces
2. Configure MFA settings according to the Access Control Policy
3. Maintain backup authentication methods

### 5.2 Authorization Controls

#### 5.2.1 Principle of Least Privilege
1. Grant minimum access required for job functions
2. Remove unnecessary access rights
3. Use time-limited access where appropriate
4. Implement workflow approvals for sensitive actions

#### 5.2.2 Segregation of Duties
1. Identify conflicting duties and responsibilities
2. Implement controls to prevent individuals from having conflicting access
3. Document and monitor segregation of duties matrices
4. Review segregation controls during system changes

### 5.3 Audit and Logging

#### 5.3.1 Access Logging
1. Enable access logging for all systems
2. Log successful and failed access attempts
3. Protect log integrity
4. Retain logs according to retention policy

#### 5.3.2 Log Review
1. Review access logs for suspicious activity
2. Investigate unusual access patterns
3. Report security incidents as per the Incident Response Policy
4. Document log review activities

## 6. Special Access Situations

### 6.1 Vendor Access Management

#### 6.1.1 Vendor Access Request
1. Business owner submits vendor access request
2. Request includes:
   - Vendor details
   - Systems requiring access
   - Access duration and schedule
   - Business justification
   - Confidentiality agreement status
3. Information Security reviews and approves vendor access
4. IT Operations implements with appropriate restrictions

#### 6.1.2 Vendor Access Controls
1. Implement time-limited access for vendors
2. Restrict access to specific IP addresses where possible
3. Enable enhanced monitoring during vendor access
4. Require vendor activities to be logged and reviewed

### 6.2 Developer Access to Production

#### 6.2.1 Developer Access Restrictions
1. Developer access to production environments is generally prohibited
2. Exception process:
   - Requires CISO approval
   - Must have detailed justification
   - Is time-limited and monitored
   - Is logged and audited
3. Segregation between development and production environments is maintained

#### 6.2.2 Emergency Developer Access
1. In emergency situations requiring developer access:
   - Formal approval process is followed
   - Access is monitored in real-time
   - All actions are logged
   - Access is revoked immediately after the emergency
2. Post-incident review is conducted

### 6.3 Physical Access Management

#### 6.3.1 Data Center Access
1. Data center access is restricted to authorized personnel
2. Access request requires:
   - Business justification
   - Manager approval
   - Security approval
3. Access is implemented using:
   - Access cards
   - Biometric authentication
   - Visitor logs
4. Data center access is reviewed quarterly

#### 6.3.2 Office Access
1. Office access is managed through:
   - Access cards/badges
   - Reception procedures
   - Visitor management
2. Different access zones are defined based on sensitivity
3. Access rights are tied to employment status

## 7. Compliance and Reporting

### 7.1 Compliance Monitoring
1. Regular audits of user access management are conducted
2. Automated monitoring of compliance with access control requirements
3. Self-assessments by system owners
4. Independent reviews by Information Security

### 7.2 Reporting
1. Access management metrics are reported monthly, including:
   - Number of access requests processed
   - Time to fulfill access requests
   - Access review completion rates
   - Policy exceptions granted
   - Compliance issues identified
2. Reports are provided to:
   - Information Security Committee
   - IT Management
   - System Owners

### 7.3 Continuous Improvement
1. Identify opportunities for improving the access management process
2. Implement automation where possible
3. Update procedures based on lessons learned
4. Incorporate feedback from stakeholders

## 8. References
- ISMS-POL-001 Information Security Policy
- ISMS-POL-006 Access Control Policy
- ISMS-STD-001 Password Standard
- ISMS-PRO-008 Privileged Access Management Procedure
- ISMS-TPL-004 Access Request Form

## 9. Document History

| Version | Date | Description of Changes | Author | Approved By |
|---------|------|------------------------|--------|------------|
| 1.0 | April 15, 2025 | Initial version | Security Team | [APPROVER] | 