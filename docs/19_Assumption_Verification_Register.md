# Source & Evidence Discipline, Assumption & Verification Register
## VELOOP Rewards — Product Analytics, Data Readiness & Data Management Blueprint
**Deliverable Code:** `DELIV-21` (Work Package S & Section 6)  
**Author / Analyst:** Pushti Kotak  
**Document Classification:** Internal Analytics Standard / Data Governance Blueprint  
**Date of Initial Assessment:** 02 November 2026  
**Status:** Maintained & Active  

---

## 1. Executive Context & Mandatory Data Integrity Standard

Per Section 2, Section 6, and Section 34 of the VELOOP Data Analyst Internship Task 01 Specification, this document establishes the **formal evidentiary baseline** for the entire analytical foundation. 

VELOOP Rewards is an active, developing product ecosystem. Production telemetry is not yet established at scale. Under senior analytics governance:
1. **Never convert assumptions into facts.** If an engineering mechanism or operational threshold is unverified, it must be explicitly recorded and tagged as `Proposed` or `To Be Verified`.
2. **Never invent production figures.** All analytical testing is executed on explicitly labeled simulated datasets.
3. **Traceability:** Every architectural decision, KPI formulation, and data schema field in this blueprint traces back directly to official documentation, verified industry benchmarks, or recorded engineering proposals.

```
+-----------------------------------------------------------------------------------------+
| MANDATORY GOVERNANCE NOTICE:                                                            |
| All datasets, profiling results, and numerical examples presented in this project are: |
| "SIMULATED DATA — CREATED FOR ANALYTICAL TESTING"                                       |
| They do not represent actual VELOOP production statistics, users, earnings, or margins. |
+-----------------------------------------------------------------------------------------+
```

---

## 2. Master Source & Evidence Register

This register catalogues every confirmed piece of product knowledge, competitor benchmark, and technical requirement utilized in the blueprint, establishing exact lineage, publication/access dates, and evidentiary confidence.

