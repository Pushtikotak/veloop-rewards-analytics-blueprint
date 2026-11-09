import openpyxl
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter
import os

def create_styled_workbook(filepath, sheet_configs):
    """
    Creates an enterprise-styled multi-sheet workbook.
    sheet_configs: dict of {sheet_name: {'headers': [...], 'rows': [...], 'tab_color': '...'}}
    """
    wb = openpyxl.Workbook()
    # Remove default sheet
    default_sheet = wb.active

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
    
    for idx, (title, cfg) in enumerate(sheet_configs.items()):
        ws = wb.create_sheet(title=title)
        if 'tab_color' in cfg:
            ws.sheet_properties.tabColor = cfg['tab_color']
            
        # Title block
        ws.cell(row=1, column=1, value=cfg.get('sheet_title', title)).font = title_font
        ws.cell(row=2, column=1, value=f"Author: Pushti Kotak | Project: VELOOP Rewards Analytics Blueprint | Generated: 2026-11-02").font = meta_font
        ws.cell(row=3, column=1, value="CLASSIFICATION: CONFIRMED / PROPOSED / TO BE VERIFIED | SIMULATED DATA TEST PROTOCOL").font = meta_font
        
        start_row = 5
        headers = cfg['headers']
        rows = cfg['rows']
        
        # Write Headers
        for col_idx, header in enumerate(headers, 1):
            cell = ws.cell(row=start_row, column=col_idx, value=header)
            cell.font = header_font
            cell.fill = header_fill
            cell.alignment = Alignment(horizontal="center", vertical="center", wrap_text=True)
            cell.border = thin_border
        
        # Write Data Rows
        for r_idx, row_data in enumerate(rows, start_row + 1):
            is_zebra = (r_idx % 2 == 0)
            row_fill = zebra_fill if is_zebra else white_fill
            for c_idx, val in enumerate(row_data, 1):
                cell = ws.cell(row=r_idx, column=c_idx, value=val)
                cell.font = data_font
                cell.fill = row_fill
                cell.border = thin_border
                
                # Alignments based on type/value
                if str(val).upper() in ['CRITICAL', 'HIGH', 'MEDIUM', 'LOW', 'CONFIRMED', 'PROPOSED', 'TO BE VERIFIED', 'OPEN', 'RESOLVED']:
                    cell.alignment = Alignment(horizontal="center", vertical="center")
                    # Priority badges
                    if str(val).upper() == 'CRITICAL':
                        cell.font = Font(name="Segoe UI", size=10, bold=True, color="9C0006")
                    elif str(val).upper() == 'HIGH':
                        cell.font = Font(name="Segoe UI", size=10, bold=True, color="B25E00")
                    elif str(val).upper() == 'CONFIRMED':
                        cell.font = Font(name="Segoe UI", size=10, bold=True, color="006100")
                elif isinstance(val, (int, float)):
                    cell.alignment = Alignment(horizontal="right", vertical="center")
                else:
                    cell.alignment = Alignment(horizontal="left", vertical="center", wrap_text=True)
                    
        # Set freeze pane & filters
        ws.freeze_panes = ws[f'A{start_row + 1}']
        max_col_letter = get_column_letter(len(headers))
        ws.auto_filter.ref = f"A{start_row}:{max_col_letter}{start_row + len(rows)}"
        
        # Auto-fit column widths with padding
        for col in ws.columns:
            max_len = 0
            col_letter = get_column_letter(col[0].column)
            # Inspect values in this column starting from header
            for cell in col[start_row-1:]:
                if cell.value:
                    val_str = str(cell.value)
                    max_len = max(max_len, len(val_str.split('\n')[0]))
            ws.column_dimensions[col_letter].width = min(max(max_len + 4, 12), 45)

    wb.remove(default_sheet)
    wb.save(filepath)
    print(f"Saved: {filepath}")

# ----------------- BUILD DELIV-03: DATA COVERAGE MATRIX -----------------
dcm_headers = [
    "Row ID", "Product Area", "User Action", "System Action", "Business Outcome", 
    "Data Required", "Proposed Event Name", "Ingestion Source", "Core Business Question", "Status", "Priority"
]

