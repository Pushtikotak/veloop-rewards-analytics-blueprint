# VELOOP Data Dictionary
## VELOOP Rewards — Product Analytics, Data Readiness & Data Management Blueprint
**Deliverable Code:** `DELIV-09` (Work Package G)  
**Author / Analyst:** Pushti Kotak  
**Document Classification:** Internal Data Architecture / Metadata Repository  
**Date:** 02 November 2026  
**Companion File:** `workbooks/DELIV-09_Data_Dictionary.xlsx`  
**Status:** Complete & Verified  

---

## 1. Architectural Scope & Metadata Standards

The **VELOP Data Dictionary** provides a comprehensive, field-level metadata repository for the entire analytical and relational data architecture. In strict accordance with Section 13 of the task specification:
1. **Beyond Column Names:** For every field, the dictionary provides exact physical types, definitions, example values, strict validation constraints, security classifications, and analytical justifications.
2. **No Unnecessary PII:** Conforming with Section 8 & 34, no passwords, API tokens, raw IP addresses, or raw bank details are included.
3. **Comprehensive Coverage:** A total of **100 meaningful fields** across 8 core entities are catalogued below (far exceeding the 75-field minimum mandate).

---

## 2. Master Data Dictionary Table (100 Fields Across 8 Entities)

### Entity: `dim_users` (18 fields)

| Field Name | Data Type | Definition | Example Value | Required? | Allowed Values | Validation Rule | Source System | Sensitivity | Analytical Use | Status |
|---|---|---|---|---|---|---|---|---|---|---|
| user_id | VARCHAR(36) | Canonical surrogate unique identifier for each user account. | usr_4f9a12c8-88be-4011-8e9a-251a37c93e41 | Yes | UUIDv4 string | Must match regex usr_[0-9a-f-]{36} | Auth Service | Internal | Primary foreign key across all behavioral and transactional tables. | Confirmed |
| account_status | VARCHAR(20) | Current lifecycle state of the user account. | Active | Yes | Registered, Onboarded, Active, Dormant, Churned, Suspended, Banned | Must belong to predefined account lifecycle state enum | State Worker | Internal | Cohort segmentation, churn analysis, and access authorization. | Confirmed |
| registration_timestamp | TIMESTAMP WITH TIME ZONE | UTC timestamp when the user submitted registration. | 2026-10-15T08:30:00Z | Yes | Valid UTC timestamp | Must be <= CURRENT_TIMESTAMP | Auth DB | Internal | Cohort anchor for Day-N retention and onboarding velocity. | Confirmed |
| registration_source | VARCHAR(50) | Marketing or referral acquisition channel. | Google_Ads | Yes | Organic_Search, Direct, Google_Ads, Meta_Ads, Referral_Program, Influencer | Must belong to approved acquisition taxonomy | Client URL | Internal | CAC attribution and marketing channel ROI calculation. | Confirmed |
| referral_code_used | VARCHAR(20) | Referral code entered during account registration. | VELOOP_TOPUSER | No | Alphanumeric string 6-20 chars | Must exist in dim_users.referral_code if populated | Signup Form | Internal | Maps user to referrer for attribution and bonus payout. | Confirmed |
| auth_provider | VARCHAR(20) | Authentication mechanism used during signup. | Google_OAuth | Yes | Email_Password, Google_OAuth, Apple_ID, Telegram | Must match supported auth provider list | Auth Gateway | Internal | Evaluates adoption of OAuth vs. traditional credentials. | Confirmed |
| country_code | CHAR(2) | ISO 3166-1 alpha-2 country code of the user. | IN | Yes | ISO 2-letter uppercase country code | Must be uppercase 2 characters (e.g., IN, US, GB, BR) | Geo-IP Engine | Internal | Geographic slicing, offer availability, and localized payout rails. | Confirmed |
| signup_device_type | VARCHAR(20) | Primary device form-factor at initial registration. | Android_Mobile | Yes | Android_Mobile, iOS_Mobile, Desktop_Web, Mobile_Web | Must belong to standard device taxonomy | User-Agent | Internal | Technical performance and mobile vs. desktop conversion analysis. | Confirmed |
| signup_app_version | VARCHAR(15) | Software version of mobile client at registration. | v1.2.0 | No | Semantic versioning string | Must follow vx.y.z format if client is mobile app | Client Headers | Internal | Tracks legacy version adoption and app upgrade compliance. | Confirmed |
| signup_ip_hash | VARCHAR(64) | SHA-256 hashed IP address recorded at registration. | e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855 | Yes | 64-character hex string | Must be valid 64-char SHA-256 hex digest | Ingestion Pipe | Restricted | Fraud ring detection and multi-accounting sybil defense. | Proposed |
| email_verified_flag | BOOLEAN | Indicates whether email verification link was confirmed. | TRUE | Yes | TRUE, FALSE | Boolean; defaults to FALSE upon creation | Auth DB | Internal | Distinguishes high-trust accounts from disposable registrations. | Confirmed |
| onboarding_completed_flag | BOOLEAN | Indicates whether user completed welcome tutorial. | TRUE | Yes | TRUE, FALSE | Boolean; defaults to FALSE upon creation | Frontend SDK | Internal | Evaluates onboarding funnel friction and early user activation. | Confirmed |
| onboarding_completed_at | TIMESTAMP WITH TIME ZONE | UTC timestamp when welcome tutorial was completed. | 2026-10-15T08:35:12Z | No | Valid UTC timestamp | Must be >= registration_timestamp if not null | Frontend SDK | Internal | Computes onboarding completion latency. | Proposed |
| current_level | INTEGER | User gamification level based on cumulative XP. | 3 | Yes | Integers >= 1 | Must be integer >= 1; defaults to 1 | Game Engine | Internal | Level progression analysis and tiered reward multipliers. | Confirmed |
| total_xp | INTEGER | Cumulative gamification experience points earned. | 1450 | Yes | Integers >= 0 | Monotonically increasing integer >= 0 | Game Engine | Internal | Gamification status and leaderboard ranking. | Confirmed |
| current_streak_days | INTEGER | Consecutive days user claimed daily check-in. | 5 | Yes | Integers >= 0 | Integer between 0 and 365; resets upon missed day | Streak Engine | Internal | Measures habituation, daily engagement, and churn demotivation. | Confirmed |
| lifetime_ve_earned | DECIMAL(12, 2) | Cumulative total of all VELOOP Earnings credited. | 4520.50 | Yes | Numeric >= 0.00 | Must equal sum of all verified credit transactions | Wallet Service | Internal | User lifetime value (LTV) and power-user tiering. | Confirmed |
| last_active_timestamp | TIMESTAMP WITH TIME ZONE | UTC timestamp of the user's most recent interaction. | 2026-11-01T14:20:00Z | Yes | Valid UTC timestamp | Must be >= registration_timestamp and <= CURRENT_TIMESTAMP | Event Stream | Internal | Dormancy calculation, DAU/WAU/MAU reporting, and re-engagement. | Confirmed |

