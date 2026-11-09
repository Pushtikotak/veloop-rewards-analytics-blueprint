# Data Quality Defect Audit Report
## VELOOP Rewards — Product Analytics, Data Readiness & Data Management Blueprint
**Deliverable Code:** `DELIV-13` (Work Package K)  
**Author / Analyst:** Pushti Kotak  
**Document Classification:** Internal Technical Architecture / Data Quality Audit  
**Date:** 02 November 2026  
**Companion File:** `workbooks/DELIV-13_Data_Quality_Audit.xlsx`  
**Status:** Complete & Verified  

---

```
+-----------------------------------------------------------------------------------------+
| MANDATORY AUDIT NOTICE:                                                                 |
| This audit was executed on the intentionally corrupted 'Messy_Data' working sheet       |
| (550 records, seeded with 14 defect categories) to validate detection algorithms.       |
| Notice: 'SIMULATED DATA — CREATED FOR ANALYTICAL TESTING'                               |
+-----------------------------------------------------------------------------------------+
```

## 1. Executive Summary & Defect Overview

In accordance with Section 17 of the VELOOP Internship Task Specification, an exhaustive data quality audit was conducted on the synthetic `Messy_Data` sheet. All **14 mandatory defect categories** were systematically detected, categorized by operational severity, and mapped to root causes, corrections, and preventative engineering controls.

### Defect Severity Distribution across 550 Records:
* **Critical Severity:** 8 Issues (Duplicates, Null PKs, Invalid Types, Negative Credits, Orphan Records, State Skips) $ightarrow$ 315 records affected (57.3%).
* **High Severity:** 3 Issues (Missing Timestamps, Malformed Dates, Replay Events) $ightarrow$ 117 records affected (21.3%).
* **Medium Severity:** 2 Issues (Inconsistent Capitalization, Non-Standard Naming) $ightarrow$ 78 records affected (14.2%).
* **Low Severity:** 1 Issue (Whitespace Padding) $ightarrow$ 39 records affected (7.1%).

---

## 2. Complete Data Quality Defect Register (14 Issues)

