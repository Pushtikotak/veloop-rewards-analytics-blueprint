## 🚀 Live Dashboard

**Explore the interactive VELOOP Rewards Analytics Dashboard:**

[Open Live Dashboard](https://veloop-rewards-analytics-blueprint-uzuo4gyrzccnznudiuekqs.streamlit.app/)

**Platform:** Streamlit Community Cloud

---
# VELOOP Rewards — Product Analytics, Data Readiness & Data Management Blueprint
### End-to-End Enterprise Deliverable & Interactive Analytics Platform
**Author / Lead Data Analyst:** Pushti Kotak  
**Project Role:** Senior Data Analyst, Data Architect & BI Developer  
**Status:** 100% Complete, Validated, Tested & Live Application Running  
**Local Application URL:** [`http://localhost:8501`](http://localhost:8501)  
**Walkthrough & Interview Guide:** [`INTERNSHIP_PROJECT_EXPLANATION.md`](INTERNSHIP_PROJECT_EXPLANATION.md)  

---

```
+-----------------------------------------------------------------------------------------+
| MANDATORY GOVERNANCE & DATA INTEGRITY NOTICE:                                           |
| In strict compliance with Section 2, 6, 29, 30, and 34 of the Task Specification:       |
| VELOOP Rewards is an active commercial product under development. All datasets,         |
| empirical profiling results, and numerical figures in this repository are:             |
| "SIMULATED DATA — CREATED FOR ANALYTICAL TESTING"                                       |
| They do NOT represent actual VELOOP production statistics, company earnings, or users.  |
| Product facts and technical proposals are classified as Confirmed, Proposed, or Verified|
+-----------------------------------------------------------------------------------------+
```

---

## 🚀 Live Interactive Dashboard (Streamlit & Plotly)

A fully operational, commercial SaaS-grade Product Analytics Dashboard is integrated and actively running locally:

```bash
# Launch the dashboard locally
streamlit run app.py
```
* **Dashboard URL:** `http://localhost:8501`
* **Features:** 7 dedicated pages, modern light theme with navy/blue accents, interactive Plotly charts, global device & date-range filters, and CSV report export buttons.

### The 7 Specialized Dashboard Pages:
1. **Executive Overview:** High-level platform health, DAU/MAU stickiness, revenue vs. reward liability split, and cashout fulfillment health.
2. **User Analytics:** 4-stage acquisition and onboarding progression, geographic distribution, device OS split, and searchable user ledger.
3. **Engagement & Gamification:** Daily habituation loops (Streaks, Wheel Spins, Quests), day/hour task activity heatmap, and streak decay curve.
4. **Rewards & Reversals:** Virtual points economy stability, partner chargeback rates (<2.14%), reversal root-cause taxonomy, and top 10 offerwall inventory.
5. **Wallet & Ledger Reconciliation:** 100% row-level arithmetic integrity (**0.00 VE Error** across 3,500 transactions) and macro accounting flow analysis (-1.42M VE drawdown on unrecorded initial balances).
6. **Withdrawals & Payout Fulfillment:** Fulfillment queue health, success rate (80.8%), fiat disbursed ($), and median processing time by rail (<4h for UPI/PayPal).
7. **Referrals & Viral Acquisition:** 4-stage viral funnel, K-factor virality ratio (0.90), social share channels, anti-sybil IP collision defense, and power referrer leaderboard.

---

## 🛠️ Automated Testing & Quality Assurance

The codebase includes an enterprise-grade automated test suite verifying data loading, referential integrity, boundary conditions, and financial reconciliation:

```bash
# 1. Run the 16 unit tests
python -m unittest tests/test_kpis_and_data.py

# 2. Run the 29-view automated dashboard interaction test suite
python scripts/test_dashboard_full_suite.py

# 3. Run the independent financial & ledger audit script
python scripts/audit_financials_and_ledger.py
```
```text
................
----------------------------------------------------------------------
Ran 16 tests in 0.447s

OK (100% Tests Passing)

AppTest PASSED: All 29 view states verified successfully with 0 exceptions!
```

---

## 📁 Repository Structure

```text
Product Analytics, Data Readiness & Data Management Blueprint/
├── README.md                               # Master project index & navigation guide
├── INTERNSHIP_PROJECT_EXPLANATION.md       # Candidate interview guide, Q&A & elevator pitch
├── app.py                                  # Live Streamlit Product Analytics Web Application
├── requirements.txt                        # Pinned dependencies (Pandas, Plotly, Streamlit, OpenPyXL)
├── .gitignore                              # Clean Git ignore rules (OS, Python, IDE artifacts)
├── .streamlit/config.toml                  # Streamlit SaaS theme & server settings
├── Data_Analyst_01.pdf                     # Primary official task specification (44 pages)
├── Pushti VELOOP_Rewards_GPT_Industry_Research.pdf # Verified competitor benchmark study
│
├── src/                                    # Reusable Data Engineering & BI Modules
│   ├── data_loader.py                      # Robust data ingestion with datetime parsing
│   ├── data_cleaner.py                     # Data validation & clean dataset generation
│   ├── kpi_engine.py                       # Centralized logic for all 37 production KPIs
│   └── ui_components.py                    # Plotly chart builders, KPI cards, and export utilities
│
├── tests/                                  # Automated Quality Assurance Suite
│   ├── __init__.py
│   └── test_kpis_and_data.py               # 16 automated unit tests (100% passing)
│
├── data/                                   # Datasets (30,200 Total Records)
│   ├── raw/                                # 8 operational CSVs + 1 messy defect CSV
│   └── processed/                          # 9 standardized, validated, and cleaned CSVs
│
├── dashboards/                             # BI Specifications & Wireframes
│   ├── dashboard_specs.md                  # DELIV-15 (10-part specs for 7 dashboards)
│   ├── dax_measures.dax                    # 30 production Power BI DAX formulas
│   └── wireframes/                         # 7 vector SVG wireframes (100% valid XML)
│
├── docs/                                   # 21 Formal Deliverables & Reports
│   ├── 01_Executive_Summary.md             # DELIV-01 (Executive strategic briefing)
│   ├── 02_Product_Data_Readiness_Audit.md  # DELIV-02 (12 modules & 12 critical gaps)
│   ├── 03_Data_Coverage_Matrix.md          # DELIV-03 (30-row operational matrix)
│   ├── 04_User_Account_Analytics_Spec.md   # DELIV-04 (4-tier ID hierarchy & lifecycle machine)
│   ├── 05_Earning_Reward_Analytics_Spec.md # DELIV-05 (Task lifecycle & HMAC postbacks)
│   ├── 06_Wallet_Withdrawal_Analytics_Spec.md # DELIV-06 (Double-entry ledger & cashouts)
│   ├── 07_Referral_Engagement_Spec.md      # DELIV-07 (4-stage viral funnel & anti-sybil)
│   ├── 08_Event_Tracking_Plan.md           # DELIV-08 (38 production events)
│   ├── 09_Data_Dictionary.md               # DELIV-09 (100 fields across 8 entities)
│   ├── 11_KPI_Catalogue.md                 # DELIV-11 (37 production metrics with SQL)
│   ├── 12_Simulated_Data_Profiling.md      # DELIV-12 (Profiling of ~30k synthetic rows)
│   ├── 13_Data_Quality_Audit.md            # DELIV-13 (Messy_Data defect audit)
│   ├── 14_Data_Quality_Control_Framework.md# DELIV-14 (6-stage prevention framework)
│   ├── 16_Developer_Analytics_Handoff.md   # DELIV-16 (TypeScript SDK & Jest tests)
│   ├── 17_Data_Pipeline_Operating_Model.md # DELIV-17 (Micro-batch ELT under $120/mo)
│   ├── 18_Privacy_Governance_Proposal.md   # DELIV-18 (DPDP Act, GDPR, 5-role RBAC)
│   ├── 19_Analytics_Change_Management.md   # DELIV-19 (SemVer 2.0 schema evolution)
│   ├── 20_Analytics_Gap_Assessment.md      # DELIV-20 (Readiness scorecard & 18 epics)
│   ├── 21_Final_Consolidated_Blueprint.md  # DELIV-21 (Capstone master reference)
│   ├── DASHBOARD_USER_GUIDE.md             # Complete dashboard navigation guide
│   ├── DATA_VALIDATION_REPORT.md           # Empirical data validation findings
│   └── TESTING_REPORT.md                   # Full QA test execution documentation
│
├── models/                                 # Relational Database Architecture
│   ├── README.md                           # DELIV-10 (Schema architecture narrative)
│   ├── logical_data_model.mermaid          # Mermaid ER diagram (11 core entities)
│   └── schema_ddl.sql                      # PostgreSQL DDL (11 tables, 14 FKs, 53 checks)
│
├── scripts/                                # Automation & Verification Suite
│   ├── generate_simulated_data.py          # Data generation with seed 42
│   ├── profile_simulated_data.py           # Automated profiling & summary tables
│   ├── audit_data_quality.py               # 14 defect categories analysis
│   ├── build_workbooks_phase1.py           # Excel workbooks builder
│   ├── build_tracking_and_dictionary.py    # Dictionary & tracking plan workbooks
│   ├── build_kpi_catalogue.py              # 37-KPI Excel workbook
│   ├── build_dashboard_blueprint.py        # SVG wireframe compiler
│   ├── build_backlog.py                    # Backlog & register workbooks
│   ├── verify_artifacts.py                 # Artifacts syntax & schema validator
│   ├── verify_links.py                     # Relative link validator (0 broken links)
│   ├── generate_verification_evidence.py   # Master verification engine
│   ├── security_hygiene_check.py           # Secret & credential scanner
│   ├── test_dashboard_full_suite.py        # 29-view AppTest dashboard automation
│   ├── test_dashboard_integrity.py         # Empirical source data reconciliation
│   └── audit_financials_and_ledger.py      # Independent financial & ledger auditor
│
└── workbooks/                              # 10 Professional Multi-Sheet Excel Files
    ├── DELIV-03_Data_Coverage_Matrix.xlsx
    ├── DELIV-08_Event_Tracking_Plan.xlsx
    ├── DELIV-09_Data_Dictionary.xlsx
    ├── DELIV-11_KPI_Catalogue.xlsx
    ├── DELIV-12_Simulated_Data_Profiling.xlsx
    ├── DELIV-13_Data_Quality_Audit.xlsx
    ├── DELIV-19_Assumption_Verification_Register.xlsx
    ├── DELIV-20_Implementation_Backlog.xlsx
    ├── DELIV-21_Assumption_Verification_Register.xlsx
    └── DELIV-22_Implementation_Backlog.xlsx
```

---

## 📊 Summary of the 21 Section 27 Deliverables

| Deliverable Code & Name | Primary Markdown Specification | Accompanying Production Artifact | Status |
|---|---|---|:---:|
| **DELIV-01:** Executive Summary | `docs/01_Executive_Summary.md` | Strategic Capstone Briefing | **PASS** |
| **DELIV-02:** Data Readiness Audit | `docs/02_Product_Data_Readiness_Audit.md` | 12 Product Modules & Gaps | **PASS** |
| **DELIV-03:** Data Coverage Matrix | `docs/03_Data_Coverage_Matrix.md` | `workbooks/DELIV-03_Data_Coverage_Matrix.xlsx` | **PASS** |
| **DELIV-04:** User Analytics Spec | `docs/04_User_Account_Analytics_Spec.md` | 4-Tier ID Resolution Model | **PASS** |
| **DELIV-05:** Earning Analytics Spec | `docs/05_Earning_Reward_Analytics_Spec.md` | Task Lifecycle & HMAC Verification | **PASS** |
| **DELIV-06:** Wallet & Ledger Spec | `docs/06_Wallet_Withdrawal_Analytics_Spec.md` | Row-Level Integrity & Flow Analysis | **PASS** |
| **DELIV-07:** Referral & Funnel Spec | `docs/07_Referral_Engagement_Spec.md` | 4-Stage Viral Funnel & Anti-Sybil | **PASS** |
| **DELIV-08:** Event Tracking Plan | `docs/08_Event_Tracking_Plan.md` | `workbooks/DELIV-08_Event_Tracking_Plan.xlsx` (38 Events) | **PASS** |
| **DELIV-09:** Data Dictionary | `docs/09_Data_Dictionary.md` | `workbooks/DELIV-09_Data_Dictionary.xlsx` (100 Fields) | **PASS** |
| **DELIV-10:** Logical Data Model | `models/README.md` | `models/schema_ddl.sql` & `logical_data_model.mermaid` | **PASS** |
| **DELIV-11:** KPI Catalogue | `docs/11_KPI_Catalogue.md` | `workbooks/DELIV-11_KPI_Catalogue.xlsx` (37 KPIs) | **PASS** |
| **DELIV-12:** Data Profiling Report | `docs/12_Simulated_Data_Profiling.md` | `workbooks/DELIV-12_Simulated_Data_Profiling.xlsx` | **PASS** |
| **DELIV-13:** Data Quality Audit | `docs/13_Data_Quality_Audit.md` | `workbooks/DELIV-13_Data_Quality_Audit.xlsx` | **PASS** |
| **DELIV-14:** Quality Control Framework | `docs/14_Data_Quality_Control_Framework.md` | 6-Stage Prevention & Great Expectations | **PASS** |
| **DELIV-15:** Dashboard Blueprint & App | `dashboards/dashboard_specs.md` | **Live Web App (`app.py`)** & 7 SVG Wireframes | **PASS** |
| **DELIV-16:** Developer Handoff Guide | `docs/16_Developer_Analytics_Handoff.md` | TypeScript SDK Interfaces & Jest Tests | **PASS** |
| **DELIV-17:** Data Pipeline Proposal | `docs/17_Data_Pipeline_Operating_Model.md` | Micro-batch ELT Architecture ($119.50/mo) | **PASS** |
| **DELIV-18:** Privacy & Governance | `docs/18_Privacy_Governance_Proposal.md` | DPDP Act 2023, GDPR, 5-Role RBAC | **PASS** |
| **DELIV-19:** Change Management | `docs/19_Analytics_Change_Management.md` | SemVer 2.0 Schema Evolution Governance | **PASS** |
| **DELIV-20:** Gap Assessment & Backlog | `docs/20_Analytics_Gap_Assessment.md` | `workbooks/DELIV-20_Implementation_Backlog.xlsx` | **PASS** |
| **DELIV-21:** Consolidated Blueprint | `docs/21_Final_Consolidated_Blueprint.md` | Master Capstone Synthesis Reference | **PASS** |

---

## 🔒 Security, Hygiene & Privacy Assurance

- **Zero Credentials:** Verified 0 hardcoded passwords, API keys, private keys, or AWS tokens via `scripts/security_hygiene_check.py`.
- **Zero Temporary Junk:** Clean repository free of `.pyc`, `__pycache__`, `.tmp`, or OS artifacts.
- **Privacy Compliant:** Contains zero sensitive personal information, phone numbers, or academic enrollment numbers. Only author attribution for **Pushti Kotak** is included.