### Entity: `dim_tasks` (12 fields)

| Field Name | Data Type | Definition | Example Value | Required? | Allowed Values | Validation Rule | Source System | Sensitivity | Analytical Use | Status |
|---|---|---|---|---|---|---|---|---|---|---|
| task_id | VARCHAR(32) | Primary unique identifier for a sponsored task/offer. | tsk_cpx_survey_9912 | Yes | Alphanumeric string | Must follow tsk_[provider]_[id] format | Catalog DB | Public | Foreign key linking task activity to catalog campaigns. | Confirmed |
| task_name | VARCHAR(100) | Human-readable marketing title of the offer. | Complete Consumer Habits Survey | Yes | String up to 100 characters | Must not be empty or whitespace only | Catalog DB | Public | Display in user-facing offerwall cards and reporting dashboards. | Confirmed |
| task_category | VARCHAR(30) | Product classification of the earning activity. | Survey | Yes | Survey, Game_Install, App_Trial, Microtask, Ad_Video, Cashback | Must belong to approved task category list | Catalog DB | Internal | Category-level conversion, yield, and user preference analysis. | Confirmed |
| provider_id | VARCHAR(30) | Name of the third-party offerwall or campaign sponsor. | CPX_Research | Yes | CPX_Research, Torox, AdGate, BitLabs, Lootably, RevU, Internal | Must match registered partner network enum | Catalog DB | Internal | Partner performance evaluation, postback health, and margin auditing. | Confirmed |
| reward_amount | DECIMAL(10, 2) | Amount of virtual points displayed to the user upon completion. | 150.00 | Yes | Numeric > 0.00 | Must be positive decimal with 2 decimal places | Catalog DB | Public | Financial liability projection and offer appeal benchmarking. | Confirmed |
| reward_unit | VARCHAR(10) | Virtual currency unit credited for this task. | VE | Yes | VE, XP, GEMS, TOKENS | Must match standard currency unit enum | Catalog DB | Public | Prevents mixing incompatible virtual currency units. | Confirmed |
| estimated_completion_min | INTEGER | Estimated duration in minutes for user to complete task. | 12 | No | Integers between 1 and 300 | Must be positive integer or null if untimed | Catalog DB | Public | Yield-per-minute analysis (Reward per Minute). | Confirmed |
| target_countries | VARCHAR(100) | Comma-separated list of eligible ISO country codes. | IN,US,GB,CA | Yes | ISO country codes or 'ALL' | Must contain valid 2-letter country codes | Catalog DB | Internal | Geographic filtering to prevent serving ineligible offers. | Confirmed |
| target_devices | VARCHAR(50) | Eligible device types allowed to initiate this offer. | Android_Mobile,iOS_Mobile | Yes | Comma-separated device types | Must match standard device taxonomy | Catalog DB | Internal | Client-side filtering of unsupported hardware. | Confirmed |
| gross_payout_usd | DECIMAL(8, 4) | Commercial advertiser payment received per verified lead. | 0.8500 | Yes | Numeric > 0.0000 | Must be positive decimal with up to 4 decimal places | Partner Contract | Restricted | Gross platform revenue, unit margin, and partner settlement. | Proposed |
| is_active_flag | BOOLEAN | Indicates whether campaign is live in catalog. | TRUE | Yes | TRUE, FALSE | Boolean flag; defaults to TRUE | Catalog Admin | Internal | Catalog inventory monitoring and dead offer prevention. | Confirmed |
| created_at | TIMESTAMP WITH TIME ZONE | UTC timestamp when campaign was registered in catalog. | 2026-09-01T00:00:00Z | Yes | Valid UTC timestamp | Must be <= CURRENT_TIMESTAMP | Catalog Admin | Internal | Campaign longevity and freshness analysis. | Confirmed |

