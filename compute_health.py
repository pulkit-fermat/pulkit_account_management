#!/usr/bin/env python3
"""
compute_health.py — Recompute health scores for all brands using the NEW 3-factor rubric.
Reference date: 2026-03-24
"""

import json, os, re
from datetime import datetime, timedelta

DIR  = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(DIR, "data")
REF  = datetime(2026, 3, 24)  # reference date

# ─── helpers ────────────────────────────────────────────────────────────────

def days_ago(date_str):
    """Parse various date formats and return days ago from REF. Returns None on failure."""
    if not date_str:
        return None
    for fmt in (
        "%Y-%m-%dT%H:%M:%SZ",
        "%Y-%m-%dT%H:%M:%S%z",
        "%Y-%m-%dT%H:%M:%S+05:30",
        "%Y-%m-%dT%H:%M:%S",
        "%Y-%m-%d",
    ):
        try:
            dt = datetime.strptime(date_str.replace("+05:30", "").replace("+00:00", ""), fmt.replace("+05:30", "").replace("%z", ""))
            return (REF - dt).days
        except Exception:
            continue
    # fallback: try to extract just the date portion
    m = re.match(r"(\d{4}-\d{2}-\d{2})", str(date_str))
    if m:
        dt = datetime.strptime(m.group(1), "%Y-%m-%d")
        return (REF - dt).days
    return None


def parse_duration_minutes(dur):
    """Parse a duration field into minutes (int). Handles '30 min', '17 min', int, etc."""
    if dur is None:
        return None
    if isinstance(dur, (int, float)):
        return int(dur)
    s = str(dur).lower().strip()
    m = re.search(r"(\d+)", s)
    if m:
        return int(m.group(1))
    return None


def is_pulkit_msg(msg):
    """Check if a Slack/email message is from Pulkit."""
    user = str(msg.get("user", "") or msg.get("author", "") or msg.get("from", "")).lower()
    return "pulkit" in user


def is_bot_or_system(msg):
    """Check if a Slack message is from a bot or system."""
    user = str(msg.get("user", "") or msg.get("author", "")).lower()
    return any(k in user for k in ("bot", "pierre", "system", "clickup", "calendly", "fermat bot", "fermàt bot"))


def is_brand_contact(msg):
    """Check if a Slack message is from a brand contact (not Pulkit, not bot, not system, not FERMAT staff)."""
    user = str(msg.get("user", "") or msg.get("author", "")).lower()
    if not user:
        return False
    fermat_names = ["pulkit", "talia", "mia", "isabel", "ryan barry", "mukul", "kaitlin", "sarah herman"]
    if any(fn in user for fn in fermat_names):
        return False
    if is_bot_or_system(msg):
        return False
    if "joined" in str(msg.get("text", "")).lower() and "channel" in str(msg.get("text", "")).lower():
        return False
    return True


def get_msg_timestamp(msg):
    """Get the timestamp string from a message (Slack or email)."""
    return msg.get("timestamp") or msg.get("date") or msg.get("ts") or ""


def count_participants(participants_field):
    """Count unique participants from various formats."""
    if participants_field is None:
        return 0
    if isinstance(participants_field, list):
        return len(participants_field)
    if isinstance(participants_field, str):
        # comma-separated
        parts = [p.strip() for p in participants_field.split(",") if p.strip()]
        return len(parts)
    return 0


# ─── PLATFORM PERFORMANCE (35 pts) ─────────────────────────────────────────

def compute_platform_performance(perf):
    """Compute Platform Performance score (max 35). Only 4 metrics: Sessions, Revenue, CVR, Purchases."""
    d7 = perf.get("7d", {})

    sessions_7d = d7.get("sessions", 0) or 0
    revenue_7d  = d7.get("revenue", 0) or 0
    cvr_7d      = d7.get("cvr", 0) or 0
    purchases_7d = d7.get("purchases", 0) or 0

    # 7d Sessions (out of 9)
    if sessions_7d > 1000:    s_sessions = 9
    elif sessions_7d > 500:   s_sessions = 7
    elif sessions_7d > 200:   s_sessions = 5
    elif sessions_7d > 50:    s_sessions = 3
    else:                     s_sessions = 0

    # 7d Revenue (out of 9)
    if revenue_7d > 5000:     s_rev = 9
    elif revenue_7d > 1000:   s_rev = 7
    elif revenue_7d > 200:    s_rev = 5
    elif revenue_7d > 0:      s_rev = 2
    else:                     s_rev = 0

    # 7d CVR (out of 9)
    if cvr_7d > 2:            s_cvr = 9
    elif cvr_7d > 1:          s_cvr = 7
    elif cvr_7d > 0.5:        s_cvr = 5
    elif cvr_7d > 0:          s_cvr = 2
    else:                     s_cvr = 0

    # 7d Purchases (out of 8)
    if purchases_7d > 30:     s_purch = 8
    elif purchases_7d > 10:   s_purch = 6
    elif purchases_7d > 5:    s_purch = 4
    elif purchases_7d > 0:    s_purch = 2
    else:                     s_purch = 0

    total = s_sessions + s_rev + s_cvr + s_purch
    detail_str = (
        f"Sessions:{s_sessions}/9, Revenue:{s_rev}/9, CVR:{s_cvr}/9, Purchases:{s_purch}/8"
    )
    return total, detail_str


