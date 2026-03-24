#!/usr/bin/env python3
"""
Process raw FERMAT daily funnel metrics data into period aggregates.
Updates the 'performance' section of each brand's JSON data file.

Date reference: yesterday = Mar 17, 2026
Periods:
  yesterday = Mar 17
  3d = Mar 15-17
  7d = Mar 11-17
  15d = Mar 3-17
  30d = Feb 16-Mar 17
  45d = Feb 1-Mar 17
"""
import json
import os
from datetime import datetime, timedelta

DIR = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(DIR, "data")

# Date reference: Mar 17, 2026 is "yesterday"
REF = datetime(2026, 3, 17)

PERIODS = {
    "yesterday": (REF, REF),
    "3d": (REF - timedelta(days=2), REF),
    "7d": (REF - timedelta(days=6), REF),
    "15d": (REF - timedelta(days=14), REF),
    "30d": (REF - timedelta(days=29), REF),
    "45d": (REF - timedelta(days=44), REF),
}


def aggregate(daily_rows, start, end):
    """Sum sessions/revenue/purchases for days in [start, end], compute CVR and AOV."""
    total_sessions = 0
    total_revenue = 0.0
    total_purchases = 0
    for row in daily_rows:
        day_str = row["fct_product_funnels.date.day"][:10]
        d = datetime.strptime(day_str, "%Y-%m-%d")
        if start <= d <= end:
            total_sessions += row.get("fct_product_funnels.sessions", 0) or 0
            total_revenue += row.get("fct_product_funnels.revenue", 0) or 0
            total_purchases += row.get("fct_product_funnels.purchases", 0) or 0
    cvr = round((total_purchases / total_sessions * 100), 2) if total_sessions > 0 else 0
    aov = round((total_revenue / total_purchases), 2) if total_purchases > 0 else 0
    return {
        "ad_spend": None,
        "revenue": round(total_revenue, 2),
        "cvr": cvr,
        "sessions": total_sessions,
        "roas": None,
        "cpa": None,
        "purchases": total_purchases,
        "aov": aov,
    }


def update_brand(csv_id, daily_rows):
    """Read brand JSON, replace performance section with fresh aggregates, write back."""
    fpath = os.path.join(DATA, f"{csv_id}.json")
    if not os.path.exists(fpath):
        print(f"  SKIP {csv_id}: file not found")
        return

    with open(fpath) as f:
        data = json.load(f)

    perf = {}
    for period_name, (start, end) in PERIODS.items():
        perf[period_name] = aggregate(daily_rows, start, end)

    data["performance"] = perf
    data["last_updated"] = datetime.now().strftime("%Y-%m-%dT%H:%M:%SZ")

    with open(fpath, "w") as f:
        json.dump(data, f, indent=2)

    brand = data.get("brand_name", csv_id)
    rev30 = perf["30d"]["revenue"]
    sess30 = perf["30d"]["sessions"]
    rev_y = perf["yesterday"]["revenue"]
    sess_y = perf["yesterday"]["sessions"]
    print(f"  {brand}: yesterday rev=${rev_y:,.2f} / {sess_y:,} sess | 30d rev=${rev30:,.2f} / {sess30:,} sess")


# ===== RAW DATA FROM FERMAT API (fetched 2026-03-18) =====

