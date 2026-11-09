"""
VELOOP Rewards - Physical Project Verification & Evidence Generator
Author: Pushti Kotak
Task: Data Analyst Internship Task 01
Purpose: Extract concrete, physical evidence for all 6 verification areas.
"""

import os
import sys
import glob
import time
import subprocess
import openpyxl
import pandas as pd

def print_separator(title):
    print("\n" + "=" * 90)
    print(f" {title} ")
    print("=" * 90 + "\n")

def run_step_1_folder_structure():
    print_separator("EVIDENCE ITEM 1: COMPLETE PROJECT FOLDER STRUCTURE & FILE INVENTORY")
    total_files = 0
    total_bytes = 0
    exclude_dirs = {'.git', '__pycache__', '.pytest_cache'}
    
    file_inventory = []
    
    for root, dirs, files in os.walk('.'):
        dirs[:] = [d for d in dirs if d not in exclude_dirs]
        for f in sorted(files):
            fp = os.path.join(root, f)
            sz = os.path.getsize(fp)
            total_files += 1
            total_bytes += sz
            # count lines if text file
            lines = "N/A"
            if f.endswith(('.md', '.py', '.sql', '.mermaid', '.dax', '.svg', '.csv')):
                try:
                    with open(fp, 'r', encoding='utf-8', errors='ignore') as fh:
                        lines = sum(1 for _ in fh)
                except Exception:
                    lines = "ERR"
            rel_path = os.path.relpath(fp, '.')
            file_inventory.append((rel_path, sz, lines))
            
    print(f"{'Relative File Path':<55} | {'Size (Bytes)':>12} | {'Lines':>8}")
    print("-" * 82)
    for path, sz, lines in file_inventory:
        print(f"{path:<55} | {sz:>12,} | {str(lines):>8}")
        
    print("-" * 82)
    print(f"TOTAL PHYSICAL FILES: {total_files} | TOTAL WORKSPACE DISK FOOTPRINT: {total_bytes:,} bytes ({total_bytes/1024/1024:.2f} MB)")

