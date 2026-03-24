#!/usr/bin/env python3
"""
update_mar24.py — Full refresh of Slack, Gmail, Glyphic, and Calendar data for all 15 brands.
Data sourced from live MCP calls on 2026-03-24.
"""

import json, os

DIR  = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(DIR, "data")

def update_brand(csv_id, updates):
    path = os.path.join(DATA, f"{csv_id}.json")
    with open(path) as f:
        d = json.load(f)
    d["last_updated"] = "2026-03-24T16:00:00Z"
    for key in ("slack", "email", "calls", "calendar"):
        if key in updates:
            d[key] = updates[key]
    with open(path, "w") as f:
        json.dump(d, f, indent=2)
    print(f"  Updated {d.get('brand_name', csv_id)}")


# ════════════════════════════════════════════════════════════════════════════
# 1. DE SOI
# ════════════════════════════════════════════════════════════════════════════
update_brand("8fd93118-a246-431e-aebf-4aa362622342", {
    "slack": {
        "messages": [
            {"user": "Denise Shon", "text": "hi Pulkit could you have the fermat invoices sent to ap@drinkdesoi.com and cc denise@drinkdesoi.com?", "timestamp": "2026-03-11T04:01:38+05:30", "channel": "#fermat-x-de-soi"},
            {"user": "Pulkit Srivastava", "text": "Hey De Soi team! I'm Pulkit, your new GM here at FERMÀT. I've been with the FERMÀT team for about 1.5 years and I'm genuinely so excited to start working with you all! Would love to hop on a call and get to know everyone.", "timestamp": "2026-03-03T11:00:12+05:30", "channel": "#fermat-x-de-soi"},
            {"user": "Mia DyBuncio", "text": "I'm reaching out with some bittersweet but exciting news — later this week I'll be transitioning into a new role on our Product team here at FERMÀT. I'm thrilled to introduce Pulkit, one of our outstanding Onboarding and Growth Managers!", "timestamp": "2026-03-03T01:50:37+05:30", "channel": "#fermat-x-de-soi"},
            {"user": "Mia DyBuncio", "text": "hey Denise was on the zoom but don't have much to cover today so happy to connect async instead!", "timestamp": "2026-02-19T23:09:02+05:30", "channel": "#fermat-x-de-soi"},
            {"user": "Denise Shon", "text": "Out of curiosity - is it possible to do a subscription only buy box in Fermat? I was thinking it could be interesting to run a split test to this page where we offer a sub only option vs having 1 time vs sub", "timestamp": "2026-02-19T00:09:25+05:30", "channel": "#fermat-x-de-soi"},
            {"user": "Denise Shon", "text": "I'm working on another funnel (duplicated an existing template) and wondering how to change the media for the hero header?", "timestamp": "2026-02-18T05:51:52+05:30", "channel": "#fermat-x-de-soi"},
            {"user": "Denise Shon", "text": "Would you be able to take a look at this funnel I created and share any recommendations/optimizations? For context, we want to run ads promoting a unique, limited time offer: a free 4pk when you subscribe to le grand ensemble", "timestamp": "2026-02-18T03:51:03+05:30", "channel": "#fermat-x-de-soi"},
            {"user": "Pierre (Bot)", "text": "FERMÀT Weekly Roundup Jan 5-11: Sessions 4,729 | Purchases 113 | GMV $7,819 | Revenue $6,586. Top funnels: Collection Grid Page: Meta (2,867 sessions, $5,228 GMV, 2.65% CVR), Match Your Cocktail to De Soi (1,488 sessions, $2,115 GMV, 1.95% CVR)", "timestamp": "2026-01-12T22:30:24+05:30", "channel": "#fermat-x-de-soi"},
            {"user": "Rebekah (Structured)", "text": "We launched our Google Fermat LP campaign in PMAX on Dec 17th. We've spent $2.02k so far. The CPA in Google is 8% stronger than our OG PMAX campaign & nCAC in TripleWhale is 18% better than our OG PMAX going to De Soi .com.", "timestamp": "2026-01-09T00:34:07+05:30", "channel": "#fermat-x-de-soi"},
            {"user": "Denise Shon", "text": "We just got started with Snap ads and were sending traffic to Fermat but I am wondering if there is something we need to do in Fermat to make sure the Snap pixel on our Shopify store is pulling through to Fermat", "timestamp": "2026-01-08T01:19:39+05:30", "channel": "#fermat-x-de-soi"}
        ],
        "analysis": "The Slack channel shows active engagement from Denise Shon who has taken over as the primary contact after Amruta's departure. She has been proactively building funnels (le grand ensemble subscription offer), asking about features (subscription-only buy box, hero media changes), and handling operational tasks (invoice routing). The GM transition from Mia to Pulkit was announced on Mar 3, with Pulkit introducing himself. However, there has been no substantive conversation between Pulkit and the De Soi team since the introduction — the only interaction was Denise asking about invoice routing on Mar 11. The last Pierre weekly roundup was Jan 12, suggesting automated reporting may have stopped."
    },
    "email": {
        "messages": [
            {"from": "Denise Shon via Intercom <notifications@fermat-e313b71dec30.intercom-mail.com>", "subject": "Re: [FERMÀT] Denise Shon: how can i change what products show when someone clicks on 'shop all products'", "date": "2026-03-20T22:58:22Z", "snippet": "Denise at De Soi asking about customizing 'shop all products' display. Assigned to Pulkit via Intercom."},
            {"from": "Pierre via Intercom <notifications@fermat-e313b71dec30.intercom-mail.com>", "subject": "FERMÀT: Pierre assigned a conversation with Denise Shon to you", "date": "2026-03-20T22:55:37Z", "snippet": "Pierre assigned Intercom conversation with Denise Shon (shop all products question) to Pulkit."},
            {"from": "Denise Shon via Intercom <notifications@fermat-e313b71dec30.intercom-mail.com>", "subject": "Re: [FERMÀT] Denise Shon: how to pull in product reviews", "date": "2026-03-17T23:40:53Z", "snippet": "Denise at De Soi asking about how to pull in product reviews. Assigned to Pulkit via Intercom."},
            {"from": "Pierre via Intercom <notifications@fermat-e313b71dec30.intercom-mail.com>", "subject": "FERMÀT: Pierre assigned a conversation with Denise Shon to you", "date": "2026-03-17T23:38:08Z", "snippet": "Pierre assigned Intercom conversation with Denise Shon to Pulkit. Denise asking about product reviews functionality."},
            {"from": "FERMÀT Performance Reports <pulkit@fermatcommerce.com>", "subject": "De Soi × FERMÀT || Feb 27 – Mar 12, 2026 Performance Update", "date": "2026-03-13T13:56:46Z", "snippet": "Sharing FERMÀT funnel performance update covering sessions, revenue, conversion rates, ad spend, and funnel-level breakdowns with insights and recommendations."},
            {"from": "FERMÀT Performance Reports <pulkit@fermatcommerce.com>", "subject": "De Soi × FERMÀT || Feb 24 – Mar 11, 2026 Performance Update", "date": "2026-03-13T10:51:03Z", "snippet": "Sharing FERMÀT funnel performance update covering sessions, revenue, conversion rates, ad spend, and funnel-level breakdowns with insights and recommendations."}
        ],
        "analysis": "Email activity is primarily operational. Pulkit sent performance reports on Mar 13 covering Feb 24 - Mar 12 periods. Denise Shon has reached out via Intercom twice — on Mar 17 asking about product reviews and on Mar 20 asking how to change products in 'shop all products' display. Both were auto-assigned to Pulkit and need responses. These Intercom queries show Denise is actively using the platform and encountering questions, which is a positive engagement signal but also indicates unresolved support needs."
    },
    "calls": {
        "recent": [],
        "analysis": "No Glyphic calls found for De Soi in the last 30 days (since Feb 22). The last completed call was Mia's platform walkthrough with Denise on Feb 3. The Feb 19 weekly was cancelled. Since the GM transition from Mia to Pulkit on Mar 3, no calls have been scheduled — this is a significant gap that needs immediate attention to build the relationship with Denise."
    },
    "calendar": {
        "past": [],
        "upcoming": [],
        "_note": "No Google Calendar events found matching 'De Soi' between Feb 22 and Apr 30, 2026 on Pulkit's calendar. No recurring meetings have been set up since the GM transition on Mar 3."
    }
})

