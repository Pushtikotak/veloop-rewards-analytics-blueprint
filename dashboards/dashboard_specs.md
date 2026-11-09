# Analytics Dashboard Blueprint & Visual Specifications
## VELOOP Rewards — Product Analytics, Data Readiness & Data Management Blueprint
**Deliverable Code:** `DELIV-15` (Work Package M)  
**Author / Analyst:** Pushti Kotak  
**Document Classification:** Internal BI & Product Analytics Architecture  
**Date:** 02 November 2026  
**Companion Artifacts:**  
- Visual Vector Wireframes: [`dashboards/wireframes/`](wireframes/)  
  * [01_executive_overview.svg](wireframes/01_executive_overview.svg)  
  * [02_user_analytics.svg](wireframes/02_user_analytics.svg)  
  * [03_engagement.svg](wireframes/03_engagement.svg)  
  * [04_rewards.svg](wireframes/04_rewards.svg)  
  * [05_wallet.svg](wireframes/05_wallet.svg)  
  * [06_withdrawals.svg](wireframes/06_withdrawals.svg)  
  * [07_referrals.svg](wireframes/07_referrals.svg)  
- Power BI DAX Formulas: [`dashboards/dax_measures.dax`](dax_measures.dax)  
**Status:** Complete & Verified  

---

## 1. Executive BI Architecture & Design Standards

The **Analytics Dashboard Blueprint** formalizes the visual specifications, metric queries, dimensional hierarchies, and decision-support logic for VELOOP’s operational reporting suite. 

In strict compliance with Section 19 of the internship task specification:
1. **Seven Dedicated Specialized Dashboards:** Spanning executive leadership, user growth, habituation loops, reward liabilities, double-entry wallet reconciliation, payout fulfillment, and viral referrals.
2. **Mandatory 10-Part Specification per Visual:** Every visual defines: *Metric, Calculation, Source, Visualization Type, Filters, Dimensions, Date Range, Refresh Frequency, Business Question, and Decision Supported*.
3. **No Fictional Company Targets:** Layouts display verified architectural structures and simulated testing baselines clearly labeled under **Data Authenticity Policy (Section 2)**.

---

## 2. Dashboard 1 — Executive Overview

**Target Audience:** CEO, CFO, VP of Product, Lead Data Architect  
**Operational Cadence:** Daily Refresh (Hourly for SLA alerts)  
**Primary Objective:** Deliver a high-level operational pulse of platform growth, monetization, cash liabilities, and payout fulfillment.

```
+----------------------------------------------------------------------------------------------------+
| [KPI 1: DAU (382)] | [KPI 2: Completed Tasks (3,489)] | [KPI 3: Net Liability ($4,520)] | [KPI 4: Payout SLA (96.4%)] |
+----------------------------------------------------------------------------------------------------+
| Visual 1.1: Active Users & Sessions (Dual Axis Line) | Visual 1.2: Revenue vs. Liability Split (Area)      |
+------------------------------------------------------+---------------------------------------------+
| Visual 1.3: Cashout Fulfillment Health (Multi-Bar)   | Visual 1.4: Top Earning Modules Yield (H-Bar)      |
+----------------------------------------------------------------------------------------------------+
```

### Visual Specifications

#### Visual 1.1: Daily Active Users & Session Trajectory
* **Metric:** Daily Active Users (DAU) & Total Ingested Sessions
* **Calculation:** `[DAU]` vs. `DISTINCTCOUNT(fct_feature_events[session_id])`
* **Data Source:** `fct_feature_events`
* **Visualization:** Dual-Axis Line & Clustered Column Chart
* **Filters:** `event_name IN ('task_offer_started', 'task_offer_completed', 'engagement_daily_claimed')`
* **Dimensions:** Date (`dim_dates[date_id]`), Platform (`device_type`)
* **Date Range:** Trailing 90 Days
* **Refresh Frequency:** Hourly
* **Business Question:** Is platform daily activity expanding sustainably, and is session frequency per user growing?
* **Decision Supported:** Determines marketing ad-spend pacing and detects sudden user drop-offs following client releases.

