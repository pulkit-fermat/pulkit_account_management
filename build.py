#!/usr/bin/env python3
"""
Build Account Management Portal v2 — Visual Dashboard with Charts
Generates a single self-contained HTML file with Chart.js visualizations.
"""
import json, os, html as H
from datetime import datetime

DIR  = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(DIR, "data")
OUT  = os.path.join(DIR, "index.html")

FLOGO = "https://cdn.prod.website-files.com/63f5f201b1f212a5c76681f0/63f6319f0b6d0beeffa89a24_Logo.svg"

LOGOS = {
    "35845b70-d5ef-4dbf-83cf-e9f327662c17": "https://www.medik8.com/cdn/shop/t/331/assets/logo.png?v=20852127142504936671709712608",
    "508e7756-81aa-48b1-bbf5-765d2e8f1eb9": "https://www.leapingbunny.org/sites/default/files/2024-02/Westmore%20Beauty%20Logo_purple_updated_052919%20%281%29.png",
    "ae4f1f5d-f1d1-488f-8340-1890cfd0faf3": "https://d19ayerf5ehaab.cloudfront.net/assets/store-534884/534884-logo-1736177561.png",
    "39f04705-e991-461e-a98f-2dd3f29d6e47": "https://wellybelly.in/cdn/shop/files/Welly_Belly_Final_Logo_2_0f65ddea-5650-47ba-a2ab-632871ef89aa.png?v=1740736627",
    "ab6fc1e8-f245-4344-902c-b60388575aca": "https://wholesale.fondbonebroth.com/cdn/shop/files/FND_Secondary_logo_Navy_wStroke_RGB_eebc91b8-6b17-46f5-a8d5-43c1367c94f2.png?v=1686840930",
    "74128082-bd6b-4435-94a5-7a7fdfa41726": "https://t2.gstatic.com/faviconV2?client=SOCIAL&type=FAVICON&fallback_opts=TYPE,SIZE,URL&url=https://hopwtr.com&size=128",
    "8be8e4b7-d7c1-4922-b8e3-271671ee1592": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQuBCOEsyGqSBYXAFNAeg7-NTOlSijnS_jW4w&s",
    "737444a0-c397-46a8-a53f-8b32d07a1722": "https://t2.gstatic.com/faviconV2?client=SOCIAL&type=FAVICON&fallback_opts=TYPE,SIZE,URL&url=https://shopflavcity.com&size=128",
    "1e7aa370-3cde-40bf-90d9-8ce8a3aaed30": "https://t2.gstatic.com/faviconV2?client=SOCIAL&type=FAVICON&fallback_opts=TYPE,SIZE,URL&url=https://havnwear.com&size=128",
    "f0a1a21b-3832-4bfd-ad3d-af38d11a90e8": "https://drinkmoment.com/cdn/shop/files/moment-logo_e56b4e47-36a3-4a84-954f-36f0e130a451.png?v=1682983267",
    "f7983632-4d4b-49c8-8e7a-192e9e999dff": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcT6rZeCEH-H6ob3EaT2tlKC9K6_3cBsUs4r6w&s",
    "f8f83f9d-be9e-4177-ad7e-292ed079eafd": "https://cdn.sanity.io/images/r9400t60/production/77ddf8e2d8ac336bf8ee457319f63c03265d96d0-1080x1080.png?fm=webp&q=85",
    "c686cb26-9441-4aa2-883e-7204999f2bc4": "https://cdn05.zipify.com/mVnWKnc4QGQcZBz4LYnC5Co_AxE=/17x139:750x600/fit-in/3840x0/d9757b1e13b947c49c1d73c65aa1515b/simple-logo_nodate.png",
    "8fd93118-a246-431e-aebf-4aa362622342": "https://cdn.shopify.com/s/files/1/0565/6621/8952/files/De_Soi_New_Logo_2_cropped.png?v=1688586288",
    "5cc7fc09-8acf-4af0-892f-735c6686c2a2": "https://t2.gstatic.com/faviconV2?client=SOCIAL&type=FAVICON&fallback_opts=TYPE,SIZE,URL&url=https://gainsinbulk.com&size=128",
}

SLACKS = {
    "C0AK2MN11H7":"fermat-x-medik8","C0ACP5J50H2":"fermat-x-westmorebeauty",
    "C09THN58W59":"fermat-x-motherroot","C0A99HSHTCL":"belliwelli-fermat-new",
    "C09GBN46A68":"fermat-x-fond","C09BYRY8PE2":"fermat-x-hop-wtr",
    "C098PG5K6P3":"fermat-x-little-saints","C092VNA8RHU":"fermat-x-flavcity",
    "C08SNU8SHB6":"havn-x-fermat","C05Q4HDFRDE":"fermat-x-moment",
    "C08271XLYVC":"fermat-x-henry-rose","C07UG9JPS3A":"fermat-x-veracitywellness",
    "C07PRNWRZ9Q":"fermat-x-sole-toscana","C06SF766JBC":"fermat-x-de-soi",
    "C06PNPHF2E9":"fermat-x-gains-in-bulk"
}

META = {
    "35845b70-d5ef-4dbf-83cf-e9f327662c17":{"n":"Medik8","v":"Personal Care","t":"lmm","arr":24000,"ren":"","sl":"C0AK2MN11H7","ch":False,"cm":""},
    "508e7756-81aa-48b1-bbf5-765d2e8f1eb9":{"n":"Westmore Beauty","v":"Beauty","t":"lmm","arr":36000,"ren":"2027-02-14","sl":"C0ACP5J50H2","ch":False,"cm":""},
    "ae4f1f5d-f1d1-488f-8340-1890cfd0faf3":{"n":"MOTHER \u2738 ROOT","v":"Food & Beverage","t":"lmm","arr":36000,"ren":"2026-11-23","sl":"C09THN58W59","ch":False,"cm":"Brand has requested to cancel/wind down."},
    "39f04705-e991-461e-a98f-2dd3f29d6e47":{"n":"belliwelli","v":"Health & Supplements","t":"lmm","arr":24000,"ren":"2026-11-23","sl":"C0A99HSHTCL","ch":False,"cm":""},
    "ab6fc1e8-f245-4344-902c-b60388575aca":{"n":"FOND Regenerative","v":"Food & Beverage","t":"lmm","arr":24000,"ren":"2026-09-22","sl":"C09GBN46A68","ch":False,"cm":""},
    "74128082-bd6b-4435-94a5-7a7fdfa41726":{"n":"HOP WTR","v":"Food & Beverage","t":"lmm","arr":12000,"ren":"2026-03-07","sl":"C09BYRY8PE2","ch":True,"cm":"Churned 2026-03-06"},
    "8be8e4b7-d7c1-4922-b8e3-271671ee1592":{"n":"Little Saints","v":"Food & Beverage","t":"lmm","arr":18000,"ren":"2026-05-03","sl":"C098PG5K6P3","ch":False,"cm":""},
    "737444a0-c397-46a8-a53f-8b32d07a1722":{"n":"Shop FlavCity","v":"Health & Supplements","t":"lmm","arr":24000,"ren":"","sl":"C092VNA8RHU","ch":False,"cm":""},
    "1e7aa370-3cde-40bf-90d9-8ce8a3aaed30":{"n":"HAVN","v":"Consumer Goods","t":"lmm","arr":9000,"ren":"2026-02-26","sl":"C08SNU8SHB6","ch":False,"cm":"Brand is churning"},
    "f0a1a21b-3832-4bfd-ad3d-af38d11a90e8":{"n":"Moment","v":"Food & Beverage","t":"lmm","arr":9000,"ren":"2026-02-20","sl":"C05Q4HDFRDE","ch":False,"cm":""},
    "f7983632-4d4b-49c8-8e7a-192e9e999dff":{"n":"Henry Rose","v":"Fashion & Apparel","t":"lmm","arr":28800,"ren":"2026-08-29","sl":"C08271XLYVC","ch":False,"cm":""},
    "f8f83f9d-be9e-4177-ad7e-292ed079eafd":{"n":"Veracity Selfcare","v":"Health & Supplements","t":"lmm","arr":28800,"ren":"2026-10-30","sl":"C07UG9JPS3A","ch":False,"cm":""},
    "c686cb26-9441-4aa2-883e-7204999f2bc4":{"n":"Sole Toscana","v":"Personal Care","t":"lmm","arr":16800,"ren":"2026-06-30","sl":"C07PRNWRZ9Q","ch":False,"cm":""},
    "8fd93118-a246-431e-aebf-4aa362622342":{"n":"De Soi","v":"Food & Beverage","t":"lmm","arr":12000,"ren":"2026-03-31","sl":"C06SF766JBC","ch":False,"cm":""},
    "5cc7fc09-8acf-4af0-892f-735c6686c2a2":{"n":"Gains In Bulk","v":"Health & Supplements","t":"lmm","arr":36000,"ren":"2026-09-30","sl":"C06PNPHF2E9","ch":False,"cm":"Brand is churning (non-payment)"},
}

def e(s): return H.escape(str(s)) if s else ""

def dc(bid,d):
    m=META.get(bid,{})
    if m.get("ch"): return "red"
    if "churn" in m.get("cm","").lower(): return "yellow"
    s=d.get("health",{}).get("score")
    if s is not None: return "green" if s>=70 else "yellow" if s>=40 else "red"
    return "gray"

