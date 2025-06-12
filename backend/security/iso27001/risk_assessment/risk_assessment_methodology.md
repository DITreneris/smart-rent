# Information Security Risk Assessment Methodology

**Document ID:** ISMS-PRO-006  
**Version:** 1.0  
**Effective Date:** April 15, 2025  
**Status:** Draft  

## 1. Purpose

This document defines SmartRent's methodology for assessing and managing information security risks. It provides a structured approach for identifying, analyzing, and evaluating risks to information assets, and establishes the process for risk treatment decisions.

## 2. Scope

This methodology applies to:
- All information assets within the scope of the ISMS
- All information systems, applications, and services
- All business processes that handle sensitive information
- All personnel with access to information assets
- All physical locations where information is processed or stored

## 3. References

- ISO 27001:2013 - Information Security Management System
- ISO 27005:2018 - Information Security Risk Management
- NIST SP 800-30 - Guide for Conducting Risk Assessments
- ISMS-POL-001 Information Security Policy

## 4. Roles and Responsibilities

| Role | Responsibilities |
|------|------------------|
| CISO | Overall accountability for risk management, approval of risk acceptance |
| Risk Owner | Person or entity with the authority to manage a risk |
| Asset Owner | Responsible for information assets, providing input to risk assessments |
| Security Team | Facilitating risk assessments, documenting results, monitoring risk treatment |
| Department Managers | Identifying risks related to their departments, implementing controls |
| All Staff | Reporting potential risks, following security procedures |

## 5. Risk Assessment Process

SmartRent follows a 6-step process for information security risk assessment:

1. **Context Establishment**
2. **Risk Identification**
3. **Risk Analysis**
4. **Risk Evaluation**
5. **Risk Treatment**
6. **Risk Monitoring and Review**

### 5.1 Context Establishment

Before conducting a risk assessment, the following context shall be established:

- Scope and objectives of the risk assessment
- Risk assessment criteria and parameters
- Roles and responsibilities
- Information assets to be assessed
- External and internal factors that influence risk

### 5.2 Risk Identification

Risk identification involves determining what events could affect information security and how they might occur. Sources for risk identification include:

- Asset inventory reviews
- Threat intelligence
- Historical security incidents
- Vulnerability assessments
- Process and system reviews
- Interviews with key personnel
- Industry standards and best practices

For each risk, the following shall be recorded:
- Risk ID
- Risk description
- Risk category
- Affected assets
- Potential threat sources
- Existing controls

### 5.3 Risk Analysis

Risk analysis involves determining the likelihood and consequences of identified risks. SmartRent uses a qualitative risk analysis approach based on the following scales:

#### 5.3.1 Likelihood Scale

| Level | Description | Criteria |
|-------|-------------|----------|
| 5 | Almost Certain | Expected to occur in most circumstances (>80% probability) |
| 4 | Likely | Will probably occur in most circumstances (60-80% probability) |
| 3 | Possible | Might occur at some time (40-60% probability) |
| 2 | Unlikely | Could occur at some time (20-40% probability) |
| 1 | Rare | May occur only in exceptional circumstances (<20% probability) |

#### 5.3.2 Consequence Scale

| Level | Description | Confidentiality | Integrity | Availability | Financial Impact | Reputational Impact | Regulatory Impact |
|-------|-------------|-----------------|-----------|--------------|------------------|---------------------|-------------------|
| 5 | Catastrophic | Highly sensitive data exposure | Critical data corruption | Critical systems unavailable >1 day | >$500,000 | Severe, long-term damage | Major legal action, significant fines |
| 4 | Major | Sensitive data exposure | Significant data corruption | Important systems unavailable >8 hours | $100,000-$500,000 | Significant media coverage | Regulatory investigation |
| 3 | Moderate | Limited sensitive data exposure | Limited data corruption | Key systems unavailable >4 hours | $50,000-$100,000 | Some negative publicity | Reportable compliance breach |
| 2 | Minor | Minimal sensitive data exposure | Minor data corruption | Non-critical systems unavailable >4 hours | $10,000-$50,000 | Limited negative publicity | Minor compliance breach |
| 1 | Insignificant | No sensitive data exposure | Negligible data corruption | Minimal or no system downtime | <$10,000 | No reputational impact | No compliance implications |

