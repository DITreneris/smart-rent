# SmartRent MVP - Strategic Development Plan (Morning Session 1)

## 1. Assessment Summary (Agreed)

Based on the initial codebase analysis, we've identified the following:

**Strengths:**
*   Clear separation of concerns (frontend, backend, contracts).
*   Modern tech stack foundation (React, FastAPI, MongoDB, Solidity).
*   Standard project structures are in use.
*   Existing documentation provides a starting point.
*   Basic CI/CD, testing frameworks, and Docker setup exist.

**Weaknesses:**
*   **Redundant Backend:** Two separate FastAPI applications (`app` and `backend/app`) exist. `app` is more developed and considered primary.
*   **Documentation Mismatch:** Key documents (`ARCHITECTURE.md`, `ROADMAP.md`) inaccurately describe the use of Solana and Hyperledger Fabric, while the implemented contract (`SmartRent.sol`) is Solidity/EVM-based.
*   **Incomplete Core Logic:** `SmartRent.sol` is currently minimal; core rental logic resides off-chain. Complex features like transaction monitoring are incomplete.
*   **Incomplete Testing:** Critical test suites (integration, E2E, contract) are missing or incomplete.

**Risks:**
*   **Technical Debt:** Redundancy and documentation errors.
*   **Development Bottlenecks:** Unnecessary complexity (e.g., documented multi-chain features) and incomplete critical components (transaction monitoring).
*   **Instability:** Lack of comprehensive testing.
*   **Scope Creep:** Ambitious roadmap features distracting from MVP focus.

## 2. Key Strategic Decisions (Agreed)

To address the weaknesses and mitigate risks for an investor-ready MVP:

*   **Consolidate Backend:** Eliminate the `backend/app` directory. All backend logic will reside within the `app` directory structure.
*   **Correct Documentation:** Remove all references to Solana and Hyperledger Fabric from documentation. Update `ARCHITECTURE.md`, `ROADMAP.md`, and `README.md` to reflect the actual MVP stack: React, FastAPI (`app`), MongoDB, and minimal Solidity/EVM.
*   **Simplify Smart Contract:** The `SmartRent.sol` contract's role in the MVP will be strictly minimal – either as a metadata anchor or for emitting basic events (e.g., `RentalConfirmed`). Complex business logic will remain off-chain.
*   **Focus on Core MVP Flow:** Define and implement the absolute minimal viable rental process. Postpone advanced features (multi-chain, AI, advanced analytics, messaging, full ISO 27001 certification) until post-MVP.
*   **Prioritize Testing:** Focus testing efforts on integration tests for the core rental flow (Frontend <-> Backend <-> DB) and basic unit/contract tests for essential components.

## 3. Immediate Action Items & Current Status

1.  **Execute Codebase Consolidation:** Delete `backend/app`. **Status:** ✅ **DONE**.
2.  **Execute Documentation Cleanup:** Update `ARCHITECTURE.md`, `ROADMAP.md`, `README.md`. **Status:** ✅ **DONE**.
3.  **Define MVP Rental Flow:** Finalize flow (Propose -> Accept -> Confirm). **Status:** ✅ **DONE**.
4.  **Refactor Smart Contract (`SmartRent.sol`):** Update contract for MVP flow. **Status:** ✅ **DONE**.
5.  **Structure Backend Proposal Flow:** Implement models, schemas, services, router. **Status:** ✅ **DONE**.
6.  **Implement Core Service Logic:** Fill in methods in `ProposalService`. **Status:** ✅ **DONE**.
7.  **Implement Blockchain Service Logic:** Implement `BlockchainService` with web3.py. **Status:** ✅ **DONE**.
8.  **Implement Dependencies:** Ensure `get_db`, `get_current_active_user`, User model (`wallet_address`) are functional. **Status:** ✅ **DONE** (Verified `get_db`, auth service refactored, `wallet_address` exists).
9.  **Implement Metadata Handling:** Defined strategy (MongoDB collection), created model/service/router, integrated URI generation in `ProposalService`. **Status:** ✅ **DONE**.
10. **Configure Blockchain Interaction:** Set up `.env` with RPC URL, Contract Address/ABI, Platform Private Key, etc. **Status:** ✅ **DONE** (User manually configured `.env` for local SQLite & Sepolia; AI cannot read `.env` directly). **Issues:** ABI required contract compilation (`npx hardhat compile`) using Hardhat, which involved installing dependencies (`@openzeppelin/contracts`) and fixing Solidity version mismatch in `hardhat.config.js`.
11. **Implement ID Conversion:** Finalized logic in `ProposalService` (hashing proposal ID for metadata URI). **Status:** ✅ **DONE**.
12. **Run Initial Database Setup:** Apply Alembic migrations. **Status:** ✅ **DONE**. **Issues:** Required multiple fixes for SQLite compatibility in migrations (ImportError in `app/models/__init__.py`; async handling in `app/migrations/env.py`; removed `ON UPDATE CURRENT_TIMESTAMP` from `updated_at` in `001`, `002`, `003`, `006`; used batch mode for constraints in `004`, `005`, `006`).
13. **Troubleshoot Python Environment & Test Script (`scripts/test_blockchain_service.py`):** **Status:** ✅ **DONE**.
    *   **Initial Problem:** `ModuleNotFoundError: No module named 'dotenv'` despite being in `requirements.txt`.
    *   **Investigation & Fixes:**
        *   Verified `python-dotenv` was in `requirements.txt`.
        *   Attempted `pip install -r requirements.txt` - revealed `web3`/`eth-typing` compatibility issues with Python 3.11.
        *   Updated `web3` to `6.14.0` and `eth-typing` to `4.3.0` in `requirements.txt`.
        *   Resolved `PyJWT` conflict by downgrading to `1.7.1` for `fastapi-jwt-auth` compatibility.
        *   Persistent `ModuleNotFoundError: No module named 'dotenv'`.
        *   Investigated Python interpreter and `sys.path`, revealing an almost empty `site-packages` in `.venv`.
        *   Root Cause: `pip install` was not correctly installing packages into the virtual environment's `site-packages` when run as `pip install ...`.
        *   **Solution:** Used the explicit path to the virtual environment's Python interpreter for pip: `.\.venv\Scripts\python.exe -m pip install -r requirements.txt`. This correctly populated `site-packages`.
    *   **Script Execution Issues & Resolutions (`scripts/test_blockchain_service.py`):**
        *   `TypeError: Settings.__init__() got an unexpected keyword argument 'CONTRACT_ABI_PATH'` (due to Pydantic v1/v2 differences): Changed `field_validator` to `validator` and adjusted import of `BaseSettings` from `pydantic_settings` to `pydantic` in `app/core/config.py`.
        *   `ImportError: email-validator is not installed`: Added `email-validator` to `requirements.txt` and installed.
        *   `ModuleNotFoundError: No module named 'sqlalchemy'`: Added `SQLAlchemy` to `requirements.txt` and installed.
        *   `ModuleNotFoundError: No module named 'app.services.blockchain_service'`: Corrected import in `test_blockchain_service.py` from `app.services.blockchain_service` to `app.services.blockchain`.
        *   `AttributeError: 'Settings' object has no attribute 'RPC_URL'`: Corrected `settings.RPC_URL` to `settings.WEB3_PROVIDER_URL` in `test_blockchain_service.py`.
        *   `AttributeError: 'BlockchainService' object has no attribute 'get_platform_address'`: Implemented `__init__`, `get_platform_address`, and `get_contract` methods in `app/services/blockchain.py`.
        *   Refactored `trigger_confirm_rental` in `BlockchainService` to be an instance method and use initialized `self.w3`, `self.account`, `self.contract`.
    *   **Lessons Learned:**
        *   Always verify the correct Python interpreter and `pip` executable are being used, especially within virtual environments. Explicit paths can be a lifesaver.
        *   Dependency conflicts can be subtle. `pip install` output needs careful review.
        *   Pydantic v1 vs. v2 differences (e.g., `field_validator` vs. `validator`, `pydantic_settings`) require careful attention during upgrades or when working with older codebases.
        *   Module and attribute errors often point to incorrect import paths, typos, or incomplete class implementations.
        *   Systematic debugging (checking `sys.path`, listing `site-packages`, testing imports directly) is crucial for diagnosing `ModuleNotFoundError`.

