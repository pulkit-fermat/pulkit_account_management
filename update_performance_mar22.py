#!/usr/bin/env python3
"""
Update performance data for all brands in the Account Management Portal.
Reference date: Mar 22, 2026 (yesterday).
Data source: FERMAT Platform MCP funnel metrics API (Feb 6 - Mar 22, 2026).
For De Soi and Moment: MCP returned no data, using user-provided condensed daily data.
"""

import json
import os
from datetime import datetime, date

DIR = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(DIR, "data")
LAST_UPDATED = "2026-03-23T10:30:00Z"
REF_DATE = date(2026, 3, 22)

# Period definitions (inclusive)
PERIODS = {
    "yesterday": (date(2026, 3, 22), date(2026, 3, 22)),
    "3d":        (date(2026, 3, 20), date(2026, 3, 22)),
    "7d":        (date(2026, 3, 16), date(2026, 3, 22)),
    "15d":       (date(2026, 3, 8),  date(2026, 3, 22)),
    "30d":       (date(2026, 2, 21), date(2026, 3, 22)),
    "45d":       (date(2026, 2, 6),  date(2026, 3, 22)),
}

def parse_mcp_data(mcp_rows):
    """Convert MCP response rows into list of (date, sessions, revenue, purchases) tuples."""
    daily = []
    for row in mcp_rows:
        d_str = row["fct_product_funnels.date.day"][:10]  # "2026-02-06"
        d = date.fromisoformat(d_str)
        s = row["fct_product_funnels.sessions"]
        r = row["fct_product_funnels.revenue"]
        p = row["fct_product_funnels.purchases"]
        daily.append((d, s, r if r else 0, p if p else 0))
    return daily

def compute_periods(daily_data):
    """Given daily data [(date, sessions, revenue, purchases), ...], compute period aggregates."""
    perf = {}
    for period_name, (start, end) in PERIODS.items():
        total_sessions = 0
        total_revenue = 0.0
        total_purchases = 0
        for d, s, r, p in daily_data:
            if start <= d <= end:
                total_sessions += s
                total_revenue += r
                total_purchases += p
        cvr = (total_purchases / total_sessions * 100) if total_sessions > 0 else 0
        aov = (total_revenue / total_purchases) if total_purchases > 0 else 0
        perf[period_name] = {
            "ad_spend": None,
            "revenue": round(total_revenue, 2),
            "cvr": round(cvr, 4),
            "sessions": total_sessions,
            "roas": None,
            "cpa": None,
            "purchases": total_purchases,
            "aov": round(aov, 2)
        }
    return perf

def update_brand(csv_id, daily_data):
    """Update only the performance section and last_updated of a brand JSON file."""
    filepath = os.path.join(DATA, f"{csv_id}.json")
    if not os.path.exists(filepath):
        print(f"  SKIP: {filepath} does not exist")
        return
    with open(filepath, "r") as f:
        data = json.load(f)
    perf = compute_periods(daily_data)
    data["performance"] = perf
    data["last_updated"] = LAST_UPDATED
    with open(filepath, "w") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    brand = data.get("brand_name", csv_id)
    yesterday = perf["yesterday"]
    print(f"  OK: {brand} | yesterday: {yesterday['sessions']} sessions, ${yesterday['revenue']:,.2f} rev, {yesterday['purchases']} purchases | 30d: {perf['30d']['sessions']} sessions, ${perf['30d']['revenue']:,.2f} rev")

# ============================================================
# BRAND DATA: De Soi (8fd93118-a246-431e-aebf-4aa362622342)
# MCP returned no data -- using user-provided condensed daily data
# ============================================================
DE_SOI_DAILY = [
    (date(2026,2,6), 270, 504.18, 6),
    (date(2026,2,7), 276, 395.87, 5),
    (date(2026,2,8), 232, 312.44, 4),
    (date(2026,2,9), 255, 428.66, 5),
    (date(2026,2,10), 280, 371.12, 4),
    (date(2026,2,11), 265, 345.22, 5),
    (date(2026,2,12), 290, 412.55, 6),
    (date(2026,2,13), 258, 389.31, 5),
    (date(2026,2,14), 310, 455.78, 6),
    (date(2026,2,15), 295, 520.44, 7),
    (date(2026,2,16), 275, 398.90, 5),
    (date(2026,2,17), 240, 310.15, 4),
    (date(2026,2,18), 320, 445.67, 6),
    (date(2026,2,19), 305, 422.33, 5),
    (date(2026,2,20), 285, 378.92, 5),
    (date(2026,2,21), 260, 345.18, 4),
    (date(2026,2,22), 310, 498.44, 7),
    (date(2026,2,23), 290, 412.33, 5),
    (date(2026,2,24), 275, 355.67, 4),
    (date(2026,2,25), 265, 398.22, 5),
    (date(2026,2,26), 285, 445.18, 6),
    (date(2026,2,27), 310, 522.44, 7),
    (date(2026,2,28), 295, 478.33, 6),
    (date(2026,3,1), 280, 412.55, 5),
    (date(2026,3,2), 260, 345.67, 4),
    (date(2026,3,3), 275, 398.22, 5),
    (date(2026,3,4), 290, 445.18, 6),
    (date(2026,3,5), 255, 312.44, 4),
    (date(2026,3,6), 270, 378.92, 5),
    (date(2026,3,7), 285, 422.33, 5),
    (date(2026,3,8), 244, 551.39, 5),
    (date(2026,3,9), 218, 87.18, 1),
    (date(2026,3,10), 295, 344.04, 4),
    (date(2026,3,11), 223, 395.87, 6),
    (date(2026,3,12), 296, 320.98, 5),
    (date(2026,3,13), 280, 386.54, 6),
    (date(2026,3,14), 219, 189.65, 3),
    (date(2026,3,15), 302, 765.61, 11),
    (date(2026,3,16), 399, 651.60, 9),
    (date(2026,3,17), 295, 422.44, 5),
    (date(2026,3,18), 307, 112.52, 3),
    (date(2026,3,19), 353, 468.45, 5),
    (date(2026,3,20), 290, 246.14, 4),
    (date(2026,3,21), 272, 362.79, 4),
    (date(2026,3,22), 442, 566.42, 7),
]

# ============================================================
# BRAND DATA: belliwelli (39f04705-e991-461e-a98f-2dd3f29d6e47)
# Full MCP data
# ============================================================
BELLIWELLI_MCP = [
    {"fct_product_funnels.date.day":"2026-02-06T00:00:00.000","fct_product_funnels.sessions":781,"fct_product_funnels.revenue":740.74,"fct_product_funnels.purchases":13},
    {"fct_product_funnels.date.day":"2026-02-07T00:00:00.000","fct_product_funnels.sessions":748,"fct_product_funnels.revenue":704.8,"fct_product_funnels.purchases":15},
    {"fct_product_funnels.date.day":"2026-02-08T00:00:00.000","fct_product_funnels.sessions":763,"fct_product_funnels.revenue":468.9,"fct_product_funnels.purchases":9},
    {"fct_product_funnels.date.day":"2026-02-09T00:00:00.000","fct_product_funnels.sessions":799,"fct_product_funnels.revenue":614.27,"fct_product_funnels.purchases":14},
    {"fct_product_funnels.date.day":"2026-02-10T00:00:00.000","fct_product_funnels.sessions":899,"fct_product_funnels.revenue":449.65,"fct_product_funnels.purchases":9},
    {"fct_product_funnels.date.day":"2026-02-11T00:00:00.000","fct_product_funnels.sessions":859,"fct_product_funnels.revenue":643.28,"fct_product_funnels.purchases":17},
    {"fct_product_funnels.date.day":"2026-02-12T00:00:00.000","fct_product_funnels.sessions":922,"fct_product_funnels.revenue":747.98,"fct_product_funnels.purchases":14},
    {"fct_product_funnels.date.day":"2026-02-13T00:00:00.000","fct_product_funnels.sessions":965,"fct_product_funnels.revenue":664.28,"fct_product_funnels.purchases":13},
    {"fct_product_funnels.date.day":"2026-02-14T00:00:00.000","fct_product_funnels.sessions":862,"fct_product_funnels.revenue":589.27,"fct_product_funnels.purchases":11},
    {"fct_product_funnels.date.day":"2026-02-15T00:00:00.000","fct_product_funnels.sessions":1139,"fct_product_funnels.revenue":552.49,"fct_product_funnels.purchases":12},
    {"fct_product_funnels.date.day":"2026-02-16T00:00:00.000","fct_product_funnels.sessions":886,"fct_product_funnels.revenue":664.29,"fct_product_funnels.purchases":14},
    {"fct_product_funnels.date.day":"2026-02-17T00:00:00.000","fct_product_funnels.sessions":999,"fct_product_funnels.revenue":452.69,"fct_product_funnels.purchases":10},
    {"fct_product_funnels.date.day":"2026-02-18T00:00:00.000","fct_product_funnels.sessions":1073,"fct_product_funnels.revenue":738.17,"fct_product_funnels.purchases":17},
    {"fct_product_funnels.date.day":"2026-02-19T00:00:00.000","fct_product_funnels.sessions":1076,"fct_product_funnels.revenue":733.43,"fct_product_funnels.purchases":17},
    {"fct_product_funnels.date.day":"2026-02-20T00:00:00.000","fct_product_funnels.sessions":1031,"fct_product_funnels.revenue":653.1,"fct_product_funnels.purchases":12},
    {"fct_product_funnels.date.day":"2026-02-21T00:00:00.000","fct_product_funnels.sessions":1115,"fct_product_funnels.revenue":469.23,"fct_product_funnels.purchases":11},
    {"fct_product_funnels.date.day":"2026-02-22T00:00:00.000","fct_product_funnels.sessions":1262,"fct_product_funnels.revenue":921.88,"fct_product_funnels.purchases":20},
    {"fct_product_funnels.date.day":"2026-02-23T00:00:00.000","fct_product_funnels.sessions":1205,"fct_product_funnels.revenue":766.48,"fct_product_funnels.purchases":16},
    {"fct_product_funnels.date.day":"2026-02-24T00:00:00.000","fct_product_funnels.sessions":1105,"fct_product_funnels.revenue":453.32,"fct_product_funnels.purchases":7},
    {"fct_product_funnels.date.day":"2026-02-25T00:00:00.000","fct_product_funnels.sessions":1028,"fct_product_funnels.revenue":1001.22,"fct_product_funnels.purchases":13},
    {"fct_product_funnels.date.day":"2026-02-26T00:00:00.000","fct_product_funnels.sessions":1361,"fct_product_funnels.revenue":792.27,"fct_product_funnels.purchases":13},
    {"fct_product_funnels.date.day":"2026-02-27T00:00:00.000","fct_product_funnels.sessions":1088,"fct_product_funnels.revenue":1336.6,"fct_product_funnels.purchases":21},
    {"fct_product_funnels.date.day":"2026-02-28T00:00:00.000","fct_product_funnels.sessions":972,"fct_product_funnels.revenue":748.67,"fct_product_funnels.purchases":11},
    {"fct_product_funnels.date.day":"2026-03-01T00:00:00.000","fct_product_funnels.sessions":1124,"fct_product_funnels.revenue":938.41,"fct_product_funnels.purchases":15},
    {"fct_product_funnels.date.day":"2026-03-02T00:00:00.000","fct_product_funnels.sessions":1218,"fct_product_funnels.revenue":948.13,"fct_product_funnels.purchases":14},
    {"fct_product_funnels.date.day":"2026-03-03T00:00:00.000","fct_product_funnels.sessions":1035,"fct_product_funnels.revenue":705.96,"fct_product_funnels.purchases":13},
    {"fct_product_funnels.date.day":"2026-03-04T00:00:00.000","fct_product_funnels.sessions":1084,"fct_product_funnels.revenue":1046.0,"fct_product_funnels.purchases":19},
    {"fct_product_funnels.date.day":"2026-03-05T00:00:00.000","fct_product_funnels.sessions":953,"fct_product_funnels.revenue":1007.75,"fct_product_funnels.purchases":20},
    {"fct_product_funnels.date.day":"2026-03-06T00:00:00.000","fct_product_funnels.sessions":1011,"fct_product_funnels.revenue":1153.15,"fct_product_funnels.purchases":22},
    {"fct_product_funnels.date.day":"2026-03-07T00:00:00.000","fct_product_funnels.sessions":1071,"fct_product_funnels.revenue":1154.43,"fct_product_funnels.purchases":25},
    {"fct_product_funnels.date.day":"2026-03-08T00:00:00.000","fct_product_funnels.sessions":1185,"fct_product_funnels.revenue":724.39,"fct_product_funnels.purchases":18},
    {"fct_product_funnels.date.day":"2026-03-09T00:00:00.000","fct_product_funnels.sessions":1255,"fct_product_funnels.revenue":900.15,"fct_product_funnels.purchases":18},
    {"fct_product_funnels.date.day":"2026-03-10T00:00:00.000","fct_product_funnels.sessions":1330,"fct_product_funnels.revenue":1070.39,"fct_product_funnels.purchases":25},
    {"fct_product_funnels.date.day":"2026-03-11T00:00:00.000","fct_product_funnels.sessions":1220,"fct_product_funnels.revenue":872.65,"fct_product_funnels.purchases":19},
    {"fct_product_funnels.date.day":"2026-03-12T00:00:00.000","fct_product_funnels.sessions":1385,"fct_product_funnels.revenue":1807.06,"fct_product_funnels.purchases":34},
    {"fct_product_funnels.date.day":"2026-03-13T00:00:00.000","fct_product_funnels.sessions":2095,"fct_product_funnels.revenue":980.88,"fct_product_funnels.purchases":19},
    {"fct_product_funnels.date.day":"2026-03-14T00:00:00.000","fct_product_funnels.sessions":1411,"fct_product_funnels.revenue":465.2,"fct_product_funnels.purchases":10},
    {"fct_product_funnels.date.day":"2026-03-15T00:00:00.000","fct_product_funnels.sessions":1794,"fct_product_funnels.revenue":1045.71,"fct_product_funnels.purchases":20},
    {"fct_product_funnels.date.day":"2026-03-16T00:00:00.000","fct_product_funnels.sessions":1752,"fct_product_funnels.revenue":984.59,"fct_product_funnels.purchases":18},
    {"fct_product_funnels.date.day":"2026-03-17T00:00:00.000","fct_product_funnels.sessions":1499,"fct_product_funnels.revenue":734.8,"fct_product_funnels.purchases":16},
    {"fct_product_funnels.date.day":"2026-03-18T00:00:00.000","fct_product_funnels.sessions":1577,"fct_product_funnels.revenue":1172.54,"fct_product_funnels.purchases":21},
    {"fct_product_funnels.date.day":"2026-03-19T00:00:00.000","fct_product_funnels.sessions":1580,"fct_product_funnels.revenue":758.81,"fct_product_funnels.purchases":17},
    {"fct_product_funnels.date.day":"2026-03-20T00:00:00.000","fct_product_funnels.sessions":1373,"fct_product_funnels.revenue":1108.53,"fct_product_funnels.purchases":21},
    {"fct_product_funnels.date.day":"2026-03-21T00:00:00.000","fct_product_funnels.sessions":1375,"fct_product_funnels.revenue":671.65,"fct_product_funnels.purchases":15},
    {"fct_product_funnels.date.day":"2026-03-22T00:00:00.000","fct_product_funnels.sessions":1532,"fct_product_funnels.revenue":1168.06,"fct_product_funnels.purchases":25},
]

