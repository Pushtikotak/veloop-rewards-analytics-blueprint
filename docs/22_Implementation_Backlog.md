# Final Implementation Backlog
## VELOOP Rewards — Product Analytics, Data Readiness & Data Management Blueprint
**Deliverable Code:** `DELIV-22` (Section 26 & Work Package T)  
**Author / Analyst:** Pushti Kotak  
**Document Classification:** Engineering Sprint Specification / Implementation Backlog  
**Date:** 02 November 2026  
**Companion File:** `workbooks/DELIV-22_Implementation_Backlog.xlsx`  
**Status:** Complete & Verified  

---

## 1. Backlog Governance & Launch Segmentation

In accordance with Section 26 of the VELOOP Internship Task Specification, this backlog formalizes the prioritized development requirements necessary to deploy the analytics blueprint. Work is segmented into two operational stages:
1. **Pre-Launch Gate (Critical & High Priority):** 12 core epics that MUST be fully tested, verified, and signed off in staging before production user traffic or commercial payouts are enabled.
2. **Post-Launch Optimizations (Medium & Low Priority):** 6 enhancement epics focused on secondary gamification loops, currency swaps, and support telemetry scheduled for subsequent sprints.

---

## 2. Prioritized Implementation Backlog Table (18 Epics)

| Item ID | Priority | Requirement Name | Core Reason & Architectural Need | Dependency | Owner | Effort | Launch Stage |
|:---|:---|:---|:---|:---|:---|:---:|:---:|
| **BLG-001** | **Critical** | **Stable User ID Architecture** | Required for permanent cross-session tracking... | `Auth Service` | Backend / Identity Team | 5 SP | **Pre-launch** |
| **BLG-002** | **Critical** | **Double-Entry Transaction Ledger** | Eliminates race conditions and overwriting bu... | `Wallet Service` | Backend / DBA | 8 SP | **Pre-launch** |
| **BLG-003** | **Critical** | **Event Ingestion Deduplication (Redis)** | Prevents duplicate crediting when mobile clie... | `API Gateway` | Platform / Infra Eng | 5 SP | **Pre-launch** |
| **BLG-004** | **Critical** | **Outbound Click-ID Attribution** | Ensures incoming partner postbacks can be map... | `Click Router` | Backend / Partner Eng | 5 SP | **Pre-launch** |
| **BLG-005** | **Critical** | **Withdrawal Escrow Locking State Machine** | Prevents double-spending during cashouts by i... | `Payout Service` | Backend Core Team | 8 SP | **Pre-launch** |
| **BLG-006** | **Critical** | **PII Cryptographic Masking & RBAC** | Prevents exposure of sensitive PayPal/UPI han... | `Security Layer` | Data Platform / Security | 5 SP | **Pre-launch** |
| **BLG-007** | **High** | **Multi-State Balance Separation** | Separates pending rewards under hold from wit... | `Wallet Service` | Backend Core Team | 5 SP | **Pre-launch** |
| **BLG-008** | **High** | **4-Stage Referral Funnel Enforcement** | Blocks sybil registration farming by creditin... | `Referral Engine` | Growth / Backend Eng | 5 SP | **Pre-launch** |
| **BLG-009** | **High** | **Automated Daily Ledger Audit Script** | Zero-tolerance monitoring job verifying mathe... | `Data Warehouse` | Analytics Eng / DBA | 3 SP | **Pre-launch** |
| **BLG-010** | **High** | **Partner Webhook HMAC Signature Validation** | Protects platform from forged partner callbac... | `Webhook Gateway` | Security / Backend Eng | 3 SP | **Pre-launch** |
| **BLG-011** | **High** | **Micro-Batch ELT Pipeline (Bronze to Silver)** | Automates ingestion from raw S3 compressed JS... | `S3 / dbt` | Data Platform Eng | 8 SP | **Pre-launch** |
| **BLG-012** | **High** | **Core Power BI Dashboard Semantic Model** | Implements standardized DAX measures and dime... | `Power BI` | BI Specialist / Analyst | 8 SP | **Pre-launch** |
| **BLG-013** | **Medium** | **Daily Streak Reset & Recovery Telemetry** | Tracks streak continuity and provides 24-hour... | `Streak Service` | Mobile / Backend Eng | 5 SP | **Post-launch** |
| **BLG-014** | **Medium** | **Gamification Quest & Mission Engine** | Instruments missions, badges, and XP level mu... | `Game Engine` | Product / Backend Eng | 5 SP | **Post-launch** |
| **BLG-015** | **Medium** | **Customer Support Dispute CRM Integration** | Connects missing credit ticket submissions di... | `Support Desk` | Full-Stack Eng | 5 SP | **Post-launch** |
| **BLG-016** | **Medium** | **Virtual Currency Swap Ledger (VE to USD)** | Tracks internal points-to-cash conversions if... | `Exchange Service` | Backend / Finance Eng | 5 SP | **Post-launch** |
| **BLG-017** | **Low** | **FAQ Article Impression & Helpfulness Tracking** | Measures self-service support article effecti... | `Content CMS` | Frontend Web Eng | 2 SP | **Post-launch** |
| **BLG-018** | **Low** | **App Exit Screen & Bounce Telemetry** | Instruments client exit screen logging to ide... | `Mobile SDK` | Mobile Client Eng | 2 SP | **Post-launch** |

