"""
========================================================================================
VELOOP REWARDS — ANALYTICS DASHBOARD BLUEPRINT & WIREFRAME GENERATOR
Project: Product Analytics, Data Readiness & Data Management Blueprint
Author: Pushti Kotak | Deliverable: DELIV-15 (Work Package M)
Date: 2026-11-02
========================================================================================
"""

import os

WIREFRAME_DIR = "dashboards/wireframes"
os.makedirs(WIREFRAME_DIR, exist_ok=True)

def xml_escape(s):
    if not isinstance(s, str):
        s = str(s)
    return (s.replace("&", "&amp;")
             .replace("<", "&lt;")
             .replace(">", "&gt;")
             .replace('"', "&quot;")
             .replace("'", "&apos;"))

def generate_svg_wireframe(filename, title, kpis, charts):
    """
    Generates a clean vector SVG wireframe mockup for a dashboard.
    """
    esc_title = xml_escape(title.upper())
    
    svg_content = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1200 700" width="100%" height="100%">
    <style>
        .bg {{ fill: #F8FAFC; }}
        .header-bg {{ fill: #1B365D; }}
        .title {{ font-family: 'Segoe UI', Arial, sans-serif; font-size: 20px; font-weight: bold; fill: #FFFFFF; }}
        .subtitle {{ font-family: 'Segoe UI', Arial, sans-serif; font-size: 11px; fill: #94A3B8; }}
        .card {{ fill: #FFFFFF; stroke: #CBD5E1; stroke-width: 1.5; rx: 6; }}
        .kpi-title {{ font-family: 'Segoe UI', Arial, sans-serif; font-size: 11px; font-weight: 600; fill: #64748B; }}
        .kpi-val {{ font-family: 'Segoe UI', Arial, sans-serif; font-size: 20px; font-weight: bold; fill: #0F172A; }}
        .kpi-sub {{ font-family: 'Segoe UI', Arial, sans-serif; font-size: 10px; fill: #10B981; }}
        .chart-header {{ font-family: 'Segoe UI', Arial, sans-serif; font-size: 13px; font-weight: bold; fill: #1E293B; }}
        .chart-sub {{ font-family: 'Segoe UI', Arial, sans-serif; font-size: 10px; fill: #64748B; }}
        .bar-color {{ fill: #3B82F6; }}
        .line-color {{ stroke: #2563EB; stroke-width: 2.5; fill: none; }}
        .axis {{ stroke: #E2E8F0; stroke-width: 1; }}
        .legend {{ font-family: 'Segoe UI', Arial, sans-serif; font-size: 10px; fill: #475569; }}
    </style>

    <!-- Canvas Background -->
    <rect width="1200" height="700" class="bg"/>

    <!-- Top Navigation Bar -->
    <rect width="1200" height="60" class="header-bg"/>
    <text x="30" y="34" class="title">VELOOP REWARDS — {esc_title}</text>
    <text x="30" y="50" class="subtitle">Blueprint Specification &amp; Wireframe Mockup | Author: Pushti Kotak | Date: 2026-11-02</text>
    <rect x="1000" y="16" width="170" height="28" rx="4" fill="#0F172A"/>
    <text x="1085" y="34" text-anchor="middle" font-family="'Segoe UI', sans-serif" font-size="11px" font-weight="bold" fill="#38BDF8">SIMULATED BLUEPRINT</text>

    <!-- KPI Row (4 Cards) -->
    <g transform="translate(30, 80)">
"""
    # Generate 4 KPI cards
    card_width = 265
    gap = 26
    for idx, (label, val, note) in enumerate(kpis):
        x = idx * (card_width + gap)
        esc_label = xml_escape(label)
        esc_val = xml_escape(val)
        esc_note = xml_escape(note)
        svg_content += f"""
        <g transform="translate({x}, 0)">
            <rect width="{card_width}" height="75" class="card"/>
            <text x="16" y="24" class="kpi-title">{esc_label}</text>
            <text x="16" y="52" class="kpi-val">{esc_val}</text>
            <text x="250" y="52" text-anchor="end" class="kpi-sub">{esc_note}</text>
        </g>
"""

    svg_content += """    </g>

    <!-- Main Chart Grid (2x2 Layout) -->
    <g transform="translate(30, 180)">
"""
    # 4 Charts
    grid_w = 557
    grid_h = 230
    positions = [(0, 0), (583, 0), (0, 255), (583, 255)]

    for idx, (c_title, c_type, c_desc) in enumerate(charts):
        px, py = positions[idx]
        esc_c_title = xml_escape(c_title)
        esc_c_type = xml_escape(c_type)
        esc_c_desc = xml_escape(c_desc)
        svg_content += f"""
        <!-- Chart {idx+1}: {esc_c_title} -->
        <g transform="translate({px}, {py})">
            <rect width="{grid_w}" height="{grid_h}" class="card"/>
            <text x="20" y="28" class="chart-header">{esc_c_title}</text>
            <text x="20" y="44" class="chart-sub">{esc_c_type} | {esc_c_desc}</text>
            <line x1="20" y1="56" x2="{grid_w - 20}" y2="56" stroke="#F1F5F9" stroke-width="1.5"/>

            <!-- Chart Visual Mockup -->
            <rect x="40" y="80" width="{grid_w - 80}" height="120" fill="#F8FAFC" rx="4"/>
            <line x1="40" y1="180" x2="{grid_w - 40}" y2="180" class="axis"/>
            <line x1="40" y1="130" x2="{grid_w - 40}" y2="130" class="axis" stroke-dasharray="3,3"/>
            <line x1="40" y1="80" x2="{grid_w - 40}" y2="80" class="axis" stroke-dasharray="3,3"/>

            <!-- Mock visual bars / lines -->
            <rect x="70" y="120" width="35" height="60" class="bar-color" rx="2" fill-opacity="0.85"/>
            <rect x="135" y="100" width="35" height="80" class="bar-color" rx="2" fill-opacity="0.85"/>
            <rect x="200" y="90" width="35" height="90" class="bar-color" rx="2" fill-opacity="0.85"/>
            <rect x="265" y="110" width="35" height="70" class="bar-color" rx="2" fill-opacity="0.85"/>
            <rect x="330" y="85" width="35" height="95" class="bar-color" rx="2" fill-opacity="0.85"/>
            <rect x="395" y="95" width="35" height="85" class="bar-color" rx="2" fill-opacity="0.85"/>

            <!-- Line trend overlay -->
            <path d="M 87 115 Q 152 90, 217 80 T 347 75 T 412 85" class="line-color"/>
            <circle cx="217" cy="80" r="3.5" fill="#1D4ED8"/>
            <circle cx="347" cy="75" r="3.5" fill="#1D4ED8"/>
        </g>
"""

    svg_content += """    </g>
</svg>"""

    filepath = f"{WIREFRAME_DIR}/{filename}"
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(svg_content)
    print(f"Wireframe SVG generated: {filepath}")

def build_all_blueprints():
    # 1. Executive Overview
    generate_svg_wireframe(
        "01_executive_overview.svg", "Dashboard 1: Executive Overview",
        [("DAILY ACTIVE USERS (DAU)", "382", "+8.4% WoW"),
         ("COMPLETED TASKS", "3,489", "58.2% Conv"),
         ("NET REWARD LIABILITY", "$4,520 USD", "Settled VE"),
         ("PAYOUT SLA (<24H)", "96.4%", "Target >95%")],
        [("Active User & Session Trajectory", "Time-Series Dual Axis", "Daily Active Users vs. Active Sessions"),
         ("Revenue & Reward Liability Split", "Stacked Area Chart", "Partner Inflow vs. Credited User Liability"),
         ("Fulfillment & Cashout Health", "Multi-Bar Chart", "Requested vs. Completed vs. Rejected Cashouts"),
         ("Top Earning Modules Yield", "Horizontal Bar Chart", "Total Payout Volume by Product Feature")]
    )

    # 2. User Analytics
    generate_svg_wireframe(
        "02_user_analytics.svg", "Dashboard 2: User Analytics",
        [("TOTAL REGISTERED USERS", "1,000", "Simulated Base"),
         ("ONBOARDING CONVERSION", "80.0%", "Started to Done"),
         ("30-DAY RETENTION", "24.2%", "Benchmark >20%"),
         ("DORMANT RATIO", "10.0%", "14-29 Days Idle")],
        [("Acquisition Funnel Progression", "Funnel Chart", "Visits -> Registered -> Onboarded -> Activated"),
         ("Geographic User Distribution", "Choropleth Map / Bars", "Active User Share by Country (IN, US, GB)"),
         ("Signup Device & OS Breakdown", "Donut Chart", "Android Mobile (65%) vs. iOS vs. Web"),
         ("Cohort Retention Heatmap", "Matrix Heatmap", "Day 1, 7, 14, 30 Retention by Acquisition Week")]
    )

    # 3. Engagement
    generate_svg_wireframe(
        "03_engagement.svg", "Dashboard 3: Engagement",
        [("STICKINESS (DAU/MAU)", "23.8%", "Target >20%"),
         ("STREAK ADOPTION RATE", "64.2%", "Active Claims"),
         ("7-DAY STREAK MASTERY", "18.5%", "Habit Retained"),
         ("AVG SPINS PER USER", "2.4", "Daily Mini-Game")],
        [("Daily Habituation Loops", "Stacked Column Chart", "Daily Streaks vs. Spin Wheel vs. Quests"),
         ("Task Execution Hourly Heatmap", "Heatmap Grid", "Task Start Volume by Hour of Day & Day of Week"),
         ("Streak Continuance Curve", "Decay Step Line", "Drop-off Probability from Day 1 through Day 30"),
         ("Gamification Level Distribution", "Histogram", "Active User Count across Gamification Levels 1-10")]
    )

    # 4. Rewards
    generate_svg_wireframe(
        "04_rewards.svg", "Dashboard 4: Rewards",
        [("GROSS REWARD VOLUME", "745,200 VE", "All Sources"),
         ("AVG REWARD PER TASK", "154.2 VE", "~$0.15 USD"),
         ("REWARD REVERSAL RATE", "2.48%", "Target <3.0%"),
         ("CHARGEBACK LOSS", "$112.50", "30d Clawbacks")],
        [("Reward Credited by Source", "100% Stacked Bar", "Offerwalls vs. Streaks vs. Spins vs. Referrals"),
         ("Partner Chargeback Trends", "Clustered Column", "Gross Credited vs. Invalidation Reversals"),
         ("Reward Settlement Latency", "Box Plot / Distribution", "Elapsed Time between Task and Ledger Credit"),
         ("Top 10 High-Yield Campaigns", "Ranked Table", "Campaign Name, Provider, Total VE Distributed")]
    )

    # 5. Wallet
    generate_svg_wireframe(
        "05_wallet.svg", "Dashboard 5: Wallet",
        [("TOTAL LEDGER MUTATIONS", "3,500", "Double-Entry"),
         ("CIRCULATING SUPPLY", "1,240,000 VE", "Active Points"),
         ("PENDING / AVAILABLE RATIO", "0.28", "Healthy Liquidity"),
         ("LEDGER DISCREPANCY", "0.00", "100% Balanced")],
        [("Daily Inflow vs. Outflow", "Waterfall Chart", "Credits (+), Debits (-), Reversals, Net Delta"),
         ("Balance Segmentation Trend", "Stacked Area Chart", "Pending Escrow vs. Available Withdrawable VE"),
         ("Virtual Currency Velocity", "Line Chart", "Weekly Turnover of Circulating Virtual Tokens"),
         ("Ledger Transaction Type Mix", "Treemap Chart", "Volume Share by Transaction Type Enum")]
    )

    # 6. Withdrawals
    generate_svg_wireframe(
        "06_withdrawals.svg", "Dashboard 6: Withdrawals",
        [("TOTAL CASHOUT REQUESTS", "1,200", "$11,400 Gross"),
         ("MEDIAN SETTLEMENT TIME", "4.8 Hours", "SLA <24 Hours"),
         ("COMPLETION SUCCESS RATE", "82.5%", "Settled Clean"),
         ("GATEWAY REJECTION RATE", "5.0%", "KYC/Handle Error")],
        [("Withdrawal Lifecycle State Mix", "Donut Chart", "Completed vs. Processing vs. Rejected vs. Reversed"),
         ("Median Processing Time by Rail", "Horizontal Bar Chart", "PayPal vs. UPI Direct vs. Crypto vs. Gift Cards"),
         ("Pending Queue Age Monitoring", "Histogram / Area", "Count of Pending Cashouts by Age Buckets (<2h, 2-12h, >24h)"),
         ("Rejection Causal Taxonomy", "Pareto Chart", "Primary Root Causes for Failed Payout Dispatches")]
    )

    # 7. Referrals
    generate_svg_wireframe(
        "07_referrals.svg", "Dashboard 7: Referrals",
        [("REFERRAL INVITATIONS", "900", "Links Shared"),
         ("REGISTRATION CONVERSION", "75.0%", "Shared to Signup"),
         ("ACTIVATION CONVERSION", "36.4%", "Signup to Task"),
         ("EFFECTIVE VIRAL CAC", "$0.25 USD", "Per Active Lead")],
        [("4-Stage Referral Funnel", "Funnel Chart", "Created -> Registered -> Activated -> Converted"),
         ("Viral Sharing Channel Mix", "Pie Chart", "WhatsApp (45%) vs. Telegram (30%) vs. Direct Link"),
         ("Top 20 Power Referrers", "Leaderboard Table", "Referrer User ID, Total Invites, Activated Leads, Commission"),
         ("Sybil / Duplicate IP Detections", "Time-Series Column", "Referral Pairs Blocked by IP Collision Checks")]
    )

    # -------------------------------------------------------------
    # DAX MEASURES FILE (dashboards/dax_measures.dax)
    # -------------------------------------------------------------
    dax_code = """// ============================================================================
// VELOOP REWARDS — PRODUCTION POWER BI DAX MEASURES SPECIFICATION
// Project: Product Analytics, Data Readiness & Data Management Blueprint
// Author: Pushti Kotak | Deliverable: DELIV-15
// Date: 2026-11-02
// ============================================================================

// 1. CORE USER LIFECYCLE MEASURES
DAU := 
CALCULATE(
    DISTINCTCOUNT(fct_feature_events[user_id]),
    fct_feature_events[event_name] IN {
        "task_offer_started", "task_offer_completed", 
        "engagement_daily_claimed", "engagement_spin_completed", 
        "withdrawal_requested"
    }
)

MAU := 
CALCULATE(
    DISTINCTCOUNT(fct_feature_events[user_id]),
    DATESINPERIOD(dim_dates[date_id], LASTDATE(dim_dates[date_id]), -30, DAY),
    fct_feature_events[event_name] IN {
        "task_offer_started", "task_offer_completed", 
        "engagement_daily_claimed", "engagement_spin_completed", 
        "withdrawal_requested"
    }
)

Platform_Stickiness_Pct := 
DIVIDE([DAU], [MAU], 0)

New_User_Registrations := 
DISTINCTCOUNT(dim_users[user_id])

Onboarding_Completion_Rate_Pct := 
DIVIDE(
    CALCULATE(COUNTROWS(dim_users), dim_users[onboarding_completed_flag] = TRUE()),
    COUNTROWS(dim_users),
    0
)

// 2. TASK & EARNING MEASURES
Task_Starts_Count := 
COUNTROWS(fct_task_activity)

Task_Completions_Count := 
CALCULATE(
    COUNTROWS(fct_task_activity),
    fct_task_activity[activity_status] = "Completed"
)

Task_Completion_Rate_Pct := 
DIVIDE([Task_Completions_Count], [Task_Starts_Count], 0)

Gross_Advertiser_Revenue_USD := 
SUM(fct_task_activity[partner_payout_usd])

Average_Reward_Per_Completed_Task_VE := 
DIVIDE(
    CALCULATE(SUM(fct_rewards[amount]), fct_rewards[source_type] = "Offerwall_Task"),
    [Task_Completions_Count],
    0
)

// 3. REWARD & LIABILITY MEASURES
Total_Credited_Rewards_VE := 
CALCULATE(
    SUM(fct_rewards[amount]),
    fct_rewards[status] = "Credited"
)

Total_Reversed_Rewards_VE := 
CALCULATE(
    SUM(fct_rewards[amount]),
    fct_rewards[status] = "Reversed"
)

Reward_Reversal_Rate_Pct := 
DIVIDE([Total_Reversed_Rewards_VE], [Total_Credited_Rewards_VE], 0)

Net_Accrued_Reward_Liability_USD := 
SUM(dim_users[lifetime_ve_earned]) * 0.001 - SUM(dim_users[lifetime_usd_withdrawn])

// 4. WALLET & TRANSACTION MEASURES
Total_Wallet_Transactions_Count := 
COUNTROWS(fct_wallet_transactions)

Total_Credit_Volume_VE := 
CALCULATE(
    SUM(fct_wallet_transactions[amount]),
    fct_wallet_transactions[direction] = "CREDIT"
)

Total_Debit_Volume_VE := 
CALCULATE(
    SUM(fct_wallet_transactions[amount]),
    fct_wallet_transactions[direction] = "DEBIT"
)

Ledger_Audit_Check := 
[Total_Credit_Volume_VE] - [Total_Debit_Volume_VE]

// 5. WITHDRAWAL & PAYOUT MEASURES
Withdrawal_Requests_Count := 
COUNTROWS(fct_withdrawals)

Completed_Withdrawals_Count := 
CALCULATE(
    COUNTROWS(fct_withdrawals),
    fct_withdrawals[status] = "Completed"
)

Withdrawal_Completion_Rate_Pct := 
DIVIDE([Completed_Withdrawals_Count], [Withdrawal_Requests_Count], 0)

Withdrawal_Rejection_Rate_Pct := 
DIVIDE(
    CALCULATE(COUNTROWS(fct_withdrawals), fct_withdrawals[status] = "Rejected"),
    [Withdrawal_Requests_Count],
    0
)

Total_Fiat_Disbursed_USD := 
CALCULATE(
    SUM(fct_withdrawals[net_amount]),
    fct_withdrawals[status] = "Completed",
    fct_withdrawals[currency] = "USD"
)

Median_Withdrawal_Processing_Hours := 
MEDIANX(
    FILTER(fct_withdrawals, fct_withdrawals[status] = "Completed" && NOT(ISBLANK(fct_withdrawals[final_timestamp]))),
    DATEDIFF(fct_withdrawals[requested_timestamp], fct_withdrawals[final_timestamp], MINUTE) / 60.0
)

Payout_SLA_Compliance_Rate_Pct := 
DIVIDE(
    CALCULATE(
        COUNTROWS(fct_withdrawals),
        fct_withdrawals[status] = "Completed",
        DATEDIFF(fct_withdrawals[requested_timestamp], fct_withdrawals[final_timestamp], HOUR) <= 24
    ),
    [Completed_Withdrawals_Count],
    0
)

// 6. REFERRAL MEASURES
Total_Referral_Links_Created := 
COUNTROWS(fct_referrals)

Referral_Registered_Count := 
CALCULATE(
    COUNTROWS(fct_referrals),
    fct_referrals[referral_status] IN {"Registered", "Activated", "Converted"}
)

Referral_Activated_Count := 
CALCULATE(
    COUNTROWS(fct_referrals),
    fct_referrals[referral_status] IN {"Activated", "Converted"}
)

Referral_Activation_Rate_Pct := 
DIVIDE([Referral_Activated_Count], [Referral_Registered_Count], 0)

Viral_K_Factor := 
DIVIDE([Referral_Activated_Count], DISTINCTCOUNT(dim_users[user_id]), 0)
"""

    with open("dashboards/dax_measures.dax", "w", encoding="utf-8") as f:
        f.write(dax_code)
    print("DAX measures generated: dashboards/dax_measures.dax")

if __name__ == "__main__":
    build_all_blueprints()