# ════════════════════════════════════════════════════════════════════════════
# 2. FOND REGENERATIVE
# ════════════════════════════════════════════════════════════════════════════
update_brand("ab6fc1e8-f245-4344-902c-b60388575aca", {
    "slack": {
        "messages": [
            {"user": "FOND team member", "text": "Hi! Pulkit Do you have an idea why videos compress on Fermat?", "timestamp": "2026-03-13T20:17:30+05:30", "channel": "#fermat-x-fond"},
            {"user": "Pulkit Srivastava", "text": "Hey FOND team! I'm Pulkit, your new GM here at FERMÀT. I've been with the FERMÀT team for about 1.5 years and I'm genuinely so excited to start working with you all! Would love to hop on a call and get to know everyone.", "timestamp": "2026-02-25T20:46:07+05:30", "channel": "#fermat-x-fond"},
            {"user": "Talia Cohen", "text": "Hey FOND team! I'm reaching out with some bittersweet but exciting news — later this week I'll be transitioning into a new role on our Enterprise team here at FERMÀT. I'm thrilled to introduce Pulkit, one of our outstanding Onboarding and Growth Managers!", "timestamp": "2026-02-25T19:30:15+05:30", "channel": "#fermat-x-fond"},
            {"user": "FOND team member", "text": "I think I would love your insights on a different style recipe video funnel. I have 2 created (swedish meatballs & filet mignon). Could you build an Egg Drop Soup funnel and I can see how you lay it out?", "timestamp": "2026-02-18T21:15:19+05:30", "channel": "#fermat-x-fond"},
            {"user": "Talia Cohen", "text": "great, thanks all! Chelsea and Kendall - i don't believe i saw any funnels come across my way. was there anything the both of you were working on that you wanted my input on?", "timestamp": "2026-02-18T20:55:46+05:30", "channel": "#fermat-x-fond"},
            {"user": "Talia Cohen", "text": "Hey Kendall, Amy, Chelsea - any chance we can adjust our meeting time tomorrow back by a half hour?", "timestamp": "2026-02-17T23:52:24+05:30", "channel": "#fermat-x-fond"},
            {"user": "FOND team member", "text": "Hi Talia! Our funnel 'how to know your tallow can be trusted' is getting some good traction and views due to another company going viral about the tallow industry being corrupt. Can you take another look at the funnel and make edits to really get people converting?", "timestamp": "2026-01-28T20:55:04+05:30", "channel": "#fermat-x-fond"},
            {"user": "Talia Cohen", "text": "Sharing below a quick recap: Tallow for Fat Hormones Funnel recommendations implemented — added subscribe & save CTAs, updated product hyperlinks, introduced navigation menu bar, added grid shop CTA. Upcoming funnels: Shiitake & Sage, Foundational Nourishment Bundle video funnel.", "timestamp": "2026-01-22T04:04:48+05:30", "channel": "#fermat-x-fond"}
        ],
        "analysis": "The FOND channel shows an engaged brand team with Chelsea, Kendall, and Amy actively building funnels (recipe funnels, flavor-specific funnels). The GM transition from Talia to Pulkit was announced Feb 25 and warmly received (heart reactions). A FOND team member asked Pulkit about video compression on Mar 13 — this is the first direct technical question to Pulkit, showing early relationship building. The team has been proactive about funnel creation and optimizing for conversions, particularly around their tallow products."
    },
    "email": {
        "messages": [
            {"from": "Glyphic AI <noreply@glyphic.ai>", "subject": "Talia / Pulkit Accounts KT summary is ready", "date": "2026-02-23T15:01:39Z", "snippet": "Glyphic summary of the Talia to Pulkit account transition knowledge transfer call covering FOND and other accounts."}
        ],
        "analysis": "Minimal brand-specific email activity for FOND in the last 30 days. The only relevant email is the Glyphic KT summary from Feb 23 documenting the account transition from Talia to Pulkit. No direct email exchanges between Pulkit and the FOND team have occurred yet — communication has been via Slack."
    },
    "calls": {
        "recent": [],
        "analysis": "No Glyphic calls found for FOND in the last 30 days (since Feb 22). The previous GM Talia had regular weekly calls with Chelsea, Kendall, and Amy. Since the transition to Pulkit on Feb 25, no calls have been scheduled yet — this gap needs to be addressed to maintain the cadence the brand team was accustomed to."
    },
    "calendar": {
        "past": [],
        "upcoming": [],
        "_note": "No Google Calendar events found matching 'FOND' between Feb 22 and Apr 30, 2026 on Pulkit's calendar. No recurring meetings have been set up since the GM transition on Feb 25."
    }
})

# ════════════════════════════════════════════════════════════════════════════
# 3. GAINS IN BULK
# ════════════════════════════════════════════════════════════════════════════
update_brand("5cc7fc09-8acf-4af0-892f-735c6686c2a2", {
    "slack": {
        "messages": [
            {"user": "Isabel O'Keefe", "text": "Hey Raymond - thanks for the time yesterday. GiB 2026 Plans: Pushing for $50M revenue target with doubled ad spend. Expanding beyond creatine to Shape, Workout Candy, Testosterone Gain + new products. FERMÀT use case: Split testing educational/influencer-driven landing pages.", "timestamp": "2026-01-15T07:48:17+05:30", "channel": "#fermat-x-gains-in-bulk"},
            {"user": "Isabel O'Keefe", "text": "hey Raymond - happy new year! looking forward to catching up this afternoon. check in on new funnels for Creatine Revolution launching on Jan 31st and walk through AI search trial onboarding", "timestamp": "2026-01-13T20:04:15+05:30", "channel": "#fermat-x-gains-in-bulk"},
            {"user": "Raymond Stercl", "text": "Hey Isabel thanks for circling back! I have a bunch on my plate but we do plan to move forward with the free 6-month AI Search trial! For the Creatine Revolution that will be for Jan 31st. Unfortunately I will need to cancel the call today.", "timestamp": "2025-12-30T23:30:48+05:30", "channel": "#fermat-x-gains-in-bulk"}
        ],
        "analysis": "The Gains In Bulk Slack channel has been very quiet — Pulkit and the FERMÀT bot joined on Feb 24 but there has been no conversation since. The last substantive exchange was Isabel's Jan 15 recap after a call with Raymond about 2026 plans ($50M revenue target, Creatine Revolution campaign). Raymond has been responsive but busy, cancelling the Dec 30 call. The brand appears to be in a holding pattern with minimal FERMÀT engagement since the GM transition."
    },
    "email": {
        "messages": [],
        "analysis": "No brand-specific email activity found for Gains In Bulk in the last 30 days. The only result was an unrelated OpenAI newsletter. No performance reports or direct communications between Pulkit and the GiB team via email."
    },
    "calls": {
        "recent": [],
        "analysis": "No Glyphic calls found for Gains In Bulk in the last 30 days. The last call was Isabel's Jan 13 session with Raymond. The brand had very low platform usage (20 sessions/week) and engagement has been minimal. Since the GM transition, no calls have been initiated by Pulkit."
    },
    "calendar": {
        "past": [],
        "upcoming": [],
        "_note": "No Google Calendar events found matching 'Gains In Bulk' between Feb 22 and Apr 30, 2026 on Pulkit's calendar."
    }
})

# ════════════════════════════════════════════════════════════════════════════
# 4. HAVN
# ════════════════════════════════════════════════════════════════════════════
update_brand("1e7aa370-3cde-40bf-90d9-8ce8a3aaed30", {
    "slack": {
        "messages": [
            {"user": "Isabel O'Keefe", "text": "hi Tom - hope you're having a great start to the new year. wanted to check in - did you want to keep today's sync on the calendar?", "timestamp": "2026-01-16T21:06:24+05:30", "channel": "#havn-x-fermat"},
            {"user": "Tom (HAVN)", "text": "Hi! I'm having issue with the setup of an incremental test on my account. the setup is 50/50 but that's not what I get", "timestamp": "2026-01-06T23:06:41+05:30", "channel": "#havn-x-fermat"},
            {"user": "Ryan Barry", "text": "Hey Tom! I just want to give you a heads up that today is my last day at Fermat. I also wanted to introduce Mia DyBuncio. Mia's not only a team lead here at Fermat with tons of experience working with our top brands.", "timestamp": "2025-12-20T02:05:15+05:30", "channel": "#havn-x-fermat"},
            {"user": "Ryan Barry", "text": "Hey Tom -- hope you and the whole HAVN team had an incredible BFCM. Sharing next steps for Fermat's AI Search Engine Free Trial which you'd opted into via our LinkedIn announcement.", "timestamp": "2025-12-03T03:35:38+05:30", "channel": "#havn-x-fermat"}
        ],
        "analysis": "The HAVN Slack channel has been dormant since Jan 16. Pulkit and the FERMÀT bot joined on Feb 24, but no introduction message was posted (unlike other brands). The primary contact Tom had an active relationship with previous GM Ryan Barry, who left in Dec 2025. Isabel and Mia were introduced as interim contacts. Tom reported an incremental test setup issue on Jan 6 that was resolved. No engagement since the GM transition to Pulkit — an introduction and re-engagement is urgently needed."
    },
    "email": {
        "messages": [],
        "analysis": "No email activity found for HAVN in the last 30 days. No performance reports or direct communications between Pulkit and the HAVN team."
    },
    "calls": {
        "recent": [],
        "analysis": "No Glyphic calls found for HAVN in the last 30 days. The relationship was managed by Ryan Barry through Dec 2025, then briefly by Isabel. Since Pulkit's transition, no calls have been initiated. This is a significant gap given HAVN was an active account with regular syncs."
    },
    "calendar": {
        "past": [],
        "upcoming": [],
        "_note": "No Google Calendar events found matching 'HAVN' between Feb 22 and Apr 30, 2026 on Pulkit's calendar."
    }
})