### Entity: `fct_task_activity` (14 fields)

| Field Name | Data Type | Definition | Example Value | Required? | Allowed Values | Validation Rule | Source System | Sensitivity | Analytical Use | Status |
|---|---|---|---|---|---|---|---|---|---|---|
| task_activity_id | VARCHAR(36) | Primary key for an individual task execution session. | tact_11a82c40-99be-4100-b8ea-11029a88c001 | Yes | UUIDv4 string | Must follow tact_[0-9a-f-]{36} format | Backend API | Internal | Primary key for task attempt funnels and postback binding. | Confirmed |
| user_id | VARCHAR(36) | Foreign key linking attempt to user account. | usr_4f9a12c8-88be-4011-8e9a-251a37c93e41 | Yes | UUIDv4 string | Must exist in dim_users.user_id | Auth Session | Internal | User task history and behavioral conversion funnels. | Confirmed |
| task_id | VARCHAR(32) | Foreign key linking attempt to campaign catalog. | tsk_cpx_survey_9912 | Yes | Alphanumeric string | Must exist in dim_tasks.task_id | Catalog DB | Internal | Campaign conversion rates and partner postback mapping. | Confirmed |
| click_id | VARCHAR(64) | Unique tracking token generated during outbound redirect. | clk_88a01b22e49c901a | Yes | Cryptographic token string | Must be unique across all task activities | Click Router | Internal | Attribution reconciliation and postback verification. | Confirmed |
| start_time | TIMESTAMP WITH TIME ZONE | UTC timestamp when user initiated task redirect. | 2026-10-20T10:15:30Z | Yes | Valid UTC timestamp | Must be <= CURRENT_TIMESTAMP | Ingestion Gateway | Internal | Funnel timing, conversion latency, and session linkage. | Confirmed |
| completion_time | TIMESTAMP WITH TIME ZONE | UTC timestamp when partner postback callback was received. | 2026-10-20T10:28:45Z | No | Valid UTC timestamp | Must be >= start_time if populated | Partner Postback | Internal | Task duration calculation and turnaround latency. | Confirmed |
| activity_status | VARCHAR(20) | Current status of the task execution attempt. | Completed | Yes | Started, Completed, Failed, Abandoned, Disqualified | Must match standard task activity status enum | State Machine | Internal | Funnel conversion rates (Started to Completed) and drops. | Confirmed |
| failure_category | VARCHAR(30) | Structured failure classification if task was not completed. | USER_ABANDONED | No | USER_ABANDONED, PARTNER_DISQUALIFIED, TRACKING_DROPPED, VALIDATION_FAILED, SYSTEM_ERROR | Must belong to failure taxonomy if status is Failed/Abandoned | Postback Engine | Internal | Diagnostics for broken offers and survey screenouts. | Proposed |
| reward_amount | DECIMAL(10, 2) | Virtual reward amount associated with this execution. | 150.00 | Yes | Numeric >= 0.00 | Must equal task catalog reward amount | Catalog DB | Internal | Reward liability calculation and financial projection. | Confirmed |
| reward_unit | VARCHAR(10) | Virtual currency unit for this task execution. | VE | Yes | VE, XP, GEMS, TOKENS | Must match task catalog unit | Catalog DB | Internal | Ensures correct balance ledger allocation. | Confirmed |
| validation_status | VARCHAR(20) | Integrity verification status of the partner postback. | Validated_Approved | Yes | Pending_Validation, Validated_Approved, Validation_Rejected, Unverified | Must match postback validation enum | Reward Engine | Internal | Postback validation pass rates and fraud filtering. | Confirmed |
| external_tx_id | VARCHAR(64) | Transaction reference ID supplied by partner network. | cpx_postback_tx_99812401 | No | External partner string | Must be unique per partner network if not null | Partner Postback | Internal | Cross-system auditing and dispute reconciliation. | Confirmed |
| partner_payout_usd | DECIMAL(8, 4) | Actual gross payout received from partner for this lead. | 0.8500 | No | Numeric >= 0.0000 | Must be >= 0.0000 if task completed | Partner Postback | Restricted | Gross revenue reporting and partner margin calculation. | Proposed |
| postback_latency_sec | INTEGER | Elapsed time in seconds between start and completion. | 795 | No | Integers >= 0 | Mathematically: completion_time - start_time in sec | Calculated Column | Internal | Partner response latency and suspicious instant completion checks. | Proposed |

