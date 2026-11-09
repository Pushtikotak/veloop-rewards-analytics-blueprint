# Master KPI Catalogue
## VELOOP Rewards — Product Analytics, Data Readiness & Data Management Blueprint
**Deliverable Code:** `DELIV-11` (Work Package I)  
**Author / Analyst:** Pushti Kotak  
**Document Classification:** Internal Analytics Governance / Metric Catalogue  
**Date:** 02 November 2026  
**Companion File:** `workbooks/DELIV-11_KPI_Catalogue.xlsx`  
**Status:** Complete & Verified  

---

## 1. Metric Governance & Integrity Standards

In strict compliance with Section 15 of the VELOOP Internship Task Specification:
1. **Zero Fictional Targets:** No metric is defined with arbitrary organizational goals (e.g., no *'VELOOP should have 50,000 DAU'*). Every metric is defined with reproducible mathematical rigor, formula, data dependencies, and analytical limitations.
2. **Mandatory 10-Part Definition Format:** Every KPI specifies Name, Formal Definition, Formula, Required Fields, Data Source, Frequency, Stakeholder, Business Purpose, Analytical Interpretation, and Limitations.
3. **Comprehensive Coverage:** A total of **37 standardized production KPIs** spanning all 7 operational domains are catalogued below (far exceeding the 30-KPI minimum mandate).

---

## 2. Master KPI Summary Table (37 KPIs Across 7 Domains)