# ════════════════════════════════════════════════════════════════════════════
# 5. HOP WTR
# ════════════════════════════════════════════════════════════════════════════
update_brand("74128082-bd6b-4435-94a5-7a7fdfa41726", {
    "slack": {
        "messages": [
            {"user": "Pulkit Srivastava", "text": "Hey HOP WTR team! I'm Pulkit, your new GM here at FERMÀT. I've been with the FERMÀT team for about 1.5 years and I'm genuinely so excited to start working with you all!", "timestamp": "2026-02-25T20:45:43+05:30", "channel": "#fermat-x-hop-wtr"},
            {"user": "Talia Cohen", "text": "Hey HOP WTR team! I'm reaching out with some bittersweet but exciting news — I'll be transitioning into a new role on our Enterprise team here at FERMÀT. I'm thrilled to introduce Pulkit.", "timestamp": "2026-02-25T19:30:20+05:30", "channel": "#fermat-x-hop-wtr"},
            {"user": "Talia Cohen", "text": "Hi Grace Colbert - great connecting with you earlier today! Pricing Test Funnel | Google: We hit statistical significance! Variant 1 (lower price point) is showing a 2.16% CVR (400%+ over control). Recommend continuing to push traffic.", "timestamp": "2026-02-20T02:50:47+05:30", "channel": "#fermat-x-hop-wtr"},
            {"user": "Andreas (HOP WTR)", "text": "Andreas noticed the Meta experiment page didn't have the link appended at the top. Grace added it and we're now seeing sessions come through. Could you confirm the setup is now 100% correct on your end?", "timestamp": "2026-02-12T05:45:46+05:30", "channel": "#fermat-x-hop-wtr"},
            {"user": "Andreas (HOP WTR)", "text": "I see the AB price test now show up twice — once with Google as source and then Meta as source. Is that intended?", "timestamp": "2026-02-11T01:04:40+05:30", "channel": "#fermat-x-hop-wtr"},
            {"user": "Talia Cohen", "text": "Hey Grace, Andreas - deploying new links for testing purposes. Google Link and Meta Link with experiments set up as A/B tests within the funnel themselves - no need to add in a link split.", "timestamp": "2026-02-10T04:57:12+05:30", "channel": "#fermat-x-hop-wtr"},
            {"user": "Andreas (HOP WTR)", "text": "if i look at the funnels, I see the two tests side by side - directionally very encouraging as the test group has >2x conversion rate", "timestamp": "2026-02-09T06:40:40+05:30", "channel": "#fermat-x-hop-wtr"},
            {"user": "Andreas (HOP WTR)", "text": "I am a little concerned we continue to have just one conversion. Does this still seem normal?", "timestamp": "2026-02-08T05:04:47+05:30", "channel": "#fermat-x-hop-wtr"},
            {"user": "Grace Colbert", "text": "launched a campaign on Meta this afternoon to kick off the test. Daily spend $800-1000 to get started", "timestamp": "2026-02-06T06:01:39+05:30", "channel": "#fermat-x-hop-wtr"}
        ],
        "analysis": "HOP WTR is a CHURNED account. The pricing A/B test showed strong results (Variant 1 at 2.16% CVR, 400%+ over control), but the brand decided to cancel. Talia transitioned the account to Pulkit on Feb 25, and Pulkit introduced himself. However, the cancellation was processed on Mar 5 based on email data. The Slack channel shows intense activity around the pricing test from Feb 6-20, with Andreas closely monitoring results and Grace launching Meta campaigns. Despite promising test results, the brand chose to churn."
    },
    "email": {
        "messages": [
            {"from": "Glyphic AI <noreply@glyphic.ai>", "subject": "Prepare for Grace Colbert and Pulkit Srivastava", "date": "2026-03-10T15:47:27Z", "snippet": "Glyphic pre-call prep for scheduled call between Grace Colbert and Pulkit."},
            {"from": "Andreas Biebl <andreas.b@hopwtr.com>", "subject": "Re: HOP WTR x FERMÀT || Cancellation Confirmed", "date": "2026-03-05T05:31:12Z", "snippet": "Andreas thanking Pulkit for processing the cancellation."},
            {"from": "Pulkit Srivastava <pulkit@fermatcommerce.com>", "subject": "HOP WTR x FERMÀT || Cancellation Confirmed", "date": "2026-03-05T05:14:55Z", "snippet": "Pulkit confirming cancellation processing, noting one final invoice for February."},
            {"from": "Ashutosh Patel <ashutosh@fermatcommerce.com>", "subject": "Re: Brand Churn Notice: HOP WTR", "date": "2026-03-03T10:54:50Z", "snippet": "AR team confirming last invoice to be paid by March 31."},
            {"from": "Pulkit Srivastava <pulkit@fermatcommerce.com>", "subject": "Brand Churn Notice: HOP WTR", "date": "2026-03-03T04:09:17Z", "snippet": "Pulkit submitting formal churn notice for HOP WTR — contacts Brad Nogle (Head of E-Commerce) and Grace Colbert (Sr. Manager Growth)."}
        ],
        "analysis": "HOP WTR has churned. Pulkit submitted the formal churn notice on Mar 3 and processed the cancellation confirmation on Mar 5. Andreas acknowledged the cancellation. The last invoice for February is due by March 31. Despite the pricing test showing 400%+ improvement in CVR, the brand still chose to leave FERMÀT."
    },
    "calls": {
        "recent": [],
        "analysis": "No Glyphic calls found for HOP WTR in the last 30 days. The account has been churned as of Mar 5."
    },
    "calendar": {
        "past": [],
        "upcoming": [],
        "_note": "No Google Calendar events found for HOP WTR. Account churned on Mar 5, 2026."
    }
})

# ════════════════════════════════════════════════════════════════════════════
# 6. HENRY ROSE
# ════════════════════════════════════════════════════════════════════════════
update_brand("f7983632-4d4b-49c8-8e7a-192e9e999dff", {
    "slack": {
        "messages": [
            {"user": "Henry Rose team member", "text": "Pulkit lovely to meet you. I generally have issues with our weekly Fermat time, perhaps we could switch the time around a bit?", "timestamp": "2026-03-03T23:23:04+05:30", "channel": "#fermat-x-henry-rose"},
            {"user": "Henry Rose team member", "text": "Mia DyBuncio thank you for everything!! We are so sad to see you go, but excited for your next adventure!", "timestamp": "2026-03-03T23:22:11+05:30", "channel": "#fermat-x-henry-rose"},
            {"user": "Henry Rose team member", "text": "hi Pulkit, so nice to meet you! i'll get some time scheduled and hopefully we can treat that as our ongoing meeting time, will also coordinate that with Remi and Ngoc Ma.", "timestamp": "2026-03-03T19:54:14+05:30", "channel": "#fermat-x-henry-rose"},
            {"user": "Pulkit Srivastava", "text": "Hey Henry Rose team! I'm Pulkit, your new GM here at FERMÀT. I've been with the FERMÀT team for about 1.5 years and I'm genuinely so excited to start working with you all!", "timestamp": "2026-03-03T11:00:44+05:30", "channel": "#fermat-x-henry-rose"},
            {"user": "Mia DyBuncio", "text": "Hey Henry Rose team! I'm reaching out with some bittersweet but exciting news, later this week I'll be transitioning into a new role on our Product team here at FERMÀT. I'm thrilled to introduce Pulkit.", "timestamp": "2026-03-03T01:47:43+05:30", "channel": "#fermat-x-henry-rose"},
            {"user": "Pierre (Bot)", "text": "There are new AI Search funnels ready for you to approve!", "timestamp": "2026-03-12T02:55:17+05:30", "channel": "#fermat-x-henry-rose"},
            {"user": "Pierre (Bot)", "text": "There are new AI Search funnels ready for you to approve!", "timestamp": "2026-03-05T03:20:30+05:30", "channel": "#fermat-x-henry-rose"}
        ],
        "analysis": "Henry Rose's Slack channel shows a warm reception to Pulkit's introduction on Mar 3. Two team members (one asking to reschedule weekly timing, another coordinating with Remi and Ngoc Ma) responded positively. Pierre is actively generating AI Search funnels (Mar 5, Mar 12). The brand team was emotional about Mia's departure. A key next step is for Pulkit to set up the recurring meeting time as requested, coordinating with Remi and Ngoc Ma."
    },
    "email": {
        "messages": [
            {"from": "Glyphic AI <noreply@glyphic.ai>", "subject": "Pulkit / Mia - Account Transitions summary is ready", "date": "2026-02-24T15:42:34Z", "snippet": "Glyphic summary of the Mia to Pulkit account transition KT call covering Henry Rose and other accounts."}
        ],
        "analysis": "Minimal brand-specific email activity for Henry Rose in the last 30 days. The only relevant email is the Glyphic KT summary from the Mia-to-Pulkit transition. No direct email exchanges between Pulkit and the Henry Rose team yet — communication has been via Slack."
    },
    "calls": {
        "recent": [],
        "analysis": "No Glyphic calls found for Henry Rose in the last 30 days. Mia had weekly calls with the Henry Rose team. Since the GM transition, Pulkit has not yet set up recurring meetings. The brand team proactively asked to reschedule the meeting time on Mar 3, indicating they want to maintain the call cadence."
    },
    "calendar": {
        "past": [],
        "upcoming": [],
        "_note": "No Google Calendar events found matching 'Henry Rose' between Feb 22 and Apr 30, 2026 on Pulkit's calendar. The Henry Rose team has requested to set up a new recurring meeting time."
    }
})

