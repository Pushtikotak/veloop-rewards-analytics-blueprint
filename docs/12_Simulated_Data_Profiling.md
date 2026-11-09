# Simulated Data Profiling & Referential Integrity Report
## VELOOP Rewards — Product Analytics, Data Readiness & Data Management Blueprint
**Deliverable Code:** `DELIV-12` (Work Package J)  
**Author / Analyst:** Pushti Kotak  
**Document Classification:** Internal Technical Architecture / Data Profiling  
**Date:** 02 November 2026  
**Companion File:** `workbooks/DELIV-12_Simulated_Data_Profiling.xlsx`  
**Status:** Complete & Verified  

---

```
+-----------------------------------------------------------------------------------------+
| MANDATORY GOVERNANCE NOTICE:                                                            |
| All profiled datasets in this report are:                                               |
| 'SIMULATED DATA — CREATED FOR ANALYTICAL TESTING'                                       |
| Seed: 42 | Engine: scripts/generate_simulated_data.py | Generator Date: 2026-11-02       |
| These metrics test architectural readiness and do NOT represent actual VELOOP results.  |
+-----------------------------------------------------------------------------------------+
```

## 1. Executive Summary & Profiling Scope

In accordance with Section 16 (Work Package J) and Section 28 of the internship task specification, this document profiles the complete 8-dataset synthetic test working pack (~30,000+ total rows). The profiling confirms:
1. **Data Sizing & Coverage:** All 8 datasets achieve the exact target sizing mandated in Section 28.
2. **Referential Integrity:** 100% clean foreign key linkage across `dim_users`, `dim_tasks`, `fct_task_activity`, `fct_rewards`, `fct_wallet_transactions`, `fct_withdrawals`, and `fct_referrals` (zero orphan records).
3. **KPI Feasibility:** All sampled core metrics from the KPI Catalogue (`DELIV-11`) are mathematically calculable from the schema structure without missing prerequisite fields.

---

## 2. J1. Master Dataset Profiling Overview

| Dataset Name | Total Records | Total Columns | Primary Key | Unique Keys | Duplicate PKs | Null Cells | Null % | Date Range | Quality Status |
|:---|:---|:---|:---|:---|:---|:---|:---|:---|:---|
| **Users** | 1,000 | 20 | `user_id` | 1,000 | 0 | 859 | 4.3% | 2026-08-01 to 2026-10-26 | **100% Clean** |
| **Catalog Tasks** | 50 | 12 | `task_id` | 50 | 0 | 0 | 0.0% | 2026-07-02 to 2026-07-02 | **100% Clean** |
| **Task Activity** | 6,000 | 14 | `task_activity_id` | 6,000 | 0 | 9,250 | 11.01% | 2026-08-06 to 2026-11-01 | **100% Clean** |
| **Rewards** | 5,000 | 11 | `reward_id` | 5,000 | 0 | 6,600 | 12.0% | 2026-08-06 to 2026-11-01 | **100% Clean** |
| **Wallet Transactions** | 3,500 | 13 | `transaction_id` | 3,500 | 0 | 6,446 | 14.17% | 2026-08-11 to 2026-11-01 | **100% Clean** |
| **Withdrawals** | 1,200 | 14 | `withdrawal_id` | 1,200 | 0 | 1,375 | 8.18% | 2026-08-16 to 2026-11-01 | **100% Clean** |
| **Referrals** | 900 | 13 | `referral_id` | 900 | 0 | 1,608 | 13.74% | 2026-08-03 to 2026-10-27 | **100% Clean** |
| **Feature Events** | 12,000 | 10 | `event_id` | 12,000 | 0 | 0 | 0.0% | 2026-08-04 to 2026-11-01 | **100% Clean** |
| **Messy Data** | 550 | 8 | `issue_record_id` | 433 | 116 | 119 | 2.7% | 2026-10-15 to 2026-10-15 | **Defects Detected** |

---

## 3. J2. Relational Integrity & Key Linkage Audit

Testing whether `dim_users.user_id` connects cleanly across all downstream fact tables:

| Foreign Key Relationship | Tested Rows | Orphan Rows Detected | Audit Status | Diagnostic Finding |
|:---|:---|:---|:---|:---|
| `fct_task_activity.user_id -> dim_users.user_id` | 6,000 | **0** | **PASSED** | 100% referential integrity; all task attempts belong to valid users. |
| `fct_task_activity.task_id -> dim_tasks.task_id` | 6,000 | **0** | **PASSED** | 100% integrity; all attempts map to registered catalog campaigns. |
| `fct_rewards.user_id -> dim_users.user_id` | 5,000 | **0** | **PASSED** | All rewards credited to verified user accounts. |
| `fct_rewards.task_activity_id -> fct_task_activity` | 3,400 | **0** | **PASSED** | All task-based rewards trace directly to a valid task activity row. |
| `fct_wallet_transactions.user_id -> dim_users.user_id` | 3,500 | **0** | **PASSED** | Double-entry ledger references existing user accounts without orphans. |
| `fct_withdrawals.user_id -> dim_users.user_id` | 1,200 | **0** | **PASSED** | All cashout transactions link directly to registered users. |
| `fct_referrals.referrer_user_id -> dim_users` | 900 | **0** | **PASSED** | All referral links created by registered referrers. |
| `fct_referrals.referred_user_id -> dim_users` | 679 | **0** | **PASSED** | All referred registrants exist in dim_users. |

---

## 4. J3. KPI Calculability & Feasibility Test

To verify that the proposed analytical model supports production decision-making, we executed a calculability validation on a representative sample of core KPIs:

| Tested KPI | Required Tables | Required Fields | Calculability | Status | Empirical Test Result on Simulated Pack |
|:---|:---|:---|:---|:---|:---|
| **KPI-02: Daily Active Users (DAU)** | `fct_feature_events` | `user_id, server_timestamp` | Calculable | **PASSED** | Successfully computed; average DAU is 382 unique users per day. |
| **KPI-10: Task Completion Rate (%)** | `fct_task_activity` | `activity_status` | Calculable | **PASSED** | Calculated as 58.2% completed vs 78.5% initiated. |
| **KPI-15: Reward Reversal Rate (%)** | `fct_rewards` | `amount, status` | Calculable | **PASSED** | Calculated as 2.48% reversal rate; within target threshold. |
| **KPI-27: Median Withdrawal Processing Time** | `fct_withdrawals` | `requested_timestamp, final_timestamp, status` | Calculable | **PASSED** | Calculated as 4.8 hours median settlement duration. |
| **KPI-32: Referral Activation Rate (%)** | `fct_referrals` | `referral_status` | Calculable | **PASSED** | Calculated as 36.4% activation rate among registered invitees. |
| **KPI-06: Stickiness (DAU/MAU)** | `fct_feature_events` | `user_id, server_timestamp` | Calculable | **PASSED** | Calculated as 23.8% stickiness ratio; healthy habituation. |
| **KPI-22: Ledger Discrepancy Rate** | `fct_wallet_transactions` | `balance_before, balance_after, amount` | Calculable | **PASSED** | 100% mathematical consistency across all transactions. |
| **KPI-35: Missing Credit Dispute Rate** | `fct_support_tickets, fct_task_activity` | `ticket_id, task_activity_id` | Calculable with Extension | **WARNING** | Requires joining support tickets with task activities; resolved in logical model. |

---
*End of Deliverable DELIV-12 — Simulated Data Profiling Report.*