---

## 3. Detailed User Stories & Acceptance Criteria

### `BLG-001`: Stable User ID Architecture
* **Priority:** **Critical** | **Launch Stage:** **Pre-launch** | **Estimated Effort:** 5 SP
* **Architectural Reason:** Required for permanent cross-session tracking, lifetime analytics, and GDPR compliance decoupling.
* **System Dependencies:** `Auth Service` | **Responsible Team:** Backend / Identity Team
* **Acceptance Criteria:** Canonical UUIDv4 user_id generated on account creation; immutable across profile updates.

### `BLG-002`: Double-Entry Transaction Ledger
* **Priority:** **Critical** | **Launch Stage:** **Pre-launch** | **Estimated Effort:** 8 SP
* **Architectural Reason:** Eliminates race conditions and overwriting bugs; ensures user balance equals mathematical sum of credits/debits.
* **System Dependencies:** `Wallet Service` | **Responsible Team:** Backend / DBA
* **Acceptance Criteria:** fct_wallet_transactions table committed with mandatory direction, balance_before, and balance_after.

### `BLG-003`: Event Ingestion Deduplication (Redis)
* **Priority:** **Critical** | **Launch Stage:** **Pre-launch** | **Estimated Effort:** 5 SP
* **Architectural Reason:** Prevents duplicate crediting when mobile clients retry failed network requests on cellular connections.
* **System Dependencies:** `API Gateway` | **Responsible Team:** Platform / Infra Eng
* **Acceptance Criteria:** Redis cache enforces 10-minute TTL on event_id; duplicates return HTTP 200 with DUPLICATE_IGNORED.

### `BLG-004`: Outbound Click-ID Attribution
* **Priority:** **Critical** | **Launch Stage:** **Pre-launch** | **Estimated Effort:** 5 SP
* **Architectural Reason:** Ensures incoming partner postbacks can be mapped to internal user_id and task_id without attribution drops.
* **System Dependencies:** `Click Router` | **Responsible Team:** Backend / Partner Eng
* **Acceptance Criteria:** Generates unique click_id; appends sub_id={user_id}&sub_id2={task_id} to external redirect URLs.

### `BLG-005`: Withdrawal Escrow Locking State Machine
* **Priority:** **Critical** | **Launch Stage:** **Pre-launch** | **Estimated Effort:** 8 SP
* **Architectural Reason:** Prevents double-spending during cashouts by immediately locking requested funds in escrow status.
* **System Dependencies:** `Payout Service` | **Responsible Team:** Backend Core Team
* **Acceptance Criteria:** Atomic database transaction deducts balance and creates WITHDRAWAL_ESCROW ledger row simultaneously.

### `BLG-006`: PII Cryptographic Masking & RBAC
* **Priority:** **Critical** | **Launch Stage:** **Pre-launch** | **Estimated Effort:** 5 SP
* **Architectural Reason:** Prevents exposure of sensitive PayPal/UPI handles and IP addresses in analytical BI tables (GDPR/DPDP).
* **System Dependencies:** `Security Layer` | **Responsible Team:** Data Platform / Security
* **Acceptance Criteria:** destination_hash and signup_ip_hash stored as SHA-256; analytical roles granted zero raw PII access.

### `BLG-007`: Multi-State Balance Separation
* **Priority:** **High** | **Launch Stage:** **Pre-launch** | **Estimated Effort:** 5 SP
* **Architectural Reason:** Separates pending rewards under hold from withdrawable funds to prevent losses from advertiser chargebacks.
* **System Dependencies:** `Wallet Service` | **Responsible Team:** Backend Core Team
* **Acceptance Criteria:** dim_users exposes available_balance, pending_balance, and escrow_balance; cashout checks available only.

### `BLG-008`: 4-Stage Referral Funnel Enforcement
* **Priority:** **High** | **Launch Stage:** **Pre-launch** | **Estimated Effort:** 5 SP
* **Architectural Reason:** Blocks sybil registration farming by crediting referral bonuses only after invitee completes a validated task.
* **System Dependencies:** `Referral Engine` | **Responsible Team:** Growth / Backend Eng
* **Acceptance Criteria:** Referral bonus locked until referral_status transitions to Activated; self-referrals blocked via IP check.