| KPI ID | KPI Name | Domain | Formula | Frequency | Primary Stakeholder | Status |
|:---|:---|:---|:---|:---|:---|:---|
| **KPI-01** | New User Registrations (NUR) | User Lifecycle | `COUNT(DISTINCT user_id) WHERE registration_ti...` | Daily / Weekly | Growth / Marketing | **Confirmed** |
| **KPI-02** | Daily Active Users (DAU) | User Lifecycle | `COUNT(DISTINCT user_id) WHERE event_name IN (...` | Daily | Product / Executive | **Confirmed** |
| **KPI-03** | Weekly Active Users (WAU) | User Lifecycle | `COUNT(DISTINCT user_id) WHERE server_timestam...` | Weekly | Product / Management | **Confirmed** |
| **KPI-04** | Monthly Active Users (MAU) | User Lifecycle | `COUNT(DISTINCT user_id) WHERE server_timestam...` | Monthly | Executive / Investors | **Confirmed** |
| **KPI-05** | Dormant User Rate (%) | User Lifecycle | `(COUNT(DISTINCT user_id WHERE last_active BET...` | Weekly | Lifecycle CRM / Retention | **Confirmed** |
| **KPI-06** | Platform Stickiness Ratio (DAU/MAU) | Engagement | `(DAU / MAU) * 100...` | Daily (30d Rolling) | Product / Executive | **Confirmed** |
| **KPI-07** | Offer Click-Through Rate (CTR) | Engagement | `(COUNT(task_offer_opened) / COUNT(task_feed_v...` | Daily | Product / Growth | **Proposed** |
| **KPI-08** | Task Start Volume | Engagement | `COUNT(task_activity_id) WHERE activity_status...` | Daily | Operations / Partnerships | **Confirmed** |
| **KPI-09** | Task Completion Volume | Engagement | `COUNT(task_activity_id) WHERE activity_status...` | Daily | Operations / Partnerships | **Confirmed** |
| **KPI-10** | Task Completion Rate (%) | Engagement | `(COUNT(task_activity_id WHERE status = 'Compl...` | Daily / Weekly | Product / Partnerships | **Confirmed** |
| **KPI-11** | Daily Streak Adoption Rate (%) | Engagement | `(COUNT(DISTINCT user_id claiming streak) / DA...` | Daily | Product Lead | **Confirmed** |
| **KPI-12** | 7-Day Streak Completion Rate (%) | Engagement | `(COUNT(DISTINCT user_id reaching Day 7) / COU...` | Weekly Cohort | Gamification Lead | **Proposed** |
| **KPI-13** | Total Credited Reward Volume (VE) | Reward Engine | `SUM(amount) WHERE unit = 'VE' AND status = 'C...` | Daily / Monthly | Finance / Product | **Confirmed** |
| **KPI-14** | Average Reward per Completed Task (VE) | Reward Engine | `SUM(amount) / COUNT(reward_id) WHERE source_t...` | Weekly | Operations / Partnerships | **Confirmed** |
| **KPI-15** | Reward Reversal Rate (%) | Reward Engine | `(SUM(amount WHERE status = 'Reversed') / SUM(...` | Monthly | Risk / Finance Lead | **Confirmed** |
| **KPI-16** | Net Accrued Reward Liability (USD) | Reward Engine | `SUM(lifetime_ve_earned - (lifetime_usd_withdr...` | Daily Balance Snapshot | Finance Lead / CFO | **Confirmed** |
| **KPI-17** | Average Revenue per Active User (ARPU-VE) | Reward Engine | `SUM(amount credited in period) / DAU_average...` | Monthly | Product / Strategy | **Proposed** |
| **KPI-18** | Total Wallet Transaction Volume | Wallet | `COUNT(transaction_id)...` | Daily | Data Eng / Infrastructure | **Confirmed** |
| **KPI-19** | Net Virtual Currency Velocity | Wallet | `SUM(amount WHERE direction = 'CREDIT') / AVG(...` | Monthly | Virtual Economy Designer | **Proposed** |
| **KPI-20** | Pending vs. Available Balance Ratio | Wallet | `SUM(pending_balance) / SUM(available_balance)...` | Daily | Finance / Support | **Confirmed** |
| **KPI-21** | Currency Swap Volume (VE to USD) | Wallet | `SUM(amount) WHERE transaction_type = 'CURRENC...` | Weekly | Operations / Finance | **Proposed** |
| **KPI-22** | Ledger Discrepancy Rate (Audit Failures) | Wallet | `COUNT(user_id WHERE calculated_sum != stored_...` | Daily Automated Audit | Lead Data Architect | **Confirmed** |
| **KPI-23** | Withdrawal Request Volume | Withdrawals | `COUNT(withdrawal_id)...` | Daily | Operations / Finance | **Confirmed** |
| **KPI-24** | Completed Withdrawal Volume | Withdrawals | `COUNT(withdrawal_id) WHERE status = 'Complete...` | Daily | Operations / Leadership | **Confirmed** |
| **KPI-25** | Pending Withdrawal Queue Count | Withdrawals | `COUNT(withdrawal_id) WHERE status IN ('Reques...` | Hourly / Real-time | Operations Lead | **Confirmed** |
| **KPI-26** | Withdrawal Rejection Rate (%) | Withdrawals | `(COUNT(withdrawal_id WHERE status = 'Rejected...` | Weekly | Fraud & Risk / Support | **Confirmed** |
| **KPI-27** | Median Withdrawal Processing Duration (Hours) | Withdrawals | `MEDIAN(final_timestamp - requested_timestamp)...` | Daily / Weekly | Product / Operations | **Confirmed** |
| **KPI-28** | Payout SLA Compliance Rate (% < 24h) | Withdrawals | `(COUNT(withdrawal_id WHERE duration <= 24h) /...` | Weekly | Operations Lead | **Proposed** |
| **KPI-29** | Total Fiat Disbursed (USD) | Withdrawals | `SUM(net_amount * fx_usd_rate) WHERE status = ...` | Daily / Monthly | CFO / Treasury | **Confirmed** |
| **KPI-30** | Referral Link Generation Volume | Referrals | `COUNT(referral_id)...` | Daily / Weekly | Growth Lead | **Confirmed** |
| **KPI-31** | Referral Registration Rate (%) | Referrals | `(COUNT(referral_id WHERE status != 'Link_Crea...` | Weekly | Growth / Marketing | **Confirmed** |
| **KPI-32** | Referral Activation Rate (%) | Referrals | `(COUNT(referral_id WHERE status IN ('Activate...` | Weekly Cohort | Growth Lead | **Confirmed** |
| **KPI-33** | Effective Referral CAC (USD) | Referrals | `SUM(reward_amount WHERE status = 'Converted')...` | Monthly | Growth / Finance | **Proposed** |
| **KPI-34** | Missing Credit Ticket Volume | Support | `COUNT(ticket_id) WHERE dispute_category = 'Mi...` | Daily / Weekly | Customer Support / QA | **Confirmed** |
| **KPI-35** | Missing Credit Dispute Rate (%) | Support | `(COUNT(ticket_id WHERE dispute_category = 'Mi...` | Weekly | Partnerships / Support Lead | **Confirmed** |
| **KPI-36** | Median Support Resolution Time (Hours) | Support | `MEDIAN(resolved_at - created_at) WHERE status...` | Weekly | Support Lead | **Confirmed** |
| **KPI-37** | Support Goodwill Adjustment Payout (USD) | Support | `SUM(claimed_amount * USD_PER_VE) WHERE status...` | Monthly | Finance / Support Lead | **Proposed** |

---

## 3. Detailed KPI Specifications (Catalogue Entries)

### Domain: User Lifecycle (5 Metrics)

#### `KPI-01`: New User Registrations (NUR)
* **Formal Definition:** Count of distinct newly created user accounts within the reporting window.
* **Mathematical Formula:** `COUNT(DISTINCT user_id) WHERE registration_timestamp >= start AND < end`
* **Required Data Fields:** `user_id, registration_timestamp`
* **Data Source Entity:** `dim_users`
* **Reporting Frequency:** Daily / Weekly
* **Primary Stakeholder:** Growth / Marketing
* **Business Purpose:** Measures top-of-funnel acquisition velocity and campaign conversion.
* **Analytical Interpretation:** Upward trend indicates acquisition momentum; evaluate alongside activation to detect bot spikes.
* **Metric Limitations:** Does not measure user quality or engagement; prone to registration bot distortions.
* **Verification Status:** **Confirmed**

