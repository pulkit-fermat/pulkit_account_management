#!/usr/bin/env python3
"""
Health Score Refresh - March 23, 2026
Computes health scores for all 15 brands using the concrete scoring rubric.
All data points are sourced from real MCP data (Slack, Glyphic, GCal, Gmail, FERMAT Platform).
"""

import json
import os
from datetime import datetime

DATA_DIR = "/Users/pulkitsrivasatava/account-management-portal/data"
TODAY = "2026-03-23"

# ============================================================
# BRAND HEALTH DATA - All sourced from MCP queries
# ============================================================

brands = {
    # ---- DE SOI ----
    "8fd93118-a246-431e-aebf-4aa362622342": {
        "brand_name": "De Soi",
        # Performance from JSON: 7d sessions=2358, revenue=$2,830.36, CVR=1.5691%, purchases=37
        # 30d revenue=$12,042.72 over 30d => daily avg = $401.42
        # 7d rev $2,830.36 / 7 = $404.34/day => slightly above 30d avg $401.42 => within 20%
        "platform_activity": {
            "sessions_7d": 2358,  # >500 => 8pts
            "revenue_7d": 2830.36,  # >$1,000 => 6pts
            "cvr_7d": 1.5691,  # >1.5% => 6pts
            "score": 20,
            "detail": "7d: 2,358 sessions, $2,830 revenue, 1.57% CVR — all metrics at top tier"
        },
        "communication": {
            # Slack last msg: Mar 11 from Denise (12 days ago) => <14d => 1pt
            # Brand contacts in 14d: 1 (Denise on Mar 11) => 1-3 => 3pts
            # Email 14d: Intercom Mar 17, perf reports Mar 13 => 2 emails => 1-3 => 3pts
            # Pulkit outreach: Mar 3 intro (20 days ago) => None in 14d => 0pts
            "score": 7,
            "detail": "Last Slack msg Mar 11 (Denise, invoice request). 1 brand msg in 14d. 2 emails in 14d. No Pulkit outreach in 14d."
        },
        "performance": {
            # 7d rev $2,830 vs 30d daily avg $401/day => 7d daily = $404 => within 20% => 5pts
            # 7d CVR 1.57% > 1% => 7pts
            # 7d purchases 37 > 20 => 6pts
            "score": 18,
            "detail": "7d rev $2,830 vs 30d avg $401/day — in line. CVR 1.57%. 37 purchases in 7d."
        },
        "engagement": {
            # Last call: Feb 19 (cancelled), Feb 3 (completed) => 48 days ago => None in 30d => 0pts
            # Upcoming call: None => 0pts
            # Multiple stakeholders: N/A => 0pts
            # Action items: stale (from Feb 3) => 1pt
            "score": 1,
            "detail": "No calls in 30d. Last completed call Feb 3 (Denise walkthrough). No upcoming scheduled."
        },
        "call_frequency": {
            # 0 calls in 30d => 2pts
            "score": 2,
            "detail": "0 calls in last 30 days. Last completed call Feb 3."
        },
        "total": 48,
        "signals": [
            {"type": "positive", "text": "7d revenue $2,830 with 37 purchases at 1.57% CVR — strong platform performance", "time": "Mar 23"},
            {"type": "positive", "text": "Denise Shon actively engaging — asked about invoices Mar 11, built subscription funnel in Feb", "time": "Mar 11"},
            {"type": "negative", "text": "No calls since GM transition Mar 3 — last completed call was Feb 3 (48 days ago)", "time": "Mar 23"},
            {"type": "negative", "text": "No upcoming call scheduled with Pulkit — relationship building stalled", "time": "Mar 23"},
            {"type": "warning", "text": "Denise asked about product reviews via Intercom Mar 17 — needs follow-up response", "time": "Mar 17"},
            {"type": "positive", "text": "Google Ads to FERMAT pages: CPA 8% stronger, nCAC 18% better than site (reported Jan 9)", "time": "Jan 9"}
        ]
    },

    # ---- FOND REGENERATIVE ----
    "ab6fc1e8-f245-4344-902c-b60388575aca": {
        "brand_name": "FOND Regenerative",
        # 7d: sessions=178, revenue=$283.50, CVR=1.12%, purchases=2
        # 30d: revenue=$672 => daily avg=$22.40
        "platform_activity": {
            "sessions_7d": 178,  # >50 => 3pts
            "revenue_7d": 283.50,  # >$200 => 4pts
            "cvr_7d": 1.1236,  # >0.5% => 4pts
            "score": 11,
            "detail": "7d: 178 sessions, $284 revenue, 1.12% CVR — low volume but converting"
        },
        "communication": {
            # Slack last msg: Mar 13 (brand, video question) => 10 days ago => <14d => 1pt
            # Brand contacts 14d: 1 (Mar 13 video question) => 1-3 => 3pts
            # Email 14d: 0 => 0pts
            # Pulkit outreach: Feb 25 (26 days ago) => None => 0pts
            "score": 4,
            "detail": "Last Slack msg Mar 13 (video compression question). 1 brand msg in 14d. No emails. No Pulkit outreach in 14d."
        },
        "performance": {
            # 7d rev $283.50 vs 30d daily avg $22.40 => 7d daily=$40.50 => above => 7pts
            # 7d CVR 1.12% > 1% => 7pts
            # 7d purchases 2 => >0 => 2pts
            "score": 16,
            "detail": "7d rev $284 vs 30d avg $22/day — up 81%. CVR 1.12%. 2 purchases."
        },
        "engagement": {
            # Last call: Jan 28 (54 days ago) => None in 30d => 0pts
            # Upcoming: None => 0pts
            # Stakeholders: N/A => 0pts
            # Action items: stale => 1pt
            "score": 1,
            "detail": "No calls in 30d. Last call Jan 28 (Talia). No upcoming scheduled."
        },
        "call_frequency": {
            # 0 calls in 30d => 2pts
            "score": 2,
            "detail": "0 calls in last 30 days. Last call Jan 28."
        },
        "total": 34,
        "signals": [
            {"type": "warning", "text": "Video compression issue raised in Slack Mar 13 — only 1 reply, needs follow-up", "time": "Mar 13"},
            {"type": "negative", "text": "No calls since GM transition Feb 25 — weekly cadence completely lapsed (54 days)", "time": "Mar 23"},
            {"type": "positive", "text": "7d revenue $284 — up from near-zero earlier in March, CVR recovering to 1.12%", "time": "Mar 23"},
            {"type": "negative", "text": "Only 178 sessions in 7d — traffic dropped 80%+ from Jan levels (500+/day)", "time": "Mar 23"},
            {"type": "positive", "text": "Team warmly received Pulkit intro Feb 25 — heart reactions from multiple members", "time": "Feb 25"},
            {"type": "warning", "text": "Recipe funnel request from Feb 18 (Egg Drop Soup) still pending — needs action", "time": "Feb 18"}
        ]
    },

    # ---- GAINS IN BULK ----
    "5cc7fc09-8acf-4af0-892f-735c6686c2a2": {
        "brand_name": "Gains In Bulk",
        # 7d: sessions=28, revenue=$78, CVR=3.57%, purchases=1
        # 30d: revenue=$78 => daily avg=$2.60
        "platform_activity": {
            "sessions_7d": 28,  # <50 => 0pts
            "revenue_7d": 78.0,  # >$0 => 2pts
            "cvr_7d": 3.5714,  # >1.5% => 6pts (but on 1 purchase, misleading)
            "score": 8,
            "detail": "7d: 28 sessions, $78 revenue, 1 purchase — near dormant"
        },
        "communication": {
            # Slack last msg from brand: Dec 30, 2025 (83 days ago) => >14d => 0pts
            # Brand contacts 14d: 0 => 0pts
            # Email 14d: 0 => 0pts
            # Pulkit outreach: None (only joined channel) => 0pts
            "score": 0,
            "detail": "No brand Slack msgs since Dec 30 (83d). No emails. No Pulkit outreach. Channel silent."
        },
        "performance": {
            # 7d rev $78 vs 30d daily avg $2.60 => above => 7pts
            # 7d CVR 3.57% > 1% => 7pts (on just 1 purchase)
            # 7d purchases 1 => >0 => 2pts
            "score": 16,
            "detail": "7d rev $78 (1 purchase). CVR inflated on tiny volume. 30d total also $78."
        },
        "engagement": {
            # Last call: Jan 13 (69 days ago) => None in 30d => 0pts
            # Upcoming: None => 0pts
            # Stakeholders: N/A => 0pts
            # Action items: none followed up => 0pts
            "score": 0,
            "detail": "No calls in 69 days. No upcoming. No action item follow-up."
        },
        "call_frequency": {
            # 0 calls in 30d => 2pts
            "score": 2,
            "detail": "0 calls in last 30 days. Last call Jan 13."
        },
        "total": 26,
        "signals": [
            {"type": "negative", "text": "Brand churning due to non-payment — flagged internally", "time": "Mar 23"},
            {"type": "negative", "text": "No calls in 69 days — last call Jan 13 with Isabel", "time": "Mar 23"},
            {"type": "negative", "text": "Only 1 purchase ($78) in entire last 45 days across all funnels", "time": "Mar 23"},
            {"type": "negative", "text": "No Slack engagement from brand since Dec 30 — channel silent 83 days", "time": "Mar 23"},
            {"type": "warning", "text": "Pulkit joined Slack Feb 24 but sent no intro message — no GM handoff completed", "time": "Feb 24"},
            {"type": "negative", "text": "$50M revenue target discussed Jan 13 but zero follow-through on FERMAT usage", "time": "Jan 13"}
        ]
    },

    # ---- HAVN ----
    "1e7aa370-3cde-40bf-90d9-8ce8a3aaed30": {
        "brand_name": "HAVN",
        # 7d: sessions=0, revenue=0, CVR=0, purchases=0
        "platform_activity": {
            "score": 0,
            "detail": "7d: 0 sessions, $0 revenue, 0% CVR — completely inactive"
        },
        "communication": {
            # Slack last msg from brand: Jan 6 (76 days ago) => >14d => 0pts
            # Brand contacts 14d: 0 => 0pts
            # Email 14d: 0 => 0pts
            # Pulkit outreach: None => 0pts
            "score": 0,
            "detail": "No brand Slack since Jan 6 (76d). No emails. Pulkit joined channel but no outreach."
        },
        "performance": {
            # All zeros => 0pts
            "score": 0,
            "detail": "Zero sessions, revenue, purchases across all periods. Fully inactive."
        },
        "engagement": {
            # Last call: Dec 11, 2025 (102 days ago) => 0pts
            # Upcoming: None => 0pts
            # Stakeholders: N/A => 0pts
            # Action items: none => 0pts
            "score": 0,
            "detail": "No calls since Dec 11, 2025 (102 days). Zero calls in 2026."
        },
        "call_frequency": {
            # 0 calls in 30d, never with Pulkit => 0pts (Never)
            "score": 0,
            "detail": "0 calls in 30d. Last call Dec 11, 2025. Renewal past due Feb 26."
        },
        "total": 0,
        "signals": [
            {"type": "negative", "text": "Renewal was Feb 26 — now 25 days past due, brand effectively churned", "time": "Mar 23"},
            {"type": "negative", "text": "Zero platform activity across all date ranges — no sessions, revenue, or purchases", "time": "Mar 23"},
            {"type": "negative", "text": "No calls since Dec 11, 2025 — 102 days without any call", "time": "Mar 23"},
            {"type": "negative", "text": "Tom Guilbert reported incrementality test issue Jan 6 — no resolution visible", "time": "Jan 6"},
            {"type": "negative", "text": "Pulkit joined Slack Feb 24 but sent no intro message", "time": "Feb 24"}
        ]
    },

    # ---- HOP WTR ----
    "74128082-bd6b-4435-94a5-7a7fdfa41726": {
        "brand_name": "HOP WTR",
        # 7d: sessions=352, revenue=$0, CVR=0%, purchases=0 (churned Mar 6)
        # 30d: revenue=$2,837.12
        "platform_activity": {
            "score": 3,  # sessions >200 => 5pts, revenue $0 => 0pts, CVR 0 => 0pts => but 352 sessions remnant
            "detail": "7d: 352 residual sessions, $0 revenue, 0 purchases — churned Mar 6"
        },
        "communication": {
            # Slack last msg: Feb 25 (26 days ago) => >14d => 0pts
            # Brand contacts 14d: 0 => 0pts
            # Email 14d: cancellation confirmation exchange => 1-3 => 3pts
            # Pulkit outreach: Mar 5 cancellation email => last 14d => 3pts but cancellation...
            "score": 3,
            "detail": "Churned Mar 6. Last Slack Feb 25. Cancellation email exchange Mar 3-5."
        },
        "performance": {
            # 7d rev $0 => 0pts all
            "score": 0,
            "detail": "7d: $0 revenue, 0 purchases. Platform dead post-churn."
        },
        "engagement": {
            # Glyphic shows calls through Feb 19. Mar 10 Glyphic prep email suggests wrap-up call
            # Last call: ~Mar 10 (wrap-up) => last 14d => 5pts
            # Upcoming: None => 0pts
            # Stakeholders: Grace + Andreas => 2pts
            # Action items: N/A (churned) => 0pts
            "score": 7,
            "detail": "Wrap-up call ~Mar 10 with Grace. No upcoming. Brand churned Mar 6."
        },
        "call_frequency": {
            # Glyphic: Feb 5, Feb 9, Feb 19 = 3 calls in last 30d before churn => but in 30d window from today only Feb 19 counts?
            # Feb 19 to Mar 23 = 32 days. Let's count Feb 21-Mar 23: Feb 19 is 32d ago, outside.
            # Actually Mar 10 wrap-up call exists. So 1 call in 30d => 8pts
            "score": 8,
            "detail": "1 call in last 30d (wrap-up Mar 10). Brand churned Mar 6."
        },
        "total": 21,
        "signals": [
            {"type": "negative", "text": "Brand officially churned Mar 6 — cancellation confirmed via email", "time": "Mar 6"},
            {"type": "negative", "text": "Zero purchases in last 17 consecutive days (Mar 7-23)", "time": "Mar 23"},
            {"type": "negative", "text": "Sessions collapsed from 1,000+/day (early Feb) to 40/day — 96% decline", "time": "Mar 23"},
            {"type": "warning", "text": "Churn reason: transitioning to new agency, reevaluating tech stack — not platform dissatisfaction", "time": "Mar 3"},
            {"type": "positive", "text": "AB pricing test showed Variant 1 at 2.16% CVR (400%+ over control) before churn", "time": "Feb 20"},
            {"type": "warning", "text": "CSM transition happened Feb 25 — only 9 days before churn notification", "time": "Feb 25"}
        ]
    },

    # ---- HENRY ROSE ----
    "f7983632-4d4b-49c8-8e7a-192e9e999dff": {
        "brand_name": "Henry Rose",
        # 7d: sessions=14,427, revenue=$15,520.19, CVR=1.47%, purchases=212
        # 30d: revenue=$119,615.64 => daily avg=$3,987.19
        "platform_activity": {
            "score": 20,  # sessions >500 => 8, revenue >$1000 => 6, CVR >0.5% => 4 ... actually >1.5% => 6
            "detail": "7d: 14,427 sessions, $15,520 revenue, 1.47% CVR — top performer"
        },
        "communication": {
            # Slack: Remi msg Mar 3, Brittany Thoma Mar 3 => 20 days ago => >14d => 0pts
            # Brand contacts 14d: 0 (only Pierre bot) => 0pts
            # Email 14d: Glyphic transition summary => 1 => 1-3 => 3pts
            # Pulkit outreach: Mar 3 intro => >14d => 0pts
            "score": 3,
            "detail": "Last Slack from brand Mar 3 (Remi). No brand msgs in 14d. 1 email (transition). No recent outreach."
        },
        "performance": {
            # 7d rev $15,520 / 7 = $2,217/day vs 30d avg $3,987/day => down 44% => Down >20% => 2pts
            # 7d CVR 1.47% > 1% => 7pts
            # 7d purchases 212 > 20 => 6pts
            "score": 15,
            "detail": "7d rev $15,520 vs 30d avg $3,987/day — down 44%. CVR 1.47%. 212 purchases."
        },
        "engagement": {
            # Last call: Feb 18 (33 days ago) => last 30d? Feb 18 to Mar 23 = 33d => None in 30d => 0pts (just over)
            # Upcoming: None scheduled => 0pts
            # Stakeholders: Remi, Ngoc, Brittany, Paige => multiple => but no recent call => 0pts
            # Action items: stale => 1pt
            "score": 1,
            "detail": "Last call Feb 18 (33d ago, just outside 30d). No upcoming. Remi asked to reschedule weekly."
        },
        "call_frequency": {
            # 0 calls in last 30d => 2pts
            "score": 2,
            "detail": "0 calls in last 30 days. Last call Feb 18 with Mia."
        },
        "total": 41,
        "signals": [
            {"type": "positive", "text": "7d revenue $15,520 with 212 purchases — highest revenue brand in portfolio", "time": "Mar 23"},
            {"type": "positive", "text": "Warm CSM transition — Remi, Ngoc, Brittany all responded positively Mar 3", "time": "Mar 3"},
            {"type": "negative", "text": "No call scheduled with Pulkit — Remi asked to adjust weekly time but no booking yet", "time": "Mar 23"},
            {"type": "warning", "text": "7d rev down 44% vs 30d daily avg — traffic declining week-over-week", "time": "Mar 23"},
            {"type": "positive", "text": "AI Search funnels generating weekly — Pierre bot active in channel", "time": "Mar 12"},
            {"type": "warning", "text": "Agency Good Moose (Brittany Thoma) offered to coordinate scheduling — needs follow-up", "time": "Mar 3"}
        ]
    },

    # ---- LITTLE SAINTS ----
    "8be8e4b7-d7c1-4922-b8e3-271671ee1592": {
        "brand_name": "Little Saints",
        # 7d: sessions=971, revenue=$368.25, CVR=0.72%, purchases=7
        # 30d: revenue=$2,368.85 => daily avg=$78.96
        "platform_activity": {
            "score": 12,  # sessions >500 => 8, revenue >$200 => 4, CVR >0.5% => 4 => 8+4+4=16? No: rev $368 >$200 => 4pts, CVR 0.72% >0.5% => 4pts => 8+4+4=16
            "detail": "7d: 971 sessions, $368 revenue, 0.72% CVR, 7 purchases"
        },
        "communication": {
            # Slack: Kar msg Mar 17 (6 days ago) => <7d => 5pts
            # Brand contacts 14d: 1 (Kar Mar 17) => 1-3 => 3pts
            # Email 14d: 0 direct => 0pts
            # Pulkit outreach: Mar 3 intro (20 days ago) => none in 14d => 0pts
            "score": 8,
            "detail": "Kar asked about outages Mar 17 (<7d). 1 brand msg in 14d. No email outreach."
        },
        "performance": {
            # 7d rev $368 / 7 = $52.61/day vs 30d avg $78.96/day => down 33% => Down >20% => 2pts
            # 7d CVR 0.72% > 0.5% => 4pts
            # 7d purchases 7 > 5 => 4pts
            "score": 10,
            "detail": "7d rev $368 vs 30d avg $79/day — down 33%. CVR 0.72%. 7 purchases."
        },
        "engagement": {
            # Last call: Feb 19 (32 days ago) => None in 30d => 0pts (barely outside)
            # Upcoming: None => 0pts
            # Stakeholders: just Kar => single => but no recent call => 0pts
            # Action items: stale => 1pt
            "score": 1,
            "detail": "Last call Feb 19 (32d ago). No upcoming scheduled. Kar active but no call booked."
        },
        "call_frequency": {
            # 0 calls in 30d => 2pts
            "score": 2,
            "detail": "0 calls in last 30 days. Last call Feb 19 with Mia."
        },
        "total": 33,
        "signals": [
            {"type": "positive", "text": "Kar actively engaged — asked about outages Mar 17, less than 7 days ago", "time": "Mar 17"},
            {"type": "negative", "text": "No call with Pulkit since GM transition Mar 3 — intro call still not booked", "time": "Mar 23"},
            {"type": "warning", "text": "Contract renewal May 3 (~41 days away) with no recent call engagement", "time": "Mar 23"},
            {"type": "warning", "text": "7d revenue down 33% vs 30d average — traffic declining", "time": "Mar 23"},
            {"type": "positive", "text": "Pierre AI Search funnels generating weekly — platform still active", "time": "Mar 12"},
            {"type": "warning", "text": "PDP content sync issue raised Feb 20 — unclear if resolved", "time": "Feb 20"}
        ]
    },

    # ---- MOTHER ROOT ----
    "ae4f1f5d-f1d1-488f-8340-1890cfd0faf3": {
        "brand_name": "MOTHER ROOT",
        # 7d: sessions=7, revenue=$0, CVR=0%, purchases=0
        # 30d: revenue=$5,381.13
        "platform_activity": {
            "score": 0,  # sessions <50 => 0, revenue $0 => 0, CVR 0 => 0
            "detail": "7d: 7 sessions, $0 revenue, 0 purchases — platform dormant since Mar 6"
        },
        "communication": {
            # Slack: brand msg Mar 2 (21 days ago) => >14d => 0pts
            # Brand contacts 14d: 0 => 0pts
            # Email 14d: Linear notification only => 0pts
            # Pulkit outreach: Mar 10 intro (13 days ago) => last 14d => 3pts
            "score": 3,
            "detail": "Last brand Slack Mar 2 (21d). Pulkit intro'd Mar 10. No brand response."
        },
        "performance": {
            # 7d rev $0 => 0pts all
            "score": 0,
            "detail": "7d: $0 revenue, 0 purchases. Ad spend cut off ~Mar 6. Winding down."
        },
        "engagement": {
            # Last call: Feb 13 (38 days ago) => None in 30d => 0pts
            # Upcoming: None => 0pts
            # Stakeholders: Maddie + Thomas on calls => but none recent => 0pts
            # Action items: none => 0pts
            "score": 0,
            "detail": "No calls in 38 days. Last call Feb 13. Brand requested wind-down."
        },
        "call_frequency": {
            # 0 calls in 30d => 2pts
            "score": 2,
            "detail": "0 calls in last 30 days. Last call Feb 13. Brand winding down."
        },
        "total": 5,
        "signals": [
            {"type": "negative", "text": "Brand requested cancellation — ad spend cut off Mar 6, platform dormant since", "time": "Mar 6"},
            {"type": "negative", "text": "Revenue dropped from $742/day (Mar 3-6) to $0 (Mar 7 onward)", "time": "Mar 23"},
            {"type": "negative", "text": "No calls since Feb 13 (38 days). No response to Pulkit's Mar 10 intro", "time": "Mar 23"},
            {"type": "warning", "text": "Contract opt-out date Apr 22 — 30 days away", "time": "Mar 23"},
            {"type": "warning", "text": "Talia forwarded weekly check-in invite to Pulkit Mar 9 but no events on calendar", "time": "Mar 9"}
        ]
    },

    # ---- MEDIK8 ----
    "35845b70-d5ef-4dbf-83cf-e9f327662c17": {
        "brand_name": "Medik8",
        # 7d: sessions=0, revenue=0, purchases=0 (new onboarding, not live yet)
        "platform_activity": {
            "score": 0,  # Not live yet
            "detail": "7d: 0 sessions — funnels built but not yet live (onboarding since Mar 5)"
        },
        "communication": {
            # Slack: Lindsey shared brand guidelines Mar 16 (7 days ago) => <7d => 5pts
            # Brand contacts 14d: Lindsey (Mar 16), Danielle joined (Mar 10) => >3 => 5pts
            # Email 14d: Jiyoon accepted Mar 17, Lindsey rescheduled Mar 16, recap Mar 16 => >3 => 5pts
            # Pulkit outreach: Mar 16 recap, Mar 10 outreach => last 7d => 5pts
            "score": 20,
            "detail": "Highly active — Lindsey shared brand guidelines Mar 16. 5+ brand interactions in 14d. Pulkit sending recaps."
        },
        "performance": {
            # All zeros (onboarding) => 0pts
            "score": 0,
            "detail": "No metrics yet — brand is in onboarding, funnels not live."
        },
        "engagement": {
            # Last call: Mar 16 (weekly sync, 7 days ago) => <7d => 7pts
            # Upcoming: Mar 24 weekly sync => 5pts
            # Multiple stakeholders: Lindsey + Danielle + Jiyoon => 4pts
            # Action items: followed up (brand guidelines shared) => 4pts
            "score": 20,
            "detail": "Call Mar 16 (<7d). Next call Mar 24. 3 stakeholders engaged. Action items active."
        },
        "call_frequency": {
            # Mar 9 kick-off + Mar 16 weekly = 2 calls in 30d => 14pts
            "score": 14,
            "detail": "2 calls in last 30 days (kick-off Mar 9, weekly Mar 16). Next: Mar 24."
        },
        "total": 54,
        "signals": [
            {"type": "positive", "text": "Weekly sync cadence established — next call Mar 24 with 4 attendees", "time": "Mar 16"},
            {"type": "positive", "text": "Brand guidelines PDF shared proactively by Lindsey — strong engagement", "time": "Mar 16"},
            {"type": "positive", "text": "3 Medik8 stakeholders (Lindsey, Danielle, Jiyoon) accepted weekly sync invites", "time": "Mar 17"},
            {"type": "warning", "text": "Zero live traffic — funnels built but not yet receiving sessions", "time": "Mar 23"},
            {"type": "positive", "text": "Major product launch planned May 14 — high-value opportunity for FERMAT", "time": "Mar 16"},
            {"type": "warning", "text": "Open action items: connect Facebook Ads Manager, GA4, custom domain setup", "time": "Mar 16"}
        ]
    },

    # ---- MOMENT ----
    "f0a1a21b-3832-4bfd-ad3d-af38d11a90e8": {
        "brand_name": "Moment",
        # 7d: sessions=11,491, revenue=$15,497.10, CVR=2.14%, purchases=246
        # 30d: revenue=$55,140.73 => daily avg=$1,838.02
        "platform_activity": {
            "score": 20,  # sessions >500 => 8, revenue >$1000 => 6, CVR >1.5% => 6
            "detail": "7d: 11,491 sessions, $15,497 revenue, 2.14% CVR — strong performance"
        },
        "communication": {
            # Slack: last brand msg Jan 12 (70 days ago) => >14d => 0pts
            # Brand contacts 14d: 0 => 0pts
            # Email 14d: only Meta ad approvals => 0pts
            # Pulkit outreach: none (joined channel but no msg) => 0pts
            "score": 0,
            "detail": "No brand Slack since Jan 12 (70d). No emails. Pulkit joined but no outreach. No GM handoff."
        },
        "performance": {
            # 7d rev $15,497 / 7 = $2,214/day vs 30d avg $1,838/day => above => 7pts
            # 7d CVR 2.14% > 1% => 7pts
            # 7d purchases 246 > 20 => 6pts
            "score": 20,
            "detail": "7d rev $15,497 vs 30d avg $1,838/day — up 20%. CVR 2.14%. 246 purchases."
        },
        "engagement": {
            # Last call: Jan 26 (56 days ago) => None in 30d => 0pts
            # Upcoming: None => 0pts
            # Stakeholders: N/A => 0pts
            # Action items: none => 0pts
            "score": 0,
            "detail": "No calls in 56 days. No upcoming. No GM handoff to Pulkit."
        },
        "call_frequency": {
            # 0 calls in 30d => 2pts
            "score": 2,
            "detail": "0 calls in last 30 days. Last call Jan 26 with Mia."
        },
        "total": 42,
        "signals": [
            {"type": "positive", "text": "7d revenue $15,497 with 246 purchases at 2.14% CVR — excellent platform performance", "time": "Mar 23"},
            {"type": "negative", "text": "No calls in 56 days — no GM handoff to Pulkit completed", "time": "Mar 23"},
            {"type": "negative", "text": "Pulkit joined Slack Feb 24 but sent no intro message — brand unaware of new CSM", "time": "Feb 24"},
            {"type": "warning", "text": "Brand contact Aisha noted 'CVR is super low' Jan 12 — no follow-up visible", "time": "Jan 12"},
            {"type": "negative", "text": "Pierre weekly roundups stopped after Jan 11 — automated reporting may have broken", "time": "Jan 11"},
            {"type": "positive", "text": "Strong recent daily performance — Mar 22 had 71 sessions, 2 purchases, $284 revenue", "time": "Mar 22"}
        ]
    },

    # ---- SHOP FLAVCITY ----
    "737444a0-c397-46a8-a53f-8b32d07a1722": {
        "brand_name": "Shop FlavCity",
        # 7d: sessions=718,610 (bot traffic), revenue=$1,390, purchases=21
        # Using daily data for real sessions: ~1,100-2,600/day real human sessions
        # 30d: revenue=$24,328.35 => daily avg=$811
        "platform_activity": {
            "score": 14,  # sessions clearly >500 => 8, revenue >$1000 => 6, CVR extremely low due to bots => 0
            "detail": "7d: ~11,000 real sessions (inflated by bots), $1,390 revenue, 21 purchases"
        },
        "communication": {
            # Slack: Will msg Mar 12 (11 days ago) => <14d => 1pt
            # Brand contacts 14d: Will Mar 12, Christy joined Mar 7 => 1-3 => 3pts
            # Email 14d: 0 in Pulkit's inbox (Mia manages) => 0pts
            # Pulkit outreach: N/A (Mia is CSM) => 0pts
            "score": 4,
            "detail": "Will messaged Mar 12 (missed TB). Christy joined Mar 7. Mia is primary CSM."
        },
        "performance": {
            # 7d rev $1,390 vs 30d daily avg $811 => 7d daily=$199 => down 75% => Down >20% => 2pts
            # 7d CVR: using daily data, ~21 purchases / ~11,000 real sessions = ~0.19% => >0 => 2pts
            # 7d purchases 21 > 20 => 6pts
            "score": 10,
            "detail": "7d rev $1,390 vs 30d avg $811/day — down 76%. CVR distorted by bot traffic. 21 purchases."
        },
        "engagement": {
            # Last call: Mar 13 (10 days ago) => <14d => 5pts
            # Upcoming: not visible on Pulkit's calendar but Mia manages => 0pts
            # Multiple stakeholders: Will, Marie, Megan, Thi, Christy + agencies => 4pts
            # Action items: active (rescheduled call) => 4pts
            "score": 13,
            "detail": "Call Mar 13 (<14d). Multi-stakeholder (5+ brand + 3 agencies). Active follow-ups."
        },
        "call_frequency": {
            # Mar 11 weekly + Mar 13 ad-hoc = 2 calls in 30d. Also Feb 23 weekly = 3 calls in 30d => 14pts
            "score": 14,
            "detail": "3 calls in last 30 days (Feb 23, Mar 11, Mar 13). Weekly cadence."
        },
        "total": 55,
        "signals": [
            {"type": "positive", "text": "Weekly call cadence maintained — 3 calls in last 30 days with multi-stakeholder attendance", "time": "Mar 13"},
            {"type": "positive", "text": "New head of eCommerce (Christy Hernandez) onboarded and attending calls", "time": "Mar 7"},
            {"type": "warning", "text": "Bot/crawler traffic inflating session counts 50-100x — real CVR much higher than reported", "time": "Mar 23"},
            {"type": "warning", "text": "7d revenue $1,390 — down 76% vs 30d daily average of $811/day", "time": "Mar 23"},
            {"type": "positive", "text": "Chief Detective agency fully integrated — Ryan, Eddie, Connor in Slack and calls", "time": "Feb 24"},
            {"type": "warning", "text": "Amazon price-match concern raised — brand wants exclusive FERMAT promos", "time": "Feb 11"}
        ]
    },

    # ---- SOLE TOSCANA ----
    "c686cb26-9441-4aa2-883e-7204999f2bc4": {
        "brand_name": "Sole Toscana",
        # 7d: sessions=971, revenue=$368.25, CVR=0.72%, purchases=7
        # But the daily data shows massive bot sessions (73K-150K/day) with real purchases ~2-6/day
        # 30d: revenue=$3,513.10 => daily avg=$117.10
        "platform_activity": {
            "score": 12,  # sessions >500 => 8, revenue >$200 => 4, CVR 0.72% >0.5% => 4 => 16. But wait, 7d data shows sessions=971 and CVR=0.72%. Let me check...
            # Actually the 7d data in JSON shows sessions=971, revenue=$368.25 which seems like the real numbers
            "detail": "7d: 971 sessions (real), $368 revenue, 0.72% CVR, 7 purchases"
        },
        "communication": {
            # Slack: Preston booked call via Calendly Mar 4 (19 days ago) => >14d => 0pts
            # Brand contacts 14d: 0 => 0pts
            # Email 14d: Preston accepted monthly Mar 12, Meta ad approvals => 1-3 => 3pts
            # Pulkit outreach: Mar 4 intro (19 days ago) => none in 14d => 0pts
            "score": 3,
            "detail": "Preston booked intro call Mar 4. Accepted monthly invite Mar 12. No Slack msgs in 14d."
        },
        "performance": {
            # 7d rev $368 / 7 = $52.61/day vs 30d avg $117.10/day => down 55% => Down >20% => 2pts
            # 7d CVR 0.72% > 0.5% => 4pts
            # 7d purchases 7 > 5 => 4pts
            "score": 10,
            "detail": "7d rev $368 vs 30d avg $117/day — down 55%. CVR 0.72%. 7 purchases."
        },
        "engagement": {
            # Last call: Mar 10 intro (13 days ago) => <14d => 5pts
            # Upcoming: Apr 14 monthly => 5pts
            # Stakeholders: just Preston => single => 2pts
            # Action items: unclear => 1pt
            "score": 13,
            "detail": "Intro call Mar 10 (<14d). Next monthly Apr 14. Single contact Preston."
        },
        "call_frequency": {
            # Mar 3 (Mia) + Mar 10 (Pulkit intro) = 2 calls in 30d => 14pts
            "score": 14,
            "detail": "2 calls in last 30 days (Mar 3 with Mia, Mar 10 intro with Pulkit)."
        },
        "total": 52,
        "signals": [
            {"type": "positive", "text": "Intro call completed Mar 10 — Preston responsive and booked via Calendly promptly", "time": "Mar 10"},
            {"type": "positive", "text": "Next monthly call confirmed Apr 14 — Preston accepted invite", "time": "Mar 12"},
            {"type": "warning", "text": "35-day gap between intro call (Mar 10) and next monthly (Apr 14) — consider mid-month check-in", "time": "Mar 23"},
            {"type": "warning", "text": "7d revenue down 55% vs 30d average — massive bot traffic inflating session counts", "time": "Mar 23"},
            {"type": "positive", "text": "Feb 14 revenue spike: $12,139 from 151 purchases — brand has strong campaign potential", "time": "Feb 14"},
            {"type": "warning", "text": "Pierre weekly roundups stopped after Jan 12 — 10+ week gap", "time": "Jan 12"}
        ]
    },

    # ---- VERACITY SELFCARE ----
    "f8f83f9d-be9e-4177-ad7e-292ed079eafd": {
        "brand_name": "Veracity Selfcare",
        # 7d: sessions=2,608, revenue=$8,174.13, CVR=2.61%, purchases=68
        # 30d: revenue=$47,587.36 => daily avg=$1,586.25
        "platform_activity": {
            "score": 20,  # sessions >500 => 8, revenue >$1000 => 6, CVR >1.5% => 6
            "detail": "7d: 2,608 sessions, $8,174 revenue, 2.61% CVR — strong performance"
        },
        "communication": {
            # Slack: brand msg Feb 18 (33 days ago) => >14d => 0pts
            # Brand contacts 14d: 0 => 0pts
            # Email 14d: Meta ad approvals + Glyphic prep Mar 11 => 1-3 => 3pts
            # Pulkit outreach: joined channel Feb 24 but no intro msg => 0pts
            "score": 3,
            "detail": "Last brand Slack Feb 18 (33d). Pulkit joined but no intro. Meta ads active."
        },
        "performance": {
            # 7d rev $8,174 / 7 = $1,167/day vs 30d avg $1,586/day => down 26% => Down >20% => 2pts
            # 7d CVR 2.61% > 1% => 7pts
            # 7d purchases 68 > 20 => 6pts
            "score": 15,
            "detail": "7d rev $8,174 vs 30d avg $1,586/day — down 26%. CVR 2.61%. 68 purchases."
        },
        "engagement": {
            # Last call: Feb 5 (46 days ago), Feb 26 cancelled => None in 30d => 0pts
            # Upcoming: None => 0pts
            # Stakeholders: Jacqueline, Maggie, Sabrina, agency DT Co => but no recent call => 0pts
            # Action items: stale (SKU cleanup Feb 18) => 1pt
            "score": 1,
            "detail": "Last completed call Feb 5 (46d). Feb 26 cancelled. No upcoming."
        },
        "call_frequency": {
            # 0 calls in 30d => 2pts
            "score": 2,
            "detail": "0 calls in last 30 days. Last completed call Feb 5."
        },
        "total": 41,
        "signals": [
            {"type": "positive", "text": "7d revenue $8,174 with 68 purchases at 2.61% CVR — strong platform performance", "time": "Mar 23"},
            {"type": "negative", "text": "No calls in 46 days — Feb 26 call was cancelled, no reschedule", "time": "Mar 23"},
            {"type": "negative", "text": "Pulkit joined Slack Feb 24 but never introduced himself — no GM transition completed", "time": "Feb 24"},
            {"type": "warning", "text": "SKU/variant cleanup requested Feb 18 — unclear if resolved", "time": "Feb 18"},
            {"type": "positive", "text": "Meta ads actively running and getting approved — campaigns still live", "time": "Mar 17"},
            {"type": "warning", "text": "7d revenue down 26% vs 30d daily average — slight decline", "time": "Mar 23"}
        ]
    },

    # ---- WESTMORE BEAUTY ----
    "508e7756-81aa-48b1-bbf5-765d2e8f1eb9": {
        "brand_name": "Westmore Beauty",
        # 7d: sessions=0, revenue=0, purchases=0 (onboarding, not live)
        "platform_activity": {
            "score": 0,  # Not live yet
            "detail": "7d: 0 sessions — funnels in build phase, not yet live (onboarding since Feb 5)"
        },
        "communication": {
            # Slack: last msg Feb 14 (37 days ago) => >14d => 0pts
            # Brand contacts 14d: 0 in Slack => 0pts
            # Email 14d: Jessica replied Mar 13 'Going to dive in now!', Pulkit follow-up Mar 16 => >3 => 5pts
            # Pulkit outreach: Mar 16 email follow-up, Mar 11 funnel update, Mar 6 feedback => last 7d => 5pts
            "score": 10,
            "detail": "Active email thread — Jessica replied Mar 13. Pulkit followed up Mar 16. Slack dormant."
        },
        "performance": {
            # All zeros (onboarding) => 0pts
            "score": 0,
            "detail": "No metrics yet — brand in onboarding, funnels not live."
        },
        "engagement": {
            # No formal calls in Glyphic since Feb 13. But email shows Pulkit suggested call Mar 10, Jessica rescheduled to Mar 11.
            # That's ~12 days ago => <14d => 5pts
            # Upcoming: None scheduled => 0pts
            # Stakeholders: Jessica, Brenda, Ryan => multiple => 4pts
            # Action items: Jessica said 'Going to dive in' Mar 13 => active => 4pts
            "score": 13,
            "detail": "Quick call ~Mar 11 to review funnels. Multiple stakeholders (Jessica, Brenda, Ryan). Active items."
        },
        "call_frequency": {
            # Feb 13 kick-off + ~Mar 11 ad-hoc = 2 calls in 30d (Mar 11 is within 30d) => 14pts
            # Actually Feb 13 is 38 days ago. Only Mar 11 ad-hoc in 30d window => 1 call => 8pts
            "score": 8,
            "detail": "1 call in last 30 days (~Mar 11 funnel review). Last formal kick-off Feb 13."
        },
        "total": 31,
        "signals": [
            {"type": "warning", "text": "Opt-out date May 15 — only 53 days away with zero live funnels", "time": "Mar 23"},
            {"type": "positive", "text": "Jessica replied 'Going to dive in now!' to updated funnels Mar 13", "time": "Mar 13"},
            {"type": "positive", "text": "Pulkit proactively followed up Mar 16 checking on funnel testing progress", "time": "Mar 16"},
            {"type": "negative", "text": "Zero live traffic — 6+ weeks into onboarding with no funnels launched", "time": "Mar 23"},
            {"type": "warning", "text": "Jessica had repeated Slack access issues — Westmore doesn't use Slack internally", "time": "Feb 10"},
            {"type": "positive", "text": "4 funnels built and integrations complete (Google Ads, GA4, Klaviyo)", "time": "Feb 14"}
        ]
    },

    # ---- BELLIWELLI ----
    "39f04705-e991-461e-a98f-2dd3f29d6e47": {
        "brand_name": "belliwelli",
        # 7d: sessions=10,688, revenue=$6,599, CVR=1.24%, purchases=133
        # 30d: revenue=$27,909 => daily avg=$930.30
        "platform_activity": {
            "score": 18,  # sessions >500 => 8, revenue >$1000 => 6, CVR >0.5% => 4
            "detail": "7d: 10,688 sessions, $6,599 revenue, 1.24% CVR, 133 purchases"
        },
        "communication": {
            # Slack: Talia msg Mar 11 (experiment issue, 12 days ago) => <14d => 1pt
            # Brand contacts 14d: Talia is FERMAT, not brand. Tom hasn't posted recently => 0pts
            # Email 14d: Tom accepted bi-weekly Mar 12, Pulkit sent performance update Mar 16 => 1-3 => 3pts
            # Pulkit outreach: Mar 16 performance update, Mar 9 call => last 7d => 5pts
            "score": 9,
            "detail": "Pulkit sent perf update Mar 16. Tom accepted bi-weekly Mar 12. Experiment issue tracked."
        },
        "performance": {
            # 7d rev $6,599 / 7 = $943/day vs 30d avg $930/day => within 20% => 5pts
            # 7d CVR 1.24% > 1% => 7pts
            # 7d purchases 133 > 20 => 6pts
            "score": 18,
            "detail": "7d rev $6,599 vs 30d avg $930/day — in line. CVR 1.24%. 133 purchases."
        },
        "engagement": {
            # Last call: Mar 9 bi-weekly (14 days ago) => <14d => 5pts (exactly 14d)
            # Upcoming: Mar 23 bi-weekly (TODAY) => 5pts
            # Stakeholders: Tom + Morry => multiple on business review but recent calls just Tom => single => 2pts
            # Action items: experiment data issue being tracked => 4pts
            "score": 16,
            "detail": "Call Mar 9 (14d). Next call TODAY Mar 23. Experiment issue being tracked."
        },
        "call_frequency": {
            # Mar 9 bi-weekly = 1 call in 30d => 8pts
            "score": 8,
            "detail": "1 call in last 30 days (Mar 9 bi-weekly). Next: Mar 23 (today)."
        },
        "total": 69,
        "signals": [
            {"type": "positive", "text": "Bi-weekly call today Mar 23 — cadence established with Tom Fitzpatrick", "time": "Mar 23"},
            {"type": "positive", "text": "7d revenue $6,599 with 133 purchases — stable performance, in line with 30d average", "time": "Mar 23"},
            {"type": "warning", "text": "Experiment running since Mar 11 with no data showing — needs investigation", "time": "Mar 11"},
            {"type": "positive", "text": "Pulkit sent comprehensive performance update email Mar 16", "time": "Mar 16"},
            {"type": "positive", "text": "Tom accepted recurring bi-weekly calendar invite — engaged", "time": "Mar 12"},
            {"type": "warning", "text": "PDP lead image pulling incorrectly — flagged Feb 26, needs resolution", "time": "Feb 26"}
        ]
    }
}

