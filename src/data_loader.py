"""
VELOOP Rewards - Product Analytics Platform
Module: Data Loader
Author: Pushti Kotak
Description: Reusable, robust data loading module with schema enforcement,
date parsing, and caching.
"""

import os
import json
import pandas as pd
import numpy as np

RAW_DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data", "raw")
PROCESSED_DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data", "processed")

def get_raw_path(filename: str) -> str:
    return os.path.join(RAW_DATA_DIR, filename)

def get_processed_path(filename: str) -> str:
    return os.path.join(PROCESSED_DATA_DIR, filename)

def load_catalog_tasks(use_processed: bool = False) -> pd.DataFrame:
    path = get_processed_path("catalog_tasks_clean.csv") if use_processed and os.path.exists(get_processed_path("catalog_tasks_clean.csv")) else get_raw_path("catalog_tasks.csv")
    df = pd.read_csv(path)
    df["created_at"] = pd.to_datetime(df["created_at"], errors="coerce")
    df["reward_amount"] = pd.to_numeric(df["reward_amount"], errors="coerce")
    df["gross_payout_usd"] = pd.to_numeric(df["gross_payout_usd"], errors="coerce")
    df["estimated_completion_min"] = pd.to_numeric(df["estimated_completion_min"], errors="coerce")
    df["is_active_flag"] = df["is_active_flag"].astype(bool)
    return df

def load_users(use_processed: bool = False) -> pd.DataFrame:
    path = get_processed_path("users_clean.csv") if use_processed and os.path.exists(get_processed_path("users_clean.csv")) else get_raw_path("users.csv")
    df = pd.read_csv(path)
    df["registration_timestamp"] = pd.to_datetime(df["registration_timestamp"], errors="coerce")
    df["last_active_timestamp"] = pd.to_datetime(df["last_active_timestamp"], errors="coerce")
    df["onboarding_completed_at"] = pd.to_datetime(df["onboarding_completed_at"], errors="coerce")
    df["current_level"] = pd.to_numeric(df["current_level"], errors="coerce").fillna(1).astype(int)
    df["total_xp"] = pd.to_numeric(df["total_xp"], errors="coerce").fillna(0).astype(int)
    df["current_streak_days"] = pd.to_numeric(df["current_streak_days"], errors="coerce").fillna(0).astype(int)
    df["lifetime_ve_earned"] = pd.to_numeric(df["lifetime_ve_earned"], errors="coerce").fillna(0.0)
    df["lifetime_usd_withdrawn"] = pd.to_numeric(df["lifetime_usd_withdrawn"], errors="coerce").fillna(0.0)
    df["email_verified_flag"] = df["email_verified_flag"].astype(bool)
    df["onboarding_completed_flag"] = df["onboarding_completed_flag"].astype(bool)
    return df

def load_task_activity(use_processed: bool = False) -> pd.DataFrame:
    path = get_processed_path("task_activity_clean.csv") if use_processed and os.path.exists(get_processed_path("task_activity_clean.csv")) else get_raw_path("task_activity.csv")
    df = pd.read_csv(path)
    df["start_time"] = pd.to_datetime(df["start_time"], errors="coerce")
    df["completion_time"] = pd.to_datetime(df["completion_time"], errors="coerce")
    df["reward_amount"] = pd.to_numeric(df["reward_amount"], errors="coerce").fillna(0.0)
    df["partner_payout_usd"] = pd.to_numeric(df["partner_payout_usd"], errors="coerce").fillna(0.0)
    df["postback_latency_sec"] = pd.to_numeric(df["postback_latency_sec"], errors="coerce")
    return df

def load_rewards(use_processed: bool = False) -> pd.DataFrame:
    path = get_processed_path("rewards_clean.csv") if use_processed and os.path.exists(get_processed_path("rewards_clean.csv")) else get_raw_path("rewards.csv")
    df = pd.read_csv(path)
    df["created_at"] = pd.to_datetime(df["created_at"], errors="coerce")
    df["credited_at"] = pd.to_datetime(df["credited_at"], errors="coerce")
    df["amount"] = pd.to_numeric(df["amount"], errors="coerce").fillna(0.0)
    df["is_reversed_flag"] = df["is_reversed_flag"].astype(bool)
    return df

