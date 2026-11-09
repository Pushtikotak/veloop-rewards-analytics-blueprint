# VELOOP Rewards — Product Analytics Dashboard User Guide
**Author / Lead Data Analyst:** Pushti Kotak  
**Application Entry Point:** `app.py`  
**Localhost URL:** `http://localhost:8501`  
**Technology Stack:** Python, Streamlit, Plotly, Pandas  

---

## 1. Quick Start & Execution

To launch the dashboard application locally in any terminal:
```bash
streamlit run app.py
```
The application will automatically open in your default browser at `http://localhost:8501`.

---

## 2. Navigation & Layout Architecture

The dashboard is structured into **7 dedicated analytical pages** accessible via the collapsible left sidebar:

1. **Executive Overview:** High-level platform health, DAU/MAU stickiness, revenue vs. reward liability split, payout SLA compliance, and feature yield.
2. **User Analytics:** User acquisition funnel, onboarding progression, device/OS breakdown, geographic distribution, and interactive accounts ledger.
3. **Engagement & Gamification:** Habituation loops (Streaks, Spins, Quests), task activity hourly/day-of-week heatmap, streak decay curve, and level tiers.
4. **Rewards & Reversals:** Total VE distributed vs. reversed, partner chargeback rates, reversal root cause taxonomy, and top 10 high-yield offerwall campaigns.
5. **Wallet & Ledger Reconciliation:** Mathematical double-entry ledger verification, daily credit/debit inflow-outflow waterfall, transaction velocity, and real-time transaction ledger.
6. **Withdrawals & Payout Fulfillment:** Fulfillment queue health, success rate %, total fiat disbursed ($), processing time by payment rail, and rejection Pareto analysis.
7. **Referrals & Viral Acquisition:** 4-stage viral funnel, K-factor virality ratio, social share channels, anti-sybil IP collision defense, and power referrer leaderboard.

---

## 3. Global Interactive Filters

Located in the left sidebar:
- **Device Platform Filter:** Filter metrics across `All`, `Android`, `iOS`, or `Web`.
- **Date Range Picker:** Slice operational data between custom start and end dates.
- **Dynamic Caching:** Powered by `@st.cache_data` for instant multi-page responsiveness.

---

## 4. Exporting Data & Reports

Every page includes dedicated **📥 Download CSV Report** buttons:
- Export filtered user accounts (`users_analytics_report.csv`)
- Export top-yield offerwall inventory (`high_yield_tasks.csv`)
- Export double-entry ledger transactions (`wallet_ledger_audit.csv`)
- Export payout queue records (`withdrawals_queue.csv`)
- Export power referrer leaderboard (`top_referrers_leaderboard.csv`)