## 4. Next Steps (Post-Database Setup)

*   **Test `BlockchainService`:** Create a basic script to instantiate the service and test basic calls (e.g., `get_contract`, `get_platform_address`). **Status:** ✅ **DONE** (`scripts/test_blockchain_service.py` successfully runs, connects to node, loads contract, and retrieves platform address. Contract interaction calls will still fail until the contract is deployed and `CONTRACT_ADDRESS` is updated).
*   **Test `BlockchainService.trigger_confirm_rental`:** Further test this method with a deployed contract on a testnet. This will involve updating `.env` with a real `CONTRACT_ADDRESS` and potentially mock data or a simple frontend interaction.
*   **Start Frontend Development:** Set up React project (e.g., using Vite or CRA) and begin building components for the core rental flow.
*   **Implement Core Testing:** Set up `pytest` and write unit/integration tests for backend services (Auth, Proposals, etc.), potentially using a test database.
*   **Verify Docker Setup:** Ensure the full stack runs correctly using Docker Compose.

## 5. Proposed MVP Roadmap Outline (Revised Status)

*   **Phase 1: Consolidation & Simplification (Complete)**
    *   ✅ Delete `backend/app`.
    *   ✅ Update documentation.
    *   ✅ Review/simplify `SmartRent.sol`.
*   **Phase 2: Core MVP Feature Implementation (In Progress)**
    *   ⬜ Implement the defined minimal viable rental flow (Frontend UI).
    *   ✅ Implement essential backend services (`ProposalService`, `BlockchainService` logic complete, initial testing of `BlockchainService` successful).
    *   ✅ Implement blockchain interaction logic (`BlockchainService` implemented, refactored, and basic functionality tested).
    *   ✅ Implement Metadata Handling.
    *   ✅ Implement Dependencies (`get_db`, auth, User model attributes).
    *   ✅ Configure Blockchain Interaction (`.env` setup).
    *   ✅ Run Initial DB Setup (Alembic migrations).
    *   ⬜ Implement basic transaction/state monitoring (if required by flow).
    *   ⬜ Implement basic user dashboard view.
    *   ✅ Implement essential security measures (in progress via service logic).
*   **Phase 3: Testing & Stabilization (Upcoming)**
    *   ⬜ Test Blockchain Service (`trigger_confirm_rental`) against a deployed testnet contract.
    *   ⬜ Write integration tests for the core flow.
    *   ⬜ Write essential unit/component tests.
    *   ⬜ Manual testing and bug fixing.
    *   ⬜ Ensure logging and error handling are adequate.
    *   ⬜ Prepare deployment scripts/documentation.
    *   ⬜ Verify Docker setup.

---
*This plan provides a strategic framework. Detailed task breakdown should occur within sprint planning.* 