# ════════════════════════════════════════════════════════
# CSS — Visual Dashboard Design System
# ════════════════════════════════════════════════════════
CSS = """
:root{--bk:#0A0A0A;--wh:#FFFFFF;--fo:#072C1B;--sa:#DBE9E0;--mi:#9E9E9E;--ln:rgba(0,0,0,0.06);--bg:#F4F3F0;--gr:#3ED660;--gd:#B89240;--rd:#C84632;--bl:#2563EB;--pp:#9B59B6;--r:14px;--rl:20px;--sh:0 1px 3px rgba(0,0,0,0.04),0 4px 20px rgba(0,0,0,0.06);--shh:0 8px 40px rgba(0,0,0,0.12)}
*{box-sizing:border-box;margin:0;padding:0}
body{font-family:'Space Grotesk',sans-serif;background:var(--bg);color:var(--bk);-webkit-font-smoothing:antialiased;display:flex;min-height:100vh}
::-webkit-scrollbar{width:6px;height:6px}::-webkit-scrollbar-track{background:transparent}::-webkit-scrollbar-thumb{background:rgba(0,0,0,0.1);border-radius:99px}

/* Sidebar */
.sb{width:280px;min-width:280px;background:var(--fo);display:flex;flex-direction:column;height:100vh;position:sticky;top:0;z-index:100}
.sbh{padding:28px 24px 22px;border-bottom:1px solid rgba(219,233,224,0.08)}
.sbl{height:24px;filter:brightness(0) invert(1);opacity:.92}
.sbs{font-size:9.5px;color:rgba(219,233,224,0.35);margin-top:8px;text-transform:uppercase;letter-spacing:2px;font-weight:600}
.sbx{padding:16px 16px 8px}
.sbi{width:100%;padding:10px 14px;background:rgba(255,255,255,0.05);border:1px solid rgba(255,255,255,0.08);border-radius:10px;color:#fff;font-size:13px;font-family:inherit;outline:none;transition:all .2s}
.sbi:focus{background:rgba(255,255,255,0.08);border-color:rgba(62,214,96,0.35);box-shadow:0 0 0 3px rgba(62,214,96,0.08)}.sbi::placeholder{color:rgba(255,255,255,0.25)}
.bls{flex:1;overflow-y:auto;padding:8px 10px}
.bi{display:flex;align-items:center;gap:11px;padding:10px 12px;border-radius:12px;cursor:pointer;margin-bottom:1px;border:1px solid transparent;transition:all .15s}
.bi:hover{background:rgba(255,255,255,0.04)}.bi.active{background:rgba(62,214,96,0.06);border-color:rgba(62,214,96,0.12)}
.bi.active .bin{color:#fff}
.bl{width:32px;height:32px;border-radius:8px;object-fit:contain;background:#fff;padding:4px;flex-shrink:0;box-shadow:0 1px 4px rgba(0,0,0,0.15)}
.bii{flex:1;overflow:hidden}.bin{font-size:13px;font-weight:500;color:rgba(255,255,255,0.75);white-space:nowrap;overflow:hidden;text-overflow:ellipsis;transition:color .15s}.bim{font-size:10px;color:rgba(255,255,255,0.28);margin-top:2px;font-weight:400}
.bd{width:8px;height:8px;border-radius:50%;flex-shrink:0}.bd.green{background:#3ED660;box-shadow:0 0 6px rgba(62,214,96,0.4)}.bd.yellow{background:#EAB308;box-shadow:0 0 6px rgba(234,179,8,0.3)}.bd.red{background:#C84632;box-shadow:0 0 6px rgba(200,70,50,0.3)}.bd.gray{background:rgba(255,255,255,0.15)}
.sbf{padding:20px 24px;border-top:1px solid rgba(219,233,224,0.08)}.sbft{font-size:11px;color:rgba(255,255,255,0.5);font-weight:500}.sbfr{font-size:10px;color:rgba(255,255,255,0.2);margin-top:4px}

/* Main */
.mn{flex:1;display:flex;flex-direction:column;overflow:hidden;min-width:0}

/* Header */
.hdr{display:flex;align-items:center;justify-content:space-between;padding:18px 48px;background:var(--wh);border-bottom:1px solid var(--ln);position:sticky;top:0;z-index:50;backdrop-filter:blur(12px)}
.hdr-l{display:flex;align-items:center;gap:18px}.hdr-logos{display:flex;align-items:center;gap:16px}
.hdr-fl{height:20px;opacity:.85}.hdr-sep{width:1px;height:24px;background:rgba(0,0,0,0.08)}.hdr-bl{height:32px;max-width:120px;object-fit:contain}
.hdr-n{font-family:'Cormorant Garamond',serif;font-size:28px;font-weight:500;letter-spacing:-0.5px}
.hdr-v{font-size:11.5px;color:var(--mi);margin-top:2px;font-weight:400}
.hdr-r{display:flex;gap:28px;align-items:center}
.hdr-ri{text-align:right}.hdr-rl{font-size:9px;font-weight:700;letter-spacing:.12em;text-transform:uppercase;color:rgba(0,0,0,0.3)}.hdr-rv{font-size:13px;font-weight:600;margin-top:3px;color:var(--bk)}
.hdr-rv a{color:var(--fo);text-decoration:none;border-bottom:1px dashed rgba(7,44,27,0.25)}.hdr-rv a:hover{border-bottom-style:solid}
.badges{display:flex;gap:7px}.badge{padding:4px 12px;border-radius:100px;font-size:9.5px;font-weight:700;text-transform:uppercase;letter-spacing:.06em}
.badge.g{background:rgba(62,214,96,0.07);color:#1a8a3e;border:1px solid rgba(62,214,96,0.18)}
.badge.r{background:rgba(200,70,50,0.06);color:#C84632;border:1px solid rgba(200,70,50,0.12)}
.badge.a{background:rgba(7,44,27,0.04);color:var(--fo);border:1px solid rgba(7,44,27,0.08)}

/* Tabs */
.tabs{display:flex;padding:0 48px;background:var(--wh);border-bottom:1px solid var(--ln);overflow-x:auto;gap:4px}
.tab{padding:14px 18px;border:none;background:none;border-bottom:2.5px solid transparent;color:var(--mi);font-size:12.5px;font-weight:600;font-family:inherit;cursor:pointer;white-space:nowrap;transition:all .15s;letter-spacing:.01em}
.tab:hover{color:var(--bk)}.tab.active{color:var(--fo);border-bottom-color:var(--fo)}

/* Content */
.ct{flex:1;overflow-y:auto;padding:40px 48px 100px}
.tp{display:none}.tp.active{display:block}

/* Section headers */
.sh{display:flex;align-items:center;gap:12px;margin:44px 0 18px}.sh:first-child{margin-top:0}
.sh h2{font-size:10px;font-weight:700;letter-spacing:.16em;text-transform:uppercase;color:rgba(0,0,0,0.3);white-space:nowrap}
.sh::after{content:'';flex:1;height:1px;background:var(--ln)}

/* Overview summary cards */
.overview-summary{display:grid;grid-template-columns:repeat(5,1fr);gap:14px;margin-bottom:24px}
@media(max-width:1200px){.overview-summary{grid-template-columns:repeat(3,1fr)}}
.os-card{background:var(--wh);border-radius:var(--rl);padding:24px 20px;text-align:center;box-shadow:var(--sh);border:1px solid rgba(0,0,0,0.03);position:relative;overflow:hidden;transition:transform .2s}
.os-card:hover{transform:translateY(-2px)}
.os-card::before{content:'';position:absolute;top:0;left:0;right:0;height:3px;background:var(--fo)}
.os-card.os-warn::before{background:#EAB308}.os-card.os-red::before{background:var(--rd)}
.os-icon{font-size:20px;margin-bottom:8px}
.os-val{font-size:28px;font-weight:800;letter-spacing:-.03em;color:var(--bk)}
.os-card.os-warn .os-val{color:#92700c}.os-card.os-red .os-val{color:var(--rd)}
.os-lbl{font-size:9px;font-weight:700;letter-spacing:.12em;text-transform:uppercase;color:rgba(0,0,0,0.3);margin-top:6px}

/* Overview charts row */
.overview-charts{display:grid;grid-template-columns:1.2fr 0.8fr;gap:16px;margin-bottom:24px}
@media(max-width:1000px){.overview-charts{grid-template-columns:1fr}}

/* Chart cards — MUST have explicit height to prevent Chart.js infinite stretch */
.chart-card{background:var(--wh);border-radius:var(--rl);padding:24px 28px;box-shadow:var(--sh);border:1px solid rgba(0,0,0,0.03)}
.chart-card canvas{max-height:260px}
.chart-title{font-size:10px;font-weight:700;text-transform:uppercase;letter-spacing:.12em;color:rgba(0,0,0,0.3);margin-bottom:16px}
.chart-wrap{position:relative;height:260px;width:100%}

/* Brand grid (overview) */
.brand-grid{display:grid;grid-template-columns:repeat(3,1fr);gap:16px}
@media(max-width:1200px){.brand-grid{grid-template-columns:repeat(2,1fr)}}
@media(max-width:800px){.brand-grid{grid-template-columns:1fr}}
.bg-card{background:var(--wh);border-radius:var(--rl);padding:22px 24px;cursor:pointer;transition:all .25s;border:1px solid rgba(0,0,0,0.04);position:relative;overflow:hidden}
.bg-card:hover{transform:translateY(-4px);box-shadow:var(--shh);border-color:rgba(7,44,27,0.1)}
.bg-card::after{content:'';position:absolute;top:0;left:0;right:0;height:3px;background:var(--fo);opacity:0;transition:opacity .2s}
.bg-card:hover::after{opacity:1}
.bg-top{display:flex;align-items:center;justify-content:space-between;margin-bottom:14px}
.bg-logo-wrap{display:flex;align-items:center}
.bg-logo{height:32px;max-width:80px;object-fit:contain}
.bg-logo-fallback{width:36px;height:36px;border-radius:10px;display:flex;align-items:center;justify-content:center;font-size:12px;font-weight:700;color:#fff;background:var(--fo)}
.bg-name{font-size:15px;font-weight:600;letter-spacing:-.02em;margin-bottom:3px}
.bg-meta{font-size:11px;color:var(--mi);margin-bottom:14px}
.bg-kpis{display:flex;gap:10px;margin-bottom:14px}
.bg-kpi{flex:1;background:var(--bg);border-radius:10px;padding:10px 12px}
.bg-kl{font-size:8px;text-transform:uppercase;letter-spacing:.1em;color:rgba(0,0,0,0.3);display:block;font-weight:700}
.bg-kv{font-size:14px;font-weight:700;display:block;margin-top:3px;letter-spacing:-.02em}
.bg-spark{margin-bottom:12px;height:28px}
.bg-footer{display:flex;align-items:center;justify-content:space-between}
.bg-status{font-size:9px;font-weight:700;text-transform:uppercase;padding:3px 10px;border-radius:100px;letter-spacing:.04em}
.bg-active{background:rgba(62,214,96,0.08);color:#1a8a3e}
.bg-at-risk{background:rgba(234,179,8,0.08);color:#92700c}
.bg-churned{background:rgba(200,70,50,0.06);color:var(--rd)}
.bg-renewal{font-size:10px;color:var(--mi)}
.bg-alerts{position:absolute;top:12px;right:12px;font-size:9px;font-weight:700;color:var(--rd);background:rgba(200,70,50,0.06);padding:2px 8px;border-radius:100px}

/* KPI Grid */
.kpi-grid{display:grid;grid-template-columns:repeat(5,1fr);gap:14px;margin-bottom:20px}
@media(max-width:1100px){.kpi-grid{grid-template-columns:repeat(3,1fr)}}
.kpi{background:var(--wh);border-radius:var(--r);padding:22px 20px 16px;box-shadow:var(--sh);position:relative;overflow:hidden;transition:transform .2s,box-shadow .2s;border:1px solid rgba(0,0,0,0.03)}
.kpi:hover{transform:translateY(-3px);box-shadow:var(--shh)}
.kpi-accent{position:absolute;top:0;left:0;right:0;height:3px}
.kpi-name{font-size:9.5px;font-weight:700;letter-spacing:.12em;text-transform:uppercase;color:rgba(0,0,0,0.32);margin-bottom:10px}
.kpi-val{font-size:28px;font-weight:700;letter-spacing:-.03em;line-height:1;color:var(--bk)}
.kpi-spark{margin-top:10px;height:20px}

/* Performance charts */
.perf-charts{display:grid;grid-template-columns:1fr 1fr;gap:16px;margin-bottom:20px}
.perf-charts .chart-card{min-height:0}
@media(max-width:1000px){.perf-charts{grid-template-columns:1fr}}

/* Health Hero */
.health-hero{display:grid;grid-template-columns:200px 1fr;gap:36px;background:var(--wh);border-radius:var(--rl);padding:36px 40px;box-shadow:var(--sh);margin-bottom:24px;align-items:start;border:1px solid rgba(0,0,0,0.03)}
@media(max-width:900px){.health-hero{grid-template-columns:1fr;justify-items:center;text-align:center}}
.hh-left{display:flex;flex-direction:column;align-items:center}
.hh-ring{position:relative;width:180px;height:180px}
.hh-ring svg{display:block;filter:drop-shadow(0 2px 8px rgba(0,0,0,0.06))}
.hh-score-wrap{position:absolute;top:50%;left:50%;transform:translate(-50%,-50%);text-align:center}
.hh-score{font-size:48px;font-weight:800;letter-spacing:-2.5px;line-height:1}
.hh-label{font-size:9px;font-weight:700;letter-spacing:.15em;text-transform:uppercase;color:var(--mi);margin-top:2px}
.hh-status{margin-top:14px;padding:5px 18px;border-radius:100px;font-size:10px;font-weight:700;letter-spacing:.04em}
.hh-right{flex:1}
.hh-kpis{display:grid;grid-template-columns:repeat(2,1fr);gap:12px;margin-bottom:20px}
@media(min-width:1100px){.hh-kpis{grid-template-columns:repeat(4,1fr)}}
.hh-kpi{padding:16px 18px;background:var(--bg);border-radius:var(--r);border:1px solid rgba(0,0,0,0.04)}
.hh-kl{font-size:9px;font-weight:700;letter-spacing:.12em;text-transform:uppercase;color:rgba(0,0,0,0.3);margin-bottom:6px}
.hh-kv{font-size:20px;font-weight:700;letter-spacing:-.025em}

/* Signal Timeline */
.signal-timeline{position:relative;padding-left:32px}
.signal-timeline::before{content:'';position:absolute;left:8px;top:8px;bottom:8px;width:2px;background:linear-gradient(to bottom,rgba(0,0,0,0.08),rgba(0,0,0,0.02))}
.st-item{position:relative;margin-bottom:16px;display:flex;align-items:flex-start;gap:16px}
.st-dot{position:absolute;left:-28px;top:6px;width:12px;height:12px;border-radius:50%;border:2px solid var(--wh);box-shadow:0 1px 4px rgba(0,0,0,0.1);flex-shrink:0}
.st-green{background:#3ED660}.st-red{background:#C84632}.st-yellow{background:#EAB308}.st-neutral{background:var(--mi)}
.st-content{background:var(--wh);border-radius:var(--r);padding:14px 18px;box-shadow:0 1px 3px rgba(0,0,0,0.04);border:1px solid rgba(0,0,0,0.04);flex:1;transition:transform .15s}
.st-content:hover{transform:translateX(4px)}
.st-time{font-size:10px;font-weight:600;color:var(--mi);text-transform:uppercase;letter-spacing:.05em;margin-bottom:4px}
.st-text{font-size:12.5px;color:#3a3a3a;line-height:1.55}

/* Call Timeline */
.timeline{position:relative;padding-left:32px}
.timeline::before{content:'';position:absolute;left:8px;top:4px;bottom:4px;width:2px;background:linear-gradient(to bottom,var(--fo),rgba(7,44,27,0.1))}
.tl-item{position:relative;margin-bottom:28px}
.tl-dot{position:absolute;left:-28px;top:6px;width:12px;height:12px;border-radius:50%;background:var(--fo);border:2px solid var(--wh);box-shadow:0 1px 4px rgba(0,0,0,0.15)}
.tl-date{font-size:10px;font-weight:700;color:var(--mi);text-transform:uppercase;letter-spacing:.06em;margin-bottom:8px}
.tl-card{background:var(--wh);border-radius:var(--rl);padding:20px 24px;box-shadow:var(--sh);border:1px solid rgba(0,0,0,0.04);transition:transform .15s}
.tl-card:hover{transform:translateX(4px)}
.tl-header{display:flex;justify-content:space-between;align-items:flex-start;margin-bottom:4px}
.tl-title{font-size:15px;font-weight:600;letter-spacing:-.02em}
.tl-source{font-size:9px;font-weight:700;text-transform:uppercase;letter-spacing:.06em;color:var(--mi);background:var(--bg);padding:3px 8px;border-radius:6px}
.tl-meta{font-size:11.5px;color:var(--mi);margin-bottom:10px}
.tl-meta a{color:var(--fo);text-decoration:none;font-weight:600}
.tl-summary{font-size:12.5px;color:#3a3a3a;line-height:1.6}
.tl-actions{margin-top:12px;display:flex;flex-direction:column;gap:6px;padding:12px 14px;background:rgba(7,44,27,0.02);border-radius:10px;border:1px solid rgba(7,44,27,0.06)}
.tl-actions-title{font-size:9px;font-weight:700;text-transform:uppercase;letter-spacing:.1em;color:var(--fo);margin-bottom:6px}
.tl-action{font-size:11.5px;color:#3a3a3a;padding:3px 0;display:flex;align-items:flex-start;gap:8px;line-height:1.4}
.tl-action-dot{width:6px;height:6px;border-radius:50%;background:var(--gr);flex-shrink:0;margin-top:5px}

/* Chat bubbles (Slack) */
.chat-container{display:flex;flex-direction:column;gap:14px;max-width:700px}
.chat-msg{display:flex;gap:12px;align-items:flex-start}
.chat-avatar{width:36px;height:36px;border-radius:10px;display:flex;align-items:center;justify-content:center;font-size:11px;font-weight:700;color:white;flex-shrink:0}
.chat-bubble{background:var(--wh);border-radius:4px 16px 16px 16px;padding:14px 18px;box-shadow:0 1px 3px rgba(0,0,0,0.04);border:1px solid rgba(0,0,0,0.04);flex:1;max-width:600px;transition:transform .1s}
.chat-bubble:hover{transform:translateX(2px)}
.chat-name{font-size:12px;font-weight:700;color:var(--fo);margin-bottom:4px}
.chat-text{font-size:12.5px;color:#3a3a3a;line-height:1.6}
.chat-time{font-size:9px;color:var(--mi);margin-top:6px}

/* Email inbox */
.email-list{display:flex;flex-direction:column;gap:8px}
.email-item{display:flex;gap:14px;align-items:flex-start;background:var(--wh);border-radius:var(--r);padding:16px 20px;box-shadow:0 1px 2px rgba(0,0,0,0.03);border:1px solid rgba(0,0,0,0.04);cursor:default;transition:all .15s}
.email-item:hover{transform:translateX(4px);box-shadow:var(--sh)}
.email-avatar{width:36px;height:36px;border-radius:10px;display:flex;align-items:center;justify-content:center;font-size:11px;font-weight:700;color:white;flex-shrink:0}
.email-content{flex:1;min-width:0}
.email-header{display:flex;justify-content:space-between;align-items:center;margin-bottom:4px}
.email-from{font-size:13px;font-weight:600;color:var(--bk);white-space:nowrap;overflow:hidden;text-overflow:ellipsis}
.email-date{font-size:10px;color:var(--mi);flex-shrink:0;margin-left:12px}
.email-subject{font-size:12.5px;font-weight:500;color:var(--fo);margin-bottom:4px;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}
.email-snippet{font-size:11.5px;color:var(--mi);line-height:1.5;display:-webkit-box;-webkit-line-clamp:2;-webkit-box-orient:vertical;overflow:hidden}

/* Calendar */
.cal-list{display:flex;flex-direction:column;gap:6px}
.cal-item{display:flex;align-items:center;gap:16px;padding:14px 20px;background:var(--wh);border-radius:var(--r);box-shadow:0 1px 2px rgba(0,0,0,0.03);border:1px solid rgba(0,0,0,0.04);transition:transform .15s}
.cal-item:hover{transform:translateX(4px)}
.cal-upcoming{border-left:3px solid var(--fo)}
.cal-past{border-left:3px solid var(--mi);opacity:0.6}
.cal-dot{width:8px;height:8px;border-radius:50%;flex-shrink:0}
.cal-upcoming .cal-dot{background:var(--fo)}.cal-past .cal-dot{background:var(--mi)}
.cal-time{font-family:'JetBrains Mono','SF Mono',monospace;font-size:11px;color:var(--mi);min-width:130px;flex-shrink:0}
.cal-title{font-size:13px;font-weight:600}

/* Insights */
.insight-inline{display:flex;align-items:flex-start;gap:12px;background:rgba(7,44,27,0.035);border:1px solid rgba(7,44,27,0.08);border-radius:var(--r);padding:14px 16px;margin-top:14px}
.ii-icon{font-size:17px;flex-shrink:0;line-height:1.35;opacity:.8}.ii-text{font-size:12.5px;color:#3a3a3a;line-height:1.6}.ii-text strong{color:var(--fo);font-weight:700}
.insight-inline.gold{background:rgba(184,146,64,0.04);border-color:rgba(184,146,64,0.14)}
.insight-inline.alert{background:rgba(200,70,50,0.035);border-color:rgba(200,70,50,0.1)}

/* 30d Summary Banner */
.summary{background:var(--fo);border-radius:var(--rl);padding:36px 40px;color:#fff;display:flex;align-items:center;justify-content:space-between;gap:32px;flex-wrap:wrap;box-shadow:0 12px 48px rgba(7,44,27,0.25);position:relative;overflow:hidden;margin-top:24px}
.summary::before{content:'';position:absolute;inset:0;background:radial-gradient(ellipse 80% 120% at 100% -30%,rgba(219,233,224,0.1) 0%,transparent 55%),radial-gradient(ellipse 50% 80% at -10% 120%,rgba(184,146,64,0.06) 0%,transparent 50%);pointer-events:none}
.summary-text h3{font-family:'Cormorant Garamond',serif;font-weight:400;font-size:28px;line-height:1.2;margin-bottom:8px;position:relative}
.summary-text p{font-size:13px;color:rgba(255,255,255,0.5);max-width:400px;line-height:1.6;position:relative}
.s-stats{display:flex;gap:40px;flex-wrap:wrap;position:relative}.s-stat{text-align:center}
.s-val{font-size:32px;font-weight:700;letter-spacing:-.03em;display:block}.s-lbl{font-size:9px;font-weight:700;letter-spacing:.12em;text-transform:uppercase;color:rgba(255,255,255,0.32);margin-top:4px}

/* Empty state */
.empty-card{padding:56px 40px;text-align:center;background:var(--wh);border-radius:var(--rl);box-shadow:var(--sh);color:var(--mi);font-size:14px;border:1px solid rgba(0,0,0,0.03)}

/* Date range selector */
.range-bar{display:flex;align-items:center;gap:12px;margin-bottom:20px;flex-wrap:wrap}
.range-btn{padding:8px 18px;border:1px solid rgba(0,0,0,0.08);border-radius:100px;font-size:12px;font-weight:600;font-family:inherit;cursor:pointer;background:var(--wh);color:var(--mi);transition:all .15s;letter-spacing:.01em}
.range-btn:hover{border-color:rgba(7,44,27,0.2);color:var(--bk)}
.range-btn.active{background:var(--fo);color:#fff;border-color:var(--fo)}

/* Funnel visualization */
.funnel-card{background:var(--wh);border-radius:var(--rl);padding:28px;box-shadow:var(--sh);border:1px solid rgba(0,0,0,0.03)}
.funnel-stages{display:grid;grid-template-columns:repeat(5,1fr);gap:0;margin-top:16px}
.funnel-stage{padding:0 10px;position:relative}
.funnel-stage-num{font-size:24px;font-weight:700;letter-spacing:-.02em;color:var(--bk);line-height:1}
.funnel-stage-pct{display:inline-block;font-size:10px;font-weight:700;color:var(--mi);background:rgba(0,0,0,0.05);border-radius:100px;padding:2px 8px;margin-left:6px;vertical-align:middle}
.funnel-stage-name{font-size:12px;font-weight:500;color:var(--mi);margin-top:4px}
.funnel-bar{height:8px;border-radius:4px;margin-top:8px;transition:width .6s ease}

/* Animations */
@keyframes fadeIn{from{opacity:0;transform:translateY(8px)}to{opacity:1;transform:translateY(0)}}
.tp.active{animation:fadeIn .3s ease}
"""

