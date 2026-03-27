#!/usr/bin/env python3
"""
compute_health.py — Recompute health scores for all brands using the NEW 4-factor rubric.
Reference date: 2026-03-24

4 factors:
  - Platform Performance: /20
  - Communication: /20
  - Engagement: /20
  - CSM Sentiment: /40 (from sentiment.json)
"""

import json, os, re
from datetime import datetime, timedelta

DIR  = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(DIR, "data")
REF  = datetime(2026, 3, 27)  # reference date

# Sentiment data path (same as server.js logic)
SENTIMENT_DIR = os.environ.get("RAILWAY_VOLUME_MOUNT_PATH", os.path.join(DIR, "sentiment-data"))
SENTIMENT_FILE = os.path.join(SENTIMENT_DIR, "sentiment.json")

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


def load_sentiment_data():
    """Load sentiment data from sentiment.json."""
    try:
        if os.path.exists(SENTIMENT_FILE):
            with open(SENTIMENT_FILE, "r") as f:
                return json.load(f)
    except Exception as e:
        print(f"  Warning: Could not read sentiment data: {e}")
    return {}


# ─── PLATFORM PERFORMANCE (20 pts) ─────────────────────────────────────────

def compute_platform_performance(perf):
    """Compute Platform Performance score (max 20). 4 metrics: Sessions, Revenue, CVR, Purchases."""
    d7 = perf.get("7d", {})

    sessions_7d = d7.get("sessions", 0) or 0
    revenue_7d  = d7.get("revenue", 0) or 0
    cvr_7d      = d7.get("cvr", 0) or 0
    purchases_7d = d7.get("purchases", 0) or 0

    # 7d Sessions (out of 5)
    if sessions_7d > 1000:    s_sessions = 5
    elif sessions_7d > 500:   s_sessions = 4
    elif sessions_7d > 200:   s_sessions = 3
    elif sessions_7d > 50:    s_sessions = 2
    else:                     s_sessions = 0

    # 7d Revenue (out of 5)
    if revenue_7d > 5000:     s_rev = 5
    elif revenue_7d > 1000:   s_rev = 4
    elif revenue_7d > 200:    s_rev = 3
    elif revenue_7d > 0:      s_rev = 1
    else:                     s_rev = 0

    # 7d CVR (out of 5)
    if cvr_7d > 2:            s_cvr = 5
    elif cvr_7d > 1:          s_cvr = 4
    elif cvr_7d > 0.5:        s_cvr = 3
    elif cvr_7d > 0:          s_cvr = 1
    else:                     s_cvr = 0

    # 7d Purchases (out of 5)
    if purchases_7d > 30:     s_purch = 5
    elif purchases_7d > 10:   s_purch = 4
    elif purchases_7d > 5:    s_purch = 3
    elif purchases_7d > 0:    s_purch = 1
    else:                     s_purch = 0

    total = s_sessions + s_rev + s_cvr + s_purch
    detail_str = (
        f"Sessions:{s_sessions}/5, Revenue:{s_rev}/5, CVR:{s_cvr}/5, Purchases:{s_purch}/5"
    )
    return total, detail_str


# ─── COMMUNICATION (20 pts) ────────────────────────────────────────────────