dcm_rows = [
    ["DCM-01", "Identity", "Submits registration form", "Validates input, hashes password, inserts user", "User account created", "user_id, email_hash, country_code, device_type, reg_source, referral_code, timestamp", "user_registered", "Backend API", "What acquisition channels drive the highest initial registration volume?", "Confirmed", "Critical"],
    ["DCM-02", "Identity", "Submits credentials / OAuth", "Issues JWT, starts session timer", "Session initialized", "user_id, session_id, auth_provider, app_version, ip_hash, timestamp", "user_logged_in", "Backend API", "What is the distribution of Daily Active Users (DAU) by platform?", "Confirmed", "Critical"],
    ["DCM-03", "Identity", "Clicks Log Out / App closed", "Revokes JWT, flushes session state", "Session terminated", "user_id, session_id, session_duration_sec, events_in_session_count, timestamp", "user_logged_out", "Frontend SDK", "What is the average active session duration per user segment?", "Proposed", "High"],
    ["DCM-04", "Onboarding", "Views first onboarding step", "Logs onboarding impression", "Onboarding funnel started", "user_id, onboarding_flow_id, step_index, device_model, timestamp", "onboarding_started", "Frontend SDK", "What percentage of registered users actually initiate the tutorial?", "Confirmed", "High"],
    ["DCM-05", "Onboarding", "Completes final onboarding step", "Unlocks onboarding reward, sets flag", "User primed for activation", "user_id, onboarding_flow_id, total_steps, completion_time_sec, timestamp", "onboarding_completed", "Backend API", "Does tutorial completion correlate with higher day-7 task retention?", "Confirmed", "High"],
    ["DCM-06", "Task Engine", "Clicks category tab (Surveys/Games)", "Filters available offers by user segment", "Task discovery logged", "user_id, category_name, provider_filter, available_offers_count, timestamp", "task_category_selected", "Frontend SDK", "Which task categories receive the highest organic browsing interest?", "Proposed", "Medium"],
    ["DCM-07", "Task Engine", "Taps on specific offer card", "Fetches detailed offer terms and requirements", "Offer detail viewed", "user_id, task_id, task_name, provider_id, reward_amount, reward_unit, timestamp", "task_opened", "Frontend SDK", "What is the click-through rate (CTR) from feed view to offer detail?", "Confirmed", "High"],
    ["DCM-08", "Task Engine", "Taps Start Offer button", "Generates tracking click-ID, executes redirect", "Task initiated", "user_id, task_id, provider_id, click_id, target_url, estimated_payout_usd, timestamp", "task_started", "Backend API", "What is the drop-off rate between initiating a task and partner callback?", "Confirmed", "Critical"],
    ["DCM-09", "Task Engine", "Completes external survey/game", "Receives server-to-server webhook callback", "Task completed externally", "click_id, task_id, user_id, provider_id, external_tx_id, partner_status, timestamp", "task_completed", "Partner Webhook", "Which external offerwall partners deliver the highest completion volume?", "Confirmed", "Critical"],
    ["DCM-10", "Task Engine", "Abandons task / fails qualification", "Webhook receives disqualify / error response", "Task failed / abandoned", "click_id, task_id, user_id, provider_id, failure_category, error_code, timestamp", "task_failed", "Partner Webhook", "What are the primary failure modes for external survey qualification?", "Confirmed", "High"],
    ["DCM-11", "Reward Engine", "None (Automated verification)", "Validates partner signature, posts credit ledger", "Reward liability recognized", "reward_id, user_id, task_id, credit_amount, currency_unit, status, timestamp", "reward_credited", "Backend Worker", "What is the total monetary reward liability credited daily?", "Confirmed", "Critical"],
    ["DCM-12", "Reward Engine", "None (Validation delay)", "Flags transaction for manual or timer review", "Reward placed in escrow", "reward_id, user_id, task_id, hold_period_hours, hold_reason, timestamp", "reward_pending", "Backend Worker", "What is the average pending settlement latency across offer networks?", "Confirmed", "High"],
    ["DCM-13", "Reward Engine", "Partner disputes invalid lead", "Deducts unearned balance, records debit", "Financial loss prevented", "reversal_id, original_reward_id, user_id, reason_category, deduction_amount, timestamp", "reward_reversed", "Backend Worker", "What is the net chargeback and reversal rate per offerwall partner?", "Confirmed", "Critical"],
    ["DCM-14", "Engagement", "Clicks Claim Daily Bonus", "Checks 24h timer, increments streak, credits bonus", "Repeat daily habit reinforced", "user_id, streak_day_count, bonus_amount, bonus_unit, next_eligible_at, timestamp", "daily_reward_claimed", "Backend API", "Does maintaining a 7-day streak increase monthly task completion by > 50%?", "Confirmed", "High"],
    ["DCM-15", "Engagement", "Breaks daily login continuity", "Evaluates streak status, resets count to zero", "User risk of churn", "user_id, broken_streak_length, days_inactive, last_claimed_at, timestamp", "streak_broken", "Backend Cron", "What is the churn rate among users following a broken 5+ day streak?", "Proposed", "Medium"],
    ["DCM-16", "Engagement", "Clicks Spin Wheel", "Validates spin token, generates RNG prize", "Micro-reward distributed", "user_id, spin_id, prize_type, prize_amount, prize_unit, spins_remaining, timestamp", "spin_completed", "Backend API", "What is the average virtual payout cost per spin across active users?", "Confirmed", "Medium"],
    ["DCM-17", "Gamification", "Reaches quest milestone condition", "Evaluates quest criteria, sets status to completed", "User achievement unlocked", "user_id, quest_id, quest_type, target_count, reward_xp, reward_gems, timestamp", "mission_completed", "Backend Worker", "Which gamified quests drive the strongest engagement uplift?", "Confirmed", "Medium"],
    ["DCM-18", "Gamification", "Unlocks achievement criteria", "Generates badge record, awards profile flair", "Long-term loyalty fostered", "user_id, badge_id, badge_tier, prerequisite_metric, timestamp", "badge_earned", "Backend Worker", "Do badged users demonstrate higher lifetime value than unbadged users?", "Confirmed", "Medium"],
    ["DCM-19", "Referrals", "Clicks Share Referral Code", "Generates trackable link with attribution slug", "Viral acquisition hook deployed", "user_id, referral_code, share_platform, link_url, timestamp", "referral_created", "Frontend SDK", "Which messaging channels generate the most referral shares?", "Confirmed", "High"],
    ["DCM-20", "Referrals", "Invitee creates account via link", "Links referrer ID to new invitee user ID", "Referral lead registered", "referral_id, referrer_user_id, referred_user_id, campaign_id, timestamp", "referral_registered", "Backend API", "What is the conversion rate from referral share to invitee registration?", "Confirmed", "High"],
    ["DCM-21", "Referrals", "Referred user completes 1st task", "Verifies qualification rules, releases bonus", "Organic user activated", "referral_id, referrer_user_id, referred_user_id, qualifying_task_id, timestamp", "referral_activated", "Backend Worker", "What proportion of referred users reach active earning status?", "Confirmed", "Critical"],
    ["DCM-22", "Referrals", "Referral criteria locked", "Credits referrer bonus, marks referral converted", "Referral acquisition complete", "referral_id, referrer_user_id, reward_amount, reward_unit, timestamp", "referral_converted", "Backend Worker", "What is the effective Customer Acquisition Cost (CAC) via referrals?", "Confirmed", "High"],
    ["DCM-23", "Wallet", "Opens wallet view / ledger", "Fetches user balance breakdown from database", "User balance audited", "user_id, available_balance, pending_balance, currency_unit, timestamp", "wallet_viewed", "Frontend SDK", "How frequently do users check wallet balances prior to cashout?", "Proposed", "Medium"],
    ["DCM-24", "Wallet", "Swaps virtual credits (VE to Cash)", "Executes internal FX rate exchange, debits/credits", "Currency conversion settled", "transaction_id, user_id, source_unit, source_amount, target_unit, target_amount, fx_rate", "wallet_exchange_executed", "Backend API", "What is the virtual currency velocity between earned VEs and cash equivalents?", "Proposed", "High"],
    ["DCM-25", "Withdrawals", "Selects method, submits cashout", "Checks minimum threshold, escrows funds", "Payout request queued", "withdrawal_id, user_id, payout_method, requested_amount, fee_amount, net_amount, currency", "withdrawal_requested", "Backend API", "What is the total volume of pending withdrawal liabilities?", "Confirmed", "Critical"],
    ["DCM-26", "Withdrawals", "Automated risk engine runs", "Evaluates IP, velocity, fraud score; dispatches", "Payout submitted to gateway", "withdrawal_id, user_id, fraud_score, risk_status, gateway_name, timestamp", "withdrawal_processing", "Backend Worker", "What percentage of withdrawals pass automated fraud screening?", "Confirmed", "High"],
    ["DCM-27", "Withdrawals", "Payment gateway settles funds", "Posts final debit ledger, notifies user", "User value delivered", "withdrawal_id, user_id, gateway_tx_id, settlement_duration_sec, fee_deducted, timestamp", "withdrawal_completed", "Gateway Webhook", "What is the median payout settlement latency by payment method?", "Confirmed", "Critical"],
    ["DCM-28", "Withdrawals", "Gateway rejects / declines payout", "Unfreezes escrowed balance, credits user", "Payout failed, funds refunded", "withdrawal_id, user_id, rejection_code, rejection_reason, refund_amount, timestamp", "withdrawal_rejected", "Gateway Webhook", "What are the most common gateway failure causes by payout provider?", "Confirmed", "Critical"],
    ["DCM-29", "Support", "Submits missing credit inquiry", "Creates ticket, binds task_id and screenshots", "Dispute workflow initiated", "ticket_id, user_id, task_id, partner_id, claimed_amount, status, timestamp", "support_ticket_created", "Backend API", "Which third-party offerwall networks generate the highest dispute rates?", "Confirmed", "High"],
    ["DCM-30", "Support", "Support agent verifies and settles", "Issues manual credit adjustment, closes ticket", "User trust preserved", "ticket_id, user_id, agent_id, resolution_type, adjusted_amount, resolution_time_sec", "support_ticket_resolved", "Backend API", "What is the median resolution time and payout cost for user disputes?", "Confirmed", "Medium"]
]