# ════════════════════════════════════════════════════════
# JavaScript — Dynamic rendering + Chart.js
# ════════════════════════════════════════════════════════
JS_TEMPLATE = """
const BD = __BRAND_DATA__;
const M = __META__;
const L = __LOGOS__;
const SL = __SLACKS__;

let cur = null;
let curTab = 'overview';
let charts = {};

// ===== HELPERS =====
function esc(s) { if (!s) return ''; const d = document.createElement('div'); d.textContent = String(s); return d.innerHTML; }
function fc(v) { return v != null && v !== 0 ? '$' + Number(v).toLocaleString(undefined, {maximumFractionDigits: 0}) : '--'; }
function fp(v) { return v != null && v !== 0 ? Number(v).toFixed(2) + '%' : '--'; }
function fn(v) { return v != null && v !== 0 ? Number(v).toLocaleString() : '--'; }
function sc(s) { return s >= 70 ? '#1a8a3e' : s >= 40 ? '#92700c' : '#C84632'; }
function scBg(s) { return s >= 70 ? 'rgba(62,214,96,0.1)' : s >= 40 ? 'rgba(184,146,64,0.08)' : 'rgba(200,70,50,0.08)'; }
function scLbl(s) { return s >= 70 ? 'Healthy' : s >= 40 ? 'Needs Attention' : 'Critical'; }
function initials(n) { return (n||'').replace(/[^a-zA-Z0-9 ]/g, '').split(' ').filter(Boolean).map(w => w[0]).join('').substring(0, 2).toUpperCase(); }

const avColors = ['#072C1B','#2563EB','#9B59B6','#B89240','#C84632','#1a8a3e','#E67E22','#16A085'];
function avColor(n) { let h = 0; for (let i = 0; i < (n||'').length; i++) h = n.charCodeAt(i) + ((h << 5) - h); return avColors[Math.abs(h) % avColors.length]; }

function miniRing(score, size, stroke) {
  size = size || 48; stroke = stroke || 4;
  const r = (size - stroke) / 2, circ = 2 * Math.PI * r, off = circ - (score / 100) * circ, c = sc(score);
  return '<svg width="'+size+'" height="'+size+'" viewBox="0 0 '+size+' '+size+'">' +
    '<circle cx="'+(size/2)+'" cy="'+(size/2)+'" r="'+r+'" fill="none" stroke="rgba(0,0,0,0.06)" stroke-width="'+stroke+'"/>' +
    '<circle cx="'+(size/2)+'" cy="'+(size/2)+'" r="'+r+'" fill="none" stroke="'+c+'" stroke-width="'+stroke+'" stroke-linecap="round" stroke-dasharray="'+circ.toFixed(1)+'" stroke-dashoffset="'+off.toFixed(1)+'" transform="rotate(-90 '+(size/2)+' '+(size/2)+')" style="transition:stroke-dashoffset .8s"/>' +
    '<text x="'+(size/2)+'" y="'+(size/2)+'" text-anchor="middle" dominant-baseline="central" font-size="'+(size > 44 ? 13 : 10)+'" font-weight="700" font-family="Space Grotesk,sans-serif" fill="'+c+'">'+score+'</text></svg>';
}

function sparkline(values, w, h, color) {
  w = w || 80; h = h || 24; color = color || '#3ED660';
  if (!values || values.length < 2 || values.every(function(v){return v===0})) return '';
  var mn = Math.min.apply(null, values), mx = Math.max.apply(null, values), rng = mx - mn || 1;
  var pts = values.map(function(v, i) {
    var x = (i / (values.length - 1)) * w;
    var y = h - ((v - mn) / rng) * (h - 4) - 2;
    return x.toFixed(1) + ',' + y.toFixed(1);
  });
  var area = '0,' + h + ' ' + pts.join(' ') + ' ' + w + ',' + h;
  var lastPt = pts[pts.length - 1].split(',');
  return '<svg width="'+w+'" height="'+h+'" viewBox="0 0 '+w+' '+h+'" style="display:block">' +
    '<polygon points="'+area+'" fill="'+color+'" opacity="0.1"/>' +
    '<polyline points="'+pts.join(' ')+'" fill="none" stroke="'+color+'" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>' +
    '<circle cx="'+lastPt[0]+'" cy="'+lastPt[1]+'" r="2.5" fill="'+color+'"/></svg>';
}

function destroyCharts() { Object.keys(charts).forEach(function(k) { try { charts[k].destroy(); } catch(e) {} }); charts = {}; }

// ===== INIT =====
document.addEventListener('DOMContentLoaded', function() {
  switchTab('overview');
  renderOverview();
  var first = document.querySelector('.bi');
  if (first) { cur = first.dataset.bid; first.classList.add('active'); }
  // Monday popup check (after short delay so page is fully rendered)
  setTimeout(function() { checkMondayPopup(); }, 800);
});

// ===== NAV =====
function sel(id) {
  cur = id;
  document.querySelectorAll('.bi').forEach(function(el) { el.classList.toggle('active', el.dataset.bid === id); });
  updateHeader();
  if (curTab === 'overview') switchTab('health');
  else renderTab(curTab);
}

function updateHeader() {
  var m = M[cur] || {};
  document.getElementById('hdrName').textContent = m.n || '';
  document.getElementById('hdrVert').textContent = (m.v || '') + ' \\u00b7 ' + (m.t || '').toUpperCase();
  var status = m.ch ? 'Churned' : ((m.cm || '').toLowerCase().indexOf('churn') >= 0 ? 'At Risk' : 'Active');
  document.getElementById('hdrStatus').textContent = status + ' \\u00b7 $' + (m.arr || 0).toLocaleString() + ' ARR';
  document.getElementById('hdrRen').textContent = m.ren || 'Not set';
  var sn = SL[m.sl] || 'unknown';
  document.getElementById('hdrSlack').innerHTML = '<a href="https://app.slack.com/client/T/' + (m.sl||'') + '" target="_blank">#' + sn + '</a>';
}

function switchTab(tab) {
  curTab = tab;
  document.querySelectorAll('.tab').forEach(function(el) { el.classList.toggle('active', el.dataset.t === tab); });
  document.querySelectorAll('.tp').forEach(function(el) { el.style.display = 'none'; el.classList.remove('active'); });
  var panel = document.getElementById('tab-' + tab);
  if (panel) { panel.style.display = 'block'; panel.classList.add('active'); }
  if (tab === 'overview') {
    document.getElementById('overviewHdr').style.display = 'flex';
    document.getElementById('brandHdr').style.display = 'none';
    document.getElementById('tabBar').style.display = 'none';
    renderOverview();
  } else {
    document.getElementById('overviewHdr').style.display = 'none';
    document.getElementById('brandHdr').style.display = 'flex';
    document.getElementById('tabBar').style.display = 'flex';
    if (cur) updateHeader();
    renderTab(tab);
  }
}

function renderTab(tab) {
  if (!cur) return;
  var d = BD[cur] || {};
  var m = M[cur] || {};
  destroyCharts();
  if (tab === 'health') renderHealth(d, m);
  else if (tab === 'performance') renderPerformance(d, m);
  else if (tab === 'calls') renderCalls(d);
  else if (tab === 'calendar') renderCalendar(d);
  else if (tab === 'slack') renderSlack(d, m);
  else if (tab === 'email') renderEmail(d);
}

function filterBrands(q) {
  q = q.toLowerCase();
  document.querySelectorAll('.bi').forEach(function(el) { el.style.display = (!q || el.querySelector('.bin').textContent.toLowerCase().indexOf(q) >= 0) ? 'flex' : 'none'; });
}

// ===== OVERVIEW =====
function renderOverview() {
  var el = document.getElementById('overviewContent');
  if (!el) return;
  destroyCharts();
  var brands = Object.keys(M).sort(function(a,b) { return (M[a].n||'').localeCompare(M[b].n||''); });
  var totalARR = 0, active = 0, atRisk = 0, churned = 0, hSum = 0, hCnt = 0, totalRev30 = 0;
  var revData = [], healthData = [], brandNames = [];

  brands.forEach(function(id) {
    var m = M[id], d = BD[id] || {};
    totalARR += m.arr || 0;
    var hs = (d.health && d.health.score) || 0;
    var rev30 = (d.performance && d.performance['30d'] && d.performance['30d'].revenue) || 0;
    totalRev30 += rev30;
    if (m.ch) churned++; else if ((m.cm||'').toLowerCase().indexOf('churn') >= 0) atRisk++; else active++;
    if (hs > 0) { hSum += hs; hCnt++; }
    revData.push(rev30); healthData.push(hs); brandNames.push(m.n);
  });
  var avgH = hCnt ? Math.round(hSum / hCnt) : 0;

  var html = '<div class="overview-summary">' +
    '<div class="os-card"><div class="os-val">$' + totalARR.toLocaleString() + '</div><div class="os-lbl">Total ARR</div><div style="font-size:11px;color:var(--mi);margin-top:4px">$' + Math.round(totalARR/12).toLocaleString() + ' MRR</div></div>' +
    '<div class="os-card"><div class="os-val">$' + totalRev30.toLocaleString(undefined,{maximumFractionDigits:0}) + '</div><div class="os-lbl">30d Revenue</div></div>' +
    '<div class="os-card"><div class="os-val">' + active + '</div><div class="os-lbl">Active Brands</div></div>' +
    '<div class="os-card os-warn"><div class="os-val">' + atRisk + '</div><div class="os-lbl">At Risk</div></div>' +
    '<div class="os-card os-red"><div class="os-val">' + churned + '</div><div class="os-lbl">Churned</div></div>' +
    '</div>';

  html += '<div class="overview-charts">' +
    '<div class="chart-card"><div class="chart-title">30-Day Revenue by Brand</div><div class="chart-wrap"><canvas id="ovRevChart"></canvas></div></div>' +
    '<div class="chart-card"><div class="chart-title">Health Score Distribution</div><div class="chart-wrap"><canvas id="ovHealthChart"></canvas></div></div></div>';

  html += '<div class="sh"><h2>Brand Portfolio</h2></div><div class="brand-grid">';

  brands.forEach(function(id) {
    var m = M[id], d = BD[id] || {};
    var hs = (d.health && d.health.score) || 0;
    var rev30 = (d.performance && d.performance['30d'] && d.performance['30d'].revenue) || 0;
    var status = m.ch ? 'churned' : ((m.cm||'').toLowerCase().indexOf('churn') >= 0 ? 'at-risk' : 'active');
    var statusLabel = status === 'churned' ? 'Churned' : status === 'at-risk' ? 'At Risk' : 'Active';
    var logo = L[id];
    var periods = ['yesterday','3d','7d','15d','30d','45d'];
    var revVals = periods.map(function(p) { return (d.performance && d.performance[p] && d.performance[p].revenue) || 0; });
    var spark = sparkline(revVals, 120, 28, sc(hs));
    var negSigs = ((d.health && d.health.signals) || []).filter(function(s){return s.type==='negative'}).length;

    html += '<div class="bg-card" onclick="sel(\\'' + id + '\\')">' +
      '<div class="bg-top"><div class="bg-logo-wrap">' +
      (logo ? '<img src="' + logo + '" class="bg-logo" onerror="this.style.display=\\'none\\'">' : '<div class="bg-logo-fallback">' + initials(m.n) + '</div>') +
      '</div>' + miniRing(hs, 48, 4) + '</div>' +
      '<div class="bg-name">' + esc(m.n) + '</div>' +
      '<div class="bg-meta">' + esc(m.v) + '</div>' +
      '<div class="bg-kpis"><div class="bg-kpi"><span class="bg-kl">ARR</span><span class="bg-kv">$' + (m.arr||0).toLocaleString() + '</span></div>' +
      '<div class="bg-kpi"><span class="bg-kl">30d Rev</span><span class="bg-kv">' + (rev30 ? '$' + rev30.toLocaleString(undefined,{maximumFractionDigits:0}) : '--') + '</span></div></div>' +
      '<div class="bg-spark">' + spark + '</div>' +
      '<div class="bg-footer"><span class="bg-status bg-' + status + '">' + statusLabel + '</span>' +
      (m.ren ? '<span class="bg-renewal">Renews ' + m.ren + '</span>' : '') + '</div>' +
      (negSigs > 0 ? '<div class="bg-alerts">' + negSigs + ' alert' + (negSigs > 1 ? 's' : '') + '</div>' : '') +
      '</div>';
  });
  html += '</div>';
  el.innerHTML = html;

  setTimeout(function() {
    var revCtx = document.getElementById('ovRevChart');
    if (revCtx) {
      charts.ovRev = new Chart(revCtx, {
        type: 'bar',
        plugins: [ChartDataLabels],
        data: { labels: brandNames, datasets: [{
          data: revData,
          backgroundColor: revData.map(function(v,i) { var h = healthData[i]; return h >= 70 ? 'rgba(62,214,96,0.65)' : h >= 40 ? 'rgba(184,146,64,0.65)' : 'rgba(200,70,50,0.65)'; }),
          borderRadius: 6, borderSkipped: false
        }]},
        options: {
          responsive: true, maintainAspectRatio: false, layout: { padding: { top: 18 } },
          plugins: { legend: { display: false }, datalabels: { anchor: 'end', align: 'top', font: { size: 8, weight: 600, family: "'Space Grotesk'" }, color: '#072C1B', formatter: function(v) { return '$' + (v >= 1000 ? (v/1000).toFixed(0) + 'K' : Math.round(v)); } } },
          scales: {
            x: { grid: { display: false }, ticks: { font: { size: 9, family: "'Space Grotesk'" }, maxRotation: 45 } },
            y: { grid: { color: 'rgba(0,0,0,0.04)' }, ticks: { callback: function(v) { return '$' + (v >= 1000 ? (v/1000).toFixed(0) + 'K' : v); }, font: { size: 10 } } }
          }
        }
      });
    }
    var hCtx = document.getElementById('ovHealthChart');
    if (hCtx) {
      charts.ovHealth = new Chart(hCtx, {
        type: 'bar',
        plugins: [ChartDataLabels],
        data: { labels: brandNames, datasets: [{
          data: healthData,
          backgroundColor: healthData.map(function(h) { return h >= 70 ? 'rgba(62,214,96,0.65)' : h >= 40 ? 'rgba(184,146,64,0.65)' : 'rgba(200,70,50,0.65)'; }),
          borderRadius: 6, borderSkipped: false
        }]},
        options: {
          indexAxis: 'y', responsive: true, maintainAspectRatio: false,
          plugins: { legend: { display: false }, datalabels: { anchor: 'end', align: 'end', font: { size: 9, weight: 700, family: "'Space Grotesk'" }, color: function(ctx) { var v = ctx.dataset.data[ctx.dataIndex]; return v >= 70 ? '#1a8a3e' : v >= 40 ? '#92700c' : '#C84632'; }, formatter: function(v) { return v; } } },
          scales: {
            x: { max: 100, grid: { color: 'rgba(0,0,0,0.04)' }, ticks: { font: { size: 10 } } },
            y: { grid: { display: false }, ticks: { font: { size: 9, family: "'Space Grotesk'" } } }
          }
        }
      });
    }
  }, 150);
}

// ===== SENTIMENT HELPERS =====
var SENTIMENT = window.__SENTIMENT__ || {};

function getLatestSentiment(brandId) {
  var ratings = SENTIMENT[brandId];
  if (!ratings || !Array.isArray(ratings) || ratings.length === 0) return null;
  var latest = null;
  ratings.forEach(function(r) {
    if (r && r.score && (!latest || (r.date || '') > (latest.date || ''))) latest = r;
  });
  return latest;
}

function sentimentColor(score) {
  if (score >= 9) return '#3ED660';
  if (score >= 7) return '#EAB308';
  return '#C84632';
}

function sentimentLabel(score) {
  if (score >= 9) return 'Healthy';
  if (score >= 7) return 'Moderate';
  return 'Concerning';
}

function isPulkit() {
  var u = window.__PORTAL_USER__ || {};
  return u.email === 'pulkit@fermatcommerce.com';
}

// ===== RATE MODAL =====
function openRateModal(brandId) {
  var m = M[brandId] || {};
  var existing = getLatestSentiment(brandId);
  var startScore = existing ? existing.score : 7;
  var overlay = document.createElement('div');
  overlay.id = 'sentimentOverlay';
  overlay.style.cssText = 'position:fixed;inset:0;background:rgba(0,0,0,0.45);z-index:9999;display:flex;align-items:center;justify-content:center;animation:fadeIn .2s ease';

  var scoreButtons = '';
  for (var i = 1; i <= 10; i++) {
    var bg = i <= 6 ? 'rgba(200,70,50,0.12)' : i <= 8 ? 'rgba(234,179,8,0.12)' : 'rgba(62,214,96,0.12)';
    var col = i <= 6 ? '#C84632' : i <= 8 ? '#92700c' : '#1a8a3e';
    var selBg = i <= 6 ? '#C84632' : i <= 8 ? '#EAB308' : '#3ED660';
    scoreButtons += '<button class="sent-score-btn" data-score="' + i + '" style="width:36px;height:36px;border-radius:10px;border:2px solid transparent;background:' + bg + ';color:' + col + ';font-size:14px;font-weight:700;cursor:pointer;transition:all .15s;font-family:inherit" data-bg="' + bg + '" data-col="' + col + '" data-selbg="' + selBg + '">' + i + '</button>';
  }

  overlay.innerHTML = '<div style="background:#fff;border-radius:20px;width:520px;max-width:90vw;box-shadow:0 24px 80px rgba(0,0,0,0.25);overflow:hidden">' +
    '<div style="padding:24px 28px 0;display:flex;justify-content:space-between;align-items:center">' +
      '<div style="font-size:16px;font-weight:700;color:#072C1B">Rate Account: ' + esc(m.n || brandId) + '</div>' +
      '<button onclick="closeRateModal()" style="background:none;border:none;cursor:pointer;font-size:20px;color:#9E9E9E;padding:4px">&times;</button>' +
    '</div>' +
    '<div style="padding:20px 28px 28px">' +
      '<div style="font-size:13px;color:#3a3a3a;margin-bottom:14px">How do you feel about this account?</div>' +
      '<div style="display:flex;gap:6px;margin-bottom:12px" id="sentScoreBtns">' + scoreButtons + '</div>' +
      '<div id="sentScoreLabel" style="font-size:12px;font-weight:600;margin-bottom:18px;color:#9E9E9E">Selected: ' + startScore + '/10</div>' +
      '<div style="font-size:12px;font-weight:600;color:#072C1B;margin-bottom:8px">Comment</div>' +
      '<div style="position:relative">' +
        '<textarea id="sentComment" rows="3" style="width:100%;padding:12px 14px;border:1px solid rgba(0,0,0,0.1);border-radius:12px;font-size:13px;font-family:inherit;resize:vertical;outline:none;transition:border-color .2s" placeholder="Type your thoughts...">' + (existing ? esc(existing.comment || '') : '') + '</textarea>' +
      '</div>' +
      '<div style="margin-top:10px;margin-bottom:18px">' +
        '<button onclick="proofreadComment()" style="display:inline-flex;align-items:center;gap:6px;padding:7px 16px;background:rgba(155,89,182,0.08);color:#7B3FA0;border:1px solid rgba(155,89,182,0.2);border-radius:10px;font-size:11px;font-weight:600;cursor:pointer;font-family:inherit;transition:all .15s" onmouseover="this.style.background=\\'rgba(155,89,182,0.15)\\'" onmouseout="this.style.background=\\'rgba(155,89,182,0.08)\\'">' +
          '<span style="font-size:14px">&#10024;</span> AI Proofread</button>' +
      '</div>' +
      '<div style="display:flex;justify-content:flex-end;gap:10px">' +
        '<button onclick="closeRateModal()" style="padding:10px 24px;background:none;border:1px solid rgba(0,0,0,0.1);border-radius:12px;font-size:13px;font-weight:600;cursor:pointer;font-family:inherit;color:#9E9E9E">Cancel</button>' +
        '<button onclick="saveSentimentRating()" style="padding:10px 24px;background:#072C1B;color:#fff;border:none;border-radius:12px;font-size:13px;font-weight:600;cursor:pointer;font-family:inherit;box-shadow:0 2px 8px rgba(7,44,27,0.2)">Save Rating</button>' +
      '</div>' +
    '</div></div>';

  document.body.appendChild(overlay);
  overlay.addEventListener('click', function(e) { if (e.target === overlay) closeRateModal(); });

  // Set initial selection
  window.__sentBrandId = brandId;
  window.__sentScore = startScore;
  updateScoreSelection(startScore);

  // Wire up score buttons
  document.querySelectorAll('.sent-score-btn').forEach(function(btn) {
    btn.addEventListener('click', function() {
      var s = parseInt(this.dataset.score, 10);
      window.__sentScore = s;
      updateScoreSelection(s);
    });
  });
}

function updateScoreSelection(score) {
  document.querySelectorAll('.sent-score-btn').forEach(function(btn) {
    var s = parseInt(btn.dataset.score, 10);
    if (s === score) {
      btn.style.background = btn.dataset.selbg;
      btn.style.color = '#fff';
      btn.style.borderColor = btn.dataset.selbg;
      btn.style.transform = 'scale(1.12)';
      btn.style.boxShadow = '0 2px 8px rgba(0,0,0,0.15)';
    } else {
      btn.style.background = btn.dataset.bg;
      btn.style.color = btn.dataset.col;
      btn.style.borderColor = 'transparent';
      btn.style.transform = 'scale(1)';
      btn.style.boxShadow = 'none';
    }
  });
  var lbl = document.getElementById('sentScoreLabel');
  if (lbl) {
    var col = sentimentColor(score);
    lbl.innerHTML = 'Selected: <span style="color:' + col + ';font-weight:700">' + score + '/10</span> <span style="display:inline-block;width:8px;height:8px;border-radius:50%;background:' + col + ';vertical-align:middle;margin:0 4px"></span> ' + sentimentLabel(score);
  }
}

function closeRateModal() {
  var ov = document.getElementById('sentimentOverlay');
  if (ov) ov.remove();
}

function saveSentimentRating() {
  var brandId = window.__sentBrandId;
  var score = window.__sentScore;
  var comment = (document.getElementById('sentComment') || {}).value || '';

  fetch('/api/sentiment', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ brandId: brandId, score: score, comment: comment })
  }).then(function(r) { return r.json(); }).then(function(data) {
    if (data.success) {
      // Update local cache
      if (!SENTIMENT[brandId]) SENTIMENT[brandId] = [];
      SENTIMENT[brandId].unshift({ date: data.date, score: score, comment: comment });
      closeRateModal();
      // Re-render health tab
      renderTab('health');
    } else {
      alert('Failed to save: ' + (data.error || 'Unknown error'));
    }
  }).catch(function(e) { alert('Network error: ' + e.message); });
}

function proofreadComment() {
  var ta = document.getElementById('sentComment');
  if (!ta || !ta.value.trim()) return;
  var origText = ta.value;
  ta.value = 'Proofreading...';
  ta.disabled = true;

  fetch('/api/proofread', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ text: origText })
  }).then(function(r) { return r.json(); }).then(function(data) {
    ta.disabled = false;
    if (data.text) {
      ta.value = data.text;
    } else {
      ta.value = origText;
      alert('Proofread failed: ' + (data.error || 'Unknown error'));
    }
  }).catch(function(e) {
    ta.disabled = false;
    ta.value = origText;
    alert('Network error: ' + e.message);
  });
}

// ===== HISTORY MODAL =====
function openHistoryModal(brandId) {
  var m = M[brandId] || {};
  var ratings = (SENTIMENT[brandId] || []).slice().sort(function(a, b) {
    return (b.date || '').localeCompare(a.date || '');
  });

  var overlay = document.createElement('div');
  overlay.id = 'historyOverlay';
  overlay.style.cssText = 'position:fixed;inset:0;background:rgba(0,0,0,0.45);z-index:9999;display:flex;align-items:center;justify-content:center;animation:fadeIn .2s ease';

  var rows = '';
  if (ratings.length === 0) {
    rows = '<tr><td colspan="3" style="padding:20px;text-align:center;color:#9E9E9E;font-size:13px">No ratings yet</td></tr>';
  } else {
    ratings.forEach(function(r) {
      var dotColor = sentimentColor(r.score || 0);
      rows += '<tr>' +
        '<td style="padding:10px 14px;font-size:12px;color:#3a3a3a;border-bottom:1px solid rgba(0,0,0,0.04);white-space:nowrap">' + esc(r.date || '') + '</td>' +
        '<td style="padding:10px 14px;font-size:13px;font-weight:700;border-bottom:1px solid rgba(0,0,0,0.04)"><span style="display:inline-block;width:10px;height:10px;border-radius:50%;background:' + dotColor + ';margin-right:8px;vertical-align:middle"></span><span style="color:' + dotColor + '">' + (r.score || 0) + '/10</span></td>' +
        '<td style="padding:10px 14px;font-size:12px;color:#3a3a3a;border-bottom:1px solid rgba(0,0,0,0.04);line-height:1.5">' + esc(r.comment || '') + '</td>' +
        '</tr>';
    });
  }

  overlay.innerHTML = '<div style="background:#fff;border-radius:20px;width:640px;max-width:90vw;max-height:80vh;box-shadow:0 24px 80px rgba(0,0,0,0.25);overflow:hidden;display:flex;flex-direction:column">' +
    '<div style="padding:24px 28px 16px;display:flex;justify-content:space-between;align-items:center;border-bottom:1px solid rgba(0,0,0,0.06)">' +
      '<div style="font-size:16px;font-weight:700;color:#072C1B">Sentiment History: ' + esc(m.n || brandId) + '</div>' +
      '<button onclick="closeHistoryModal()" style="background:none;border:none;cursor:pointer;font-size:20px;color:#9E9E9E;padding:4px">&times;</button>' +
    '</div>' +
    '<div style="padding:16px 28px;display:flex;gap:12px;align-items:center;border-bottom:1px solid rgba(0,0,0,0.04)">' +
      '<label style="font-size:11px;font-weight:600;color:#9E9E9E">From:</label>' +
      '<input type="date" id="histFrom" style="padding:6px 10px;border:1px solid rgba(0,0,0,0.1);border-radius:8px;font-size:12px;font-family:inherit">' +
      '<label style="font-size:11px;font-weight:600;color:#9E9E9E">To:</label>' +
      '<input type="date" id="histTo" style="padding:6px 10px;border:1px solid rgba(0,0,0,0.1);border-radius:8px;font-size:12px;font-family:inherit">' +
      '<button onclick="filterHistory()" style="padding:6px 14px;background:#072C1B;color:#fff;border:none;border-radius:8px;font-size:11px;font-weight:600;cursor:pointer;font-family:inherit">Filter</button>' +
    '</div>' +
    '<div style="flex:1;overflow-y:auto;padding:0 28px 24px">' +
      '<table style="width:100%;border-collapse:collapse;margin-top:12px" id="historyTable">' +
        '<thead><tr>' +
          '<th style="padding:10px 14px;text-align:left;font-size:9px;font-weight:700;letter-spacing:.1em;text-transform:uppercase;color:rgba(0,0,0,0.3);border-bottom:2px solid rgba(0,0,0,0.06)">Date</th>' +
          '<th style="padding:10px 14px;text-align:left;font-size:9px;font-weight:700;letter-spacing:.1em;text-transform:uppercase;color:rgba(0,0,0,0.3);border-bottom:2px solid rgba(0,0,0,0.06)">Score</th>' +
          '<th style="padding:10px 14px;text-align:left;font-size:9px;font-weight:700;letter-spacing:.1em;text-transform:uppercase;color:rgba(0,0,0,0.3);border-bottom:2px solid rgba(0,0,0,0.06)">Comment</th>' +
        '</tr></thead>' +
        '<tbody id="historyBody">' + rows + '</tbody>' +
      '</table>' +
    '</div></div>';

  document.body.appendChild(overlay);
  overlay.addEventListener('click', function(e) { if (e.target === overlay) closeHistoryModal(); });
  window.__histBrandId = brandId;
}

function closeHistoryModal() {
  var ov = document.getElementById('historyOverlay');
  if (ov) ov.remove();
}

function filterHistory() {
  var brandId = window.__histBrandId;
  var fromVal = (document.getElementById('histFrom') || {}).value || '';
  var toVal = (document.getElementById('histTo') || {}).value || '';
  var ratings = (SENTIMENT[brandId] || []).slice().sort(function(a, b) {
    return (b.date || '').localeCompare(a.date || '');
  });

  if (fromVal) ratings = ratings.filter(function(r) { return (r.date || '') >= fromVal; });
  if (toVal) ratings = ratings.filter(function(r) { return (r.date || '') <= toVal; });

  var rows = '';
  if (ratings.length === 0) {
    rows = '<tr><td colspan="3" style="padding:20px;text-align:center;color:#9E9E9E;font-size:13px">No ratings in this range</td></tr>';
  } else {
    ratings.forEach(function(r) {
      var dotColor = sentimentColor(r.score || 0);
      rows += '<tr><td style="padding:10px 14px;font-size:12px;color:#3a3a3a;border-bottom:1px solid rgba(0,0,0,0.04);white-space:nowrap">' + esc(r.date || '') + '</td>' +
        '<td style="padding:10px 14px;font-size:13px;font-weight:700;border-bottom:1px solid rgba(0,0,0,0.04)"><span style="display:inline-block;width:10px;height:10px;border-radius:50%;background:' + dotColor + ';margin-right:8px;vertical-align:middle"></span><span style="color:' + dotColor + '">' + (r.score || 0) + '/10</span></td>' +
        '<td style="padding:10px 14px;font-size:12px;color:#3a3a3a;border-bottom:1px solid rgba(0,0,0,0.04);line-height:1.5">' + esc(r.comment || '') + '</td></tr>';
    });
  }
  var body = document.getElementById('historyBody');
  if (body) body.innerHTML = rows;
}

// ===== MONDAY POPUP =====
function checkMondayPopup() {
  if (!isPulkit()) return;
  var today = new Date();
  var isMonday = today.getDay() === 1;
  var todayStr = today.toISOString().substring(0, 10);
  var sevenDaysAgo = new Date(today.getTime() - 7 * 24 * 60 * 60 * 1000).toISOString().substring(0, 10);
  var dismissals = SENTIMENT.dismissals || {};

  var unratedBrands = [];
  Object.keys(M).forEach(function(brandId) {
    var mm = M[brandId] || {};
    if (mm.ch) return; // skip churned

    // Check if dismissed in last 7 days
    var dismissed = dismissals[brandId];
    if (dismissed) {
      var dismissDate = dismissed.substring(0, 10);
      if (dismissDate >= sevenDaysAgo) return;
    }

    // Check if rated in last 7 days
    var ratings = SENTIMENT[brandId] || [];
    var ratedRecently = false;
    if (Array.isArray(ratings)) {
      ratings.forEach(function(r) {
        if (r && r.date && r.date >= sevenDaysAgo) ratedRecently = true;
      });
    }
    if (!ratedRecently) unratedBrands.push({ id: brandId, name: mm.n });
  });

  if (unratedBrands.length === 0) return;
  if (!isMonday && unratedBrands.length < 5) return; // only show on non-Monday if many unrated

  var items = '';
  unratedBrands.forEach(function(b) {
    items += '<div style="display:flex;align-items:center;justify-content:space-between;padding:10px 14px;background:rgba(0,0,0,0.02);border-radius:10px;margin-bottom:6px">' +
      '<span style="font-size:13px;font-weight:600;color:#072C1B">' + esc(b.name) + '</span>' +
      '<div style="display:flex;gap:8px">' +
        '<button onclick="openRateModal(\\'' + b.id + '\\');closeMondayPopup()" style="padding:5px 14px;background:#072C1B;color:#fff;border:none;border-radius:8px;font-size:11px;font-weight:600;cursor:pointer;font-family:inherit">Rate</button>' +
        '<button onclick="dismissBrand(\\'' + b.id + '\\')" style="padding:5px 14px;background:none;border:1px solid rgba(0,0,0,0.1);border-radius:8px;font-size:11px;font-weight:500;cursor:pointer;font-family:inherit;color:#9E9E9E">Dismiss</button>' +
      '</div></div>';
  });

  var banner = document.createElement('div');
  banner.id = 'mondayPopup';
  banner.style.cssText = 'position:fixed;bottom:24px;right:24px;width:380px;background:#fff;border-radius:16px;box-shadow:0 12px 48px rgba(0,0,0,0.2);z-index:9998;overflow:hidden;border:1px solid rgba(7,44,27,0.1);animation:fadeIn .3s ease';
  banner.innerHTML = '<div style="padding:18px 20px 12px;border-bottom:1px solid rgba(0,0,0,0.06);display:flex;justify-content:space-between;align-items:center">' +
    '<div><div style="font-size:14px;font-weight:700;color:#072C1B">' + (isMonday ? 'Monday Check-in' : 'Sentiment Reminder') + '</div>' +
    '<div style="font-size:11px;color:#9E9E9E;margin-top:2px">' + unratedBrands.length + ' brand' + (unratedBrands.length > 1 ? 's' : '') + ' need rating</div></div>' +
    '<button onclick="closeMondayPopup()" style="background:none;border:none;cursor:pointer;font-size:18px;color:#9E9E9E;padding:4px">&times;</button></div>' +
    '<div style="padding:14px 20px;max-height:300px;overflow-y:auto">' + items + '</div>';
  document.body.appendChild(banner);
}

function closeMondayPopup() {
  var p = document.getElementById('mondayPopup');
  if (p) p.remove();
}

function dismissBrand(brandId) {
  fetch('/api/dismiss-popup', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ brandId: brandId })
  }).then(function(r) { return r.json(); }).then(function(data) {
    if (data.success) {
      if (!SENTIMENT.dismissals) SENTIMENT.dismissals = {};
      SENTIMENT.dismissals[brandId] = new Date().toISOString();
      // Remove from popup
      closeMondayPopup();
      checkMondayPopup();
    }
  }).catch(function() {});
}

// ===== HEALTH =====
function renderHealth(d, m) {
  var el = document.getElementById('healthContent');
  var h = d.health || {}, p = d.performance || {}, hs = h.score || 0, bd = h.breakdown || {}, sigs = h.signals || [];
  var circ = 2 * Math.PI * 66, off = circ - (hs / 100) * circ;
  var rev30 = (p['30d'] && p['30d'].revenue) || 0;
  var d7 = p['7d'] || {};
  var d30 = p['30d'] || {};
  var sentLatest = getLatestSentiment(cur);
  var sentScore = sentLatest ? sentLatest.score : 0;
  var sentMapped = bd.csm_sentiment || 0;

  // ── 3 COLUMNS: Score | KPI cards | Radar ──
  var html = '<div style="display:grid;grid-template-columns:150px 1fr 1fr;gap:16px;margin-bottom:20px;align-items:stretch">' +
    // COL 1: Score ring
    '<div style="display:flex;flex-direction:column;align-items:center;justify-content:center;background:var(--wh);border-radius:var(--rl);padding:20px 16px;box-shadow:var(--sh);border:1px solid rgba(0,0,0,0.03)">' +
    '<svg width="110" height="110" viewBox="0 0 110 110">' +
    '<circle cx="55" cy="55" r="46" fill="none" stroke="rgba(0,0,0,0.04)" stroke-width="8"/>' +
    '<circle cx="55" cy="55" r="46" fill="none" stroke="' + sc(hs) + '" stroke-width="8" stroke-linecap="round" stroke-dasharray="' + (2*Math.PI*46).toFixed(1) + '" stroke-dashoffset="' + ((2*Math.PI*46) - (hs/100)*(2*Math.PI*46)).toFixed(1) + '" transform="rotate(-90 55 55)" style="transition:stroke-dashoffset .8s"/>' +
    '<text x="55" y="52" text-anchor="middle" dominant-baseline="central" font-size="32" font-weight="800" font-family="Space Grotesk,sans-serif" fill="' + sc(hs) + '">' + hs + '</text>' +
    '<text x="55" y="72" text-anchor="middle" font-size="9" font-weight="600" fill="#9E9E9E" font-family="Space Grotesk,sans-serif">/ 100</text>' +
    '</svg>' +
    '<div style="margin-top:8px;padding:4px 14px;border-radius:100px;font-size:10px;font-weight:700;background:' + scBg(hs) + ';color:' + sc(hs) + '">' + scLbl(hs) + '</div></div>' +
    // COL 2: KPI cards stacked
    '<div style="display:flex;flex-direction:column;gap:8px;justify-content:space-between">' +
    '<div class="kpi" style="padding:14px 16px"><div class="kpi-accent" style="background:#072C1B"></div><div class="kpi-name">ARR</div><div class="kpi-val" style="font-size:22px">$' + (m.arr||0).toLocaleString() + '</div></div>' +
    '<div class="kpi" style="padding:14px 16px"><div class="kpi-accent" style="background:#DBE9E0"></div><div class="kpi-name">30d Revenue</div><div class="kpi-val" style="font-size:22px">' + fc(rev30) + '</div></div>' +
    '<div class="kpi" style="padding:14px 16px"><div class="kpi-accent" style="background:#3ED660"></div><div class="kpi-name">30d CVR</div><div class="kpi-val" style="font-size:22px">' + fp((d30.cvr) || 0) + '</div></div>' +
    '<div class="kpi" style="padding:14px 16px"><div class="kpi-accent" style="background:#B89240"></div><div class="kpi-name">Renewal</div><div class="kpi-val" style="font-size:18px">' + (m.ren || 'Not set') + '</div></div>' +
    '</div>' +
    // COL 3: Radar chart + buttons
    '<div style="background:var(--wh);border-radius:var(--rl);padding:16px;box-shadow:var(--sh);border:1px solid rgba(0,0,0,0.03);display:flex;flex-direction:column">' +
    '<div style="font-size:10px;font-weight:700;text-transform:uppercase;letter-spacing:.12em;color:rgba(0,0,0,0.3);margin-bottom:8px">Health Breakdown</div>' +
    (Object.keys(bd).length > 0 ? '<div style="flex:1;min-height:200px"><canvas id="healthRadar"></canvas></div>' : '<div style="color:var(--mi);font-size:12px">No breakdown data</div>') +
    // Sentiment buttons (Pulkit only)
    (isPulkit() ? '<div style="display:flex;gap:8px;margin-top:10px;justify-content:center">' +
      '<button onclick="openRateModal(\\'' + cur + '\\')" style="padding:7px 16px;background:#072C1B;color:#fff;border:none;border-radius:10px;font-size:11px;font-weight:600;cursor:pointer;font-family:inherit;display:inline-flex;align-items:center;gap:5px;box-shadow:0 2px 6px rgba(7,44,27,0.15);transition:all .15s" onmouseover="this.style.transform=\\'translateY(-1px)\\';this.style.boxShadow=\\'0 4px 12px rgba(7,44,27,0.25)\\'" onmouseout="this.style.transform=\\'none\\';this.style.boxShadow=\\'0 2px 6px rgba(7,44,27,0.15)\\'">' +
        (sentLatest ? '&#9998; Update Rating' : '&#9733; Rate Account') + '</button>' +
      '<button onclick="openHistoryModal(\\'' + cur + '\\')" style="padding:7px 16px;background:none;border:1px solid rgba(0,0,0,0.1);border-radius:10px;font-size:11px;font-weight:600;cursor:pointer;font-family:inherit;color:#9E9E9E;transition:all .15s" onmouseover="this.style.borderColor=\\'rgba(7,44,27,0.3)\\';this.style.color=\\'#072C1B\\'" onmouseout="this.style.borderColor=\\'rgba(0,0,0,0.1)\\';this.style.color=\\'#9E9E9E\\'">&#128203; History</button>' +
    '</div>' : '') +
    // Show current sentiment inline
    (sentLatest ? '<div style="text-align:center;margin-top:8px;font-size:11px;color:#9E9E9E">Current: <span style="color:' + sentimentColor(sentScore) + ';font-weight:700">' + sentScore + '/10</span> <span style="display:inline-block;width:7px;height:7px;border-radius:50%;background:' + sentimentColor(sentScore) + ';vertical-align:middle"></span> ' + sentimentLabel(sentScore) + ' (' + (sentLatest.date || '') + ')</div>' : '') +
    '</div></div>';

  // ── Account Note ──
  if (m.cm) {
    var isChurn = (m.cm||'').toLowerCase().indexOf('churn') >= 0 || m.ch;
    html += '<div class="insight-inline ' + (isChurn ? 'alert' : '') + '" style="margin-bottom:16px;margin-top:0">' +
      '<span class="ii-icon">' + (isChurn ? '&#10060;' : '&#9888;') + '</span>' +
      '<span class="ii-text"><strong>Account Note:</strong> ' + esc(m.cm) + '</span></div>';
  }

  // ── ROW 3: Signals ──
  if (sigs.length > 0) {
    html += '<div class="sh"><h2>Health Signals</h2></div><div class="signal-timeline">';
    sigs.forEach(function(s) {
      var t = s.type || 'warning';
      var dotCls = t === 'positive' ? 'st-green' : t === 'negative' ? 'st-red' : t === 'neutral' ? 'st-neutral' : 'st-yellow';
      html += '<div class="st-item"><div class="st-dot ' + dotCls + '"></div><div class="st-content">' +
        '<div class="st-time">' + esc(s.time || '') + '</div>' +
        '<div class="st-text">' + esc(s.text || '') + '</div></div></div>';
    });
    html += '</div>';
  }

  el.innerHTML = html;

  setTimeout(function() {
    var ctx = document.getElementById('healthRadar');
    if (ctx && Object.keys(bd).length > 0) {
      var detailTexts = [bd.platform_performance_detail || bd.platform_detail || '', bd.communication_detail || '', bd.engagement_detail || '', bd.csm_sentiment_detail || ''];
      charts.healthRadar = new Chart(ctx, {
        type: 'radar',
        data: {
          labels: ['Platform (20)', 'Communication (20)', 'Engagement (20)', 'CSM Sentiment (40)'],
          datasets: [{
            data: [bd.platform_performance || bd.platform_activity || 0, bd.communication || 0, bd.engagement || 0, bd.csm_sentiment || 0],
            backgroundColor: sc(hs) + '22',
            borderColor: sc(hs),
            borderWidth: 2.5,
            pointBackgroundColor: sc(hs),
            pointRadius: 5,
            pointHoverRadius: 7
          }]
        },
        options: {
          responsive: true, maintainAspectRatio: false,
          plugins: {
            legend: { display: false },
            tooltip: {
              enabled: true,
              backgroundColor: 'rgba(7,44,27,0.95)',
              titleFont: { size: 12, weight: 700, family: "'Space Grotesk'" },
              bodyFont: { size: 11, family: "'Space Grotesk'" },
              padding: 14,
              cornerRadius: 10,
              displayColors: false,
              callbacks: {
                title: function(items) {
                  var idx = items[0].dataIndex;
                  var names = ['Platform Performance', 'Communication', 'Engagement', 'CSM Sentiment'];
                  var maxes = [20, 20, 20, 40];
                  return names[idx] + ': ' + items[0].raw + '/' + maxes[idx];
                },
                label: function(item) {
                  var detail = detailTexts[item.dataIndex] || 'No detail available';
                  var lines = [];
                  var parts = detail.split(',');
                  parts.forEach(function(p) { if (p.trim()) lines.push(p.trim()); });
                  return lines.length > 0 ? lines : [detail];
                }
              }
            }
          },
          scales: { r: {
            beginAtZero: true, max: 40,
            ticks: { stepSize: 8, font: { size: 9 }, backdropColor: 'transparent', color: 'rgba(0,0,0,0.25)' },
            grid: { color: 'rgba(0,0,0,0.05)' },
            pointLabels: { font: { size: 10, family: "'Space Grotesk'", weight: '600' }, color: 'rgba(0,0,0,0.5)' }
          }}
        }
      });
    }
  }, 150);
}

// ===== PERFORMANCE =====
var perfRange = '7d';
function renderPerformance(d, m) {
  var el = document.getElementById('perfContent');
  var p = d.performance || {};
  var daily = p.daily || [];
  var periods = ['yesterday','3d','7d','15d','30d','45d'];
  var pLabels = ['Yesterday','3 Day','7 Day','15 Day','30 Day','45 Day'];
  var pDays = [1,3,7,15,30,45];

  // Date range selector
  var html = '<div class="range-bar">';
  periods.forEach(function(per, i) {
    html += '<button class="range-btn ' + (per === perfRange ? 'active' : '') + '" onclick="perfRange=\\'' + per + '\\';renderPerformance(BD[cur]||{},M[cur]||{})">' + pLabels[i] + '</button>';
  });
  html += '</div>';

  var sel = p[perfRange] || {};
  var selIdx = periods.indexOf(perfRange);
  var selLabel = pLabels[selIdx];
  var selDays = pDays[selIdx];
  var rps = sel.sessions ? (sel.revenue / sel.sessions) : 0;
  var d30 = p['30d'] || {};

  // ── KPI CARDS ──
  html += '<div class="sh" style="margin-top:0"><h2>Key Metrics &mdash; ' + selLabel + '</h2></div><div class="kpi-grid">' +
    '<div class="kpi"><div class="kpi-accent" style="background:#072C1B"></div><div class="kpi-name">Sessions</div><div class="kpi-val">' + fn(sel.sessions) + '</div><div class="kpi-period">' + selLabel + '</div></div>' +
    '<div class="kpi"><div class="kpi-accent" style="background:#DBE9E0"></div><div class="kpi-name">Revenue</div><div class="kpi-val">' + fc(sel.revenue) + '</div><div class="kpi-period">' + selLabel + '</div></div>' +
    '<div class="kpi"><div class="kpi-accent" style="background:#3ED660"></div><div class="kpi-name">Conv. Rate</div><div class="kpi-val">' + fp(sel.cvr) + '</div><div class="kpi-period">' + selLabel + '</div></div>' +
    '<div class="kpi"><div class="kpi-accent" style="background:#B89240"></div><div class="kpi-name">Purchases</div><div class="kpi-val">' + fn(sel.purchases) + '</div><div class="kpi-period">' + selLabel + '</div></div>' +
    '<div class="kpi"><div class="kpi-accent" style="background:#9B59B6"></div><div class="kpi-name">AOV</div><div class="kpi-val">' + fc(sel.aov) + '</div><div class="kpi-period">' + selLabel + '</div></div>' +
    '</div><div class="kpi-grid" style="grid-template-columns:repeat(3,1fr)">' +
    '<div class="kpi"><div class="kpi-accent" style="background:#0A0A0A"></div><div class="kpi-name">Rev / Session</div><div class="kpi-val">$' + rps.toFixed(2) + '</div><div class="kpi-period">' + selLabel + '</div></div>' +
    '<div class="kpi"><div class="kpi-accent" style="background:#C8A894"></div><div class="kpi-name">Rev / Day</div><div class="kpi-val">' + fc(sel.revenue / selDays) + '</div><div class="kpi-period">Daily avg</div></div>' +
    '<div class="kpi"><div class="kpi-accent" style="background:#2563EB"></div><div class="kpi-name">Purchases / Day</div><div class="kpi-val">' + (sel.purchases / selDays).toFixed(1) + '</div><div class="kpi-period">Daily avg</div></div>' +
    '</div>';

  // ── EXECUTIVE SUMMARY (richer) ──
  var revTrend = sel.revenue > 0 && d30.revenue > 0 ? ((sel.revenue / (d30.revenue / 30 * selDays) - 1) * 100) : 0;
  var trendDir = revTrend > 5 ? 'up' : revTrend < -5 ? 'down' : 'flat';
  var trendIcon = trendDir === 'up' ? '&#9650;' : trendDir === 'down' ? '&#9660;' : '&#9654;';
  var trendColor = trendDir === 'up' ? '#1a8a3e' : trendDir === 'down' ? '#C84632' : '#92700c';
  var summaryText = esc(m.n) + ' generated <strong>' + fc(sel.revenue) + '</strong> in revenue from <strong>' + fn(sel.sessions) + ' sessions</strong> over ' + selLabel.toLowerCase() + '. The <strong>' + fp(sel.cvr) + ' conversion rate</strong> produced <strong>' + fn(sel.purchases) + ' purchases</strong> at an average order value of <strong>' + fc(sel.aov) + '</strong>. Revenue per session is <strong>$' + rps.toFixed(2) + '</strong>, averaging <strong>' + fc(sel.revenue / selDays) + '/day</strong>.';
  html += '<div class="sh"><h2>Executive Summary</h2></div>' +
    '<div class="card" style="margin-bottom:0"><div style="display:flex;align-items:center;gap:8px;margin-bottom:10px"><span style="color:' + trendColor + ';font-size:13px;font-weight:700">' + trendIcon + ' ' + Math.abs(revTrend).toFixed(1) + '%</span><span style="font-size:11px;color:var(--mi)">vs 30-day average</span></div><p style="font-size:13.5px;line-height:1.75;color:#3a3a3a">' + summaryText + '</p></div>';

  // ── CONVERSION FUNNEL + 3 INSIGHTS (side by side) ──
  var fSess = sel.sessions || 0;
  var fPurch = sel.purchases || 0;
  var fCvr = fSess ? (fPurch / fSess * 100) : 0;
  var fPdp = sel.pdp_views || 0;
  var fAtc = sel.atc || 0;
  var fChk = sel.checkouts || 0;
  var pdpPct = fSess ? (fPdp / fSess * 100).toFixed(1) : '0';
  var atcPct = fSess ? (fAtc / fSess * 100).toFixed(1) : '0';
  var chkPct = fSess ? (fChk / fSess * 100).toFixed(1) : '0';
  var pdpToAtc = fPdp ? (fAtc / fPdp * 100).toFixed(1) : '0';
  var chkToP = fChk ? (fPurch / fChk * 100).toFixed(1) : '0';
  var dropOff = fSess ? ((1 - fPdp / fSess) * 100).toFixed(1) : '0';

  html += '<div class="sh"><h2>Conversion Funnel</h2></div>' +
    '<div style="display:grid;grid-template-columns:7fr 3fr;gap:16px">' +
    '<div class="funnel-card">' +
    '<div style="font-size:14px;font-weight:600;margin-bottom:4px">Session &#8594; Purchase Funnel</div>' +
    '<div style="font-size:11px;color:var(--mi);margin-bottom:18px">' + selLabel + ' aggregate &middot; 5 stages</div>' +
    '<svg viewBox="0 0 1000 180" preserveAspectRatio="none" style="width:100%;height:120px;display:block">' +
    '<path d="M 0,5 C 80,5 140,40 200,40 C 260,40 340,65 400,65 C 460,65 540,75 600,75 C 700,75 800,85 1000,85 L 1000,95 C 800,95 700,105 600,105 C 540,105 460,115 400,115 C 340,115 260,140 200,140 C 140,140 80,175 0,175 Z" fill="rgba(7,44,27,0.5)"/>' +
    '<line x1="200" y1="0" x2="200" y2="180" stroke="rgba(0,0,0,0.08)" stroke-width="1" stroke-dasharray="4,4"/>' +
    '<line x1="400" y1="0" x2="400" y2="180" stroke="rgba(0,0,0,0.08)" stroke-width="1" stroke-dasharray="4,4"/>' +
    '<line x1="600" y1="0" x2="600" y2="180" stroke="rgba(0,0,0,0.08)" stroke-width="1" stroke-dasharray="4,4"/>' +
    '<line x1="800" y1="0" x2="800" y2="180" stroke="rgba(0,0,0,0.08)" stroke-width="1" stroke-dasharray="4,4"/>' +
    '</svg>' +
    '<div class="funnel-stages">' +
    '<div class="funnel-stage"><span class="funnel-stage-num">' + fn(fSess) + '</span><span class="funnel-stage-pct">100%</span><div class="funnel-stage-name">Sessions</div></div>' +
    '<div class="funnel-stage"><span class="funnel-stage-num">' + fn(fPdp) + '</span><span class="funnel-stage-pct">' + pdpPct + '%</span><div class="funnel-stage-name">PDP Views</div></div>' +
    '<div class="funnel-stage"><span class="funnel-stage-num">' + fn(fAtc) + '</span><span class="funnel-stage-pct">' + atcPct + '%</span><div class="funnel-stage-name">Add to Cart</div></div>' +
    '<div class="funnel-stage"><span class="funnel-stage-num">' + fn(fChk) + '</span><span class="funnel-stage-pct">' + chkPct + '%</span><div class="funnel-stage-name">Checkout</div></div>' +
    '<div class="funnel-stage"><span class="funnel-stage-num">' + fn(fPurch) + '</span><span class="funnel-stage-pct">' + fCvr.toFixed(2) + '%</span><div class="funnel-stage-name">Purchases</div></div>' +
    '</div></div>' +
    '<div style="display:flex;flex-direction:column;gap:12px">' +
    '<div class="insight-inline alert" style="flex:1"><span class="ii-icon">&#9888;&#65039;</span><span class="ii-text"><strong>' + dropOff + '% of sessions never view a PDP.</strong> This is the biggest drop-off. Focus on above-fold product visibility and stronger CTAs to drive PDP engagement.</span></div>' +
    '<div class="insight-inline" style="flex:1"><span class="ii-icon">&#128161;</span><span class="ii-text"><strong>PDP&#8594;ATC rate is ' + pdpToAtc + '%.</strong> ' + (parseFloat(pdpToAtc) > 15 ? 'This is healthy — product pages are converting browsers into intenders.' : 'This is below average. Consider stronger product imagery, reviews, and urgency on PDPs.') + '</span></div>' +
    '<div class="insight-inline gold" style="flex:1"><span class="ii-icon">&#127919;</span><span class="ii-text"><strong>Checkout&#8594;Purchase is ' + chkToP + '%.</strong> ' + (parseFloat(chkToP) > 60 ? 'Strong checkout completion. Payment flow is working well.' : 'Cart abandonment is high. Review shipping costs, payment options, and trust signals.') + '</span></div>' +
    '</div></div>';

  // ── DAILY TREND CHARTS (date-wise for selected range) ──
  var dSlice = daily.slice(-selDays);
  var hasDailyData = dSlice.length > 0;

  html += '<div class="sh"><h2>Daily Trends &mdash; ' + selLabel + '</h2></div>';

  if (hasDailyData) {
    var dLabels = dSlice.map(function(r) { var d2 = r.date || ''; var mm = ['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec'][parseInt(d2.substring(5,7),10)-1]||''; return d2.substring(8,10)+' '+mm; });
    html += '<div class="perf-charts">' +
      '<div class="chart-card"><div class="chart-title">Daily Revenue</div><div class="chart-wrap"><canvas id="perfRevChart"></canvas></div></div>' +
      '<div class="chart-card"><div class="chart-title">Daily Sessions</div><div class="chart-wrap"><canvas id="perfSessChart"></canvas></div></div></div>' +
      '<div class="perf-charts">' +
      '<div class="chart-card"><div class="chart-title">Daily CVR</div><div class="chart-wrap"><canvas id="perfCvrChart"></canvas></div></div>' +
      '<div class="chart-card"><div class="chart-title">Daily AOV</div><div class="chart-wrap"><canvas id="perfAovChart"></canvas></div></div></div>';
  } else {
    html += '<div class="empty-card" style="margin-bottom:16px">Daily chart data not yet loaded. Run <code>/account-dashboard</code> to pull daily data from FERM\\u00c0T.</div>';
  }

  // ── SUMMARY BANNER ──
  html += '<div class="summary" style="margin-top:24px"><div class="summary-text"><h3>' + selLabel + ' Performance Summary</h3><p>Aggregate FERM\\u00c0T funnel performance for ' + esc(m.n) + '.</p></div>' +
    '<div class="s-stats"><div class="s-stat"><span class="s-val">' + fc(sel.revenue) + '</span><span class="s-lbl">Revenue</span></div>' +
    '<div class="s-stat"><span class="s-val">' + fc(sel.aov) + '</span><span class="s-lbl">AOV</span></div>' +
    '<div class="s-stat"><span class="s-val">' + fn(sel.sessions) + '</span><span class="s-lbl">Sessions</span></div>' +
    '<div class="s-stat"><span class="s-val">' + fp(sel.cvr) + '</span><span class="s-lbl">CVR</span></div></div></div>';

  if (p._note) {
    html += '<div class="insight-inline gold" style="margin-top:16px"><span class="ii-icon">&#128221;</span><span class="ii-text">' + esc(p._note) + '</span></div>';
  }

  el.innerHTML = html;

  // ── CHARTS (daily data, date-wise) ──
  if (hasDailyData) {
    setTimeout(function() {
      destroyCharts();
      var dLabels = dSlice.map(function(r) { var d2 = r.date || ''; var mm = ['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec'][parseInt(d2.substring(5,7),10)-1]||''; return d2.substring(8,10)+' '+mm; });
      var dRev = dSlice.map(function(r) { return r.revenue || 0; });
      var dSess = dSlice.map(function(r) { return r.sessions || 0; });
      var dCvr = dSlice.map(function(r) { return r.sessions ? (r.purchases / r.sessions * 100) : 0; });
      var dAov = dSlice.map(function(r) { return r.purchases ? (r.revenue / r.purchases) : 0; });
      var showDL = true;
      var dlBase = { anchor: 'end', align: 'top', font: { size: 8, weight: 600, family: "'Space Grotesk'" }, padding: { bottom: 2 } };
      var xCfg = { grid: { display: false }, ticks: { font: { size: 9, family: "'Space Grotesk'" }, maxRotation: 45 } };
      var rc = document.getElementById('perfRevChart');
      if (rc) { charts.perfRev = new Chart(rc, { type: 'bar', data: { labels: dLabels, datasets: [{ data: dRev, backgroundColor: 'rgba(7,44,27,0.65)', borderRadius: 4, borderSkipped: false }] }, plugins: [ChartDataLabels], options: { responsive: true, maintainAspectRatio: false, layout: { padding: { top: 18 } }, plugins: { legend: { display: false }, datalabels: Object.assign({}, dlBase, { display: showDL, color: '#072C1B', formatter: function(v) { return '$' + Math.round(v).toLocaleString(); } }) }, scales: { x: xCfg, y: { grid: { color: 'rgba(0,0,0,0.04)' }, ticks: { callback: function(v) { return '$' + v.toLocaleString(); }, font: { size: 9 } } } } } }); }
      var sc2 = document.getElementById('perfSessChart');
      if (sc2) { charts.perfSess = new Chart(sc2, { type: 'bar', data: { labels: dLabels, datasets: [{ data: dSess, backgroundColor: 'rgba(37,99,235,0.5)', borderRadius: 4, borderSkipped: false }] }, plugins: [ChartDataLabels], options: { responsive: true, maintainAspectRatio: false, layout: { padding: { top: 18 } }, plugins: { legend: { display: false }, datalabels: Object.assign({}, dlBase, { display: showDL, color: '#2563EB', formatter: function(v) { return v.toLocaleString(); } }) }, scales: { x: xCfg, y: { grid: { color: 'rgba(0,0,0,0.04)' }, ticks: { callback: function(v) { return v.toLocaleString(); }, font: { size: 9 } } } } } }); }
      var cc = document.getElementById('perfCvrChart');
      if (cc) { charts.perfCvr = new Chart(cc, { type: 'line', data: { labels: dLabels, datasets: [{ data: dCvr, borderColor: '#3ED660', backgroundColor: 'rgba(62,214,96,0.08)', fill: true, tension: 0.4, pointRadius: 3, pointBackgroundColor: '#3ED660', pointBorderColor: '#fff', pointBorderWidth: 1.5 }] }, plugins: [ChartDataLabels], options: { responsive: true, maintainAspectRatio: false, layout: { padding: { top: 18 } }, plugins: { legend: { display: false }, datalabels: Object.assign({}, dlBase, { display: showDL, color: '#1a8a3e', formatter: function(v) { return v.toFixed(1) + '%'; } }) }, scales: { x: xCfg, y: { grid: { color: 'rgba(0,0,0,0.04)' }, ticks: { callback: function(v) { return v.toFixed(1) + '%'; }, font: { size: 9 } } } } } }); }
      var ac = document.getElementById('perfAovChart');
      if (ac) { charts.perfAov = new Chart(ac, { type: 'line', data: { labels: dLabels, datasets: [{ data: dAov, borderColor: '#9B59B6', backgroundColor: 'rgba(155,89,182,0.06)', fill: true, tension: 0.4, pointRadius: 3, pointBackgroundColor: '#9B59B6', pointBorderColor: '#fff', pointBorderWidth: 1.5 }] }, plugins: [ChartDataLabels], options: { responsive: true, maintainAspectRatio: false, layout: { padding: { top: 18 } }, plugins: { legend: { display: false }, datalabels: Object.assign({}, dlBase, { display: showDL, color: '#7B3FA0', formatter: function(v) { return '$' + Math.round(v).toLocaleString(); } }) }, scales: { x: xCfg, y: { grid: { color: 'rgba(0,0,0,0.04)' }, ticks: { callback: function(v) { return '$' + v.toFixed(0); }, font: { size: 9 } } } } } }); }
    }, 150);
  }
}

// ===== CALLS (TIMELINE) =====
function renderCalls(d) {
  var el = document.getElementById('callsContent');
  var ca = d.calls || {};
  var html = '';
  if (ca.analysis) {
    html += '<div class="insight-inline" style="margin-bottom:20px;margin-top:0"><span class="ii-icon">&#128161;</span><span class="ii-text"><strong>Call Analysis:</strong> ' + esc(ca.analysis) + '</span></div>';
  }
  var recs = ca.recent || [];
  if (recs.length > 0) {
    html += '<div class="sh" style="margin-top:0"><h2>Call Timeline</h2></div><div class="timeline">';
    recs.forEach(function(c) {
      var date = (c.date || '').substring(0, 10);
      var dur = c.duration || (c.duration_minutes ? c.duration_minutes + ' min' : '');
      var parts = Array.isArray(c.participants) ? c.participants.join(', ') : (c.participants || '');
      var actions = c.action_items || [];
      html += '<div class="tl-item"><div class="tl-dot"></div><div class="tl-date">' + esc(date) + '</div><div class="tl-card">' +
        '<div class="tl-header"><div class="tl-title">' + esc(c.title || 'Call') + '</div>' +
        (c.source ? '<div class="tl-source">' + esc(c.source) + '</div>' : '') + '</div>' +
        '<div class="tl-meta">' + esc(dur) + ' &middot; ' + esc(parts) +
        (c.recording_url ? ' &middot; <a href="' + c.recording_url + '" target="_blank">Recording &#x2197;</a>' : '') + '</div>' +
        (c.summary ? '<div class="tl-summary">' + esc(c.summary) + '</div>' : '');
      if (actions.length > 0) {
        html += '<div class="tl-actions"><div class="tl-actions-title">Action Items</div>';
        actions.forEach(function(a) { html += '<div class="tl-action"><div class="tl-action-dot"></div>' + esc(a) + '</div>'; });
        html += '</div>';
      }
      html += '</div></div>';
    });
    html += '</div>';
  } else {
    html += '<div class="empty-card">No call data available.</div>';
  }
  el.innerHTML = html;
}

// ===== CALENDAR =====
function renderCalendar(d) {
  var el = document.getElementById('calendarContent');
  var cl = d.calendar || {};
  var html = '';
  var up = cl.upcoming || [], pa = cl.past || [];
  if (up.length > 0) {
    html += '<div class="sh" style="margin-top:0"><h2>Upcoming</h2></div><div class="cal-list">';
    up.forEach(function(ev) {
      var t = (ev.start || '').substring(0, 16).replace('T', ' ');
      html += '<div class="cal-item cal-upcoming"><div class="cal-dot"></div><div class="cal-time">' + esc(t) + '</div><div class="cal-title">' + esc(ev.title || '') + '</div></div>';
    });
    html += '</div>';
  } else {
    html += '<div class="empty-card" style="margin-bottom:20px">No upcoming calls scheduled.</div>';
  }
  if (pa.length > 0) {
    html += '<div class="sh"><h2>Past</h2></div><div class="cal-list">';
    pa.forEach(function(ev) {
      var t = (ev.start || '').substring(0, 16).replace('T', ' ');
      html += '<div class="cal-item cal-past"><div class="cal-dot"></div><div class="cal-time">' + esc(t) + '</div><div class="cal-title">' + esc(ev.title || '') + '</div></div>';
    });
    html += '</div>';
  }
  if (cl._note) {
    html += '<div class="insight-inline gold" style="margin-top:16px"><span class="ii-icon">&#128221;</span><span class="ii-text">' + esc(cl._note) + '</span></div>';
  }
  el.innerHTML = html;
}

// ===== SLACK (CHAT BUBBLES) =====
function renderSlack(d, m) {
  var el = document.getElementById('slackContent');
  var sk = d.slack || {};
  var slName = SL[m.sl] || 'unknown';
  var html = '';
  if (sk.analysis) {
    html += '<div class="insight-inline" style="margin-bottom:20px;margin-top:0"><span class="ii-icon">&#128172;</span><span class="ii-text"><strong>Slack Analysis:</strong> ' + esc(sk.analysis) + '</span></div>';
  }
  var msgs = sk.messages || [];
  if (msgs.length > 0) {
    html += '<div class="sh" style="margin-top:0"><h2>#' + esc(slName) + '</h2></div><div class="chat-container">';
    msgs.forEach(function(msg) {
      var name = msg.user || 'Unknown';
      var ini = initials(name);
      var col = avColor(name);
      var ts = (msg.timestamp || '').substring(0, 10);
      html += '<div class="chat-msg"><div class="chat-avatar" style="background:' + col + '">' + ini + '</div>' +
        '<div class="chat-bubble"><div class="chat-name">' + esc(name) + '</div>' +
        '<div class="chat-text">' + esc(msg.text || '') + '</div>' +
        '<div class="chat-time">' + esc(ts) + ' &middot; ' + esc(msg.channel || '#' + slName) + '</div></div></div>';
    });
    html += '</div>';
  } else {
    html += '<div class="empty-card">No Slack messages.</div>';
  }
  el.innerHTML = html;
}

// ===== EMAIL =====
function renderEmail(d) {
  var el = document.getElementById('emailContent');
  var em = d.email || {};
  var html = '';
  if (em.analysis) {
    html += '<div class="insight-inline" style="margin-bottom:20px;margin-top:0"><span class="ii-icon">&#9993;</span><span class="ii-text"><strong>Email Analysis:</strong> ' + esc(em.analysis) + '</span></div>';
  }
  var msgs = em.messages || [];
  if (msgs.length > 0) {
    html += '<div class="sh" style="margin-top:0"><h2>Recent Emails</h2></div><div class="email-list">';
    msgs.forEach(function(msg) {
      var from = (msg.from || '').split('<')[0].trim() || 'Unknown';
      var date = (msg.date || '').substring(0, 10);
      var ini = initials(from);
      var col = avColor(from);
      html += '<div class="email-item"><div class="email-avatar" style="background:' + col + '">' + ini + '</div>' +
        '<div class="email-content"><div class="email-header"><div class="email-from">' + esc(from) + '</div><div class="email-date">' + esc(date) + '</div></div>' +
        (msg.subject ? '<div class="email-subject">' + esc(msg.subject) + '</div>' : '') +
        '<div class="email-snippet">' + esc(msg.snippet || '') + '</div></div></div>';
    });
    html += '</div>';
  } else {
    html += '<div class="empty-card">No email data.</div>';
  }
  el.innerHTML = html;
}
"""