# ════════════════════════════════════════════════════════════════════════════
# 7. LITTLE SAINTS
# ════════════════════════════════════════════════════════════════════════════
update_brand("8be8e4b7-d7c1-4922-b8e3-271671ee1592", {
    "slack": {
        "messages": [
            {"user": "Kar (Little Saints)", "text": "Hi Pulkit were there any outages yesterday with Fermat or Shopify?", "timestamp": "2026-03-17T18:47:07+05:30", "channel": "#fermat-x-little-saints"},
            {"user": "Pierre (Bot)", "text": "There are new AI Search funnels ready for you to approve!", "timestamp": "2026-03-12T02:55:19+05:30", "channel": "#fermat-x-little-saints"},
            {"user": "Pierre (Bot)", "text": "There are new AI Search funnels ready for you to approve!", "timestamp": "2026-03-05T03:20:32+05:30", "channel": "#fermat-x-little-saints"},
            {"user": "Pulkit Srivastava", "text": "Hey Little Saints team! I'm Pulkit, your new GM here at FERMÀT. I've been with the FERMÀT team for about 1.5 years and I'm genuinely so excited to start working with you all!", "timestamp": "2026-03-03T11:00:32+05:30", "channel": "#fermat-x-little-saints"},
            {"user": "Mia DyBuncio", "text": "Hey Kar — I'm reaching out with some bittersweet but exciting news, I'll be transitioning into a new role on our Product team here at FERMÀT. I'm thrilled to introduce Pulkit.", "timestamp": "2026-03-03T01:51:26+05:30", "channel": "#fermat-x-little-saints"},
            {"user": "Kar (Little Saints)", "text": "Hi Mia I knew i totally forgot a coupla questions 1) was wondering if you guys set up an LLMS.txt file for us. 2) Was wondering how to edit content in a PDP like the actual About section", "timestamp": "2026-02-20T18:40:08+05:30", "channel": "#fermat-x-little-saints"}
        ],
        "analysis": "The Little Saints channel shows Kar as the sole brand contact. She asked Pulkit about potential outages on Mar 17 — this is the first direct engagement with Pulkit and shows the brand is actively using the platform and monitoring it. Pierre is generating AI Search funnels regularly. Kar had questions about LLMS.txt setup and PDP editing on Feb 20, indicating she's exploring the platform's capabilities. The GM transition was announced Mar 3."
    },
    "email": {
        "messages": [
            {"from": "Notion Team <notify@mail.notion.so>", "subject": "Jennifer Schnadig made updates in Fermat Commerce", "date": "2026-03-11T01:23:04Z", "snippet": "Internal Notion update notification related to account management documentation."}
        ],
        "analysis": "Minimal email activity for Little Saints in the last 30 days. No direct email exchanges between Pulkit and Kar. Communication is primarily via Slack."
    },
    "calls": {
        "recent": [],
        "analysis": "No Glyphic calls found for Little Saints in the last 30 days. Mia had periodic calls with Kar. Since the GM transition, no calls have been scheduled between Pulkit and Kar."
    },
    "calendar": {
        "past": [],
        "upcoming": [],
        "_note": "No Google Calendar events found matching 'Little Saints' between Feb 22 and Apr 30, 2026 on Pulkit's calendar."
    }
})

# ════════════════════════════════════════════════════════════════════════════
# 8. MOTHER ROOT
# ════════════════════════════════════════════════════════════════════════════
update_brand("ae4f1f5d-f1d1-488f-8340-1890cfd0faf3", {
    "slack": {
        "messages": [
            {"user": "Pulkit Srivastava", "text": "Hey Mother Root team! I'm Pulkit, your new GM here at FERMÀT. Would love to hop on a call and get to know everyone.", "timestamp": "2026-03-10T18:31:15+05:30", "channel": "#fermàt-x-motherroot"},
            {"user": "Talia Cohen", "text": "Hi Maddie Carey - welcome back to the office. I'm reaching out with some bittersweet but exciting news — I'll be transitioning into a new role on our Enterprise team. I'm thrilled to introduce Pulkit.", "timestamp": "2026-03-10T18:30:18+05:30", "channel": "#fermàt-x-motherroot"},
            {"user": "Maddie Carey", "text": "Hi Talia Do you know if we have any Marmalade landing page live? We've had a couple random orders appear that we can't seem to find out where from.", "timestamp": "2026-03-02T21:59:32+05:30", "channel": "#fermàt-x-motherroot"},
            {"user": "Talia Cohen", "text": "Hey Tom - yes, all good to go here! Looks Maddie set the traffic split on the FERMÀT link to send 0% to FERMÀT with 100% to the site. Would you like me to adjust that to a 50/50 split?", "timestamp": "2026-02-26T21:53:31+05:30", "channel": "#fermàt-x-motherroot"},
            {"user": "Tom (Mother Root)", "text": "We've got paid ads live using the Fermat link. Hey Talia, are we all good to go live for the Mother's Day funnel?", "timestamp": "2026-02-26T16:17:52+05:30", "channel": "#fermàt-x-motherroot"},
            {"user": "Maddie Carey", "text": "Hey Talia — I'm OOO for the next two weeks but the channel will be monitored if any issues", "timestamp": "2026-02-20T19:13:17+05:30", "channel": "#fermàt-x-motherroot"},
            {"user": "Maddie Carey", "text": "Hey Talia - This product isn't appearing in Fermat — I've resynced too. Could you take a look please? MOTHERSDAYSET", "timestamp": "2026-02-19T20:48:59+05:30", "channel": "#fermàt-x-motherroot"},
            {"user": "Talia Cohen", "text": "Module Visibility Controls are now live! This will give you the ability to show or hide specific modules based on device.", "timestamp": "2026-02-18T00:58:19+05:30", "channel": "#fermàt-x-motherroot"}
        ],
        "analysis": "Mother Root is an actively engaged UK-based brand with Maddie Carey as the primary contact and Tom handling ad operations. The Mother's Day funnel went live in late Feb with paid ads using the Fermat link. Talia discovered the traffic split was set to 0% Fermat / 100% site and offered to adjust to 50/50. Maddie was OOO for two weeks (Feb 20 - early Mar). The GM transition to Pulkit was announced Mar 10 (later than other brands due to Maddie's OOO). Maddie had asked about a Marmalade landing page with mystery orders on Mar 2. The Rhubarb Q1 launch is planned for Mar 10 (retention early access) and Mar 26 (general launch via ads)."
    },
    "email": {
        "messages": [
            {"from": "Talia Cohen <talia@fermatcommerce.com>", "subject": "Invitation: Mother Root <> FERMÀT | Weekly Check In @ Weekly from 9pm to 9:30pm on Wednesday (IST)", "date": "2026-03-09T19:00:13Z", "snippet": "Talia forwarding the Mother Root weekly check-in calendar invite to Pulkit, Maddie, and Thomas."},
            {"from": "Glyphic AI <noreply@glyphic.ai>", "subject": "Talia / Pulkit Accounts KT summary is ready", "date": "2026-02-23T15:01:39Z", "snippet": "Glyphic summary of the Talia to Pulkit account transition KT call."}
        ],
        "analysis": "Email shows Talia forwarded the Mother Root weekly check-in calendar invite to Pulkit on Mar 9, ensuring continuity of the recurring Wednesday meeting. The Glyphic KT summary from Feb 23 documented the transition. The calendar invite includes both Maddie and Thomas from Mother Root."
    },
    "calls": {
        "recent": [],
        "analysis": "No Glyphic calls found for MOTHER ROOT in the last 30 days. Talia had weekly check-ins with Maddie. Maddie was OOO for two weeks (Feb 20 - early Mar) which partly explains the gap. Since Pulkit's transition on Mar 10, no calls have been logged yet."
    },
    "calendar": {
        "past": [],
        "upcoming": [],
        "_note": "No Google Calendar events found matching 'Mother Root' on Pulkit's calendar between Feb 22 and Apr 30, 2026. However, Talia forwarded the weekly check-in invite (Wednesday 9-9:30pm IST) to Pulkit on Mar 9 — this may need to be accepted or re-created."
    }
})