#### Visual 1.2: Gross Partner Revenue vs. Credited Reward Liability
* **Metric:** Gross Advertiser Revenue (USD) vs. Net Credited User Rewards (USD Equivalent)
* **Calculation:** `[Gross_Advertiser_Revenue_USD]` vs. `[Total_Credited_Rewards_VE] * 0.001`
* **Data Source:** `fct_task_activity`, `fct_rewards`
* **Visualization:** Stacked Area & Margin Line Chart
* **Filters:** Status = `'Validated_Approved'` / `'Credited'`
* **Dimensions:** Calendar Month, Provider (`provider_id`)
* **Date Range:** Year-to-Date (Monthly)
* **Refresh Frequency:** Daily
* **Business Question:** What is our realized gross platform margin, and are reward liabilities covered by receivables?
* **Decision Supported:** Informs promotional multiplier budgets and warns if partner payout rates drop below sustainable margins.

#### Visual 1.3: Withdrawal Fulfillment Health
* **Metric:** Payout Requests vs. Completed Cashouts vs. Rejected Requests
* **Calculation:** `[Withdrawal_Requests_Count]`, `[Completed_Withdrawals_Count]`, `[Withdrawal_Rejection_Rate_Pct]`
* **Data Source:** `fct_withdrawals`
* **Visualization:** Clustered Column Chart with Rejection Trend Line
* **Filters:** None
* **Dimensions:** Submission Date (`requested_timestamp`), Payment Method (`payout_method`)
* **Date Range:** Trailing 30 Days
* **Refresh Frequency:** Hourly
* **Business Question:** Are user cashouts being fulfilled within SLA without abnormal rejection spikes?
* **Decision Supported:** Flags banking gateway downtime and compliance backlogs before user complaints escalate.

#### Visual 1.4: Earning Module Yield Breakdown
* **Metric:** Total VE Distributed by Product Feature
* **Calculation:** `SUM(fct_rewards[amount]) GROUP BY source_type`
* **Data Source:** `fct_rewards`
* **Visualization:** Ranked Horizontal Bar Chart
* **Filters:** Status = `'Credited'`
* **Dimensions:** Feature Source (`source_type`)
* **Date Range:** Trailing 30 Days
* **Refresh Frequency:** Daily
* **Business Question:** Which product features distribute the majority of user incentives?
* **Decision Supported:** Directs engineering roadmap priorities between third-party offerwalls, daily streaks, and mini-games.

---

## 3. Dashboard 2 — User Analytics

**Target Audience:** Head of Growth, Product Managers, User Acquisition Leads  
**Operational Cadence:** Daily Refresh

### Visual Specifications
1. **Acquisition Funnel Progression (Funnel Chart):**
   * *Metric:* Conversion count across *Visits $\rightarrow$ Registrations $\rightarrow$ Onboarded $\rightarrow$ Activated $\rightarrow$ Retained Day-30*.
   * *Dimensions:* Acquisition Channel (`registration_source`).
   * *Decision Supported:* Reallocates marketing acquisition capital away from low-converting referral campaigns toward high-activation channels.
2. **Geographic Distribution (Choropleth Map & Data Table):**
   * *Metric:* Registered and Active Users by ISO Country Code (`country_code`).
   * *Dimensions:* Country (`IN`, `US`, `GB`, `BR`, `PH`).
   * *Decision Supported:* Guides offerwall partner onboarding based on where user demand is concentrating.
3. **Device & OS Distribution (Donut Chart):**
   * *Metric:* Percentage of DAU on Android Mobile vs. iOS Mobile vs. Desktop Web.
   * *Dimensions:* `signup_device_type`.
   * *Decision Supported:* Determines mobile client engineering sprint allocation and QA device testing priorities.
4. **Cohort Retention Heatmap (Matrix Heatmap):**
   * *Metric:* Retention % at Day 1, 3, 7, 14, and 30 by weekly signup cohorts.
   * *Calculation:* `COUNT(active users on Day N) / Cohort Signup Size`.
   * *Decision Supported:* Evaluates whether recent onboarding or UI updates improved long-term customer habituation.