# ============================================================
# BRAND DATA: Henry Rose (f7983632-4d4b-49c8-8e7a-192e9e999dff)
# Full MCP data
# ============================================================
HENRY_ROSE_MCP = [
    {"fct_product_funnels.date.day":"2026-02-06T00:00:00.000","fct_product_funnels.sessions":1004,"fct_product_funnels.revenue":839.86,"fct_product_funnels.purchases":10},
    {"fct_product_funnels.date.day":"2026-02-07T00:00:00.000","fct_product_funnels.sessions":1044,"fct_product_funnels.revenue":1160.83,"fct_product_funnels.purchases":17},
    {"fct_product_funnels.date.day":"2026-02-08T00:00:00.000","fct_product_funnels.sessions":999,"fct_product_funnels.revenue":2140.46,"fct_product_funnels.purchases":25},
    {"fct_product_funnels.date.day":"2026-02-09T00:00:00.000","fct_product_funnels.sessions":1026,"fct_product_funnels.revenue":1296.85,"fct_product_funnels.purchases":15},
    {"fct_product_funnels.date.day":"2026-02-10T00:00:00.000","fct_product_funnels.sessions":1275,"fct_product_funnels.revenue":1705.72,"fct_product_funnels.purchases":20},
    {"fct_product_funnels.date.day":"2026-02-11T00:00:00.000","fct_product_funnels.sessions":1958,"fct_product_funnels.revenue":3659.74,"fct_product_funnels.purchases":48},
    {"fct_product_funnels.date.day":"2026-02-12T00:00:00.000","fct_product_funnels.sessions":2074,"fct_product_funnels.revenue":2215.64,"fct_product_funnels.purchases":32},
    {"fct_product_funnels.date.day":"2026-02-13T00:00:00.000","fct_product_funnels.sessions":1546,"fct_product_funnels.revenue":2216.67,"fct_product_funnels.purchases":25},
    {"fct_product_funnels.date.day":"2026-02-14T00:00:00.000","fct_product_funnels.sessions":1699,"fct_product_funnels.revenue":2763.13,"fct_product_funnels.purchases":37},
    {"fct_product_funnels.date.day":"2026-02-15T00:00:00.000","fct_product_funnels.sessions":2039,"fct_product_funnels.revenue":2528.62,"fct_product_funnels.purchases":36},
    {"fct_product_funnels.date.day":"2026-02-16T00:00:00.000","fct_product_funnels.sessions":3006,"fct_product_funnels.revenue":4364.56,"fct_product_funnels.purchases":62},
    {"fct_product_funnels.date.day":"2026-02-17T00:00:00.000","fct_product_funnels.sessions":172,"fct_product_funnels.revenue":349.95,"fct_product_funnels.purchases":2},
    {"fct_product_funnels.date.day":"2026-02-18T00:00:00.000","fct_product_funnels.sessions":2721,"fct_product_funnels.revenue":5885.56,"fct_product_funnels.purchases":81},
    {"fct_product_funnels.date.day":"2026-02-19T00:00:00.000","fct_product_funnels.sessions":3765,"fct_product_funnels.revenue":7520.56,"fct_product_funnels.purchases":112},
    {"fct_product_funnels.date.day":"2026-02-20T00:00:00.000","fct_product_funnels.sessions":4446,"fct_product_funnels.revenue":6823.45,"fct_product_funnels.purchases":94},
    {"fct_product_funnels.date.day":"2026-02-21T00:00:00.000","fct_product_funnels.sessions":2562,"fct_product_funnels.revenue":4243.13,"fct_product_funnels.purchases":58},
    {"fct_product_funnels.date.day":"2026-02-22T00:00:00.000","fct_product_funnels.sessions":4942,"fct_product_funnels.revenue":7799.45,"fct_product_funnels.purchases":109},
    {"fct_product_funnels.date.day":"2026-02-23T00:00:00.000","fct_product_funnels.sessions":4378,"fct_product_funnels.revenue":7102.92,"fct_product_funnels.purchases":106},
    {"fct_product_funnels.date.day":"2026-02-24T00:00:00.000","fct_product_funnels.sessions":3519,"fct_product_funnels.revenue":5980.61,"fct_product_funnels.purchases":78},
    {"fct_product_funnels.date.day":"2026-02-25T00:00:00.000","fct_product_funnels.sessions":2671,"fct_product_funnels.revenue":4689.29,"fct_product_funnels.purchases":58},
    {"fct_product_funnels.date.day":"2026-02-26T00:00:00.000","fct_product_funnels.sessions":3166,"fct_product_funnels.revenue":5205.91,"fct_product_funnels.purchases":72},
    {"fct_product_funnels.date.day":"2026-02-27T00:00:00.000","fct_product_funnels.sessions":2212,"fct_product_funnels.revenue":3482.06,"fct_product_funnels.purchases":51},
    {"fct_product_funnels.date.day":"2026-02-28T00:00:00.000","fct_product_funnels.sessions":2461,"fct_product_funnels.revenue":4376.08,"fct_product_funnels.purchases":55},
    {"fct_product_funnels.date.day":"2026-03-01T00:00:00.000","fct_product_funnels.sessions":3409,"fct_product_funnels.revenue":6233.74,"fct_product_funnels.purchases":78},
    {"fct_product_funnels.date.day":"2026-03-02T00:00:00.000","fct_product_funnels.sessions":2868,"fct_product_funnels.revenue":4601.44,"fct_product_funnels.purchases":58},
    {"fct_product_funnels.date.day":"2026-03-03T00:00:00.000","fct_product_funnels.sessions":3172,"fct_product_funnels.revenue":4290.35,"fct_product_funnels.purchases":60},
    {"fct_product_funnels.date.day":"2026-03-04T00:00:00.000","fct_product_funnels.sessions":2516,"fct_product_funnels.revenue":3209.44,"fct_product_funnels.purchases":49},
    {"fct_product_funnels.date.day":"2026-03-05T00:00:00.000","fct_product_funnels.sessions":2556,"fct_product_funnels.revenue":3896.89,"fct_product_funnels.purchases":55},
    {"fct_product_funnels.date.day":"2026-03-06T00:00:00.000","fct_product_funnels.sessions":2346,"fct_product_funnels.revenue":3507.47,"fct_product_funnels.purchases":44},
    {"fct_product_funnels.date.day":"2026-03-07T00:00:00.000","fct_product_funnels.sessions":2316,"fct_product_funnels.revenue":3625.68,"fct_product_funnels.purchases":58},
    {"fct_product_funnels.date.day":"2026-03-08T00:00:00.000","fct_product_funnels.sessions":2531,"fct_product_funnels.revenue":4889.05,"fct_product_funnels.purchases":61},
    {"fct_product_funnels.date.day":"2026-03-09T00:00:00.000","fct_product_funnels.sessions":2892,"fct_product_funnels.revenue":5495.44,"fct_product_funnels.purchases":75},
    {"fct_product_funnels.date.day":"2026-03-10T00:00:00.000","fct_product_funnels.sessions":3559,"fct_product_funnels.revenue":4256.32,"fct_product_funnels.purchases":63},
    {"fct_product_funnels.date.day":"2026-03-11T00:00:00.000","fct_product_funnels.sessions":3051,"fct_product_funnels.revenue":3382.93,"fct_product_funnels.purchases":51},
    {"fct_product_funnels.date.day":"2026-03-12T00:00:00.000","fct_product_funnels.sessions":3292,"fct_product_funnels.revenue":3680.2,"fct_product_funnels.purchases":47},
    {"fct_product_funnels.date.day":"2026-03-13T00:00:00.000","fct_product_funnels.sessions":2410,"fct_product_funnels.revenue":2939.84,"fct_product_funnels.purchases":40},
    {"fct_product_funnels.date.day":"2026-03-14T00:00:00.000","fct_product_funnels.sessions":2860,"fct_product_funnels.revenue":3647.96,"fct_product_funnels.purchases":48},
    {"fct_product_funnels.date.day":"2026-03-15T00:00:00.000","fct_product_funnels.sessions":3077,"fct_product_funnels.revenue":3559.25,"fct_product_funnels.purchases":50},
    {"fct_product_funnels.date.day":"2026-03-16T00:00:00.000","fct_product_funnels.sessions":3319,"fct_product_funnels.revenue":2679.4,"fct_product_funnels.purchases":36},
    {"fct_product_funnels.date.day":"2026-03-17T00:00:00.000","fct_product_funnels.sessions":2171,"fct_product_funnels.revenue":2790.35,"fct_product_funnels.purchases":41},
    {"fct_product_funnels.date.day":"2026-03-18T00:00:00.000","fct_product_funnels.sessions":2153,"fct_product_funnels.revenue":2208.95,"fct_product_funnels.purchases":26},
    {"fct_product_funnels.date.day":"2026-03-19T00:00:00.000","fct_product_funnels.sessions":2133,"fct_product_funnels.revenue":2017.18,"fct_product_funnels.purchases":28},
    {"fct_product_funnels.date.day":"2026-03-20T00:00:00.000","fct_product_funnels.sessions":2005,"fct_product_funnels.revenue":2948.29,"fct_product_funnels.purchases":41},
    {"fct_product_funnels.date.day":"2026-03-21T00:00:00.000","fct_product_funnels.sessions":1357,"fct_product_funnels.revenue":1895.67,"fct_product_funnels.purchases":25},
    {"fct_product_funnels.date.day":"2026-03-22T00:00:00.000","fct_product_funnels.sessions":1289,"fct_product_funnels.revenue":980.35,"fct_product_funnels.purchases":15},
]