# ════════════════════════════════════════════════════════════════════════════
# 9. MEDIK8
# ════════════════════════════════════════════════════════════════════════════
update_brand("35845b70-d5ef-4dbf-83cf-e9f327662c17", {
    "slack": {
        "messages": [
            {"user": "Lindsey Shin", "text": "Pulkit these are the assets we are running on our new welcome offer via facebook. can you please use these assets to ideate a fermat landing page so we can use this as the first campaign for fermat?", "timestamp": "2026-03-19T23:55:34+05:30", "channel": "#fermat-x-medik8"},
            {"user": "Pulkit Srivastava", "text": "Thanks for sharing Lindsey and Danielle — I will go ahead and accept the partner invite. You can go ahead with the next steps.", "timestamp": "2026-03-19T23:40:36+05:30", "channel": "#fermat-x-medik8"},
            {"user": "Lindsey Shin", "text": "we sent a partner invite for tiktok integration, can you please accept it?", "timestamp": "2026-03-19T22:20:01+05:30", "channel": "#fermat-x-medik8"},
            {"user": "Pulkit Srivastava", "text": "Hey Lindsey — great connecting today! Recap: Brand Alignment Priority, May Product Launch (May 14th), Testing Strategy, Canada Expansion (late April). Action Items shared for both Medik8 and FERMÀT teams.", "timestamp": "2026-03-16T22:50:42+05:30", "channel": "#fermat-x-medik8"},
            {"user": "Lindsey Shin", "text": "here are the brand guidelines for you!", "timestamp": "2026-03-16T22:48:05+05:30", "channel": "#fermat-x-medik8"},
            {"user": "Pulkit Srivastava", "text": "Hey Lindsey — great connecting today! Here's a quick recap from our kick-off call. Key Funnels: Crystal Retinal Funnel with Octane quiz, Bundle Funnel (C-Tetra + Crystal Retinal). Integrations this week, funnels live before April.", "timestamp": "2026-03-09T20:59:05+05:30", "channel": "#fermat-x-medik8"},
            {"user": "Lindsey Shin", "text": "Pulkit can you add Danielle Finn to this chat?", "timestamp": "2026-03-09T21:02:35+05:30", "channel": "#fermat-x-medik8"},
            {"user": "Mukul Varshney", "text": "Hey Lindsey Shin, welcome to FERMÀT! This will be our main space for quick questions, updates, and everything in between. Also introducing Pulkit, your Account Manager & Primary Point of Contact.", "timestamp": "2026-03-05T19:58:29+05:30", "channel": "#fermat-x-medik8"}
        ],
        "analysis": "Medik8 is a NEW BRAND onboarding with strong momentum. Lindsey Shin is the primary contact with Danielle Finn and Jiyoon Cha also involved. The kick-off call happened Mar 9, with a check-in on Mar 16 where brand guidelines were shared. On Mar 19, Lindsey sent ad creative assets and requested a landing page build, plus shared TikTok partner invite for integration. Major milestones: May 14 product launch, Canada expansion in late April requiring separate FERMÀT account. Weekly sync-ups are scheduled. This is one of the most active and engaged brands in the portfolio."
    },
    "email": {
        "messages": [
            {"from": "Pulkit Srivastava <pulkit@fermatcommerce.com>", "subject": "Re: Medik8 x FERMÀT | Check-in Call Recap", "date": "2026-03-16T17:23:58Z", "snippet": "Pulkit sending check-in call recap to Lindsey, cc'ing Danielle and Jiyoon — brand alignment, May launch, testing strategy, Canada expansion."},
            {"from": "Jiyoon Cha <jiyoon.cha@medik8.com>", "subject": "Accepted: Medik8 x FERMÀT|| Weekly Sync-up @ Tue Apr 7", "date": "2026-03-18T20:25:04Z", "snippet": "Jiyoon accepting weekly sync-up calendar invite for Apr 7."},
            {"from": "Jiyoon Cha <jiyoon.cha@medik8.com>", "subject": "Accepted: Medik8 x FERMÀT|| Weekly Sync-up @ Tue Mar 31", "date": "2026-03-18T20:24:59Z", "snippet": "Jiyoon accepting weekly sync-up calendar invite for Mar 31."},
            {"from": "Jiyoon Cha <jiyoon.cha@medik8.com>", "subject": "Accepted: Medik8 x FERMÀT|| Weekly Sync-up @ Tue Mar 24", "date": "2026-03-17T12:59:48Z", "snippet": "Jiyoon accepting weekly sync-up for Mar 24."},
            {"from": "Danielle Finn <danielle.finn@medik8.com>", "subject": "Accepted: Medik8 x FERMÀT|| Weekly Sync-up", "date": "2026-03-16T17:21:29Z", "snippet": "Danielle accepting recurring weekly sync-up invites."},
            {"from": "Glyphic AI <noreply@glyphic.ai>", "subject": "Medik8 x FERMÀT|| Weekly Sync-up summary is ready", "date": "2026-03-16T17:20:43Z", "snippet": "Glyphic summary of the Mar 16 weekly sync-up with Medik8."},
            {"from": "Lindsey Shin <lindsey.shin@medik8.com>", "subject": "Accepted: Medik8 x FERMÀT|| Weekly Sync-up @ Mon Mar 16", "date": "2026-03-16T14:34:58Z", "snippet": "Lindsey accepting the Mar 16 weekly sync-up."}
        ],
        "analysis": "Strong email activity reflecting an engaged onboarding. Pulkit sent the check-in recap on Mar 16 to Lindsey, Danielle, and Jiyoon. All three Medik8 contacts (Lindsey, Danielle, Jiyoon) have accepted the recurring weekly sync-up invites through April. Glyphic captured the Mar 16 sync-up summary. This is the most active email trail across all brands — a sign of healthy onboarding momentum."
    },
    "calls": {
        "recent": [],
        "analysis": "No calls found via Glyphic title search for 'Medik8' in the last 30 days, though Glyphic captured the Mar 9 kick-off and Mar 16 check-in (visible in email summaries). The calls may be logged under a different title pattern. Weekly sync-ups are confirmed through April with Lindsey, Danielle, and Jiyoon."
    },
    "calendar": {
        "past": [
            {"title": "Medik8 x FERMÀT|| Kick-Off Call", "date": "2026-03-09T20:00:00+05:30", "type": "past"},
            {"title": "Medik8 x FERMÀT|| Weekly Sync-up", "date": "2026-03-16T22:30:00+05:30", "type": "past"}
        ],
        "upcoming": [
            {"title": "Medik8 x FERMÀT|| Weekly Sync-up", "date": "2026-03-24T20:30:00+05:30", "type": "upcoming"},
            {"title": "Medik8 x FERMÀT|| Weekly Sync-up", "date": "2026-03-31T20:30:00+05:30", "type": "upcoming"},
            {"title": "Medik8 x FERMÀT|| Weekly Sync-up", "date": "2026-04-07T20:30:00+05:30", "type": "upcoming"},
            {"title": "Medik8 x FERMÀT|| Weekly Sync-up", "date": "2026-04-14T20:30:00+05:30", "type": "upcoming"}
        ]
    }
})