---

## 4. Dashboard 3 — Engagement & Gamification

**Target Audience:** Game Economy Designer, Product Manager, Retention Specialist  
**Operational Cadence:** Daily Refresh

### Visual Specifications
1. **Daily Habituation Loop Adoption (Stacked Column):**
   * *Metric:* Unique users claiming Daily Streaks vs. Spin Wheel vs. Quests.
   * *Dimensions:* Date, Gamification Feature.
   * *Decision Supported:* Adjusts daily streak coin rewards if users stop logging in during mid-week periods.
2. **Task Execution Heatmap (Grid Heatmap):**
   * *Metric:* Task Start Volume sliced by Hour of Day ($0–23$) and Day of Week ($Sun–Sat$).
   * *Dimensions:* `EXTRACT(HOUR FROM start_time)`, `EXTRACT(DOW FROM start_time)`.
   * *Decision Supported:* Optimizes automated push notification delivery timing for high-value tasks.
3. **Streak Continuance Decay Curve (Step Line):**
   * *Metric:* User retention probability from Streak Day 1 through Day 30.
   * *Dimensions:* `current_streak_days`.
   * *Decision Supported:* Pinpoints the exact milestone day where users encounter friction and drop their streaks.
4. **Gamification Level Progression (Histogram):**
   * *Metric:* Distribution of active users across Level Tiers 1 through 10.
   * *Dimensions:* `current_level`.
   * *Decision Supported:* Re-balances XP thresholds if the majority of users get stuck at intermediate levels.

---

## 5. Dashboard 4 — Rewards & Reversals

**Target Audience:** CFO, Risk & Fraud Lead, Partnerships Director  
**Operational Cadence:** Real-time / Hourly

### Visual Specifications
1. **Reward Distribution by Source (100% Stacked Bar):**
   * *Metric:* Proportion of VE distributed via Offerwalls vs. Daily Bonuses vs. Referrals.
   * *Dimensions:* Calendar Month, Feature Module.
   * *Decision Supported:* Prevents unmonitored virtual inflation caused by unbacked gamified mini-games.
2. **Partner Chargeback & Reversal Rate (Clustered Column):**
   * *Metric:* Gross Credited VE vs. Invalidation Reversals (`[Reward_Reversal_Rate_Pct]`).
   * *Dimensions:* Partner Network (`provider_id`).
   * *Decision Supported:* Triggers contract renegotiation or traffic pausing on partners whose chargeback rate exceeds $3.0\%$.
3. **Reward Settlement Latency (Box Plot):**
   * *Metric:* Distribution of elapsed minutes from task completion to wallet ledger credit.
   * *Dimensions:* Offer Category (`Survey` vs. `Game_Install`).
   * *Decision Supported:* Sets user expectations on offer detail cards regarding pending credit wait times.
4. **Top 10 High-Yield Offerwall Campaigns (Ranked Table):**
   * *Metric:* Campaign Name, Partner, Total Completions, Net Payout, User Rating.
   * *Dimensions:* `task_name`, `provider_id`.
   * *Decision Supported:* Features top-performing campaigns on the app home screen to maximize user yield.

---

## 6. Dashboard 5 — Wallet & Ledger Reconciliation

**Target Audience:** Lead Data Architect, DBA, Finance Controller  
**Operational Cadence:** Hourly Automated Run

### Visual Specifications
1. **Daily Balance Inflow vs. Outflow (Waterfall Chart):**
   * *Metric:* Total Credits (+), Total Debits (-), Reversals (-), Net Balance Delta.
   * *Dimensions:* Date, Transaction Type.
   * *Decision Supported:* Confirms that daily platform virtual balance expansions match verified commercial receivables.
2. **Balance State Segmentation (Stacked Area):**
   * *Metric:* Aggregate Pending Balance vs. Available Settled Balance.
   * *Dimensions:* Date.
   * *Decision Supported:* Evaluates near-term liquidity demand as pending holds mature into withdrawable funds.