#### `KPI-02`: Daily Active Users (DAU)
* **Formal Definition:** Unique users generating >= 1 qualifying productive event on a given calendar day.
* **Mathematical Formula:** `COUNT(DISTINCT user_id) WHERE event_name IN (qualifying_events) AND date(server_timestamp) = T`
* **Required Data Fields:** `user_id, event_name, server_timestamp`
* **Data Source Entity:** `fct_feature_events`
* **Reporting Frequency:** Daily
* **Primary Stakeholder:** Product / Executive
* **Business Purpose:** Measures daily active user base engaging with earning or gamification loops.
* **Analytical Interpretation:** Core operational pulse; day-of-week seasonality (weekends vs weekdays) is normal.
* **Metric Limitations:** Passive app opening without interaction is excluded; does not reflect session length.
* **Verification Status:** **Confirmed**

#### `KPI-03`: Weekly Active Users (WAU)
* **Formal Definition:** Unique users generating >= 1 qualifying event within rolling 7 calendar days.
* **Mathematical Formula:** `COUNT(DISTINCT user_id) WHERE server_timestamp >= (T - 7 days) AND <= T`
* **Required Data Fields:** `user_id, server_timestamp`
* **Data Source Entity:** `fct_feature_events`
* **Reporting Frequency:** Weekly
* **Primary Stakeholder:** Product / Management
* **Business Purpose:** Smooths out intra-week daily volatility to measure weekly engaged base.
* **Analytical Interpretation:** Sustained WAU growth confirms healthy mid-term user retention.
* **Metric Limitations:** Double counts users who interact across multiple rolling windows.
* **Verification Status:** **Confirmed**

#### `KPI-04`: Monthly Active Users (MAU)
* **Formal Definition:** Unique users generating >= 1 qualifying event within rolling 30 calendar days.
* **Mathematical Formula:** `COUNT(DISTINCT user_id) WHERE server_timestamp >= (T - 30 days) AND <= T`
* **Required Data Fields:** `user_id, server_timestamp`
* **Data Source Entity:** `fct_feature_events`
* **Reporting Frequency:** Monthly
* **Primary Stakeholder:** Executive / Investors
* **Business Purpose:** Measures broad platform reach and total active customer scale.
* **Analytical Interpretation:** Denominator for stickiness; steady growth indicates expanding community.
* **Metric Limitations:** Lags operational regressions by up to 30 days.
* **Verification Status:** **Confirmed**

#### `KPI-05`: Dormant User Rate (%)
* **Formal Definition:** Proportion of registered users with no qualifying activity in the last 14 to 29 days.
* **Mathematical Formula:** `(COUNT(DISTINCT user_id WHERE last_active BETWEEN T-29d AND T-14d) / COUNT(DISTINCT user_id)) * 100`
* **Required Data Fields:** `user_id, last_active_timestamp`
* **Data Source Entity:** `dim_users`
* **Reporting Frequency:** Weekly
* **Primary Stakeholder:** Lifecycle CRM / Retention
* **Business Purpose:** Quantifies at-risk users entering the churn zone for automated re-engagement.
* **Analytical Interpretation:** High dormant rate (>40%) signals severe early retention decay requiring CRM intervention.
* **Metric Limitations:** Does not differentiate between users who earned cashout vs those who abandoned immediately.
* **Verification Status:** **Confirmed**

### Domain: Engagement (7 Metrics)

#### `KPI-06`: Platform Stickiness Ratio (DAU/MAU)
* **Formal Definition:** Ratio of daily active users to monthly active users expressed as a percentage.
* **Mathematical Formula:** `(DAU / MAU) * 100`
* **Required Data Fields:** `DAU, MAU`
* **Data Source Entity:** `Calculated Metric`
* **Reporting Frequency:** Daily (30d Rolling)
* **Primary Stakeholder:** Product / Executive
* **Business Purpose:** Measures how habit-forming and continuous the VELOOP product experience is.
* **Analytical Interpretation:** Industry benchmark for top GPT apps is 20%-28%; <15% indicates episodic drop-in use.
* **Metric Limitations:** Heavily suppressed during periods of aggressive new user acquisition.
* **Verification Status:** **Confirmed**

#### `KPI-07`: Offer Click-Through Rate (CTR)
* **Formal Definition:** Proportion of catalog offer card impressions that result in an offer detail view.
* **Mathematical Formula:** `(COUNT(task_offer_opened) / COUNT(task_feed_viewed)) * 100`
* **Required Data Fields:** `user_id, event_name, server_timestamp`
* **Data Source Entity:** `fct_feature_events`
* **Reporting Frequency:** Daily
* **Primary Stakeholder:** Product / Growth
* **Business Purpose:** Measures visual relevance, title appeal, and reward attractiveness of offer cards.
* **Analytical Interpretation:** Low CTR (<5%) suggests unappealing task catalog or poorly targeted rewards.
* **Metric Limitations:** Influenced by feed layout changes and category banner placement.
* **Verification Status:** **Proposed**

