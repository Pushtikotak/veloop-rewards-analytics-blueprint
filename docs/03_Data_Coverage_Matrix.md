# Data Coverage Matrix
## VELOOP Rewards — Product Analytics, Data Readiness & Data Management Blueprint
**Deliverable Code:** `DELIV-03` (Work Package A4)  
**Author / Analyst:** Pushti Kotak  
**Document Classification:** Internal Technical Architecture / Matrix Specification  
**Date:** 02 November 2026  
**Companion File:** `workbooks/DELIV-03_Data_Coverage_Matrix.xlsx`  
**Status:** Complete & Verified  

---

## 1. Matrix Overview & Governance Guidelines

The **Data Coverage Matrix** serves as the authoritative operational blueprint connecting raw user actions and system operations with analytical data collection, event logging, business questions, and architectural priorities.

Every entry in this matrix is classified under the **Source & Evidence Discipline**:
* **Confirmed:** Backed by official VELOOP requirements or established product design.
* **Proposed:** Recommended engineering specification designed to eliminate identified architectural vulnerabilities.
* **To Be Verified:** Subject to final verification with engineering leads, payment gateways, or partner network technical teams.

Prioritization follows the rigorous standard mandated in Section 24 & 31:
* **Critical:** Operational non-negotiables without which core transaction integrity, ledger reconciliation, or fraud prevention fails.
* **High:** Required for core product funnel reporting, cohort retention, and operational decision-making.
* **Medium:** Optimizes feature performance, engagement loops, and gamification balancing.
* **Low:** Non-critical operational metrics and auxiliary content telemetry.

---

## 2. Complete Data Coverage Matrix

