"""
========================================================================================
VELOOP REWARDS — FINAL IMPLEMENTATION BACKLOG GENERATOR
Project: Product Analytics, Data Readiness & Data Management Blueprint
Author: Pushti Kotak | Deliverable: DELIV-22 (Section 26)
Date: 2026-11-02
========================================================================================
"""

import openpyxl
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter
import os

header_font = Font(name="Segoe UI", size=11, bold=True, color="FFFFFF")
header_fill = PatternFill(start_color="1B365D", end_color="1B365D", fill_type="solid")
title_font = Font(name="Segoe UI", size=13, bold=True, color="1B365D")
meta_font = Font(name="Segoe UI", size=9, italic=True, color="595959")
data_font = Font(name="Segoe UI", size=10, color="000000")
zebra_fill = PatternFill(start_color="F2F5F9", end_color="F2F5F9", fill_type="solid")
white_fill = PatternFill(start_color="FFFFFF", end_color="FFFFFF", fill_type="solid")
thin_border = Border(
    left=Side(style='thin', color="D9D9D9"),
    right=Side(style='thin', color="D9D9D9"),
    top=Side(style='thin', color="D9D9D9"),
    bottom=Side(style='thin', color="D9D9D9")
)

def create_styled_sheet(ws, sheet_title, headers, rows, tab_color=None):
    if tab_color:
        ws.sheet_properties.tabColor = tab_color
    ws.cell(row=1, column=1, value=sheet_title).font = title_font
    ws.cell(row=2, column=1, value="Author: Pushti Kotak | Project: VELOOP Rewards Analytics Blueprint | Date: 2026-11-02").font = meta_font
    ws.cell(row=3, column=1, value="ENGINEERING IMPLEMENTATION BACKLOG — PRIORITIZED SPRINT SPECIFICATION").font = meta_font
    
    start_row = 5
    for col_idx, header in enumerate(headers, 1):
        cell = ws.cell(row=start_row, column=col_idx, value=header)
        cell.font = header_font
        cell.fill = header_fill
        cell.alignment = Alignment(horizontal="center", vertical="center", wrap_text=True)
        cell.border = thin_border
        
    for r_idx, row_data in enumerate(rows, start_row + 1):
        is_zebra = (r_idx % 2 == 0)
        row_fill = zebra_fill if is_zebra else white_fill
        for c_idx, val in enumerate(row_data, 1):
            cell = ws.cell(row=r_idx, column=c_idx, value=val)
            cell.font = data_font
            cell.fill = row_fill
            cell.border = thin_border
            
            str_val = str(val).upper()
            if str_val in ['CRITICAL', 'HIGH', 'MEDIUM', 'LOW', 'PRE-LAUNCH', 'POST-LAUNCH']:
                cell.alignment = Alignment(horizontal="center", vertical="center")
                if str_val == 'CRITICAL':
                    cell.font = Font(name="Segoe UI", size=10, bold=True, color="9C0006")
                elif str_val == 'HIGH':
                    cell.font = Font(name="Segoe UI", size=10, bold=True, color="B25E00")
                elif str_val == 'PRE-LAUNCH':
                    cell.font = Font(name="Segoe UI", size=10, bold=True, color="006100")
            elif isinstance(val, (int, float)):
                cell.alignment = Alignment(horizontal="right", vertical="center")
            else:
                cell.alignment = Alignment(horizontal="left", vertical="center", wrap_text=True)
                
    ws.freeze_panes = ws[f'A{start_row + 1}']
    max_col_letter = get_column_letter(len(headers))
    ws.auto_filter.ref = f"A{start_row}:{max_col_letter}{start_row + len(rows)}"
    
    for col in ws.columns:
        max_len = 0
        col_letter = get_column_letter(col[0].column)
        for cell in col[start_row-1:]:
            if cell.value:
                val_str = str(cell.value)
                max_len = max(max_len, len(val_str.split('\n')[0]))
        ws.column_dimensions[col_letter].width = min(max(max_len + 4, 12), 48)

backlog_headers = [
    "Item ID", "Priority", "Feature / Requirement Name", "Architectural Reason & Technical Need", 
    "Core Dependency", "Responsible Engineering Owner", "Estimated Effort", "Launch Stage", "Acceptance Criteria Summary"
]