def compute_communication(data):
    """Compute Communication score (max 20)."""
    slack_msgs = data.get("slack", {}).get("messages", [])
    email_msgs = data.get("email", {}).get("messages", [])

    # --- Slack recency (out of 4) ---
    most_recent_slack_days = None
    for msg in slack_msgs:
        ts = get_msg_timestamp(msg)
        d = days_ago(ts)
        if d is not None:
            if most_recent_slack_days is None or d < most_recent_slack_days:
                most_recent_slack_days = d

    if most_recent_slack_days is not None and most_recent_slack_days < 3:
        s_slack_recency = 4
    elif most_recent_slack_days is not None and most_recent_slack_days < 7:
        s_slack_recency = 3
    elif most_recent_slack_days is not None and most_recent_slack_days < 14:
        s_slack_recency = 1
    else:
        s_slack_recency = 0

    # --- Brand contacts in Slack 14d (out of 4) ---
    brand_msgs_14d = 0
    for msg in slack_msgs:
        ts = get_msg_timestamp(msg)
        d = days_ago(ts)
        if d is not None and d <= 14:
            if is_brand_contact(msg):
                brand_msgs_14d += 1

    if brand_msgs_14d > 5:     s_brand_slack = 4
    elif brand_msgs_14d >= 3:  s_brand_slack = 3
    elif brand_msgs_14d >= 1:  s_brand_slack = 1
    else:                      s_brand_slack = 0

    # --- Pulkit active in Slack 14d (out of 4) ---
    pulkit_msgs_14d = 0
    for msg in slack_msgs:
        ts = get_msg_timestamp(msg)
        d = days_ago(ts)
        if d is not None and d <= 14:
            if is_pulkit_msg(msg):
                text = str(msg.get("text", "")).lower()
                if "joined" in text and "channel" in text:
                    continue
                pulkit_msgs_14d += 1

    if pulkit_msgs_14d > 3:   s_pulkit_slack = 4
    elif pulkit_msgs_14d >= 1: s_pulkit_slack = 2
    else:                      s_pulkit_slack = 0

    # --- Email threads 14d (out of 4) ---
    email_count_14d = 0
    for msg in email_msgs:
        ts = msg.get("date", "")
        d = days_ago(ts)
        if d is not None and d <= 14:
            email_count_14d += 1

    if email_count_14d > 5:    s_email = 4
    elif email_count_14d >= 2: s_email = 3
    elif email_count_14d >= 1: s_email = 1
    else:                      s_email = 0

    # --- Pulkit sent outreach (out of 4) ---
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
        s_pulkit_email = 4
    elif pulkit_email_days is not None and pulkit_email_days < 14:
        s_pulkit_email = 3
    elif pulkit_email_days is not None and pulkit_email_days < 30:
        s_pulkit_email = 1
    else:
        s_pulkit_email = 0

    total = s_slack_recency + s_brand_slack + s_pulkit_slack + s_pulkit_email + s_email
    detail_str = (
        f"SlackRecency:{s_slack_recency}/4, BrandSlack14d:{s_brand_slack}/4, "
        f"PulkitSlack14d:{s_pulkit_slack}/4, EmailThreads14d:{s_email}/4, "
        f"PulkitOutreach:{s_pulkit_email}/4"
    )
    return total, detail_str


# ─── ENGAGEMENT (20 pts) ──────────────────────────────────────────────────

