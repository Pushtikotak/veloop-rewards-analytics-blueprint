"""
VELOP Rewards - Comprehensive Dashboard Test Suite
Author: Pushti Kotak
Task: Full-suite programmatic interaction, multi-page navigation,
filter testing, and rendering verification with deep content assertions
using Streamlit AppTest.
"""

import sys
import os
import pandas as pd
from streamlit.testing.v1 import AppTest

# Ensure project root in sys.path
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

def run_apptest_comprehensive_suite():
    """Systematically navigate all 7 pages, toggle filters, and assert deep content congruence."""
    app_path = os.path.join(PROJECT_ROOT, "app.py")
    print(f"\n[AppTest] Initializing Streamlit AppTest runner on {app_path}...")
    at = AppTest.from_file(app_path, default_timeout=25)
    at.run()
    
    assert len(at.exception) == 0, f"Initial launch exceptions: {[e.value for e in at.exception]}"
    print("[AppTest] App launched successfully with 0 exceptions.")
    
    pages = [
        "Executive Overview",
        "User Analytics",
        "Engagement & Gamification",
        "Rewards & Reversals",
        "Wallet & Ledger Reconciliation",
        "Withdrawals & Payout Fulfillment",
        "Referrals & Viral Acquisition"
    ]
    
    devices = ["All", "Android", "iOS", "Web"]
    total_checks = 0
    
    # -------------------------------------------------------------
    # 1. PAGE-BY-PAGE NAVIGATION & DEEP CONTENT ASSERTIONS
    # -------------------------------------------------------------
    for page in pages:
        print(f"\n---> Testing Page: '{page}'")
        at.radio[0].set_value(page).run()
        
        if len(at.exception) > 0:
            print(f"  FAILED on page {page}:")
            for e in at.exception:
                print("    ", e.value)
            raise AssertionError(f"Exception on page {page}")
            
        all_md = " ".join([m.value for m in at.markdown])
        
        # Deep Assertions per Page:
        if page == "Executive Overview":
            assert "123" in all_md, "DAU 123 missing from Executive Overview"
            assert "3,463" in all_md, "Completed tasks 3,463 missing from Executive Overview"
            assert "$850.34" in all_md, "Remaining obligation $850.34 missing from Executive Overview"
            assert "$537.34" in all_md, "Available balance $537.34 missing from Executive Overview"
            assert "$313.00" in all_md, "Processing escrow $313.00 missing from Executive Overview"
            assert "100.0%" in all_md, "Payout SLA 100.0% missing from Executive Overview"
            print("  [PASS] Page 1 KPI assertions: DAU=123, Tasks=3,463, Obligation=$850.34 ($537.34+$313.00), SLA=100.0%")
            
        elif page == "User Analytics":
            assert "1,000" in all_md, "Total users 1,000 missing from User Analytics"
            assert "655" in all_md, "Active users 655 missing from User Analytics"
            assert len(at.dataframe) >= 1, "User accounts table missing"
            assert len(at.dataframe[0].value) == 1000, "User accounts table row count mismatch"
            print("  [PASS] Page 2 KPI assertions: Total=1,000, Active=655, User Table=1,000 rows")
            
        elif page == "Engagement & Gamification":
            assert len(at.markdown) >= 10, "Gamification markdown count mismatch"
            print("  [PASS] Page 3 KPI assertions: Habituation loop cards and heatmaps rendered")
            
        elif page == "Rewards & Reversals":
            assert "4,685,761" in all_md, "Credited VE missing from Rewards page"
            assert "141,919" in all_md, "Reversed VE missing from Rewards page"
            assert "2.94%" in all_md, "Reversal rate 2.94% missing from Rewards page"
            assert len(at.dataframe) >= 1, "Offerwall inventory table missing"
            assert len(at.dataframe[0].value) == 10, "Top 10 offerwall table row count mismatch"
            print("  [PASS] Page 4 KPI assertions: Credited=4,685,761 VE, Reversed=141,919 VE, Rate=2.94%")
            
        elif page == "Wallet & Ledger Reconciliation":
            assert "3,500" in all_md, "Total transactions 3,500 missing from Wallet page"
            assert "456,210" in all_md, "Credit volume 456,210 missing from Wallet page"
            assert "1,876,150" in all_md, "Debit volume 1,876,150 missing from Wallet page"
            assert "0 Discrepancies" in all_md, "Row-level check 0 Discrepancies missing"
            assert "1,419,940" in all_md, "Macro net gap 1,419,940 missing from Wallet page"
            assert len(at.dataframe) >= 1, "Ledger transactions table missing"
            print("  [PASS] Page 5 KPI assertions: 3,500 txs, 456,210 Cr, 1,876,150 Dr, 0 Discrepancies, -1,419,940 Flow Gap")
            
        elif page == "Withdrawals & Payout Fulfillment":
            assert "1,200" in all_md, "Total withdrawals 1,200 missing from Withdrawals page"
            assert "1,012 Completed" in all_md, "Completed withdrawals 1,012 missing"
            assert "$3,693.50" in all_md, "Disbursed fiat $3,693.50 missing"
            assert "51 Rejections" in all_md, "Rejections count 51 missing"
            assert len(at.dataframe) >= 1, "Withdrawal queue table missing"
            print("  [PASS] Page 6 KPI assertions: 1,200 requests, 1,012 completed, $3,693.50 disbursed, 51 rejected")
            
        elif page == "Referrals & Viral Acquisition":
            assert "900" in all_md, "Links created 900 missing from Referrals page"
            assert "679 Joined" in all_md, "Registered referrals 679 missing"
            assert "1.17" in all_md, "Viral K-factor 1.17 missing"
            assert "37" in all_md, "Sybil blocks 37 missing"
            assert len(at.dataframe) >= 1, "Ambassador leaderboard table missing"
            print("  [PASS] Page 7 KPI assertions: 900 links, 679 joined, K=1.17, 37 sybil blocks")
            
        total_checks += 1
        
        # Test device filters on this page
        for dev in devices[1:]: # Test Android, iOS, Web
            at.selectbox[0].set_value(dev).run()
            if len(at.exception) > 0:
                print(f"  FAILED on page {page} with filter {dev}:")
                for e in at.exception:
                    print("    ", e.value)
                raise AssertionError(f"Exception on page {page} with device {dev}")
            total_checks += 1
        print(f"  [OK] Device filters (Android, iOS, Web) verified with 0 errors.")
        
        # Reset device filter to All
        at.selectbox[0].set_value("All").run()

    # -------------------------------------------------------------
    # 2. SYNCHRONIZED FILTER STATE ASSERTIONS
    # -------------------------------------------------------------
    print("\n---> Testing Synchronized Filter Header Assertions")
    # Default state: All devices
    at.radio[0].set_value("Executive Overview").run()
    md_all = " ".join([m.value for m in at.markdown])
    assert "12,000 Events" in md_all, "Default 12,000 events badge missing"
    assert "1,000 Users" in md_all, "Default 1,000 users badge missing"
    print("  [PASS] Default partition verified: 12,000 Events • 1,000 Users")
    
    # Filter: Android
    at.selectbox[0].set_value("Android").run()
    md_android = " ".join([m.value for m in at.markdown])
    assert "7,802 Events" in md_android, "Android 7,802 events badge missing"
    assert "637 Users" in md_android, "Android 637 users badge missing"
    print("  [PASS] Android filter verified: 7,802 Events • 637 Users")
    
    # Filter: iOS
    at.selectbox[0].set_value("iOS").run()
    md_ios = " ".join([m.value for m in at.markdown])
    assert "2,193 Events" in md_ios, "iOS 2,193 events badge missing"
    assert "182 Users" in md_ios, "iOS 182 users badge missing"
    print("  [PASS] iOS filter verified: 2,193 Events • 182 Users")
    
    # Filter: Web
    at.selectbox[0].set_value("Web").run()
    md_web = " ".join([m.value for m in at.markdown])
    assert "2,005 Events" in md_web, "Web 2,005 events badge missing"
    assert "181 Users" in md_web, "Web 181 users badge missing"
    print("  [PASS] Web filter verified: 2,005 Events • 181 Users")
    
    # Reset device filter
    at.selectbox[0].set_value("All").run()

    # -------------------------------------------------------------
    # 3. SINGLE-DAY DATE FILTER ASSERTION
    # -------------------------------------------------------------
    print("\n---> Testing Global Date Filter: Single Day Selection")
    single_date = [pd.to_datetime("2026-09-01").date(), pd.to_datetime("2026-09-01").date()]
    at.date_input[0].set_value(single_date).run()
    assert len(at.exception) == 0, f"Single-day filter failed: {[e.value for e in at.exception]}"
    md_single = " ".join([m.value for m in at.markdown])
    assert "117 Events" in md_single, "Single day 117 events badge missing"
    assert "113" in md_single, "Single day DAU 113 missing"
    print("  [PASS] Single-day filter verified: exactly 117 Events, DAU=113 users")
    total_checks += 1

    print(f"\n================================================================================")
    print(f"AppTest PASSED: All {total_checks} view states and deep assertions verified with 0 exceptions!")
    print(f"================================================================================")

if __name__ == "__main__":
    run_apptest_comprehensive_suite()