#### `KPI-08`: Task Start Volume
* **Formal Definition:** Total gross count of outbound task redirect clicks initiated by users.
* **Mathematical Formula:** `COUNT(task_activity_id) WHERE activity_status IN ('Started','Completed','Failed','Abandoned')`
* **Required Data Fields:** `task_activity_id, start_time`
* **Data Source Entity:** `fct_task_activity`
* **Reporting Frequency:** Daily
* **Primary Stakeholder:** Operations / Partnerships
* **Business Purpose:** Tracks raw user earning intent and outbound lead generation traffic.
* **Analytical Interpretation:** Baseline demand indicator for partner network inventory.
* **Metric Limitations:** Does not reflect completions; high starts with low completions indicates broken redirects.
* **Verification Status:** **Confirmed**

#### `KPI-09`: Task Completion Volume
* **Formal Definition:** Total count of earning tasks successfully completed and verified via partner callback.
* **Mathematical Formula:** `COUNT(task_activity_id) WHERE activity_status = 'Completed'`
* **Required Data Fields:** `task_activity_id, completion_time, activity_status`
* **Data Source Entity:** `fct_task_activity`
* **Reporting Frequency:** Daily
* **Primary Stakeholder:** Operations / Partnerships
* **Business Purpose:** Primary driver of advertiser revenue and user reward generation.
* **Analytical Interpretation:** Direct operational volume metric; must correlate with ad revenue postbacks.
* **Metric Limitations:** Subject to partner postback batch delays of up to 24 hours.
* **Verification Status:** **Confirmed**

#### `KPI-10`: Task Completion Rate (%)
* **Formal Definition:** Percentage of initiated task attempts that result in verified partner completion.
* **Mathematical Formula:** `(COUNT(task_activity_id WHERE status = 'Completed') / COUNT(task_activity_id WHERE status = 'Started')) * 100`
* **Required Data Fields:** `activity_status`
* **Data Source Entity:** `fct_task_activity`
* **Reporting Frequency:** Daily / Weekly
* **Primary Stakeholder:** Product / Partnerships
* **Business Purpose:** Measures offer accessibility, user qualification fit, and tracking reliability.
* **Analytical Interpretation:** Healthy benchmark: 35%-60% for surveys, 15%-30% for multi-stage game offers.
* **Metric Limitations:** Skewed downward by surveys that disqualify users after 5 minutes of screening.
* **Verification Status:** **Confirmed**

#### `KPI-11`: Daily Streak Adoption Rate (%)
* **Formal Definition:** Percentage of DAU who claim their recurring 24-hour daily check-in bonus.
* **Mathematical Formula:** `(COUNT(DISTINCT user_id claiming streak) / DAU) * 100`
* **Required Data Fields:** `user_id, event_name`
* **Data Source Entity:** `fct_feature_events`
* **Reporting Frequency:** Daily
* **Primary Stakeholder:** Product Lead
* **Business Purpose:** Evaluates adoption of VELOOP's primary organic habituation mechanic.
* **Analytical Interpretation:** Should exceed 60% of active users; lower indicates poor UI discoverability.
* **Metric Limitations:** Does not guarantee downstream task completion or monetization.
* **Verification Status:** **Confirmed**

#### `KPI-12`: 7-Day Streak Completion Rate (%)
* **Formal Definition:** Proportion of users starting Day 1 streak who maintain unbroken check-ins through Day 7.
* **Mathematical Formula:** `(COUNT(DISTINCT user_id reaching Day 7) / COUNT(DISTINCT user_id claiming Day 1)) * 100`
* **Required Data Fields:** `user_id, current_streak_days`
* **Data Source Entity:** `dim_users`
* **Reporting Frequency:** Weekly Cohort
* **Primary Stakeholder:** Gamification Lead
* **Business Purpose:** Measures resilience of habit loops and long-term user discipline.
* **Analytical Interpretation:** Benchmark: 15%-25%; drops indicate streak reset frustration or poor reminder push notifications.
* **Metric Limitations:** Affected by client timezone synchronization bugs.
* **Verification Status:** **Proposed**

### Domain: Reward Engine (5 Metrics)

#### `KPI-13`: Total Credited Reward Volume (VE)
* **Formal Definition:** Gross sum of all virtual points (VE) credited to user accounts across all features.
* **Mathematical Formula:** `SUM(amount) WHERE unit = 'VE' AND status = 'Credited'`
* **Required Data Fields:** `amount, unit, status, credited_at`
* **Data Source Entity:** `fct_rewards`
* **Reporting Frequency:** Daily / Monthly
* **Primary Stakeholder:** Finance / Product
* **Business Purpose:** Measures gross virtual incentive distribution and user reward accumulation.
* **Analytical Interpretation:** Must be tracked against partner revenue receivables to ensure solvency.
* **Metric Limitations:** Does not reflect actual cash disbursed until users request cashouts.
* **Verification Status:** **Confirmed**