| Row ID | Product Area | User Action | System Action | Business Outcome | Data Required | Proposed Event Name | Ingestion Source | Core Business Question | Status | Priority |
|:---|:---|:---|:---|:---|:---|:---|:---|:---|:---|:---|
| **DCM-01** | **Identity** | Submits registration form | Validates input, hashes password, inserts user | User account created | `user_id`, `email_hash`, `country_code`, `device_type`, `reg_source`, `referral_code`, `timestamp` | `user_registered` | Backend API | What acquisition channels drive the highest initial registration volume? | **Confirmed** | **Critical** |
| **DCM-02** | **Identity** | Submits credentials / OAuth | Issues JWT, starts session timer | Session initialized | `user_id`, `session_id`, `auth_provider`, `app_version`, `ip_hash`, `timestamp` | `user_logged_in` | Backend API | What is the distribution of Daily Active Users (DAU) by platform? | **Confirmed** | **Critical** |
| **DCM-03** | **Identity** | Clicks 'Log Out' / App closed | Revokes JWT, flushes session state | Session terminated | `user_id`, `session_id`, `session_duration_sec`, `events_in_session_count`, `timestamp` | `user_logged_out` | Frontend SDK | What is the average active session duration per user segment? | **Proposed** | **High** |
| **DCM-04** | **Onboarding** | Views first onboarding step | Logs onboarding impression | Onboarding funnel started | `user_id`, `onboarding_flow_id`, `step_index`, `device_model`, `timestamp` | `onboarding_started` | Frontend SDK | What percentage of registered users actually initiate the tutorial? | **Confirmed** | **High** |
| **DCM-05** | **Onboarding** | Completes final onboarding step | Unlocks onboarding reward, sets flag | User primed for activation | `user_id`, `onboarding_flow_id`, `total_steps`, `completion_time_sec`, `timestamp` | `onboarding_completed` | Backend API | Does tutorial completion correlate with higher day-7 task retention? | **Confirmed** | **High** |
| **DCM-06** | **Task Engine** | Clicks category tab (Surveys/Games) | Filters available offers by user segment | Task discovery logged | `user_id`, `category_name`, `provider_filter`, `available_offers_count`, `timestamp` | `task_category_selected` | Frontend SDK | Which task categories receive the highest organic browsing interest? | **Proposed** | **Medium** |
| **DCM-07** | **Task Engine** | Taps on specific offer card | Fetches detailed offer terms and requirements | Offer detail viewed | `user_id`, `task_id`, `task_name`, `provider_id`, `reward_amount`, `reward_unit`, `timestamp` | `task_opened` | Frontend SDK | What is the click-through rate (CTR) from feed view to offer detail? | **Confirmed** | **High** |
| **DCM-08** | **Task Engine** | Taps 'Start Offer' button | Generates tracking click-ID, executes redirect | Task initiated | `user_id`, `task_id`, `provider_id`, `click_id`, `target_url`, `estimated_payout_usd`, `timestamp` | `task_started` | Backend API | What is the drop-off rate between initiating a task and partner callback? | **Confirmed** | **Critical** |
| **DCM-09** | **Task Engine** | Completes external survey/game | Receives server-to-server webhook callback | Task completed externally | `click_id`, `task_id`, `user_id`, `provider_id`, `external_tx_id`, `partner_status`, `timestamp` | `task_completed` | Partner Webhook | Which external offerwall partners deliver the highest completion volume? | **Confirmed** | **Critical** |
| **DCM-10** | **Task Engine** | Abandons task / fails qualification | Webhook receives disqualify / error response | Task failed / abandoned | `click_id`, `task_id`, `user_id`, `provider_id`, `failure_category`, `error_code`, `timestamp` | `task_failed` | Partner Webhook | What are the primary failure modes for external survey qualification? | **Confirmed** | **High** |
| **DCM-11** | **Reward Engine** | None (Automated verification) | Validates partner signature, posts credit ledger | Reward liability recognized | `reward_id`, `user_id`, `task_id`, `credit_amount`, `currency_unit`, `status`, `timestamp` | `reward_credited` | Backend Worker | What is the total monetary reward liability credited daily? | **Confirmed** | **Critical** |
| **DCM-12** | **Reward Engine** | None (Validation delay) | Flags transaction for manual or timer review | Reward placed in escrow | `reward_id`, `user_id`, `task_id`, `hold_period_hours`, `hold_reason`, `timestamp` | `reward_pending` | Backend Worker | What is the average pending settlement latency across offer networks? | **Confirmed** | **High** |
| **DCM-13** | **Reward Engine** | Partner disputes invalid lead | Deducts unearned balance, records debit | Financial loss prevented | `reversal_id`, `original_reward_id`, `user_id`, `reason_category`, `deduction_amount`, `timestamp` | `reward_reversed` | Backend Worker | What is the net chargeback and reversal rate per offerwall partner? | **Confirmed** | **Critical** |
| **DCM-14** | **Engagement** | Clicks 'Claim Daily Bonus' | Checks 24h timer, increments streak, credits bonus | Repeat daily habit reinforced | `user_id`, `streak_day_count`, `bonus_amount`, `bonus_unit`, `next_eligible_at`, `timestamp` | `daily_reward_claimed` | Backend API | Does maintaining a 7-day streak increase monthly task completion by $> 50\%$? | **Confirmed** | **High** |
| **DCM-15** | **Engagement** | Breaks daily login continuity | Evaluates streak status, resets count to zero | User risk of churn | `user_id`, `broken_streak_length`, `days_inactive`, `last_claimed_at`, `timestamp` | `streak_broken` | Backend Cron | What is the churn rate among users following a broken 5+ day streak? | **Proposed** | **Medium** |
| **DCM-16** | **Engagement** | Clicks 'Spin Wheel' | Validates spin token, generates RNG prize | Micro-reward distributed | `user_id`, `spin_id`, `prize_type`, `prize_amount`, `prize_unit`, `spins_remaining`, `timestamp` | `spin_completed` | Backend API | What is the average virtual payout cost per spin across active users? | **Confirmed** | **Medium** |
| **DCM-17** | **Gamification** | Reaches quest milestone condition | Evaluates quest criteria, sets status to completed | User achievement unlocked | `user_id`, `quest_id`, `quest_type`, `target_count`, `reward_xp`, `reward_gems`, `timestamp` | `mission_completed` | Backend Worker | Which gamified quests drive the strongest engagement uplift? | **Confirmed** | **Medium** |
| **DCM-18** | **Gamification** | Unlocks achievement criteria | Generates badge record, awards profile flair | Long-term loyalty fostered | `user_id`, `badge_id`, `badge_tier`, `prerequisite_metric`, `timestamp` | `badge_earned` | Backend Worker | Do badged users demonstrate higher lifetime value than unbadged users? | **Confirmed** | **Medium** |
| **DCM-19** | **Referrals** | Clicks 'Share Referral Code' | Generates trackable link with attribution slug | Viral acquisition hook deployed | `user_id`, `referral_code`, `share_platform`, `link_url`, `timestamp` | `referral_created` | Frontend SDK | Which messaging channels generate the most referral shares? | **Confirmed** | **High** |
| **DCM-20** | **Referrals** | Invitee creates account via link | Links referrer ID to new invitee user ID | Referral lead registered | `referral_id`, `referrer_user_id`, `referred_user_id`, `campaign_id`, `timestamp` | `referral_registered` | Backend API | What is the conversion rate from referral share to invitee registration? | **Confirmed** | **High** |
| **DCM-21** | **Referrals** | Referred user completes 1st task | Verifies qualification rules, releases bonus | Organic user activated | `referral_id`, `referrer_user_id`, `referred_user_id`, `qualifying_task_id`, `timestamp` | `referral_activated` | Backend Worker | What proportion of referred users reach active earning status? | **Confirmed** | **Critical** |
| **DCM-22** | **Referrals** | Referral criteria locked | Credits referrer bonus, marks referral converted | Referral acquisition complete | `referral_id`, `referrer_user_id`, `reward_amount`, `reward_unit`, `timestamp` | `referral_converted` | Backend Worker | What is the effective Customer Acquisition Cost (CAC) via referrals? | **Confirmed** | **High** |
| **DCM-23** | **Wallet** | Opens wallet view / ledger | Fetches user balance breakdown from database | User balance audited | `user_id`, `available_balance`, `pending_balance`, `currency_unit`, `timestamp` | `wallet_viewed` | Frontend SDK | How frequently do users check wallet balances prior to cashout? | **Proposed** | **Medium** |
| **DCM-24** | **Wallet** | Swaps virtual credits (VE to Cash) | Executes internal FX rate exchange, debits/credits | Currency conversion settled | `transaction_id`, `user_id`, `source_unit`, `source_amount`, `target_unit`, `target_amount`, `fx_rate` | `wallet_exchange_executed` | Backend API | What is the virtual currency velocity between earned VEs and cash equivalents? | **Proposed** | **High** |
| **DCM-25** | **Withdrawals** | Selects method, submits cashout | Checks minimum threshold, escrows funds | Payout request queued | `withdrawal_id`, `user_id`, `payout_method`, `requested_amount`, `fee_amount`, `net_amount`, `currency` | `withdrawal_requested` | Backend API | What is the total volume of pending withdrawal liabilities? | **Confirmed** | **Critical** |
| **DCM-26** | **Withdrawals** | Automated risk engine runs | Evaluates IP, velocity, fraud score; dispatches | Payout submitted to gateway | `withdrawal_id`, `user_id`, `fraud_score`, `risk_status`, `gateway_name`, `timestamp` | `withdrawal_processing` | Backend Worker | What percentage of withdrawals pass automated fraud screening? | **Confirmed** | **High** |
| **DCM-27** | **Withdrawals** | Payment gateway settles funds | Posts final debit ledger, notifies user | User value delivered | `withdrawal_id`, `user_id`, `gateway_tx_id`, `settlement_duration_sec`, `fee_deducted`, `timestamp` | `withdrawal_completed` | Gateway Webhook | What is the median payout settlement latency by payment method? | **Confirmed** | **Critical** |
| **DCM-28** | **Withdrawals** | Gateway rejects / declines payout | Unfreezes escrowed balance, credits user | Payout failed, funds refunded | `withdrawal_id`, `user_id`, `rejection_code`, `rejection_reason`, `refund_amount`, `timestamp` | `withdrawal_rejected` | Gateway Webhook | What are the most common gateway failure causes by payout provider? | **Confirmed** | **Critical** |
| **DCM-29** | **Support** | Submits missing credit inquiry | Creates ticket, binds `task_id` and screenshots | Dispute workflow initiated | `ticket_id`, `user_id`, `task_id`, `partner_id`, `claimed_amount`, `status`, `timestamp` | `support_ticket_created` | Backend API | Which third-party offerwall networks generate the highest dispute rates? | **Confirmed** | **High** |
| **DCM-30** | **Support** | Support agent verifies and settles | Issues manual credit adjustment, closes ticket | User trust preserved | `ticket_id`, `user_id`, `agent_id`, `resolution_type`, `adjusted_amount`, `resolution_time_sec` | `support_ticket_resolved` | Backend API | What is the median resolution time and payout cost for user disputes? | **Confirmed** | **Medium** |

---

## 3. Analytics Gap Cross-Reference & Priority Allocation

This matrix directly incorporates the resolution of the **12 Critical Analytics Gaps** established in `DELIV-02`:

```
+---------------------------------------------------------------------------------------------------+
| PRIORITY BREAKDOWN ACROSS 30 MATRIX ROWS:                                                         |
| - Critical Priority:  8 rows (26.7%) -> Core transaction, ledger, postback, and identity integrity|
| - High Priority:     15 rows (50.0%) -> Key funnel, retention, gamification, and compliance events |
| - Medium Priority:    7 rows (23.3%) -> Micro-interactions, browsing trends, and support metrics |
+---------------------------------------------------------------------------------------------------+
```

Each critical item is tied to an explicit engineering payload specification in the **Developer Analytics Handoff** (`DELIV-16`) and mapped to schema entities in the **Logical Data Model** (`DELIV-10`).

---
*End of Deliverable DELIV-03 — Data Coverage Matrix Specification.*