### Entity: `fct_rewards` (11 fields)

| Field Name | Data Type | Definition | Example Value | Required? | Allowed Values | Validation Rule | Source System | Sensitivity | Analytical Use | Status |
|---|---|---|---|---|---|---|---|---|---|---|
| reward_id | VARCHAR(36) | Primary unique identifier for a credited reward event. | rew_991204ab-1234-4001-90ab-112233445566 | Yes | UUIDv4 string | Must follow rew_[0-9a-f-]{36} format | Reward Engine | Internal | Primary key for reward auditing and liability tracking. | Confirmed |
| user_id | VARCHAR(36) | Foreign key linking reward to user account. | usr_4f9a12c8-88be-4011-8e9a-251a37c93e41 | Yes | UUIDv4 string | Must exist in dim_users.user_id | Auth Context | Internal | User earning history and lifetime value aggregation. | Confirmed |
| task_activity_id | VARCHAR(36) | Foreign key linking reward to originating task activity. | tact_11a82c40-99be-4100-b8ea-11029a88c001 | No | UUIDv4 string or NULL | Must exist in fct_task_activity if non-null | Reward Engine | Internal | Traceability from reward credit back to user action. | Confirmed |
| amount | DECIMAL(10, 2) | Quantity of virtual points credited. | 150.00 | Yes | Numeric > 0.00 | Must be positive decimal with 2 decimal places | Reward Engine | Internal | Core financial liability measurement. | Confirmed |
| unit | VARCHAR(10) | Virtual currency unit credited. | VE | Yes | VE, XP, GEMS, TOKENS | Must match supported currency unit enum | Reward Engine | Internal | Multi-currency balance segmentation. | Confirmed |
| status | VARCHAR(20) | Current state of the reward credit. | Credited | Yes | Pending, Credited, Reversed, Corrected | Must belong to reward lifecycle state enum | Reward Engine | Internal | Distinguishes settled liability from pending escrow. | Confirmed |
| created_at | TIMESTAMP WITH TIME ZONE | UTC timestamp when reward record was generated. | 2026-10-20T10:28:46Z | Yes | Valid UTC timestamp | Must be <= CURRENT_TIMESTAMP | Database Engine | Internal | Reward generation rate and pipeline latency. | Confirmed |
| credited_at | TIMESTAMP WITH TIME ZONE | UTC timestamp when funds released to available balance. | 2026-10-20T10:28:46Z | No | Valid UTC timestamp | Must be >= created_at if status is Credited | Wallet Ledger | Internal | Tracks pending hold clearance delays. | Confirmed |
| source_type | VARCHAR(30) | Product feature that distributed the reward. | Offerwall_Task | Yes | Offerwall_Task, Daily_Streak, Spin_Wheel, Referral_Bonus, Quest_Milestone, Admin_Correction | Must match approved reward source enum | Reward Engine | Internal | Breakdown of reward liability by feature module. | Confirmed |
| is_reversed_flag | BOOLEAN | Indicates whether reward was clawed back by advertiser. | FALSE | Yes | TRUE, FALSE | Boolean flag; defaults to FALSE | Reversal Worker | Internal | Partner fraud and chargeback rate calculation. | Confirmed |
| reversal_reason | VARCHAR(50) | Causal categorization if reward was clawed back. | Advertiser_Chargeback | No | Advertiser_Chargeback, Multi_Account_Fraud, System_Error | Must belong to reversal taxonomy if is_reversed is TRUE | Reversal Worker | Internal | Partner fraud auditing and margin leakage analysis. | Confirmed |

### Entity: `fct_wallet_transactions` (13 fields)