RAW_DATA = {
    # FOND Regenerative
    "ab6fc1e8-f245-4344-902c-b60388575aca": [
        {"fct_product_funnels.date.day": "2026-02-01T00:00:00.000", "fct_product_funnels.sessions": 212, "fct_product_funnels.purchases": 2, "fct_product_funnels.revenue": 204},
        {"fct_product_funnels.date.day": "2026-02-02T00:00:00.000", "fct_product_funnels.sessions": 103, "fct_product_funnels.purchases": 0, "fct_product_funnels.revenue": 0},
        {"fct_product_funnels.date.day": "2026-02-03T00:00:00.000", "fct_product_funnels.sessions": 112, "fct_product_funnels.purchases": 2, "fct_product_funnels.revenue": 459},
        {"fct_product_funnels.date.day": "2026-02-04T00:00:00.000", "fct_product_funnels.sessions": 97, "fct_product_funnels.purchases": 1, "fct_product_funnels.revenue": 200},
        {"fct_product_funnels.date.day": "2026-02-05T00:00:00.000", "fct_product_funnels.sessions": 37, "fct_product_funnels.purchases": 0, "fct_product_funnels.revenue": 0},
        {"fct_product_funnels.date.day": "2026-02-06T00:00:00.000", "fct_product_funnels.sessions": 26, "fct_product_funnels.purchases": 0, "fct_product_funnels.revenue": 0},
        {"fct_product_funnels.date.day": "2026-02-07T00:00:00.000", "fct_product_funnels.sessions": 31, "fct_product_funnels.purchases": 0, "fct_product_funnels.revenue": 0},
        {"fct_product_funnels.date.day": "2026-02-08T00:00:00.000", "fct_product_funnels.sessions": 43, "fct_product_funnels.purchases": 0, "fct_product_funnels.revenue": 0},
        {"fct_product_funnels.date.day": "2026-02-09T00:00:00.000", "fct_product_funnels.sessions": 51, "fct_product_funnels.purchases": 0, "fct_product_funnels.revenue": 0},
        {"fct_product_funnels.date.day": "2026-02-10T00:00:00.000", "fct_product_funnels.sessions": 22, "fct_product_funnels.purchases": 1, "fct_product_funnels.revenue": 270},
        {"fct_product_funnels.date.day": "2026-02-11T00:00:00.000", "fct_product_funnels.sessions": 39, "fct_product_funnels.purchases": 0, "fct_product_funnels.revenue": 0},
        {"fct_product_funnels.date.day": "2026-02-12T00:00:00.000", "fct_product_funnels.sessions": 24, "fct_product_funnels.purchases": 0, "fct_product_funnels.revenue": 0},
        {"fct_product_funnels.date.day": "2026-02-13T00:00:00.000", "fct_product_funnels.sessions": 20, "fct_product_funnels.purchases": 1, "fct_product_funnels.revenue": 270},
        {"fct_product_funnels.date.day": "2026-02-14T00:00:00.000", "fct_product_funnels.sessions": 35, "fct_product_funnels.purchases": 1, "fct_product_funnels.revenue": 135},
        {"fct_product_funnels.date.day": "2026-02-15T00:00:00.000", "fct_product_funnels.sessions": 57, "fct_product_funnels.purchases": 1, "fct_product_funnels.revenue": 135},
        {"fct_product_funnels.date.day": "2026-02-16T00:00:00.000", "fct_product_funnels.sessions": 65, "fct_product_funnels.purchases": 0, "fct_product_funnels.revenue": 0},
        {"fct_product_funnels.date.day": "2026-02-17T00:00:00.000", "fct_product_funnels.sessions": 74, "fct_product_funnels.purchases": 0, "fct_product_funnels.revenue": 0},
        {"fct_product_funnels.date.day": "2026-02-18T00:00:00.000", "fct_product_funnels.sessions": 39, "fct_product_funnels.purchases": 0, "fct_product_funnels.revenue": 0},
        {"fct_product_funnels.date.day": "2026-02-19T00:00:00.000", "fct_product_funnels.sessions": 31, "fct_product_funnels.purchases": 0, "fct_product_funnels.revenue": 0},
        {"fct_product_funnels.date.day": "2026-02-20T00:00:00.000", "fct_product_funnels.sessions": 85, "fct_product_funnels.purchases": 0, "fct_product_funnels.revenue": 0},
        {"fct_product_funnels.date.day": "2026-02-21T00:00:00.000", "fct_product_funnels.sessions": 99, "fct_product_funnels.purchases": 2, "fct_product_funnels.revenue": 296},
        {"fct_product_funnels.date.day": "2026-02-22T00:00:00.000", "fct_product_funnels.sessions": 56, "fct_product_funnels.purchases": 0, "fct_product_funnels.revenue": 0},
        {"fct_product_funnels.date.day": "2026-02-23T00:00:00.000", "fct_product_funnels.sessions": 38, "fct_product_funnels.purchases": 0, "fct_product_funnels.revenue": 0},
        {"fct_product_funnels.date.day": "2026-02-24T00:00:00.000", "fct_product_funnels.sessions": 52, "fct_product_funnels.purchases": 0, "fct_product_funnels.revenue": 0},
        {"fct_product_funnels.date.day": "2026-02-25T00:00:00.000", "fct_product_funnels.sessions": 30, "fct_product_funnels.purchases": 0, "fct_product_funnels.revenue": 0},
        {"fct_product_funnels.date.day": "2026-02-26T00:00:00.000", "fct_product_funnels.sessions": 6, "fct_product_funnels.purchases": 0, "fct_product_funnels.revenue": 0},
        {"fct_product_funnels.date.day": "2026-02-27T00:00:00.000", "fct_product_funnels.sessions": 6, "fct_product_funnels.purchases": 0, "fct_product_funnels.revenue": 0},
        {"fct_product_funnels.date.day": "2026-02-28T00:00:00.000", "fct_product_funnels.sessions": 2, "fct_product_funnels.purchases": 0, "fct_product_funnels.revenue": 0},
        {"fct_product_funnels.date.day": "2026-03-01T00:00:00.000", "fct_product_funnels.sessions": 16, "fct_product_funnels.purchases": 0, "fct_product_funnels.revenue": 0},
        {"fct_product_funnels.date.day": "2026-03-02T00:00:00.000", "fct_product_funnels.sessions": 4, "fct_product_funnels.purchases": 0, "fct_product_funnels.revenue": 0},
        {"fct_product_funnels.date.day": "2026-03-03T00:00:00.000", "fct_product_funnels.sessions": 4, "fct_product_funnels.purchases": 0, "fct_product_funnels.revenue": 0},
        {"fct_product_funnels.date.day": "2026-03-04T00:00:00.000", "fct_product_funnels.sessions": 4, "fct_product_funnels.purchases": 0, "fct_product_funnels.revenue": 0},
        {"fct_product_funnels.date.day": "2026-03-05T00:00:00.000", "fct_product_funnels.sessions": 30, "fct_product_funnels.purchases": 0, "fct_product_funnels.revenue": 0},
        {"fct_product_funnels.date.day": "2026-03-06T00:00:00.000", "fct_product_funnels.sessions": 3, "fct_product_funnels.purchases": 0, "fct_product_funnels.revenue": 0},
        {"fct_product_funnels.date.day": "2026-03-07T00:00:00.000", "fct_product_funnels.sessions": 3, "fct_product_funnels.purchases": 0, "fct_product_funnels.revenue": 0},
        {"fct_product_funnels.date.day": "2026-03-08T00:00:00.000", "fct_product_funnels.sessions": 5, "fct_product_funnels.purchases": 0, "fct_product_funnels.revenue": 0},
        {"fct_product_funnels.date.day": "2026-03-09T00:00:00.000", "fct_product_funnels.sessions": 12, "fct_product_funnels.purchases": 0, "fct_product_funnels.revenue": 0},
        {"fct_product_funnels.date.day": "2026-03-10T00:00:00.000", "fct_product_funnels.sessions": 22, "fct_product_funnels.purchases": 0, "fct_product_funnels.revenue": 0},
        {"fct_product_funnels.date.day": "2026-03-11T00:00:00.000", "fct_product_funnels.sessions": 19, "fct_product_funnels.purchases": 0, "fct_product_funnels.revenue": 0},
        {"fct_product_funnels.date.day": "2026-03-12T00:00:00.000", "fct_product_funnels.sessions": 14, "fct_product_funnels.purchases": 0, "fct_product_funnels.revenue": 0},
        {"fct_product_funnels.date.day": "2026-03-13T00:00:00.000", "fct_product_funnels.sessions": 38, "fct_product_funnels.purchases": 1, "fct_product_funnels.revenue": 92.5},
        {"fct_product_funnels.date.day": "2026-03-14T00:00:00.000", "fct_product_funnels.sessions": 12, "fct_product_funnels.purchases": 0, "fct_product_funnels.revenue": 0},
        {"fct_product_funnels.date.day": "2026-03-15T00:00:00.000", "fct_product_funnels.sessions": 18, "fct_product_funnels.purchases": 0, "fct_product_funnels.revenue": 0},
        {"fct_product_funnels.date.day": "2026-03-16T00:00:00.000", "fct_product_funnels.sessions": 34, "fct_product_funnels.purchases": 0, "fct_product_funnels.revenue": 0},
        {"fct_product_funnels.date.day": "2026-03-17T00:00:00.000", "fct_product_funnels.sessions": 34, "fct_product_funnels.purchases": 0, "fct_product_funnels.revenue": 0},
    ],

    # HOP WTR (churned)
    "74128082-bd6b-4435-94a5-7a7fdfa41726": [
        {"fct_product_funnels.date.day": "2026-02-01T00:00:00.000", "fct_product_funnels.sessions": 1047, "fct_product_funnels.purchases": 14, "fct_product_funnels.revenue": 882.4},
        {"fct_product_funnels.date.day": "2026-02-02T00:00:00.000", "fct_product_funnels.sessions": 893, "fct_product_funnels.purchases": 16, "fct_product_funnels.revenue": 773.14},
        {"fct_product_funnels.date.day": "2026-02-03T00:00:00.000", "fct_product_funnels.sessions": 915, "fct_product_funnels.purchases": 7, "fct_product_funnels.revenue": 172.94},
        {"fct_product_funnels.date.day": "2026-02-04T00:00:00.000", "fct_product_funnels.sessions": 712, "fct_product_funnels.purchases": 2, "fct_product_funnels.revenue": 125.78},
        {"fct_product_funnels.date.day": "2026-02-05T00:00:00.000", "fct_product_funnels.sessions": 705, "fct_product_funnels.purchases": 11, "fct_product_funnels.revenue": 563},
        {"fct_product_funnels.date.day": "2026-02-06T00:00:00.000", "fct_product_funnels.sessions": 830, "fct_product_funnels.purchases": 8, "fct_product_funnels.revenue": 587.11},
        {"fct_product_funnels.date.day": "2026-02-07T00:00:00.000", "fct_product_funnels.sessions": 1176, "fct_product_funnels.purchases": 7, "fct_product_funnels.revenue": 351.78},
        {"fct_product_funnels.date.day": "2026-02-08T00:00:00.000", "fct_product_funnels.sessions": 1246, "fct_product_funnels.purchases": 7, "fct_product_funnels.revenue": 358.56},
        {"fct_product_funnels.date.day": "2026-02-09T00:00:00.000", "fct_product_funnels.sessions": 1098, "fct_product_funnels.purchases": 8, "fct_product_funnels.revenue": 432.61},
        {"fct_product_funnels.date.day": "2026-02-10T00:00:00.000", "fct_product_funnels.sessions": 1229, "fct_product_funnels.purchases": 10, "fct_product_funnels.revenue": 547.65},
        {"fct_product_funnels.date.day": "2026-02-11T00:00:00.000", "fct_product_funnels.sessions": 1185, "fct_product_funnels.purchases": 6, "fct_product_funnels.revenue": 244.13},
        {"fct_product_funnels.date.day": "2026-02-12T00:00:00.000", "fct_product_funnels.sessions": 1192, "fct_product_funnels.purchases": 10, "fct_product_funnels.revenue": 514.99},
        {"fct_product_funnels.date.day": "2026-02-13T00:00:00.000", "fct_product_funnels.sessions": 595, "fct_product_funnels.purchases": 7, "fct_product_funnels.revenue": 278.2},
        {"fct_product_funnels.date.day": "2026-02-14T00:00:00.000", "fct_product_funnels.sessions": 390, "fct_product_funnels.purchases": 9, "fct_product_funnels.revenue": 391.48},
        {"fct_product_funnels.date.day": "2026-02-15T00:00:00.000", "fct_product_funnels.sessions": 435, "fct_product_funnels.purchases": 6, "fct_product_funnels.revenue": 244.17},
        {"fct_product_funnels.date.day": "2026-02-16T00:00:00.000", "fct_product_funnels.sessions": 587, "fct_product_funnels.purchases": 8, "fct_product_funnels.revenue": 266.37},
        {"fct_product_funnels.date.day": "2026-02-17T00:00:00.000", "fct_product_funnels.sessions": 443, "fct_product_funnels.purchases": 11, "fct_product_funnels.revenue": 488.33},
        {"fct_product_funnels.date.day": "2026-02-18T00:00:00.000", "fct_product_funnels.sessions": 352, "fct_product_funnels.purchases": 1, "fct_product_funnels.revenue": 31.44},
        {"fct_product_funnels.date.day": "2026-02-19T00:00:00.000", "fct_product_funnels.sessions": 311, "fct_product_funnels.purchases": 8, "fct_product_funnels.revenue": 495.29},
        {"fct_product_funnels.date.day": "2026-02-20T00:00:00.000", "fct_product_funnels.sessions": 209, "fct_product_funnels.purchases": 2, "fct_product_funnels.revenue": 62.9},
        {"fct_product_funnels.date.day": "2026-02-21T00:00:00.000", "fct_product_funnels.sessions": 158, "fct_product_funnels.purchases": 2, "fct_product_funnels.revenue": 94.34},
        {"fct_product_funnels.date.day": "2026-02-22T00:00:00.000", "fct_product_funnels.sessions": 274, "fct_product_funnels.purchases": 4, "fct_product_funnels.revenue": 157.24},
        {"fct_product_funnels.date.day": "2026-02-23T00:00:00.000", "fct_product_funnels.sessions": 296, "fct_product_funnels.purchases": 4, "fct_product_funnels.revenue": 244.93},
        {"fct_product_funnels.date.day": "2026-02-24T00:00:00.000", "fct_product_funnels.sessions": 644, "fct_product_funnels.purchases": 4, "fct_product_funnels.revenue": 193.13},
        {"fct_product_funnels.date.day": "2026-02-25T00:00:00.000", "fct_product_funnels.sessions": 396, "fct_product_funnels.purchases": 14, "fct_product_funnels.revenue": 839.11},
        {"fct_product_funnels.date.day": "2026-02-26T00:00:00.000", "fct_product_funnels.sessions": 550, "fct_product_funnels.purchases": 6, "fct_product_funnels.revenue": 283.12},
        {"fct_product_funnels.date.day": "2026-02-27T00:00:00.000", "fct_product_funnels.sessions": 478, "fct_product_funnels.purchases": 4, "fct_product_funnels.revenue": 170.64},
        {"fct_product_funnels.date.day": "2026-02-28T00:00:00.000", "fct_product_funnels.sessions": 413, "fct_product_funnels.purchases": 3, "fct_product_funnels.revenue": 117.34},
        {"fct_product_funnels.date.day": "2026-03-01T00:00:00.000", "fct_product_funnels.sessions": 560, "fct_product_funnels.purchases": 4, "fct_product_funnels.revenue": 201.27},
        {"fct_product_funnels.date.day": "2026-03-02T00:00:00.000", "fct_product_funnels.sessions": 381, "fct_product_funnels.purchases": 2, "fct_product_funnels.revenue": 65.18},
        {"fct_product_funnels.date.day": "2026-03-03T00:00:00.000", "fct_product_funnels.sessions": 317, "fct_product_funnels.purchases": 0, "fct_product_funnels.revenue": 0},
        {"fct_product_funnels.date.day": "2026-03-04T00:00:00.000", "fct_product_funnels.sessions": 617, "fct_product_funnels.purchases": 2, "fct_product_funnels.revenue": 95.31},
        {"fct_product_funnels.date.day": "2026-03-05T00:00:00.000", "fct_product_funnels.sessions": 219, "fct_product_funnels.purchases": 2, "fct_product_funnels.revenue": 64.84},
        {"fct_product_funnels.date.day": "2026-03-06T00:00:00.000", "fct_product_funnels.sessions": 99, "fct_product_funnels.purchases": 2, "fct_product_funnels.revenue": 93.19},
        {"fct_product_funnels.date.day": "2026-03-07T00:00:00.000", "fct_product_funnels.sessions": 75, "fct_product_funnels.purchases": 2, "fct_product_funnels.revenue": 33.1},
        {"fct_product_funnels.date.day": "2026-03-08T00:00:00.000", "fct_product_funnels.sessions": 159, "fct_product_funnels.purchases": 2, "fct_product_funnels.revenue": 98.8},
        {"fct_product_funnels.date.day": "2026-03-09T00:00:00.000", "fct_product_funnels.sessions": 96, "fct_product_funnels.purchases": 2, "fct_product_funnels.revenue": 85.58},
        {"fct_product_funnels.date.day": "2026-03-10T00:00:00.000", "fct_product_funnels.sessions": 138, "fct_product_funnels.purchases": 0, "fct_product_funnels.revenue": 0},
        {"fct_product_funnels.date.day": "2026-03-11T00:00:00.000", "fct_product_funnels.sessions": 84, "fct_product_funnels.purchases": 0, "fct_product_funnels.revenue": 0},
        {"fct_product_funnels.date.day": "2026-03-12T00:00:00.000", "fct_product_funnels.sessions": 72, "fct_product_funnels.purchases": 0, "fct_product_funnels.revenue": 0},
        {"fct_product_funnels.date.day": "2026-03-13T00:00:00.000", "fct_product_funnels.sessions": 183, "fct_product_funnels.purchases": 0, "fct_product_funnels.revenue": 0},
        {"fct_product_funnels.date.day": "2026-03-14T00:00:00.000", "fct_product_funnels.sessions": 107, "fct_product_funnels.purchases": 0, "fct_product_funnels.revenue": 0},
        {"fct_product_funnels.date.day": "2026-03-15T00:00:00.000", "fct_product_funnels.sessions": 91, "fct_product_funnels.purchases": 0, "fct_product_funnels.revenue": 0},
        {"fct_product_funnels.date.day": "2026-03-16T00:00:00.000", "fct_product_funnels.sessions": 145, "fct_product_funnels.purchases": 0, "fct_product_funnels.revenue": 0},
        {"fct_product_funnels.date.day": "2026-03-17T00:00:00.000", "fct_product_funnels.sessions": 56, "fct_product_funnels.purchases": 0, "fct_product_funnels.revenue": 0},
    ],

    # Little Saints
    "8be8e4b7-d7c1-4922-b8e3-271671ee1592": [
        {"fct_product_funnels.date.day": "2026-02-01T00:00:00.000", "fct_product_funnels.sessions": 524, "fct_product_funnels.purchases": 2, "fct_product_funnels.revenue": 315},
        {"fct_product_funnels.date.day": "2026-02-02T00:00:00.000", "fct_product_funnels.sessions": 370, "fct_product_funnels.purchases": 2, "fct_product_funnels.revenue": 382.5},
        {"fct_product_funnels.date.day": "2026-02-03T00:00:00.000", "fct_product_funnels.sessions": 123, "fct_product_funnels.purchases": 3, "fct_product_funnels.revenue": 251.25},
        {"fct_product_funnels.date.day": "2026-02-04T00:00:00.000", "fct_product_funnels.sessions": 73, "fct_product_funnels.purchases": 0, "fct_product_funnels.revenue": 0},
        {"fct_product_funnels.date.day": "2026-02-05T00:00:00.000", "fct_product_funnels.sessions": 183, "fct_product_funnels.purchases": 2, "fct_product_funnels.revenue": 262.5},
        {"fct_product_funnels.date.day": "2026-02-06T00:00:00.000", "fct_product_funnels.sessions": 200, "fct_product_funnels.purchases": 1, "fct_product_funnels.revenue": 157.5},
        {"fct_product_funnels.date.day": "2026-02-07T00:00:00.000", "fct_product_funnels.sessions": 41, "fct_product_funnels.purchases": 1, "fct_product_funnels.revenue": 225},
        {"fct_product_funnels.date.day": "2026-02-08T00:00:00.000", "fct_product_funnels.sessions": 4, "fct_product_funnels.purchases": 0, "fct_product_funnels.revenue": 0},
        {"fct_product_funnels.date.day": "2026-02-09T00:00:00.000", "fct_product_funnels.sessions": 16, "fct_product_funnels.purchases": 0, "fct_product_funnels.revenue": 0},
        {"fct_product_funnels.date.day": "2026-02-10T00:00:00.000", "fct_product_funnels.sessions": 5, "fct_product_funnels.purchases": 0, "fct_product_funnels.revenue": 0},
        {"fct_product_funnels.date.day": "2026-02-11T00:00:00.000", "fct_product_funnels.sessions": 6, "fct_product_funnels.purchases": 0, "fct_product_funnels.revenue": 0},
        {"fct_product_funnels.date.day": "2026-02-12T00:00:00.000", "fct_product_funnels.sessions": 35, "fct_product_funnels.purchases": 0, "fct_product_funnels.revenue": 0},
        {"fct_product_funnels.date.day": "2026-02-13T00:00:00.000", "fct_product_funnels.sessions": 2, "fct_product_funnels.purchases": 0, "fct_product_funnels.revenue": 0},
        {"fct_product_funnels.date.day": "2026-02-14T00:00:00.000", "fct_product_funnels.sessions": 5, "fct_product_funnels.purchases": 0, "fct_product_funnels.revenue": 0},
        {"fct_product_funnels.date.day": "2026-02-15T00:00:00.000", "fct_product_funnels.sessions": 9, "fct_product_funnels.purchases": 1, "fct_product_funnels.revenue": 123.75},
        {"fct_product_funnels.date.day": "2026-02-16T00:00:00.000", "fct_product_funnels.sessions": 4, "fct_product_funnels.purchases": 0, "fct_product_funnels.revenue": 0},
        {"fct_product_funnels.date.day": "2026-02-17T00:00:00.000", "fct_product_funnels.sessions": 15, "fct_product_funnels.purchases": 0, "fct_product_funnels.revenue": 0},
        {"fct_product_funnels.date.day": "2026-02-18T00:00:00.000", "fct_product_funnels.sessions": 31, "fct_product_funnels.purchases": 0, "fct_product_funnels.revenue": 0},
        {"fct_product_funnels.date.day": "2026-02-19T00:00:00.000", "fct_product_funnels.sessions": 59, "fct_product_funnels.purchases": 0, "fct_product_funnels.revenue": 0},
        {"fct_product_funnels.date.day": "2026-02-20T00:00:00.000", "fct_product_funnels.sessions": 5, "fct_product_funnels.purchases": 0, "fct_product_funnels.revenue": 0},
        {"fct_product_funnels.date.day": "2026-02-21T00:00:00.000", "fct_product_funnels.sessions": 584, "fct_product_funnels.purchases": 3, "fct_product_funnels.revenue": 191.25},
        {"fct_product_funnels.date.day": "2026-02-22T00:00:00.000", "fct_product_funnels.sessions": 1612, "fct_product_funnels.purchases": 11, "fct_product_funnels.revenue": 891.25},
        {"fct_product_funnels.date.day": "2026-02-23T00:00:00.000", "fct_product_funnels.sessions": 302, "fct_product_funnels.purchases": 2, "fct_product_funnels.revenue": 198.75},
        {"fct_product_funnels.date.day": "2026-02-24T00:00:00.000", "fct_product_funnels.sessions": 113, "fct_product_funnels.purchases": 0, "fct_product_funnels.revenue": 0},
        {"fct_product_funnels.date.day": "2026-02-25T00:00:00.000", "fct_product_funnels.sessions": 79, "fct_product_funnels.purchases": 1, "fct_product_funnels.revenue": 63.75},
        {"fct_product_funnels.date.day": "2026-02-26T00:00:00.000", "fct_product_funnels.sessions": 101, "fct_product_funnels.purchases": 2, "fct_product_funnels.revenue": 232.5},
        {"fct_product_funnels.date.day": "2026-02-27T00:00:00.000", "fct_product_funnels.sessions": 99, "fct_product_funnels.purchases": 0, "fct_product_funnels.revenue": 0},
        {"fct_product_funnels.date.day": "2026-02-28T00:00:00.000", "fct_product_funnels.sessions": 85, "fct_product_funnels.purchases": 1, "fct_product_funnels.revenue": 63.75},
        {"fct_product_funnels.date.day": "2026-03-01T00:00:00.000", "fct_product_funnels.sessions": 119, "fct_product_funnels.purchases": 0, "fct_product_funnels.revenue": 0},
        {"fct_product_funnels.date.day": "2026-03-02T00:00:00.000", "fct_product_funnels.sessions": 79, "fct_product_funnels.purchases": 0, "fct_product_funnels.revenue": 0},
        {"fct_product_funnels.date.day": "2026-03-03T00:00:00.000", "fct_product_funnels.sessions": 101, "fct_product_funnels.purchases": 0, "fct_product_funnels.revenue": 0},
        {"fct_product_funnels.date.day": "2026-03-04T00:00:00.000", "fct_product_funnels.sessions": 32, "fct_product_funnels.purchases": 0, "fct_product_funnels.revenue": 0},
        {"fct_product_funnels.date.day": "2026-03-05T00:00:00.000", "fct_product_funnels.sessions": 8, "fct_product_funnels.purchases": 0, "fct_product_funnels.revenue": 0},
        {"fct_product_funnels.date.day": "2026-03-06T00:00:00.000", "fct_product_funnels.sessions": 3, "fct_product_funnels.purchases": 0, "fct_product_funnels.revenue": 0},
        {"fct_product_funnels.date.day": "2026-03-07T00:00:00.000", "fct_product_funnels.sessions": 7, "fct_product_funnels.purchases": 0, "fct_product_funnels.revenue": 0},
        {"fct_product_funnels.date.day": "2026-03-08T00:00:00.000", "fct_product_funnels.sessions": 1, "fct_product_funnels.purchases": 0, "fct_product_funnels.revenue": 0},
        {"fct_product_funnels.date.day": "2026-03-09T00:00:00.000", "fct_product_funnels.sessions": 2, "fct_product_funnels.purchases": 0, "fct_product_funnels.revenue": 0},
        {"fct_product_funnels.date.day": "2026-03-10T00:00:00.000", "fct_product_funnels.sessions": 3, "fct_product_funnels.purchases": 0, "fct_product_funnels.revenue": 0},
        {"fct_product_funnels.date.day": "2026-03-11T00:00:00.000", "fct_product_funnels.sessions": 8, "fct_product_funnels.purchases": 0, "fct_product_funnels.revenue": 0},
        {"fct_product_funnels.date.day": "2026-03-12T00:00:00.000", "fct_product_funnels.sessions": 2, "fct_product_funnels.purchases": 0, "fct_product_funnels.revenue": 0},
        {"fct_product_funnels.date.day": "2026-03-13T00:00:00.000", "fct_product_funnels.sessions": 25, "fct_product_funnels.purchases": 0, "fct_product_funnels.revenue": 0},
        {"fct_product_funnels.date.day": "2026-03-14T00:00:00.000", "fct_product_funnels.sessions": 47, "fct_product_funnels.purchases": 0, "fct_product_funnels.revenue": 0},
        {"fct_product_funnels.date.day": "2026-03-15T00:00:00.000", "fct_product_funnels.sessions": 162, "fct_product_funnels.purchases": 1, "fct_product_funnels.revenue": 63.75},
        {"fct_product_funnels.date.day": "2026-03-16T00:00:00.000", "fct_product_funnels.sessions": 144, "fct_product_funnels.purchases": 0, "fct_product_funnels.revenue": 0},
        {"fct_product_funnels.date.day": "2026-03-17T00:00:00.000", "fct_product_funnels.sessions": 123, "fct_product_funnels.purchases": 1, "fct_product_funnels.revenue": 63.75},
    ],

    # Henry Rose
    "f7983632-4d4b-49c8-8e7a-192e9e999dff": [
        {"fct_product_funnels.date.day": "2026-02-01T00:00:00.000", "fct_product_funnels.sessions": 1891, "fct_product_funnels.purchases": 44, "fct_product_funnels.revenue": 3233},
        {"fct_product_funnels.date.day": "2026-02-02T00:00:00.000", "fct_product_funnels.sessions": 1602, "fct_product_funnels.purchases": 29, "fct_product_funnels.revenue": 2313.66},
        {"fct_product_funnels.date.day": "2026-02-03T00:00:00.000", "fct_product_funnels.sessions": 1318, "fct_product_funnels.purchases": 21, "fct_product_funnels.revenue": 1409.79},
        {"fct_product_funnels.date.day": "2026-02-04T00:00:00.000", "fct_product_funnels.sessions": 1319, "fct_product_funnels.purchases": 19, "fct_product_funnels.revenue": 1395.78},
        {"fct_product_funnels.date.day": "2026-02-05T00:00:00.000", "fct_product_funnels.sessions": 1038, "fct_product_funnels.purchases": 13, "fct_product_funnels.revenue": 919.86},
        {"fct_product_funnels.date.day": "2026-02-06T00:00:00.000", "fct_product_funnels.sessions": 1004, "fct_product_funnels.purchases": 10, "fct_product_funnels.revenue": 839.86},
        {"fct_product_funnels.date.day": "2026-02-07T00:00:00.000", "fct_product_funnels.sessions": 1044, "fct_product_funnels.purchases": 17, "fct_product_funnels.revenue": 1160.83},
        {"fct_product_funnels.date.day": "2026-02-08T00:00:00.000", "fct_product_funnels.sessions": 999, "fct_product_funnels.purchases": 25, "fct_product_funnels.revenue": 2140.46},
        {"fct_product_funnels.date.day": "2026-02-09T00:00:00.000", "fct_product_funnels.sessions": 1026, "fct_product_funnels.purchases": 15, "fct_product_funnels.revenue": 1296.85},
        {"fct_product_funnels.date.day": "2026-02-10T00:00:00.000", "fct_product_funnels.sessions": 1275, "fct_product_funnels.purchases": 20, "fct_product_funnels.revenue": 1705.72},
        {"fct_product_funnels.date.day": "2026-02-11T00:00:00.000", "fct_product_funnels.sessions": 1958, "fct_product_funnels.purchases": 48, "fct_product_funnels.revenue": 3659.74},
        {"fct_product_funnels.date.day": "2026-02-12T00:00:00.000", "fct_product_funnels.sessions": 2074, "fct_product_funnels.purchases": 32, "fct_product_funnels.revenue": 2215.64},
        {"fct_product_funnels.date.day": "2026-02-13T00:00:00.000", "fct_product_funnels.sessions": 1546, "fct_product_funnels.purchases": 25, "fct_product_funnels.revenue": 2216.67},
        {"fct_product_funnels.date.day": "2026-02-14T00:00:00.000", "fct_product_funnels.sessions": 1699, "fct_product_funnels.purchases": 37, "fct_product_funnels.revenue": 2763.13},
        {"fct_product_funnels.date.day": "2026-02-15T00:00:00.000", "fct_product_funnels.sessions": 2039, "fct_product_funnels.purchases": 36, "fct_product_funnels.revenue": 2528.62},
        {"fct_product_funnels.date.day": "2026-02-16T00:00:00.000", "fct_product_funnels.sessions": 3006, "fct_product_funnels.purchases": 62, "fct_product_funnels.revenue": 4364.56},
        {"fct_product_funnels.date.day": "2026-02-17T00:00:00.000", "fct_product_funnels.sessions": 172, "fct_product_funnels.purchases": 2, "fct_product_funnels.revenue": 349.95},
        {"fct_product_funnels.date.day": "2026-02-18T00:00:00.000", "fct_product_funnels.sessions": 2721, "fct_product_funnels.purchases": 81, "fct_product_funnels.revenue": 5885.56},
        {"fct_product_funnels.date.day": "2026-02-19T00:00:00.000", "fct_product_funnels.sessions": 3765, "fct_product_funnels.purchases": 112, "fct_product_funnels.revenue": 7520.56},
        {"fct_product_funnels.date.day": "2026-02-20T00:00:00.000", "fct_product_funnels.sessions": 4446, "fct_product_funnels.purchases": 94, "fct_product_funnels.revenue": 6823.45},
        {"fct_product_funnels.date.day": "2026-02-21T00:00:00.000", "fct_product_funnels.sessions": 2562, "fct_product_funnels.purchases": 58, "fct_product_funnels.revenue": 4243.13},
        {"fct_product_funnels.date.day": "2026-02-22T00:00:00.000", "fct_product_funnels.sessions": 4942, "fct_product_funnels.purchases": 109, "fct_product_funnels.revenue": 7799.45},
        {"fct_product_funnels.date.day": "2026-02-23T00:00:00.000", "fct_product_funnels.sessions": 4378, "fct_product_funnels.purchases": 106, "fct_product_funnels.revenue": 7102.92},
        {"fct_product_funnels.date.day": "2026-02-24T00:00:00.000", "fct_product_funnels.sessions": 3519, "fct_product_funnels.purchases": 78, "fct_product_funnels.revenue": 5980.61},
        {"fct_product_funnels.date.day": "2026-02-25T00:00:00.000", "fct_product_funnels.sessions": 2671, "fct_product_funnels.purchases": 58, "fct_product_funnels.revenue": 4689.29},
        {"fct_product_funnels.date.day": "2026-02-26T00:00:00.000", "fct_product_funnels.sessions": 3166, "fct_product_funnels.purchases": 72, "fct_product_funnels.revenue": 5205.91},
        {"fct_product_funnels.date.day": "2026-02-27T00:00:00.000", "fct_product_funnels.sessions": 2212, "fct_product_funnels.purchases": 51, "fct_product_funnels.revenue": 3482.06},
        {"fct_product_funnels.date.day": "2026-02-28T00:00:00.000", "fct_product_funnels.sessions": 2461, "fct_product_funnels.purchases": 55, "fct_product_funnels.revenue": 4376.08},
        {"fct_product_funnels.date.day": "2026-03-01T00:00:00.000", "fct_product_funnels.sessions": 3409, "fct_product_funnels.purchases": 78, "fct_product_funnels.revenue": 6233.74},
        {"fct_product_funnels.date.day": "2026-03-02T00:00:00.000", "fct_product_funnels.sessions": 2868, "fct_product_funnels.purchases": 58, "fct_product_funnels.revenue": 4601.44},
        {"fct_product_funnels.date.day": "2026-03-03T00:00:00.000", "fct_product_funnels.sessions": 3172, "fct_product_funnels.purchases": 60, "fct_product_funnels.revenue": 4290.35},
        {"fct_product_funnels.date.day": "2026-03-04T00:00:00.000", "fct_product_funnels.sessions": 2516, "fct_product_funnels.purchases": 49, "fct_product_funnels.revenue": 3209.44},
        {"fct_product_funnels.date.day": "2026-03-05T00:00:00.000", "fct_product_funnels.sessions": 2556, "fct_product_funnels.purchases": 55, "fct_product_funnels.revenue": 3896.89},
        {"fct_product_funnels.date.day": "2026-03-06T00:00:00.000", "fct_product_funnels.sessions": 2346, "fct_product_funnels.purchases": 44, "fct_product_funnels.revenue": 3507.47},
        {"fct_product_funnels.date.day": "2026-03-07T00:00:00.000", "fct_product_funnels.sessions": 2316, "fct_product_funnels.purchases": 58, "fct_product_funnels.revenue": 3625.68},
        {"fct_product_funnels.date.day": "2026-03-08T00:00:00.000", "fct_product_funnels.sessions": 2531, "fct_product_funnels.purchases": 61, "fct_product_funnels.revenue": 4889.05},
        {"fct_product_funnels.date.day": "2026-03-09T00:00:00.000", "fct_product_funnels.sessions": 2892, "fct_product_funnels.purchases": 75, "fct_product_funnels.revenue": 5495.44},
        {"fct_product_funnels.date.day": "2026-03-10T00:00:00.000", "fct_product_funnels.sessions": 3559, "fct_product_funnels.purchases": 63, "fct_product_funnels.revenue": 4256.32},
        {"fct_product_funnels.date.day": "2026-03-11T00:00:00.000", "fct_product_funnels.sessions": 3051, "fct_product_funnels.purchases": 51, "fct_product_funnels.revenue": 3382.93},
        {"fct_product_funnels.date.day": "2026-03-12T00:00:00.000", "fct_product_funnels.sessions": 3292, "fct_product_funnels.purchases": 47, "fct_product_funnels.revenue": 3680.2},
        {"fct_product_funnels.date.day": "2026-03-13T00:00:00.000", "fct_product_funnels.sessions": 2410, "fct_product_funnels.purchases": 40, "fct_product_funnels.revenue": 2939.84},
        {"fct_product_funnels.date.day": "2026-03-14T00:00:00.000", "fct_product_funnels.sessions": 2860, "fct_product_funnels.purchases": 48, "fct_product_funnels.revenue": 3647.96},
        {"fct_product_funnels.date.day": "2026-03-15T00:00:00.000", "fct_product_funnels.sessions": 3077, "fct_product_funnels.purchases": 50, "fct_product_funnels.revenue": 3559.25},
        {"fct_product_funnels.date.day": "2026-03-16T00:00:00.000", "fct_product_funnels.sessions": 3319, "fct_product_funnels.purchases": 36, "fct_product_funnels.revenue": 2679.4},
        {"fct_product_funnels.date.day": "2026-03-17T00:00:00.000", "fct_product_funnels.sessions": 2171, "fct_product_funnels.purchases": 41, "fct_product_funnels.revenue": 2790.35},
    ],

    # Veracity Selfcare
    "f8f83f9d-be9e-4177-ad7e-292ed079eafd": [
        {"fct_product_funnels.date.day": "2026-02-01T00:00:00.000", "fct_product_funnels.sessions": 561, "fct_product_funnels.purchases": 10, "fct_product_funnels.revenue": 1041.78},
        {"fct_product_funnels.date.day": "2026-02-02T00:00:00.000", "fct_product_funnels.sessions": 601, "fct_product_funnels.purchases": 13, "fct_product_funnels.revenue": 1566.27},
        {"fct_product_funnels.date.day": "2026-02-03T00:00:00.000", "fct_product_funnels.sessions": 515, "fct_product_funnels.purchases": 9, "fct_product_funnels.revenue": 978.24},
        {"fct_product_funnels.date.day": "2026-02-04T00:00:00.000", "fct_product_funnels.sessions": 464, "fct_product_funnels.purchases": 7, "fct_product_funnels.revenue": 1006.05},
        {"fct_product_funnels.date.day": "2026-02-05T00:00:00.000", "fct_product_funnels.sessions": 515, "fct_product_funnels.purchases": 8, "fct_product_funnels.revenue": 891.51},
        {"fct_product_funnels.date.day": "2026-02-06T00:00:00.000", "fct_product_funnels.sessions": 581, "fct_product_funnels.purchases": 15, "fct_product_funnels.revenue": 1486.47},
        {"fct_product_funnels.date.day": "2026-02-07T00:00:00.000", "fct_product_funnels.sessions": 431, "fct_product_funnels.purchases": 8, "fct_product_funnels.revenue": 967.25},
        {"fct_product_funnels.date.day": "2026-02-08T00:00:00.000", "fct_product_funnels.sessions": 513, "fct_product_funnels.purchases": 5, "fct_product_funnels.revenue": 571.45},
        {"fct_product_funnels.date.day": "2026-02-09T00:00:00.000", "fct_product_funnels.sessions": 500, "fct_product_funnels.purchases": 11, "fct_product_funnels.revenue": 1263.55},
        {"fct_product_funnels.date.day": "2026-02-10T00:00:00.000", "fct_product_funnels.sessions": 594, "fct_product_funnels.purchases": 10, "fct_product_funnels.revenue": 1321.06},
        {"fct_product_funnels.date.day": "2026-02-11T00:00:00.000", "fct_product_funnels.sessions": 453, "fct_product_funnels.purchases": 9, "fct_product_funnels.revenue": 1019.76},
        {"fct_product_funnels.date.day": "2026-02-12T00:00:00.000", "fct_product_funnels.sessions": 410, "fct_product_funnels.purchases": 9, "fct_product_funnels.revenue": 876.65},
        {"fct_product_funnels.date.day": "2026-02-13T00:00:00.000", "fct_product_funnels.sessions": 461, "fct_product_funnels.purchases": 5, "fct_product_funnels.revenue": 679.25},
        {"fct_product_funnels.date.day": "2026-02-14T00:00:00.000", "fct_product_funnels.sessions": 509, "fct_product_funnels.purchases": 8, "fct_product_funnels.revenue": 871.21},
        {"fct_product_funnels.date.day": "2026-02-15T00:00:00.000", "fct_product_funnels.sessions": 612, "fct_product_funnels.purchases": 14, "fct_product_funnels.revenue": 1329.1},
        {"fct_product_funnels.date.day": "2026-02-16T00:00:00.000", "fct_product_funnels.sessions": 542, "fct_product_funnels.purchases": 6, "fct_product_funnels.revenue": 676.3},
        {"fct_product_funnels.date.day": "2026-02-17T00:00:00.000", "fct_product_funnels.sessions": 561, "fct_product_funnels.purchases": 6, "fct_product_funnels.revenue": 706.41},
        {"fct_product_funnels.date.day": "2026-02-18T00:00:00.000", "fct_product_funnels.sessions": 465, "fct_product_funnels.purchases": 13, "fct_product_funnels.revenue": 1869.15},
        {"fct_product_funnels.date.day": "2026-02-19T00:00:00.000", "fct_product_funnels.sessions": 524, "fct_product_funnels.purchases": 7, "fct_product_funnels.revenue": 764.66},
        {"fct_product_funnels.date.day": "2026-02-20T00:00:00.000", "fct_product_funnels.sessions": 472, "fct_product_funnels.purchases": 3, "fct_product_funnels.revenue": 525.9},
        {"fct_product_funnels.date.day": "2026-02-21T00:00:00.000", "fct_product_funnels.sessions": 419, "fct_product_funnels.purchases": 12, "fct_product_funnels.revenue": 1358.44},
        {"fct_product_funnels.date.day": "2026-02-22T00:00:00.000", "fct_product_funnels.sessions": 564, "fct_product_funnels.purchases": 14, "fct_product_funnels.revenue": 1870.44},
        {"fct_product_funnels.date.day": "2026-02-23T00:00:00.000", "fct_product_funnels.sessions": 459, "fct_product_funnels.purchases": 11, "fct_product_funnels.revenue": 1464.47},
        {"fct_product_funnels.date.day": "2026-02-24T00:00:00.000", "fct_product_funnels.sessions": 504, "fct_product_funnels.purchases": 12, "fct_product_funnels.revenue": 1035.65},
        {"fct_product_funnels.date.day": "2026-02-25T00:00:00.000", "fct_product_funnels.sessions": 495, "fct_product_funnels.purchases": 7, "fct_product_funnels.revenue": 810.05},
        {"fct_product_funnels.date.day": "2026-02-26T00:00:00.000", "fct_product_funnels.sessions": 384, "fct_product_funnels.purchases": 6, "fct_product_funnels.revenue": 785.3},
        {"fct_product_funnels.date.day": "2026-02-27T00:00:00.000", "fct_product_funnels.sessions": 387, "fct_product_funnels.purchases": 9, "fct_product_funnels.revenue": 1573.27},
        {"fct_product_funnels.date.day": "2026-02-28T00:00:00.000", "fct_product_funnels.sessions": 471, "fct_product_funnels.purchases": 10, "fct_product_funnels.revenue": 1307.07},
        {"fct_product_funnels.date.day": "2026-03-01T00:00:00.000", "fct_product_funnels.sessions": 428, "fct_product_funnels.purchases": 15, "fct_product_funnels.revenue": 1653.81},
        {"fct_product_funnels.date.day": "2026-03-02T00:00:00.000", "fct_product_funnels.sessions": 428, "fct_product_funnels.purchases": 9, "fct_product_funnels.revenue": 994.46},
        {"fct_product_funnels.date.day": "2026-03-03T00:00:00.000", "fct_product_funnels.sessions": 1068, "fct_product_funnels.purchases": 49, "fct_product_funnels.revenue": 6588.07},
        {"fct_product_funnels.date.day": "2026-03-04T00:00:00.000", "fct_product_funnels.sessions": 770, "fct_product_funnels.purchases": 29, "fct_product_funnels.revenue": 3604.16},
        {"fct_product_funnels.date.day": "2026-03-05T00:00:00.000", "fct_product_funnels.sessions": 692, "fct_product_funnels.purchases": 12, "fct_product_funnels.revenue": 1660.16},
        {"fct_product_funnels.date.day": "2026-03-06T00:00:00.000", "fct_product_funnels.sessions": 651, "fct_product_funnels.purchases": 13, "fct_product_funnels.revenue": 1993.96},
        {"fct_product_funnels.date.day": "2026-03-07T00:00:00.000", "fct_product_funnels.sessions": 653, "fct_product_funnels.purchases": 15, "fct_product_funnels.revenue": 1498.07},
        {"fct_product_funnels.date.day": "2026-03-08T00:00:00.000", "fct_product_funnels.sessions": 754, "fct_product_funnels.purchases": 12, "fct_product_funnels.revenue": 1261.07},
        {"fct_product_funnels.date.day": "2026-03-09T00:00:00.000", "fct_product_funnels.sessions": 822, "fct_product_funnels.purchases": 31, "fct_product_funnels.revenue": 4030.48},
        {"fct_product_funnels.date.day": "2026-03-10T00:00:00.000", "fct_product_funnels.sessions": 387, "fct_product_funnels.purchases": 12, "fct_product_funnels.revenue": 1445.46},
        {"fct_product_funnels.date.day": "2026-03-11T00:00:00.000", "fct_product_funnels.sessions": 351, "fct_product_funnels.purchases": 3, "fct_product_funnels.revenue": 332.25},
        {"fct_product_funnels.date.day": "2026-03-12T00:00:00.000", "fct_product_funnels.sessions": 303, "fct_product_funnels.purchases": 9, "fct_product_funnels.revenue": 795.2},
        {"fct_product_funnels.date.day": "2026-03-13T00:00:00.000", "fct_product_funnels.sessions": 197, "fct_product_funnels.purchases": 6, "fct_product_funnels.revenue": 884.55},
        {"fct_product_funnels.date.day": "2026-03-14T00:00:00.000", "fct_product_funnels.sessions": 340, "fct_product_funnels.purchases": 11, "fct_product_funnels.revenue": 1233.63},
        {"fct_product_funnels.date.day": "2026-03-15T00:00:00.000", "fct_product_funnels.sessions": 431, "fct_product_funnels.purchases": 12, "fct_product_funnels.revenue": 1233.21},
        {"fct_product_funnels.date.day": "2026-03-16T00:00:00.000", "fct_product_funnels.sessions": 396, "fct_product_funnels.purchases": 10, "fct_product_funnels.revenue": 1119.02},
        {"fct_product_funnels.date.day": "2026-03-17T00:00:00.000", "fct_product_funnels.sessions": 367, "fct_product_funnels.purchases": 10, "fct_product_funnels.revenue": 1240.5},
    ],

    # Sole Toscana
    "c686cb26-9441-4aa2-883e-7204999f2bc4": [
        {"fct_product_funnels.date.day": "2026-02-01T00:00:00.000", "fct_product_funnels.sessions": 861, "fct_product_funnels.purchases": 3, "fct_product_funnels.revenue": 173.25},
        {"fct_product_funnels.date.day": "2026-02-02T00:00:00.000", "fct_product_funnels.sessions": 1279, "fct_product_funnels.purchases": 2, "fct_product_funnels.revenue": 135},
        {"fct_product_funnels.date.day": "2026-02-03T00:00:00.000", "fct_product_funnels.sessions": 1299, "fct_product_funnels.purchases": 0, "fct_product_funnels.revenue": 0},
        {"fct_product_funnels.date.day": "2026-02-04T00:00:00.000", "fct_product_funnels.sessions": 1395, "fct_product_funnels.purchases": 2, "fct_product_funnels.revenue": 115},
        {"fct_product_funnels.date.day": "2026-02-05T00:00:00.000", "fct_product_funnels.sessions": 1814, "fct_product_funnels.purchases": 0, "fct_product_funnels.revenue": 0},
        {"fct_product_funnels.date.day": "2026-02-06T00:00:00.000", "fct_product_funnels.sessions": 1469, "fct_product_funnels.purchases": 2, "fct_product_funnels.revenue": 135},
        {"fct_product_funnels.date.day": "2026-02-07T00:00:00.000", "fct_product_funnels.sessions": 1230, "fct_product_funnels.purchases": 2, "fct_product_funnels.revenue": 68},
        {"fct_product_funnels.date.day": "2026-02-08T00:00:00.000", "fct_product_funnels.sessions": 1465, "fct_product_funnels.purchases": 2, "fct_product_funnels.revenue": 90},
        {"fct_product_funnels.date.day": "2026-02-09T00:00:00.000", "fct_product_funnels.sessions": 1486, "fct_product_funnels.purchases": 1, "fct_product_funnels.revenue": 90},
        {"fct_product_funnels.date.day": "2026-02-10T00:00:00.000", "fct_product_funnels.sessions": 1518, "fct_product_funnels.purchases": 2, "fct_product_funnels.revenue": 80},
        {"fct_product_funnels.date.day": "2026-02-11T00:00:00.000", "fct_product_funnels.sessions": 1133, "fct_product_funnels.purchases": 1, "fct_product_funnels.revenue": 40.5},
        {"fct_product_funnels.date.day": "2026-02-12T00:00:00.000", "fct_product_funnels.sessions": 1350, "fct_product_funnels.purchases": 0, "fct_product_funnels.revenue": 0},
        {"fct_product_funnels.date.day": "2026-02-13T00:00:00.000", "fct_product_funnels.sessions": 1326, "fct_product_funnels.purchases": 0, "fct_product_funnels.revenue": 0},
        {"fct_product_funnels.date.day": "2026-02-14T00:00:00.000", "fct_product_funnels.sessions": 1226, "fct_product_funnels.purchases": 1, "fct_product_funnels.revenue": 38.25},
        {"fct_product_funnels.date.day": "2026-02-15T00:00:00.000", "fct_product_funnels.sessions": 1180, "fct_product_funnels.purchases": 2, "fct_product_funnels.revenue": 83.25},
        {"fct_product_funnels.date.day": "2026-02-16T00:00:00.000", "fct_product_funnels.sessions": 627, "fct_product_funnels.purchases": 0, "fct_product_funnels.revenue": 0},
        {"fct_product_funnels.date.day": "2026-02-17T00:00:00.000", "fct_product_funnels.sessions": 3201, "fct_product_funnels.purchases": 0, "fct_product_funnels.revenue": 0},
        {"fct_product_funnels.date.day": "2026-02-18T00:00:00.000", "fct_product_funnels.sessions": 59, "fct_product_funnels.purchases": 1, "fct_product_funnels.revenue": 45},
        {"fct_product_funnels.date.day": "2026-02-19T00:00:00.000", "fct_product_funnels.sessions": 70, "fct_product_funnels.purchases": 0, "fct_product_funnels.revenue": 0},
        {"fct_product_funnels.date.day": "2026-02-20T00:00:00.000", "fct_product_funnels.sessions": 76, "fct_product_funnels.purchases": 2, "fct_product_funnels.revenue": 147},
        {"fct_product_funnels.date.day": "2026-02-21T00:00:00.000", "fct_product_funnels.sessions": 97, "fct_product_funnels.purchases": 1, "fct_product_funnels.revenue": 35},
        {"fct_product_funnels.date.day": "2026-02-22T00:00:00.000", "fct_product_funnels.sessions": 49, "fct_product_funnels.purchases": 0, "fct_product_funnels.revenue": 0},
        {"fct_product_funnels.date.day": "2026-02-23T00:00:00.000", "fct_product_funnels.sessions": 62, "fct_product_funnels.purchases": 1, "fct_product_funnels.revenue": 102},
        {"fct_product_funnels.date.day": "2026-02-24T00:00:00.000", "fct_product_funnels.sessions": 107, "fct_product_funnels.purchases": 2, "fct_product_funnels.revenue": 178.8},
        {"fct_product_funnels.date.day": "2026-02-25T00:00:00.000", "fct_product_funnels.sessions": 117, "fct_product_funnels.purchases": 1, "fct_product_funnels.revenue": 38.25},
        {"fct_product_funnels.date.day": "2026-02-26T00:00:00.000", "fct_product_funnels.sessions": 213, "fct_product_funnels.purchases": 3, "fct_product_funnels.revenue": 217},
        {"fct_product_funnels.date.day": "2026-02-27T00:00:00.000", "fct_product_funnels.sessions": 332, "fct_product_funnels.purchases": 2, "fct_product_funnels.revenue": 76.5},
        {"fct_product_funnels.date.day": "2026-02-28T00:00:00.000", "fct_product_funnels.sessions": 235, "fct_product_funnels.purchases": 2, "fct_product_funnels.revenue": 76.5},
        {"fct_product_funnels.date.day": "2026-03-01T00:00:00.000", "fct_product_funnels.sessions": 336, "fct_product_funnels.purchases": 4, "fct_product_funnels.revenue": 236.25},
        {"fct_product_funnels.date.day": "2026-03-02T00:00:00.000", "fct_product_funnels.sessions": 297, "fct_product_funnels.purchases": 4, "fct_product_funnels.revenue": 255},
        {"fct_product_funnels.date.day": "2026-03-03T00:00:00.000", "fct_product_funnels.sessions": 213, "fct_product_funnels.purchases": 1, "fct_product_funnels.revenue": 38.25},
        {"fct_product_funnels.date.day": "2026-03-04T00:00:00.000", "fct_product_funnels.sessions": 168, "fct_product_funnels.purchases": 0, "fct_product_funnels.revenue": 0},
        {"fct_product_funnels.date.day": "2026-03-05T00:00:00.000", "fct_product_funnels.sessions": 120, "fct_product_funnels.purchases": 1, "fct_product_funnels.revenue": 38.25},
        {"fct_product_funnels.date.day": "2026-03-06T00:00:00.000", "fct_product_funnels.sessions": 86, "fct_product_funnels.purchases": 1, "fct_product_funnels.revenue": 76.5},
        {"fct_product_funnels.date.day": "2026-03-07T00:00:00.000", "fct_product_funnels.sessions": 53, "fct_product_funnels.purchases": 1, "fct_product_funnels.revenue": 76.5},
        {"fct_product_funnels.date.day": "2026-03-08T00:00:00.000", "fct_product_funnels.sessions": 65, "fct_product_funnels.purchases": 1, "fct_product_funnels.revenue": 23.8},
        {"fct_product_funnels.date.day": "2026-03-09T00:00:00.000", "fct_product_funnels.sessions": 82, "fct_product_funnels.purchases": 0, "fct_product_funnels.revenue": 0},
        {"fct_product_funnels.date.day": "2026-03-10T00:00:00.000", "fct_product_funnels.sessions": 119, "fct_product_funnels.purchases": 2, "fct_product_funnels.revenue": 83.25},
        {"fct_product_funnels.date.day": "2026-03-11T00:00:00.000", "fct_product_funnels.sessions": 87, "fct_product_funnels.purchases": 0, "fct_product_funnels.revenue": 0},
        {"fct_product_funnels.date.day": "2026-03-12T00:00:00.000", "fct_product_funnels.sessions": 149, "fct_product_funnels.purchases": 1, "fct_product_funnels.revenue": 38.25},
        {"fct_product_funnels.date.day": "2026-03-13T00:00:00.000", "fct_product_funnels.sessions": 121, "fct_product_funnels.purchases": 0, "fct_product_funnels.revenue": 0},
        {"fct_product_funnels.date.day": "2026-03-14T00:00:00.000", "fct_product_funnels.sessions": 65, "fct_product_funnels.purchases": 1, "fct_product_funnels.revenue": 102},
        {"fct_product_funnels.date.day": "2026-03-15T00:00:00.000", "fct_product_funnels.sessions": 97, "fct_product_funnels.purchases": 3, "fct_product_funnels.revenue": 308.5},
        {"fct_product_funnels.date.day": "2026-03-16T00:00:00.000", "fct_product_funnels.sessions": 291, "fct_product_funnels.purchases": 2, "fct_product_funnels.revenue": 57.75},
        {"fct_product_funnels.date.day": "2026-03-17T00:00:00.000", "fct_product_funnels.sessions": 113, "fct_product_funnels.purchases": 0, "fct_product_funnels.revenue": 0},
    ],

    # Gains In Bulk
    "5cc7fc09-8acf-4af0-892f-735c6686c2a2": [
        {"fct_product_funnels.date.day": "2026-02-01T00:00:00.000", "fct_product_funnels.sessions": 2, "fct_product_funnels.purchases": 0, "fct_product_funnels.revenue": 0},
        {"fct_product_funnels.date.day": "2026-02-02T00:00:00.000", "fct_product_funnels.sessions": 2, "fct_product_funnels.purchases": 0, "fct_product_funnels.revenue": 0},
        {"fct_product_funnels.date.day": "2026-02-04T00:00:00.000", "fct_product_funnels.sessions": 5, "fct_product_funnels.purchases": 0, "fct_product_funnels.revenue": 0},
        {"fct_product_funnels.date.day": "2026-02-05T00:00:00.000", "fct_product_funnels.sessions": 5, "fct_product_funnels.purchases": 0, "fct_product_funnels.revenue": 0},
        {"fct_product_funnels.date.day": "2026-02-06T00:00:00.000", "fct_product_funnels.sessions": 1, "fct_product_funnels.purchases": 0, "fct_product_funnels.revenue": 0},
        {"fct_product_funnels.date.day": "2026-02-07T00:00:00.000", "fct_product_funnels.sessions": 2, "fct_product_funnels.purchases": 0, "fct_product_funnels.revenue": 0},
        {"fct_product_funnels.date.day": "2026-02-08T00:00:00.000", "fct_product_funnels.sessions": 2, "fct_product_funnels.purchases": 0, "fct_product_funnels.revenue": 0},
        {"fct_product_funnels.date.day": "2026-02-09T00:00:00.000", "fct_product_funnels.sessions": 1, "fct_product_funnels.purchases": 0, "fct_product_funnels.revenue": 0},
        {"fct_product_funnels.date.day": "2026-02-11T00:00:00.000", "fct_product_funnels.sessions": 5, "fct_product_funnels.purchases": 0, "fct_product_funnels.revenue": 0},
        {"fct_product_funnels.date.day": "2026-02-12T00:00:00.000", "fct_product_funnels.sessions": 3, "fct_product_funnels.purchases": 0, "fct_product_funnels.revenue": 0},
        {"fct_product_funnels.date.day": "2026-02-13T00:00:00.000", "fct_product_funnels.sessions": 2, "fct_product_funnels.purchases": 0, "fct_product_funnels.revenue": 0},
        {"fct_product_funnels.date.day": "2026-02-14T00:00:00.000", "fct_product_funnels.sessions": 1, "fct_product_funnels.purchases": 0, "fct_product_funnels.revenue": 0},
        {"fct_product_funnels.date.day": "2026-02-15T00:00:00.000", "fct_product_funnels.sessions": 1, "fct_product_funnels.purchases": 0, "fct_product_funnels.revenue": 0},
        {"fct_product_funnels.date.day": "2026-02-16T00:00:00.000", "fct_product_funnels.sessions": 5, "fct_product_funnels.purchases": 0, "fct_product_funnels.revenue": 0},
        {"fct_product_funnels.date.day": "2026-02-18T00:00:00.000", "fct_product_funnels.sessions": 2, "fct_product_funnels.purchases": 0, "fct_product_funnels.revenue": 0},
        {"fct_product_funnels.date.day": "2026-02-20T00:00:00.000", "fct_product_funnels.sessions": 1, "fct_product_funnels.purchases": 0, "fct_product_funnels.revenue": 0},
        {"fct_product_funnels.date.day": "2026-02-21T00:00:00.000", "fct_product_funnels.sessions": 1, "fct_product_funnels.purchases": 0, "fct_product_funnels.revenue": 0},
        {"fct_product_funnels.date.day": "2026-02-22T00:00:00.000", "fct_product_funnels.sessions": 1, "fct_product_funnels.purchases": 0, "fct_product_funnels.revenue": 0},
        {"fct_product_funnels.date.day": "2026-02-23T00:00:00.000", "fct_product_funnels.sessions": 5, "fct_product_funnels.purchases": 0, "fct_product_funnels.revenue": 0},
        {"fct_product_funnels.date.day": "2026-02-24T00:00:00.000", "fct_product_funnels.sessions": 2, "fct_product_funnels.purchases": 0, "fct_product_funnels.revenue": 0},
        {"fct_product_funnels.date.day": "2026-02-25T00:00:00.000", "fct_product_funnels.sessions": 2, "fct_product_funnels.purchases": 0, "fct_product_funnels.revenue": 0},
        {"fct_product_funnels.date.day": "2026-02-26T00:00:00.000", "fct_product_funnels.sessions": 3, "fct_product_funnels.purchases": 0, "fct_product_funnels.revenue": 0},
        {"fct_product_funnels.date.day": "2026-02-27T00:00:00.000", "fct_product_funnels.sessions": 4, "fct_product_funnels.purchases": 0, "fct_product_funnels.revenue": 0},
        {"fct_product_funnels.date.day": "2026-02-28T00:00:00.000", "fct_product_funnels.sessions": 2, "fct_product_funnels.purchases": 0, "fct_product_funnels.revenue": 0},
        {"fct_product_funnels.date.day": "2026-03-01T00:00:00.000", "fct_product_funnels.sessions": 1, "fct_product_funnels.purchases": 0, "fct_product_funnels.revenue": 0},
        {"fct_product_funnels.date.day": "2026-03-02T00:00:00.000", "fct_product_funnels.sessions": 5, "fct_product_funnels.purchases": 0, "fct_product_funnels.revenue": 0},
        {"fct_product_funnels.date.day": "2026-03-03T00:00:00.000", "fct_product_funnels.sessions": 5, "fct_product_funnels.purchases": 0, "fct_product_funnels.revenue": 0},
        {"fct_product_funnels.date.day": "2026-03-04T00:00:00.000", "fct_product_funnels.sessions": 1, "fct_product_funnels.purchases": 0, "fct_product_funnels.revenue": 0},
        {"fct_product_funnels.date.day": "2026-03-06T00:00:00.000", "fct_product_funnels.sessions": 6, "fct_product_funnels.purchases": 0, "fct_product_funnels.revenue": 0},
        {"fct_product_funnels.date.day": "2026-03-08T00:00:00.000", "fct_product_funnels.sessions": 4, "fct_product_funnels.purchases": 0, "fct_product_funnels.revenue": 0},
        {"fct_product_funnels.date.day": "2026-03-09T00:00:00.000", "fct_product_funnels.sessions": 1, "fct_product_funnels.purchases": 0, "fct_product_funnels.revenue": 0},
        {"fct_product_funnels.date.day": "2026-03-10T00:00:00.000", "fct_product_funnels.sessions": 5, "fct_product_funnels.purchases": 0, "fct_product_funnels.revenue": 0},
        {"fct_product_funnels.date.day": "2026-03-11T00:00:00.000", "fct_product_funnels.sessions": 3, "fct_product_funnels.purchases": 0, "fct_product_funnels.revenue": 0},
        {"fct_product_funnels.date.day": "2026-03-12T00:00:00.000", "fct_product_funnels.sessions": 6, "fct_product_funnels.purchases": 0, "fct_product_funnels.revenue": 0},
        {"fct_product_funnels.date.day": "2026-03-13T00:00:00.000", "fct_product_funnels.sessions": 2, "fct_product_funnels.purchases": 0, "fct_product_funnels.revenue": 0},
        {"fct_product_funnels.date.day": "2026-03-14T00:00:00.000", "fct_product_funnels.sessions": 5, "fct_product_funnels.purchases": 0, "fct_product_funnels.revenue": 0},
        {"fct_product_funnels.date.day": "2026-03-15T00:00:00.000", "fct_product_funnels.sessions": 4, "fct_product_funnels.purchases": 0, "fct_product_funnels.revenue": 0},
        {"fct_product_funnels.date.day": "2026-03-16T00:00:00.000", "fct_product_funnels.sessions": 4, "fct_product_funnels.purchases": 0, "fct_product_funnels.revenue": 0},
        {"fct_product_funnels.date.day": "2026-03-17T00:00:00.000", "fct_product_funnels.sessions": 6, "fct_product_funnels.purchases": 1, "fct_product_funnels.revenue": 78},
    ],
}

# Brands with no API data returned — skip (keep existing)
SKIP_BRANDS = [
    "1e7aa370-3cde-40bf-90d9-8ce8a3aaed30",  # HAVN
    "f0a1a21b-3832-4bfd-ad3d-af38d11a90e8",   # Moment
    "35845b70-d5ef-4dbf-83cf-e9f327662c17",   # Medik8
    "508e7756-81aa-48b1-bbf5-765d2e8f1eb9",   # Westmore Beauty
]

print("=" * 60)
print("Updating performance data from FERMAT API daily metrics")
print(f"Reference date: {REF.strftime('%Y-%m-%d')} (yesterday)")
print("=" * 60)

for csv_id, rows in RAW_DATA.items():
    update_brand(csv_id, rows)

print()
for brand_id in SKIP_BRANDS:
    fpath = os.path.join(DATA, f"{brand_id}.json")
    if os.path.exists(fpath):
        with open(fpath) as f:
            data = json.load(f)
        print(f"  SKIPPED {data.get('brand_name', brand_id)}: no API data returned, keeping existing")
    else:
        print(f"  SKIPPED {brand_id}: file not found")

print()
print("Done! Run 'python3 build.py' to rebuild the dashboard.")