# ─── COMMUNICATION (30 pts) ────────────────────────────────────────────────

def compute_communication(data):
    """Compute Communication score (max 30)."""
    slack_msgs = data.get("slack", {}).get("messages", [])
    email_msgs = data.get("email", {}).get("messages", [])

    # --- Slack recency (out of 6) ---
    # Find most recent Slack message timestamp
    most_recent_slack_days = None
    for msg in slack_msgs:
        ts = get_msg_timestamp(msg)
        d = days_ago(ts)
        if d is not None:
            if most_recent_slack_days is None or d < most_recent_slack_days:
                most_recent_slack_days = d

    if most_recent_slack_days is not None and most_recent_slack_days < 3:
        s_slack_recency = 6
    elif most_recent_slack_days is not None and most_recent_slack_days < 7:
        s_slack_recency = 4
    elif most_recent_slack_days is not None and most_recent_slack_days < 14:
        s_slack_recency = 2
    else:
        s_slack_recency = 0

    # --- Brand contacts in Slack 14d (out of 6) ---
    brand_msgs_14d = 0
    for msg in slack_msgs:
        ts = get_msg_timestamp(msg)
        d = days_ago(ts)
        if d is not None and d <= 14:
            if is_brand_contact(msg):
                brand_msgs_14d += 1

    if brand_msgs_14d > 5:     s_brand_slack = 6
    elif brand_msgs_14d >= 3:  s_brand_slack = 4
    elif brand_msgs_14d >= 1:  s_brand_slack = 2
    else:                      s_brand_slack = 0

    # --- Pulkit active in Slack 14d (out of 6) ---
    pulkit_msgs_14d = 0
    for msg in slack_msgs:
        ts = get_msg_timestamp(msg)
        d = days_ago(ts)
        if d is not None and d <= 14:
            if is_pulkit_msg(msg):
                # Don't count "joined the channel" messages
                text = str(msg.get("text", "")).lower()
                if "joined" in text and "channel" in text:
                    continue
                pulkit_msgs_14d += 1

    if pulkit_msgs_14d > 3:   s_pulkit_slack = 6
    elif pulkit_msgs_14d >= 1: s_pulkit_slack = 4
    else:                      s_pulkit_slack = 0

    # --- Email threads 14d (out of 6) ---
    email_count_14d = 0
    for msg in email_msgs:
        ts = msg.get("date", "")
        d = days_ago(ts)
        if d is not None and d <= 14:
            email_count_14d += 1

    if email_count_14d > 5:    s_email = 6
    elif email_count_14d >= 2: s_email = 4
    elif email_count_14d >= 1: s_email = 2
    else:                      s_email = 0

    # --- Pulkit sent outreach (out of 6) ---
    pulkit_email_days = None
    for msg in email_msgs:
        frm = str(msg.get("from", "")).lower()
        if "pulkit" in frm:
            ts = msg.get("date", "")
            d = days_ago(ts)
            if d is not None:
                if pulkit_email_days is None or d < pulkit_email_days:
                    pulkit_email_days = d

    if pulkit_email_days is not None and pulkit_email_days < 7:
        s_pulkit_email = 6
    elif pulkit_email_days is not None and pulkit_email_days < 14:
        s_pulkit_email = 4
    elif pulkit_email_days is not None and pulkit_email_days < 30:
        s_pulkit_email = 2
    else:
        s_pulkit_email = 0

    total = s_slack_recency + s_brand_slack + s_pulkit_slack + s_pulkit_email + s_email
    detail_str = (
        f"SlackRecency:{s_slack_recency}/6, BrandSlack14d:{s_brand_slack}/6, "
        f"PulkitSlack14d:{s_pulkit_slack}/6, EmailThreads14d:{s_email}/6, "
        f"PulkitOutreach:{s_pulkit_email}/6"
    )
    return total, detail_str


# ─── ENGAGEMENT (35 pts) ──────────────────────────────────────────────────