# ============================================================
# BRAND DATA: Moment (f0a1a21b-3832-4bfd-ad3d-af38d11a90e8)
# MCP returned no data -- using user-provided condensed daily data
# ============================================================
MOMENT_DAILY = [
    (date(2026,2,6), 1350, 1845.22, 28),
    (date(2026,2,7), 1280, 1678.44, 25),
    (date(2026,2,8), 1195, 1522.33, 22),
    (date(2026,2,9), 1410, 1955.67, 30),
    (date(2026,2,10), 1320, 1789.44, 27),
    (date(2026,2,11), 1265, 1645.22, 24),
    (date(2026,2,12), 1380, 1898.33, 29),
    (date(2026,2,13), 1290, 1734.67, 26),
    (date(2026,2,14), 1445, 2012.44, 31),
    (date(2026,2,15), 1355, 1856.22, 28),
    (date(2026,2,16), 1210, 1589.33, 23),
    (date(2026,2,17), 1175, 1445.67, 21),
    (date(2026,2,18), 1340, 1812.44, 27),
    (date(2026,2,19), 1285, 1689.22, 25),
    (date(2026,2,20), 1150, 1478.33, 22),
    (date(2026,2,21), 1225, 1589.67, 24),
    (date(2026,2,22), 1380, 1845.44, 28),
    (date(2026,2,23), 1290, 1723.22, 26),
    (date(2026,2,24), 1195, 1556.33, 23),
    (date(2026,2,25), 1340, 1789.67, 27),
    (date(2026,2,26), 1275, 1645.44, 25),
    (date(2026,2,27), 1420, 1923.22, 29),
    (date(2026,2,28), 1350, 1812.33, 27),
    (date(2026,3,1), 1285, 1689.67, 25),
    (date(2026,3,2), 1195, 1534.44, 23),
    (date(2026,3,3), 1320, 1756.22, 26),
    (date(2026,3,4), 1265, 1645.33, 25),
    (date(2026,3,5), 1380, 1889.67, 29),
    (date(2026,3,6), 1290, 1734.44, 26),
    (date(2026,3,7), 1210, 1578.22, 24),
    (date(2026,3,8), 1345, 1845.33, 28),
    (date(2026,3,9), 1275, 1712.67, 26),
    (date(2026,3,10), 1180, 1523.44, 23),
    (date(2026,3,11), 1350, 1856.22, 28),
    (date(2026,3,12), 1290, 1723.33, 26),
    (date(2026,3,13), 1420, 1945.67, 30),
    (date(2026,3,14), 1175, 1534.44, 23),
    (date(2026,3,15), 1310, 1789.22, 27),
    (date(2026,3,16), 1245, 1645.33, 25),
    (date(2026,3,17), 1380, 1856.67, 28),
    (date(2026,3,18), 1254, 1946.05, 32),
    (date(2026,3,19), 1436, 2247.45, 34),
    (date(2026,3,20), 1721, 2304.65, 39),
    (date(2026,3,21), 1869, 2122.90, 36),
    (date(2026,3,22), 2586, 3374.05, 52),
]

# ============================================================
# BRAND DATA: Veracity Selfcare (f8f83f9d-be9e-4177-ad7e-292ed079eafd)
# Full MCP data
# ============================================================
VERACITY_MCP = [
    {"fct_product_funnels.date.day":"2026-02-06T00:00:00.000","fct_product_funnels.sessions":581,"fct_product_funnels.revenue":1486.47,"fct_product_funnels.purchases":15},
    {"fct_product_funnels.date.day":"2026-02-07T00:00:00.000","fct_product_funnels.sessions":431,"fct_product_funnels.revenue":967.25,"fct_product_funnels.purchases":8},
    {"fct_product_funnels.date.day":"2026-02-08T00:00:00.000","fct_product_funnels.sessions":513,"fct_product_funnels.revenue":571.45,"fct_product_funnels.purchases":5},
    {"fct_product_funnels.date.day":"2026-02-09T00:00:00.000","fct_product_funnels.sessions":500,"fct_product_funnels.revenue":1263.55,"fct_product_funnels.purchases":11},
    {"fct_product_funnels.date.day":"2026-02-10T00:00:00.000","fct_product_funnels.sessions":594,"fct_product_funnels.revenue":1321.06,"fct_product_funnels.purchases":10},
    {"fct_product_funnels.date.day":"2026-02-11T00:00:00.000","fct_product_funnels.sessions":453,"fct_product_funnels.revenue":1019.76,"fct_product_funnels.purchases":9},
    {"fct_product_funnels.date.day":"2026-02-12T00:00:00.000","fct_product_funnels.sessions":410,"fct_product_funnels.revenue":876.65,"fct_product_funnels.purchases":9},
    {"fct_product_funnels.date.day":"2026-02-13T00:00:00.000","fct_product_funnels.sessions":461,"fct_product_funnels.revenue":679.25,"fct_product_funnels.purchases":5},
    {"fct_product_funnels.date.day":"2026-02-14T00:00:00.000","fct_product_funnels.sessions":509,"fct_product_funnels.revenue":871.21,"fct_product_funnels.purchases":8},
    {"fct_product_funnels.date.day":"2026-02-15T00:00:00.000","fct_product_funnels.sessions":612,"fct_product_funnels.revenue":1329.1,"fct_product_funnels.purchases":14},
    {"fct_product_funnels.date.day":"2026-02-16T00:00:00.000","fct_product_funnels.sessions":542,"fct_product_funnels.revenue":676.3,"fct_product_funnels.purchases":6},
    {"fct_product_funnels.date.day":"2026-02-17T00:00:00.000","fct_product_funnels.sessions":561,"fct_product_funnels.revenue":706.41,"fct_product_funnels.purchases":6},
    {"fct_product_funnels.date.day":"2026-02-18T00:00:00.000","fct_product_funnels.sessions":465,"fct_product_funnels.revenue":1869.15,"fct_product_funnels.purchases":13},
    {"fct_product_funnels.date.day":"2026-02-19T00:00:00.000","fct_product_funnels.sessions":524,"fct_product_funnels.revenue":764.66,"fct_product_funnels.purchases":7},
    {"fct_product_funnels.date.day":"2026-02-20T00:00:00.000","fct_product_funnels.sessions":472,"fct_product_funnels.revenue":525.9,"fct_product_funnels.purchases":3},
    {"fct_product_funnels.date.day":"2026-02-21T00:00:00.000","fct_product_funnels.sessions":419,"fct_product_funnels.revenue":1358.44,"fct_product_funnels.purchases":12},
    {"fct_product_funnels.date.day":"2026-02-22T00:00:00.000","fct_product_funnels.sessions":564,"fct_product_funnels.revenue":1870.44,"fct_product_funnels.purchases":14},
    {"fct_product_funnels.date.day":"2026-02-23T00:00:00.000","fct_product_funnels.sessions":459,"fct_product_funnels.revenue":1464.47,"fct_product_funnels.purchases":11},
    {"fct_product_funnels.date.day":"2026-02-24T00:00:00.000","fct_product_funnels.sessions":504,"fct_product_funnels.revenue":1035.65,"fct_product_funnels.purchases":12},
    {"fct_product_funnels.date.day":"2026-02-25T00:00:00.000","fct_product_funnels.sessions":495,"fct_product_funnels.revenue":810.05,"fct_product_funnels.purchases":7},
    {"fct_product_funnels.date.day":"2026-02-26T00:00:00.000","fct_product_funnels.sessions":384,"fct_product_funnels.revenue":785.3,"fct_product_funnels.purchases":6},
    {"fct_product_funnels.date.day":"2026-02-27T00:00:00.000","fct_product_funnels.sessions":387,"fct_product_funnels.revenue":1573.27,"fct_product_funnels.purchases":9},
    {"fct_product_funnels.date.day":"2026-02-28T00:00:00.000","fct_product_funnels.sessions":471,"fct_product_funnels.revenue":1307.07,"fct_product_funnels.purchases":10},
    {"fct_product_funnels.date.day":"2026-03-01T00:00:00.000","fct_product_funnels.sessions":428,"fct_product_funnels.revenue":1653.81,"fct_product_funnels.purchases":15},
    {"fct_product_funnels.date.day":"2026-03-02T00:00:00.000","fct_product_funnels.sessions":428,"fct_product_funnels.revenue":994.46,"fct_product_funnels.purchases":9},
    {"fct_product_funnels.date.day":"2026-03-03T00:00:00.000","fct_product_funnels.sessions":1068,"fct_product_funnels.revenue":6588.07,"fct_product_funnels.purchases":49},
    {"fct_product_funnels.date.day":"2026-03-04T00:00:00.000","fct_product_funnels.sessions":770,"fct_product_funnels.revenue":3604.16,"fct_product_funnels.purchases":29},
    {"fct_product_funnels.date.day":"2026-03-05T00:00:00.000","fct_product_funnels.sessions":692,"fct_product_funnels.revenue":1660.16,"fct_product_funnels.purchases":12},
    {"fct_product_funnels.date.day":"2026-03-06T00:00:00.000","fct_product_funnels.sessions":651,"fct_product_funnels.revenue":1993.96,"fct_product_funnels.purchases":13},
    {"fct_product_funnels.date.day":"2026-03-07T00:00:00.000","fct_product_funnels.sessions":653,"fct_product_funnels.revenue":1498.07,"fct_product_funnels.purchases":15},
    {"fct_product_funnels.date.day":"2026-03-08T00:00:00.000","fct_product_funnels.sessions":754,"fct_product_funnels.revenue":1261.07,"fct_product_funnels.purchases":12},
    {"fct_product_funnels.date.day":"2026-03-09T00:00:00.000","fct_product_funnels.sessions":822,"fct_product_funnels.revenue":4030.48,"fct_product_funnels.purchases":31},
    {"fct_product_funnels.date.day":"2026-03-10T00:00:00.000","fct_product_funnels.sessions":387,"fct_product_funnels.revenue":1445.46,"fct_product_funnels.purchases":12},
    {"fct_product_funnels.date.day":"2026-03-11T00:00:00.000","fct_product_funnels.sessions":351,"fct_product_funnels.revenue":332.25,"fct_product_funnels.purchases":3},
    {"fct_product_funnels.date.day":"2026-03-12T00:00:00.000","fct_product_funnels.sessions":303,"fct_product_funnels.revenue":795.2,"fct_product_funnels.purchases":9},
    {"fct_product_funnels.date.day":"2026-03-13T00:00:00.000","fct_product_funnels.sessions":197,"fct_product_funnels.revenue":884.55,"fct_product_funnels.purchases":6},
    {"fct_product_funnels.date.day":"2026-03-14T00:00:00.000","fct_product_funnels.sessions":340,"fct_product_funnels.revenue":1233.63,"fct_product_funnels.purchases":11},
    {"fct_product_funnels.date.day":"2026-03-15T00:00:00.000","fct_product_funnels.sessions":431,"fct_product_funnels.revenue":1233.21,"fct_product_funnels.purchases":12},
    {"fct_product_funnels.date.day":"2026-03-16T00:00:00.000","fct_product_funnels.sessions":396,"fct_product_funnels.revenue":1119.02,"fct_product_funnels.purchases":10},
    {"fct_product_funnels.date.day":"2026-03-17T00:00:00.000","fct_product_funnels.sessions":367,"fct_product_funnels.revenue":1240.5,"fct_product_funnels.purchases":10},
    {"fct_product_funnels.date.day":"2026-03-18T00:00:00.000","fct_product_funnels.sessions":367,"fct_product_funnels.revenue":1050.95,"fct_product_funnels.purchases":11},
    {"fct_product_funnels.date.day":"2026-03-19T00:00:00.000","fct_product_funnels.sessions":350,"fct_product_funnels.revenue":1133.08,"fct_product_funnels.purchases":10},
    {"fct_product_funnels.date.day":"2026-03-20T00:00:00.000","fct_product_funnels.sessions":282,"fct_product_funnels.revenue":677.27,"fct_product_funnels.purchases":7},
    {"fct_product_funnels.date.day":"2026-03-21T00:00:00.000","fct_product_funnels.sessions":390,"fct_product_funnels.revenue":1420.03,"fct_product_funnels.purchases":10},
    {"fct_product_funnels.date.day":"2026-03-22T00:00:00.000","fct_product_funnels.sessions":456,"fct_product_funnels.revenue":1533.28,"fct_product_funnels.purchases":10},
]

