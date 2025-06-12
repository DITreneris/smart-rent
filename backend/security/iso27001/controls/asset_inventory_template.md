# Information Asset Inventory Template

**Document ID:** ISMS-TPL-002  
**Version:** 1.0  
**Effective Date:** April 15, 2025  
**Status:** Draft  

## Purpose

This template provides a standardized format for maintaining SmartRent's information asset inventory as required by ISO 27001 control A.8.1.1 (Inventory of Assets). All information assets within the scope of the ISMS must be identified and inventoried using this template.

## Asset Classification Guide

### Confidentiality Classification

| Level | Description |
|-------|-------------|
| Public | Information that has been explicitly approved for public distribution |
| Internal | Information intended for use within SmartRent but not sensitive |
| Confidential | Sensitive information that requires protection from unauthorized disclosure |
| Restricted | Highly sensitive information that would cause significant harm if disclosed |

### Integrity Classification

| Level | Description |
|-------|-------------|
| Low | Information where integrity is not critical |
| Medium | Information where accuracy is important but temporary inaccuracies are tolerable |
| High | Information where accuracy is essential and modifications must be controlled |
| Critical | Information where any unauthorized modification would cause significant harm |

### Availability Classification

| Level | Description |
|-------|-------------|
| Low | Information or systems where downtime of days is tolerable |
| Medium | Information or systems where downtime of hours is tolerable |
| High | Information or systems where downtime of minutes is tolerable |
| Critical | Information or systems requiring continuous availability |

## Asset Inventory Table

| Asset ID | Asset Name | Description | Asset Type | Owner | Custodian | Location | Classification (C/I/A) | Backup Requirements | Review Date | Status |
|----------|------------|-------------|------------|-------|-----------|----------|------------------------|---------------------|-------------|--------|
| AST-DB-001 | Production Database | Primary MongoDB database for SmartRent platform | Database | Database Administrator | IT Operations | Cloud (AWS) | Confidential/High/Critical | Daily backup, monthly testing | 2025-04-15 | Active |
| AST-APP-001 | SmartRent Web Application | Customer-facing web application | Application | Product Manager | Development Team | Cloud (AWS) | Internal/High/Critical | Continuous deployment, version control | 2025-04-15 | Active |
| AST-APP-002 | SmartRent Mobile App | iOS and Android mobile applications | Application | Product Manager | Development Team | App Stores | Internal/High/High | Version control | 2025-04-15 | Active |
| AST-SRV-001 | Authentication Server | Handles user authentication and session management | Server | Security Manager | IT Operations | Cloud (AWS) | Confidential/Critical/Critical | Real-time replication | 2025-04-15 | Active |
| AST-SRV-002 | API Server | Provides API access to SmartRent services | Server | CTO | Development Team | Cloud (AWS) | Internal/High/Critical | Real-time replication | 2025-04-15 | Active |
| AST-NET-001 | Production Network | Main production network | Network | Network Administrator | IT Operations | Cloud (AWS) | Confidential/High/Critical | Configuration backup | 2025-04-15 | Active |
| AST-DOC-001 | System Architecture Documentation | Technical documentation of system design | Document | CTO | Development Team | Document Management System | Confidential/High/Medium | Version control | 2025-04-15 | Active |
| AST-SW-001 | Source Code Repository | Git repository containing all application source code | Software | CTO | Development Team | GitHub/GitLab | Restricted/Critical/High | Daily backup, off-site replication | 2025-04-15 | Active |

## Asset Types

1. **Information Assets**
   - Databases
   - Documents
   - Source code
   - Configuration files
   - Logs
   - Backups

2. **Software Assets**
   - Applications
   - Operating systems
   - Virtual machines
   - Development tools
   - Utilities

3. **Physical Assets**
   - Servers
   - Network equipment
   - Storage systems
   - User devices

4. **Services**
   - Cloud services
   - SaaS applications
   - Outsourced services
   - Utilities

5. **Personnel**
   - Employees
   - Contractors
   - Consultants
   - Service providers

## Asset Details Form

For each asset identified, complete the following information:

### Basic Information
- **Asset ID:** [Unique identifier]
- **Asset Name:** [Descriptive name]
- **Description:** [Brief description of the asset and its purpose]
- **Asset Type:** [From the categories above]
- **Owner:** [Person responsible for the asset]
- **Custodian:** [Person/team maintaining the asset]
- **Location:** [Physical or logical location]

### Classification
- **Confidentiality:** [Public/Internal/Confidential/Restricted]
- **Integrity:** [Low/Medium/High/Critical]
- **Availability:** [Low/Medium/High/Critical]

### Technical and Management Information
- **Make/Model/Version:** [For hardware/software assets]
- **Supplier/Vendor:** [Provider of the asset]
- **Purchase/Creation Date:** [When acquired or created]
- **Expected End-of-Life:** [When replacement expected]
- **Associated Contracts/SLAs:** [Reference to contracts]

### Security Controls
- **Authentication Requirements:** [How access is controlled]
- **Authorization Requirements:** [Who can access and what they can do]
- **Backup Requirements:** [How often backed up, where stored]
- **Business Continuity Requirements:** [Recovery requirements]

### Compliance Information
- **Regulatory Requirements:** [Regulations affecting this asset]
- **Audit Requirements:** [Audit controls needed]
- **Retention Requirements:** [How long the asset must be kept]

### Status Information
- **Status:** [Active/Inactive/Planned/Retired]
- **Review Date:** [When asset was last reviewed]
- **Next Review Date:** [When asset will be reviewed next]
- **Changes Since Last Review:** [Summary of changes]

## Maintenance Instructions

1. **Initial Inventory**
   - All departments must identify information assets under their control
   - Complete the asset details form for each identified asset
   - Submit to the Information Security Team for review

2. **Periodic Review**
   - Asset inventory must be reviewed quarterly
   - Changes to assets (new, modified, retired) must be updated
   - Asset classification must be reassessed

3. **Responsibilities**
   - Information Security Team: Maintain the master inventory
   - Asset Owners: Provide accurate information about assets
   - Department Managers: Ensure their assets are inventoried

4. **Approval Process**
   - New assets must be approved before being added to the inventory
   - Asset retirement must follow the appropriate disposal procedure
   - Changes to critical assets require CISO approval

## Related Documents

- ISMS-POL-001 Information Security Policy
- ISMS-POL-004 Data Classification Policy
- ISMS-PRO-003 Asset Management Procedure
- ISMS-PRO-004 Secure Disposal Procedure

## Document History

| Version | Date | Author | Description of Changes |
|---------|------|--------|------------------------|
| 1.0 | 2025-04-15 | Security Team | Initial document | 