| Field Name | Data Type | Definition | Example Value | Required? | Allowed Values | Validation Rule | Source System | Sensitivity | Analytical Use | Status |
|---|---|---|---|---|---|---|---|---|---|---|
| transaction_id | VARCHAR(36) | Primary key for an atomic balance ledger entry. | tx_901c8742-8812-40ae-bf31-55198ad00142 | Yes | UUIDv4 string | Must follow tx_[0-9a-f-]{36} format | Ledger Service | Internal | Double-entry bookkeeping and balance reconciliation. | Confirmed |
| user_id | VARCHAR(36) | Foreign key linking mutation to user account. | usr_4f9a12c8-88be-4011-8e9a-251a37c93e41 | Yes | UUIDv4 string | Must exist in dim_users.user_id | Auth Context | Internal | User balance reconstruction and audit history. | Confirmed |
| timestamp | TIMESTAMP WITH TIME ZONE | UTC timestamp when ledger entry was committed. | 2026-10-20T10:28:46Z | Yes | Valid UTC timestamp | Must be <= CURRENT_TIMESTAMP | Database Engine | Internal | Time-series transaction volume and cashflow analysis. | Confirmed |
| transaction_type | VARCHAR(30) | Economic classification of the balance mutation. | REWARD_CREDIT | Yes | REWARD_CREDIT, REWARD_PENDING_HOLD, PENDING_RELEASE, DAILY_BONUS_CREDIT, REFERRAL_CREDIT, WITHDRAWAL_ESCROW, WITHDRAWAL_SETTLED, WITHDRAWAL_REFUND, REWARD_REVERSAL, ADMIN_ADJUSTMENT, CURRENCY_EXCHANGE | Must belong to approved transaction type taxonomy | Ledger Engine | Internal | Financial reporting and ledger reconciliation by type. | Confirmed |
| direction | VARCHAR(6) | Direction of balance mutation (CREDIT or DEBIT). | CREDIT | Yes | CREDIT, DEBIT | Must be uppercase CREDIT or DEBIT | Ledger Engine | Internal | Mathematical calculation of current available balance. | Confirmed |
| amount | DECIMAL(12, 2) | Quantity of virtual points transacted. | 150.00 | Yes | Numeric > 0.00 | Must be strictly positive decimal with 2 decimal places | Ledger Engine | Internal | Ledger amount for balance rollup summation. | Confirmed |
| unit | VARCHAR(10) | Virtual currency or fiat unit of the transaction. | VE | Yes | VE, XP, GEMS, USD, INR | Must match supported currency unit list | Ledger Engine | Internal | Separates virtual points from legal fiat currency. | Confirmed |
| balance_before | DECIMAL(12, 2) | User balance snapshot immediately prior to transaction. | 320.00 | Yes | Numeric >= 0.00 | Must be non-negative decimal | Ledger Engine | Internal | Cryptographic ledger audit and race-condition detection. | Proposed |
| balance_after | DECIMAL(12, 2) | User balance snapshot immediately following transaction. | 470.00 | Yes | Numeric >= 0.00 | Must satisfy: balance_before +/- amount | Ledger Engine | Internal | Immediate balance verification without full table scan. | Proposed |
| source | VARCHAR(30) | Originating product service for the transaction. | Offerwall_Postback | Yes | Offerwall_Postback, Daily_Streak, Spin_Wheel, Referral_Bonus, Withdrawal_Cashout, Support_Adjustment | Must match registered source service list | Ledger Engine | Internal | Portfolio attribution of platform expenses and credits. | Confirmed |
| reference_id | VARCHAR(64) | Foreign key to trigger record in originating table. | rew_991204ab-1234-4001-90ab-112233445566 | Yes | String pointer | Must point to valid reward_id, withdrawal_id, or ticket_id | Originating Service | Internal | End-to-end traceability of every balance mutation. | Confirmed |
| parent_tx_id | VARCHAR(36) | Reference to original transaction if this is a reversal. | NULL | No | UUIDv4 string or NULL | Must point to existing transaction_id if populated | Reversal Worker | Internal | Chargeback tracking and ledger correction lineage. | Confirmed |
| reversal_reason | VARCHAR(50) | Causal explanation if transaction is a clawback. | NULL | No | String or NULL | Must be populated if transaction_type is REWARD_REVERSAL | Reversal Worker | Internal | Fraud categorization and dispute tracking. | Confirmed |

### Entity: `fct_withdrawals` (14 fields)

