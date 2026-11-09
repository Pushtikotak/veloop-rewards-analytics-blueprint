-- ============================================================================
-- VELOOP REWARDS — LOGICAL DATA MODEL (ANSI / POSTGRESQL DDL)
-- Project: Product Analytics, Data Readiness & Data Management Blueprint
-- Deliverable Code: DELIV-10 (Work Package H)
-- Author / Analyst: Pushti Kotak
-- Classification: Internal Technical Architecture / Relational Schema
-- Date: 02 November 2026
-- Notice: SIMULATED DATA TEST PROTOCOL — Production Blueprint
-- ============================================================================

-- Drop tables in reverse topological order if rebuilding
DROP TABLE IF EXISTS fct_support_tickets CASCADE;
DROP TABLE IF EXISTS map_user_badges CASCADE;
DROP TABLE IF EXISTS dim_badges_missions CASCADE;
DROP TABLE IF EXISTS fct_feature_events CASCADE;
DROP TABLE IF EXISTS fct_referrals CASCADE;
DROP TABLE IF EXISTS fct_withdrawals CASCADE;
DROP TABLE IF EXISTS fct_wallet_transactions CASCADE;
DROP TABLE IF EXISTS fct_rewards CASCADE;
DROP TABLE IF EXISTS fct_task_activity CASCADE;
DROP TABLE IF EXISTS dim_tasks CASCADE;
DROP TABLE IF EXISTS dim_users CASCADE;

-- ============================================================================
-- 1. DIMENSION: dim_users
-- Canonical entity representing registered VELOOP user accounts.
-- ============================================================================
CREATE TABLE dim_users (
    user_id                     VARCHAR(36) PRIMARY KEY,
    account_status              VARCHAR(20) NOT NULL DEFAULT 'Registered' 
                                CHECK (account_status IN ('Registered', 'Onboarded', 'Active', 'Dormant', 'Churned', 'Suspended', 'Banned')),
    registration_timestamp      TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT CURRENT_TIMESTAMP,
    registration_source         VARCHAR(50) NOT NULL DEFAULT 'Organic_Search'
                                CHECK (registration_source IN ('Organic_Search', 'Direct', 'Google_Ads', 'Meta_Ads', 'Referral_Program', 'Influencer')),
    referral_code_used          VARCHAR(20) NULL,
    auth_provider               VARCHAR(20) NOT NULL DEFAULT 'Email_Password'
                                CHECK (auth_provider IN ('Email_Password', 'Google_OAuth', 'Apple_ID', 'Telegram')),
    country_code                CHAR(2) NOT NULL,
    signup_device_type          VARCHAR(20) NOT NULL DEFAULT 'Android_Mobile'
                                CHECK (signup_device_type IN ('Android_Mobile', 'iOS_Mobile', 'Desktop_Web', 'Mobile_Web')),
    signup_app_version          VARCHAR(15) NULL,
    signup_ip_hash              VARCHAR(64) NOT NULL,
    email_verified_flag         BOOLEAN NOT NULL DEFAULT FALSE,
    onboarding_completed_flag   BOOLEAN NOT NULL DEFAULT FALSE,
    onboarding_completed_at     TIMESTAMP WITH TIME ZONE NULL,
    current_level               INTEGER NOT NULL DEFAULT 1 CHECK (current_level >= 1),
    total_xp                    INTEGER NOT NULL DEFAULT 0 CHECK (total_xp >= 0),
    current_streak_days         INTEGER NOT NULL DEFAULT 0 CHECK (current_streak_days >= 0),
    lifetime_ve_earned          DECIMAL(12, 2) NOT NULL DEFAULT 0.00 CHECK (lifetime_ve_earned >= 0.00),
    lifetime_usd_withdrawn      DECIMAL(10, 2) NOT NULL DEFAULT 0.00 CHECK (lifetime_usd_withdrawn >= 0.00),
    last_active_timestamp       TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT CURRENT_TIMESTAMP,
    last_login_device           VARCHAR(50) NULL,
    
    CONSTRAINT chk_onboarding_dates CHECK (onboarding_completed_at IS NULL OR onboarding_completed_at >= registration_timestamp)
);

