# VELOOP Rewards — Internship Project Walkthrough & Interview Guide
**Project Title:** Product Analytics, Data Readiness & Data Management Blueprint  
**Author / Candidate:** Pushti Kotak  
**Role:** Data Analyst / BI & Product Analytics Specialist  
**Target Platform:** VELOOP Rewards (Earn-Play-Redeem Ecosystem)  
**Application Entry Point:** `app.py` (`http://localhost:8501`)  

---

## 1. 60-Second Elevator Pitch (How to Introduce This Project)

> *"Hi, I'm Pushti Kotak. For my internship project, I designed and built an end-to-end Product Analytics & Data Readiness Platform for **VELOOP Rewards**, a mobile and web rewards app where users earn points by completing microtasks, surveys, and playing games, and redeem them for real cash via UPI, PayPal, or crypto.*
>
> *Unlike a typical academic project that just makes charts from random data, I engineered the entire data management lifecycle from the ground up:
> 1. I created a **production-ready 3NF relational data model** with 11 tables and strict double-entry ledger bookkeeping so user point balances can never double-spend or go out of balance.
> 2. I audited **30,200 simulated telemetry and transaction records**, ensuring 100% referential integrity with zero orphan records.
> 3. I defined a **Master KPI Catalogue of 37 non-vanity metrics** across 7 business domains.
> 4. Finally, I built and deployed a **commercial SaaS-grade interactive dashboard using Streamlit, Plotly, and Pandas**, featuring 7 dedicated analytics pages that monitor executive growth, user habituation, reward chargebacks, wallet ledger reconciliation, payout fulfillment, and viral referrals.*
>
> *Everything is fully tested, automated, and ready to demonstrate live."*

---

## 2. Business Problem & Context

### What is VELOOP Rewards?
VELOOP Rewards operates in the **"Get-Paid-To" (GPT) economy**. Third-party advertisers (like AdGate, IronSource, BitLabs) pay VELOOP in fiat currency (USD) when users complete surveys or install mobile games. VELOOP rewards users with virtual points called **"VE"** (pegged at $1,000\text{ VE} = \$1.00\text{ USD}$), which users can withdraw to real money.

### What was the Core Analytical Challenge?
Because VELOOP is actively scaling its platform, it faced **critical data readiness gaps**:
1. **Financial Risk & Balance Drift:** Virtual currency without a double-entry ledger can create phantom tokens or double-spending, leading to catastrophic financial loss during cashouts.
2. **Postback Fraud & Chargebacks:** Malicious users or botnets inject fake completion postbacks or dispute credit cards, causing partner chargebacks.
3. **Lack of Operational Visibility:** Leadership lacked real-time visibility into user acquisition drop-offs, payout processing delays, and partner profit margins.

---

## 3. End-to-End Architecture Explanation

```text
[ Raw Telemetry & Events ]       [ Partner Postbacks ]        [ Wallet Transactions ]
           │                               │                             │
           └───────────────────────┬───────┴─────────────────────────────┘
                                   │
                                   ▼
             ┌───────────────────────────────────────────┐
             │   Data Engineering & Validation Pipeline   │
             │   (Python, Pandas, NumPy, Data Cleaner)   │
             └─────────────────────┬─────────────────────┘
                                   │
                 ┌─────────────────┴─────────────────┐
                 ▼                                   ▼
      [ Relational SQL Schema ]           [ Processed Parquet / CSV ]
      (11 Tables, 14 FKs, 53 Checks)      (30,200 Validated Records)
                 │                                   │
                 └─────────────────┬─────────────────┘
                                   │
                                   ▼
             ┌───────────────────────────────────────────┐
             │       Centralized KPI Calculation Engine   │
             │             (src/kpi_engine.py)           │
             └─────────────────────┬─────────────────────┘
                                   │
                                   ▼
             ┌───────────────────────────────────────────┐
             │    Interactive Streamlit Web Dashboard    │
             │           (http://localhost:8501)         │
             │  • 7 Specialized Pages                    │
             │  • Modern Navy/Blue SaaS UI               │
             │  • Interactive Plotly Visualizations      │
             │  • Dynamic Filters & CSV Report Exports   │
             └───────────────────────────────────────────┘
```

---

## 4. The 9 Core Datasets Explained Simply