# ════════════════════════════════════════════════════════════════════════════
# 10. MOMENT
# ════════════════════════════════════════════════════════════════════════════
update_brand("f0a1a21b-3832-4bfd-ad3d-af38d11a90e8", {
    "slack": {
        "messages": [
            {"user": "Moment team member", "text": "wow, cvr is super low / why is that?", "timestamp": "2026-01-12T22:40:31+05:30", "channel": "#fermat-x-moment"},
            {"user": "Pierre (Bot)", "text": "FERMÀT Weekly Roundup Jan 5-11: Sessions 24,512 | Purchases 679 | GMV $47,915 | Revenue $41,785. Top funnel: 3 Reasons Why - Better than Booze (24,361 sessions, $47,915 GMV, 2.79% CVR)", "timestamp": "2026-01-12T22:30:38+05:30", "channel": "#fermat-x-moment"},
            {"user": "Pierre (Bot)", "text": "FERMÀT Weekly Roundup Dec 29 - Jan 4: Sessions 11,126 | Purchases 572 | GMV $39,569 | Revenue $34,477. Top funnel: 3 Reasons Why - Better than Booze (11,044 sessions, 5.14% CVR)", "timestamp": "2026-01-05T22:30:41+05:30", "channel": "#fermat-x-moment"}
        ],
        "analysis": "The Moment Slack channel has been completely silent since Jan 12 — no human messages in over 2 months. Pulkit and the FERMÀT bot joined Feb 24 but no introduction was posted. The brand had strong weekly roundup numbers (24K+ sessions, 679 purchases in one week) driven by the '3 Reasons Why - Better than Booze' funnel. A Moment team member noted low CVR on Jan 12. The channel appears to be running on autopilot with minimal engagement needed, but Pulkit should still introduce himself and build the relationship."
    },
    "email": {
        "messages": [],
        "analysis": "No relevant brand-specific email activity for Moment in the last 30 days. The Gmail search returned unrelated Meta ad approvals and LinkedIn notifications. No direct communications between Pulkit and the Moment team."
    },
    "calls": {
        "recent": [
            {"title": "FERMÀT | Live Momentous", "date": "2026-02-26T20:58:03Z", "duration": "48 min", "participants": "Crystal Haggard, Gillian Roth", "source": "Glyphic", "summary": "Call between FERMÀT (Gillian Roth) and Momentous (Crystal Haggard). Note: This appears to be a different brand (Momentous/livemomentous.com) rather than the Moment brand in this portfolio.", "recording_url": None, "snippets": [], "action_items": []}
        ],
        "analysis": "The Glyphic search returned one call titled 'FERMÀT | Live Momentous' from Feb 26, but this appears to be for a different brand (Momentous/livemomentous.com, not Moment). No calls found specifically for the Moment brand in the portfolio. The brand is managed by Mia DyBuncio's team — Pulkit has not been involved in any calls."
    },
    "calendar": {
        "past": [],
        "upcoming": [],
        "_note": "No Google Calendar events found matching 'Moment' between Feb 22 and Apr 30, 2026 on Pulkit's calendar."
    }
})

# ════════════════════════════════════════════════════════════════════════════
# 11. SHOP FLAVCITY
# ════════════════════════════════════════════════════════════════════════════
update_brand("737444a0-c397-46a8-a53f-8b32d07a1722", {
    "slack": {
        "messages": [
            {"user": "Will (FlavCity)", "text": "Hey Mia sorry I missed the TB, something else came up - do you have a quick 15 on Friday afternoon to chat?", "timestamp": "2026-03-12T13:19:12+05:30", "channel": "#fermat-x-flavcity"},
            {"user": "Will (FlavCity)", "text": "Also meet Christy Hernandez our new head of eCommerce! Mia can you invite her to the meeting - and also find time to set up a 1 on 1 with her!", "timestamp": "2026-03-07T03:57:12+05:30", "channel": "#fermat-x-flavcity"},
            {"user": "Mia DyBuncio", "text": "Hey Ryan Longo, Will — I'll be travelling during our meeting on Monday, any chance we can push this to Wednesday at 3 pm ET?", "timestamp": "2026-03-07T03:01:49+05:30", "channel": "#fermat-x-flavcity"},
            {"user": "Will (FlavCity)", "text": "We want to run a promo just on Fermatt for a few select SKUS but dont want AMZ to price match. Do you know if AMZ will crawl a Fermatt landing page when looking at pricing?", "timestamp": "2026-02-11T04:13:52+05:30", "channel": "#fermat-x-flavcity"},
            {"user": "Will (FlavCity)", "text": "Mia — can you invite Ryan and Connor to this channel? Also adding connor@chiefdetective.com and ryan@chiefdetective.com", "timestamp": "2026-02-18T20:49:32+05:30", "channel": "#fermat-x-flavcity"},
            {"user": "Mia DyBuncio", "text": "Hey Will I saw you went through our AI Search onboarding and generated your first set of funnels! Let me know if you'd like to hop on a call to review your visibility score.", "timestamp": "2026-01-27T22:14:27+05:30", "channel": "#fermat-x-flavcity"}
        ],
        "analysis": "FlavCity is actively managed by Mia DyBuncio (not transitioned to Pulkit). The brand is highly engaged with regular weekly meetings. A new head of eCommerce (Christy Hernandez) joined in early March. The brand's agency partners (Chief Detective — Ryan Longo, Connor, Nate Lee; Ecko Digital Media — Sammie) are also active in the channel. Will asked about Amazon price matching on FERMÀT-exclusive promos (Feb 11). Will completed AI Search onboarding (Jan 27). Pulkit is not the GM for this brand — Mia continues to manage it."
    },
    "email": {
        "messages": [],
        "analysis": "No email activity found for FlavCity in the last 30 days on Pulkit's inbox. This is expected as Mia DyBuncio manages this account."
    },
    "calls": {
        "recent": [
            {"title": "Flavcity x Fermat", "date": "2026-03-13T19:58:03Z", "duration": "30 min", "participants": "Mia DyBuncio, Will, Christy Hernandez", "source": "Glyphic", "summary": "Meeting between Mia and FlavCity team including new head of eCommerce Christy Hernandez.", "recording_url": None, "snippets": [], "action_items": []},
            {"title": "FlavCity x Fermat Weekly", "date": "2026-03-11T18:58:03Z", "duration": "19 min", "participants": "Christy, Ryan Longo, Kaitlin Frye, Mia DyBuncio, Sammie Walker, Will, Megan Hart, Thi Tran, Marie Leroux, Eddie, Ryan Barry, Travis Halff", "source": "Glyphic", "summary": "Weekly meeting with full FlavCity team and agency partners (Chief Detective, Ecko Digital Media, Y'all).", "recording_url": None, "snippets": [], "action_items": []},
            {"title": "Fermat x FlavCity - Platform Walkthrough", "date": "2026-02-23T19:28:04Z", "duration": "17 min", "participants": "Mia DyBuncio, SarahJay Kucyk", "source": "Glyphic", "summary": "Platform walkthrough with agency partner.", "recording_url": None, "snippets": [], "action_items": []},
            {"title": "FlavCity x Fermat Weekly", "date": "2026-02-23T18:58:04Z", "duration": "16 min", "participants": "Ryan Longo, Mia DyBuncio, Will, Marie Leroux, Sammie Walker, Megan Hart, Eddie, Ryan Barry, Thi Tran, Travis Halff", "source": "Glyphic", "summary": "Regular weekly meeting with FlavCity team and agency partners.", "recording_url": None, "snippets": [], "action_items": []}
        ],
        "analysis": "FlavCity has an active call cadence with weekly meetings managed by Mia DyBuncio. Four calls were recorded in the last 30 days, including a platform walkthrough with agency partner SarahJay Kucyk (Feb 23), two weekly meetings (Feb 23, Mar 11), and a separate meeting with new eCommerce head Christy Hernandez (Mar 13). The team includes multiple agency partners (Chief Detective, Ecko Digital Media, Y'all)."
    },
    "calendar": {
        "past": [],
        "upcoming": [],
        "_note": "No Google Calendar events found matching 'FlavCity' on Pulkit's calendar. This brand is managed by Mia DyBuncio."
    }
})