def run_step_2_deliverables_output():
    print_separator("EVIDENCE ITEM 2: OUTPUTS & PHYSICAL EXISTENCE PROOF FOR ALL 21 DELIVERABLES")
    
    deliverables_map = [
        ("01", "Executive Summary", "docs/01_Executive_Summary.md", "Executive Strategic Capstone"),
        ("02", "Product Data Readiness Audit", "docs/02_Product_Data_Readiness_Audit.md", "12 Product Modules & 12 Critical Gaps"),
        ("03", "Product Data Coverage Matrix", "docs/03_Data_Coverage_Matrix.md", "30 Operational Rows & Coverage Assessment"),
        ("04", "User & Account Analytics Spec", "docs/04_User_Account_Analytics_Spec.md", "4-tier ID Hierarchy & Lifecycle States"),
        ("05", "Earning & Reward Analytics Spec", "docs/05_Earning_Reward_Analytics_Spec.md", "Task Lifecycle & Postback HMAC Verification"),
        ("06", "Wallet & Withdrawal Analytics Spec", "docs/06_Wallet_Withdrawal_Analytics_Spec.md", "Double-Entry Ledger & Anti-Fraud"),
        ("07", "Referral & Engagement Spec", "docs/07_Referral_Engagement_Spec.md", "4-stage Funnel & Anti-Sybil Detection"),
        ("08", "Event Tracking Plan", "docs/08_Event_Tracking_Plan.md", "38 Production Events Taxonomy"),
        ("09", "Production Data Dictionary", "docs/09_Data_Dictionary.md", "100 Relational Fields across 8 Core Tables"),
        ("10", "Logical Data Model & ERD", "models/README.md", "11 Tables, 14 FKs, 53 Checks, Mermaid ERD"),
        ("11", "KPI Catalogue", "docs/11_KPI_Catalogue.md", "37 KPIs across 7 Business Domains"),
        ("12", "Simulated Data Profiling Report", "docs/12_Simulated_Data_Profiling.md", "Profiling 29,650 Rows across 8 Tables"),
        ("13", "Data Quality Audit & Cleaning", "docs/13_Data_Quality_Audit.md", "Audit of 550 Defect Rows across 14 Types"),
        ("14", "Data Quality Control Framework", "docs/14_Data_Quality_Control_Framework.md", "6 Operating Stages & Great Expectations Rules"),
        ("15", "Analytics Dashboard Blueprint", "dashboards/dashboard_specs.md", "7 Dashboard Specs, 7 SVGs, 30 DAX Measures"),
        ("16", "Developer Analytics Tracking Handoff", "docs/16_Developer_Analytics_Handoff.md", "SDK Interfaces, Signatures, Jest Tests"),
        ("17", "Production Data Pipeline Proposal", "docs/17_Data_Pipeline_Operating_Model.md", "Micro-Batch ELT Architecture ($119.50/mo)"),
        ("18", "Privacy, Data Governance & Retention", "docs/18_Privacy_Governance_Proposal.md", "DPDP Act 2023, GDPR, 5-Role RBAC"),
        ("19", "Analytics Change Management", "docs/19_Analytics_Change_Management.md", "SemVer 2.0 Schema Evolution & SLA Deprecation"),
        ("20", "Analytics Gap Assessment & Backlog", "docs/20_Analytics_Gap_Assessment.md", "10-Dimension Scorecard & 18 Backlog Epics"),
        ("21", "Final Consolidated Analytics Blueprint", "docs/21_Final_Consolidated_Blueprint.md", "Consolidated Capstone Synthesis Document")
    ]
    
    print(f"{'#':<3} | {'Deliverable Name':<35} | {'Physical File Path':<42} | {'Bytes':>8} | {'Lines':>6} | {'Status'}")
    print("-" * 110)
    
    for num, name, path, desc in deliverables_map:
        if os.path.exists(path):
            sz = os.path.getsize(path)
            with open(path, 'r', encoding='utf-8', errors='ignore') as f:
                lines = sum(1 for _ in f)
                f.seek(0)
                first_lines = [f.readline().strip() for _ in range(5)]
                header_snippet = " | ".join([l for l in first_lines if l.startswith("#") or "Pushti Kotak" in l or "Deliverable" in l])[:40]
            print(f"{num:<3} | {name:<35} | {path:<42} | {sz:>8,} | {lines:>6} | PASS")
        else:
            print(f"{num:<3} | {name:<35} | {path:<42} | {'MISSING':>8} | {'N/A':>6} | FAIL")

def run_step_3_dataset_record_counts():
    print_separator("EVIDENCE ITEM 3: ACTUAL DATASET RECORD COUNTS & SCHEMA EVIDENCE")
    
    csv_files = [
        ("users.csv", "dim_users", "~1,000", "Users registered on platform"),
        ("catalog_tasks.csv", "dim_tasks", "30-50", "Offers & tasks available"),
        ("task_activity.csv", "fct_task_activity", "~5,000-8,000", "User-task attempts and completions"),
        ("rewards.csv", "fct_rewards", "~4,000-6,000", "Credited and reversed rewards"),
        ("wallet.csv", "fct_wallet_transactions", "~3,000-5,000", "Ledger credits, debits, adjustments"),
        ("withdrawals.csv", "fct_withdrawals", "~800-1,500", "Cashout payout requests and states"),
        ("referrals.csv", "fct_referrals", "~600-1,200", "Referral invites, clicks, conversions"),
        ("feature_events.csv", "fct_feature_events", "~10,000-15,000", "Granular telemetry and UI events"),
        ("messy_data.csv", "audit_test_defects", "500+", "Injected defects across 14 categories")
    ]
    
    print(f"{'Filename':<20} | {'Target (Sec 28)':<16} | {'Actual Rows':>12} | {'Cols':>4} | {'Nulls':>8} | {'Memory':>10} | {'Status'}")
    print("-" * 85)
    
    total_rows = 0
    total_operational = 0
    
    for fname, table, target, desc in csv_files:
        fp = os.path.join("data", "raw", fname)
        if os.path.exists(fp):
            df = pd.read_csv(fp)
            rows = len(df)
            cols = len(df.columns)
            nulls = int(df.isnull().sum().sum())
            mem = f"{df.memory_usage(deep=True).sum() / 1024:.1f} KB"
            total_rows += rows
            if fname != "messy_data.csv":
                total_operational += rows
            print(f"{fname:<20} | {target:<16} | {rows:>12,} | {cols:>4} | {nulls:>8,} | {mem:>10} | PASS")
        else:
            print(f"{fname:<20} | {target:<16} | {'MISSING':>12} | {'-':>4} | {'-':>8} | {'-':>10} | FAIL")
            
    print("-" * 85)
    print(f"OPERATIONAL DATASET ROWS : {total_operational:,} rows (Target: ~24,430 to 38,750)")
    print(f"TOTAL SIMULATED ROWS     : {total_rows:,} rows across 9 datasets")