| Ref ID | Information / Product Fact | Source Name & Origin | Source Type | Date Checked | Verification Status | Analytical Significance & Operational Notes |
|:---|:---|:---|:---|:---|:---|:---|
| **SRC-01** | VELOOP core mission: multi-sided rewards platform connecting users with advertisers, tasks, games, and payout partners. | `Data_Analyst_01.pdf` (p. 1–5, 44) | Official Task Spec | 02 Nov 2026 | **Confirmed** | Establishes the three-sided marketplace model: Advertiser $\rightarrow$ VELOOP $\rightarrow$ User. |
| **SRC-02** | Core product areas: User accounts, earning activities, VEs, XP, Gems, Tokens, Spins, daily rewards, streaks, tasks, missions, badges, levels, referrals, wallet, withdrawals. | `Data_Analyst_01.pdf` (p. 2) | Official Task Spec | 02 Nov 2026 | **Confirmed** | Forms the foundational domain taxonomy for the Logical Data Model and Event Tracking Plan. |
| **SRC-03** | Earning lifecycle progression: Discovery $\rightarrow$ Start $\rightarrow$ Completion $\rightarrow$ Validation $\rightarrow$ Reward. | `Data_Analyst_01.pdf` (p. 8, C1–C4) | Official Task Spec | 02 Nov 2026 | **Confirmed** | Mandates distinguishing task completion from reward crediting, and accounting for external partner postbacks. |
| **SRC-04** | Withdrawal lifecycle progression: Requested $\rightarrow$ Under Review / Processing $\rightarrow$ Completed / Rejected / Reversed. | `Data_Analyst_01.pdf` (p. 10–11, D1–D3) | Official Task Spec | 02 Nov 2026 | **Confirmed** | Establishes double-entry wallet reconciliation and asynchronous payout status transitions. |
| **SRC-05** | Referral lifecycle progression: Referral Created $\rightarrow$ User Registered $\rightarrow$ User Activated $\rightarrow$ Referral Converted. | `Data_Analyst_01.pdf` (p. 12, E1) | Official Task Spec | 02 Nov 2026 | **Confirmed** | Prohibits equating registration with referral conversion; requires multi-stage attribution. |
| **SRC-06** | Third-party offerwall networks: CPX Research, Torox, AdGate, Lootably, BitLabs, RevU, AyeT Studios, AdGem, TimeWall, Monlix, YourSurveys. | `Pushti VELOOP_Rewards_GPT_Industry_Research.pdf` (p. 11, 14) | Industry Benchmark | 31 Oct 2026 | **Confirmed (Benchmarked)** | Partner integrations vary by region; analytics must isolate provider-specific postbacks and dispute rates. |
| **SRC-07** | Monetization & unit economics benchmark: Advertiser gross payout vs. User reward share (hypothetical 65/35 split model) & reverse chargebacks. | `Pushti VELOOP_Rewards_GPT_Industry_Research.pdf` (p. 15) | Industry Benchmark | 31 Oct 2026 | **Confirmed (Model)** | Mandates separating partner receivables, pending user rewards, and approved liability in the wallet data model. |
| **SRC-08** | JumpTask credit economics: Fixed conversion of 1,000 credits = US$1.00; minimum cashout US$0.50. | JumpTask Official Doc (`jumptask.io/how-does-jumptask-work/`) | External Official | 31 Oct 2026 | **Confirmed (Competitor)** | Informs VELOOP’s multi-currency reward exchange model (VEs, Gems, USD/INR conversion). |
| **SRC-09** | Freecash engagement mechanics: Streaks, leagues, level-based tiering, and region-locked payout rules. | Freecash Support & Academy (`freecash.com/academy/en/support/`) | External Official | 31 Oct 2026 | **Confirmed (Competitor)** | Provides architecture for gamification entities (streaks, badges, leagues) and fraud prevention. |
| **SRC-10** | Swagbucks everyday engagement: Search, magic receipts, daily polls, and tiered goal streak bonuses. | Swagbucks Help Center (`help.swagbucks.com/hc/en-us/`) | External Official | 31 Oct 2026 | **Confirmed (Competitor)** | Guides daily check-in logic and non-task micro-engagement event tracking. |
| **SRC-11** | Minimum Event Tracking Plan mandate: $\ge 25$ meaningful events across 6 product domains. | `Data_Analyst_01.pdf` (p. 13–15, F1) | Official Task Spec | 02 Nov 2026 | **Confirmed** | Minimum regulatory requirement for production event telemetry deliverable. |
| **SRC-12** | VELOOP Data Dictionary mandate: $\ge 75$ meaningful fields across 12 metadata dimensions. | `Data_Analyst_01.pdf` (p. 16, G1) | Official Task Spec | 02 Nov 2026 | **Confirmed** | Core metadata governance requirement across logical entities. |
| **SRC-13** | KPI Catalogue mandate: $\ge 30$ standardized KPIs with reproducible definitions and formulas. | `Data_Analyst_01.pdf` (p. 18–20, I1) | Official Task Spec | 02 Nov 2026 | **Confirmed** | Formal metric governance standard prohibiting arbitrary operational targets. |
| **SRC-14** | Simulated dataset working pack sizing: Users (1,000), Tasks (6,000), Rewards (5,000), Wallet (3,500), Withdrawals (1,200), Referrals (900), Events (12,000), Messy Data (500+). | `Data_Analyst_01.pdf` (p. 36, Sec 28) | Official Task Spec | 02 Nov 2026 | **Confirmed** | Sizing parameters for synthetic testing generation and profiling scripts. |
| **SRC-15** | Data quality defect taxonomy: 14 mandatory anomaly categories in `Messy_Data` sheet. | `Data_Analyst_01.pdf` (p. 22, Sec 17) | Official Task Spec | 02 Nov 2026 | **Confirmed** | Benchmark for automated data quality detection and prevention frameworks. |

---

## 3. Master Assumption & Verification Register

This register documents every technical unknown, engineering dependency, data model assumption, and integration risk encountered during blueprint formulation. Each item is assigned an operational risk level, mitigation strategy, and verification owner.