def compute_engagement(data):
    """Compute Engagement score (max 20). 3 metrics: Last call, Calls in 30d, Upcoming call.
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

    # Also check past calendar events
    for ev in (past_events or []):
        date_str = ev.get("start", "")
        d = days_ago(date_str)
        if d is not None:
            all_call_days.append(d)

    # --- Last call date (out of 8) ---
    last_call_days = min(all_call_days) if all_call_days else None

    if last_call_days is not None and last_call_days < 7:
        s_last_call = 8
    elif last_call_days is not None and last_call_days < 14:
        s_last_call = 6
    elif last_call_days is not None and last_call_days < 30:
        s_last_call = 4
    elif last_call_days is not None:
        s_last_call = 1
    else:
        s_last_call = 0

    # --- Calls in 30d (out of 6) ---
    calls_30d = len([d for d in all_call_days if d <= 30])

    if calls_30d >= 4:        s_calls_30d = 6
    elif calls_30d >= 2:      s_calls_30d = 4
    elif calls_30d >= 1:      s_calls_30d = 3
    else:                     s_calls_30d = 1

    # --- Upcoming call (out of 6) ---
    has_upcoming = len(upcoming) > 0 if upcoming else False
    s_upcoming = 6 if has_upcoming else 0

    total = s_last_call + s_calls_30d + s_upcoming
    detail_str = (
        f"LastCall:{s_last_call}/8, Calls30d:{s_calls_30d}/6, Upcoming:{s_upcoming}/6"
    )
    return total, detail_str


# ─── CSM SENTIMENT (40 pts) ──────────────────────────────────────────────

def compute_csm_sentiment(brand_id, sentiment_data):
    """Compute CSM Sentiment score (max 40) from latest rating in sentiment.json.
    Mapping: 10=40, 9=36, 8=32, 7=28, 6=24, 5=20, 4=16, 3=12, 2=8, 1=4, 0(not rated)=0
    """
    ratings = sentiment_data.get(brand_id, [])
    if not ratings or not isinstance(ratings, list):
        return 0, "Not rated yet"

    # Find the latest rating by date
    latest = None
    for r in ratings:
        if isinstance(r, dict) and r.get("score"):
            if latest is None or (r.get("date", "") > latest.get("date", "")):
                latest = r

    if not latest:
        return 0, "Not rated yet"

    raw_score = latest.get("score", 0)
    mapped = raw_score * 4  # 1=4, 2=8, ... 10=40

    # Color label
    if raw_score >= 9:
        label = "Green"
    elif raw_score >= 7:
        label = "Yellow"
    else:
        label = "Red"

    detail_str = f"Rating:{raw_score}/10 ({label}), Mapped:{mapped}/40, Date:{latest.get('date', 'N/A')}"
    return mapped, detail_str


# ─── MAIN ──────────────────────────────────────────────────────────────────

def main():
    files = sorted([f for f in os.listdir(DATA) if f.endswith(".json")])
    results = []

    # Load sentiment data
    sentiment_data = load_sentiment_data()
    print(f"Loaded sentiment data: {len([k for k in sentiment_data if k != 'dismissals'])} brands with ratings")

    for fname in files:
        fpath = os.path.join(DATA, fname)
        with open(fpath, "r") as f:
            data = json.load(f)

        brand_name = data.get("brand_name", fname)
        brand_id = fname.replace(".json", "")
        perf = data.get("performance", {})

        # Compute 4 factors
        pp_score, pp_detail = compute_platform_performance(perf)
        comm_score, comm_detail = compute_communication(data)
        eng_score, eng_detail = compute_engagement(data)
        sent_score, sent_detail = compute_csm_sentiment(brand_id, sentiment_data)

        total = pp_score + comm_score + eng_score + sent_score
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
                "csm_sentiment": sent_score,
                "csm_sentiment_detail": sent_detail,
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
            "sent": sent_score,
            "pp_detail": pp_detail,
            "comm_detail": comm_detail,
            "eng_detail": eng_detail,
            "sent_detail": sent_detail,
        })

    # Sort by score descending
    results.sort(key=lambda x: x["total"], reverse=True)

    # Print summary table
    print()
    print("=" * 140)
    print(f"{'BRAND':<25} {'TOTAL':>6} {'STATUS':<8} {'PLATFORM':>9} {'COMMS':>6} {'ENGAGE':>7} {'SENTIMENT':>10}")
    print("=" * 140)
    for r in results:
        emoji = {"green": "\U0001f7e2", "yellow": "\U0001f7e1", "red": "\U0001f534"}.get(r["status"], "")
        print(f"{r['brand']:<25} {r['total']:>5}/100 {emoji} {r['status']:<6} {r['pp']:>5}/20   {r['comm']:>4}/20  {r['eng']:>4}/20  {r['sent']:>6}/40")
    print("=" * 140)

    # Print detailed breakdowns
    print()
    print("DETAILED BREAKDOWNS")
    print("-" * 140)
    for r in results:
        print(f"\n  {r['brand']} ({r['total']}/100 {r['status']})")
        print(f"    Platform Performance ({r['pp']}/20): {r['pp_detail']}")
        print(f"    Communication ({r['comm']}/20):       {r['comm_detail']}")
        print(f"    Engagement ({r['eng']}/20):           {r['eng_detail']}")
        print(f"    CSM Sentiment ({r['sent']}/40):       {r['sent_detail']}")

    print()
    print(f"Total brands processed: {len(results)}")
    green = sum(1 for r in results if r["status"] == "green")
    yellow = sum(1 for r in results if r["status"] == "yellow")
    red = sum(1 for r in results if r["status"] == "red")
    print(f"  Green (70+): {green}  |  Yellow (40-69): {yellow}  |  Red (0-39): {red}")
    print()


if __name__ == "__main__":
    main()
