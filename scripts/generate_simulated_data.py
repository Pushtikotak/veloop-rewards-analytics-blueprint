"""
========================================================================================
VELOOP REWARDS — SIMULATED DATASET GENERATION ENGINE
Project: Product Analytics, Data Readiness & Data Management Blueprint
Author: Pushti Kotak
Date: 2026-11-02
Notice: SIMULATED DATA — CREATED FOR ANALYTICAL TESTING
Random Seed: 42 (Fully Reproducible)
========================================================================================
"""

import os
import random
import uuid
from datetime import datetime, timedelta
import pandas as pd
import numpy as np

# Set fixed random seeds for deterministic output
RANDOM_SEED = 42
random.seed(RANDOM_SEED)
np.random.seed(RANDOM_SEED)

OUTPUT_DIR = "data/raw"
os.makedirs(OUTPUT_DIR, exist_ok=True)

# Common Reference Pools
COUNTRIES = ['IN', 'US', 'GB', 'CA', 'BR', 'PH', 'DE', 'ID']
COUNTRY_WEIGHTS = [0.45, 0.20, 0.08, 0.05, 0.07, 0.08, 0.04, 0.03]

AUTH_PROVIDERS = ['Google_OAuth', 'Email_Password', 'Apple_ID', 'Telegram']
AUTH_WEIGHTS = [0.55, 0.30, 0.10, 0.05]

DEVICE_TYPES = ['Android_Mobile', 'iOS_Mobile', 'Desktop_Web', 'Mobile_Web']
DEVICE_WEIGHTS = [0.65, 0.18, 0.12, 0.05]

REG_SOURCES = ['Organic_Search', 'Direct', 'Google_Ads', 'Meta_Ads', 'Referral_Program', 'Influencer']
REG_WEIGHTS = [0.25, 0.15, 0.20, 0.15, 0.15, 0.10]

PROVIDERS = ['CPX_Research', 'Torox', 'AdGate', 'BitLabs', 'Lootably', 'RevU', 'Internal']
PROVIDER_WEIGHTS = [0.30, 0.22, 0.16, 0.12, 0.10, 0.06, 0.04]

TASK_CATEGORIES = ['Survey', 'Game_Install', 'App_Trial', 'Microtask', 'Ad_Video', 'Cashback']
CATEGORY_WEIGHTS = [0.40, 0.25, 0.15, 0.10, 0.06, 0.04]

START_DATE = datetime(2026, 8, 1, 0, 0, 0)
END_DATE = datetime(2026, 11, 1, 23, 59, 59)
TOTAL_DAYS = (END_DATE - START_DATE).days

def random_date(start, end):
    delta = end - start
    random_seconds = random.randint(0, int(delta.total_seconds()))
    return start + timedelta(seconds=random_seconds)