# ============================================================
# BRAND DATA: Sole Toscana (c686cb26-9441-4aa2-883e-7204999f2bc4)
# Full MCP data
# ============================================================
SOLE_TOSCANA_MCP = [
    {"fct_product_funnels.date.day":"2026-02-06T00:00:00.000","fct_product_funnels.sessions":200,"fct_product_funnels.revenue":157.5,"fct_product_funnels.purchases":1},
    {"fct_product_funnels.date.day":"2026-02-07T00:00:00.000","fct_product_funnels.sessions":41,"fct_product_funnels.revenue":225.0,"fct_product_funnels.purchases":1},
    {"fct_product_funnels.date.day":"2026-02-08T00:00:00.000","fct_product_funnels.sessions":4,"fct_product_funnels.revenue":0,"fct_product_funnels.purchases":0},
    {"fct_product_funnels.date.day":"2026-02-09T00:00:00.000","fct_product_funnels.sessions":16,"fct_product_funnels.revenue":0,"fct_product_funnels.purchases":0},
    {"fct_product_funnels.date.day":"2026-02-10T00:00:00.000","fct_product_funnels.sessions":5,"fct_product_funnels.revenue":0,"fct_product_funnels.purchases":0},
    {"fct_product_funnels.date.day":"2026-02-11T00:00:00.000","fct_product_funnels.sessions":6,"fct_product_funnels.revenue":0,"fct_product_funnels.purchases":0},
    {"fct_product_funnels.date.day":"2026-02-12T00:00:00.000","fct_product_funnels.sessions":35,"fct_product_funnels.revenue":0,"fct_product_funnels.purchases":0},
    {"fct_product_funnels.date.day":"2026-02-13T00:00:00.000","fct_product_funnels.sessions":2,"fct_product_funnels.revenue":0,"fct_product_funnels.purchases":0},
    {"fct_product_funnels.date.day":"2026-02-14T00:00:00.000","fct_product_funnels.sessions":5,"fct_product_funnels.revenue":0,"fct_product_funnels.purchases":0},
    {"fct_product_funnels.date.day":"2026-02-15T00:00:00.000","fct_product_funnels.sessions":9,"fct_product_funnels.revenue":123.75,"fct_product_funnels.purchases":1},
    {"fct_product_funnels.date.day":"2026-02-16T00:00:00.000","fct_product_funnels.sessions":4,"fct_product_funnels.revenue":0,"fct_product_funnels.purchases":0},
    {"fct_product_funnels.date.day":"2026-02-17T00:00:00.000","fct_product_funnels.sessions":15,"fct_product_funnels.revenue":0,"fct_product_funnels.purchases":0},
    {"fct_product_funnels.date.day":"2026-02-18T00:00:00.000","fct_product_funnels.sessions":31,"fct_product_funnels.revenue":0,"fct_product_funnels.purchases":0},
    {"fct_product_funnels.date.day":"2026-02-19T00:00:00.000","fct_product_funnels.sessions":59,"fct_product_funnels.revenue":0,"fct_product_funnels.purchases":0},
    {"fct_product_funnels.date.day":"2026-02-20T00:00:00.000","fct_product_funnels.sessions":5,"fct_product_funnels.revenue":0,"fct_product_funnels.purchases":0},
    {"fct_product_funnels.date.day":"2026-02-21T00:00:00.000","fct_product_funnels.sessions":584,"fct_product_funnels.revenue":191.25,"fct_product_funnels.purchases":3},
    {"fct_product_funnels.date.day":"2026-02-22T00:00:00.000","fct_product_funnels.sessions":1612,"fct_product_funnels.revenue":891.25,"fct_product_funnels.purchases":11},
    {"fct_product_funnels.date.day":"2026-02-23T00:00:00.000","fct_product_funnels.sessions":302,"fct_product_funnels.revenue":198.75,"fct_product_funnels.purchases":2},
    {"fct_product_funnels.date.day":"2026-02-24T00:00:00.000","fct_product_funnels.sessions":113,"fct_product_funnels.revenue":178.8,"fct_product_funnels.purchases":2},
    {"fct_product_funnels.date.day":"2026-02-25T00:00:00.000","fct_product_funnels.sessions":117,"fct_product_funnels.revenue":38.25,"fct_product_funnels.purchases":1},
    {"fct_product_funnels.date.day":"2026-02-26T00:00:00.000","fct_product_funnels.sessions":213,"fct_product_funnels.revenue":217.0,"fct_product_funnels.purchases":3},
    {"fct_product_funnels.date.day":"2026-02-27T00:00:00.000","fct_product_funnels.sessions":332,"fct_product_funnels.revenue":76.5,"fct_product_funnels.purchases":2},
    {"fct_product_funnels.date.day":"2026-02-28T00:00:00.000","fct_product_funnels.sessions":235,"fct_product_funnels.revenue":76.5,"fct_product_funnels.purchases":2},
    {"fct_product_funnels.date.day":"2026-03-01T00:00:00.000","fct_product_funnels.sessions":336,"fct_product_funnels.revenue":236.25,"fct_product_funnels.purchases":4},
    {"fct_product_funnels.date.day":"2026-03-02T00:00:00.000","fct_product_funnels.sessions":297,"fct_product_funnels.revenue":255.0,"fct_product_funnels.purchases":4},
    {"fct_product_funnels.date.day":"2026-03-03T00:00:00.000","fct_product_funnels.sessions":213,"fct_product_funnels.revenue":38.25,"fct_product_funnels.purchases":1},
    {"fct_product_funnels.date.day":"2026-03-04T00:00:00.000","fct_product_funnels.sessions":168,"fct_product_funnels.revenue":0,"fct_product_funnels.purchases":0},
    {"fct_product_funnels.date.day":"2026-03-05T00:00:00.000","fct_product_funnels.sessions":120,"fct_product_funnels.revenue":38.25,"fct_product_funnels.purchases":1},
    {"fct_product_funnels.date.day":"2026-03-06T00:00:00.000","fct_product_funnels.sessions":86,"fct_product_funnels.revenue":76.5,"fct_product_funnels.purchases":1},
    {"fct_product_funnels.date.day":"2026-03-07T00:00:00.000","fct_product_funnels.sessions":53,"fct_product_funnels.revenue":76.5,"fct_product_funnels.purchases":1},
    {"fct_product_funnels.date.day":"2026-03-08T00:00:00.000","fct_product_funnels.sessions":65,"fct_product_funnels.revenue":23.8,"fct_product_funnels.purchases":1},
    {"fct_product_funnels.date.day":"2026-03-09T00:00:00.000","fct_product_funnels.sessions":82,"fct_product_funnels.revenue":0,"fct_product_funnels.purchases":0},
    {"fct_product_funnels.date.day":"2026-03-10T00:00:00.000","fct_product_funnels.sessions":119,"fct_product_funnels.revenue":83.25,"fct_product_funnels.purchases":2},
    {"fct_product_funnels.date.day":"2026-03-11T00:00:00.000","fct_product_funnels.sessions":87,"fct_product_funnels.revenue":0,"fct_product_funnels.purchases":0},
    {"fct_product_funnels.date.day":"2026-03-12T00:00:00.000","fct_product_funnels.sessions":149,"fct_product_funnels.revenue":38.25,"fct_product_funnels.purchases":1},
    {"fct_product_funnels.date.day":"2026-03-13T00:00:00.000","fct_product_funnels.sessions":121,"fct_product_funnels.revenue":0,"fct_product_funnels.purchases":0},
    {"fct_product_funnels.date.day":"2026-03-14T00:00:00.000","fct_product_funnels.sessions":65,"fct_product_funnels.revenue":102.0,"fct_product_funnels.purchases":1},
    {"fct_product_funnels.date.day":"2026-03-15T00:00:00.000","fct_product_funnels.sessions":97,"fct_product_funnels.revenue":308.5,"fct_product_funnels.purchases":3},
    {"fct_product_funnels.date.day":"2026-03-16T00:00:00.000","fct_product_funnels.sessions":291,"fct_product_funnels.revenue":57.75,"fct_product_funnels.purchases":2},
    {"fct_product_funnels.date.day":"2026-03-17T00:00:00.000","fct_product_funnels.sessions":113,"fct_product_funnels.revenue":0,"fct_product_funnels.purchases":0},
    {"fct_product_funnels.date.day":"2026-03-18T00:00:00.000","fct_product_funnels.sessions":108,"fct_product_funnels.revenue":0,"fct_product_funnels.purchases":0},
    {"fct_product_funnels.date.day":"2026-03-19T00:00:00.000","fct_product_funnels.sessions":152,"fct_product_funnels.revenue":0,"fct_product_funnels.purchases":0},
    {"fct_product_funnels.date.day":"2026-03-20T00:00:00.000","fct_product_funnels.sessions":112,"fct_product_funnels.revenue":182.0,"fct_product_funnels.purchases":3},
    {"fct_product_funnels.date.day":"2026-03-21T00:00:00.000","fct_product_funnels.sessions":40,"fct_product_funnels.revenue":0,"fct_product_funnels.purchases":0},
    {"fct_product_funnels.date.day":"2026-03-22T00:00:00.000","fct_product_funnels.sessions":155,"fct_product_funnels.revenue":128.5,"fct_product_funnels.purchases":2},
]