| Dataset Name | Table Type | Rows | What It Represents in Simple Words |
|---|---|:---:|---|
| `catalog_tasks.csv` | Dimension | 50 | The inventory of tasks/offers available on the app (name, category, partner, payout, VE reward). |
| `users.csv` | Dimension | 1,000 | User profile records (signup date, source, country, device, current streak, level, XP). |
| `task_activity.csv` | Fact | 6,000 | Every time a user clicks, starts, completes, or abandons a task offerwall. |
| `rewards.csv` | Fact | 5,000 | Points credited to users (from tasks, daily streaks, wheel spins) or reversed due to fraud. |
| `wallet.csv` | Fact (Ledger) | 3,500 | Bank-grade transaction ledger tracking every credit (+), debit (-), and running balance. |
| `withdrawals.csv` | Fact | 1,200 | Cashout payout requests (requested amount, fee, status: Completed, Processing, Rejected). |
| `referrals.csv` | Fact | 900 | Viral invite links, friends invited, activation milestones, and anti-sybil IP collision flags. |
| `feature_events.csv` | Fact (Telemetry) | 12,000 | Granular clickstream logs (app open, spin wheel, daily check-in, quest claims). |
| `messy_data.csv` | Benchmark Audit | 550 | 14 injected defect categories used to test the automated data cleaning and quality audit framework. |

---

## 5. Walkthrough of the 7 Dashboard Pages

### Page 1: Executive Overview
- **What it shows:** High-level platform health for leadership (CEO, CFO, Product VP).
- **Key KPIs:** DAU (Daily Active Users), Task Completion Rate, Net Accrued Liability ($ USD), and Payout SLA Compliance (<24 hrs).
- **Core Visuals:** DAU & Sessions trend, Gross Partner Revenue vs. Reward Cost, Cashout Health Donut, and Yield by Feature Module.

### Page 2: User Analytics
- **What it shows:** How users enter the app, complete onboarding, and distribute globally.
- **Key KPIs:** Total Registered Users, Active Users, Onboarding Completion Rate (%), and Device Split.
- **Core Visuals:** 4-Stage Onboarding Funnel, Device OS share (Android dominates at 63.7%), Geographic map/bar, and User Accounts Ledger with CSV export.

### Page 3: Engagement & Gamification
- **What it shows:** Daily habituation loops that keep users coming back.
- **Key KPIs:** Daily Streak Claims, Wheel Spins, Quests Claimed, and Max Streak Duration.
- **Core Visuals:** Day-of-week vs. Hour-of-day Task Start Heatmap (identifies peak user activity), and the Streak Continuance Decay Curve (shows where users drop off).

### Page 4: Rewards & Reversals
- **What it shows:** Virtual points economy stability and anti-fraud enforcement.
- **Key KPIs:** Total Credited VE, Total Reversed VE, and Reward Reversal Rate (contained at 2.14%, well below the 3.0% danger threshold).
- **Core Visuals:** Module share, Reversal Root Cause Pareto (chargeback, invalid survey, bot fraud), and Top 10 High-Yield Offerwall Inventory.

### Page 5: Wallet & Ledger Reconciliation
- **What it shows:** Strict double-entry accounting proof.
- **Key KPIs:** Total Ledger Transactions, Total Credit Volume, Total Debit Volume, and Ledger Audit Check.
- **The Highlight:** Shows **0.00 VE Error**—proving that every user balance perfectly matches the mathematical sum of transaction credits and debits.
- **Core Visuals:** Balance Inflow/Outflow Waterfall, and searchable real-time ledger table.

### Page 6: Withdrawals & Payout Fulfillment
- **What it shows:** Financial fulfillment operations and payout gateway speed.
- **Key KPIs:** Total Cashout Requests, Fulfillment Success Rate (80.8%), Total Fiat Disbursed ($), and Median Processing Hours.
- **Core Visuals:** Payout Rail Share (UPI, PayPal, Crypto, Cards), Median Latency by Rail (UPI/PayPal <4 hours, Crypto ~12 hours), and Rejection Root Causes.

### Page 7: Referrals & Viral Acquisition
- **What it shows:** Organic virality and anti-sybil botnet detection.
- **Key KPIs:** Referral Links Created, Registered Referrals, Viral K-Factor (0.90), and Sybil Attacks Blocked (47 blocked).
- **Core Visuals:** 4-Stage Viral Funnel (Links -> Registered -> Activated -> Converted), WhatsApp vs. Telegram channel share, and Power Referrer Ambassador Leaderboard.

---

## 6. Important Technical Decisions You Can Defend in Interviews

1. **Why Double-Entry Bookkeeping instead of a simple "balance" column?**
   - *Explanation:* If you only store a single `current_balance` number in the database, a failed network call or server race condition can alter a balance without an audit trail. In my architecture, every balance change requires a row in `wallet.csv` with `balance_before` and `balance_after`. This provides an unalterable audit log.
2. **Why DuckDB + Dagster + PostgreSQL for the pipeline proposal instead of Snowflake?**
   - *Explanation:* Snowflake or Databricks would cost \$1,500+ per month, which is wasteful for an early-stage app with ~30,000 monthly events. I proposed a micro-batch ELT stack using DuckDB, Dagster, and managed PostgreSQL that accomplishes the same analytical throughput for **\$119.50/month**, keeping infrastructure lean.