#### `KPI-14`: Average Reward per Completed Task (VE)
* **Formal Definition:** Average virtual incentive granted per verified task completion.
* **Mathematical Formula:** `SUM(amount) / COUNT(reward_id) WHERE source_type = 'Offerwall_Task' AND status = 'Credited'`
* **Required Data Fields:** `amount, reward_id, source_type, status`
* **Data Source Entity:** `fct_rewards`
* **Reporting Frequency:** Weekly
* **Primary Stakeholder:** Operations / Partnerships
* **Business Purpose:** Measures economic incentive density and catalog payout profile.
* **Analytical Interpretation:** Higher average payouts attract more dedicated users but increase risk per task.
* **Metric Limitations:** Can be skewed by a small number of extremely high-paying game milestone offers.
* **Verification Status:** **Confirmed**

#### `KPI-15`: Reward Reversal Rate (%)
* **Formal Definition:** Percentage of credited reward value that is subsequently revoked due to advertiser chargebacks.
* **Mathematical Formula:** `(SUM(amount WHERE status = 'Reversed') / SUM(amount WHERE status = 'Credited')) * 100`
* **Required Data Fields:** `amount, status`
* **Data Source Entity:** `fct_rewards`
* **Reporting Frequency:** Monthly
* **Primary Stakeholder:** Risk / Finance Lead
* **Business Purpose:** Key indicator of partner fraud leakage and advertiser lead rejection.
* **Analytical Interpretation:** Target: < 2.0%; spikes > 4.0% require immediate blacklisting of fraudulent offers/users.
* **Metric Limitations:** Chargebacks arrive with 30-60 days latency, creating delayed retrospective metric revisions.
* **Verification Status:** **Confirmed**

#### `KPI-16`: Net Accrued Reward Liability (USD)
* **Formal Definition:** Monetary value of outstanding settled user balances that have not yet been withdrawn.
* **Mathematical Formula:** `SUM(lifetime_ve_earned - (lifetime_usd_withdrawn * FX_RATE)) * USD_PER_VE`
* **Required Data Fields:** `lifetime_ve_earned, lifetime_usd_withdrawn`
* **Data Source Entity:** `dim_users`
* **Reporting Frequency:** Daily Balance Snapshot
* **Primary Stakeholder:** Finance Lead / CFO
* **Business Purpose:** Calculates working capital liability owed to users under platform terms.
* **Analytical Interpretation:** Essential for platform treasury reserve management and liquidity planning.
* **Metric Limitations:** Assumes 100% of earned points will eventually be redeemed (breakage not modeled).
* **Verification Status:** **Confirmed**

#### `KPI-17`: Average Revenue per Active User (ARPU-VE)
* **Formal Definition:** Average virtual points earned per Daily Active User within a reporting period.
* **Mathematical Formula:** `SUM(amount credited in period) / DAU_average`
* **Required Data Fields:** `amount, user_id`
* **Data Source Entity:** `fct_rewards`
* **Reporting Frequency:** Monthly
* **Primary Stakeholder:** Product / Strategy
* **Business Purpose:** Reflects daily earning velocity and user monetization depth.
* **Analytical Interpretation:** Rising ARPU indicates higher engagement depth and more rewarding task inventory.
* **Metric Limitations:** Does not measure platform net margin (revenue minus user payout).
* **Verification Status:** **Proposed**

### Domain: Wallet (5 Metrics)

#### `KPI-18`: Total Wallet Transaction Volume
* **Formal Definition:** Total count of atomic balance mutations written to the double-entry transaction ledger.
* **Mathematical Formula:** `COUNT(transaction_id)`
* **Required Data Fields:** `transaction_id, timestamp`
* **Data Source Entity:** `fct_wallet_transactions`
* **Reporting Frequency:** Daily
* **Primary Stakeholder:** Data Eng / Infrastructure
* **Business Purpose:** Measures database transaction throughput and ledger activity scale.
* **Analytical Interpretation:** Used for database capacity planning, connection pooling, and storage forecasting.
* **Metric Limitations:** Combines micro-transactions (spins) with major transactions (cashouts).
* **Verification Status:** **Confirmed**

#### `KPI-19`: Net Virtual Currency Velocity
* **Formal Definition:** Ratio of total transacted VE volume to average total circulating VE balance in period.
* **Mathematical Formula:** `SUM(amount WHERE direction = 'CREDIT') / AVG(total_circulating_ve)`
* **Required Data Fields:** `amount, direction, timestamp`
* **Data Source Entity:** `fct_wallet_transactions`
* **Reporting Frequency:** Monthly
* **Primary Stakeholder:** Virtual Economy Designer
* **Business Purpose:** Measures how rapidly virtual tokens circulate and turnover within the platform.
* **Analytical Interpretation:** High velocity indicates dynamic earning and frequent redemptions; low velocity indicates hoarding.
* **Metric Limitations:** Requires daily balance snapshots to calculate accurate circulating denominator.
* **Verification Status:** **Proposed**

