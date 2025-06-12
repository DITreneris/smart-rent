# Risk Register Template

## Document Information
- **Document ID**: RISK-REG-001
- **Version**: 1.0
- **Last Updated**: [DATE]
- **Document Owner**: [OWNER NAME/ROLE]
- **Approved By**: [APPROVER NAME/ROLE]

## Overview
This risk register documents information security risks identified within SmartRent. It is maintained as part of our ISO 27001 Information Security Management System (ISMS) and serves as the central repository for risk information.

## Instructions for Use
1. Each identified risk should be assigned a unique ID in the format: RISK-[YY]-[XXX] where YY is the year and XXX is a sequential number
2. All fields must be completed for each risk
3. The risk register must be reviewed and updated according to the schedule defined in the Risk Assessment Methodology
4. New risks should be added promptly as they are identified
5. Risk treatments must be documented and tracked to completion

## Risk Register

| Risk ID | Date Identified | Risk Description | Asset/Process Affected | Threat Source | Vulnerability | Existing Controls | Initial Assessment ||||||| Risk Treatment ||||||| Current Status |
|---------|----------------|------------------|------------------------|---------------|---------------|-------------------|-------------------|---|---|---|---|---|---|---|---|---|---|---|---|---|
| | | | | | | | **L** | **C** | **Level** | **Owner** | **Review Date** | **Risk Appetite** | **Action** | **Option** | **Controls to Implement** | **Residual Risk Level** | **Responsible Party** | **Target Date** | **Progress** | |

### Key to Fields

**L** = Likelihood (1-5)  
**C** = Consequence/Impact (1-5)  
**Level** = Risk Level (Low, Medium, High, Critical)  
**Owner** = Person responsible for the risk  
**Action** = Accept/Treat/Transfer/Avoid  
**Progress** = Not Started/In Progress/Completed/Ongoing  

## Risk Ratings

### Likelihood Ratings
1. **Rare**: May occur only in exceptional circumstances (less than once in 5 years)
2. **Unlikely**: Could occur at some time (once in 2-5 years)
3. **Possible**: Might occur at some time (once in 1-2 years)
4. **Likely**: Will probably occur in most circumstances (multiple times per year)
5. **Almost Certain**: Expected to occur in most circumstances (monthly or more frequently)

### Consequence/Impact Ratings
1. **Insignificant**: No measurable operational impact; minimal financial loss (<$1,000)
2. **Minor**: Minor operational impact; small financial loss ($1,000-$10,000)
3. **Moderate**: Significant operational impact; moderate financial loss ($10,000-$100,000)
4. **Major**: Substantial operational impact; major financial loss ($100,000-$1M)
5. **Catastrophic**: Critical operational impact; enormous financial loss (>$1M)

### Risk Level Matrix

| Likelihood/Consequence | 1 - Insignificant | 2 - Minor | 3 - Moderate | 4 - Major | 5 - Catastrophic |
|------------------------|-------------------|-----------|--------------|-----------|------------------|
| 5 - Almost Certain     | Medium           | High      | High         | Critical  | Critical         |
| 4 - Likely             | Medium           | Medium    | High         | Critical  | Critical         |
| 3 - Possible           | Low              | Medium    | High         | High      | Critical         |
| 2 - Unlikely           | Low              | Low       | Medium       | High      | High             |
| 1 - Rare               | Low              | Low       | Medium       | Medium    | High             |

## Sample Risk Entry

| Risk ID | Date Identified | Risk Description | Asset/Process Affected | Threat Source | Vulnerability | Existing Controls | Initial Assessment ||||||| Risk Treatment ||||||| Current Status |
|---------|----------------|------------------|------------------------|---------------|---------------|-------------------|-------------------|---|---|---|---|---|---|---|---|---|---|---|---|---|
| RISK-23-001 | 2023-04-01 | Unauthorized access to customer data due to weak authentication | Customer Database | External Hackers | Single-factor authentication | Access logging, Firewall | 4 | 4 | Critical | IT Manager | 2023-10-01 | Low | Treat | Implement Control | Implement MFA for all database access | Medium | Security Team | 2023-07-01 | In Progress | 75% complete - MFA implemented for admin users, regular users pending |

## Document History

| Version | Date | Description of Changes | Author | Approved By |
|---------|------|------------------------|--------|------------|
| 1.0 | [DATE] | Initial version | [AUTHOR] | [APPROVER] |

## Appendix: Risk Treatment Options

1. **Modify**: Implement controls to reduce the risk
2. **Retain**: Accept the risk as it falls within risk appetite
3. **Avoid**: Eliminate the risk by removing the asset or process
4. **Share**: Transfer the risk to a third party (e.g., insurance)

## Related Documents
- Risk Assessment Methodology
- Statement of Applicability
- Information Security Policy 