def load_wallet(use_processed: bool = False) -> pd.DataFrame:
    path = get_processed_path("wallet_clean.csv") if use_processed and os.path.exists(get_processed_path("wallet_clean.csv")) else get_raw_path("wallet.csv")
    df = pd.read_csv(path)
    df["timestamp"] = pd.to_datetime(df["timestamp"], errors="coerce")
    df["amount"] = pd.to_numeric(df["amount"], errors="coerce").fillna(0.0)
    df["balance_before"] = pd.to_numeric(df["balance_before"], errors="coerce").fillna(0.0)
    df["balance_after"] = pd.to_numeric(df["balance_after"], errors="coerce").fillna(0.0)
    return df

def load_withdrawals(use_processed: bool = False) -> pd.DataFrame:
    path = get_processed_path("withdrawals_clean.csv") if use_processed and os.path.exists(get_processed_path("withdrawals_clean.csv")) else get_raw_path("withdrawals.csv")
    df = pd.read_csv(path)
    df["requested_timestamp"] = pd.to_datetime(df["requested_timestamp"], errors="coerce")
    df["processing_timestamp"] = pd.to_datetime(df["processing_timestamp"], errors="coerce")
    df["final_timestamp"] = pd.to_datetime(df["final_timestamp"], errors="coerce")
    df["requested_amount"] = pd.to_numeric(df["requested_amount"], errors="coerce").fillna(0.0)
    df["fee_amount"] = pd.to_numeric(df["fee_amount"], errors="coerce").fillna(0.0)
    df["net_amount"] = pd.to_numeric(df["net_amount"], errors="coerce").fillna(0.0)
    return df

def load_referrals(use_processed: bool = False) -> pd.DataFrame:
    path = get_processed_path("referrals_clean.csv") if use_processed and os.path.exists(get_processed_path("referrals_clean.csv")) else get_raw_path("referrals.csv")
    df = pd.read_csv(path)
    df["creation_timestamp"] = pd.to_datetime(df["creation_timestamp"], errors="coerce")
    df["registration_timestamp"] = pd.to_datetime(df["registration_timestamp"], errors="coerce")
    df["activation_timestamp"] = pd.to_datetime(df["activation_timestamp"], errors="coerce")
    df["conversion_timestamp"] = pd.to_datetime(df["conversion_timestamp"], errors="coerce")
    df["reward_amount"] = pd.to_numeric(df["reward_amount"], errors="coerce").fillna(0.0)
    df["ip_collision_flag"] = df["ip_collision_flag"].astype(bool)
    return df

def load_feature_events(use_processed: bool = False) -> pd.DataFrame:
    path = get_processed_path("feature_events_clean.csv") if use_processed and os.path.exists(get_processed_path("feature_events_clean.csv")) else get_raw_path("feature_events.csv")
    df = pd.read_csv(path)
    df["client_timestamp"] = pd.to_datetime(df["client_timestamp"], errors="coerce")
    df["server_timestamp"] = pd.to_datetime(df["server_timestamp"], errors="coerce")
    return df

def load_messy_data() -> pd.DataFrame:
    path = get_raw_path("messy_data.csv")
    df = pd.read_csv(path)
    return df

def load_all_datasets(use_processed: bool = False) -> dict:
    return {
        "catalog_tasks": load_catalog_tasks(use_processed),
        "users": load_users(use_processed),
        "task_activity": load_task_activity(use_processed),
        "rewards": load_rewards(use_processed),
        "wallet": load_wallet(use_processed),
        "withdrawals": load_withdrawals(use_processed),
        "referrals": load_referrals(use_processed),
        "feature_events": load_feature_events(use_processed),
        "messy_data": load_messy_data()
    }