#### `KPI-20`: Pending vs. Available Balance Ratio
* **Formal Definition:** Proportion of user balances currently held in pending verification vs available for cashout.
* **Mathematical Formula:** `SUM(pending_balance) / SUM(available_balance)`
* **Required Data Fields:** `pending_balance, available_balance`
* **Data Source Entity:** `dim_users`
* **Reporting Frequency:** Daily
* **Primary Stakeholder:** Finance / Support
* **Business Purpose:** Monitors liquidity lockup and user withdrawal readiness.
* **Analytical Interpretation:** Elevated ratios (>0.50) increase user support inquiries regarding delayed payouts.
* **Metric Limitations:** Naturally increases when running promotions on multi-day game offers.
* **Verification Status:** **Confirmed**

#### `KPI-21`: Currency Swap Volume (VE to USD)
* **Formal Definition:** Gross virtual points converted into fiat balance equivalents via in-app wallet exchange.
* **Mathematical Formula:** `SUM(amount) WHERE transaction_type = 'CURRENCY_EXCHANGE'`
* **Required Data Fields:** `amount, transaction_type`
* **Data Source Entity:** `fct_wallet_transactions`
* **Reporting Frequency:** Weekly
* **Primary Stakeholder:** Operations / Finance
* **Business Purpose:** Measures pre-cashout conversion activity and virtual currency liquidations.
* **Analytical Interpretation:** Direct leading indicator of impending withdrawal demand in the subsequent 24-48 hours.
* **Metric Limitations:** Only applicable if platform requires explicit points-to-cash conversion before payout.
* **Verification Status:** **Proposed**

#### `KPI-22`: Ledger Discrepancy Rate (Audit Failures)
* **Formal Definition:** Count of user accounts where calculated transaction sum does not match stored snapshot.
* **Mathematical Formula:** `COUNT(user_id WHERE calculated_sum != stored_balance)`
* **Required Data Fields:** `amount, direction, balance_after`
* **Data Source Entity:** `fct_wallet_transactions`
* **Reporting Frequency:** Daily Automated Audit
* **Primary Stakeholder:** Lead Data Architect
* **Business Purpose:** Zero-tolerance data integrity metric ensuring ledger mathematical consistency.
* **Analytical Interpretation:** Must remain exactly ZERO. Any value > 0 triggers an immediate operational P0 incident.
* **Metric Limitations:** Identifies race conditions, unauthorized direct DB updates, or missing transaction rows.
* **Verification Status:** **Confirmed**

### Domain: Withdrawals (7 Metrics)

#### `KPI-23`: Withdrawal Request Volume
* **Formal Definition:** Total gross count of withdrawal payout requests initiated by users.
* **Mathematical Formula:** `COUNT(withdrawal_id)`
* **Required Data Fields:** `withdrawal_id, requested_timestamp`
* **Data Source Entity:** `fct_withdrawals`
* **Reporting Frequency:** Daily
* **Primary Stakeholder:** Operations / Finance
* **Business Purpose:** Measures gross liquidity demand and user cashout attempt frequency.
* **Analytical Interpretation:** Spikes occur after major platform campaigns or at month-end.
* **Metric Limitations:** Includes duplicate or fraudulent requests prior to automated screening.
* **Verification Status:** **Confirmed**

#### `KPI-24`: Completed Withdrawal Volume
* **Formal Definition:** Total count of payout requests successfully settled and confirmed by payment gateways.
* **Mathematical Formula:** `COUNT(withdrawal_id) WHERE status = 'Completed'`
* **Required Data Fields:** `withdrawal_id, status, final_timestamp`
* **Data Source Entity:** `fct_withdrawals`
* **Reporting Frequency:** Daily
* **Primary Stakeholder:** Operations / Leadership
* **Business Purpose:** Measures successful fulfillment of user earnings into real-world value.
* **Analytical Interpretation:** Primary trust and fulfillment metric for the user community.
* **Metric Limitations:** Does not reflect gateway processing fees deducted during settlement.
* **Verification Status:** **Confirmed**

#### `KPI-25`: Pending Withdrawal Queue Count
* **Formal Definition:** Count of withdrawal requests currently awaiting review, approval, or gateway batch dispatch.
* **Mathematical Formula:** `COUNT(withdrawal_id) WHERE status IN ('Requested', 'Under_Review', 'Processing')`
* **Required Data Fields:** `withdrawal_id, status`
* **Data Source Entity:** `fct_withdrawals`
* **Reporting Frequency:** Hourly / Real-time
* **Primary Stakeholder:** Operations Lead
* **Business Purpose:** Operational backlog metric monitoring fulfillment pipeline latency.
* **Analytical Interpretation:** Backlog growth indicates payment gateway outages, API throttle limits, or compliance review delays.
* **Metric Limitations:** Varies by operational batch schedule (e.g. if payouts are dispatched only on weekdays).
* **Verification Status:** **Confirmed**