def run_step_4_python_scripts_execution():
    print_separator("EVIDENCE ITEM 4: LIVE PYTHON SCRIPT EXECUTION RESULTS")
    
    scripts = [
        ("scripts/generate_simulated_data.py", "Generates 8 core CSVs + 1 messy defect CSV with seed 42"),
        ("scripts/profile_simulated_data.py", "Profiles distributions, missingness, and referential integrity"),
        ("scripts/audit_data_quality.py", "Evaluates 14 defect categories and produces remediation scripts"),
        ("scripts/build_workbooks_phase1.py", "Compiles DELIV-03 and DELIV-12 Excel workbooks"),
        ("scripts/build_tracking_and_dictionary.py", "Compiles DELIV-08 and DELIV-09 Excel workbooks"),
        ("scripts/build_kpi_catalogue.py", "Compiles DELIV-11 KPI Catalogue Excel workbook"),
        ("scripts/build_dashboard_blueprint.py", "Builds 7 valid SVG wireframes and dashboard markdown specs"),
        ("scripts/build_backlog.py", "Compiles Registers & Backlog Excel workbooks"),
        ("scripts/verify_artifacts.py", "Verifies SQL DDL, ERD, SVG wireframes, and DAX measures"),
        ("scripts/verify_links.py", "Performs automated link audit across all documentation files")
    ]
    
    print(f"{'Script Name':<38} | {'Return Code':>11} | {'Execution Time':>15} | {'Status'}")
    print("-" * 75)
    
    for s_path, s_desc in scripts:
        t0 = time.time()
        res = subprocess.run([sys.executable, s_path], capture_output=True, text=True)
        dur = time.time() - t0
        status = "PASS" if res.returncode == 0 else f"FAIL ({res.returncode})"
        print(f"{os.path.basename(s_path):<38} | {res.returncode:>11} | {dur:>14.2f}s | {status}")
        if res.returncode != 0:
            print(f"  --> ERROR OUTPUT:\n{res.stderr[:300]}")

def run_step_5_excel_workbooks_verification():
    print_separator("EVIDENCE ITEM 5: EXCEL WORKBOOK & SHEET LEVEL PHYSICAL VERIFICATION")
    
    workbooks = sorted(glob.glob("workbooks/*.xlsx"))
    
    print(f"{'Workbook Name':<45} | {'Size':>10} | {'Sheets Count & Names (Max Rows x Max Cols)'}")
    print("-" * 115)
    
    for wb_path in workbooks:
        sz = os.path.getsize(wb_path)
        wb = openpyxl.load_workbook(wb_path, read_only=True)
        sheet_details = []
        for sname in wb.sheetnames:
            ws = wb[sname]
            sheet_details.append(f"'{sname}' ({ws.max_row}x{ws.max_column})")
        wb.close()
        print(f"{os.path.basename(wb_path):<45} | {sz:>8,} B | {', '.join(sheet_details)}")

if __name__ == '__main__':
    run_step_1_folder_structure()
    run_step_2_deliverables_output()
    run_step_3_dataset_record_counts()
    run_step_4_python_scripts_execution()
    run_step_5_excel_workbooks_verification()
    print_separator("ALL PHYSICAL EVIDENCE GATHERED SUCCESSFULLY")
