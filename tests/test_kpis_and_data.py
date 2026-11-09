"""
VELOP Rewards - Automated Test Suite
Author: Pushti Kotak
Task: Comprehensive Unit, Regression, and Boundary Testing for Data Readiness & KPI Engine
"""

import unittest
import os
import sys
import pandas as pd
import numpy as np

# Ensure project root is in sys.path
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from src.data_loader import load_all_datasets
from src.kpi_engine import (
    filter_dataset,
    compute_executive_kpis,
    compute_user_analytics,
    compute_engagement_kpis,
    compute_rewards_kpis,
    compute_wallet_ledger_kpis,
    compute_withdrawal_kpis,
    compute_referral_kpis
)

class TestVeloopDataAndKPIs(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.data = load_all_datasets(use_processed=True)

    def test_datasets_exist_and_non_empty(self):
        """Verify all 9 datasets load and contain expected minimum records and columns."""
        expected_counts = {
            "catalog_tasks": 50,
            "users": 1000,
            "task_activity": 6000,
            "rewards": 5000,
            "wallet": 3500,
            "withdrawals": 1200,
            "referrals": 900,
            "feature_events": 12000,
            "messy_data": 550
        }
        for name, expected in expected_counts.items():
            self.assertIn(name, self.data)
            self.assertEqual(len(self.data[name]), expected, f"Dataset {name} row count mismatch")
            self.assertGreater(len(self.data[name].columns), 2, f"Dataset {name} columns missing")

    def test_referential_integrity(self):
        """Verify 0 orphan records across core relational foreign keys."""
        valid_user_ids = set(self.data["users"]["user_id"])
        valid_task_ids = set(self.data["catalog_tasks"]["task_id"])

        # task_activity -> users & tasks
        self.assertTrue(self.data["task_activity"]["user_id"].isin(valid_user_ids).all())
        self.assertTrue(self.data["task_activity"]["task_id"].isin(valid_task_ids).all())

        # rewards -> users
        self.assertTrue(self.data["rewards"]["user_id"].isin(valid_user_ids).all())

        # wallet -> users
        self.assertTrue(self.data["wallet"]["user_id"].isin(valid_user_ids).all())

        # withdrawals -> users
        self.assertTrue(self.data["withdrawals"]["user_id"].isin(valid_user_ids).all())

        # referrals -> referrers
        self.assertTrue(self.data["referrals"]["referrer_user_id"].isin(valid_user_ids).all())

    def test_double_entry_ledger_balance(self):
        """Verify row-level mathematical identity and macro flow of the wallet transaction ledger."""
        df_wal = self.data["wallet"]
        expected_after = np.where(
            df_wal["direction"] == "CREDIT",
            df_wal["balance_before"] + df_wal["amount"],
            df_wal["balance_before"] - df_wal["amount"]
        )
        discrepancies = np.abs(df_wal["balance_after"] - expected_after) > 0.001
        self.assertEqual(discrepancies.sum(), 0, "Ledger balance discrepancies detected")

        # Macro ledger flow verification:
        # Wallet credits = 456,210 VE, debits = 1,876,150 VE, net flow = -1,419,940 VE
        total_credits = df_wal[df_wal["direction"] == "CREDIT"]["amount"].sum()
        total_debits = df_wal[df_wal["direction"] == "DEBIT"]["amount"].sum()
        self.assertEqual(total_credits, 456210.0, "Wallet credits mismatch")
        self.assertEqual(total_debits, 1876150.0, "Wallet debits mismatch")
        self.assertEqual(total_credits - total_debits, -1419940.0, "Macro net flow mismatch")

    def test_executive_kpis(self):
        """Verify executive KPI calculations produce exact verified figures."""
        kpis = compute_executive_kpis(self.data)
        
        # Telemetry & Engagement
        self.assertAlmostEqual(kpis["avg_dau"], 122.97, delta=0.1)
        self.assertEqual(kpis["latest_dau"], 100)
        self.assertEqual(kpis["mau"], 811)
        self.assertAlmostEqual(kpis["stickiness_pct"], 15.16, delta=0.1)
        
        # Commercial Task Offerwall
        self.assertEqual(kpis["total_task_starts"], 6000)
        self.assertEqual(kpis["total_completed_tasks"], 3463)
        self.assertAlmostEqual(kpis["gross_partner_revenue_usd"], 7171.59, delta=0.01)
        self.assertAlmostEqual(kpis["task_reward_cost_usd"], 4661.52, delta=0.01)
        self.assertAlmostEqual(kpis["gross_margin_usd"], 2510.06, delta=0.02)
        self.assertAlmostEqual(kpis["gross_margin_pct"], 35.00, delta=0.01)
        
        # Cumulative Rewards, Withdrawals & Remaining Obligation
        self.assertAlmostEqual(kpis["cumulative_net_rewards_usd"], 4543.84, delta=0.01)
        self.assertAlmostEqual(kpis["completed_withdrawals_usd"], 3693.50, delta=0.01)
        self.assertAlmostEqual(kpis["remaining_obligation_usd"], 850.34, delta=0.01)
        self.assertAlmostEqual(kpis["processing_escrow_usd"], 313.00, delta=0.01)
        self.assertAlmostEqual(kpis["available_balance_usd"], 537.34, delta=0.01)
        self.assertAlmostEqual(
            kpis["available_balance_usd"] + kpis["processing_escrow_usd"],
            kpis["remaining_obligation_usd"],
            delta=0.001
        )
        
        # Fulfillment SLA
        self.assertAlmostEqual(kpis["payout_sla_pct"], 100.0, delta=0.01)
        self.assertAlmostEqual(kpis["median_processing_hours"], 7.11, delta=0.1)

    def test_user_analytics_kpis(self):
        """Verify user analytics calculations."""
        u_kpis = compute_user_analytics(self.data)
        self.assertEqual(u_kpis["total_users"], 1000)
        self.assertEqual(u_kpis["active_users"], 655)
        self.assertEqual(u_kpis["onboarded_users"], 1000)
        self.assertEqual(u_kpis["onboarding_completion_rate_pct"], 100.0)
        self.assertEqual(u_kpis["device_counts"]["Android_Mobile"], 637)
        self.assertEqual(u_kpis["device_counts"]["iOS_Mobile"], 182)
        self.assertEqual(u_kpis["device_counts"]["Desktop_Web"], 115)
        self.assertEqual(u_kpis["device_counts"]["Mobile_Web"], 66)

    def test_rewards_and_reversals(self):
        """Verify reward and reversal computations."""
        r_kpis = compute_rewards_kpis(self.data)
        self.assertEqual(r_kpis["total_rewards_count"], 5000)
        self.assertAlmostEqual(r_kpis["total_credited_ve"], 4685760.56, delta=0.01)
        self.assertAlmostEqual(r_kpis["total_reversed_ve"], 141919.04, delta=0.01)
        self.assertEqual(r_kpis["reversal_count"], 108)
        self.assertAlmostEqual(r_kpis["reversal_rate_pct"], 2.94, delta=0.01)

    def test_withdrawals_kpis(self):
        """Verify withdrawal metrics, status reconciliation, and processing latencies."""
        w_kpis = compute_withdrawal_kpis(self.data)
        self.assertEqual(w_kpis["total_withdrawals"], 1200)
        self.assertEqual(w_kpis["completed_count"], 1012)
        self.assertEqual(w_kpis["processing_count"], 104)
        self.assertEqual(w_kpis["rejected_count"], 51)
        self.assertEqual(w_kpis["reversed_count"], 33)
        self.assertAlmostEqual(w_kpis["completion_rate_pct"], (1012 / 1200 * 100), delta=0.01)
        self.assertEqual(w_kpis["total_disbursed_ve"], 3693500.0)
        self.assertEqual(w_kpis["total_disbursed_usd"], 3693.50)
        self.assertEqual(w_kpis["processing_ve"], 313000.0)
        self.assertEqual(w_kpis["rejected_ve"], 162500.0)
        self.assertEqual(w_kpis["reversed_ve"], 126500.0)
        self.assertEqual(w_kpis["escrow_and_refund_ve"], 602000.0)

    def test_referrals_kpis(self):
        """Verify referral conversion funnel and viral K factor."""
        ref_kpis = compute_referral_kpis(self.data)
        self.assertEqual(ref_kpis["total_links_created"], 900)
        self.assertEqual(ref_kpis["registered_referrals"], 679)
        self.assertEqual(ref_kpis["activated_referrals"], 405)
        self.assertEqual(ref_kpis["converted_referrals"], 229)
        self.assertAlmostEqual(ref_kpis["viral_k_factor"], 1.17, delta=0.01)
        self.assertEqual(ref_kpis["ip_collisions_blocked"], 37)

    # -------------------------------------------------------------
    # NEW COMPREHENSIVE AUDIT & ROBUSTNESS TESTS (8 ADDITIONS)
    # -------------------------------------------------------------

    def test_device_filters(self):
        """Verify device filtering across All, Android, iOS, and Web partitions."""
        devices = {
            "All": (1000, 12000),
            "Android": (637, 7802),
            "iOS": (182, 2193),
            "Web": (181, 2005)
        }
        for dev, (exp_users, exp_events) in devices.items():
            filtered = filter_dataset(self.data, device_filter=dev)
            self.assertEqual(len(filtered["users"]), exp_users, f"Device {dev} user count mismatch")
            self.assertEqual(len(filtered["feature_events"]), exp_events, f"Device {dev} event count mismatch")
            
            # Verify internal device strings match criteria
            if dev == "Android":
                self.assertTrue(filtered["feature_events"]["device_type"].str.startswith("Android").all())
            elif dev == "iOS":
                self.assertTrue(filtered["feature_events"]["device_type"].str.startswith("iOS").all())
            elif dev == "Web":
                self.assertTrue(filtered["feature_events"]["device_type"].str.contains("Web", case=False).all())

        # Test Desktop_Web and Web_Desktop aliases resolution
        f_desk1 = filter_dataset(self.data, device_filter="Desktop_Web")
        f_desk2 = filter_dataset(self.data, device_filter="Web_Desktop")
        self.assertEqual(len(f_desk1["feature_events"]), 1393)
        self.assertEqual(len(f_desk2["feature_events"]), 1393)
        self.assertEqual(len(f_desk1["users"]), 115)
        self.assertEqual(len(f_desk2["users"]), 115)

    def test_single_day_date_selection(self):
        """Verify single-day date filter captures all events on that day and computes correct DAU."""
        f_single = filter_dataset(self.data, date_range=["2026-09-01", "2026-09-01"])
        evts = f_single["feature_events"]
        self.assertEqual(len(evts), 117, "Single-day event count mismatch")
        
        # All events must fall strictly within 2026-09-01
        self.assertTrue((evts["client_timestamp"].dt.date == pd.to_datetime("2026-09-01").date()).all())
        
        # Exactly 113 unique users fired 117 events
        self.assertEqual(evts["user_id"].nunique(), 113)
        
        kpis = compute_executive_kpis(f_single)
        self.assertEqual(kpis["avg_dau"], 113.0)
        self.assertEqual(kpis["latest_dau"], 113)

    def test_end_date_boundary_inclusion(self):
        """Verify that events at 23:59:59.999 on end date are included and next day is excluded."""
        synthetic_evt = pd.DataFrame({
            "event_id": ["evt_morning", "evt_end_of_day", "evt_next_morning"],
            "user_id": ["u1", "u2", "u3"],
            "client_timestamp": [
                pd.to_datetime("2026-09-01 10:00:00"),
                pd.to_datetime("2026-09-01 23:59:59"),
                pd.to_datetime("2026-09-02 00:00:01")
            ],
            "device_type": ["Android_Mobile", "Android_Mobile", "Android_Mobile"]
        })
        mock_data = {k: v.iloc[0:0].copy() for k, v in self.data.items()}
        mock_data["feature_events"] = synthetic_evt
        mock_data["users"] = self.data["users"]
        
        filtered = filter_dataset(mock_data, date_range=["2026-09-01", "2026-09-01"])
        included_ids = set(filtered["feature_events"]["event_id"])
        
        self.assertIn("evt_morning", included_ids)
        self.assertIn("evt_end_of_day", included_ids, "23:59:59 event must be included in end-date range")
        self.assertNotIn("evt_next_morning", included_ids, "Next day 00:00:01 event must be excluded")

    def test_empty_datasets_resilience(self):
        """Verify that all 7 KPI functions handle 0-row empty datasets gracefully without crashing."""
        empty_data = {k: v.iloc[0:0].copy() for k, v in self.data.items()}
        
        kpi_exec = compute_executive_kpis(empty_data)
        self.assertEqual(kpi_exec["avg_dau"], 0.0)
        self.assertEqual(kpi_exec["gross_partner_revenue_usd"], 0.0)
        self.assertEqual(kpi_exec["task_completion_rate_pct"], 0.0)
        self.assertEqual(kpi_exec["remaining_obligation_usd"], 0.0)
        self.assertEqual(kpi_exec["available_balance_usd"], 0.0)
        self.assertEqual(kpi_exec["processing_escrow_usd"], 0.0)
        
        kpi_usr = compute_user_analytics(empty_data)
        self.assertEqual(kpi_usr["total_users"], 0)
        self.assertEqual(kpi_usr["onboarding_completion_rate_pct"], 0.0)
        
        kpi_eng = compute_engagement_kpis(empty_data)
        self.assertEqual(kpi_eng["daily_streak_claims"], 0)
        
        kpi_rew = compute_rewards_kpis(empty_data)
        self.assertEqual(kpi_rew["total_credited_ve"], 0.0)
        self.assertEqual(kpi_rew["reversal_rate_pct"], 0.0)
        
        kpi_wal = compute_wallet_ledger_kpis(empty_data)
        self.assertEqual(kpi_wal["total_transactions"], 0)
        self.assertEqual(kpi_wal["ledger_discrepancies_count"], 0)
        self.assertIn("ROW-VERIFIED", kpi_wal["ledger_audit_status"])
        
        kpi_wth = compute_withdrawal_kpis(empty_data)
        self.assertEqual(kpi_wth["total_withdrawals"], 0)
        self.assertEqual(kpi_wth["completion_rate_pct"], 0.0)
        
        kpi_ref = compute_referral_kpis(empty_data)
        self.assertEqual(kpi_ref["total_links_created"], 0)
        self.assertEqual(kpi_ref["viral_k_factor"], 0.0)

    def test_missing_values_imputation_and_handling(self):
        """Verify KPI computations succeed without exceptions when data contains nulls/NaNs."""
        dirty_data = {k: v.copy() for k, v in self.data.items()}
        # Inject NaNs
        dirty_data["task_activity"].loc[0:50, "partner_payout_usd"] = np.nan
        dirty_data["rewards"].loc[0:50, "reversal_reason"] = np.nan
        dirty_data["withdrawals"].loc[0:50, "fee_amount"] = np.nan
        dirty_data["users"].loc[0:50, "signup_device_type"] = np.nan
        
        # Ensure calculations run cleanly
        exec_kpis = compute_executive_kpis(dirty_data)
        self.assertGreater(exec_kpis["gross_partner_revenue_usd"], 0)
        
        rew_kpis = compute_rewards_kpis(dirty_data)
        self.assertGreater(rew_kpis["total_credited_ve"], 0)
        
        wth_kpis = compute_withdrawal_kpis(dirty_data)
        self.assertGreater(wth_kpis["completion_rate_pct"], 0)

    def test_kpi_and_chart_consistency(self):
        """Verify mathematical identity between summary KPI cards and underlying chart data."""
        kpis = compute_executive_kpis(self.data)
        
        # 1. Page 1 DAU: KPI average equals mean of chart's daily grouped series
        daily_trends = self.data["feature_events"].groupby(
            self.data["feature_events"]["client_timestamp"].dt.date
        )["user_id"].nunique()
        self.assertAlmostEqual(kpis["avg_dau"], daily_trends.mean(), places=2)
        
        # 2. Page 1 Gross Revenue: KPI card equals sum of monthly bar chart values
        comp_act = self.data["task_activity"][self.data["task_activity"]["activity_status"] == "Completed"]
        comp_act = comp_act.copy()
        comp_act["month"] = comp_act["start_time"].dt.to_period("M").astype(str)
        monthly_rev = comp_act.groupby("month")["partner_payout_usd"].sum().sum()
        self.assertAlmostEqual(kpis["gross_partner_revenue_usd"], monthly_rev, places=2)
        
        # 3. Page 1 Reward Cost: KPI card equals sum of monthly cost bars
        monthly_cost = comp_act.groupby("month")["reward_amount"].sum().sum() * 0.001
        self.assertAlmostEqual(kpis["task_reward_cost_usd"], monthly_cost, places=2)
        
        # 4. Page 6 Cashouts: Total status breakdown equals total withdrawals
        wth_status_sum = self.data["withdrawals"]["status"].value_counts().sum()
        wth_kpis = compute_withdrawal_kpis(self.data)
        self.assertEqual(wth_status_sum, wth_kpis["total_withdrawals"])

    def test_financial_reconciliation(self):
        """Verify full platform accounting reconciliation across tasks, rewards, and withdrawals."""
        comp_act = self.data["task_activity"][self.data["task_activity"]["activity_status"] == "Completed"]
        gross_rev = float(comp_act["partner_payout_usd"].sum())
        reward_cost = float(comp_act["reward_amount"].sum() * 0.001)
        gross_margin_usd = gross_rev - reward_cost
        gross_margin_pct = (gross_margin_usd / gross_rev * 100)
        
        # 1. Revenue & Margin
        self.assertAlmostEqual(gross_rev, 7171.59, delta=0.01)
        self.assertAlmostEqual(reward_cost, 4661.52, delta=0.01)
        self.assertAlmostEqual(gross_margin_usd, 2510.06, delta=0.02)
        self.assertAlmostEqual(gross_margin_pct, 35.00, delta=0.01)
        
        # 2. Cumulative Net Rewards Issued (Rewards table)
        rew = self.data["rewards"]
        credited_ve = float(rew[rew["status"] == "Credited"]["amount"].sum())
        reversed_ve = float(rew[rew["is_reversed_flag"]]["amount"].sum())
        net_rewards_ve = credited_ve - reversed_ve
        self.assertAlmostEqual(credited_ve, 4685760.56, delta=0.01)
        self.assertAlmostEqual(reversed_ve, 141919.04, delta=0.01)
        self.assertAlmostEqual(net_rewards_ve, 4543841.52, delta=0.01)
        self.assertAlmostEqual(net_rewards_ve * 0.001, 4543.84, delta=0.01)
        
        # 3. Liquidated Completed Cashouts
        wth = self.data["withdrawals"]
        completed_wth_ve = float(wth[wth["status"] == "Completed"]["requested_amount"].sum())
        self.assertAlmostEqual(completed_wth_ve, 3693500.00, delta=0.01)
        self.assertAlmostEqual(completed_wth_ve * 0.001, 3693.50, delta=0.01)
        
        # 4. Remaining Aggregate Obligation
        remaining_obligation_ve = net_rewards_ve - completed_wth_ve
        self.assertAlmostEqual(remaining_obligation_ve, 850341.52, delta=0.01)
        self.assertAlmostEqual(remaining_obligation_ve * 0.001, 850.34, delta=0.01)
        
        # 5. Escrow and Available Balance Split
        processing_escrow_ve = float(wth[wth["status"] == "Processing"]["requested_amount"].sum())
        available_balance_ve = remaining_obligation_ve - processing_escrow_ve
        self.assertAlmostEqual(processing_escrow_ve, 313000.00, delta=0.01)
        self.assertAlmostEqual(processing_escrow_ve * 0.001, 313.00, delta=0.01)
        self.assertAlmostEqual(available_balance_ve, 537341.52, delta=0.01)
        self.assertAlmostEqual(available_balance_ve * 0.001, 537.34, delta=0.01)
        self.assertAlmostEqual(available_balance_ve + processing_escrow_ve, remaining_obligation_ve, delta=0.001)

    def test_csv_download_payloads(self):
        """Verify that UI download exports generate valid, non-empty CSV payloads."""
        # User dataset export payload
        user_csv = self.data["users"].head(10).to_csv(index=False)
        self.assertTrue(len(user_csv) > 0)
        self.assertIn("user_id", user_csv)
        self.assertIn("registration_timestamp", user_csv)
        
        # Offerwall inventory export payload
        tasks_csv = self.data["catalog_tasks"].head(10).to_csv(index=False)
        self.assertTrue(len(tasks_csv) > 0)
        self.assertIn("task_id", tasks_csv)
        self.assertIn("gross_payout_usd", tasks_csv)
        
        # Wallet ledger export payload
        wallet_csv = self.data["wallet"].head(10).to_csv(index=False)
        self.assertTrue(len(wallet_csv) > 0)
        self.assertIn("transaction_id", wallet_csv)
        self.assertIn("balance_before", wallet_csv)
        
        # Withdrawals export payload
        wth_csv = self.data["withdrawals"].head(10).to_csv(index=False)
        self.assertTrue(len(wth_csv) > 0)
        self.assertIn("withdrawal_id", wth_csv)
        self.assertIn("requested_amount", wth_csv)

if __name__ == "__main__":
    unittest.main()