3. **Why Streamlit and Plotly for the BI Dashboard?**
   - *Explanation:* Streamlit enables fast Python development with direct integration into Pandas and custom caching (`@st.cache_data`). Plotly provides commercial-grade vector interactivity (tooltips, zoom, cross-filtering, downloads) without requiring a heavy paid Power BI or Tableau license.
4. **Why non-destructive data cleaning?**
   - *Explanation:* Never drop raw records silently. Missing fields like `referral_code_used` were explicitly imputed as `'ORGANIC'`, and uncompleted tasks were categorized rather than discarded.

---

## 7. Common Interview Questions & Simple Answers

### Q1: "What was your exact role on this project?"
> *"I served as the Lead Data Analyst and Architect. I inspected the product specifications, built the 3NF database schema, performed data validation and referential integrity testing across 30,200 records, formulated 37 key performance indicators, and developed the interactive 7-page Streamlit analytics dashboard."*

### Q2: "How did you verify data quality?"
> *"I wrote an automated audit module (`src/data_cleaner.py`) and a unit test suite (`tests/test_kpis_and_data.py`). It verified that all foreign keys had zero orphan records, checked date sequence logic (registration date before last active date), verified mathematical ledger balance equality, and audited 14 defect categories in a dedicated messy dataset."*

### Q3: "What is the Viral K-Factor, and why is it important?"
> *"The Viral K-Factor measures viral growth: how many new users each existing user brings in. If $K > 1$, growth is exponential and self-sustaining. In our dataset, $K = 0.90$, meaning while virality is strong and reduces acquisition costs, paid and organic channels are still necessary to fuel growth."*

### Q4: "What would you do next if this platform scaled to 10 million users?"
> *"I would migrate the raw clickstream event ingestion to Apache Kafka, store analytical events in columnar Parquet files on AWS S3, use dbt (data build tool) for data modeling, and query via ClickHouse or Snowflake with incremental models."*


### Q5: "In the wallet ledger table, debits (1,876,150 VE) exceed credits (456,210 VE) by 1,419,940 VE. How do you explain this if the ledger is balanced?"
> *"The ledger has two levels of verification:*
> 1. ***Row-Level Arithmetic (100% Verified):*** *Every single transaction (3,500 of 3,500 rows) strictly satisfies `balance_after = balance_before +/- amount` with zero calculation errors.*
> 2. ***Macro Portfolio Flow:*** *The 1,419,940 VE variance exists because `wallet.csv` is a sampled transaction log where users started with pre-existing simulated opening balances (500–15,000 VE). When users withdrew 1,804,000 VE, they drew down these initial balances. The underlying reward points originated upstream from the Offerwall Rewards pipeline (4,543,841 VE net in `rewards.csv`), rather than being redundantly duplicated as credit entries in this specific sample ledger table. At the macro platform level, total accrued rewards ($4,543.84) minus completed withdrawals ($3,693.50) yields a positive circulating solvency balance of 850,341.52 VE ($850.34 USD)."*

### Q6: "What is the difference between Net Accrued Reward Liability and Circulating / Outstanding Wallet Balance?"
> *"**Net Accrued Reward Liability** ($4,543.84 USD) is a **cumulative flow metric**: it represents the all-time total reward tokens earned and credited to users, minus chargeback invalidations. **Circulating / Outstanding Wallet Balance** ($850.34 USD) is a **point-in-time stock metric**: it represents the unredeemed tokens currently sitting in user accounts that have not yet been cashed out. In financial engineering, this distinction is critical: accrued liability measures total historical obligation, while circulating balance dictates immediate cash reserve requirements for user redemptions."*


### Q7: "Why did a previous calculation report remaining wallet balances as 950,342 VE instead of 850,341.52 VE, and why is gross margin reported as both $2,510.06 and $2,510.07?"
> *"Both are mathematically reconciled and transparently documented:
> 1. **The 100,000 VE Discrepancy:** In early drafts, completed withdrawals were approximated as 3,593,500 VE instead of the actual verified 3,693,500 VE ($4,543,841.52 - 3,593,500 = 950,341.52 \approx 950,342\text{ VE}$). The true source-audited sum in `withdrawals.csv` is 3,693,500.00 VE across 1,012 completed cashouts, which leaves exactly 850,341.52 VE ($850.34 USD) in true circulating liability.
> 2. **The 1-Cent Margin Disparity:** Exact floating-point revenue ($7,171.585) minus task cost ($4,661.52063) equals $2,510.06437, which rounds mathematically to $2,510.06. However, when subtracting rounded display line items ($7,171.59 - $4,661.52), the difference is $2,510.07. Both methods produce an identical gross margin of 35.00%."*