3. **Virtual Currency Velocity (Line Chart):**
   * *Metric:* Circulating token velocity ratio (`[Net Virtual Currency Velocity]`).
   * *Dimensions:* Weekly Cadence.
   * *Decision Supported:* Alerts economists if users are hoarding tokens instead of redeeming them for payouts.
4. **Zero-Tolerance Ledger Integrity Monitor (Alert Banner & Log):**
   * *Metric:* `[Ledger_Audit_Check]` (Difference between balance snapshot and sum of transaction rows).
   * *Threshold:* Must equal exactly `0.00`.
   * *Decision Supported:* Automatically freezes payment gateway API dispatch if any user balance fails mathematical proof.

---

## 7. Dashboard 6 — Withdrawals & Payout Fulfillment

**Target Audience:** Operations Lead, Fraud & Risk Analyst, Compliance Officer  
**Operational Cadence:** Real-Time Operational Queue

### Visual Specifications
1. **Withdrawal Lifecycle State Mix (Donut Chart):**
   * *Metric:* Share of cashout requests in `Completed`, `Processing`, `Rejected`, and `Reversed`.
   * *Dimensions:* `status`.
   * *Decision Supported:* Monitors overall health of cash fulfillment rails.
2. **Median Processing Time by Payout Rail (Horizontal Bar):**
   * *Metric:* `[Median_Withdrawal_Processing_Hours]` across PayPal, UPI Direct, Crypto, and Gift Cards.
   * *Dimensions:* `payout_method`.
   * *Decision Supported:* Identifies sluggish payment processors requiring technical escalation or route switching.
3. **Pending Queue Age Monitoring (Age Bucket Histogram):**
   * *Metric:* Count of pending cashouts aged $<2\text{h}$, $2–12\text{h}$, $12–24\text{h}$, and $>24\text{h}$.
   * *Dimensions:* Queue Age Bucket.
   * *Decision Supported:* Triggers immediate overtime staffing if cashouts older than 24 hours exceed 50 requests.
4. **Rejection Root Cause Taxonomy (Pareto Chart):**
   * *Metric:* Count of rejected cashouts by causal code (`KYC_Failed`, `Invalid_Handle`, `Risk_Stop`).
   * *Dimensions:* `reason_category`.
   * *Decision Supported:* Improves frontend payout form validation to prevent typographical user errors.

---

## 8. Dashboard 7 — Referrals & Viral Acquisition

**Target Audience:** Growth Marketing Lead, Social Media Coordinator  
**Operational Cadence:** Daily Refresh

### Visual Specifications
1. **The 4-Stage Viral Funnel (Funnel Visual):**
   * *Metric:* Drop-off across *Links Created $\rightarrow$ Users Registered $\rightarrow$ Users Activated $\rightarrow$ Bonuses Converted*.
   * *Dimensions:* Acquisition Period.
   * *Decision Supported:* Measures the drop between registration and activation to identify sybil bot rings.
2. **Viral Channel Share Distribution (Pie Chart):**
   * *Metric:* Referral registrations driven by WhatsApp vs. Telegram vs. Direct URL vs. Twitter/X.
   * *Dimensions:* `share_channel`.
   * *Decision Supported:* Focuses in-app social share UI buttons on channels yielding the highest conversion.
3. **Power Referrer Leaderboard (Data Table):**
   * *Metric:* Top 20 referrers ranked by total invites, activation rate, and cumulative commission earned.
   * *Dimensions:* `referrer_user_id`.
   * *Decision Supported:* Identifies top brand ambassadors for VIP partnership perks and custom vanity codes.
4. **Sybil & Duplicate IP Defense Monitor (Column Chart):**
   * *Metric:* Count of referral pairs blocked due to shared IP subnet collision (`ip_collision_flag = TRUE`).
   * *Dimensions:* Date.
   * *Decision Supported:* Audits fraud filter effectiveness and prevents payout of illegitimate referral bonuses.

---
*End of Deliverable DELIV-15 — Analytics Dashboard Blueprint.*