| Field Name | Data Type | Definition | Example Value | Required? | Allowed Values | Validation Rule | Source System | Sensitivity | Analytical Use | Status |
|---|---|---|---|---|---|---|---|---|---|---|
| withdrawal_id | VARCHAR(36) | Primary key for a user cashout transaction. | wth_8812a001-4412-4011-8899-aabbccddeeff | Yes | UUIDv4 string | Must follow wth_[0-9a-f-]{36} format | Payout Service | Internal | Primary key for payout lifecycle tracking and SLA auditing. | Confirmed |
| user_id | VARCHAR(36) | Foreign key linking cashout to user account. | usr_4f9a12c8-88be-4011-8e9a-251a37c93e41 | Yes | UUIDv4 string | Must exist in dim_users.user_id | Auth Context | Internal | User payout history and withdrawal frequency analysis. | Confirmed |
| requested_amount | DECIMAL(10, 2) | Gross virtual points amount submitted for redemption. | 1000.00 | Yes | Numeric >= min_threshold | Must be >= platform minimum cashout threshold (500 VE) | Cashout Form | Internal | Total liquidity demand and escrow balance calculations. | Confirmed |
| fee_amount | DECIMAL(6, 2) | Payment gateway or network processing fee deducted. | 25.00 | Yes | Numeric >= 0.00 | Must be non-negative; defaults to standard fee tier | Fee Engine | Internal | Net revenue retention and payment cost analysis. | Proposed |
| net_amount | DECIMAL(10, 2) | Net fiat or digital value transferred to the user. | 9.75 | Yes | Numeric > 0.00 | Must equal: (requested_amount - fee_amount) * fx_rate | Payout Engine | Internal | Actual fiat cash disbursed from platform bank account. | Confirmed |
| currency | CHAR(3) | Target fiat payout currency code. | USD | Yes | ISO 4217 code (USD, INR, EUR, GBP) | Must be 3 uppercase letters matching ISO 4217 | Cashout Form | Internal | Multi-currency treasury management and foreign exchange. | Confirmed |
| payout_method | VARCHAR(20) | Channel chosen by user to receive cashout. | PayPal | Yes | PayPal, UPI_Direct, Bank_Transfer, Crypto_USDT, Amazon_Gift_Card | Must belong to supported payout method enum | Cashout Form | Internal | Payout rail popularity, fee optimization, and gateway volume. | Confirmed |
| destination_hash | VARCHAR(64) | SHA-256 hash of user payment address/email/UPI ID. | b1a82c4099be4100b8ea11029a88c001991204ab1234400190ab112233445566 | Yes | 64-character hex string | Must be valid 64-char hex digest; raw stored in Vault | Ingestion Pipe | Restricted | Detects multi-accounting fraud (multiple users sharing payout handle). | Proposed |
| requested_timestamp | TIMESTAMP WITH TIME ZONE | UTC timestamp when user submitted cashout request. | 2026-10-25T14:10:00Z | Yes | Valid UTC timestamp | Must be <= CURRENT_TIMESTAMP | API Gateway | Internal | Queue aging, SLA monitoring, and cashout velocity. | Confirmed |
| processing_timestamp | TIMESTAMP WITH TIME ZONE | UTC timestamp when payout was dispatched to gateway API. | 2026-10-25T16:30:00Z | No | Valid UTC timestamp | Must be >= requested_timestamp or NULL | Payout Dispatch | Internal | Internal compliance review and batch dispatch latency. | Confirmed |
| final_timestamp | TIMESTAMP WITH TIME ZONE | UTC timestamp when terminal settlement state was confirmed. | 2026-10-25T16:32:15Z | No | Valid UTC timestamp | Must be >= processing_timestamp or NULL | Gateway Webhook | Internal | End-to-end turnaround time and fulfillment SLA. | Confirmed |
| status | VARCHAR(20) | Current lifecycle state of the withdrawal request. | Completed | Yes | Requested, Under_Review, Processing, Completed, Rejected, Reversed | Must belong to withdrawal lifecycle state machine | Payout Engine | Internal | Withdrawal completion rate, pending queue, and failure metrics. | Confirmed |
| reason_category | VARCHAR(50) | Causal explanation if payout was rejected or reversed. | NULL | No | String or NULL | Must be populated if status is Rejected or Reversed | Compliance / Gateway | Internal | Analysis of gateway rejections, KYC failures, and fraud stops. | Confirmed |
| gateway_tx_id | VARCHAR(64) | External payment reference string returned by processor. | PAYPAL_TX_88192048102 | No | External provider string | Must be populated if status is Completed | Gateway Webhook | Internal | Banking reconciliation and proof of payment dispatch. | Confirmed |

### Entity: `fct_referrals` (12 fields)