# ----------------- BUILD DELIV-21: ASSUMPTION & VERIFICATION REGISTER -----------------
src_headers = [
    "Ref ID", "Information / Product Fact", "Source Name & Origin", "Source Type", 
    "Date Checked", "Verification Status", "Analytical Significance & Operational Notes"
]

src_rows = [
    ["SRC-01", "Core mission: multi-sided rewards platform connecting users with advertisers, tasks, games, and payout partners.", "Data_Analyst_01.pdf (p. 1-5, 44)", "Official Task Spec", "2026-11-02", "Confirmed", "Establishes three-sided marketplace model: Advertiser -> VELOOP -> User."],
    ["SRC-02", "Core product areas: User accounts, earning activities, VEs, XP, Gems, Tokens, Spins, daily rewards, streaks, tasks, missions, badges, levels, referrals, wallet, withdrawals.", "Data_Analyst_01.pdf (p. 2)", "Official Task Spec", "2026-11-02", "Confirmed", "Forms foundational domain taxonomy for Logical Data Model and Event Tracking Plan."],
    ["SRC-03", "Earning lifecycle progression: Discovery -> Start -> Completion -> Validation -> Reward.", "Data_Analyst_01.pdf (p. 8, C1-C4)", "Official Task Spec", "2026-11-02", "Confirmed", "Mandates distinguishing task completion from reward crediting, and accounting for external partner postbacks."],
    ["SRC-04", "Withdrawal lifecycle progression: Requested -> Under Review / Processing -> Completed / Rejected / Reversed.", "Data_Analyst_01.pdf (p. 10-11, D1-D3)", "Official Task Spec", "2026-11-02", "Confirmed", "Establishes double-entry wallet reconciliation and asynchronous payout status transitions."],
    ["SRC-05", "Referral lifecycle progression: Referral Created -> User Registered -> User Activated -> Referral Converted.", "Data_Analyst_01.pdf (p. 12, E1)", "Official Task Spec", "2026-11-02", "Confirmed", "Prohibits equating registration with referral conversion; requires multi-stage attribution."],
    ["SRC-06", "Third-party offerwall networks: CPX Research, Torox, AdGate, Lootably, BitLabs, RevU, AyeT Studios, AdGem, TimeWall, Monlix, YourSurveys.", "Pushti VELOOP_Rewards_GPT_Industry_Research.pdf (p. 11, 14)", "Industry Benchmark", "2026-10-31", "Confirmed", "Partner integrations vary by region; analytics must isolate provider-specific postbacks and dispute rates."],
    ["SRC-07", "Monetization & unit economics benchmark: Advertiser gross payout vs. User reward share (hypothetical 65/35 split model) & reverse chargebacks.", "Pushti VELOOP_Rewards_GPT_Industry_Research.pdf (p. 15)", "Industry Benchmark", "2026-10-31", "Confirmed", "Mandates separating partner receivables, pending user rewards, and approved liability in wallet model."],
    ["SRC-08", "JumpTask credit economics: Fixed conversion of 1,000 credits = US$1.00; minimum cashout US$0.50.", "JumpTask Official Doc (jumptask.io/how-does-jumptask-work/)", "External Official", "2026-10-31", "Confirmed", "Informs VELOOP multi-currency reward exchange model (VEs, Gems, USD/INR conversion)."],
    ["SRC-09", "Freecash engagement mechanics: Streaks, leagues, level-based tiering, and region-locked payout rules.", "Freecash Support & Academy (freecash.com/academy/en/support/)", "External Official", "2026-10-31", "Confirmed", "Provides architecture for gamification entities (streaks, badges, leagues) and fraud prevention."],
    ["SRC-10", "Swagbucks everyday engagement: Search, magic receipts, daily polls, and tiered goal streak bonuses.", "Swagbucks Help Center (help.swagbucks.com/hc/en-us/)", "External Official", "2026-10-31", "Confirmed", "Guides daily check-in logic and non-task micro-engagement event tracking."],
    ["SRC-11", "Minimum Event Tracking Plan mandate: >= 25 meaningful events across 6 product domains.", "Data_Analyst_01.pdf (p. 13-15, F1)", "Official Task Spec", "2026-11-02", "Confirmed", "Minimum regulatory requirement for production event telemetry deliverable."],
    ["SRC-12", "Data Dictionary mandate: >= 75 meaningful fields across 12 metadata dimensions.", "Data_Analyst_01.pdf (p. 16, G1)", "Official Task Spec", "2026-11-02", "Confirmed", "Core metadata governance requirement across logical entities."],
    ["SRC-13", "KPI Catalogue mandate: >= 30 standardized KPIs with reproducible definitions and formulas.", "Data_Analyst_01.pdf (p. 18-20, I1)", "Official Task Spec", "2026-11-02", "Confirmed", "Formal metric governance standard prohibiting arbitrary operational targets."],
    ["SRC-14", "Simulated dataset working pack sizing: Users (1k), Tasks (6k), Rewards (5k), Wallet (3.5k), Withdrawals (1.2k), Referrals (900), Events (12k), Messy Data (500+).", "Data_Analyst_01.pdf (p. 36, Sec 28)", "Official Task Spec", "2026-11-02", "Confirmed", "Sizing parameters for synthetic testing generation and profiling scripts."],
    ["SRC-15", "Data quality defect taxonomy: 14 mandatory anomaly categories in Messy_Data sheet.", "Data_Analyst_01.pdf (p. 22, Sec 17)", "Official Task Spec", "2026-11-02", "Confirmed", "Benchmark for automated data quality detection and prevention frameworks."]
]