backlog_rows = [
    ["BLG-001", "Critical", "Stable User ID Architecture", 
     "Required for permanent cross-session tracking, lifetime analytics, and GDPR compliance decoupling.", 
     "Auth Service", "Backend / Identity Team", "5 SP", "Pre-launch", 
     "Canonical UUIDv4 user_id generated on account creation; immutable across profile updates."],

    ["BLG-002", "Critical", "Double-Entry Transaction Ledger", 
     "Eliminates race conditions and overwriting bugs; ensures user balance equals mathematical sum of credits/debits.", 
     "Wallet Service", "Backend / DBA", "8 SP", "Pre-launch", 
     "fct_wallet_transactions table committed with mandatory direction, balance_before, and balance_after."],

    ["BLG-003", "Critical", "Event Ingestion Deduplication (Redis)", 
     "Prevents duplicate crediting when mobile clients retry failed network requests on cellular connections.", 
     "API Gateway", "Platform / Infra Eng", "5 SP", "Pre-launch", 
     "Redis cache enforces 10-minute TTL on event_id; duplicates return HTTP 200 with DUPLICATE_IGNORED."],

    ["BLG-004", "Critical", "Outbound Click-ID Attribution", 
     "Ensures incoming partner postbacks can be mapped to internal user_id and task_id without attribution drops.", 
     "Click Router", "Backend / Partner Eng", "5 SP", "Pre-launch", 
     "Generates unique click_id; appends sub_id={user_id}&sub_id2={task_id} to external redirect URLs."],

    ["BLG-005", "Critical", "Withdrawal Escrow Locking State Machine", 
     "Prevents double-spending during cashouts by immediately locking requested funds in escrow status.", 
     "Payout Service", "Backend Core Team", "8 SP", "Pre-launch", 
     "Atomic database transaction deducts balance and creates WITHDRAWAL_ESCROW ledger row simultaneously."],

    ["BLG-006", "Critical", "PII Cryptographic Masking & RBAC", 
     "Prevents exposure of sensitive PayPal/UPI handles and IP addresses in analytical BI tables (GDPR/DPDP).", 
     "Security Layer", "Data Platform / Security", "5 SP", "Pre-launch", 
     "destination_hash and signup_ip_hash stored as SHA-256; analytical roles granted zero raw PII access."],

    ["BLG-007", "High", "Multi-State Balance Separation", 
     "Separates pending rewards under hold from withdrawable funds to prevent losses from advertiser chargebacks.", 
     "Wallet Service", "Backend Core Team", "5 SP", "Pre-launch", 
     "dim_users exposes available_balance, pending_balance, and escrow_balance; cashout checks available only."],

    ["BLG-008", "High", "4-Stage Referral Funnel Enforcement", 
     "Blocks sybil registration farming by crediting referral bonuses only after invitee completes a validated task.", 
     "Referral Engine", "Growth / Backend Eng", "5 SP", "Pre-launch", 
     "Referral bonus locked until referral_status transitions to Activated; self-referrals blocked via IP check."],

    ["BLG-009", "High", "Automated Daily Ledger Audit Script", 
     "Zero-tolerance monitoring job verifying mathematical balance consistency across all user wallets.", 
     "Data Warehouse", "Analytics Eng / DBA", "3 SP", "Pre-launch", 
     "Automated cron at 00:30 UTC checks balance discrepancies; triggers P0 alert if discrepancy > 0."],

    ["BLG-010", "High", "Partner Webhook HMAC Signature Validation", 
     "Protects platform from forged partner callbacks by cryptographically validating webhook signature headers.", 
     "Webhook Gateway", "Security / Backend Eng", "3 SP", "Pre-launch", 
     "Validates HMAC SHA-256 against partner secret; invalid signatures rejected with HTTP 401."],

    ["BLG-011", "High", "Micro-Batch ELT Pipeline (Bronze to Silver)", 
     "Automates ingestion from raw S3 compressed JSONL files into normalized PostgreSQL reporting warehouse.", 
     "S3 / dbt", "Data Platform Eng", "8 SP", "Pre-launch", 
     "Hourly dbt runner transforms raw payloads into dimensional fact tables with automated schema tests."],

    ["BLG-012", "High", "Core Power BI Dashboard Semantic Model", 
     "Implements standardized DAX measures and dimensional star-schema for Executive and Operations reporting.", 
     "Power BI", "BI Specialist / Analyst", "8 SP", "Pre-launch", 
     "7 dashboard views functional; DAX measures reconciled against raw SQL queries with zero variance."],

    ["BLG-013", "Medium", "Daily Streak Reset & Recovery Telemetry", 
     "Tracks streak continuity and provides 24-hour buffer window adjusted for user local timezone.", 
     "Streak Service", "Mobile / Backend Eng", "5 SP", "Post-launch", 
     "Streak evaluates against local timezone offset; streak_broken event emitted upon missed check-in."],

    ["BLG-014", "Medium", "Gamification Quest & Mission Engine", 
     "Instruments missions, badges, and XP level multipliers to drive long-term habituation.", 
     "Game Engine", "Product / Backend Eng", "5 SP", "Post-launch", 
     "Missions track real-time event triggers; badges unlocked automatically upon milestone reach."],

    ["BLG-015", "Medium", "Customer Support Dispute CRM Integration", 
     "Connects missing credit ticket submissions directly to partner postback logs for rapid agent resolution.", 
     "Support Desk", "Full-Stack Eng", "5 SP", "Post-launch", 
     "Support portal renders task_activity_id and partner click_id alongside user ticket."],

    ["BLG-016", "Medium", "Virtual Currency Swap Ledger (VE to USD)", 
     "Tracks internal points-to-cash conversions if platform introduces intermediate currency exchange.", 
     "Exchange Service", "Backend / Finance Eng", "5 SP", "Post-launch", 
     "Executes atomic currency conversion ledger entry with locked exchange rate."],

    ["BLG-017", "Low", "FAQ Article Impression & Helpfulness Tracking", 
     "Measures self-service support article effectiveness in reducing repetitive ticket volume.", 
     "Content CMS", "Frontend Web Eng", "2 SP", "Post-launch", 
     "Logs article_viewed and article_rated_helpful events for knowledge base optimization."],

    ["BLG-018", "Low", "App Exit Screen & Bounce Telemetry", 
     "Instruments client exit screen logging to identify screens causing user session terminations.", 
     "Mobile SDK", "Mobile Client Eng", "2 SP", "Post-launch", 
     "Emits user_logged_out with last_viewed_screen and session_duration_sec."]
]