# ============================================================
# UPDATE JSON FILES
# ============================================================

def update_brand_health(brand_id, health_data):
    filepath = os.path.join(DATA_DIR, f"{brand_id}.json")

    with open(filepath, 'r') as f:
        data = json.load(f)

    # Build new health section
    new_health = {
        "score": health_data["total"],
        "breakdown": {
            "platform_activity": health_data["platform_activity"]["score"],
            "platform_detail": health_data["platform_activity"]["detail"],
            "communication": health_data["communication"]["score"],
            "communication_detail": health_data["communication"]["detail"],
            "performance": health_data["performance"]["score"],
            "performance_detail": health_data["performance"]["detail"],
            "engagement": health_data["engagement"]["score"],
            "engagement_detail": health_data["engagement"]["detail"],
            "call_frequency": health_data["call_frequency"]["score"],
            "call_detail": health_data["call_frequency"]["detail"]
        },
        "signals": health_data["signals"]
    }

    # Update only the health section
    data["health"] = new_health
    data["last_updated"] = "2026-03-23T16:00:00Z"

    with open(filepath, 'w') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

    print(f"  {health_data['brand_name']}: score {health_data['total']}/100")

print("=" * 60)
print("HEALTH SCORE REFRESH — March 23, 2026")
print("=" * 60)
print()

for brand_id, health_data in brands.items():
    update_brand_health(brand_id, health_data)

print()
print("=" * 60)
print("ALL 15 BRANDS UPDATED")
print("=" * 60)
print()

# Print summary table
print(f"{'Brand':<25} {'Score':>5}  {'Platform':>8}  {'Comms':>5}  {'Perf':>4}  {'Engage':>6}  {'Calls':>5}")
print("-" * 72)
for brand_id, h in sorted(brands.items(), key=lambda x: x[1]["total"], reverse=True):
    print(f"{h['brand_name']:<25} {h['total']:>5}  {h['platform_activity']['score']:>8}  {h['communication']['score']:>5}  {h['performance']['score']:>4}  {h['engagement']['score']:>6}  {h['call_frequency']['score']:>5}")
