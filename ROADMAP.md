# SmartRent Project Roadmap - MVP Focus

## Current Status (Pre-MVP Consolidation - ~v0.5.x)

### Recently Completed
- ✅ Web3 wallet integration (Basic)
- ✅ Property listing implementation (Basic UI/Backend)
- ✅ MongoDB Atlas integration
- ✅ Basic user authentication
- ✅ Core UI components (Foundation)
- ✅ Foundational ISO 27001 Policies (Documentation)
  - ✅ Information Security Policy
  - ✅ Access Control Policy
  - ✅ Acceptable Use Policy
  - ✅ Incident Response Policy
  - ✅ Password Standard
  - ✅ Encryption Standard
  - ✅ User Access Management Procedure
  - ✅ Security Incident Report Template

## MVP Roadmap (Targeting v0.6.0 - v0.6.x)

**Goal:** Deliver a stable, minimal viable product demonstrating the core rental flow on a simplified tech stack (React, FastAPI (`app`), MongoDB, minimal EVM/Solidity) for investor readiness.

**Key Phases (Aligned with `morning_ses1.md`):**

### Phase 1: Consolidation & Simplification (Target: Sprint 1-2)
- 🟡 **Consolidate Backend:** Delete `backend/app`, migrate necessary logic to `app`. (Requires manual deletion first)
- 🟡 **Update Documentation:** Align `ARCHITECTURE.md`, `ROADMAP.md`, `README.md` with MVP scope and stack (Remove Solana/Hyperledger). (In Progress)
- ⬜ **Define MVP Rental Flow:** Finalize core process (Propose -> Accept -> Confirm) and on-chain role (Team Workshop Needed).
- ⬜ **Simplify Smart Contract:** Refactor `SmartRent.sol` based on defined MVP flow (metadata anchor / simple events).
- ⬜ **Verify Core Connections:** Ensure Frontend <-> Backend (`app`) API communication works.
- ⬜ **Verify Docker:** Confirm `docker-compose.yml` builds and runs the simplified stack.

### Phase 2: Core MVP Feature Implementation (Target: Sprint 3-5)
- ⬜ **Implement Core Rental Flow:** Build UI components and backend logic for:
    - Tenant: View properties, propose rental.
    - Landlord: View proposals, accept rental.
    - System: Update state (DB primarily, minimal contract interaction if defined).
- ⬜ **Implement Basic Dashboard:** View relevant properties/rentals for logged-in user.
- ⬜ **Implement Essential Backend Services:** Robust services in `app/services` for property/rental management.
- ⬜ **Implement Basic On-Chain Interaction:** If defined in flow (e.g., read metadata, emit event).
- ⬜ **Implement Basic Transaction Monitoring:** Off-chain monitoring for essential steps (if needed).
- ⬜ **Implement Essential Security:** Input validation, auth middleware checks.

### Phase 3: Testing & Stabilization (Target: Sprint 6-7)
- ⬜ **Core Flow Integration Tests:** Frontend <-> Backend <-> DB tests for rental process.
- ⬜ **Essential Unit Tests:** Critical backend services, utils, key frontend components.
- ⬜ **Basic Smart Contract Tests:** If contract has logic/events.
- ⬜ **Manual Testing & Bug Fixing:** Ensure MVP stability.
- ⬜ **Logging & Error Handling:** Verify adequacy for troubleshooting.
- ⬜ **Deployment Prep:** Finalize scripts/documentation for MVP deployment.

## Post-MVP / Future Roadmap (v0.7.0+)

*(Features postponed from original roadmap - requires re-prioritization based on MVP feedback)*

### Technology Stack Development
- Advanced transaction monitoring
- Smart contract upgradability
- Advanced error handling & Performance optimization
- Caching layer
- Potential Microservices architecture
- Advanced UI/UX & Mobile responsiveness
- Progressive Web App features / Offline mode

### Business Features
- Advanced search and filters
- Property analytics / Property verification
- Secure payment processing (Real)
- Rental history / Automated notifications
- Dispute resolution
- User messaging system / Enhanced notifications
- Rating and review system
- User preferences and recommendations
- Smart home integration

### Security & Compliance
- Comprehensive ISO 27001 Implementation (Risk Assessment, BCP, Audits, etc.)
- Advanced authentication / MFA options
- Penetration testing / Vulnerability management
- Advanced Security monitoring

### DevOps & Infrastructure
- Advanced CI/CD (Environment management, Config management, IaC)
- Advanced Monitoring & Analytics Dashboard / Anomaly detection

### Long-Term Vision (v1.0.0+)
- AI-powered property recommendations
- Blockchain-based dispute resolution
- Comprehensive mobile application
- ISO 27001 certification readiness
- Multi-chain support (If validated need emerges)
- Feature Backlog items (Marketplace, IoT, etc.)

## Maintenance and Support (Ongoing)
- Security patches and updates
- Performance optimization
- User feedback collection and response
- Documentation updates
- Dependency management
- Code refactoring / Technical debt management
- ISO 27001 continuous improvement (Post-MVP)

---

This roadmap focuses on delivering the MVP. Post-MVP items are subject to change.

Last Updated: [Insert Current Date] - MVP Refocus
Version: 0.6.0 (MVP Plan) 