# ════════════════════════════════════════════════════════
# BUILD
# ════════════════════════════════════════════════════════
def build():
    all_data = {}
    for f in os.listdir(DATA):
        if f.endswith('.json'):
            with open(os.path.join(DATA, f)) as fh:
                all_data[f.replace('.json','')] = json.load(fh)

    brands = sorted(META.items(), key=lambda x: x[1]["n"])
    first = brands[0][0]
    now = datetime.now().strftime("%b %d, %Y %I:%M %p")
    totalARR = sum(m["arr"] for _,m in brands)

    # Sidebar
    sb = ""
    for bid,m in brands:
        d = all_data.get(bid,{})
        logo = LOGOS.get(bid,"")
        sb += f'<div class="bi" onclick="sel(\'{bid}\')" data-bid="{bid}">'
        if logo: sb += f'<img src="{logo}" class="bl" onerror="this.style.display=\'none\'">'
        sb += f'<div class="bii"><div class="bin">{e(m["n"])}</div><div class="bim">{e(m["v"])} &middot; ${m["arr"]//1000}K</div></div>'
        sb += f'<div class="bd {dc(bid,d)}"></div></div>\n'

    # Build JS with embedded data
    meta_js = {}
    for k,v in META.items():
        meta_js[k] = dict(v)

    js = JS_TEMPLATE
    js = js.replace('__BRAND_DATA__', json.dumps(all_data))
    js = js.replace('__META__', json.dumps(meta_js))
    js = js.replace('__LOGOS__', json.dumps(LOGOS))
    js = js.replace('__SLACKS__', json.dumps(SLACKS))

    page = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>FERMÀT Account Management Portal</title>