def generate_datasets():
    print("Generating simulated datasets...")

    # -------------------------------------------------------------
    # 1. USERS (Target: ~1,000 rows)
    # -------------------------------------------------------------
    num_users = 1000
    user_rows = []
    user_ids = [f"usr_{uuid.uuid4()}" for _ in range(num_users)]

    for i, u_id in enumerate(user_ids):
        reg_time = random_date(START_DATE, START_DATE + timedelta(days=TOTAL_DAYS - 5))
        country = random.choices(COUNTRIES, weights=COUNTRY_WEIGHTS)[0]
        auth = random.choices(AUTH_PROVIDERS, weights=AUTH_WEIGHTS)[0]
        device = random.choices(DEVICE_TYPES, weights=DEVICE_WEIGHTS)[0]
        source = random.choices(REG_SOURCES, weights=REG_WEIGHTS)[0]
        
        # Account status distribution
        status_r = random.random()
        if status_r < 0.65:
            status = 'Active'
        elif status_r < 0.80:
            status = 'Onboarded'
        elif status_r < 0.90:
            status = 'Dormant'
        elif status_r < 0.97:
            status = 'Churned'
        else:
            status = 'Suspended'

        onboarding_done = status != 'Registered'
        onboarding_time = reg_time + timedelta(minutes=random.randint(2, 45)) if onboarding_done else None
        
        # Last active time
        if status in ['Active', 'Onboarded']:
            last_active = random_date(END_DATE - timedelta(days=7), END_DATE)
        elif status == 'Dormant':
            last_active = random_date(END_DATE - timedelta(days=28), END_DATE - timedelta(days=14))
        else:
            last_active = random_date(reg_time, reg_time + timedelta(days=3))

        user_rows.append({
            'user_id': u_id,
            'account_status': status,
            'registration_timestamp': reg_time.strftime('%Y-%m-%d %H:%M:%S'),
            'registration_source': source,
            'referral_code_used': f"REF_{random.randint(100, 999)}" if source == 'Referral_Program' else None,
            'auth_provider': auth,
            'country_code': country,
            'signup_device_type': device,
            'signup_app_version': f"v{random.choice(['1.0.0', '1.1.2', '1.2.0'])}",
            'signup_ip_hash': uuid.uuid4().hex,
            'email_verified_flag': random.random() > 0.15,
            'onboarding_completed_flag': onboarding_done,
            'onboarding_completed_at': onboarding_time.strftime('%Y-%m-%d %H:%M:%S') if onboarding_time else None,
            'current_level': random.randint(1, 10),
            'total_xp': random.randint(50, 8500),
            'current_streak_days': random.randint(0, 14) if status == 'Active' else 0,
            'lifetime_ve_earned': round(random.uniform(50.0, 12500.0), 2),
            'lifetime_usd_withdrawn': round(random.choice([0.0, 0.0, 5.0, 10.0, 25.0, 50.0]), 2),
            'last_active_timestamp': last_active.strftime('%Y-%m-%d %H:%M:%S'),
            'last_login_device': f"{device}_Model_{random.randint(10, 99)}"
        })

    df_users = pd.DataFrame(user_rows)
    df_users.to_csv(f"{OUTPUT_DIR}/users.csv", index=False)
    print(f"Users generated: {len(df_users)} records")

    # -------------------------------------------------------------
    # 2. CATALOG TASKS (Dimension: ~50 tasks)
    # -------------------------------------------------------------
    tasks = []
    for i in range(1, 51):
        cat = random.choices(TASK_CATEGORIES, weights=CATEGORY_WEIGHTS)[0]
        prov = random.choices(PROVIDERS, weights=PROVIDER_WEIGHTS)[0]
        reward = round(random.uniform(25.0, 2500.0), 2)
        gross_usd = round(reward * 0.001 / 0.65, 4)
        tasks.append({
            'task_id': f"tsk_{prov[:3].lower()}_{cat[:3].lower()}_{i:03d}",
            'task_name': f"{prov} {cat} #{i}",
            'task_category': cat,
            'provider_id': prov,
            'reward_amount': reward,
            'reward_unit': 'VE',
            'estimated_completion_min': random.randint(3, 45),
            'target_countries': 'ALL' if random.random() > 0.3 else 'IN,US,GB,CA',
            'target_devices': 'ALL' if random.random() > 0.4 else 'Android_Mobile,iOS_Mobile',
            'gross_payout_usd': gross_usd,
            'is_active_flag': True,
            'created_at': (START_DATE - timedelta(days=30)).strftime('%Y-%m-%d %H:%M:%S')
        })
    df_tasks = pd.DataFrame(tasks)
    df_tasks.to_csv(f"{OUTPUT_DIR}/catalog_tasks.csv", index=False)
    print(f"Tasks Catalog generated: {len(df_tasks)} records")

    # -------------------------------------------------------------
    # 3. TASK ACTIVITY (Target: ~6,000 rows)
    # -------------------------------------------------------------
    num_activities = 6000
    act_rows = []
    
    # Active users generate more activity
    active_users = df_users[df_users['account_status'].isin(['Active', 'Onboarded'])]['user_id'].tolist()
    all_user_pool = df_users['user_id'].tolist()

    for i in range(num_activities):
        act_id = f"tact_{uuid.uuid4()}"
        u_id = random.choice(active_users) if random.random() < 0.85 else random.choice(all_user_pool)
        t_row = df_tasks.sample(1).iloc[0]
        
        start_t = random_date(START_DATE + timedelta(days=5), END_DATE)
        
        # Outcome distributions
        status_r = random.random()
        if status_r < 0.58:
            act_status = 'Completed'
            val_status = 'Validated_Approved'
            fail_cat = None
            duration_sec = random.randint(120, 2400)
            comp_t = start_t + timedelta(seconds=duration_sec)
            ext_tx = f"ext_{uuid.uuid4().hex[:12]}"
            payout = t_row['gross_payout_usd']
        elif status_r < 0.78:
            act_status = 'Failed'
            val_status = 'Validation_Rejected'
            fail_cat = random.choice(['PARTNER_DISQUALIFIED', 'TRACKING_DROPPED', 'VALIDATION_FAILED'])
            duration_sec = random.randint(30, 600)
            comp_t = start_t + timedelta(seconds=duration_sec)
            ext_tx = None
            payout = 0.0
        elif status_r < 0.95:
            act_status = 'Abandoned'
            val_status = 'Unverified'
            fail_cat = 'USER_ABANDONED'
            duration_sec = None
            comp_t = None
            ext_tx = None
            payout = 0.0
        else:
            act_status = 'Started'
            val_status = 'Pending_Validation'
            fail_cat = None
            duration_sec = None
            comp_t = None
            ext_tx = None
            payout = None

        act_rows.append({
            'task_activity_id': act_id,
            'user_id': u_id,
            'task_id': t_row['task_id'],
            'click_id': f"clk_{uuid.uuid4().hex[:16]}",
            'start_time': start_t.strftime('%Y-%m-%d %H:%M:%S'),
            'completion_time': comp_t.strftime('%Y-%m-%d %H:%M:%S') if comp_t else None,
            'activity_status': act_status,
            'failure_category': fail_cat,
            'reward_amount': t_row['reward_amount'],
            'reward_unit': 'VE',
            'validation_status': val_status,
            'external_tx_id': ext_tx,
            'partner_payout_usd': payout,
            'postback_latency_sec': duration_sec
        })

    df_task_act = pd.DataFrame(act_rows)
    df_task_act.to_csv(f"{OUTPUT_DIR}/task_activity.csv", index=False)
    print(f"Task Activity generated: {len(df_task_act)} records")

    # -------------------------------------------------------------
    # 4. REWARDS (Target: ~5,000 rows)
    # -------------------------------------------------------------
    num_rewards = 5000
    reward_rows = []
    
    # Take completed task activities as base
    completed_tasks = df_task_act[df_task_act['activity_status'] == 'Completed']
    completed_task_list = completed_tasks.to_dict('records')

    # Assign rewards from tasks (~3,400) + daily streaks + spins (~1,600)
    task_count = min(len(completed_task_list), 3400)
    for i in range(task_count):
        ct = completed_task_list[i]
        c_time = datetime.strptime(ct['completion_time'], '%Y-%m-%d %H:%M:%S')
        is_rev = random.random() < 0.025  # 2.5% chargeback reversal rate
        rew_status = 'Reversed' if is_rev else 'Credited'
        
        reward_rows.append({
            'reward_id': f"rew_{uuid.uuid4()}",
            'user_id': ct['user_id'],
            'task_activity_id': ct['task_activity_id'],
            'amount': ct['reward_amount'],
            'unit': 'VE',
            'status': rew_status,
            'created_at': ct['completion_time'],
            'credited_at': ct['completion_time'] if rew_status == 'Credited' else None,
            'source_type': 'Offerwall_Task',
            'is_reversed_flag': is_rev,
            'reversal_reason': 'Advertiser_Chargeback' if is_rev else None
        })

    # Add Streak & Mini-game rewards to reach 5,000
    remaining_rewards = num_rewards - len(reward_rows)
    for _ in range(remaining_rewards):
        u_id = random.choice(active_users)
        src = random.choice(['Daily_Streak', 'Spin_Wheel', 'Referral_Bonus', 'Quest_Milestone'])
        r_time = random_date(START_DATE + timedelta(days=5), END_DATE)
        
        if src == 'Daily_Streak':
            amt = random.choice([10.0, 20.0, 30.0, 50.0, 100.0])
        elif src == 'Spin_Wheel':
            amt = random.choice([5.0, 15.0, 25.0, 50.0, 250.0])
        elif src == 'Referral_Bonus':
            amt = 250.0
        else:
            amt = random.choice([100.0, 200.0, 500.0])

        reward_rows.append({
            'reward_id': f"rew_{uuid.uuid4()}",
            'user_id': u_id,
            'task_activity_id': None,
            'amount': amt,
            'unit': 'VE',
            'status': 'Credited',
            'created_at': r_time.strftime('%Y-%m-%d %H:%M:%S'),
            'credited_at': r_time.strftime('%Y-%m-%d %H:%M:%S'),
            'source_type': src,
            'is_reversed_flag': False,
            'reversal_reason': None
        })

    df_rewards = pd.DataFrame(reward_rows)
    df_rewards.to_csv(f"{OUTPUT_DIR}/rewards.csv", index=False)
    print(f"Rewards generated: {len(df_rewards)} records")

    # -------------------------------------------------------------
    # 5. WALLET TRANSACTIONS (Target: ~3,500 rows)
    # -------------------------------------------------------------
    num_tx = 3500
    tx_rows = []

    # Map credits from rewards and debits from cashouts
    for i in range(num_tx):
        tx_id = f"tx_{uuid.uuid4()}"
        u_id = random.choice(active_users)
        t_time = random_date(START_DATE + timedelta(days=10), END_DATE)
        
        tx_r = random.random()
        if tx_r < 0.70:
            # Reward credit
            direction = 'CREDIT'
            tx_type = random.choice(['REWARD_CREDIT', 'DAILY_BONUS_CREDIT', 'REFERRAL_CREDIT'])
            amt = round(random.choice([15.0, 50.0, 120.0, 250.0, 500.0]), 2)
            src = 'Offerwall_Postback' if tx_type == 'REWARD_CREDIT' else 'Daily_Streak'
            ref_id = f"rew_{uuid.uuid4().hex[:12]}"
            p_id = None
            rev_reason = None
        elif tx_r < 0.92:
            # Withdrawal debit / escrow
            direction = 'DEBIT'
            tx_type = 'WITHDRAWAL_ESCROW'
            amt = round(random.choice([500.0, 1000.0, 2500.0, 5000.0]), 2)
            src = 'Withdrawal_Cashout'
            ref_id = f"wth_{uuid.uuid4().hex[:12]}"
            p_id = None
            rev_reason = None
        else:
            # Reversal / adjustment
            direction = 'DEBIT'
            tx_type = 'REWARD_REVERSAL'
            amt = round(random.choice([100.0, 250.0, 450.0]), 2)
            src = 'Partner_Chargeback'
            ref_id = f"rev_{uuid.uuid4().hex[:12]}"
            p_id = f"tx_{uuid.uuid4().hex[:12]}"
            rev_reason = 'Advertiser_Chargeback'

        bal_before = round(random.uniform(500.0, 15000.0), 2)
        bal_after = round(bal_before + amt if direction == 'CREDIT' else bal_before - amt, 2)

        tx_rows.append({
            'transaction_id': tx_id,
            'user_id': u_id,
            'timestamp': t_time.strftime('%Y-%m-%d %H:%M:%S'),
            'transaction_type': tx_type,
            'direction': direction,
            'amount': amt,
            'unit': 'VE',
            'balance_before': bal_before,
            'balance_after': bal_after,
            'source': src,
            'reference_id': ref_id,
            'parent_tx_id': p_id,
            'reversal_reason': rev_reason
        })

    df_wallet = pd.DataFrame(tx_rows)
    df_wallet.to_csv(f"{OUTPUT_DIR}/wallet.csv", index=False)
    print(f"Wallet Transactions generated: {len(df_wallet)} records")

    # -------------------------------------------------------------
    # 6. WITHDRAWALS (Target: ~1,200 rows)
    # -------------------------------------------------------------
    num_wth = 1200
    wth_rows = []
    methods = ['PayPal', 'UPI_Direct', 'Bank_Transfer', 'Crypto_USDT', 'Amazon_Gift_Card']
    method_weights = [0.40, 0.25, 0.15, 0.12, 0.08]

    for i in range(num_wth):
        w_id = f"wth_{uuid.uuid4()}"
        u_id = random.choice(active_users)
        req_t = random_date(START_DATE + timedelta(days=15), END_DATE)
        method = random.choices(methods, weights=method_weights)[0]
        curr = 'INR' if method == 'UPI_Direct' else 'USD'
        
        req_ve = random.choice([500.0, 1000.0, 2000.0, 5000.0, 10000.0])
        fee_ve = round(req_ve * 0.02, 2)
        net_fiat = round((req_ve - fee_ve) * (83.5 if curr == 'INR' else 0.001), 2)

        # Status distribution
        st_r = random.random()
        if st_r < 0.82:
            status = 'Completed'
            proc_t = req_t + timedelta(hours=random.randint(1, 12))
            fin_t = proc_t + timedelta(minutes=random.randint(5, 60))
            reason = None
            gtw_id = f"GTW_{uuid.uuid4().hex[:12].upper()}"
        elif st_r < 0.92:
            status = 'Processing'
            proc_t = req_t + timedelta(hours=random.randint(1, 8))
            fin_t = None
            reason = None
            gtw_id = None
        elif st_r < 0.97:
            status = 'Rejected'
            proc_t = req_t + timedelta(hours=random.randint(2, 24))
            fin_t = proc_t + timedelta(minutes=5)
            reason = random.choice(['KYC_Failed', 'Invalid_Account_Handle', 'Compliance_Stop'])
            gtw_id = None
        else:
            status = 'Reversed'
            proc_t = req_t + timedelta(hours=2)
            fin_t = req_t + timedelta(days=random.randint(7, 21))
            reason = 'Bank_Chargeback_Clawback'
            gtw_id = f"GTW_REV_{uuid.uuid4().hex[:8].upper()}"

        wth_rows.append({
            'withdrawal_id': w_id,
            'user_id': u_id,
            'requested_amount': req_ve,
            'fee_amount': fee_ve,
            'net_amount': net_fiat,
            'currency': curr,
            'payout_method': method,
            'destination_hash': uuid.uuid4().hex,
            'requested_timestamp': req_t.strftime('%Y-%m-%d %H:%M:%S'),
            'processing_timestamp': proc_t.strftime('%Y-%m-%d %H:%M:%S') if proc_t else None,
            'final_timestamp': fin_t.strftime('%Y-%m-%d %H:%M:%S') if fin_t else None,
            'status': status,
            'reason_category': reason,
            'gateway_tx_id': gtw_id
        })

    df_wth = pd.DataFrame(wth_rows)
    df_wth.to_csv(f"{OUTPUT_DIR}/withdrawals.csv", index=False)
    print(f"Withdrawals generated: {len(df_wth)} records")

    # -------------------------------------------------------------
    # 7. REFERRALS (Target: ~900 rows)
    # -------------------------------------------------------------
    num_ref = 900
    ref_rows = []
    channels = ['WhatsApp', 'Telegram', 'Twitter_X', 'Direct_Link', 'YouTube']

    for i in range(num_ref):
        ref_id = f"ref_{uuid.uuid4()}"
        referrer = random.choice(all_user_pool)
        created_t = random_date(START_DATE + timedelta(days=2), END_DATE - timedelta(days=5))
        
        st_r = random.random()
        if st_r < 0.25:
            # Just created link, no signup
            status = 'Link_Created'
            referred = None
            reg_t = None
            act_t = None
            conv_t = None
        elif st_r < 0.55:
            # Registered but not active
            status = 'Registered'
            referred = random.choice(all_user_pool)
            while referred == referrer:
                referred = random.choice(all_user_pool)
            reg_t = created_t + timedelta(hours=random.randint(1, 48))
            act_t = None
            conv_t = None
        elif st_r < 0.75:
            # Activated (completed task)
            status = 'Activated'
            referred = random.choice(active_users)
            while referred == referrer:
                referred = random.choice(active_users)
            reg_t = created_t + timedelta(hours=random.randint(1, 24))
            act_t = reg_t + timedelta(days=random.randint(1, 4))
            conv_t = None
        else:
            # Fully converted and reward paid
            status = 'Converted'
            referred = random.choice(active_users)
            while referred == referrer:
                referred = random.choice(active_users)
            reg_t = created_t + timedelta(hours=random.randint(1, 12))
            act_t = reg_t + timedelta(days=random.randint(1, 3))
            conv_t = act_t + timedelta(minutes=5)

        ref_rows.append({
            'referral_id': ref_id,
            'referrer_user_id': referrer,
            'referred_user_id': referred,
            'referral_code': f"REF_{referrer[4:8].upper()}",
            'share_channel': random.choice(channels),
            'creation_timestamp': created_t.strftime('%Y-%m-%d %H:%M:%S'),
            'registration_timestamp': reg_t.strftime('%Y-%m-%d %H:%M:%S') if reg_t else None,
            'activation_timestamp': act_t.strftime('%Y-%m-%d %H:%M:%S') if act_t else None,
            'conversion_timestamp': conv_t.strftime('%Y-%m-%d %H:%M:%S') if conv_t else None,
            'referral_status': status,
            'reward_amount': 250.00,
            'reward_unit': 'VE',
            'ip_collision_flag': random.random() < 0.04
        })

    df_ref = pd.DataFrame(ref_rows)
    df_ref.to_csv(f"{OUTPUT_DIR}/referrals.csv", index=False)
    print(f"Referrals generated: {len(df_ref)} records")

    # -------------------------------------------------------------
    # 8. FEATURE EVENTS (Target: ~12,000 rows)
    # -------------------------------------------------------------
    num_events = 12000
    event_rows = []
    
    event_names = [
        ('task_feed_viewed', 'Task_Engine'),
        ('task_offer_opened', 'Task_Engine'),
        ('task_offer_started', 'Task_Engine'),
        ('task_offer_completed', 'Task_Engine'),
        ('engagement_daily_claimed', 'Engagement'),
        ('engagement_spin_started', 'Engagement'),
        ('engagement_spin_completed', 'Engagement'),
        ('wallet_balance_viewed', 'Wallet'),
        ('auth_user_logged_in', 'Authentication'),
        ('auth_user_logged_out', 'Authentication')
    ]
    event_weights = [0.22, 0.18, 0.14, 0.10, 0.12, 0.08, 0.06, 0.05, 0.03, 0.02]

    # Pre-generate session ids for users
    user_sessions = {u: [f"ses_{uuid.uuid4()}" for _ in range(random.randint(3, 10))] for u in active_users}

    for i in range(num_events):
        u_id = random.choice(active_users)
        session_list = user_sessions.get(u_id, [f"ses_{uuid.uuid4()}"])
        s_id = random.choice(session_list)
        
        evt_choice = random.choices(event_names, weights=event_weights)[0]
        s_time = random_date(START_DATE + timedelta(days=3), END_DATE)
        c_time = s_time - timedelta(milliseconds=random.randint(150, 950))
        dev = random.choices(DEVICE_TYPES, weights=DEVICE_WEIGHTS)[0]

        event_rows.append({
            'event_id': f"evt_{uuid.uuid4()}",
            'user_id': u_id,
            'session_id': s_id,
            'event_name': evt_choice[0],
            'feature_domain': evt_choice[1],
            'client_timestamp': c_time.strftime('%Y-%m-%d %H:%M:%S.%f')[:-3],
            'server_timestamp': s_time.strftime('%Y-%m-%d %H:%M:%S.%f')[:-3],
            'device_type': dev,
            'app_version': 'v1.2.0',
            'event_properties_json': f"{{\"client_platform\": \"{dev}\", \"sample_index\": {i}}}"
        })

    df_events = pd.DataFrame(event_rows)
    df_events.to_csv(f"{OUTPUT_DIR}/feature_events.csv", index=False)
    print(f"Feature Events generated: {len(df_events)} records")

    # -------------------------------------------------------------
    # 9. MESSY DATA (Target: ~500+ rows with 14 intentional defect types)
    # -------------------------------------------------------------
    num_messy = 550
    messy_rows = []

    defect_categories = [
        'duplicate_id', 'missing_id', 'missing_timestamp', 'malformed_date',
        'invalid_status', 'inconsistent_capitalization', 'trailing_spaces',
        'invalid_numeric_value', 'negative_value_inappropriate', 'unexpected_null',
        'orphan_record', 'duplicate_event', 'inconsistent_naming', 'impossible_state_transition'
    ]

    for i in range(num_messy):
        defect = defect_categories[i % len(defect_categories)]
        row_id = f"err_{i+1:04d}"
        
        # Base realistic record
        u_id = f"usr_{uuid.uuid4()}"
        ts = "2026-10-15 12:30:00"
        tx_type = "REWARD_CREDIT"
        amt = 150.00
        status = "Completed"
        method = "PayPal"

        # Inject specific defect
        if defect == 'duplicate_id':
            row_id = "err_DUPLICATE_001"  # Repetitive ID
        elif defect == 'missing_id':
            row_id = ""                   # Blank ID
        elif defect == 'missing_timestamp':
            ts = ""                       # Missing timestamp
        elif defect == 'malformed_date':
            ts = "15/10/2026 25:99:00"    # Impossible hour/minute & format
        elif defect == 'invalid_status':
            status = "UNKNOWN_GLITCH"     # Unapproved state
        elif defect == 'inconsistent_capitalization':
            status = "cOmPLeTeD"          # Messy case
        elif defect == 'trailing_spaces':
            status = "Completed   "       # Trailing whitespace
            tx_type = "  REWARD_CREDIT "
        elif defect == 'invalid_numeric_value':
            amt = "ONE_HUNDRED"           # String instead of decimal
        elif defect == 'negative_value_inappropriate':
            amt = -500.00                 # Illegal negative reward
        elif defect == 'unexpected_null':
            u_id = None                   # Null user ID
        elif defect == 'orphan_record':
            u_id = "usr_NON_EXISTENT_GHOST_9999" # Orphan user
        elif defect == 'duplicate_event':
            row_id = "err_DUPE_EVENT_777" # Replayed event
        elif defect == 'inconsistent_naming':
            tx_type = "reward-payout-bonus" # Hyphenated non-standard naming
        elif defect == 'impossible_state_transition':
            status = "Requested_Then_Instantly_Refunded_Without_Processing"

        messy_rows.append({
            'issue_record_id': row_id,
            'user_id': u_id,
            'timestamp': ts,
            'transaction_type': tx_type,
            'amount': amt,
            'status': status,
            'payout_method': method,
            'injected_defect_type': defect
        })

    df_messy = pd.DataFrame(messy_rows)
    df_messy.to_csv(f"{OUTPUT_DIR}/messy_data.csv", index=False)
    print(f"Messy Data generated: {len(df_messy)} records with 14 defect categories")

    print("\n--- ALL 8 SIMULATED DATASETS GENERATED SUCCESSFULLY ---")

if __name__ == "__main__":
    generate_datasets()