CREATE INDEX idx_users_status_country ON dim_users(account_status, country_code);
CREATE INDEX idx_users_last_active ON dim_users(last_active_timestamp);

-- ============================================================================
-- 2. DIMENSION: dim_tasks
-- Campaign catalog defining earning opportunities, rewards, and rate cards.
-- ============================================================================
CREATE TABLE dim_tasks (
    task_id                     VARCHAR(32) PRIMARY KEY,
    task_name                   VARCHAR(100) NOT NULL,
    task_category               VARCHAR(30) NOT NULL 
                                CHECK (task_category IN ('Survey', 'Game_Install', 'App_Trial', 'Microtask', 'Ad_Video', 'Cashback')),
    provider_id                 VARCHAR(30) NOT NULL 
                                CHECK (provider_id IN ('CPX_Research', 'Torox', 'AdGate', 'BitLabs', 'Lootably', 'RevU', 'Internal')),
    reward_amount               DECIMAL(10, 2) NOT NULL CHECK (reward_amount > 0.00),
    reward_unit                 VARCHAR(10) NOT NULL DEFAULT 'VE'
                                CHECK (reward_unit IN ('VE', 'XP', 'GEMS', 'TOKENS')),
    estimated_completion_min    INTEGER NULL CHECK (estimated_completion_min IS NULL OR estimated_completion_min > 0),
    target_countries            VARCHAR(100) NOT NULL DEFAULT 'ALL',
    target_devices              VARCHAR(50) NOT NULL DEFAULT 'ALL',
    gross_payout_usd            DECIMAL(8, 4) NOT NULL CHECK (gross_payout_usd > 0.0000),
    is_active_flag              BOOLEAN NOT NULL DEFAULT TRUE,
    created_at                  TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_tasks_provider_cat ON dim_tasks(provider_id, task_category);

-- ============================================================================
-- 3. FACT: fct_task_activity
-- Individual execution attempts by users to complete catalog tasks.
-- ============================================================================
CREATE TABLE fct_task_activity (
    task_activity_id            VARCHAR(36) PRIMARY KEY,
    user_id                     VARCHAR(36) NOT NULL REFERENCES dim_users(user_id) ON DELETE RESTRICT,
    task_id                     VARCHAR(32) NOT NULL REFERENCES dim_tasks(task_id) ON DELETE RESTRICT,
    click_id                    VARCHAR(64) NOT NULL UNIQUE,
    start_time                  TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT CURRENT_TIMESTAMP,
    completion_time             TIMESTAMP WITH TIME ZONE NULL,
    activity_status             VARCHAR(20) NOT NULL DEFAULT 'Started'
                                CHECK (activity_status IN ('Started', 'Completed', 'Failed', 'Abandoned', 'Disqualified')),
    failure_category            VARCHAR(30) NULL
                                CHECK (failure_category IS NULL OR failure_category IN ('USER_ABANDONED', 'PARTNER_DISQUALIFIED', 'TRACKING_DROPPED', 'VALIDATION_FAILED', 'SYSTEM_ERROR')),
    reward_amount               DECIMAL(10, 2) NOT NULL CHECK (reward_amount >= 0.00),
    reward_unit                 VARCHAR(10) NOT NULL DEFAULT 'VE',
    validation_status           VARCHAR(20) NOT NULL DEFAULT 'Pending_Validation'
                                CHECK (validation_status IN ('Pending_Validation', 'Validated_Approved', 'Validation_Rejected', 'Unverified')),
    external_tx_id              VARCHAR(64) NULL,
    partner_payout_usd          DECIMAL(8, 4) NULL CHECK (partner_payout_usd IS NULL OR partner_payout_usd >= 0.0000),
    postback_latency_sec        INTEGER NULL CHECK (postback_latency_sec IS NULL OR postback_latency_sec >= 0),
    
    CONSTRAINT chk_task_times CHECK (completion_time IS NULL OR completion_time >= start_time)
);

CREATE INDEX idx_task_act_user_time ON fct_task_activity(user_id, start_time);
CREATE INDEX idx_task_act_status ON fct_task_activity(activity_status, validation_status);

-- ============================================================================
-- 4. FACT: fct_rewards
-- Formal financial incentive records generated across all product features.
-- ============================================================================
CREATE TABLE fct_rewards (
    reward_id                   VARCHAR(36) PRIMARY KEY,
    user_id                     VARCHAR(36) NOT NULL REFERENCES dim_users(user_id) ON DELETE RESTRICT,
    task_activity_id            VARCHAR(36) NULL REFERENCES fct_task_activity(task_activity_id) ON DELETE RESTRICT,
    amount                      DECIMAL(10, 2) NOT NULL CHECK (amount > 0.00),
    unit                        VARCHAR(10) NOT NULL DEFAULT 'VE'
                                CHECK (unit IN ('VE', 'XP', 'GEMS', 'TOKENS')),
    status                      VARCHAR(20) NOT NULL DEFAULT 'Credited'
                                CHECK (status IN ('Pending', 'Credited', 'Reversed', 'Corrected')),
    created_at                  TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT CURRENT_TIMESTAMP,
    credited_at                 TIMESTAMP WITH TIME ZONE NULL,
    source_type                 VARCHAR(30) NOT NULL DEFAULT 'Offerwall_Task'
                                CHECK (source_type IN ('Offerwall_Task', 'Daily_Streak', 'Spin_Wheel', 'Referral_Bonus', 'Quest_Milestone', 'Admin_Correction')),
    is_reversed_flag            BOOLEAN NOT NULL DEFAULT FALSE,
    reversal_reason             VARCHAR(50) NULL,
    
    CONSTRAINT chk_reward_settlement CHECK (credited_at IS NULL OR credited_at >= created_at)
);

CREATE INDEX idx_rewards_user_source ON fct_rewards(user_id, source_type);
CREATE INDEX idx_rewards_status ON fct_rewards(status, created_at);

-- ============================================================================
-- 5. FACT: fct_wallet_transactions
-- Double-entry transactional ledger tracking all user balance mutations.
-- ============================================================================
CREATE TABLE fct_wallet_transactions (
    transaction_id              VARCHAR(36) PRIMARY KEY,
    user_id                     VARCHAR(36) NOT NULL REFERENCES dim_users(user_id) ON DELETE RESTRICT,
    timestamp                   TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT CURRENT_TIMESTAMP,
    transaction_type            VARCHAR(30) NOT NULL
                                CHECK (transaction_type IN ('REWARD_CREDIT', 'REWARD_PENDING_HOLD', 'PENDING_RELEASE', 'DAILY_BONUS_CREDIT', 'REFERRAL_CREDIT', 'WITHDRAWAL_ESCROW', 'WITHDRAWAL_SETTLED', 'WITHDRAWAL_REFUND', 'REWARD_REVERSAL', 'ADMIN_ADJUSTMENT', 'CURRENCY_EXCHANGE')),
    direction                   VARCHAR(6) NOT NULL CHECK (direction IN ('CREDIT', 'DEBIT')),
    amount                      DECIMAL(12, 2) NOT NULL CHECK (amount > 0.00),
    unit                        VARCHAR(10) NOT NULL DEFAULT 'VE'
                                CHECK (unit IN ('VE', 'XP', 'GEMS', 'USD', 'INR')),
    balance_before              DECIMAL(12, 2) NOT NULL CHECK (balance_before >= 0.00),
    balance_after               DECIMAL(12, 2) NOT NULL CHECK (balance_after >= 0.00),
    source                      VARCHAR(30) NOT NULL,
    reference_id                VARCHAR(64) NOT NULL,
    parent_tx_id                VARCHAR(36) NULL REFERENCES fct_wallet_transactions(transaction_id) ON DELETE RESTRICT,
    reversal_reason             VARCHAR(50) NULL
);

CREATE INDEX idx_wallet_tx_user ON fct_wallet_transactions(user_id, timestamp);
CREATE INDEX idx_wallet_tx_type ON fct_wallet_transactions(transaction_type, direction);

-- ============================================================================
-- 6. FACT: fct_withdrawals
-- Payout transactions converting virtual balance into fiat / gift cards.
-- ============================================================================
CREATE TABLE fct_withdrawals (
    withdrawal_id               VARCHAR(36) PRIMARY KEY,
    user_id                     VARCHAR(36) NOT NULL REFERENCES dim_users(user_id) ON DELETE RESTRICT,
    requested_amount            DECIMAL(10, 2) NOT NULL CHECK (requested_amount >= 500.00), -- Minimum 500 VE
    fee_amount                  DECIMAL(6, 2) NOT NULL DEFAULT 0.00 CHECK (fee_amount >= 0.00),
    net_amount                  DECIMAL(10, 2) NOT NULL CHECK (net_amount > 0.00),
    currency                    CHAR(3) NOT NULL DEFAULT 'USD',
    payout_method               VARCHAR(20) NOT NULL
                                CHECK (payout_method IN ('PayPal', 'UPI_Direct', 'Bank_Transfer', 'Crypto_USDT', 'Amazon_Gift_Card')),
    destination_hash            VARCHAR(64) NOT NULL,
    requested_timestamp         TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT CURRENT_TIMESTAMP,
    processing_timestamp        TIMESTAMP WITH TIME ZONE NULL,
    final_timestamp             TIMESTAMP WITH TIME ZONE NULL,
    status                      VARCHAR(20) NOT NULL DEFAULT 'Requested'
                                CHECK (status IN ('Requested', 'Under_Review', 'Processing', 'Completed', 'Rejected', 'Reversed')),
    reason_category             VARCHAR(50) NULL,
    gateway_tx_id               VARCHAR(64) NULL,
    
    CONSTRAINT chk_wth_dates CHECK (
        (processing_timestamp IS NULL OR processing_timestamp >= requested_timestamp) AND
        (final_timestamp IS NULL OR final_timestamp >= processing_timestamp)
    )
);

CREATE INDEX idx_withdrawals_status ON fct_withdrawals(status, requested_timestamp);
CREATE INDEX idx_withdrawals_method ON fct_withdrawals(payout_method, currency);

-- ============================================================================
-- 7. FACT: fct_referrals
-- Attribution and viral acquisition tracking connecting referrers and invitees.
-- ============================================================================
CREATE TABLE fct_referrals (
    referral_id                 VARCHAR(36) PRIMARY KEY,
    referrer_user_id            VARCHAR(36) NOT NULL REFERENCES dim_users(user_id) ON DELETE RESTRICT,
    referred_user_id            VARCHAR(36) NULL REFERENCES dim_users(user_id) ON DELETE RESTRICT,
    referral_code               VARCHAR(20) NOT NULL,
    share_channel               VARCHAR(30) NULL
                                CHECK (share_channel IS NULL OR share_channel IN ('WhatsApp', 'Telegram', 'Twitter_X', 'Direct_Link', 'YouTube')),
    creation_timestamp          TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT CURRENT_TIMESTAMP,
    registration_timestamp      TIMESTAMP WITH TIME ZONE NULL,
    activation_timestamp        TIMESTAMP WITH TIME ZONE NULL,
    conversion_timestamp        TIMESTAMP WITH TIME ZONE NULL,
    referral_status             VARCHAR(20) NOT NULL DEFAULT 'Link_Created'
                                CHECK (referral_status IN ('Link_Created', 'Registered', 'Activated', 'Converted', 'Fraud_Blocked')),
    reward_amount               DECIMAL(10, 2) NOT NULL DEFAULT 250.00 CHECK (reward_amount >= 0.00),
    reward_unit                 VARCHAR(10) NOT NULL DEFAULT 'VE',
    ip_collision_flag           BOOLEAN NOT NULL DEFAULT FALSE,
    
    CONSTRAINT chk_ref_distinct_users CHECK (referred_user_id IS NULL OR referrer_user_id != referred_user_id),
    CONSTRAINT chk_ref_dates CHECK (
        (registration_timestamp IS NULL OR registration_timestamp >= creation_timestamp) AND
        (activation_timestamp IS NULL OR activation_timestamp >= registration_timestamp) AND
        (conversion_timestamp IS NULL OR conversion_timestamp >= activation_timestamp)
    )
);

CREATE INDEX idx_referrals_referrer ON fct_referrals(referrer_user_id, referral_status);

-- ============================================================================
-- 8. FACT: fct_feature_events
-- Raw and enriched behavioral clickstream telemetry.
-- ============================================================================
CREATE TABLE fct_feature_events (
    event_id                    VARCHAR(36) PRIMARY KEY,
    user_id                     VARCHAR(36) NOT NULL REFERENCES dim_users(user_id) ON DELETE RESTRICT,
    session_id                  VARCHAR(36) NOT NULL,
    event_name                  VARCHAR(50) NOT NULL,
    feature_domain              VARCHAR(30) NOT NULL,
    client_timestamp            TIMESTAMP WITH TIME ZONE NOT NULL,
    server_timestamp            TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT CURRENT_TIMESTAMP,
    device_type                 VARCHAR(20) NOT NULL,
    app_version                 VARCHAR(15) NULL,
    event_properties_json       TEXT NOT NULL DEFAULT '{}'
);

CREATE INDEX idx_events_name_time ON fct_feature_events(event_name, server_timestamp);
CREATE INDEX idx_events_session ON fct_feature_events(session_id);

-- ============================================================================
-- 9. DIMENSION: dim_badges_missions
-- Master catalog of gamification quests, challenges, and badges.
-- ============================================================================
CREATE TABLE dim_badges_missions (
    item_id                     VARCHAR(32) PRIMARY KEY,
    item_type                   VARCHAR(15) NOT NULL CHECK (item_type IN ('Badge', 'Mission', 'Achievement')),
    title                       VARCHAR(100) NOT NULL,
    description                 TEXT NOT NULL,
    reward_xp                   INTEGER NOT NULL DEFAULT 0 CHECK (reward_xp >= 0),
    reward_gems                 INTEGER NOT NULL DEFAULT 0 CHECK (reward_gems >= 0),
    prerequisite_metric         VARCHAR(50) NOT NULL,
    threshold_value             INTEGER NOT NULL CHECK (threshold_value >= 1)
);

-- ============================================================================
-- 10. MAPPING: map_user_badges
-- User unlocked achievements and trophy flairs.
-- ============================================================================
CREATE TABLE map_user_badges (
    map_id                      VARCHAR(36) PRIMARY KEY,
    user_id                     VARCHAR(36) NOT NULL REFERENCES dim_users(user_id) ON DELETE RESTRICT,
    item_id                     VARCHAR(32) NOT NULL REFERENCES dim_badges_missions(item_id) ON DELETE RESTRICT,
    earned_at                   TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT CURRENT_TIMESTAMP,
    
    CONSTRAINT uq_user_badge UNIQUE (user_id, item_id)
);

-- ============================================================================
-- 11. FACT: fct_support_tickets
-- Customer support and missing credit dispute inquiries.
-- ============================================================================
CREATE TABLE fct_support_tickets (
    ticket_id                   VARCHAR(36) PRIMARY KEY,
    user_id                     VARCHAR(36) NOT NULL REFERENCES dim_users(user_id) ON DELETE RESTRICT,
    task_id                     VARCHAR(32) NULL REFERENCES dim_tasks(task_id) ON DELETE RESTRICT,
    dispute_category            VARCHAR(30) NOT NULL 
                                CHECK (dispute_category IN ('Missing_Credit', 'Payout_Delay', 'Account_Flag', 'Technical_Bug')),
    claimed_amount              DECIMAL(10, 2) NOT NULL DEFAULT 0.00 CHECK (claimed_amount >= 0.00),
    status                      VARCHAR(20) NOT NULL DEFAULT 'Open'
                                CHECK (status IN ('Open', 'In_Review', 'Resolved', 'Rejected')),
    created_at                  TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT CURRENT_TIMESTAMP,
    resolved_at                 TIMESTAMP WITH TIME ZONE NULL,
    
    CONSTRAINT chk_ticket_times CHECK (resolved_at IS NULL OR resolved_at >= created_at)
);

CREATE INDEX idx_tickets_user_status ON fct_support_tickets(user_id, status);