<link href="https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@300;400;500;600;700&family=Cormorant+Garamond:ital,wght@0,300;0,400;0,500;0,600;1,300;1,400;1,500&display=swap" rel="stylesheet">
<script src="https://cdn.jsdelivr.net/npm/chart.js@4"></script>
<script src="https://cdn.jsdelivr.net/npm/chartjs-plugin-datalabels@2.2.0"></script>
<style>
{CSS}
</style>
</head>
<body>

<aside class="sb">
<div class="sbh" style="cursor:pointer" onclick="switchTab('overview')"><div style="display:flex;align-items:center;gap:10px"><svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="rgba(255,255,255,0.5)" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" style="flex-shrink:0"><path d="M3 9l9-7 9 7v11a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2z"/><polyline points="9 22 9 12 15 12 15 22"/></svg><img src="{FLOGO}" class="sbl" onerror="this.outerHTML='<div style=font-size:18px;font-weight:700;color:#fff>FERMÀT</div>'"></div><div class="sbs">Account Management Portal</div></div>
<div class="sbx"><input type="text" class="sbi" placeholder="Search brands..." oninput="filterBrands(this.value)"></div>
<div class="bls" id="brandList">{sb}</div>
<div class="sbf"><div class="sbft">Pulkit Srivastava &middot; CSM</div><div class="sbfr">Last refresh: {now}</div></div>
</aside>