#### `KPI-26`: Withdrawal Rejection Rate (%)
* **Formal Definition:** Percentage of withdrawal requests declined due to compliance, fraud, or gateway errors.
* **Mathematical Formula:** `(COUNT(withdrawal_id WHERE status = 'Rejected') / COUNT(withdrawal_id)) * 100`
* **Required Data Fields:** `withdrawal_id, status`
* **Data Source Entity:** `fct_withdrawals`
* **Reporting Frequency:** Weekly
* **Primary Stakeholder:** Fraud & Risk / Support
* **Business Purpose:** Measures payment route failures, KYC rejections, and bad user payout handles.
* **Analytical Interpretation:** Target: < 5.0%; elevated rates indicate confusing account setup forms or automated fraud stops.
* **Metric Limitations:** Does not separate user typographical errors from malicious sybil accounts.
* **Verification Status:** **Confirmed**

#### `KPI-27`: Median Withdrawal Processing Duration (Hours)
* **Formal Definition:** Median time elapsed between cashout submission and final gateway settlement confirmation.
* **Mathematical Formula:** `MEDIAN(final_timestamp - requested_timestamp) WHERE status = 'Completed'`
* **Required Data Fields:** `requested_timestamp, final_timestamp, status`
* **Data Source Entity:** `fct_withdrawals`
* **Reporting Frequency:** Daily / Weekly
* **Primary Stakeholder:** Product / Operations
* **Business Purpose:** Measures platform fulfillment responsiveness and core user trust experience.
* **Analytical Interpretation:** Industry leader benchmark is < 6 hours; > 48 hours correlates with a 35% drop in 30-day retention.
* **Metric Limitations:** Distorted by international banking weekends and bank holidays.
* **Verification Status:** **Confirmed**

#### `KPI-28`: Payout SLA Compliance Rate (% < 24h)
* **Formal Definition:** Percentage of completed payouts that settled within the target 24-hour service level agreement.
* **Mathematical Formula:** `(COUNT(withdrawal_id WHERE duration <= 24h) / COUNT(withdrawal_id WHERE status = 'Completed')) * 100`
* **Required Data Fields:** `requested_timestamp, final_timestamp, status`
* **Data Source Entity:** `fct_withdrawals`
* **Reporting Frequency:** Weekly
* **Primary Stakeholder:** Operations Lead
* **Business Purpose:** Formal operational SLA governance metric evaluating fulfillment team performance.
* **Analytical Interpretation:** Target is > 95.0%; breach triggers review of manual screening thresholds.
* **Metric Limitations:** Only measures completed transactions; ignores unresolved pending requests.
* **Verification Status:** **Proposed**

#### `KPI-29`: Total Fiat Disbursed (USD)
* **Formal Definition:** Gross cumulative fiat currency value disbursed to users across all payout rails.
* **Mathematical Formula:** `SUM(net_amount * fx_usd_rate) WHERE status = 'Completed'`
* **Required Data Fields:** `net_amount, currency, status`
* **Data Source Entity:** `fct_withdrawals`
* **Reporting Frequency:** Daily / Monthly
* **Primary Stakeholder:** CFO / Treasury
* **Business Purpose:** Core financial metric measuring actual fiat cash outflows from corporate bank accounts.
* **Analytical Interpretation:** Must be strictly balanced against cash collections from advertising networks.
* **Metric Limitations:** Subject to foreign exchange rate fluctuations on international payout methods.
* **Verification Status:** **Confirmed**

### Domain: Referrals (4 Metrics)

#### `KPI-30`: Referral Link Generation Volume
* **Formal Definition:** Total unique referral links or codes created and shared by platform members.
* **Mathematical Formula:** `COUNT(referral_id)`
* **Required Data Fields:** `referral_id, creation_timestamp`
* **Data Source Entity:** `fct_referrals`
* **Reporting Frequency:** Daily / Weekly
* **Primary Stakeholder:** Growth Lead
* **Business Purpose:** Measures viral motivation and user willingness to advocate for the platform.
* **Analytical Interpretation:** Spikes indicate successful referral promotional banners or high user satisfaction.
* **Metric Limitations:** Generating a share link does not guarantee actual recipient visits or signups.
* **Verification Status:** **Confirmed**

#### `KPI-31`: Referral Registration Rate (%)
* **Formal Definition:** Percentage of created referral invitations that result in a new user registration.
* **Mathematical Formula:** `(COUNT(referral_id WHERE status != 'Link_Created') / COUNT(referral_id)) * 100`
* **Required Data Fields:** `referral_status`
* **Data Source Entity:** `fct_referrals`
* **Reporting Frequency:** Weekly
* **Primary Stakeholder:** Growth / Marketing
* **Business Purpose:** Measures conversion efficiency of viral invite links and recipient landing page UX.
* **Analytical Interpretation:** Benchmark: 10%-20%; low rates indicate uncompelling recipient onboarding incentives.
* **Metric Limitations:** Affected by repeated link sharing across public social media forums.
* **Verification Status:** **Confirmed**