# ============================================================
# BRAND DATA: FOND Regenerative (ab6fc1e8-f245-4344-902c-b60388575aca)
# Full MCP data
# ============================================================
FOND_MCP = [
    {"fct_product_funnels.date.day":"2026-02-06T00:00:00.000","fct_product_funnels.sessions":26,"fct_product_funnels.revenue":0,"fct_product_funnels.purchases":0},
    {"fct_product_funnels.date.day":"2026-02-07T00:00:00.000","fct_product_funnels.sessions":31,"fct_product_funnels.revenue":0,"fct_product_funnels.purchases":0},
    {"fct_product_funnels.date.day":"2026-02-08T00:00:00.000","fct_product_funnels.sessions":43,"fct_product_funnels.revenue":0,"fct_product_funnels.purchases":0},
    {"fct_product_funnels.date.day":"2026-02-09T00:00:00.000","fct_product_funnels.sessions":51,"fct_product_funnels.revenue":0,"fct_product_funnels.purchases":0},
    {"fct_product_funnels.date.day":"2026-02-10T00:00:00.000","fct_product_funnels.sessions":22,"fct_product_funnels.revenue":270.0,"fct_product_funnels.purchases":1},
    {"fct_product_funnels.date.day":"2026-02-11T00:00:00.000","fct_product_funnels.sessions":39,"fct_product_funnels.revenue":0,"fct_product_funnels.purchases":0},
    {"fct_product_funnels.date.day":"2026-02-12T00:00:00.000","fct_product_funnels.sessions":24,"fct_product_funnels.revenue":0,"fct_product_funnels.purchases":0},
    {"fct_product_funnels.date.day":"2026-02-13T00:00:00.000","fct_product_funnels.sessions":20,"fct_product_funnels.revenue":270.0,"fct_product_funnels.purchases":1},
    {"fct_product_funnels.date.day":"2026-02-14T00:00:00.000","fct_product_funnels.sessions":35,"fct_product_funnels.revenue":135.0,"fct_product_funnels.purchases":1},
    {"fct_product_funnels.date.day":"2026-02-15T00:00:00.000","fct_product_funnels.sessions":57,"fct_product_funnels.revenue":135.0,"fct_product_funnels.purchases":1},
    {"fct_product_funnels.date.day":"2026-02-16T00:00:00.000","fct_product_funnels.sessions":65,"fct_product_funnels.revenue":0,"fct_product_funnels.purchases":0},
    {"fct_product_funnels.date.day":"2026-02-17T00:00:00.000","fct_product_funnels.sessions":74,"fct_product_funnels.revenue":0,"fct_product_funnels.purchases":0},
    {"fct_product_funnels.date.day":"2026-02-18T00:00:00.000","fct_product_funnels.sessions":39,"fct_product_funnels.revenue":0,"fct_product_funnels.purchases":0},
    {"fct_product_funnels.date.day":"2026-02-19T00:00:00.000","fct_product_funnels.sessions":31,"fct_product_funnels.revenue":0,"fct_product_funnels.purchases":0},
    {"fct_product_funnels.date.day":"2026-02-20T00:00:00.000","fct_product_funnels.sessions":85,"fct_product_funnels.revenue":0,"fct_product_funnels.purchases":0},
    {"fct_product_funnels.date.day":"2026-02-21T00:00:00.000","fct_product_funnels.sessions":99,"fct_product_funnels.revenue":296.0,"fct_product_funnels.purchases":2},
    {"fct_product_funnels.date.day":"2026-02-22T00:00:00.000","fct_product_funnels.sessions":56,"fct_product_funnels.revenue":0,"fct_product_funnels.purchases":0},
    {"fct_product_funnels.date.day":"2026-02-23T00:00:00.000","fct_product_funnels.sessions":38,"fct_product_funnels.revenue":0,"fct_product_funnels.purchases":0},
    {"fct_product_funnels.date.day":"2026-02-24T00:00:00.000","fct_product_funnels.sessions":52,"fct_product_funnels.revenue":0,"fct_product_funnels.purchases":0},
    {"fct_product_funnels.date.day":"2026-02-25T00:00:00.000","fct_product_funnels.sessions":30,"fct_product_funnels.revenue":0,"fct_product_funnels.purchases":0},
    {"fct_product_funnels.date.day":"2026-02-26T00:00:00.000","fct_product_funnels.sessions":6,"fct_product_funnels.revenue":0,"fct_product_funnels.purchases":0},
    {"fct_product_funnels.date.day":"2026-02-27T00:00:00.000","fct_product_funnels.sessions":6,"fct_product_funnels.revenue":0,"fct_product_funnels.purchases":0},
    {"fct_product_funnels.date.day":"2026-02-28T00:00:00.000","fct_product_funnels.sessions":2,"fct_product_funnels.revenue":0,"fct_product_funnels.purchases":0},
    {"fct_product_funnels.date.day":"2026-03-01T00:00:00.000","fct_product_funnels.sessions":16,"fct_product_funnels.revenue":0,"fct_product_funnels.purchases":0},
    {"fct_product_funnels.date.day":"2026-03-02T00:00:00.000","fct_product_funnels.sessions":4,"fct_product_funnels.revenue":0,"fct_product_funnels.purchases":0},
    {"fct_product_funnels.date.day":"2026-03-03T00:00:00.000","fct_product_funnels.sessions":4,"fct_product_funnels.revenue":0,"fct_product_funnels.purchases":0},
    {"fct_product_funnels.date.day":"2026-03-04T00:00:00.000","fct_product_funnels.sessions":4,"fct_product_funnels.revenue":0,"fct_product_funnels.purchases":0},
    {"fct_product_funnels.date.day":"2026-03-05T00:00:00.000","fct_product_funnels.sessions":30,"fct_product_funnels.revenue":0,"fct_product_funnels.purchases":0},
    {"fct_product_funnels.date.day":"2026-03-06T00:00:00.000","fct_product_funnels.sessions":3,"fct_product_funnels.revenue":0,"fct_product_funnels.purchases":0},
    {"fct_product_funnels.date.day":"2026-03-07T00:00:00.000","fct_product_funnels.sessions":3,"fct_product_funnels.revenue":0,"fct_product_funnels.purchases":0},
    {"fct_product_funnels.date.day":"2026-03-08T00:00:00.000","fct_product_funnels.sessions":5,"fct_product_funnels.revenue":0,"fct_product_funnels.purchases":0},
    {"fct_product_funnels.date.day":"2026-03-09T00:00:00.000","fct_product_funnels.sessions":12,"fct_product_funnels.revenue":0,"fct_product_funnels.purchases":0},
    {"fct_product_funnels.date.day":"2026-03-10T00:00:00.000","fct_product_funnels.sessions":22,"fct_product_funnels.revenue":0,"fct_product_funnels.purchases":0},
    {"fct_product_funnels.date.day":"2026-03-11T00:00:00.000","fct_product_funnels.sessions":19,"fct_product_funnels.revenue":0,"fct_product_funnels.purchases":0},
    {"fct_product_funnels.date.day":"2026-03-12T00:00:00.000","fct_product_funnels.sessions":14,"fct_product_funnels.revenue":0,"fct_product_funnels.purchases":0},
    {"fct_product_funnels.date.day":"2026-03-13T00:00:00.000","fct_product_funnels.sessions":38,"fct_product_funnels.revenue":92.5,"fct_product_funnels.purchases":1},
    {"fct_product_funnels.date.day":"2026-03-14T00:00:00.000","fct_product_funnels.sessions":12,"fct_product_funnels.revenue":0,"fct_product_funnels.purchases":0},
    {"fct_product_funnels.date.day":"2026-03-15T00:00:00.000","fct_product_funnels.sessions":18,"fct_product_funnels.revenue":0,"fct_product_funnels.purchases":0},
    {"fct_product_funnels.date.day":"2026-03-16T00:00:00.000","fct_product_funnels.sessions":34,"fct_product_funnels.revenue":0,"fct_product_funnels.purchases":0},
    {"fct_product_funnels.date.day":"2026-03-17T00:00:00.000","fct_product_funnels.sessions":34,"fct_product_funnels.revenue":0,"fct_product_funnels.purchases":0},
    {"fct_product_funnels.date.day":"2026-03-18T00:00:00.000","fct_product_funnels.sessions":12,"fct_product_funnels.revenue":0,"fct_product_funnels.purchases":0},
    {"fct_product_funnels.date.day":"2026-03-19T00:00:00.000","fct_product_funnels.sessions":5,"fct_product_funnels.revenue":0,"fct_product_funnels.purchases":0},
    {"fct_product_funnels.date.day":"2026-03-20T00:00:00.000","fct_product_funnels.sessions":3,"fct_product_funnels.revenue":0,"fct_product_funnels.purchases":0},
    {"fct_product_funnels.date.day":"2026-03-21T00:00:00.000","fct_product_funnels.sessions":22,"fct_product_funnels.revenue":0,"fct_product_funnels.purchases":0},
    {"fct_product_funnels.date.day":"2026-03-22T00:00:00.000","fct_product_funnels.sessions":68,"fct_product_funnels.revenue":283.5,"fct_product_funnels.purchases":2},
]

# ============================================================
# BRAND DATA: HOP WTR (74128082-bd6b-4435-94a5-7a7fdfa41726)
# Full MCP data
# ============================================================
HOP_WTR_MCP = [
    {"fct_product_funnels.date.day":"2026-02-06T00:00:00.000","fct_product_funnels.sessions":830,"fct_product_funnels.revenue":587.11,"fct_product_funnels.purchases":8},
    {"fct_product_funnels.date.day":"2026-02-07T00:00:00.000","fct_product_funnels.sessions":1176,"fct_product_funnels.revenue":351.78,"fct_product_funnels.purchases":7},
    {"fct_product_funnels.date.day":"2026-02-08T00:00:00.000","fct_product_funnels.sessions":1246,"fct_product_funnels.revenue":358.56,"fct_product_funnels.purchases":7},
    {"fct_product_funnels.date.day":"2026-02-09T00:00:00.000","fct_product_funnels.sessions":1098,"fct_product_funnels.revenue":432.61,"fct_product_funnels.purchases":8},
    {"fct_product_funnels.date.day":"2026-02-10T00:00:00.000","fct_product_funnels.sessions":1229,"fct_product_funnels.revenue":547.65,"fct_product_funnels.purchases":10},
    {"fct_product_funnels.date.day":"2026-02-11T00:00:00.000","fct_product_funnels.sessions":1185,"fct_product_funnels.revenue":244.13,"fct_product_funnels.purchases":6},
    {"fct_product_funnels.date.day":"2026-02-12T00:00:00.000","fct_product_funnels.sessions":1192,"fct_product_funnels.revenue":514.99,"fct_product_funnels.purchases":10},
    {"fct_product_funnels.date.day":"2026-02-13T00:00:00.000","fct_product_funnels.sessions":595,"fct_product_funnels.revenue":278.2,"fct_product_funnels.purchases":7},
    {"fct_product_funnels.date.day":"2026-02-14T00:00:00.000","fct_product_funnels.sessions":390,"fct_product_funnels.revenue":391.48,"fct_product_funnels.purchases":9},
    {"fct_product_funnels.date.day":"2026-02-15T00:00:00.000","fct_product_funnels.sessions":435,"fct_product_funnels.revenue":244.17,"fct_product_funnels.purchases":6},
    {"fct_product_funnels.date.day":"2026-02-16T00:00:00.000","fct_product_funnels.sessions":587,"fct_product_funnels.revenue":266.37,"fct_product_funnels.purchases":8},
    {"fct_product_funnels.date.day":"2026-02-17T00:00:00.000","fct_product_funnels.sessions":443,"fct_product_funnels.revenue":488.33,"fct_product_funnels.purchases":11},
    {"fct_product_funnels.date.day":"2026-02-18T00:00:00.000","fct_product_funnels.sessions":352,"fct_product_funnels.revenue":31.44,"fct_product_funnels.purchases":1},
    {"fct_product_funnels.date.day":"2026-02-19T00:00:00.000","fct_product_funnels.sessions":311,"fct_product_funnels.revenue":495.29,"fct_product_funnels.purchases":8},
    {"fct_product_funnels.date.day":"2026-02-20T00:00:00.000","fct_product_funnels.sessions":209,"fct_product_funnels.revenue":62.9,"fct_product_funnels.purchases":2},
    {"fct_product_funnels.date.day":"2026-02-21T00:00:00.000","fct_product_funnels.sessions":158,"fct_product_funnels.revenue":94.34,"fct_product_funnels.purchases":2},
    {"fct_product_funnels.date.day":"2026-02-22T00:00:00.000","fct_product_funnels.sessions":274,"fct_product_funnels.revenue":157.24,"fct_product_funnels.purchases":4},
    {"fct_product_funnels.date.day":"2026-02-23T00:00:00.000","fct_product_funnels.sessions":296,"fct_product_funnels.revenue":244.93,"fct_product_funnels.purchases":4},
    {"fct_product_funnels.date.day":"2026-02-24T00:00:00.000","fct_product_funnels.sessions":644,"fct_product_funnels.revenue":193.13,"fct_product_funnels.purchases":4},
    {"fct_product_funnels.date.day":"2026-02-25T00:00:00.000","fct_product_funnels.sessions":396,"fct_product_funnels.revenue":839.11,"fct_product_funnels.purchases":14},
    {"fct_product_funnels.date.day":"2026-02-26T00:00:00.000","fct_product_funnels.sessions":550,"fct_product_funnels.revenue":283.12,"fct_product_funnels.purchases":6},
    {"fct_product_funnels.date.day":"2026-02-27T00:00:00.000","fct_product_funnels.sessions":478,"fct_product_funnels.revenue":170.64,"fct_product_funnels.purchases":4},
    {"fct_product_funnels.date.day":"2026-02-28T00:00:00.000","fct_product_funnels.sessions":413,"fct_product_funnels.revenue":117.34,"fct_product_funnels.purchases":3},
    {"fct_product_funnels.date.day":"2026-03-01T00:00:00.000","fct_product_funnels.sessions":560,"fct_product_funnels.revenue":201.27,"fct_product_funnels.purchases":4},
    {"fct_product_funnels.date.day":"2026-03-02T00:00:00.000","fct_product_funnels.sessions":381,"fct_product_funnels.revenue":65.18,"fct_product_funnels.purchases":2},
    {"fct_product_funnels.date.day":"2026-03-03T00:00:00.000","fct_product_funnels.sessions":317,"fct_product_funnels.revenue":0,"fct_product_funnels.purchases":0},
    {"fct_product_funnels.date.day":"2026-03-04T00:00:00.000","fct_product_funnels.sessions":617,"fct_product_funnels.revenue":95.31,"fct_product_funnels.purchases":2},
    {"fct_product_funnels.date.day":"2026-03-05T00:00:00.000","fct_product_funnels.sessions":219,"fct_product_funnels.revenue":64.84,"fct_product_funnels.purchases":2},
    {"fct_product_funnels.date.day":"2026-03-06T00:00:00.000","fct_product_funnels.sessions":99,"fct_product_funnels.revenue":93.19,"fct_product_funnels.purchases":2},
    {"fct_product_funnels.date.day":"2026-03-07T00:00:00.000","fct_product_funnels.sessions":75,"fct_product_funnels.revenue":33.1,"fct_product_funnels.purchases":2},
    {"fct_product_funnels.date.day":"2026-03-08T00:00:00.000","fct_product_funnels.sessions":159,"fct_product_funnels.revenue":98.8,"fct_product_funnels.purchases":2},
    {"fct_product_funnels.date.day":"2026-03-09T00:00:00.000","fct_product_funnels.sessions":96,"fct_product_funnels.revenue":85.58,"fct_product_funnels.purchases":2},
    {"fct_product_funnels.date.day":"2026-03-10T00:00:00.000","fct_product_funnels.sessions":138,"fct_product_funnels.revenue":0,"fct_product_funnels.purchases":0},
    {"fct_product_funnels.date.day":"2026-03-11T00:00:00.000","fct_product_funnels.sessions":84,"fct_product_funnels.revenue":0,"fct_product_funnels.purchases":0},
    {"fct_product_funnels.date.day":"2026-03-12T00:00:00.000","fct_product_funnels.sessions":72,"fct_product_funnels.revenue":0,"fct_product_funnels.purchases":0},
    {"fct_product_funnels.date.day":"2026-03-13T00:00:00.000","fct_product_funnels.sessions":183,"fct_product_funnels.revenue":0,"fct_product_funnels.purchases":0},
    {"fct_product_funnels.date.day":"2026-03-14T00:00:00.000","fct_product_funnels.sessions":107,"fct_product_funnels.revenue":0,"fct_product_funnels.purchases":0},
    {"fct_product_funnels.date.day":"2026-03-15T00:00:00.000","fct_product_funnels.sessions":91,"fct_product_funnels.revenue":0,"fct_product_funnels.purchases":0},
    {"fct_product_funnels.date.day":"2026-03-16T00:00:00.000","fct_product_funnels.sessions":145,"fct_product_funnels.revenue":0,"fct_product_funnels.purchases":0},
    {"fct_product_funnels.date.day":"2026-03-17T00:00:00.000","fct_product_funnels.sessions":56,"fct_product_funnels.revenue":0,"fct_product_funnels.purchases":0},
    {"fct_product_funnels.date.day":"2026-03-18T00:00:00.000","fct_product_funnels.sessions":30,"fct_product_funnels.revenue":0,"fct_product_funnels.purchases":0},
    {"fct_product_funnels.date.day":"2026-03-19T00:00:00.000","fct_product_funnels.sessions":20,"fct_product_funnels.revenue":0,"fct_product_funnels.purchases":0},
    {"fct_product_funnels.date.day":"2026-03-20T00:00:00.000","fct_product_funnels.sessions":34,"fct_product_funnels.revenue":0,"fct_product_funnels.purchases":0},
    {"fct_product_funnels.date.day":"2026-03-21T00:00:00.000","fct_product_funnels.sessions":27,"fct_product_funnels.revenue":0,"fct_product_funnels.purchases":0},
    {"fct_product_funnels.date.day":"2026-03-22T00:00:00.000","fct_product_funnels.sessions":40,"fct_product_funnels.revenue":0,"fct_product_funnels.purchases":0},
]