#### 5.3.3 Risk Level Matrix

Risk levels are determined by cross-referencing the likelihood and consequence ratings according to the following matrix:

|                | **Consequence** |         |            |        |               |
|----------------|----------------|---------|------------|--------|---------------|
| **Likelihood** | **1 Insignificant** | **2 Minor** | **3 Moderate** | **4 Major** | **5 Catastrophic** |
| **5 Almost Certain** | Medium | High | High | Extreme | Extreme |
| **4 Likely** | Medium | Medium | High | High | Extreme |
| **3 Possible** | Low | Medium | Medium | High | High |
| **2 Unlikely** | Low | Low | Medium | Medium | High |
| **1 Rare** | Low | Low | Low | Medium | Medium |

### 5.4 Risk Evaluation

Risk evaluation involves comparing the risk levels determined during analysis against risk acceptance criteria to make decisions about risk treatment. SmartRent's risk acceptance criteria are as follows:

| Risk Level | Description | Response Required |
|------------|-------------|-------------------|
| Extreme | Unacceptable risk | Immediate action required to reduce risk; CISO approval required for any acceptance |
| High | Generally unacceptable risk | Risk treatment required; CISO approval required for any acceptance |
| Medium | Potentially acceptable risk | Risk treatment recommended; Department head approval for acceptance |
| Low | Acceptable risk | Routine management; monitor and reassess periodically |

### 5.5 Risk Treatment

For each risk that exceeds acceptance criteria, one or more of the following risk treatment options shall be selected:

- **Risk Modification (Mitigation)**: Implementing controls to reduce risk
- **Risk Avoidance**: Avoiding or discontinuing the activity causing the risk
- **Risk Sharing**: Transferring or sharing the risk with a third party (e.g., insurance)
- **Risk Retention (Acceptance)**: Accepting the risk after informed decision

#### 5.5.1 Risk Treatment Plan

A risk treatment plan shall be developed for all risks requiring treatment. The plan shall include:
- Selected risk treatment option(s)
- Required controls (referencing ISO 27001 Annex A controls where applicable)
- Resources required
- Responsibilities and timeline
- Measurement and verification method
- Residual risk after treatment

### 5.6 Risk Monitoring and Review

All risks and their treatments shall be regularly monitored and reviewed to ensure:
- Risk treatments remain effective
- Changes in the risk environment are identified
- New risks are assessed
- Risk treatments are adjusted as necessary

The frequency of risk monitoring shall be determined based on the risk level:
- Extreme risks: Monthly review
- High risks: Quarterly review
- Medium risks: Bi-annual review
- Low risks: Annual review

## 6. Risk Assessment Documentation

### 6.1 Risk Register

A centralized risk register shall be maintained with the following information:
- Risk ID and description
- Risk category
- Affected assets
- Inherent risk assessment (likelihood, consequence, risk level)
- Existing controls
- Risk treatment plan
- Residual risk assessment
- Risk owner
- Review date
- Status

### 6.2 Risk Assessment Report

A formal risk assessment report shall be produced for each comprehensive risk assessment, including:
- Executive summary
- Scope and objectives
- Methodology
- Key findings
- High and extreme risks
- Recommended risk treatments
- Conclusion and next steps

## 7. Risk Assessment Frequency

Risk assessments shall be conducted at the following intervals:
- Comprehensive risk assessment: Annually
- Targeted risk assessments: As needed (e.g., for new systems, significant changes)
- Continuous risk monitoring: Ongoing

## 8. Document Review

This methodology shall be reviewed annually or when significant changes occur to ensure its continued adequacy and effectiveness.

## 9. Document History

| Version | Date | Author | Description of Changes |
|---------|------|--------|------------------------|
| 1.0 | 2025-04-15 | Security Team | Initial document | 