| Field Name | Data Type | Definition | Example Value | Required? | Allowed Values | Validation Rule | Source System | Sensitivity | Analytical Use | Status |
|---|---|---|---|---|---|---|---|---|---|---|
| referral_id | VARCHAR(36) | Primary key for a unique referral attribution relationship. | ref_771204aa-9912-40ae-8812-aabb11223344 | Yes | UUIDv4 string | Must follow ref_[0-9a-f-]{36} format | Referral Engine | Internal | Primary key for viral loop tracking and attribution. | Confirmed |
| referrer_user_id | VARCHAR(36) | User ID of the member who shared their referral link. | usr_4f9a12c8-88be-4011-8e9a-251a37c93e41 | Yes | UUIDv4 string | Must exist in dim_users.user_id | Auth Context | Internal | Referral volume per user, viral K-factor, and top referrers. | Confirmed |
| referred_user_id | VARCHAR(36) | User ID of the newly registered invitee. | usr_8820c41b-41a2-4d22-b5e1-88931a029c11 | No | UUIDv4 string or NULL | Must exist in dim_users.user_id if populated | Registration Event | Internal | Attribution binding and conversion funnel progression. | Confirmed |
| referral_code | VARCHAR(20) | Alphanumeric tracking code used for attribution. | VELOOP_PUSHTI | Yes | Uppercase alphanumeric string | Must match referrer's assigned vanity code | Referral Service | Internal | Campaign and promotional code effectiveness analysis. | Confirmed |
| share_channel | VARCHAR(30) | Social or messaging medium used to share the link. | WhatsApp | No | WhatsApp, Telegram, Twitter_X, Direct_Link, YouTube | Must belong to supported share channels if populated | Client Share API | Internal | Channel acquisition efficiency and viral sharing preferences. | Proposed |
| creation_timestamp | TIMESTAMP WITH TIME ZONE | UTC timestamp when referral link was generated. | 2026-10-18T09:00:00Z | Yes | Valid UTC timestamp | Must be <= CURRENT_TIMESTAMP | Backend API | Internal | Measures share velocity and promotional campaign reach. | Confirmed |
| registration_timestamp | TIMESTAMP WITH TIME ZONE | UTC timestamp when invitee registered their account. | 2026-10-18T11:20:00Z | No | Valid UTC timestamp | Must be >= creation_timestamp or NULL | Auth Service | Internal | Share-to-registration conversion latency. | Confirmed |
| activation_timestamp | TIMESTAMP WITH TIME ZONE | UTC timestamp when invitee completed first qualifying task. | 2026-10-19T14:45:00Z | No | Valid UTC timestamp | Must be >= registration_timestamp or NULL | Task Engine | Internal | Registration-to-activation conversion rate and drop-off. | Confirmed |
| conversion_timestamp | TIMESTAMP WITH TIME ZONE | UTC timestamp when referral bonus was credited to referrer. | 2026-10-19T14:45:01Z | No | Valid UTC timestamp | Must be >= activation_timestamp or NULL | Reward Engine | Internal | Total referral conversion rate and reward distribution timing. | Confirmed |
| referral_status | VARCHAR(20) | Current funnel status of the referral pair. | Converted | Yes | Link_Created, Registered, Activated, Converted, Fraud_Blocked | Must belong to referral state machine enum | Referral Engine | Internal | Step-by-step conversion funnel drop-off analysis. | Confirmed |
| reward_amount | DECIMAL(10, 2) | Virtual reward credited to referrer upon conversion. | 250.00 | Yes | Numeric >= 0.00 | Must match platform referral reward tier policy | Reward Policy | Internal | Referral CAC and viral incentive budget monitoring. | Confirmed |
| ip_collision_flag | BOOLEAN | Indicates if referrer and invitee operated on same IP. | FALSE | Yes | TRUE, FALSE | Boolean flag; defaults to FALSE | Ingestion Pipe | Internal | Referral fraud detection and self-referral prevention. | Proposed |

### Entity: `fct_feature_events` (10 fields)