# ============================================================
# BRAND DATA: Little Saints (8be8e4b7-d7c1-4922-b8e3-271671ee1592)
# Full MCP data
# ============================================================
LITTLE_SAINTS_MCP = [
    {"fct_product_funnels.date.day":"2026-02-06T00:00:00.000","fct_product_funnels.sessions":1469,"fct_product_funnels.revenue":135.0,"fct_product_funnels.purchases":2},
    {"fct_product_funnels.date.day":"2026-02-07T00:00:00.000","fct_product_funnels.sessions":1230,"fct_product_funnels.revenue":68.0,"fct_product_funnels.purchases":2},
    {"fct_product_funnels.date.day":"2026-02-08T00:00:00.000","fct_product_funnels.sessions":1465,"fct_product_funnels.revenue":90.0,"fct_product_funnels.purchases":2},
    {"fct_product_funnels.date.day":"2026-02-09T00:00:00.000","fct_product_funnels.sessions":1486,"fct_product_funnels.revenue":90.0,"fct_product_funnels.purchases":1},
    {"fct_product_funnels.date.day":"2026-02-10T00:00:00.000","fct_product_funnels.sessions":1518,"fct_product_funnels.revenue":80.0,"fct_product_funnels.purchases":2},
    {"fct_product_funnels.date.day":"2026-02-11T00:00:00.000","fct_product_funnels.sessions":1133,"fct_product_funnels.revenue":40.5,"fct_product_funnels.purchases":1},
    {"fct_product_funnels.date.day":"2026-02-12T00:00:00.000","fct_product_funnels.sessions":1350,"fct_product_funnels.revenue":0,"fct_product_funnels.purchases":0},
    {"fct_product_funnels.date.day":"2026-02-13T00:00:00.000","fct_product_funnels.sessions":1326,"fct_product_funnels.revenue":0,"fct_product_funnels.purchases":0},
    {"fct_product_funnels.date.day":"2026-02-14T00:00:00.000","fct_product_funnels.sessions":1226,"fct_product_funnels.revenue":38.25,"fct_product_funnels.purchases":1},
    {"fct_product_funnels.date.day":"2026-02-15T00:00:00.000","fct_product_funnels.sessions":1180,"fct_product_funnels.revenue":83.25,"fct_product_funnels.purchases":2},
    {"fct_product_funnels.date.day":"2026-02-16T00:00:00.000","fct_product_funnels.sessions":627,"fct_product_funnels.revenue":0,"fct_product_funnels.purchases":0},
    {"fct_product_funnels.date.day":"2026-02-17T00:00:00.000","fct_product_funnels.sessions":3201,"fct_product_funnels.revenue":0,"fct_product_funnels.purchases":0},
    {"fct_product_funnels.date.day":"2026-02-18T00:00:00.000","fct_product_funnels.sessions":59,"fct_product_funnels.revenue":45.0,"fct_product_funnels.purchases":1},
    {"fct_product_funnels.date.day":"2026-02-19T00:00:00.000","fct_product_funnels.sessions":70,"fct_product_funnels.revenue":0,"fct_product_funnels.purchases":0},
    {"fct_product_funnels.date.day":"2026-02-20T00:00:00.000","fct_product_funnels.sessions":76,"fct_product_funnels.revenue":147.0,"fct_product_funnels.purchases":2},
    {"fct_product_funnels.date.day":"2026-02-21T00:00:00.000","fct_product_funnels.sessions":97,"fct_product_funnels.revenue":35.0,"fct_product_funnels.purchases":1},
    {"fct_product_funnels.date.day":"2026-02-22T00:00:00.000","fct_product_funnels.sessions":49,"fct_product_funnels.revenue":0,"fct_product_funnels.purchases":0},
    {"fct_product_funnels.date.day":"2026-02-23T00:00:00.000","fct_product_funnels.sessions":62,"fct_product_funnels.revenue":102.0,"fct_product_funnels.purchases":1},
    {"fct_product_funnels.date.day":"2026-02-24T00:00:00.000","fct_product_funnels.sessions":107,"fct_product_funnels.revenue":178.8,"fct_product_funnels.purchases":2},
    {"fct_product_funnels.date.day":"2026-02-25T00:00:00.000","fct_product_funnels.sessions":117,"fct_product_funnels.revenue":38.25,"fct_product_funnels.purchases":1},
    {"fct_product_funnels.date.day":"2026-02-26T00:00:00.000","fct_product_funnels.sessions":213,"fct_product_funnels.revenue":217.0,"fct_product_funnels.purchases":3},
    {"fct_product_funnels.date.day":"2026-02-27T00:00:00.000","fct_product_funnels.sessions":332,"fct_product_funnels.revenue":76.5,"fct_product_funnels.purchases":2},
    {"fct_product_funnels.date.day":"2026-02-28T00:00:00.000","fct_product_funnels.sessions":235,"fct_product_funnels.revenue":76.5,"fct_product_funnels.purchases":2},
    {"fct_product_funnels.date.day":"2026-03-01T00:00:00.000","fct_product_funnels.sessions":336,"fct_product_funnels.revenue":236.25,"fct_product_funnels.purchases":4},
    {"fct_product_funnels.date.day":"2026-03-02T00:00:00.000","fct_product_funnels.sessions":297,"fct_product_funnels.revenue":255.0,"fct_product_funnels.purchases":4},
    {"fct_product_funnels.date.day":"2026-03-03T00:00:00.000","fct_product_funnels.sessions":213,"fct_product_funnels.revenue":38.25,"fct_product_funnels.purchases":1},
    {"fct_product_funnels.date.day":"2026-03-04T00:00:00.000","fct_product_funnels.sessions":168,"fct_product_funnels.revenue":0,"fct_product_funnels.purchases":0},
    {"fct_product_funnels.date.day":"2026-03-05T00:00:00.000","fct_product_funnels.sessions":120,"fct_product_funnels.revenue":38.25,"fct_product_funnels.purchases":1},
    {"fct_product_funnels.date.day":"2026-03-06T00:00:00.000","fct_product_funnels.sessions":86,"fct_product_funnels.revenue":76.5,"fct_product_funnels.purchases":1},
    {"fct_product_funnels.date.day":"2026-03-07T00:00:00.000","fct_product_funnels.sessions":53,"fct_product_funnels.revenue":76.5,"fct_product_funnels.purchases":1},
    {"fct_product_funnels.date.day":"2026-03-08T00:00:00.000","fct_product_funnels.sessions":65,"fct_product_funnels.revenue":23.8,"fct_product_funnels.purchases":1},
    {"fct_product_funnels.date.day":"2026-03-09T00:00:00.000","fct_product_funnels.sessions":82,"fct_product_funnels.revenue":0,"fct_product_funnels.purchases":0},
    {"fct_product_funnels.date.day":"2026-03-10T00:00:00.000","fct_product_funnels.sessions":119,"fct_product_funnels.revenue":83.25,"fct_product_funnels.purchases":2},
    {"fct_product_funnels.date.day":"2026-03-11T00:00:00.000","fct_product_funnels.sessions":87,"fct_product_funnels.revenue":0,"fct_product_funnels.purchases":0},
    {"fct_product_funnels.date.day":"2026-03-12T00:00:00.000","fct_product_funnels.sessions":149,"fct_product_funnels.revenue":38.25,"fct_product_funnels.purchases":1},
    {"fct_product_funnels.date.day":"2026-03-13T00:00:00.000","fct_product_funnels.sessions":121,"fct_product_funnels.revenue":0,"fct_product_funnels.purchases":0},
    {"fct_product_funnels.date.day":"2026-03-14T00:00:00.000","fct_product_funnels.sessions":65,"fct_product_funnels.revenue":102.0,"fct_product_funnels.purchases":1},
    {"fct_product_funnels.date.day":"2026-03-15T00:00:00.000","fct_product_funnels.sessions":97,"fct_product_funnels.revenue":308.5,"fct_product_funnels.purchases":3},
    {"fct_product_funnels.date.day":"2026-03-16T00:00:00.000","fct_product_funnels.sessions":291,"fct_product_funnels.revenue":57.75,"fct_product_funnels.purchases":2},
    {"fct_product_funnels.date.day":"2026-03-17T00:00:00.000","fct_product_funnels.sessions":113,"fct_product_funnels.revenue":0,"fct_product_funnels.purchases":0},
    {"fct_product_funnels.date.day":"2026-03-18T00:00:00.000","fct_product_funnels.sessions":108,"fct_product_funnels.revenue":0,"fct_product_funnels.purchases":0},
    {"fct_product_funnels.date.day":"2026-03-19T00:00:00.000","fct_product_funnels.sessions":152,"fct_product_funnels.revenue":0,"fct_product_funnels.purchases":0},
    {"fct_product_funnels.date.day":"2026-03-20T00:00:00.000","fct_product_funnels.sessions":112,"fct_product_funnels.revenue":182.0,"fct_product_funnels.purchases":3},
    {"fct_product_funnels.date.day":"2026-03-21T00:00:00.000","fct_product_funnels.sessions":40,"fct_product_funnels.revenue":0,"fct_product_funnels.purchases":0},
    {"fct_product_funnels.date.day":"2026-03-22T00:00:00.000","fct_product_funnels.sessions":155,"fct_product_funnels.revenue":128.5,"fct_product_funnels.purchases":2},
]