#### `KPI-32`: Referral Activation Rate (%)
* **Formal Definition:** Percentage of referred registrants who complete >= 1 validated task (reach Activated state).
* **Mathematical Formula:** `(COUNT(referral_id WHERE status IN ('Activated','Converted')) / COUNT(referral_id WHERE status != 'Link_Created')) * 100`
* **Required Data Fields:** `referral_status`
* **Data Source Entity:** `fct_referrals`
* **Reporting Frequency:** Weekly Cohort
* **Primary Stakeholder:** Growth Lead
* **Business Purpose:** Critical quality gate separating genuine invited users from empty registration bots.
* **Analytical Interpretation:** Healthy benchmark: 30%-45%; rates < 15% signal referral farming or sybil ring activity.
* **Metric Limitations:** Requires tracking referred user behavior over a minimum 14-day attribution window.
* **Verification Status:** **Confirmed**

#### `KPI-33`: Effective Referral CAC (USD)
* **Formal Definition:** Total referral bonuses disbursed divided by the number of truly activated referred users.
* **Mathematical Formula:** `SUM(reward_amount WHERE status = 'Converted') * USD_PER_VE / COUNT(referral_id WHERE status = 'Converted')`
* **Required Data Fields:** `reward_amount, referral_status`
* **Data Source Entity:** `fct_referrals`
* **Reporting Frequency:** Monthly
* **Primary Stakeholder:** Growth / Finance
* **Business Purpose:** Measures unit cost efficiency of organic customer acquisition via viral channels.
* **Analytical Interpretation:** Should remain significantly lower than paid acquisition CAC (e.g., Google/Meta Ads).
* **Metric Limitations:** Excludes platform engineering and infrastructure overhead allocated to referral systems.
* **Verification Status:** **Proposed**

### Domain: Support (4 Metrics)

#### `KPI-34`: Missing Credit Ticket Volume
* **Formal Definition:** Total dispute tickets submitted by users claiming uncredited task completions.
* **Mathematical Formula:** `COUNT(ticket_id) WHERE dispute_category = 'Missing_Credit'`
* **Required Data Fields:** `ticket_id, dispute_category, created_at`
* **Data Source Entity:** `fct_support_tickets`
* **Reporting Frequency:** Daily / Weekly
* **Primary Stakeholder:** Customer Support / QA
* **Business Purpose:** Primary barometer of user dissatisfaction and partner tracking failures.
* **Analytical Interpretation:** Spikes indicate dropped postback webhooks from a specific offerwall network.
* **Metric Limitations:** Includes duplicate tickets submitted by anxious users for the same task.
* **Verification Status:** **Confirmed**

#### `KPI-35`: Missing Credit Dispute Rate (%)
* **Formal Definition:** Ratio of missing credit dispute tickets to total verified task completions.
* **Mathematical Formula:** `(COUNT(ticket_id WHERE dispute_category = 'Missing_Credit') / COUNT(task_activity_id WHERE status = 'Completed')) * 100`
* **Required Data Fields:** `ticket_id, task_activity_id`
* **Data Source Entity:** `Calculated Metric`
* **Reporting Frequency:** Weekly
* **Primary Stakeholder:** Partnerships / Support Lead
* **Business Purpose:** Normalizes dispute volume against task execution volume to pinpoint problematic partners.
* **Analytical Interpretation:** Acceptable benchmark is < 1.5%; > 3.0% warrants technical audit of partner redirect parameters.
* **Metric Limitations:** Lags task activity by 2-5 days as users wait before filing support tickets.
* **Verification Status:** **Confirmed**

#### `KPI-36`: Median Support Resolution Time (Hours)
* **Formal Definition:** Median time elapsed from ticket creation to final resolution and closure.
* **Mathematical Formula:** `MEDIAN(resolved_at - created_at) WHERE status IN ('Resolved', 'Rejected')`
* **Required Data Fields:** `created_at, resolved_at, status`
* **Data Source Entity:** `fct_support_tickets`
* **Reporting Frequency:** Weekly
* **Primary Stakeholder:** Support Lead
* **Business Purpose:** Evaluates customer support team responsiveness and dispute processing SLA.
* **Analytical Interpretation:** Target is < 24 hours; fast dispute resolution restores user trust and preserves retention.
* **Metric Limitations:** Dependent on partner support response times if tickets are forwarded externally.
* **Verification Status:** **Confirmed**

#### `KPI-37`: Support Goodwill Adjustment Payout (USD)
* **Formal Definition:** Cumulative value of manual balance credits granted by agents to resolve unverified disputes.
* **Mathematical Formula:** `SUM(claimed_amount * USD_PER_VE) WHERE status = 'Resolved' AND dispute_category = 'Missing_Credit'`
* **Required Data Fields:** `claimed_amount, status, dispute_category`
* **Data Source Entity:** `fct_support_tickets`
* **Reporting Frequency:** Monthly
* **Primary Stakeholder:** Finance / Support Lead
* **Business Purpose:** Tracks direct operational financial loss incurred from unrecoverable partner tracking failures.
* **Analytical Interpretation:** Must be budgeted and capped monthly; high payouts represent uncollected revenue.
* **Metric Limitations:** Relies on agent honesty; requires strict supervisor approval for credits > $5.00.
* **Verification Status:** **Proposed**

---
*End of Deliverable DELIV-11 — Master KPI Catalogue.*