def generate_markdown_backlog(filepath, headers, rows):
    with open(filepath, "w", encoding="utf-8") as f:
        f.write("# Final Implementation Backlog\n")
        f.write("## VELOOP Rewards — Product Analytics, Data Readiness & Data Management Blueprint\n")
        f.write("**Deliverable Code:** `DELIV-22` (Section 26 & Work Package T)  \n")
        f.write("**Author / Analyst:** Pushti Kotak  \n")
        f.write("**Document Classification:** Engineering Sprint Specification / Implementation Backlog  \n")
        f.write("**Date:** 02 November 2026  \n")
        f.write("**Companion File:** `workbooks/DELIV-22_Implementation_Backlog.xlsx`  \n")
        f.write("**Status:** Complete & Verified  \n\n")
        f.write("---\n\n")
        f.write("## 1. Backlog Governance & Launch Segmentation\n\n")
        f.write("In accordance with Section 26 of the VELOOP Internship Task Specification, this backlog formalizes the prioritized development requirements necessary to deploy the analytics blueprint. Work is segmented into two operational stages:\n")
        f.write("1. **Pre-Launch Gate (Critical & High Priority):** 12 core epics that MUST be fully tested, verified, and signed off in staging before production user traffic or commercial payouts are enabled.\n")
        f.write("2. **Post-Launch Optimizations (Medium & Low Priority):** 6 enhancement epics focused on secondary gamification loops, currency swaps, and support telemetry scheduled for subsequent sprints.\n\n")
        f.write("---\n\n")
        f.write("## 2. Prioritized Implementation Backlog Table (18 Epics)\n\n")
        
        f.write("| Item ID | Priority | Requirement Name | Core Reason & Architectural Need | Dependency | Owner | Effort | Launch Stage |\n")
        f.write("|:---|:---|:---|:---|:---|:---|:---:|:---:|\n")
        for r in rows:
            f.write(f"| **{r[0]}** | **{r[1]}** | **{r[2]}** | {r[3][:45]}... | `{r[4]}` | {r[5]} | {r[6]} | **{r[7]}** |\n")
        f.write("\n---\n\n")
        f.write("## 3. Detailed User Stories & Acceptance Criteria\n\n")
        
        for r in rows:
            f.write(f"### `{r[0]}`: {r[2]}\n")
            f.write(f"* **Priority:** **{r[1]}** | **Launch Stage:** **{r[7]}** | **Estimated Effort:** {r[6]}\n")
            f.write(f"* **Architectural Reason:** {r[3]}\n")
            f.write(f"* **System Dependencies:** `{r[4]}` | **Responsible Team:** {r[5]}\n")
            f.write(f"* **Acceptance Criteria:** {r[8]}\n\n")
            
        f.write("---\n*End of Deliverable DELIV-22 — Final Implementation Backlog.*\n")
    print(f"Saved: {filepath}")

if __name__ == "__main__":
    os.makedirs("workbooks", exist_ok=True)
    os.makedirs("docs", exist_ok=True)
    
    # 1. Excel Workbook
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Implementation_Backlog"
    create_styled_sheet(ws, "VELOOP REWARDS — IMPLEMENTATION BACKLOG (DELIV-22)", backlog_headers, backlog_rows, tab_color="1B365D")
    wb.save("workbooks/DELIV-22_Implementation_Backlog.xlsx")
    print("Saved: workbooks/DELIV-22_Implementation_Backlog.xlsx")
    
    # 2. Markdown File
    generate_markdown_backlog("docs/22_Implementation_Backlog.md", backlog_headers, backlog_rows)