| Assumption ID | Category | Item / Unknown Description | Why It Matters to Analytics | Source Checked | Risk Level | Verification Owner | Current Status | Proposed Solution / Architectural Mitigation |
|:---|:---|:---|:---|:---|:---|:---|:---|:---|
| **ASM-001** | Identity | Does the client application generate and store a persistent `session_id` across app foreground/background transitions? | Essential for calculating session duration, bounce rates, and session-level task conversion. | Official Docs | **High** | Client Eng Lead | `Proposed` | Implement client-side UUIDv4 session generator with 30-minute inactivity timeout window. |
| **ASM-002** | Tracking | Do third-party offerwall postbacks include a deterministic `click_id` / `sub_id` that maps to VELOOP's internal `user_id` and `task_id`? | Critical for attribution reconciliation and detecting third-party partner tracking discrepancies. | Competitor Review | **Critical** | Backend / Partner Eng | `To Be Verified` | Mandate dynamic query parameter `sub_id={user_id}` and `sub_id2={task_id}` in all outgoing offerwall redirect URLs. |
| **ASM-003** | Currency | Are VEs (VELOOP Earnings), XP, and Gems distinct virtual currencies with separate ledger balances? | Dictates whether the wallet schema requires a multi-currency ledger or a single-currency table with rate conversion. | Spec p. 2 | **High** | Product Manager | `Proposed` | Design a multi-currency transaction model supporting `unit IN ('VE', 'XP', 'GEM', 'TOKEN', 'USD', 'INR')`. |
| **ASM-004** | Ledger | Is wallet balance calculated as a materialized aggregate column or dynamically computed from transaction history? | Materialized balance risks race conditions; dynamic calculation risks query latency at scale. | Spec p. 10 | **Critical** | Backend / DBA | `Proposed` | Implement double-entry transaction ledger with periodic snapshotting (daily user balance rollups). |
| **ASM-005** | Deduplication | How does backend prevent duplicate event ingestion when mobile clients retry failed network requests? | Prevents double-counting user registrations, task starts, and critical reward credits. | Spec p. 27 | **Critical** | Platform Eng | `Proposed` | Mandate client-side `event_id` (UUIDv4) and unique server-side idempotency constraint on `(event_name, user_id, idempotency_key)`. |
| **ASM-006** | Task Status | Can a task transition directly from `task_started` to `reward_credited` without an intermediate `task_completed` or `validation_pending` event? | Direct skips distort task completion funnels and prevent tracking validation latency. | Spec p. 8–9 | **High** | Product / QA | `To Be Verified` | Enforce strict state machine: `Started` $\rightarrow$ `Submitted` $\rightarrow$ `Validating` $\rightarrow$ `Completed` $\rightarrow$ `Credited`. Flag illegal transitions as data quality defects. |
| **ASM-007** | Reversals | What is the maximum operational lookback window for third-party offerwall chargebacks/reversals? | Determines how long user balances must hold "pending liability" before becoming fully withdrawable. | Competitor Doc p. 15 | **High** | Finance / Ops | `To Be Verified` | Propose a 30-day rolling reversal reserve for high-risk offers, releasing funds to withdrawable balance upon validation. |
| **ASM-008** | Referrals | What constitutes "User Activated" for referral reward qualification? (e.g., email verify vs. first task complete). | Essential for defining the referral conversion funnel and calculating referral CAC. | Spec p. 12 | **High** | Growth / Marketing | `Proposed` | Define `User Activated` as completing $\ge 1$ validated task or reaching 100 VEs earned; document in KPI Catalogue. |
| **ASM-009** | Identity/PII | Does VELOOP capture IP addresses or precise GPS coordinates during user login/withdrawal? | Highly sensitive personal data governed by GDPR/DPDP. Required for fraud detection but restricted for analytics. | Spec p. 29 | **High** | Legal / Privacy | `Proposed` | Mask IP addresses at ingestion (`192.168.1.0/24`) and convert to coarse ISO country/region codes; truncate geo coordinates to 2 decimal places. |
| **ASM-010** | Ingestion | What is the planned ingestion architecture for product telemetry (batch ETL vs. event streaming)? | Influences event latency, pipeline reliability, and dashboard refresh cadences. | Spec p. 28 | **Medium** | Data Eng Lead | `Proposed` | Propose a lightweight serverless HTTP ingestion endpoint buffering to cloud object storage (S3/GCS) with hourly micro-batch ELT into PostgreSQL/Snowflake. |
| **ASM-011** | Payout Fees | Are withdrawal transaction fees deducted from user payout or absorbed by VELOOP? | Impacts net payout calculations and withdrawal KPI formulas (`net_payout_amount` vs. `requested_amount`). | Competitor Doc p. 12 | **Medium** | Finance Lead | `To Be Verified` | Model explicit `fee_amount` and `net_amount` columns in `withdrawals` table to support both business models without schema changes. |
| **ASM-012** | Gamification | Are daily streaks reset based on UTC midnight or the user's local timezone? | Inconsistent streak resets trigger user disputes and corrupt retention analytics. | Spec p. 2 | **Medium** | Product / Eng | `Proposed` | Propose evaluating streaks against user's stored `timezone` offset, falling back to UTC if timezone metadata is missing. |

---

## 4. Operational Sign-off & Verification Workflow

To maintain absolute data integrity throughout development, the following lifecycle is applied to every item in this register:

```
[ Proposed ]  --> (Engineering Review / Source Validation) 
              --> [ To Be Verified ] 
              --> (Official Implementation / Source Confirmation) 
              --> [ Confirmed ]
```

1. **Analytical Grounding:** No database column, event property, or KPI calculation is treated as production-ready until its status reaches `Confirmed`.
2. **Backlog Linkage:** Any item marked `Critical` or `High` risk with status `To Be Verified` is mapped directly to a user story in the **Final Implementation Backlog** (`DELIV-22`) for pre-launch resolution.
3. **Audit Trail:** Dates, reviewer IDs, and verification notes are permanently logged in the accompanying spreadsheet workbook (`workbooks/DELIV-21_Assumption_Verification_Register.xlsx`).

---
*End of Deliverable DELIV-21 — Maintained under VELOOP Product Analytics Governance Standard.*