| Issue ID | Affected Field | Issue Type | Records Affected | Severity | Root Cause | Preventative Control | Owner | Status |
|:---|:---|:---|:---|:---|:---|:---|:---|:---|
| **DQ-01** | `issue_record_id` | **Duplicate Primary Key** | 40 | **Critical** | Client retry without idempotency key; ra... | Enforce UNIQUE constraint on primary key... | Data Platform Eng | **Proposed** |
| **DQ-02** | `issue_record_id` | **Missing Primary Key** | 40 | **Critical** | Client-side payload generation error whe... | Schema validation on API gateway: reject... | Backend Gateway Team | **Proposed** |
| **DQ-03** | `timestamp` | **Missing Timestamp** | 40 | **High** | Mobile client failed to inject device ti... | Default column to CURRENT_TIMESTAMP on i... | Data Eng / Mobile Lead | **Proposed** |
| **DQ-04** | `timestamp` | **Malformed Date Format** | 40 | **High** | Regional locale formatting applied clien... | Enforce strict UTC epoch milliseconds (b... | Mobile Client Eng | **Proposed** |
| **DQ-05** | `status` | **Invalid Status Code** | 39 | **Critical** | Unannounced partner webhook payload chan... | Postgres ENUM or CHECK constraint at dat... | Backend Platform Eng | **Proposed** |
| **DQ-06** | `status` | **Inconsistent Capitalization** | 39 | **Medium** | Mixed client implementations (cOmPLeTeD ... | Normalize string formatting at API inges... | Analytics Eng | **Proposed** |
| **DQ-07** | `status, transaction_type` | **Trailing / Leading Whitespace** | 39 | **Low** | Unsanitized string concatenation in clie... | Pydantic / input validation middleware s... | Analytics Eng | **Proposed** |
| **DQ-08** | `amount` | **Invalid Numeric Format (String in Decimal)** | 39 | **Critical** | Corrupted form input or unvalidated JSON... | Strict JSON schema validation: amount MU... | Backend Gateway Team | **Proposed** |
| **DQ-09** | `amount` | **Illegal Negative Value** | 39 | **Critical** | Incorrect debit sign applied to credit t... | Add database CHECK constraint: amount > ... | Lead Data Architect | **Proposed** |
| **DQ-010** | `user_id` | **Unexpected Null Foreign Key** | 39 | **Critical** | Unauthenticated guest user action errone... | Enforce NOT NULL constraint on user_id a... | Lead Data Architect | **Proposed** |
| **DQ-011** | `user_id` | **Orphan Record (Missing Parent Entity)** | 39 | **Critical** | Out-of-order event ingestion where trans... | Enforce relational FOREIGN KEY constrain... | Data Platform Eng | **Proposed** |
| **DQ-012** | `issue_record_id` | **Duplicate Event Payload (Replay Attack)** | 39 | **High** | Mobile client retry loop on slow cellula... | API gateway Redis deduplication filter w... | Platform Eng | **Proposed** |
| **DQ-013** | `transaction_type` | **Inconsistent Naming Convention** | 39 | **Medium** | Non-standardized ad-hoc logging added by... | Data dictionary linter in CI/CD pipeline... | Data Governance Lead | **Proposed** |
| **DQ-014** | `status` | **Impossible State Transition** | 39 | **Critical** | Race condition or unhandled edge case in... | State machine validation pattern in appl... | Backend Core Team | **Proposed** |

---

## 3. Detailed Root Cause Analysis & Engineering Runbooks

### `DQ-01`: Duplicate Primary Key (Field: `issue_record_id`)
* **Severity Level:** **Critical** | **Records Impacted:** 40 rows
* **Detection SQL / Logic:** `COUNT(issue_record_id) > 1 on primary key column`
* **Likely Root Cause:** Client retry without idempotency key; race condition in message queue.
* **Recommended Data Correction:** Deduplicate by (user_id, timestamp); retain earliest valid receipt.
* **Permanent Preventative Control:** Enforce UNIQUE constraint on primary key and Redis distributed lock at ingestion.
* **Responsible Team:** Data Platform Eng | **Status:** **Proposed**

### `DQ-02`: Missing Primary Key (Field: `issue_record_id`)
* **Severity Level:** **Critical** | **Records Impacted:** 40 rows
* **Detection SQL / Logic:** `ISNULL(issue_record_id) OR issue_record_id = ''`
* **Likely Root Cause:** Client-side payload generation error where UUID generator failed silently.
* **Recommended Data Correction:** Quarantine records in Dead-Letter Queue (DLQ); reject from ingestion.
* **Permanent Preventative Control:** Schema validation on API gateway: reject HTTP payloads lacking valid UUID.
* **Responsible Team:** Backend Gateway Team | **Status:** **Proposed**

### `DQ-03`: Missing Timestamp (Field: `timestamp`)
* **Severity Level:** **High** | **Records Impacted:** 40 rows
* **Detection SQL / Logic:** `ISNULL(timestamp) OR timestamp = ''`
* **Likely Root Cause:** Mobile client failed to inject device time during offline event buffering.
* **Recommended Data Correction:** Backfill using server_received_timestamp with data quality flag.
* **Permanent Preventative Control:** Default column to CURRENT_TIMESTAMP on ingestion database table.
* **Responsible Team:** Data Eng / Mobile Lead | **Status:** **Proposed**

### `DQ-04`: Malformed Date Format (Field: `timestamp`)
* **Severity Level:** **High** | **Records Impacted:** 40 rows
* **Detection SQL / Logic:** `REGEX mismatch against standard ISO-8601 YYYY-MM-DD HH:MM:SS format`
* **Likely Root Cause:** Regional locale formatting applied client-side (DD/MM/YYYY with invalid hours).
* **Recommended Data Correction:** Parse via flexible date parser or route unparseable strings to DLQ.
* **Permanent Preventative Control:** Enforce strict UTC epoch milliseconds (bigint) in mobile SDK payload.
* **Responsible Team:** Mobile Client Eng | **Status:** **Proposed**

### `DQ-05`: Invalid Status Code (Field: `status`)
* **Severity Level:** **Critical** | **Records Impacted:** 39 rows
* **Detection SQL / Logic:** `status NOT IN ('Started', 'Completed', 'Failed', 'Abandoned', 'Requested', 'Processing', 'Rejected', 'Reversed')`
* **Likely Root Cause:** Unannounced partner webhook payload change or unhandled error string.
* **Recommended Data Correction:** Map unrecognized status strings to 'Unknown_Review' and notify operations.
* **Permanent Preventative Control:** Postgres ENUM or CHECK constraint at database layer; strict schema gating.
* **Responsible Team:** Backend Platform Eng | **Status:** **Proposed**

### `DQ-06`: Inconsistent Capitalization (Field: `status`)
* **Severity Level:** **Medium** | **Records Impacted:** 39 rows
* **Detection SQL / Logic:** `status != INITCAP(status) AND status != UPPER(status)`
* **Likely Root Cause:** Mixed client implementations (cOmPLeTeD vs Completed) without canonicalization.
* **Recommended Data Correction:** Apply UPPER() or INITCAP() standard during dbt/SQL transformation layer.
* **Permanent Preventative Control:** Normalize string formatting at API ingestion middleware before database insert.
* **Responsible Team:** Analytics Eng | **Status:** **Proposed**

### `DQ-07`: Trailing / Leading Whitespace (Field: `status, transaction_type`)
* **Severity Level:** **Low** | **Records Impacted:** 39 rows
* **Detection SQL / Logic:** `LEN(status) != LEN(TRIM(status))`
* **Likely Root Cause:** Unsanitized string concatenation in client SDK or CSV export utility.
* **Recommended Data Correction:** Apply TRIM() cleansing in transformation staging models.
* **Permanent Preventative Control:** Pydantic / input validation middleware stripping whitespace on string fields.
* **Responsible Team:** Analytics Eng | **Status:** **Proposed**

### `DQ-08`: Invalid Numeric Format (String in Decimal) (Field: `amount`)
* **Severity Level:** **Critical** | **Records Impacted:** 39 rows
* **Detection SQL / Logic:** `TRY_CAST(amount AS DECIMAL) IS NULL (e.g., 'ONE_HUNDRED')`
* **Likely Root Cause:** Corrupted form input or unvalidated JSON string field passed to decimal column.
* **Recommended Data Correction:** Discard non-numeric record or lookup mapped numerical value in translation table.
* **Permanent Preventative Control:** Strict JSON schema validation: amount MUST be numeric type, not string.
* **Responsible Team:** Backend Gateway Team | **Status:** **Proposed**

### `DQ-09`: Illegal Negative Value (Field: `amount`)
* **Severity Level:** **Critical** | **Records Impacted:** 39 rows
* **Detection SQL / Logic:** `amount < 0.00 WHERE transaction_type IN ('REWARD_CREDIT', 'DAILY_BONUS_CREDIT')`
* **Likely Root Cause:** Incorrect debit sign applied to credit transaction; legacy accounting bug.
* **Recommended Data Correction:** Flip sign to positive if direction is CREDIT, or reclassify as REWARD_REVERSAL.
* **Permanent Preventative Control:** Add database CHECK constraint: amount > 0.00; direction dictates debit/credit.
* **Responsible Team:** Lead Data Architect | **Status:** **Proposed**

### `DQ-010`: Unexpected Null Foreign Key (Field: `user_id`)
* **Severity Level:** **Critical** | **Records Impacted:** 39 rows
* **Detection SQL / Logic:** `user_id IS NULL on transactional row`
* **Likely Root Cause:** Unauthenticated guest user action erroneously logged to transaction pipeline.
* **Recommended Data Correction:** Quarantine row in orphan review table; investigate guest session token.
* **Permanent Preventative Control:** Enforce NOT NULL constraint on user_id across all transactional tables.
* **Responsible Team:** Lead Data Architect | **Status:** **Proposed**

### `DQ-011`: Orphan Record (Missing Parent Entity) (Field: `user_id`)
* **Severity Level:** **Critical** | **Records Impacted:** 39 rows
* **Detection SQL / Logic:** `user_id NOT IN (SELECT user_id FROM dim_users)`
* **Likely Root Cause:** Out-of-order event ingestion where transaction arrived before user creation committed.
* **Recommended Data Correction:** Buffer events in staging table until parent user_id is materialized.
* **Permanent Preventative Control:** Enforce relational FOREIGN KEY constraint with transactional event ordering.
* **Responsible Team:** Data Platform Eng | **Status:** **Proposed**

### `DQ-012`: Duplicate Event Payload (Replay Attack) (Field: `issue_record_id`)
* **Severity Level:** **High** | **Records Impacted:** 39 rows
* **Detection SQL / Logic:** `Duplicate payload hash or identical event_id within 5-minute window`
* **Likely Root Cause:** Mobile client retry loop on slow cellular connection.
* **Recommended Data Correction:** Deduplicate using event_id; record idempotency hit in monitoring logs.
* **Permanent Preventative Control:** API gateway Redis deduplication filter with 10-minute TTL per event_id.
* **Responsible Team:** Platform Eng | **Status:** **Proposed**

### `DQ-013`: Inconsistent Naming Convention (Field: `transaction_type`)
* **Severity Level:** **Medium** | **Records Impacted:** 39 rows
* **Detection SQL / Logic:** `transaction_type NOT IN approved SCREAMING_SNAKE_CASE enum`
* **Likely Root Cause:** Non-standardized ad-hoc logging added by feature developer without taxonomy review.
* **Recommended Data Correction:** Mapping dictionary in transformation layer translating legacy slugs to standard.
* **Permanent Preventative Control:** Data dictionary linter in CI/CD pipeline blocking unapproved event names.
* **Responsible Team:** Data Governance Lead | **Status:** **Proposed**

### `DQ-014`: Impossible State Transition (Field: `status`)
* **Severity Level:** **Critical** | **Records Impacted:** 39 rows
* **Detection SQL / Logic:** `Direct skip from Requested to Refunded without passing through Processing/Rejected`
* **Likely Root Cause:** Race condition or unhandled edge case in payment gateway callback handler.
* **Recommended Data Correction:** Reconcile payment gateway logs manually and correct state to Rejected.
* **Permanent Preventative Control:** State machine validation pattern in application code rejecting illegal transitions.
* **Responsible Team:** Backend Core Team | **Status:** **Proposed**

---
*End of Deliverable DELIV-13 — Data Quality Defect Audit Report.*