<main class="mn">

<div class="hdr" id="overviewHdr">
<div class="hdr-l">
<div><div class="hdr-n">Portfolio Overview</div><div class="hdr-v">{len(brands)} Brands &middot; Pulkit Srivastava</div></div>
</div>
<div class="hdr-r">
<div class="hdr-ri"><div class="hdr-rl">Total ARR</div><div class="hdr-rv">${totalARR:,}</div></div>
<div class="hdr-ri"><div class="hdr-rl">Total MRR</div><div class="hdr-rv">${totalARR // 12:,}</div></div>
<div class="hdr-ri"><div class="hdr-rl">Last Refresh</div><div class="hdr-rv">{now}</div></div>
</div>
</div>

<div class="hdr" id="brandHdr" style="display:none">
<div class="hdr-l">
<div><div class="hdr-n" id="hdrName"></div><div class="hdr-v" id="hdrVert"></div><div class="hdr-v" id="hdrStatus" style="margin-top:2px"></div></div>
</div>
<div class="hdr-r">
<div class="hdr-ri"><div class="hdr-rl">Renewal</div><div class="hdr-rv" id="hdrRen"></div></div>
<div class="hdr-ri"><div class="hdr-rl">Slack</div><div class="hdr-rv" id="hdrSlack"></div></div>
</div>
</div>

<div class="tabs" id="tabBar">
<button class="tab" data-t="health" onclick="switchTab('health')">Health Score</button>
<button class="tab" data-t="performance" onclick="switchTab('performance')">Performance</button>
<button class="tab" data-t="calls" onclick="switchTab('calls')">Calls &amp; Analysis</button>
<button class="tab" data-t="calendar" onclick="switchTab('calendar')">Calendar</button>
<button class="tab" data-t="slack" onclick="switchTab('slack')">Slack</button>
<button class="tab" data-t="email" onclick="switchTab('email')">Email</button>
</div>

<div class="ct">
<div class="tp active" id="tab-overview"><div id="overviewContent"></div></div>
<div class="tp" id="tab-health"><div id="healthContent"></div></div>
<div class="tp" id="tab-performance"><div id="perfContent"></div></div>
<div class="tp" id="tab-calls"><div id="callsContent"></div></div>
<div class="tp" id="tab-calendar"><div id="calendarContent"></div></div>
<div class="tp" id="tab-slack"><div id="slackContent"></div></div>
<div class="tp" id="tab-email"><div id="emailContent"></div></div>
</div>

</main>

<script>
{js}
</script>
</body>
</html>"""

    with open(OUT, "w") as f:
        f.write(page)
    print(f"Built {OUT} ({os.path.getsize(OUT):,} bytes) with {len(all_data)} brands")

if __name__ == "__main__":
    build()