asm_headers = [
    "Assumption ID", "Category", "Item / Unknown Description", "Why It Matters to Analytics", 
    "Source Checked", "Risk Level", "Verification Owner", "Current Status", "Proposed Solution / Architectural Mitigation"
]

asm_rows = [
    ["ASM-001", "Identity", "Does client application generate and store persistent session_id across app states?", "Essential for calculating session duration, bounce rates, and session-level conversion.", "Official Docs", "High", "Client Eng Lead", "Proposed", "Implement client-side UUIDv4 session generator with 30-minute inactivity timeout window."],
    ["ASM-002", "Tracking", "Do third-party offerwall postbacks include deterministic click_id / sub_id?", "Critical for attribution reconciliation and detecting third-party partner tracking discrepancies.", "Competitor Review", "Critical", "Backend / Partner Eng", "To Be Verified", "Mandate dynamic query parameter sub_id={user_id} and sub_id2={task_id} in all outgoing offerwall redirect URLs."],
    ["ASM-003", "Currency", "Are VEs (VELOOP Earnings), XP, and Gems distinct virtual currencies with separate ledger balances?", "Dictates whether wallet schema requires multi-currency ledger or single-currency table with rate conversion.", "Spec p. 2", "High", "Product Manager", "Proposed", "Design multi-currency transaction model supporting unit IN ('VE', 'XP', 'GEM', 'TOKEN', 'USD', 'INR')."],
    ["ASM-004", "Ledger", "Is wallet balance calculated as materialized aggregate column or dynamically computed from transaction history?", "Materialized balance risks race conditions; dynamic calculation risks query latency at scale.", "Spec p. 10", "Critical", "Backend / DBA", "Proposed", "Implement double-entry transaction ledger with periodic snapshotting (daily user balance rollups)."],
    ["ASM-005", "Deduplication", "How does backend prevent duplicate event ingestion when mobile clients retry failed network requests?", "Prevents double-counting user registrations, task starts, and critical reward credits.", "Spec p. 27", "Critical", "Platform Eng", "Proposed", "Mandate client-side event_id (UUIDv4) and unique server-side idempotency constraint on (event_name, user_id, idempotency_key)."],
    ["ASM-006", "Task Status", "Can a task transition directly from task_started to reward_credited without intermediate validation event?", "Direct skips distort task completion funnels and prevent tracking validation latency.", "Spec p. 8-9", "High", "Product / QA", "To Be Verified", "Enforce strict state machine: Started -> Submitted -> Validating -> Completed -> Credited. Flag illegal transitions as data quality defects."],
    ["ASM-007", "Reversals", "What is the maximum operational lookback window for third-party offerwall chargebacks/reversals?", "Determines how long user balances must hold pending liability before becoming fully withdrawable.", "Competitor Doc p. 15", "High", "Finance / Ops", "To Be Verified", "Propose 30-day rolling reversal reserve for high-risk offers, releasing funds to withdrawable balance upon validation."],
    ["ASM-008", "Referrals", "What constitutes User Activated for referral reward qualification?", "Essential for defining referral conversion funnel and calculating referral CAC.", "Spec p. 12", "High", "Growth / Marketing", "Proposed", "Define User Activated as completing >= 1 validated task or reaching 100 VEs earned; document in KPI Catalogue."],
    ["ASM-009", "Identity/PII", "Does VELOOP capture IP addresses or precise GPS coordinates during user login/withdrawal?", "Highly sensitive personal data governed by GDPR/DPDP. Required for fraud detection but restricted for analytics.", "Spec p. 29", "High", "Legal / Privacy", "Proposed", "Mask IP addresses at ingestion (192.168.1.0/24) and convert to coarse ISO country/region codes; truncate geo coordinates to 2 decimal places."],
    ["ASM-010", "Ingestion", "What is planned ingestion architecture for product telemetry (batch ETL vs. event streaming)?", "Influences event latency, pipeline reliability, and dashboard refresh cadences.", "Spec p. 28", "Medium", "Data Eng Lead", "Proposed", "Propose lightweight serverless HTTP ingestion endpoint buffering to cloud object storage with hourly micro-batch ELT."],
    ["ASM-011", "Payout Fees", "Are withdrawal transaction fees deducted from user payout or absorbed by VELOOP?", "Impacts net payout calculations and withdrawal KPI formulas (net_payout_amount vs. requested_amount).", "Competitor Doc p. 12", "Medium", "Finance Lead", "To Be Verified", "Model explicit fee_amount and net_amount columns in withdrawals table to support both business models without schema changes."],
    ["ASM-012", "Gamification", "Are daily streaks reset based on UTC midnight or the user local timezone?", "Inconsistent streak resets trigger user disputes and corrupt retention analytics.", "Spec p. 2", "Medium", "Product / Eng", "Proposed", "Propose evaluating streaks against user stored timezone offset, falling back to UTC if timezone metadata is missing."]
]

if __name__ == "__main__":
    os.makedirs("workbooks", exist_ok=True)
    
    # 1. DELIV-03 Workbook
    create_styled_workbook("workbooks/DELIV-03_Data_Coverage_Matrix.xlsx", {
        "Data_Coverage_Matrix": {
            "sheet_title": "VELOOP REWARDS — DATA COVERAGE MATRIX (DELIV-03)",
            "headers": dcm_headers,
            "rows": dcm_rows,
            "tab_color": "1B365D"
        }
    })
    
    # 2. DELIV-21 Workbook
    create_styled_workbook("workbooks/DELIV-21_Assumption_Verification_Register.xlsx", {
        "Source_Register": {
            "sheet_title": "VELOOP REWARDS — MASTER SOURCE & EVIDENCE REGISTER (DELIV-21)",
            "headers": src_headers,
            "rows": src_rows,
            "tab_color": "006100"
        },
        "Assumption_Register": {
            "sheet_title": "VELOOP REWARDS — MASTER ASSUMPTION & VERIFICATION REGISTER (DELIV-21)",
            "headers": asm_headers,
            "rows": asm_rows,
            "tab_color": "B25E00"
        }
    })