# ════════════════════════════════════════════════════════════════════════════
# 12. SOLE TOSCANA
# ════════════════════════════════════════════════════════════════════════════
update_brand("c686cb26-9441-4aa2-883e-7204999f2bc4", {
    "slack": {
        "messages": [
            {"user": "Preston (Sole Toscana)", "text": "Hi Pulkit, I just scheduled a time on your calendar for next week. Looking forward to meeting you!", "timestamp": "2026-03-04T22:20:49+05:30", "channel": "#fermat-x-sole-toscana"},
            {"user": "Pulkit Srivastava", "text": "Hey Sole Toscana team! I'm Pulkit, your new GM here at FERMÀT. I've been with the FERMÀT team for about 1.5 years and I'm genuinely so excited to start working with you all!", "timestamp": "2026-03-04T08:45:49+05:30", "channel": "#fermat-x-sole-toscana"},
            {"user": "Mia DyBuncio", "text": "Hey Preston! As mentioned on our call earlier I'm transitioning to our Product team at FERMÀT so I'm excited to introduce Pulkit as your new Growth Manager!", "timestamp": "2026-03-04T01:41:49+05:30", "channel": "#fermat-x-sole-toscana"},
            {"user": "Pierre (Bot)", "text": "FERMÀT Weekly Roundup Jan 5-11: Sessions 2,180 | Purchases 54 | GMV $8,187 | Revenue $7,079. Top funnel: Sole Toscana Shop Returning Customers (219 sessions, 11.87% CVR, $14.76 Rev/Session)", "timestamp": "2026-01-12T22:30:26+05:30", "channel": "#fermat-x-sole-toscana"}
        ],
        "analysis": "Sole Toscana has Preston as the sole brand contact, and he responded quickly and positively to Pulkit's introduction on Mar 4, immediately scheduling a call. The GM transition from Mia to Pulkit was announced Mar 4. Preston booked time on Pulkit's calendar for Mar 10 and also accepted a recurring monthly meeting. The brand shows excellent retention funnel performance (11.87% CVR for returning customers). This is a healthy, engaged account with smooth GM transition."
    },
    "email": {
        "messages": [
            {"from": "Preston Alder <preston@soletoscana.com>", "subject": "Accepted: Sole Toscana x FERMÀT||Monthly @ Monthly from 9pm to 9:30pm on the second Tuesday", "date": "2026-03-12T18:12:31Z", "snippet": "Preston accepting the recurring monthly meeting invite."},
            {"from": "Glyphic AI <noreply@glyphic.ai>", "subject": "Preston (Sole Toscana) and Pulkit Srivastava summary is ready", "date": "2026-03-10T15:49:05Z", "snippet": "Glyphic summary of the Mar 10 introductory call between Preston and Pulkit."},
            {"from": "Preston Alder <preston@soletoscana.com>", "subject": "Accepted: Preston (Sole Toscana) and Pulkit Srivastava @ Tue Mar 10, 2026", "date": "2026-03-04T16:52:45Z", "snippet": "Preston accepting the introductory call invite for Mar 10."}
        ],
        "analysis": "Strong email engagement for Sole Toscana. Preston accepted the Mar 10 introductory call with Pulkit, and the Glyphic summary was generated. Preston also accepted the recurring monthly meeting (second Tuesday at 9pm IST). Meta ad approvals show Pulkit is running ads for Sole Toscana's FERMÀT funnels."
    },
    "calls": {
        "recent": [
            {"title": "Sole Toscana x Fermat", "date": "2026-03-03T17:58:10Z", "duration": "13 min", "participants": "Mia DyBuncio, Preston, Sarah", "source": "Glyphic", "summary": "Mia's final call with Preston as she transitions to the Product team. Introduced the upcoming transition to Pulkit and discussed current funnel performance.", "recording_url": None, "snippets": [], "action_items": []}
        ],
        "analysis": "One call found in the last 30 days — Mia's Mar 3 transition call with Preston (13 min). The Glyphic summary from Mar 10 (visible in email) indicates Pulkit had an introductory call with Preston that day, though it wasn't captured under the 'Sole Toscana' title filter. Monthly recurring calls have been set up."
    },
    "calendar": {
        "past": [
            {"title": "Sole Toscana x FERMÀT||Monthly", "date": "2026-03-10T21:00:00+05:30", "type": "past"}
        ],
        "upcoming": [
            {"title": "Sole Toscana x FERMÀT||Monthly", "date": "2026-04-14T21:00:00+05:30", "type": "upcoming"}
        ]
    }
})

# ════════════════════════════════════════════════════════════════════════════
# 13. VERACITY SELFCARE
# ════════════════════════════════════════════════════════════════════════════
update_brand("f8f83f9d-be9e-4177-ad7e-292ed079eafd", {
    "slack": {
        "messages": [
            {"user": "Veracity team member", "text": "hey team - are you able to share what SKUs/variants are being used on the fermat side? trying to do a cleanup of some of our promo SKUs", "timestamp": "2026-02-18T03:15:11+05:30", "channel": "#fermat-x-veracitywellness"},
            {"user": "Veracity team member", "text": "hey Mia! mind if we push this meeting out to next week?", "timestamp": "2026-01-29T22:09:35+05:30", "channel": "#fermat-x-veracitywellness"},
            {"user": "Mia DyBuncio", "text": "hey Maggie Sullivan it looks like the singular protein sku hasn't been shared with fermat, i'm only seeing the metabolism + protein power set. could you help share this over?", "timestamp": "2026-01-16T22:15:39+05:30", "channel": "#fermat-x-veracitywellness"},
            {"user": "Mia DyBuncio", "text": "Hi team, thanks for the time today! Recap: subdomain change notified to engineering, protein SKU sharing, two protein landing pages for 1/15, rebrand images across funnels pending go-ahead.", "timestamp": "2026-01-06T02:28:17+05:30", "channel": "#fermat-x-veracitywellness"}
        ],
        "analysis": "The Veracity Selfcare channel has been quiet since Feb 18 when a team member asked about SKUs/variants in use. Pulkit and the FERMÀT bot joined Feb 24 but no introduction message was posted. The brand team includes Jacqueline Lin, Maggie Sullivan, and Yuliia (agency). Mia was managing the account with weekly calls and active funnel work (protein landing pages, rebrand). Since Pulkit's transition, there has been zero engagement — an introduction message is urgently needed."
    },
    "email": {
        "messages": [],
        "analysis": "No email activity found for Veracity Selfcare in the last 30 days. No direct communications between Pulkit and the Veracity team."
    },
    "calls": {
        "recent": [
            {"title": "Fermat x Veracity", "date": "2026-02-26T16:58:10Z", "duration": "7 min", "participants": "Mia DyBuncio, Jacqueline Lin, Adaeze, Yuliia, James, Sabrina Pereira, Maggie Sullivan", "source": "Glyphic", "summary": "Cancelled call — 7 minutes of brief connection before cancellation. Full team was present but no substantive discussion.", "recording_url": None, "snippets": [], "action_items": []}
        ],
        "analysis": "One call found but it was cancelled (only 7 min). This was Mia's last scheduled call with the Veracity team on Feb 26, with full team present but no substantive discussion. Since Pulkit's transition, no calls have been initiated. The brand had weekly calls with Mia — this cadence has completely dropped off."
    },
    "calendar": {
        "past": [],
        "upcoming": [],
        "_note": "No Google Calendar events found matching 'Veracity' between Feb 22 and Apr 30, 2026 on Pulkit's calendar."
    }
})

# ════════════════════════════════════════════════════════════════════════════
# 14. WESTMORE BEAUTY
# ════════════════════════════════════════════════════════════════════════════
update_brand("508e7756-81aa-48b1-bbf5-765d2e8f1eb9", {
    "slack": {
        "messages": [
            {"user": "Talia Cohen", "text": "Cross posting call update: Hi Jessica and Brenda! Confirming invites have been reshared to our Slack channel. Key Takeaways: 60 Second Eye Effect funnel to match paid social offer page, Body Coverage Perfector funnel next, integrations complete (Google Ads, GA4, Klaviyo).", "timestamp": "2026-02-14T00:20:17+05:30", "channel": "#fermat-x-westmorebeauty"},
            {"user": "Jessica Tennant", "text": "can you please add us as members from the admin? We don't use slack internally and are having issues accessing slack past a free trial period", "timestamp": "2026-02-10T03:21:37+05:30", "channel": "#fermat-x-westmorebeauty"},
            {"user": "Talia Cohen", "text": "Hi jtennant - cross-posting my email here. Ahead of our call tomorrow, please make sure Dashboard Setup and Integrations (Shopify, GA4, Meta) are completed.", "timestamp": "2026-02-05T00:16:27+05:30", "channel": "#fermat-x-westmorebeauty"}
        ],
        "analysis": "Westmore Beauty is a NEW BRAND in early onboarding. The Slack channel was set up by Talia in early Feb with Jessica Tennant (VP eCommerce & Growth) and Brenda Hernandez as contacts. Jessica had Slack access issues (free trial period expiring) and was re-invited. Talia ran the kick-off call on Feb 13 covering the 60 Second Eye Effect and Body Coverage Perfector funnels. Pulkit joined the channel and has been handling follow-ups via email. The brand is currently focused on a rebrand which is delaying funnel testing."
    },
    "email": {
        "messages": [
            {"from": "Pulkit Srivastava <pulkit@fermatcommerce.com>", "subject": "Re: FERMÀT <> Westmore Beauty | Call Recap 2/13", "date": "2026-03-18T17:51:21Z", "snippet": "Pulkit acknowledging Jessica's rebrand update and offering to help when ready."},
            {"from": "Jessica Tennant <jtennant@westmorebeauty.com>", "subject": "Re: FERMÀT <> Westmore Beauty | Call Recap 2/13", "date": "2026-03-18T16:59:08Z", "snippet": "Jessica explaining they've been deep in rebrand which requires updating all creative. Haven't started testing funnels yet."},
            {"from": "Pulkit Srivastava <pulkit@fermatcommerce.com>", "subject": "Re: FERMÀT <> Westmore Beauty | Call Recap 2/13", "date": "2026-03-18T16:24:31Z", "snippet": "Pulkit following up to check if Jessica has tested the updated funnels."},
            {"from": "Pulkit Srivastava <pulkit@fermatcommerce.com>", "subject": "Re: FERMÀT <> Westmore Beauty | Call Recap 2/13", "date": "2026-03-16T10:51:28Z", "snippet": "Pulkit following up on funnel testing progress."},
            {"from": "Jessica Tennant <jtennant@westmorebeauty.com>", "subject": "Re: FERMÀT <> Westmore Beauty | Call Recap 2/13", "date": "2026-03-13T01:24:50Z", "snippet": "Jessica saying 'Thank you so much! Going to dive in now!' regarding updated funnels."},
            {"from": "Pulkit Srivastava <pulkit@fermatcommerce.com>", "subject": "Re: FERMÀT <> Westmore Beauty | Call Recap 2/13", "date": "2026-03-11T18:17:10Z", "snippet": "Pulkit sharing updated funnel flows based on Jessica's feedback for both 60 Second Eye Effect and Body Coverage Perfector."},
            {"from": "Glyphic AI <noreply@glyphic.ai>", "subject": "Jessica Tennant and Pulkit Srivastava summary is ready", "date": "2026-03-11T16:34:54Z", "snippet": "Glyphic summary of the Mar 11 call between Jessica and Pulkit."}
        ],
        "analysis": "Active email thread with Westmore Beauty. Pulkit had a call with Jessica on Mar 11 (Glyphic captured summary), then sent updated funnel flows. Jessica was enthusiastic ('Going to dive in now!' on Mar 13) but by Mar 18 explained she hasn't tested because they're deep in a rebrand that requires updating all creative. Pulkit has been consistently following up (Mar 11, 13, 16, 18). The brand is engaged but delayed by internal rebrand work."
    },
    "calls": {
        "recent": [],
        "analysis": "No Glyphic calls found under 'Westmore' title in the last 30 days, though the email data confirms a call happened on Mar 11 between Jessica Tennant and Pulkit (Glyphic summary was generated). The call likely was titled differently."
    },
    "calendar": {
        "past": [],
        "upcoming": [],
        "_note": "No Google Calendar events found matching 'Westmore' between Feb 22 and Apr 30, 2026 on Pulkit's calendar. The brand is in early onboarding and currently delayed by their rebrand."
    }
})