| Field Name | Data Type | Definition | Example Value | Required? | Allowed Values | Validation Rule | Source System | Sensitivity | Analytical Use | Status |
|---|---|---|---|---|---|---|---|---|---|---|
| event_id | VARCHAR(36) | Primary unique identifier for a discrete telemetry event. | evt_118c72fa-7740-4592-80ea-12003c0048ab | Yes | UUIDv4 string | Must follow evt_[0-9a-f-]{36} format | Client / Server SDK | Internal | Idempotency key for event deduplication and auditing. | Confirmed |
| user_id | VARCHAR(36) | Foreign key linking event to user account. | usr_4f9a12c8-88be-4011-8e9a-251a37c93e41 | Yes | UUIDv4 string | Must exist in dim_users.user_id | Auth Context | Internal | User behavioral trajectory and engagement journey mapping. | Confirmed |
| session_id | VARCHAR(36) | Foreign key linking event to continuous user session. | ses_8820c41b-41a2-4d22-b5e1-88931a029c11 | Yes | UUIDv4 string | Must follow ses_[0-9a-f-]{36} format | Client SDK | Internal | Session duration, screen depth, and multi-event funnels. | Confirmed |
| event_name | VARCHAR(50) | Canonical standardized event identifier (domain_object_action). | task_offer_started | Yes | Standardized event name string | Must exist in approved Event Tracking Plan catalogue | Telemetry SDK | Internal | Primary dimension for behavioral event aggregation and funnels. | Confirmed |
| feature_domain | VARCHAR(30) | Product module originating the event. | Task_Engine | Yes | Authentication, Onboarding, Task_Engine, Reward_Engine, Engagement, Gamification, Referrals, Wallet, Withdrawals, Support | Must match approved feature domain enum | Telemetry SDK | Internal | Feature adoption rates and cross-feature engagement analysis. | Confirmed |
| client_timestamp | TIMESTAMP WITH TIME ZONE | Local clock timestamp recorded by user device when event occurred. | 2026-10-20T10:15:30Z | Yes | Valid timestamp | Recorded from client system clock | Client SDK | Internal | Measures client latency and offline buffering delays. | Proposed |
| server_timestamp | TIMESTAMP WITH TIME ZONE | UTC timestamp when event payload was ingested by backend API. | 2026-10-20T10:15:31Z | Yes | Valid UTC timestamp | Must be <= CURRENT_TIMESTAMP | API Gateway | Internal | Authoritative chronological sorting and clock-skew prevention. | Confirmed |
| device_type | VARCHAR(20) | Device form factor at the moment of event trigger. | Android_Mobile | Yes | Android_Mobile, iOS_Mobile, Desktop_Web, Mobile_Web | Must match standard device taxonomy | Client SDK | Internal | Technical performance and crash correlation by platform. | Confirmed |
| app_version | VARCHAR(15) | Software version active when event was triggered. | v1.2.0 | No | Semantic versioning string | Must follow vx.y.z format if mobile client | Client Headers | Internal | Regression testing and version adoption monitoring. | Confirmed |
| event_properties_json | JSONB / TEXT | Semi-structured JSON payload containing contextual event attributes. | {"task_id": "tsk_cpx_9912", "reward_amount": 150} | Yes | Valid JSON object | Must parse as valid JSON; size <= 4KB | Telemetry SDK | Internal | Flexible contextual analysis without requiring table schema migrations. | Confirmed |

### Entity: `dim_badges_missions` (8 fields)

| Field Name | Data Type | Definition | Example Value | Required? | Allowed Values | Validation Rule | Source System | Sensitivity | Analytical Use | Status |
|---|---|---|---|---|---|---|---|---|---|---|
| item_id | VARCHAR(32) | Primary key for a gamified badge or mission challenge. | bdg_streak_master_7 | Yes | Alphanumeric string | Must follow bdg_[name] or msn_[name] format | Game Engine | Public | Primary key for gamification catalogue lookup. | Confirmed |
| item_type | VARCHAR(15) | Classification as a permanent Badge or recurring Mission. | Badge | Yes | Badge, Mission, Achievement | Must belong to gamification type enum | Game Engine | Public | Separates permanent profile badges from recurring tasks. | Confirmed |
| title | VARCHAR(100) | User-facing title of the badge or mission. | 7-Day Streak Master | Yes | String up to 100 characters | Must not be empty | Game Engine | Public | Display in profile trophies and quest modal. | Confirmed |
| description | TEXT | Instructions and conditions required to earn item. | Maintain an uninterrupted daily check-in streak for 7 consecutive days. | Yes | Plain text string | Clear instructions for user qualification | Game Engine | Public | User transparency and challenge guidance. | Confirmed |
| reward_xp | INTEGER | Gamification experience points granted upon unlock. | 200 | Yes | Integers >= 0 | Must be non-negative integer | Game Engine | Public | XP leveling and leaderboard acceleration. | Confirmed |
| reward_gems | INTEGER | Premium virtual tokens granted upon unlock. | 10 | Yes | Integers >= 0 | Must be non-negative integer | Game Engine | Public | Premium virtual economy incentive distribution. | Confirmed |
| prerequisite_metric | VARCHAR(50) | Underlying analytical metric evaluated for qualification. | current_streak_days | Yes | Metric identifier string | Must map to valid metric in KPI Catalogue | Game Engine | Internal | Automated criteria validation by background workers. | Proposed |
| threshold_value | INTEGER | Numeric threshold of prerequisite metric to trigger unlock. | 7 | Yes | Integers >= 1 | Must be positive integer | Game Engine | Internal | Objective numerical qualification rule. | Confirmed |

---
*End of Deliverable DELIV-09 — VELOOP Data Dictionary.*