### `BLG-009`: Automated Daily Ledger Audit Script
* **Priority:** **High** | **Launch Stage:** **Pre-launch** | **Estimated Effort:** 3 SP
* **Architectural Reason:** Zero-tolerance monitoring job verifying mathematical balance consistency across all user wallets.
* **System Dependencies:** `Data Warehouse` | **Responsible Team:** Analytics Eng / DBA
* **Acceptance Criteria:** Automated cron at 00:30 UTC checks balance discrepancies; triggers P0 alert if discrepancy > 0.

### `BLG-010`: Partner Webhook HMAC Signature Validation
* **Priority:** **High** | **Launch Stage:** **Pre-launch** | **Estimated Effort:** 3 SP
* **Architectural Reason:** Protects platform from forged partner callbacks by cryptographically validating webhook signature headers.
* **System Dependencies:** `Webhook Gateway` | **Responsible Team:** Security / Backend Eng
* **Acceptance Criteria:** Validates HMAC SHA-256 against partner secret; invalid signatures rejected with HTTP 401.

### `BLG-011`: Micro-Batch ELT Pipeline (Bronze to Silver)
* **Priority:** **High** | **Launch Stage:** **Pre-launch** | **Estimated Effort:** 8 SP
* **Architectural Reason:** Automates ingestion from raw S3 compressed JSONL files into normalized PostgreSQL reporting warehouse.
* **System Dependencies:** `S3 / dbt` | **Responsible Team:** Data Platform Eng
* **Acceptance Criteria:** Hourly dbt runner transforms raw payloads into dimensional fact tables with automated schema tests.

### `BLG-012`: Core Power BI Dashboard Semantic Model
* **Priority:** **High** | **Launch Stage:** **Pre-launch** | **Estimated Effort:** 8 SP
* **Architectural Reason:** Implements standardized DAX measures and dimensional star-schema for Executive and Operations reporting.
* **System Dependencies:** `Power BI` | **Responsible Team:** BI Specialist / Analyst
* **Acceptance Criteria:** 7 dashboard views functional; DAX measures reconciled against raw SQL queries with zero variance.

### `BLG-013`: Daily Streak Reset & Recovery Telemetry
* **Priority:** **Medium** | **Launch Stage:** **Post-launch** | **Estimated Effort:** 5 SP
* **Architectural Reason:** Tracks streak continuity and provides 24-hour buffer window adjusted for user local timezone.
* **System Dependencies:** `Streak Service` | **Responsible Team:** Mobile / Backend Eng
* **Acceptance Criteria:** Streak evaluates against local timezone offset; streak_broken event emitted upon missed check-in.

### `BLG-014`: Gamification Quest & Mission Engine
* **Priority:** **Medium** | **Launch Stage:** **Post-launch** | **Estimated Effort:** 5 SP
* **Architectural Reason:** Instruments missions, badges, and XP level multipliers to drive long-term habituation.
* **System Dependencies:** `Game Engine` | **Responsible Team:** Product / Backend Eng
* **Acceptance Criteria:** Missions track real-time event triggers; badges unlocked automatically upon milestone reach.

### `BLG-015`: Customer Support Dispute CRM Integration
* **Priority:** **Medium** | **Launch Stage:** **Post-launch** | **Estimated Effort:** 5 SP
* **Architectural Reason:** Connects missing credit ticket submissions directly to partner postback logs for rapid agent resolution.
* **System Dependencies:** `Support Desk` | **Responsible Team:** Full-Stack Eng
* **Acceptance Criteria:** Support portal renders task_activity_id and partner click_id alongside user ticket.

### `BLG-016`: Virtual Currency Swap Ledger (VE to USD)
* **Priority:** **Medium** | **Launch Stage:** **Post-launch** | **Estimated Effort:** 5 SP
* **Architectural Reason:** Tracks internal points-to-cash conversions if platform introduces intermediate currency exchange.
* **System Dependencies:** `Exchange Service` | **Responsible Team:** Backend / Finance Eng
* **Acceptance Criteria:** Executes atomic currency conversion ledger entry with locked exchange rate.

### `BLG-017`: FAQ Article Impression & Helpfulness Tracking
* **Priority:** **Low** | **Launch Stage:** **Post-launch** | **Estimated Effort:** 2 SP
* **Architectural Reason:** Measures self-service support article effectiveness in reducing repetitive ticket volume.
* **System Dependencies:** `Content CMS` | **Responsible Team:** Frontend Web Eng
* **Acceptance Criteria:** Logs article_viewed and article_rated_helpful events for knowledge base optimization.

### `BLG-018`: App Exit Screen & Bounce Telemetry
* **Priority:** **Low** | **Launch Stage:** **Post-launch** | **Estimated Effort:** 2 SP
* **Architectural Reason:** Instruments client exit screen logging to identify screens causing user session terminations.
* **System Dependencies:** `Mobile SDK` | **Responsible Team:** Mobile Client Eng
* **Acceptance Criteria:** Emits user_logged_out with last_viewed_screen and session_duration_sec.

---
*End of Deliverable DELIV-22 — Final Implementation Backlog.*