# ════════════════════════════════════════════════════════════════════════════
# 15. BELLIWELLI
# ════════════════════════════════════════════════════════════════════════════
update_brand("39f04705-e991-461e-a98f-2dd3f29d6e47", {
    "slack": {
        "messages": [
            {"user": "Pulkit Srivastava", "text": "Hey Tom Fitz — great call today! Performance: Revenue $28K (30d), Subscription Rate 56% (30% above benchmark), CVR 1.38% (targeting 3%). Top Performer: Best Seller GLP-1 funnel with 29K sessions. Action Items shared for both teams.", "timestamp": "2026-03-23T22:02:46+05:30", "channel": "#belliwelli-fermàt-new"},
            {"user": "Tom Fitz", "text": "CODE RED — this page is 404ing. What's going on?? (shop.belliwelli.com link)", "timestamp": "2026-03-18T17:12:52+05:30", "channel": "#belliwelli-fermàt-new"},
            {"user": "Tom Fitz", "text": "Checked the url in my mobile chrome browser and saw the same 404", "timestamp": "2026-03-18T17:14:26+05:30", "channel": "#belliwelli-fermàt-new"},
            {"user": "Tom Fitz", "text": "Talia, Pulkit — We've been running this experiment since Friday and still no data is showing up", "timestamp": "2026-03-11T22:10:36+05:30", "channel": "#belliwelli-fermàt-new"},
            {"user": "Tom Fitz", "text": "Talia, Pulkit - would you be able to look into this pdp and advise why the wrong lead image is pulling?", "timestamp": "2026-02-26T01:35:07+05:30", "channel": "#belliwelli-fermàt-new"},
            {"user": "Tom Fitz", "text": "Talia congratulations on your new role! Pulkit good to meet you and looking forward to working together. I'll grab a call on your calendar now", "timestamp": "2026-02-25T22:51:10+05:30", "channel": "#belliwelli-fermàt-new"},
            {"user": "Pulkit Srivastava", "text": "Hey BelliWelli team! I'm Pulkit, your new GM here at FERMÀT.", "timestamp": "2026-02-25T20:47:10+05:30", "channel": "#belliwelli-fermàt-new"},
            {"user": "Talia Cohen", "text": "Hey BelliWelli team! I'm transitioning into a new role on our Enterprise team. I'm thrilled to introduce Pulkit.", "timestamp": "2026-02-25T19:30:22+05:30", "channel": "#belliwelli-fermàt-new"},
            {"user": "Talia Cohen", "text": "Hey Tom Fitz - thanks for the time earlier today! Sending performance analysis and recommendations for 'Best Sellers | GLP1' and 'Gummies GLP1 | Version 1'. Also reminder: contract rolls into remainder on February 22nd.", "timestamp": "2026-02-20T02:35:33+05:30", "channel": "#belliwelli-fermàt-new"},
            {"user": "Tom Fitz", "text": "We just set up a test running half traffic to Fermat, half to the website. How do we determine if the test is winning?", "timestamp": "2026-02-11T04:30:53+05:30", "channel": "#belliwelli-fermàt-new"}
        ],
        "analysis": "Belliwelli is one of the most actively engaged brands with Tom Fitz as the primary contact and Morry also involved. Pulkit had a bi-weekly call on Mar 23 and posted a detailed recap with performance data ($28K revenue, 56% subscription rate). There have been urgent issues — a 404 error on Mar 18 (CODE RED) and experiment data not showing on Mar 11. Tom was quick to engage with Pulkit after the GM transition on Feb 25, immediately booking a call. The brand has bi-weekly recurring calls and is actively running experiments and split tests. Contract renewed past the Feb 22 opt-in date."
    },
    "email": {
        "messages": [
            {"from": "Glyphic AI <noreply@glyphic.ai>", "subject": "Belliwelli x FERMÀT|| Bi-Weekly summary is ready", "date": "2026-03-23T16:31:33Z", "snippet": "Glyphic summary of today's (Mar 23) bi-weekly call with BelliWelli."},
            {"from": "Tom Fitzpatrick (via Google Sheets)", "subject": "Spreadsheet shared with you: BELLIWELLI CREATIVE PIPELINE", "date": "2026-03-23T16:13:24Z", "snippet": "Tom sharing the BelliWelli creative pipeline spreadsheet with Pulkit for ad-to-funnel mapping."},
            {"from": "Zoom <no-reply@zoom.us>", "subject": "FERMÀT Copilot has joined your meeting - Belliwelli x FERMÀT|| Bi-Weekly", "date": "2026-03-23T15:58:27Z", "snippet": "Zoom notification for bi-weekly meeting."},
            {"from": "Nidhi Singh <nidhi@fermatcommerce.com>", "subject": "Accepted: Belliwelli x FERMÀT|| Bi-Weekly @ Mon Mar 23", "date": "2026-03-23T09:40:54Z", "snippet": "Nidhi (FERMÀT) accepting the bi-weekly meeting invite."}
        ],
        "analysis": "Strong email activity for BelliWelli. The Mar 23 bi-weekly call happened today — Glyphic captured the summary, Tom shared the creative pipeline spreadsheet. Nidhi Singh (FERMÀT) is also involved in the calls. Multiple Meta ad approval emails show Pulkit is actively running ads for BelliWelli's FERMÀT funnels. The brand is highly active with consistent bi-weekly cadence."
    },
    "calls": {
        "recent": [],
        "analysis": "No Glyphic calls found under 'belliwelli' title search, but email data confirms bi-weekly calls are happening (Mar 9, Mar 23). The Glyphic summary from Mar 23 was generated. Calls may be logged under a different title or the Glyphic search is case-sensitive. The bi-weekly cadence is confirmed through calendar data."
    },
    "calendar": {
        "past": [
            {"title": "Belliwelli x FERMÀT|| Bi-Weekly", "date": "2026-03-09T21:30:00+05:30", "type": "past"},
            {"title": "Belliwelli x FERMÀT|| Bi-Weekly", "date": "2026-03-23T21:30:00+05:30", "type": "past"}
        ],
        "upcoming": [
            {"title": "Belliwelli x FERMÀT|| Bi-Weekly", "date": "2026-04-06T21:30:00+05:30", "type": "upcoming"},
            {"title": "Belliwelli x FERMÀT|| Bi-Weekly", "date": "2026-04-20T21:30:00+05:30", "type": "upcoming"}
        ]
    }
})

print("\n All 15 brands updated successfully!")