def compute_engagement(data):
    """Compute Engagement score (max 35). Only 3 metrics: Last call, Calls in 30d, Upcoming call.
    Sources: Glyphic calls + Granola meetings + Calendar."""
    calls = data.get("calls", {}).get("recent", [])
    calendar = data.get("calendar", {})
    upcoming = calendar.get("upcoming", [])
    past_events = calendar.get("past", [])

    # Collect all call/meeting dates from both Glyphic calls AND calendar past events
    all_call_days = []
    for call in calls:
        status = str(call.get("status", "")).lower()
        if status == "cancelled":
            continue
        date_str = call.get("date", "")
        d = days_ago(date_str)
        if d is not None:
            all_call_days.append(d)

    # Also check past calendar events (may include Granola-sourced meetings)
    for ev in (past_events or []):
        date_str = ev.get("start", "")
        d = days_ago(date_str)
        if d is not None:
            all_call_days.append(d)

    # --- Last call date (out of 12) ---
    last_call_days = min(all_call_days) if all_call_days else None

    if last_call_days is not None and last_call_days < 7:
        s_last_call = 12
    elif last_call_days is not None and last_call_days < 14:
        s_last_call = 9
    elif last_call_days is not None and last_call_days < 30:
        s_last_call = 6
    elif last_call_days is not None:
        s_last_call = 2
    else:
        s_last_call = 0

    # --- Calls in 30d (out of 12) --- count unique dates from both sources
    calls_30d = len([d for d in all_call_days if d <= 30])

    if calls_30d >= 4:        s_calls_30d = 12
    elif calls_30d >= 2:      s_calls_30d = 9
    elif calls_30d >= 1:      s_calls_30d = 6
    else:                     s_calls_30d = 2

    # --- Upcoming call (out of 11) ---
    has_upcoming = len(upcoming) > 0 if upcoming else False
    s_upcoming = 11 if has_upcoming else 0

    total = s_last_call + s_calls_30d + s_upcoming
    detail_str = (
        f"LastCall:{s_last_call}/12, Calls30d:{s_calls_30d}/12, Upcoming:{s_upcoming}/11"
    )
    return total, detail_str


# ─── MAIN ──────────────────────────────────────────────────────────────────

def main():
    files = sorted([f for f in os.listdir(DATA) if f.endswith(".json")])
    results = []

    for fname in files:
        fpath = os.path.join(DATA, fname)
        with open(fpath, "r") as f:
            data = json.load(f)

        brand_name = data.get("brand_name", fname)
        perf = data.get("performance", {})

        # Compute 3 factors
        pp_score, pp_detail = compute_platform_performance(perf)
        comm_score, comm_detail = compute_communication(data)
        eng_score, eng_detail = compute_engagement(data)

        total = pp_score + comm_score + eng_score
        if total >= 70:
            status = "green"
        elif total >= 40:
            status = "yellow"
        else:
            status = "red"

        # Update health section — preserve signals
        old_health = data.get("health", {})
        signals = old_health.get("signals", [])

        data["health"] = {
            "score": total,
            "status": status,
            "breakdown": {
                "platform_performance": pp_score,
                "platform_performance_detail": pp_detail,
                "communication": comm_score,
                "communication_detail": comm_detail,
                "engagement": eng_score,
                "engagement_detail": eng_detail,
            },
            "signals": signals,
        }

        # Write back
        with open(fpath, "w") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)

        results.append({
            "brand": brand_name,
            "total": total,
            "status": status,
            "pp": pp_score,
            "comm": comm_score,
            "eng": eng_score,
            "pp_detail": pp_detail,
            "comm_detail": comm_detail,
            "eng_detail": eng_detail,
        })

    # Sort by score descending
    results.sort(key=lambda x: x["total"], reverse=True)

    # Print summary table
    print()
    print("=" * 120)
    print(f"{'BRAND':<25} {'TOTAL':>6} {'STATUS':<8} {'PLATFORM':>9} {'COMMS':>6} {'ENGAGE':>7}")
    print("=" * 120)
    for r in results:
        emoji = {"green": "🟢", "yellow": "🟡", "red": "🔴"}.get(r["status"], "")
        print(f"{r['brand']:<25} {r['total']:>5}/100 {emoji} {r['status']:<6} {r['pp']:>5}/35   {r['comm']:>4}/30  {r['eng']:>4}/35")
    print("=" * 120)

    # Print detailed breakdowns
    print()
    print("DETAILED BREAKDOWNS")
    print("-" * 120)
    for r in results:
        print(f"\n  {r['brand']} ({r['total']}/100 {r['status']})")
        print(f"    Platform Performance ({r['pp']}/35): {r['pp_detail']}")
        print(f"    Communication ({r['comm']}/30):       {r['comm_detail']}")
        print(f"    Engagement ({r['eng']}/35):           {r['eng_detail']}")

    print()
    print(f"Total brands processed: {len(results)}")
    green = sum(1 for r in results if r["status"] == "green")
    yellow = sum(1 for r in results if r["status"] == "yellow")
    red = sum(1 for r in results if r["status"] == "red")
    print(f"  Green (70+): {green}  |  Yellow (40-69): {yellow}  |  Red (0-39): {red}")
    print()


if __name__ == "__main__":
    main()