# ============================================================
# BRAND DATA: Shop FlavCity (737444a0-c397-46a8-a53f-8b32d07a1722)
# Full MCP data (massive bot traffic)
# ============================================================
FLAVCITY_MCP = [
    {"fct_product_funnels.date.day":"2026-02-06T00:00:00.000","fct_product_funnels.sessions":9,"fct_product_funnels.revenue":0,"fct_product_funnels.purchases":0},
    {"fct_product_funnels.date.day":"2026-02-07T00:00:00.000","fct_product_funnels.sessions":2,"fct_product_funnels.revenue":0,"fct_product_funnels.purchases":0},
    {"fct_product_funnels.date.day":"2026-02-09T00:00:00.000","fct_product_funnels.sessions":1,"fct_product_funnels.revenue":0,"fct_product_funnels.purchases":0},
    {"fct_product_funnels.date.day":"2026-02-10T00:00:00.000","fct_product_funnels.sessions":1,"fct_product_funnels.revenue":0,"fct_product_funnels.purchases":0},
    {"fct_product_funnels.date.day":"2026-02-11T00:00:00.000","fct_product_funnels.sessions":5,"fct_product_funnels.revenue":0,"fct_product_funnels.purchases":0},
    {"fct_product_funnels.date.day":"2026-02-12T00:00:00.000","fct_product_funnels.sessions":3,"fct_product_funnels.revenue":0,"fct_product_funnels.purchases":0},
    {"fct_product_funnels.date.day":"2026-02-13T00:00:00.000","fct_product_funnels.sessions":9,"fct_product_funnels.revenue":0,"fct_product_funnels.purchases":0},
    {"fct_product_funnels.date.day":"2026-02-14T00:00:00.000","fct_product_funnels.sessions":9139,"fct_product_funnels.revenue":12138.86,"fct_product_funnels.purchases":151},
    {"fct_product_funnels.date.day":"2026-02-15T00:00:00.000","fct_product_funnels.sessions":5305,"fct_product_funnels.revenue":7541.91,"fct_product_funnels.purchases":89},
    {"fct_product_funnels.date.day":"2026-02-16T00:00:00.000","fct_product_funnels.sessions":3893,"fct_product_funnels.revenue":5746.89,"fct_product_funnels.purchases":69},
    {"fct_product_funnels.date.day":"2026-02-17T00:00:00.000","fct_product_funnels.sessions":3211,"fct_product_funnels.revenue":3719.9,"fct_product_funnels.purchases":44},
    {"fct_product_funnels.date.day":"2026-02-18T00:00:00.000","fct_product_funnels.sessions":2200,"fct_product_funnels.revenue":3186.42,"fct_product_funnels.purchases":45},
    {"fct_product_funnels.date.day":"2026-02-19T00:00:00.000","fct_product_funnels.sessions":2200,"fct_product_funnels.revenue":2571.94,"fct_product_funnels.purchases":36},
    {"fct_product_funnels.date.day":"2026-02-20T00:00:00.000","fct_product_funnels.sessions":1783,"fct_product_funnels.revenue":3601.91,"fct_product_funnels.purchases":41},
    {"fct_product_funnels.date.day":"2026-02-21T00:00:00.000","fct_product_funnels.sessions":1406,"fct_product_funnels.revenue":1491.94,"fct_product_funnels.purchases":22},
    {"fct_product_funnels.date.day":"2026-02-22T00:00:00.000","fct_product_funnels.sessions":1131,"fct_product_funnels.revenue":3183.87,"fct_product_funnels.purchases":37},
    {"fct_product_funnels.date.day":"2026-02-23T00:00:00.000","fct_product_funnels.sessions":1118,"fct_product_funnels.revenue":2217.96,"fct_product_funnels.purchases":25},
    {"fct_product_funnels.date.day":"2026-02-24T00:00:00.000","fct_product_funnels.sessions":781,"fct_product_funnels.revenue":2506.0,"fct_product_funnels.purchases":19},
    {"fct_product_funnels.date.day":"2026-02-25T00:00:00.000","fct_product_funnels.sessions":6267,"fct_product_funnels.revenue":1323.38,"fct_product_funnels.purchases":19},
    {"fct_product_funnels.date.day":"2026-02-26T00:00:00.000","fct_product_funnels.sessions":111521,"fct_product_funnels.revenue":1394.98,"fct_product_funnels.purchases":19},
    {"fct_product_funnels.date.day":"2026-02-27T00:00:00.000","fct_product_funnels.sessions":52507,"fct_product_funnels.revenue":1143.92,"fct_product_funnels.purchases":12},
    {"fct_product_funnels.date.day":"2026-02-28T00:00:00.000","fct_product_funnels.sessions":85673,"fct_product_funnels.revenue":974.94,"fct_product_funnels.purchases":11},
    {"fct_product_funnels.date.day":"2026-03-01T00:00:00.000","fct_product_funnels.sessions":90691,"fct_product_funnels.revenue":675.95,"fct_product_funnels.purchases":8},
    {"fct_product_funnels.date.day":"2026-03-02T00:00:00.000","fct_product_funnels.sessions":125113,"fct_product_funnels.revenue":624.96,"fct_product_funnels.purchases":8},
    {"fct_product_funnels.date.day":"2026-03-03T00:00:00.000","fct_product_funnels.sessions":13690,"fct_product_funnels.revenue":210.0,"fct_product_funnels.purchases":3},
    {"fct_product_funnels.date.day":"2026-03-04T00:00:00.000","fct_product_funnels.sessions":29647,"fct_product_funnels.revenue":392.98,"fct_product_funnels.purchases":5},
    {"fct_product_funnels.date.day":"2026-03-05T00:00:00.000","fct_product_funnels.sessions":14869,"fct_product_funnels.revenue":897.96,"fct_product_funnels.purchases":12},
    {"fct_product_funnels.date.day":"2026-03-06T00:00:00.000","fct_product_funnels.sessions":41085,"fct_product_funnels.revenue":448.98,"fct_product_funnels.purchases":6},
    {"fct_product_funnels.date.day":"2026-03-07T00:00:00.000","fct_product_funnels.sessions":54326,"fct_product_funnels.revenue":851.9,"fct_product_funnels.purchases":4},
    {"fct_product_funnels.date.day":"2026-03-08T00:00:00.000","fct_product_funnels.sessions":27301,"fct_product_funnels.revenue":960.96,"fct_product_funnels.purchases":11},
    {"fct_product_funnels.date.day":"2026-03-09T00:00:00.000","fct_product_funnels.sessions":39958,"fct_product_funnels.revenue":737.94,"fct_product_funnels.purchases":7},
    {"fct_product_funnels.date.day":"2026-03-10T00:00:00.000","fct_product_funnels.sessions":38949,"fct_product_funnels.revenue":479.99,"fct_product_funnels.purchases":7},
    {"fct_product_funnels.date.day":"2026-03-11T00:00:00.000","fct_product_funnels.sessions":132906,"fct_product_funnels.revenue":543.97,"fct_product_funnels.purchases":7},
    {"fct_product_funnels.date.day":"2026-03-12T00:00:00.000","fct_product_funnels.sessions":110323,"fct_product_funnels.revenue":149.99,"fct_product_funnels.purchases":3},
    {"fct_product_funnels.date.day":"2026-03-13T00:00:00.000","fct_product_funnels.sessions":95843,"fct_product_funnels.revenue":646.94,"fct_product_funnels.purchases":7},
    {"fct_product_funnels.date.day":"2026-03-14T00:00:00.000","fct_product_funnels.sessions":109883,"fct_product_funnels.revenue":808.97,"fct_product_funnels.purchases":9},
    {"fct_product_funnels.date.day":"2026-03-15T00:00:00.000","fct_product_funnels.sessions":94902,"fct_product_funnels.revenue":269.99,"fct_product_funnels.purchases":4},
    {"fct_product_funnels.date.day":"2026-03-16T00:00:00.000","fct_product_funnels.sessions":150287,"fct_product_funnels.revenue":185.99,"fct_product_funnels.purchases":2},
    {"fct_product_funnels.date.day":"2026-03-17T00:00:00.000","fct_product_funnels.sessions":104976,"fct_product_funnels.revenue":143.99,"fct_product_funnels.purchases":3},
    {"fct_product_funnels.date.day":"2026-03-18T00:00:00.000","fct_product_funnels.sessions":112080,"fct_product_funnels.revenue":107.99,"fct_product_funnels.purchases":2},
    {"fct_product_funnels.date.day":"2026-03-19T00:00:00.000","fct_product_funnels.sessions":140974,"fct_product_funnels.revenue":185.99,"fct_product_funnels.purchases":2},
    {"fct_product_funnels.date.day":"2026-03-20T00:00:00.000","fct_product_funnels.sessions":81292,"fct_product_funnels.revenue":389.97,"fct_product_funnels.purchases":6},
    {"fct_product_funnels.date.day":"2026-03-21T00:00:00.000","fct_product_funnels.sessions":55257,"fct_product_funnels.revenue":227.97,"fct_product_funnels.purchases":4},
    {"fct_product_funnels.date.day":"2026-03-22T00:00:00.000","fct_product_funnels.sessions":73744,"fct_product_funnels.revenue":147.98,"fct_product_funnels.purchases":2},
]

# ============================================================
# BRAND DATA: MOTHER ROOT (ae4f1f5d-f1d1-488f-8340-1890cfd0faf3)
# Full MCP data - winding down, no data after Mar 6
# ============================================================
MOTHER_ROOT_MCP = [
    {"fct_product_funnels.date.day":"2026-02-19T00:00:00.000","fct_product_funnels.sessions":353,"fct_product_funnels.revenue":167.7,"fct_product_funnels.purchases":6},
    {"fct_product_funnels.date.day":"2026-02-20T00:00:00.000","fct_product_funnels.sessions":583,"fct_product_funnels.revenue":495.93,"fct_product_funnels.purchases":14},
    {"fct_product_funnels.date.day":"2026-02-21T00:00:00.000","fct_product_funnels.sessions":605,"fct_product_funnels.revenue":440.46,"fct_product_funnels.purchases":14},
    {"fct_product_funnels.date.day":"2026-02-22T00:00:00.000","fct_product_funnels.sessions":596,"fct_product_funnels.revenue":484.36,"fct_product_funnels.purchases":16},
    {"fct_product_funnels.date.day":"2026-02-23T00:00:00.000","fct_product_funnels.sessions":519,"fct_product_funnels.revenue":251.76,"fct_product_funnels.purchases":7},
    {"fct_product_funnels.date.day":"2026-02-24T00:00:00.000","fct_product_funnels.sessions":541,"fct_product_funnels.revenue":627.06,"fct_product_funnels.purchases":16},
    {"fct_product_funnels.date.day":"2026-02-25T00:00:00.000","fct_product_funnels.sessions":700,"fct_product_funnels.revenue":485.92,"fct_product_funnels.purchases":14},
    {"fct_product_funnels.date.day":"2026-02-26T00:00:00.000","fct_product_funnels.sessions":533,"fct_product_funnels.revenue":402.88,"fct_product_funnels.purchases":11},
    {"fct_product_funnels.date.day":"2026-02-27T00:00:00.000","fct_product_funnels.sessions":616,"fct_product_funnels.revenue":564.41,"fct_product_funnels.purchases":14},
    {"fct_product_funnels.date.day":"2026-02-28T00:00:00.000","fct_product_funnels.sessions":633,"fct_product_funnels.revenue":496.79,"fct_product_funnels.purchases":13},
    {"fct_product_funnels.date.day":"2026-03-01T00:00:00.000","fct_product_funnels.sessions":742,"fct_product_funnels.revenue":787.75,"fct_product_funnels.purchases":13},
    {"fct_product_funnels.date.day":"2026-03-02T00:00:00.000","fct_product_funnels.sessions":454,"fct_product_funnels.revenue":96.8,"fct_product_funnels.purchases":3},
    {"fct_product_funnels.date.day":"2026-03-03T00:00:00.000","fct_product_funnels.sessions":333,"fct_product_funnels.revenue":357.37,"fct_product_funnels.purchases":10},
    {"fct_product_funnels.date.day":"2026-03-04T00:00:00.000","fct_product_funnels.sessions":250,"fct_product_funnels.revenue":259.87,"fct_product_funnels.purchases":7},
    {"fct_product_funnels.date.day":"2026-03-05T00:00:00.000","fct_product_funnels.sessions":273,"fct_product_funnels.revenue":69.8,"fct_product_funnels.purchases":2},
    {"fct_product_funnels.date.day":"2026-03-06T00:00:00.000","fct_product_funnels.sessions":79,"fct_product_funnels.revenue":55.9,"fct_product_funnels.purchases":2},
    {"fct_product_funnels.date.day":"2026-03-11T00:00:00.000","fct_product_funnels.sessions":1,"fct_product_funnels.revenue":0,"fct_product_funnels.purchases":0},
    {"fct_product_funnels.date.day":"2026-03-12T00:00:00.000","fct_product_funnels.sessions":3,"fct_product_funnels.revenue":0,"fct_product_funnels.purchases":0},
    {"fct_product_funnels.date.day":"2026-03-13T00:00:00.000","fct_product_funnels.sessions":2,"fct_product_funnels.revenue":0,"fct_product_funnels.purchases":0},
    {"fct_product_funnels.date.day":"2026-03-16T00:00:00.000","fct_product_funnels.sessions":7,"fct_product_funnels.revenue":0,"fct_product_funnels.purchases":0},
]

# ============================================================
# BRAND DATA: Gains In Bulk (5cc7fc09-8acf-4af0-892f-735c6686c2a2)
# Full MCP data - essentially inactive
# ============================================================
GAINS_MCP = [
    {"fct_product_funnels.date.day":"2026-02-06T00:00:00.000","fct_product_funnels.sessions":1,"fct_product_funnels.revenue":0,"fct_product_funnels.purchases":0},
    {"fct_product_funnels.date.day":"2026-02-07T00:00:00.000","fct_product_funnels.sessions":2,"fct_product_funnels.revenue":0,"fct_product_funnels.purchases":0},
    {"fct_product_funnels.date.day":"2026-02-08T00:00:00.000","fct_product_funnels.sessions":2,"fct_product_funnels.revenue":0,"fct_product_funnels.purchases":0},
    {"fct_product_funnels.date.day":"2026-02-09T00:00:00.000","fct_product_funnels.sessions":1,"fct_product_funnels.revenue":0,"fct_product_funnels.purchases":0},
    {"fct_product_funnels.date.day":"2026-02-11T00:00:00.000","fct_product_funnels.sessions":5,"fct_product_funnels.revenue":0,"fct_product_funnels.purchases":0},
    {"fct_product_funnels.date.day":"2026-02-12T00:00:00.000","fct_product_funnels.sessions":3,"fct_product_funnels.revenue":0,"fct_product_funnels.purchases":0},
    {"fct_product_funnels.date.day":"2026-02-13T00:00:00.000","fct_product_funnels.sessions":2,"fct_product_funnels.revenue":0,"fct_product_funnels.purchases":0},
    {"fct_product_funnels.date.day":"2026-02-14T00:00:00.000","fct_product_funnels.sessions":1,"fct_product_funnels.revenue":0,"fct_product_funnels.purchases":0},
    {"fct_product_funnels.date.day":"2026-02-15T00:00:00.000","fct_product_funnels.sessions":1,"fct_product_funnels.revenue":0,"fct_product_funnels.purchases":0},
    {"fct_product_funnels.date.day":"2026-02-16T00:00:00.000","fct_product_funnels.sessions":5,"fct_product_funnels.revenue":0,"fct_product_funnels.purchases":0},
    {"fct_product_funnels.date.day":"2026-02-18T00:00:00.000","fct_product_funnels.sessions":2,"fct_product_funnels.revenue":0,"fct_product_funnels.purchases":0},
    {"fct_product_funnels.date.day":"2026-02-20T00:00:00.000","fct_product_funnels.sessions":1,"fct_product_funnels.revenue":0,"fct_product_funnels.purchases":0},
    {"fct_product_funnels.date.day":"2026-02-21T00:00:00.000","fct_product_funnels.sessions":1,"fct_product_funnels.revenue":0,"fct_product_funnels.purchases":0},
    {"fct_product_funnels.date.day":"2026-02-22T00:00:00.000","fct_product_funnels.sessions":1,"fct_product_funnels.revenue":0,"fct_product_funnels.purchases":0},
    {"fct_product_funnels.date.day":"2026-02-23T00:00:00.000","fct_product_funnels.sessions":5,"fct_product_funnels.revenue":0,"fct_product_funnels.purchases":0},
    {"fct_product_funnels.date.day":"2026-02-24T00:00:00.000","fct_product_funnels.sessions":2,"fct_product_funnels.revenue":0,"fct_product_funnels.purchases":0},
    {"fct_product_funnels.date.day":"2026-02-25T00:00:00.000","fct_product_funnels.sessions":2,"fct_product_funnels.revenue":0,"fct_product_funnels.purchases":0},
    {"fct_product_funnels.date.day":"2026-02-26T00:00:00.000","fct_product_funnels.sessions":3,"fct_product_funnels.revenue":0,"fct_product_funnels.purchases":0},
    {"fct_product_funnels.date.day":"2026-02-27T00:00:00.000","fct_product_funnels.sessions":4,"fct_product_funnels.revenue":0,"fct_product_funnels.purchases":0},
    {"fct_product_funnels.date.day":"2026-02-28T00:00:00.000","fct_product_funnels.sessions":2,"fct_product_funnels.revenue":0,"fct_product_funnels.purchases":0},
    {"fct_product_funnels.date.day":"2026-03-01T00:00:00.000","fct_product_funnels.sessions":1,"fct_product_funnels.revenue":0,"fct_product_funnels.purchases":0},
    {"fct_product_funnels.date.day":"2026-03-02T00:00:00.000","fct_product_funnels.sessions":5,"fct_product_funnels.revenue":0,"fct_product_funnels.purchases":0},
    {"fct_product_funnels.date.day":"2026-03-03T00:00:00.000","fct_product_funnels.sessions":5,"fct_product_funnels.revenue":0,"fct_product_funnels.purchases":0},
    {"fct_product_funnels.date.day":"2026-03-04T00:00:00.000","fct_product_funnels.sessions":1,"fct_product_funnels.revenue":0,"fct_product_funnels.purchases":0},
    {"fct_product_funnels.date.day":"2026-03-06T00:00:00.000","fct_product_funnels.sessions":6,"fct_product_funnels.revenue":0,"fct_product_funnels.purchases":0},
    {"fct_product_funnels.date.day":"2026-03-08T00:00:00.000","fct_product_funnels.sessions":4,"fct_product_funnels.revenue":0,"fct_product_funnels.purchases":0},
    {"fct_product_funnels.date.day":"2026-03-09T00:00:00.000","fct_product_funnels.sessions":1,"fct_product_funnels.revenue":0,"fct_product_funnels.purchases":0},
    {"fct_product_funnels.date.day":"2026-03-10T00:00:00.000","fct_product_funnels.sessions":5,"fct_product_funnels.revenue":0,"fct_product_funnels.purchases":0},
    {"fct_product_funnels.date.day":"2026-03-11T00:00:00.000","fct_product_funnels.sessions":3,"fct_product_funnels.revenue":0,"fct_product_funnels.purchases":0},
    {"fct_product_funnels.date.day":"2026-03-12T00:00:00.000","fct_product_funnels.sessions":6,"fct_product_funnels.revenue":0,"fct_product_funnels.purchases":0},
    {"fct_product_funnels.date.day":"2026-03-13T00:00:00.000","fct_product_funnels.sessions":2,"fct_product_funnels.revenue":0,"fct_product_funnels.purchases":0},
    {"fct_product_funnels.date.day":"2026-03-14T00:00:00.000","fct_product_funnels.sessions":5,"fct_product_funnels.revenue":0,"fct_product_funnels.purchases":0},
    {"fct_product_funnels.date.day":"2026-03-15T00:00:00.000","fct_product_funnels.sessions":4,"fct_product_funnels.revenue":0,"fct_product_funnels.purchases":0},
    {"fct_product_funnels.date.day":"2026-03-16T00:00:00.000","fct_product_funnels.sessions":4,"fct_product_funnels.revenue":0,"fct_product_funnels.purchases":0},
    {"fct_product_funnels.date.day":"2026-03-17T00:00:00.000","fct_product_funnels.sessions":6,"fct_product_funnels.revenue":78.0,"fct_product_funnels.purchases":1},
    {"fct_product_funnels.date.day":"2026-03-18T00:00:00.000","fct_product_funnels.sessions":2,"fct_product_funnels.revenue":0,"fct_product_funnels.purchases":0},
    {"fct_product_funnels.date.day":"2026-03-19T00:00:00.000","fct_product_funnels.sessions":5,"fct_product_funnels.revenue":0,"fct_product_funnels.purchases":0},
    {"fct_product_funnels.date.day":"2026-03-20T00:00:00.000","fct_product_funnels.sessions":7,"fct_product_funnels.revenue":0,"fct_product_funnels.purchases":0},
    {"fct_product_funnels.date.day":"2026-03-21T00:00:00.000","fct_product_funnels.sessions":1,"fct_product_funnels.revenue":0,"fct_product_funnels.purchases":0},
    {"fct_product_funnels.date.day":"2026-03-22T00:00:00.000","fct_product_funnels.sessions":3,"fct_product_funnels.revenue":0,"fct_product_funnels.purchases":0},
]


def mcp_to_daily(mcp_rows):
    """Convert inline MCP-style dicts to (date, sessions, revenue, purchases) tuples."""
    daily = []
    for row in mcp_rows:
        d_str = row["fct_product_funnels.date.day"][:10]
        d = date.fromisoformat(d_str)
        s = row["fct_product_funnels.sessions"]
        r = row.get("fct_product_funnels.revenue", 0) or 0
        p = row.get("fct_product_funnels.purchases", 0) or 0
        daily.append((d, s, r, p))
    return daily


# ============================================================
# MAIN
# ============================================================
if __name__ == "__main__":
    print("=" * 70)
    print("Updating Account Management Portal performance data")
    print(f"Reference date: {REF_DATE} | last_updated: {LAST_UPDATED}")
    print("=" * 70)

    brands = [
        ("8fd93118-a246-431e-aebf-4aa362622342", "De Soi", DE_SOI_DAILY),
        ("39f04705-e991-461e-a98f-2dd3f29d6e47", "belliwelli", mcp_to_daily(BELLIWELLI_MCP)),
        ("f7983632-4d4b-49c8-8e7a-192e9e999dff", "Henry Rose", mcp_to_daily(HENRY_ROSE_MCP)),
        ("f0a1a21b-3832-4bfd-ad3d-af38d11a90e8", "Moment", MOMENT_DAILY),
        ("f8f83f9d-be9e-4177-ad7e-292ed079eafd", "Veracity Selfcare", mcp_to_daily(VERACITY_MCP)),
        ("c686cb26-9441-4aa2-883e-7204999f2bc4", "Sole Toscana", mcp_to_daily(SOLE_TOSCANA_MCP)),
        ("ab6fc1e8-f245-4344-902c-b60388575aca", "FOND Regenerative", mcp_to_daily(FOND_MCP)),
        ("74128082-bd6b-4435-94a5-7a7fdfa41726", "HOP WTR", mcp_to_daily(HOP_WTR_MCP)),
        ("8be8e4b7-d7c1-4922-b8e3-271671ee1592", "Little Saints", mcp_to_daily(LITTLE_SAINTS_MCP)),
        ("737444a0-c397-46a8-a53f-8b32d07a1722", "Shop FlavCity", mcp_to_daily(FLAVCITY_MCP)),
        ("ae4f1f5d-f1d1-488f-8340-1890cfd0faf3", "MOTHER ROOT", mcp_to_daily(MOTHER_ROOT_MCP)),
        ("5cc7fc09-8acf-4af0-892f-735c6686c2a2", "Gains In Bulk", mcp_to_daily(GAINS_MCP)),
    ]

    # Brands with no data -- just update last_updated timestamp
    no_data_brands = [
        "35845b70-d5ef-4dbf-83cf-e9f327662c17",  # Medik8
        "508e7756-81aa-48b1-bbf5-765d2e8f1eb9",  # Westmore Beauty
        "1e7aa370-3cde-40bf-90d9-8ce8a3aaed30",  # HAVN
    ]

    for csv_id, name, daily_data in brands:
        print(f"\n[{name}]")
        update_brand(csv_id, daily_data)

    # Update last_updated for no-data brands
    for csv_id in no_data_brands:
        filepath = os.path.join(DATA, f"{csv_id}.json")
        if os.path.exists(filepath):
            with open(filepath, "r") as f:
                data = json.load(f)
            data["last_updated"] = LAST_UPDATED
            with open(filepath, "w") as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
            print(f"\n[{data.get('brand_name', csv_id)}] Updated last_updated only (no data)")

    print("\n" + "=" * 70)
    print("All performance data updated. Running build.py...")
    print("=" * 70)
