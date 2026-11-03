#!/usr/bin/env python3
"""Generates the Butler Legal Services static site.
Edit the CONFIG block, then run:  python3 build_site.py <output-dir>
Anything set to None is left out of the site (phone, address, analytics, social links)."""
import sys, os, json, html, datetime

# ---------------- CONFIG ----------------
SITE = "https://butlerlegalservices.ca"
NAME = "Butler Legal Services"
EMAIL = "hello@butlerlegalservices.ca"
LICENSEE = "Sierra Walker"          # name as it appears on the LSO licence (see README note)
PHONE = ("(289) 312-0277", "+12893120277")  # e.g. ("(905) 555-0123", "+19055550123"); None hides every phone link and the mobile Call button
ADDRESS = None                      # e.g. "123 Example St, Ajax, ON L1S 0A0"; None leaves it out
GA_ID = None                        # e.g. "G-XXXXXXXXXX"; None leaves out Google Analytics
INSTAGRAM = None                    # full URL or None
TIKTOK = None                       # full URL or None
SERVICE_AREA = "clients across Ontario, virtually and in person"
SISTER_URL = "https://notablenotary.ca"
SISTER_REVIEWS_URL = "https://share.google/GvSFvuqAJfzFqtLcJ"
BOOKING_URL = None                  # payment/booking link for the paid consultation; None shows the contact form only
# Prices are left out until you decide them. Fill in any of these, e.g. "$150" or "From $350".
PRICES = {"free_call": None, "strategy": "$75, HST included", "limited_task": None, "single_appearance": None, "ticket": None, "minor_criminal": None, "small_claims": None}
FREE_CALL_LENGTH = "15 minutes"
STRATEGY_LENGTH = "30 minutes"
TODAY = "2026-10-30"
# ----------------------------------------

OUT = sys.argv[1]
os.makedirs(OUT, exist_ok=True)

ICONS = {
 "car": '<path d="M5 17h14M3 13l2-6a2 2 0 0 1 2-1h10a2 2 0 0 1 2 1l2 6v4h-3v-2H6v2H3z"/><circle cx="7.5" cy="13.5" r=".6"/><circle cx="16.5" cy="13.5" r=".6"/>',
 "doc": '<path d="M14 3H7a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h10a2 2 0 0 0 2-2V8z"/><path d="M14 3v5h5M9 13h6M9 17h6"/>',
 "scale": '<path d="M12 3v18M6 21h12M5 7h14"/><path d="M5 7l-3 7a3.5 3.5 0 0 0 6 0zM19 7l-3 7a3.5 3.5 0 0 0 6 0z"/>',
 "shield": '<path d="M12 3l8 3v6c0 5-3.5 8-8 9-4.5-1-8-4-8-9V6z"/><path d="M9 12l2 2 4-4"/>',
 "clock": '<circle cx="12" cy="12" r="9"/><path d="M12 7v5l3 2"/>',
 "check": '<circle cx="12" cy="12" r="9"/><path d="M8 12l3 3 5-6"/>',
 "pin": '<path d="M12 21s7-6.2 7-11a7 7 0 0 0-14 0c0 4.8 7 11 7 11z"/><circle cx="12" cy="10" r="2.5"/>',
 "award": '<circle cx="12" cy="9" r="6"/><path d="M8.5 14L7 22l5-3 5 3-1.5-8"/>',
 "phone": '<path d="M22 16.9v3a2 2 0 0 1-2.2 2 19.8 19.8 0 0 1-8.6-3.1 19.5 19.5 0 0 1-6-6A19.8 19.8 0 0 1 2.1 4.2 2 2 0 0 1 4.1 2h3a2 2 0 0 1 2 1.7c.1 1 .4 1.9.7 2.8a2 2 0 0 1-.5 2.1L8.1 9.9a16 16 0 0 0 6 6l1.3-1.3a2 2 0 0 1 2.1-.4c.9.3 1.8.6 2.8.7a2 2 0 0 1 1.7 2z"/>',
 "menu": '<path d="M4 7h16M4 12h16M4 17h16"/>',
 "chat": '<path d="M21 12a8 8 0 0 1-11.7 7L4 20l1.1-4.4A8 8 0 1 1 21 12z"/>',
 "compass": '<circle cx="12" cy="12" r="9"/><path d="M15.5 8.5l-2 5-5 2 2-5z"/>',
 "heart": '<path d="M12 20s-7-4.4-7-10a4 4 0 0 1 7-2.5A4 4 0 0 1 19 10c0 5.6-7 10-7 10z"/>',
 "globe": '<circle cx="12" cy="12" r="9"/><path d="M3 12h18M12 3a14 14 0 0 1 0 18M12 3a14 14 0 0 0 0 18"/>',
 "cal": '<rect x="3" y="5" width="18" height="16" rx="2"/><path d="M16 3v4M8 3v4M3 11h18"/>',
}
def ic(name, cls="icon"):
    return f'<svg class="{cls}" viewBox="0 0 24 24" aria-hidden="true">{ICONS[name]}</svg>'

def esc(s): return html.escape(s, quote=True)

NAV = [
 ("Services", "/services", [("All Services","/services"),("Small Claims Court","/small-claims-court"),("Traffic Tickets & Highway Offences","/traffic-tickets"),("Minor Criminal Offences","/minor-criminal-offences"),("Provincial Offences","/provincial-offences"),("Limited Scope Services","/limited-scope-services")]),
 ("About", "/about", None),
 ("FAQ", "/faq", None),
 ("Contact", "/contact", None),
]

def header(active):
    items = []
    for label, href, sub in NAV:
        cls = "nav-item" + (" active" if active == href else "")
        if sub:
            dd = "".join(f'<a href="{h}">{esc(l)}</a>' for l, h in sub)
            items.append(f'<div class="{cls}"><a href="{href}">{label}</a><span class="caret">&#9662;</span><div class="dropdown">{dd}</div></div>')
        else:
            items.append(f'<div class="{cls}"><a href="{href}">{label}</a></div>')
    phone = f'<a class="nav-phone" href="tel:{PHONE[1]}">{PHONE[0]}</a>' if PHONE else ""
    mm = []
    for label, href, sub in NAV:
        mm.append(f'<a href="{href}">{label}</a>')
        if sub:
            mm += [f'<a class="sub" href="{h}">{esc(l)}</a>' for l, h in sub[1:]]
    if PHONE:
        mm.append(f'<a href="tel:{PHONE[1]}">Call {PHONE[0]}</a>')
    mm.append('<a class="btn btn-primary" href="/contact" style="color:#fff;border:0">Book a Consultation</a>')
    return f'''<a class="skip" href="#main">Skip to content</a>
<nav class="top" aria-label="Main">
  <a class="logo-link" href="/"><img src="/logo-horizontal.png" alt="{NAME}" width="215" height="50"></a>
  <div class="nav-links">{"".join(items)}</div>
  <div class="nav-btns">{phone}<a class="btn btn-primary" href="/contact">Book a Consultation</a>
  <button class="menu-toggle" aria-label="Menu" aria-expanded="false" onclick="var m=document.getElementById('mm');var o=m.classList.toggle('open');this.setAttribute('aria-expanded',o)">{ic("menu")}</button></div>
</nav>
<div class="mobile-menu" id="mm">{"".join(mm)}</div>'''

DISCLAIMER = (f"{NAME} provides legal services through {LICENSEE}, a paralegal licensed and regulated by the Law Society of Ontario. "
  "Services are provided by a licensed paralegal, not a lawyer, and only within the scope of practice the Law Society permits paralegals. "
  "This website offers general information, not legal advice about your situation. Visiting this site or sending a message does not create a paralegal-client relationship; "
  "that begins only when a written retainer is signed after a conflict check. Please do not send confidential details or documents through the contact form until it is confirmed that Butler Legal Services can act for you. "
  "Past results do not predict future outcomes, and no outcome is guaranteed. Notable Notary is a separate, sister business and its services are not paralegal services.")

def footer():
    contact = [f'<div><a href="mailto:{EMAIL}">{EMAIL}</a></div>']
    if PHONE: contact.insert(0, f'<div><a href="tel:{PHONE[1]}">{PHONE[0]}</a></div>')
    contact.append(f'<div>{esc(ADDRESS) if ADDRESS else "Ajax, Ontario"}</div>')
    social = ""
    if INSTAGRAM: social += f'<div><a href="{INSTAGRAM}" rel="noopener">Instagram</a></div>'
    if TIKTOK: social += f'<div><a href="{TIKTOK}" rel="noopener">TikTok</a></div>'
    return f'''<footer>
  <div class="footer-top">
    <div class="footer-brand"><img src="/logo-horizontal.png" alt="{NAME}" width="189" height="44">
      <p>Licensed paralegal services for Small Claims Court, traffic tickets, minor criminal and provincial offences.</p>
      <p>Representing {SERVICE_AREA}.</p></div>
    <div class="footer-col"><h5>Services</h5><div><a href="/small-claims-court">Small Claims Court</a></div><div><a href="/traffic-tickets">Traffic Tickets</a></div><div><a href="/minor-criminal-offences">Minor Criminal</a></div><div><a href="/provincial-offences">Provincial Offences</a></div><div><a href="/limited-scope-services">Limited Scope</a></div></div>
    <div class="footer-col"><h5>Popular</h5><div><a href="/speeding-ticket-ontario">Speeding Tickets</a></div><div><a href="/stunt-driving-charge-ontario">Stunt Driving</a></div><div><a href="/careless-driving-charge-ontario">Careless Driving</a></div><div><a href="/defend-small-claims-claim-ontario">Been Sued?</a></div><div><a href="/unpaid-invoice-small-claims-ontario">Unpaid Invoices</a></div></div>
    <div class="footer-col"><h5>Company</h5><div><a href="/about">About</a></div><div><a href="/faq">FAQ</a></div><div><a href="/paralegal-durham-region">Ajax &amp; Durham</a></div><div><a href="/contact">Contact</a></div><div><a href="{SISTER_URL}" rel="noopener">Sister company: Notable Notary</a></div></div>
    <div class="footer-col"><h5>Contact</h5>{"".join(contact)}{social}</div>
  </div>
  <div class="footer-bottom"><span>&copy; 2026 {NAME}. All rights reserved.</span>
    <span><a href="/privacy-policy">Privacy Policy</a><a href="/terms-conditions">Terms &amp; Conditions</a></span></div>
  <div class="footer-disclaimer" data-nosnippet>{DISCLAIMER}</div>
</footer>
{f'<a class="call-fab" href="tel:{PHONE[1]}">{ic("phone")} Call</a>' if PHONE else ''}'''

def cta(title="Not sure where you stand? Start with a conversation.", text="Tell me about your ticket or claim. I will reply with next steps, the deadlines that apply, and a written fee quote."):
    ph = f'<a class="btn btn-outline-white" href="tel:{PHONE[1]}">Call {PHONE[0]}</a>' if PHONE else ""
    return f'<section class="cta-band"><h2>{title}</h2><p>{text}</p><div class="row"><a class="btn btn-gold" href="/contact">Book a Consultation</a>{ph}</div></section>'

def ld(obj): return '<script type="application/ld+json">' + json.dumps(obj, ensure_ascii=False) + '</script>'

def org_schema():
    o = {"@type":"LegalService","@id":SITE+"/#org","name":NAME,"url":SITE+"/","logo":SITE+"/logo.png","image":SITE+"/og-image.jpg",
         "email":EMAIL,"description":"Licensed paralegal providing Small Claims Court, traffic ticket and highway offence, minor criminal and provincial offences representation across Ontario, virtually and in person.",
         "address":{"@type":"PostalAddress","addressLocality":"Ajax","addressRegion":"ON","addressCountry":"CA"},
         "areaServed":{"@type":"AdministrativeArea","name":"Ontario"},
         "knowsAbout":["Small Claims Court","Traffic tickets","Highway Traffic Act offences","Provincial Offences Act","Minor criminal offences","Limited scope legal services"],
         "founder":{"@id":SITE+"/#sierra"},
         "makesOffer":[{"@type":"Offer","itemOffered":{"@type":"Service","name":n}} for n in ("Small Claims Court representation","Traffic ticket and highway offence defence","Minor criminal offence representation","Provincial offences representation","Limited scope legal services","Strategy consultation")]}
    if PHONE: o["telephone"] = PHONE[1]
    if ADDRESS: o["address"]["streetAddress"] = ADDRESS.split(",")[0]
    p = {"@type":"Person","@id":SITE+"/#sierra","name":LICENSEE,"jobTitle":"Licensed Paralegal and Founder","worksFor":{"@id":SITE+"/#org"},
         "affiliation":[{"@type":"Organization","name":"Law Society of Ontario"},{"@type":"Organization","name":"Ontario Association of Black Paralegals"}],
         "image":SITE+"/sierra.jpg"}
    return ld({"@context":"https://schema.org","@graph":[o,p]})

def service_schema(name, desc, path):
    return ld({"@context":"https://schema.org","@type":"Service","name":name,"description":desc,"url":SITE+path,
               "provider":{"@id":SITE+"/#org"},"areaServed":{"@type":"AdministrativeArea","name":"Ontario"},"serviceType":name})

def byline():
    return f'<p class="byline">Written and reviewed by {LICENSEE}, Licensed Paralegal. Last updated October 30, 2026. General information only, not legal advice.</p>'

def related(items):
    return '<div class="related"><h3>Related</h3><ul>' + "".join(f'<li><a href="{h}">{t}</a></li>' for h, t in items) + '</ul></div>'

def crumbs_schema(path, label):
    return ld({"@context":"https://schema.org","@type":"BreadcrumbList","itemListElement":[
        {"@type":"ListItem","position":1,"name":"Home","item":SITE+"/"},
        {"@type":"ListItem","position":2,"name":label,"item":SITE+path}]})

PAGES = []
def page(path, title, desc, body, active="", extra="", noindex=False, hero_html=""):
    PAGES.append(dict(path=path, title=title, desc=desc, body=body, active=active, extra=extra, noindex=noindex))

def render(p):
    url = SITE + (p["path"] if p["path"] != "/" else "/")
    t = esc(p["title"]); d = esc(p["desc"])
    ga = (f'<script async src="https://www.googletagmanager.com/gtag/js?id={GA_ID}"></script>\n<script>window.dataLayer=window.dataLayer||[];function gtag(){{dataLayer.push(arguments);}}gtag("js",new Date());gtag("config","{GA_ID}");</script>') if GA_ID else "<!-- Google Analytics: set GA_ID in build_site.py to add it -->"
    robots = '<meta name="robots" content="noindex, follow">\n' if p["noindex"] else ""
    return f'''<!DOCTYPE html>
<html lang="en-CA">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="format-detection" content="telephone=no">
{ga}
<title>{t}</title>
<meta name="description" content="{d}">
{robots}<link rel="canonical" href="{url}">
<link rel="icon" href="/favicon.ico">
<link rel="icon" type="image/png" sizes="48x48" href="/favicon-48x48.png">
<link rel="icon" type="image/png" sizes="32x32" href="/favicon-32x32.png">
<link rel="icon" type="image/png" sizes="16x16" href="/favicon-16x16.png">
<link rel="apple-touch-icon" sizes="180x180" href="/apple-touch-icon.png">
<link rel="manifest" href="/site.webmanifest">
<meta name="theme-color" content="#7A1F3D">
<meta property="og:title" content="{t}">
<meta property="og:description" content="{d}">
<meta property="og:type" content="website">
<meta property="og:url" content="{url}">
<meta property="og:image" content="{SITE}/og-image.jpg">
<meta property="og:site_name" content="{NAME}">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{t}">
<meta name="twitter:description" content="{d}">
<meta name="twitter:image" content="{SITE}/og-image.jpg">
<link rel="stylesheet" href="/styles.css">
{p["extra"]}
</head>
<body>
{header(p["active"])}
<main id="main">
{p["body"]}
</main>
{footer()}
</body>
</html>
'''

def faq_html(items):
    return '<div class="faq">' + "".join(f'<details><summary>{q}</summary><p>{a}</p></details>' for q, a in items) + '</div>'

def faq_schema(items):
    import re
    strip = lambda s: re.sub(r"<[^>]+>", "", html.unescape(s))
    return ld({"@context":"https://schema.org","@type":"FAQPage","mainEntity":[
        {"@type":"Question","name":strip(q),"acceptedAnswer":{"@type":"Answer","text":strip(a)}} for q, a in items]})

def page_hero(eyebrow, h1, lead, buttons=True):
    b = '<div class="hero-btns" style="margin:0"><a class="btn btn-gold" href="/contact">Book a Consultation</a></div>' if buttons else ""
    return f'<section class="page-hero"><div class="eyebrow">{eyebrow}</div><h1>{h1}</h1><p>{lead}</p>{b}</section>'

def crumb(label):
    return f'<div class="crumbs"><a href="/">Home</a> / {label}</div>'

def price(k, default="Quoted in writing"):
    return PRICES.get(k) or default

# ---- helpers (new) ----
def affil_html():
    return f'<div class="affil"><div>{ic("shield")} Licensed and regulated by the Law Society of Ontario</div><div>{ic("award")} Associated with the Ontario Association of Black Paralegals</div></div>'

def sister_html():
    return f"""<div class="nn"><div class="logo"><img src="/notable-notary-logo.png" alt="Notable Notary and Apostille Services" width="146" height="64" loading="lazy"></div>
<div><div class="eyebrow">Our sister company</div><h3>Notable Notary and Apostille Services</h3>
<p>Butler Legal Services is the sister company of Notable Notary, a notary, apostille and translation company serving individuals, families and businesses across Ontario since 2021. It is rated 5.0 from more than 200 Google reviews.</p>
<div class="pills"><span>Notary &amp; commissioning</span><span>Apostille</span><span>Certified translation</span></div>
<p><a class="btn btn-nn" href="{SISTER_URL}" rel="noopener">Visit Notable Notary</a> &nbsp; <a class="btn btn-nnw" href="{SISTER_REVIEWS_URL}" rel="noopener">Read the reviews</a></p>
<p class="small">Those reviews are for notary, apostille and translation services, not paralegal services. Butler Legal Services is a newer practice, and the same founder is behind both.</p></div></div>"""

def bio_paragraphs():
    return f"""<p>Handing a ticket, a charge or a claim to someone you have never met is not a small thing. You want to know it is being handled carefully and correctly, by someone who understands what is at stake if it is not.</p>
<p>Butler Legal Services was founded by {LICENSEE}, a paralegal licensed by the Law Society of Ontario since 2021. {LICENSEE.split()[0]} built her career in corporate governance and finance and at law firms, and has run her sister company, Notable Notary, since 2021 before branching out to open Butler Legal Services. While this practice is new, the experience behind it is not.</p>
<p>That background shapes how the practice works: careful with details, clear about process, and focused on getting it right the first time. {LICENSEE.split()[0]} is also the founder of The Notary Blueprint, an education venture that trains other notaries, and regularly speaks and teaches, so explaining complicated rules in plain language is part of the job.</p>
<p>Butler Legal Services represents clients across Ontario, virtually and in person, in Small Claims Court, traffic and highway offence matters, and minor criminal and provincial offence matters. Removing barriers to legal services is central to how the practice works: clear explanations, honest advice and no surprises.</p>"""

def consult_cards(show_price=True):
    fl = f" ({FREE_CALL_LENGTH})" if FREE_CALL_LENGTH else ""
    sl = f" ({STRATEGY_LENGTH})" if STRATEGY_LENGTH else ""
    book = f'<p style="margin-top:12px"><a class="btn btn-gold" href="{BOOKING_URL}" rel="noopener">Book and pay online</a></p>' if BOOKING_URL else ""
    return f"""<div class="two-col">
  <div class="panel"><h3>Free consultation{fl}</h3><div class="tag">{price("free_call","Free")}</div>
    <p>A short conversation to confirm what the matter is, check for conflicts and flag any urgent deadline. It is a screening call, not a legal advice session.</p>
    <ul><li>Confirms whether Butler Legal Services can act</li><li>Identifies deadlines and the court involved</li><li>Explains your service options and the next step</li></ul></div>
  <div class="panel"><h3>Strategy consultation{sl}</h3><div class="tag">{price("strategy","Fee confirmed at booking")}</div>
    <p>A booked, paid session for people who want real answers before deciding how to proceed.</p>
    <ul><li>Detailed review of your documents and situation</li><li>Advice on options, risks, strengths and likely outcomes</li><li>A recommended plan, whether you hire for it or not</li></ul>
    <p style="margin-top:10px">Booked and paid in advance, which holds your time slot. The consultation fee is credited toward your retainer if you hire Butler Legal Services.</p>{book}</div>
</div>"""

def faq_block(items):
    return f'<h2>Frequently asked questions</h2>{faq_html(items)}'

# ================= HOME =================
HOME_FAQ = [
 ("Can a paralegal really represent me in court?", "Yes. Paralegals licensed by the Law Society of Ontario can represent clients in Small Claims Court, in Provincial Offences Court and in certain minor criminal matters, within the scope of practice the Law Society sets. If a matter falls outside that scope, Butler Legal Services will say so at the start."),
 ("How long do I have to respond to a traffic ticket?", "Usually 15 days from the date on the ticket. Missing the deadline can lead to a conviction without a hearing, so reach out as soon as possible. The ticket itself shows the exact dates that apply."),
 ("What is the Small Claims Court limit?", "In Ontario, Small Claims Court hears claims up to $35,000, not counting interest and costs."),
 ("Is there a free consultation?", "Yes. A free consultation of about 15 minutes confirms whether Butler Legal Services can help, checks for conflicts and flags any urgent deadlines. A 30-minute strategy consultation goes further, with a detailed review of your matter and advice on your options, and its fee is credited toward your retainer if you hire Butler Legal Services. <a href=\"/contact\">Book a consultation</a>."),
 ("Can you guarantee a result?", "No, and no honest representative can. What you get is a clear explanation of your options, the risks, and what a good outcome looks like in your situation, before you decide how to proceed."),
]

home_body = f'''
<section class="hero">
  <div class="badge-pill">{ic("shield","icon")} Licensed Paralegal | Across Ontario</div>
  <h1>Clear, practical paralegal representation for <span class="accent">tickets</span>, <span class="accent">charges</span> and <span class="accent">claims</span></h1>
  <p class="lead">Butler Legal Services helps individuals and small businesses with Small Claims Court, traffic tickets and highway offences, and minor criminal and provincial offences. Virtual and in person, with a personalized strategy and plain-language guidance at every step.</p>
  <div class="hero-btns"><a class="btn btn-primary" href="/contact">Book a Free Consultation</a><a class="btn btn-outline" href="/services">View Services</a></div>
</section>

<div class="service-strip">
  <div class="card"><div class="ic">{ic("scale")}</div><h3>Small Claims Court</h3><div class="tag">Claims up to $35,000</div><p>Start or defend a claim: unpaid invoices, contracts, deposits and property damage.</p><a class="more" href="/small-claims-court">Small claims &rarr;</a></div>
  <div class="card"><div class="ic gold">{ic("car")}</div><h3>Traffic Tickets &amp; Highway Offences</h3><div class="tag">Protect your licence and record</div><p>Speeding, stunt driving, distracted driving, careless driving and other Highway Traffic Act charges.</p><a class="more" href="/traffic-tickets">Traffic tickets &rarr;</a></div>
  <div class="card"><div class="ic">{ic("shield")}</div><h3>Minor Criminal &amp; Provincial Offences</h3><div class="tag">Within a paralegal&rsquo;s permitted scope</div><p>Summary conviction matters, insurance and trespass charges, and municipal by-law charges.</p><a class="more" href="/minor-criminal-offences">Minor criminal &rarr;</a> &nbsp; <a class="more" href="/provincial-offences">Provincial offences &rarr;</a></div>
</div>

<div class="stat-bar">
  <div class="stat-item">{ic("shield")}<div class="num">LSO Licensed</div><div class="label">Licensed and regulated by the Law Society of Ontario</div></div>
  <div class="stat-item">{ic("globe")}<div class="num">Across Ontario</div><div class="label">Virtual and in-person representation</div></div>
  <div class="stat-item">{ic("award")}<div class="num">Since 2021</div><div class="label">Licensed paralegal serving Ontario clients</div></div>
  <div class="stat-item">{ic("clock")}<div class="num">10+ Years</div><div class="label">In legal and client services</div></div>
</div>

<section class="block white">
  <div class="meet" style="max-width:1000px">
    <img src="/sierra.jpg" alt="{LICENSEE}, licensed paralegal and founder of {NAME}" width="260" height="260">
    <div><div class="eyebrow">Meet your paralegal</div><h2>{LICENSEE}, Licensed Paralegal and Founder</h2>
    {bio_paragraphs()}
    <a class="btn btn-outline" href="/about">More about {LICENSEE.split()[0]}</a></div>
  </div>
  {affil_html()}
</section>

<section class="block">
  <div class="eyebrow">Our approach</div>
  <h2>Legal help that is personal, transparent and practical</h2>
  <div class="values">
    <div class="value"><div class="ic">{ic("compass")}</div><h4>Personalized legal strategy</h4><p>Every matter gets a plan built around your goals, your risks and your deadlines, not a template.</p></div>
    <div class="value"><div class="ic">{ic("chat")}</div><h4>Transparent communication</h4><p>Plain language, regular updates and no surprises, whether the news is good or bad.</p></div>
    <div class="value"><div class="ic">{ic("heart")}</div><h4>Client-focused commitment</h4><p>Your matter is treated as important because to you, it is. Questions are welcome at every stage.</p></div>
    <div class="value"><div class="ic">{ic("check")}</div><h4>Practical solutions</h4><p>Honest advice on what is worth fighting and what is better resolved, with the costs in view.</p></div>
  </div>
</section>

<section class="block white">
  <div class="eyebrow">Why timing matters</div>
  <h2>The deadlines are short, and the courts do not wait</h2>
  <p>Many people learn about their deadline after it is already close. Here are two that catch people out.</p>
  <div class="steps" style="margin-top:28px;max-width:900px">
    <div class="step"><div class="n">15</div><h4>Days to respond to most tickets</h4><p>There are generally 15 days from the date on the ticket to pay, request a meeting with the prosecutor, or ask for a trial. Miss it and a conviction can follow without a hearing.</p></div>
    <div class="step"><div class="n">20</div><h4>Days to defend a Small Claims suit</h4><p>Once served with a claim, there are generally 20 days to file a defence. Without one, the other side can ask for judgment.</p></div>
  </div>
</section>

<section class="block">
  <div class="eyebrow">Flexible service levels</div>
  <h2>Full representation, or just the help you need</h2>
  <p>Not every matter needs full representation. Limited scope services let you pick specific help, such as strategy advice, document preparation, court coaching or a single appearance, and handle the rest yourself.</p>
  <p style="margin-top:20px"><a class="btn btn-outline" href="/limited-scope-services">Explore limited scope services</a></p>
</section>

<section class="block white">
  <div class="eyebrow">How it works</div>
  <h2>Three steps from first message to resolution</h2>
  <div class="steps" style="max-width:960px">
    <div class="step"><div class="n">1</div><h4>Start with a free consultation</h4><p>A short call confirms the basics, checks for conflicts and flags any urgent deadline.</p></div>
    <div class="step"><div class="n">2</div><h4>Choose your service level</h4><p>Full representation or limited scope, with the scope and fee confirmed in writing before any work begins.</p></div>
    <div class="step"><div class="n">3</div><h4>Move forward with clear updates</h4><p>Filings, negotiation and appearances are handled as agreed, with updates at each stage and the outcome explained plainly.</p></div>
  </div>
</section>

<section class="block">
  {sister_html()}
</section>

<section class="block white">
  <div class="eyebrow">Honest about scope</div>
  <h2>A focused practice, with clear limits</h2>
  <p>Licensed paralegals can only act within the scope of practice the Law Society allows. If a matter is outside it, such as family law, estates, real estate transactions or serious criminal charges, Butler Legal Services will say so at the start and point toward the right kind of help rather than take a retainer.</p>
</section>

<section class="block">
  <div class="eyebrow">Common questions</div>
  <h2>Quick answers</h2>
  {faq_html(HOME_FAQ)}
  <p style="margin-top:22px"><a class="btn btn-outline" href="/faq">See all FAQs</a></p>
</section>
{cta("Not sure where you stand? Start with a conversation.", "Tell us about your ticket, charge or claim. A free consultation confirms the next step, and any deadline is looked at first.")}
'''
page("/", "Small Claims & Traffic Ticket Paralegal | Butler Legal Services",
     "Licensed Ajax paralegal representing clients across Ontario, virtually and in person. Small Claims, traffic tickets, minor criminal and provincial offences.",
     home_body, active="/", extra=org_schema()+faq_schema(HOME_FAQ))

# ================= SERVICES =================
services_body = f'''{page_hero("Services", "Paralegal services for claims, tickets and charges", "Three practice areas, delivered virtually or in person across Ontario, with full or limited scope representation.")}
{crumb("Services")}
<div class="service-strip" style="margin-top:30px">
  <div class="card"><div class="ic">{ic("scale")}</div><h3>Small Claims Court</h3><div class="tag">Up to $35,000</div>
    <ul><li>Unpaid invoices and loans</li><li>Contract and service disputes</li><li>Deposits and property damage</li><li>Defending a claim</li></ul>
    <a class="more" href="/small-claims-court">Details &rarr;</a></div>
  <div class="card"><div class="ic gold">{ic("car")}</div><h3>Traffic Tickets &amp; Highway Offences</h3><div class="tag">Highway Traffic Act</div>
    <ul><li><a href="/speeding-ticket-ontario">Speeding tickets</a></li><li><a href="/stunt-driving-charge-ontario">Stunt driving</a></li><li><a href="/careless-driving-charge-ontario">Careless driving</a></li><li>Distracted driving, novice and commercial drivers</li></ul>
    <a class="more" href="/traffic-tickets">Details &rarr;</a></div>
  <div class="card"><div class="ic">{ic("shield")}</div><h3>Minor Criminal &amp; Provincial Offences</h3><div class="tag">Within paralegal scope</div>
    <ul><li>Summary conviction matters</li><li>Insurance and trespass charges</li><li>Municipal by-law charges</li><li>Early resolution and trial</li></ul>
    <a class="more" href="/minor-criminal-offences">Minor criminal &rarr;</a> &nbsp; <a class="more" href="/provincial-offences">Provincial offences &rarr;</a></div>
</div>
<section class="block">
  <div class="eyebrow">Choose your level of help</div>
  <h2>Full representation or limited scope</h2>
  <p>Every practice area is available as full representation, or as limited scope services for people who want specific help and plan to handle the rest. <a href="/limited-scope-services">See how limited scope works</a>.</p>
  {affil_html()}
</section>
<section class="block white">
  <h2>How services are billed</h2>
  <div class="narrow" style="padding-top:18px;padding-bottom:0">
  <table class="t"><thead><tr><th>Service</th><th>How it is billed</th><th>Fee</th></tr></thead><tbody>
    <tr><td><strong>Free consultation</strong> ({FREE_CALL_LENGTH})</td><td>No charge</td><td>{price("free_call","Free")}</td></tr>
    <tr><td><strong>Strategy consultation</strong> ({STRATEGY_LENGTH})</td><td>Fixed fee, credited toward your retainer</td><td>{price("strategy","Confirmed at booking")}</td></tr>
    <tr><td><strong>Limited scope task</strong> (advice, document review, coaching)</td><td>Flat fee for the agreed task</td><td>{price("limited_task")}</td></tr>
    <tr><td><strong>Single appearance</strong></td><td>Flat fee per appearance</td><td>{price("single_appearance")}</td></tr>
    <tr><td><strong>Traffic ticket or highway offence</strong>, full representation</td><td>Flat fee per matter, where the scope is clear</td><td>{price("ticket")}</td></tr>
    <tr><td><strong>Minor criminal or provincial offence</strong>, full representation</td><td>Flat fee by stage, or hourly with an estimate</td><td>{price("minor_criminal")}</td></tr>
    <tr><td><strong>Small Claims Court</strong>, full representation</td><td>Flat fee by stage, or hourly with an estimate</td><td>{price("small_claims")}</td></tr>
  </tbody></table>
  <p style="font-size:14px;color:var(--muted)">Every quote is confirmed in writing before work starts and states whether taxes and disbursements (court filing fees, process server, disclosure, courier) are included in the fee or added on top. No outcome is guaranteed.</p></div>
</section>
<section class="block"><div class="eyebrow">Outside our scope</div><h2>Where a lawyer or another professional is the right call</h2>
  <p>Butler Legal Services does not handle family law, wills and estates, real estate transactions, or serious criminal charges that a paralegal is not permitted to take. If a matter falls in one of those areas, that is stated up front.</p></section>
{cta()}'''
page("/services", "Paralegal Services in Ontario | Butler Legal Services",
     "Small Claims Court, traffic tickets and highway offences, minor criminal and provincial offences, with full or limited scope representation across Ontario.",
     services_body, active="/services", extra=crumbs_schema("/services","Services")+service_schema("Paralegal services","Small Claims Court, traffic ticket, minor criminal and provincial offence representation by a licensed paralegal in Ontario.","/services"))

TRAFFIC_REL2 = [("/speeding-ticket-ontario","Speeding tickets"),("/stunt-driving-charge-ontario","Stunt driving charges"),("/careless-driving-charge-ontario","Careless driving charges"),("/limited-scope-services","Limited scope services")]
SC_REL2 = [("/defend-small-claims-claim-ontario","Served with a claim? What to do"),("/unpaid-invoice-small-claims-ontario","Collecting an unpaid invoice"),("/limited-scope-services","Limited scope services")]
# ================= SMALL CLAIMS =================
sc_body = f'''{page_hero("Small Claims Court", "Small Claims Court representation in Ontario", "Owed money, or being sued? Ontario Small Claims Court hears claims up to $35,000, not counting interest and costs. Butler Legal Services helps start a claim or defend one.")}
{crumb('<a href="/services">Services</a> / Small Claims Court')}
<div class="narrow">
  <h2>Common Small Claims matters</h2>
  <ul><li>Unpaid invoices and unpaid loans</li><li>Breach of contract and disputes over services or work done</li><li>Deposits that were not returned</li><li>Property damage</li><li>Defending a claim filed against you or your business</li></ul>
  <h2>How a Small Claims case unfolds</h2>
  <ol>
    <li><strong>Demand letter.</strong> A clear written demand often resolves things, and it supports the case if it goes further.</li>
    <li><strong>Plaintiff&rsquo;s Claim.</strong> The claim is filed with the court and served on the other side.</li>
    <li><strong>Defence.</strong> The defendant generally has 20 days after being served to file a defence.</li>
    <li><strong>Settlement conference.</strong> A judge helps the parties try to settle before trial.</li>
    <li><strong>Trial.</strong> Without a settlement, the judge hears the evidence and decides.</li>
    <li><strong>Collecting.</strong> A judgment is not the same as being paid. Enforcement options exist, such as garnishment.</li>
  </ol>
  <div class="callout"><strong>Time limits apply.</strong> There are generally two years from when a claim was discovered to start it, with some exceptions. Waiting can cost the right to sue.</div>
  <h2>Is it worth suing?</h2>
  <p>Three practical questions come first: Can it be proven? Can the other side pay? Is the cost of pursuing it reasonable compared with what could be recovered? The costs recoverable from the other side in Small Claims Court are limited, so those numbers are reviewed together before any commitment.</p>
  <h2>If you have been sued</h2>
  <p>Do not ignore the claim. Check the date you were served and reach out quickly. A defence filed on time keeps you in the case, and there is then room to consider settling, making a formal offer, or going to trial.</p>
  <h2>Ways to get help</h2>
  <p>Full representation covers the matter from start to finish. <a href="/limited-scope-services">Limited scope services</a> cover specific tasks, such as preparing your claim or defence, coaching you for a settlement conference or trial, or appearing for you once.</p>
{related(SC_REL2)}
</div>
{cta("Owed money, or served with a claim?", "Share the documents and the date of service, if any. The deadline and your options come first.")}'''
page("/small-claims-court", "Small Claims Court Paralegal Ontario | Butler Legal Services",
     "Start or defend a Small Claims Court claim up to $35,000 in Ontario with a licensed paralegal, virtually or in person. Clear process, deadlines and fees.",
     sc_body, active="/services", extra=crumbs_schema("/small-claims-court","Small Claims Court"))

# ================= TRAFFIC =================
tt_opts = '''<table class="t"><thead><tr><th>Your option</th><th>What it means</th><th>Worth knowing</th></tr></thead><tbody>
<tr><td><strong>Pay the ticket</strong></td><td>You plead guilty and are convicted.</td><td>Demerit points and insurance effects can follow. Get advice before paying if your record matters.</td></tr>
<tr><td><strong>Meet the prosecutor</strong></td><td>An early resolution meeting, where a reduced charge or penalty may be discussed.</td><td>An offer is possible, never promised. Reviewing disclosure first shows what to ask for.</td></tr>
<tr><td><strong>Ask for a trial</strong></td><td>The prosecution must prove its case, and the evidence can be challenged.</td><td>It takes longer and carries risk. Both are explained before you decide.</td></tr>
</tbody></table>'''
tt_body = f'''{page_hero("Traffic Tickets &amp; Highway Offences", "Traffic ticket and highway offence paralegal in Ontario", "A ticket is more than a fine. Demerit points, insurance premiums and your licence can all be affected. Get help deciding whether to pay, negotiate or fight.")}
{crumb('<a href="/services">Services</a> / Traffic Tickets &amp; Highway Offences')}
<div class="narrow">
  <div class="callout"><strong>Check your deadline first.</strong> Most tickets give about 15 days from the date on the ticket to respond. If that date has passed, reach out anyway. There may still be options.</div>
  <h2>Tickets and charges we handle</h2>
  <ul><li>Speeding, stop sign and red light tickets</li><li>Distracted driving (hand-held device) and seat belt tickets</li><li>Careless driving and other serious Highway Traffic Act charges</li><li>Novice (G1 and G2) and commercial driver tickets</li><li>Driving without insurance, a licence or a valid permit</li></ul>
  <h2>What a conviction can cost</h2>
  <p>The fine is only the start. A conviction can add demerit points, raise insurance premiums for years, and lead to licence consequences if points add up. Novice and commercial drivers face stricter rules. Serious charges, such as careless driving or stunt driving, can carry licence suspensions, vehicle impoundment and large fines.</p>
  <h2>Your options with a ticket</h2>
  {tt_opts}
  <h2>What the service includes</h2>
  <ol><li>Review of the ticket, the deadlines and what is at stake for your record.</li><li>Request and review of the prosecution&rsquo;s disclosure.</li><li>A clear explanation of realistic options, including the risks of each.</li><li>Negotiation with the prosecutor, or representation at trial.</li><li>In many cases, an appearance on your behalf, so attending in person may not be needed.</li></ol>
  <div class="callout"><strong>No guarantees.</strong> A reduced charge or dismissal cannot be promised. What you do get is an honest view of what is likely, and whether fighting the ticket is worth it for you.</div>
  <p>Prefer to handle the ticket yourself with expert support? <a href="/limited-scope-services">Limited scope services</a> include strategy advice, court coaching and single-appearance representation.</p>
{related(TRAFFIC_REL2)}
</div>
{cta("Got a ticket? Send the details.", "Include the date on the ticket and the court location if it is shown. The deadline and your options are confirmed first.")}'''
page("/traffic-tickets", "Traffic Ticket Paralegal in Ontario | Butler Legal Services",
     "Traffic ticket or highway offence in Ontario? Understand your options, deadlines and demerit points, and how a licensed paralegal can help.",
     tt_body, active="/services", extra=crumbs_schema("/traffic-tickets","Traffic Tickets"))

# ================= MINOR CRIMINAL =================
mc_body = f'''{page_hero("Minor Criminal Offences", "Minor criminal offence representation in Ontario", "Some criminal charges can be handled by a licensed paralegal. Butler Legal Services confirms at the start whether yours is one of them.")}
{crumb('<a href="/services">Services</a> / Minor Criminal Offences')}
<div class="narrow">
  <div class="callout"><strong>Scope matters here.</strong> Paralegals may only represent clients on summary conviction criminal offences where the maximum penalty is six months in jail or less. Whether a charge qualifies depends on the specific offence and how the Crown proceeds, so eligibility is confirmed at the very start. If it does not qualify, that is explained and a lawyer is recommended.</div>
  <h2>What this service covers</h2>
  <ul><li>Reviewing the charge, the paperwork you were given and the dates you must attend</li><li>Requesting and reviewing disclosure</li><li>Explaining your options, the risks and the possible outcomes</li><li>Speaking with the Crown on your behalf</li><li>Representation at appearances and at trial</li></ul>
  <h2>What matters early</h2>
  <ul><li>Any court date on your paperwork is mandatory, so keep every document you were given.</li><li>Conditions you agreed to, such as an undertaking, must be followed exactly.</li><li>Share the charge details before the first court date, so options are ready when you attend.</li></ul>
  <h2>If a lawyer is needed</h2>
  <p>Serious charges and anything outside a paralegal&rsquo;s permitted scope need a lawyer. Butler Legal Services will tell you directly rather than accept a retainer it cannot properly act on.</p>
</div>
{cta("Facing a charge? Start with the paperwork.", "Send the details you were given. Whether it falls within paralegal scope is confirmed first.")}'''
page("/minor-criminal-offences", "Minor Criminal Offence Paralegal | Butler Legal Services",
     "Representation for summary conviction criminal offences within a paralegal's permitted scope in Ontario, with scope confirmed before you commit.",
     mc_body, active="/services", extra=crumbs_schema("/minor-criminal-offences","Minor Criminal Offences"))

# ================= PROVINCIAL OFFENCES =================
poa_body = f'''{page_hero("Provincial Offences", "Provincial Offences Court representation in Ontario", "Charges under Ontario laws and municipal by-laws are heard in Provincial Offences Court. Get representation from disclosure through resolution or trial.")}
{crumb('<a href="/services">Services</a> / Provincial Offences')}
<div class="narrow">
  <h2>What are provincial offences?</h2>
  <p>Provincial offences are breaches of Ontario laws and municipal by-laws, handled under the Provincial Offences Act. Many are traffic related, but they also include charges under laws such as the Compulsory Automobile Insurance Act and the Trespass to Property Act, and by-law charges laid by a municipality.</p>
  <h2>How these matters usually start</h2>
  <ul>
    <li><strong>A ticket (offence notice).</strong> The most common route. You choose to pay, meet the prosecutor, or request a trial.</li>
    <li><strong>A parking ticket.</strong> Handled through a separate, simpler process.</li>
    <li><strong>A summons.</strong> Used for more serious charges. Attending court on the date shown is required.</li>
  </ul>
  <div class="callout"><strong>Do not ignore it.</strong> Ignoring a ticket or summons can lead to a conviction without a hearing, added penalties, and trouble renewing a licence or plates.</div>
  <h2>How the service helps</h2>
  <ul><li>Confirming exactly which charge applies and what deadlines run</li><li>Requesting and reviewing disclosure, the evidence the prosecution intends to use</li><li>Explaining options and the realistic risks of each</li><li>Negotiating with the prosecutor where it makes sense</li><li>Representation at trial, including questioning witnesses and making submissions</li></ul>
  <h2>Before you decide</h2>
  <p>Not every charge is worth fighting, and some are. Honest advice on which applies comes before any retainer. Fees are quoted in writing up front. See <a href="/services">services and billing</a>.</p>
</div>
{cta("Charged under an Ontario law or by-law?", "Send the notice or summons. The court, the deadlines and your options are confirmed first.")}'''
page("/provincial-offences", "Provincial Offences Paralegal | Butler Legal Services",
     "Licensed paralegal representation for Provincial Offences Act charges across Ontario, including insurance, trespass and municipal by-law matters.",
     poa_body, active="/services", extra=crumbs_schema("/provincial-offences","Provincial Offences"))

# ================= LIMITED SCOPE =================
ls_body = f'''{page_hero("Limited Scope Services", "Limited scope services: get the help you need, handle the rest", "Not every matter needs full representation. Limited scope services let you choose specific support, with the scope and fee agreed in writing.")}
{crumb('<a href="/services">Services</a> / Limited Scope Services')}
<div class="narrow">
  <h2>What is limited scope representation?</h2>
  <p>With limited scope representation, a paralegal handles only the tasks you agree on, and you handle the rest of your matter yourself. It can lower costs and keep you in control, while still giving you professional guidance where it counts most. The agreed scope is confirmed in writing before work begins.</p>
</div>
<section class="block stone" style="padding-top:44px">
  <h2>Examples of limited services</h2>
  <div class="two-col">
    <div class="panel"><h3>Legal advice and strategy</h3><ul><li>Reviewing your case and explaining your options</li><li>Helping you understand risk, strength and possible outcomes</li><li>Preparing you for court or tribunal appearances</li></ul></div>
    <div class="panel"><h3>Document preparation</h3><ul><li>Drafting or reviewing court forms</li><li>Assisting with affidavits, motions or written submissions</li><li>Reviewing contracts or legal documents before you sign, for matters within a paralegal&rsquo;s permitted scope</li></ul></div>
    <div class="panel"><h3>Court and tribunal coaching</h3><ul><li>Explaining what to expect at your appearance</li><li>Helping you prepare what to say to a prosecutor, adjudicator or judge</li><li>Guiding you through procedures and timelines</li></ul></div>
    <div class="panel"><h3>One-time or single appearance</h3><ul><li>Attending court for a specific date only, such as an adjournment or an early resolution meeting</li><li>Speaking to the prosecutor or opposing party on your behalf for a limited, agreed purpose</li></ul></div>
  </div>
</section>
<section class="block white">
  <h2>How limited scope is different from full representation</h2>
  <div class="narrow" style="padding-top:20px;padding-bottom:0">
  <table class="t"><thead><tr><th></th><th>Limited scope</th><th>Full representation</th></tr></thead><tbody>
  <tr><td><strong>Who does what</strong></td><td>Shared. Specific tasks are handled by Butler Legal Services, the rest by you.</td><td>Butler Legal Services manages the matter from start to finish.</td></tr>
  <tr><td><strong>Cost</strong></td><td>Typically lower, because the scope is smaller.</td><td>Typically higher, because more work is covered.</td></tr>
  <tr><td><strong>Court appearances</strong></td><td>Only the dates agreed in advance.</td><td>All appearances within the retainer.</td></tr>
  <tr><td><strong>Your involvement</strong></td><td>Higher. You take on tasks outside the agreed scope.</td><td>Lower. Most steps are handled for you.</td></tr>
  <tr><td><strong>Best for</strong></td><td>People comfortable handling parts of their own matter with guidance.</td><td>Complex or high-stakes matters, or people who want it handled for them.</td></tr>
  </tbody></table></div>
</section>
<div class="narrow">
  <h2>Your responsibilities</h2>
  <ul class="checks"><li>Meet every deadline for the tasks that remain with you.</li><li>Keep track of court dates, filings and notices outside the agreed scope.</li><li>Share complete and accurate information and documents promptly.</li><li>Ask for help early if something changes, because scope can be widened by agreement.</li></ul>
  <h2>Is limited representation right for you?</h2>
  <p>It is often a good fit if:</p>
  <ul class="checks"><li>You are comfortable handling parts of your matter yourself.</li><li>Your matter is straightforward, or you only need help at one stage.</li><li>You want expert advice and a plan before deciding on next steps.</li><li>You want to control costs.</li></ul>
  <p>Full representation is usually the better choice if the matter is complex, the stakes are high, or you do not have the time or confidence to manage your side. A strategy consultation is a good way to find out which suits you.</p>
</div>
{cta("Not sure which level of help fits?", "Start with a free consultation, or book a strategy consultation to map out your options.")}'''
page("/limited-scope-services", "Limited Scope Legal Services | Butler Legal Services",
     "Limited scope paralegal services in Ontario: legal advice and strategy, document preparation, court coaching and single-appearance representation.",
     ls_body, active="/services", extra=crumbs_schema("/limited-scope-services","Limited Scope Services"))

# ================= DURHAM =================
dr_body = f'''{page_hero("Local", "Paralegal services in Ajax and Durham Region", "Based in Ajax, representing clients across Ontario, virtually and in person.")}
{crumb('<a href="/services">Services</a> / Ajax &amp; Durham Region')}
<div class="narrow">
  <h2>Based in Ajax, serving Ontario</h2>
  <p>Butler Legal Services supports people in Ajax, Pickering, Whitby, Oshawa, Clarington, Scugog, Uxbridge and Brock, and represents clients in courts across Ontario, both virtually and in person.</p>
  <h2>Which court will hear a matter?</h2>
  <p>It depends on the matter, not where you live. A ticket shows the court location where it will be dealt with. A Small Claims case is generally heard where the dispute arose or where the defendant lives or carries on business. The court is confirmed at intake, along with how the matter can be handled there.</p>
  <h2>What to send</h2>
  <ul><li>A photo or scan of the ticket, summons or claim</li><li>The date on the ticket, or the date you were served</li><li>Any contracts, invoices, messages or photos related to the matter</li></ul>
</div>
{cta()}'''
page("/paralegal-durham-region", "Paralegal in Ajax & Durham Region | Butler Legal Services",
     "Licensed paralegal based in Ajax, representing clients across Ontario, virtually and in person, with traffic tickets, Small Claims and provincial offences.",
     dr_body, active="/services", extra=crumbs_schema("/paralegal-durham-region","Ajax & Durham Region"))


# ================= SITUATION PAGES =================
def opts_table():
    return tt_opts

TRAFFIC_REL = [("/traffic-tickets","Traffic tickets and highway offences"),("/speeding-ticket-ontario","Speeding tickets"),("/stunt-driving-charge-ontario","Stunt driving charges"),("/careless-driving-charge-ontario","Careless driving charges"),("/limited-scope-services","Limited scope services")]

# --- speeding ---
sp_faq = [
 ("How many demerit points do I get for speeding in Ontario?", "Speeding 1 to 15 km/h over the limit carries no demerit points. 16 to 29 km/h over carries 3 points, and 30 to 49 km/h over carries 4 points. Going 50 km/h or more over is treated as stunt driving, with 6 points and much heavier penalties."),
 ("How long do I have to respond to a speeding ticket?", "Usually 15 days from the date on the ticket. The ticket shows the exact dates that apply. If the deadline has passed, reach out anyway, because there may still be options."),
 ("Will a speeding ticket raise my insurance?", "A conviction can raise your premiums, sometimes for several years, depending on your insurer and how far over the limit you were. Resolving the ticket before you plead guilty can matter for your record and your rates."),
 ("Do speed camera tickets carry demerit points?", "Automated speed camera tickets are generally issued to the vehicle owner and do not carry demerit points. Tickets issued by an officer do."),
 ("Do I have to attend court for a speeding ticket?", "Often not. In many cases a licensed paralegal can appear on your behalf, though some hearings need you to attend, for example to give evidence. What applies to your ticket is confirmed up front."),
]
sp_body = f'''{page_hero("Speeding Tickets", "Fight a speeding ticket in Ontario", "Speeding tickets affect your demerit points, your insurance and, for some drivers, your licence. Find out your options before you pay.")}
{crumb('<a href="/services">Services</a> / <a href="/traffic-tickets">Traffic Tickets</a> / Speeding Tickets')}
{byline()}
<div class="narrow">
  <div class="callout"><strong>Deadline first.</strong> Most speeding tickets give about 15 days from the date on the ticket to choose an option. Missing it can lead to a conviction without a hearing.</div>
  <h2>Speeding demerit points in Ontario</h2>
  <table class="t"><thead><tr><th>Speed over the limit</th><th>Demerit points</th></tr></thead><tbody>
    <tr><td>1 to 15 km/h over</td><td>0</td></tr>
    <tr><td>16 to 29 km/h over</td><td>3</td></tr>
    <tr><td>30 to 49 km/h over</td><td>4</td></tr>
    <tr><td>50 km/h or more over (or 40 or more where the limit is under 80 km/h)</td><td>Stunt driving charge, 6 points. See <a href="/stunt-driving-charge-ontario">stunt driving</a></td></tr>
  </tbody></table>
  <p>Fines are set by the number of kilometres over the limit, and they are increased in community safety zones and in construction zones when workers are present.</p>
  <h2>When it is worth getting help</h2>
  <ul><li>The points would put you near a warning or suspension threshold</li><li>You are a novice (G1 or G2) driver, or you drive commercially</li><li>You drive for work, or a clean record matters for your insurance</li><li>You believe the reading, the signage or the stop was wrong</li></ul>
  <h2>Your options with a speeding ticket</h2>
  {tt_opts}
  <h2>What the service includes</h2>
  <ol><li>Review of the ticket, deadlines and the points involved.</li><li>A request for disclosure, including the officer&rsquo;s notes and information about the speed measurement.</li><li>A clear explanation of realistic options and the risk of each.</li><li>Negotiation with the prosecutor, or representation at trial.</li></ol>
  <div class="callout"><strong>No guarantees.</strong> A reduced charge or dismissal cannot be promised. What you do get is an honest view of what is likely, and whether fighting is worth it for you.</div>
  {faq_block(sp_faq)}
  {related(TRAFFIC_REL)}
</div>
{cta("Got a speeding ticket? Send the details.", "Include the date on the ticket and the speed alleged. The deadline and your options are confirmed first.")}'''
page("/speeding-ticket-ontario", "Fight a Speeding Ticket in Ontario | Butler Legal Services",
     "Speeding ticket in Ontario? See demerit points, your options and deadlines, and how a licensed paralegal can help you pay less, keep points off or fight it.",
     sp_body, active="/services", extra=faq_schema(sp_faq)+crumbs_schema("/speeding-ticket-ontario","Speeding Tickets")+service_schema("Speeding ticket defence","Licensed paralegal representation for speeding tickets in Ontario.","/speeding-ticket-ontario"))

# --- stunt ---
st_faq = [
 ("What counts as stunt driving in Ontario?", "Driving 50 km/h or more over the limit on roads posted at 80 km/h or higher, 40 km/h or more over on roads posted under 80 km/h, or driving at 150 km/h or more. Racing and certain other dangerous driving behaviour can also be charged as stunt driving."),
 ("What happens at the roadside?", "A stunt driving charge usually brings an immediate 30-day licence suspension and a 14-day vehicle impoundment, before you ever reach court."),
 ("What are the penalties on conviction?", "A conviction can bring a fine of $2,000 to $10,000, up to six months in jail, six demerit points, a long licence suspension and a mandatory driver improvement course. Penalties are set by law and can change, so current details are confirmed at intake."),
 ("Can a paralegal handle a stunt driving charge?", "Stunt driving is a Highway Traffic Act offence, which falls within a paralegal&rsquo;s permitted scope. Where a matter is more serious or complex than a paralegal can properly take, you will be told and a lawyer will be recommended."),
 ("Will I have to go to court?", "Stunt driving charges usually involve court proceedings. In many cases a paralegal can appear for you on court dates, but some hearings need you to attend. What applies to your matter is explained at the start."),
]
st_body = f'''{page_hero("Stunt Driving", "Stunt driving charge in Ontario", "A stunt driving charge can mean an immediate licence suspension, an impounded vehicle and serious penalties. Early advice makes a difference.")}
{crumb('<a href="/services">Services</a> / <a href="/traffic-tickets">Traffic Tickets</a> / Stunt Driving')}
{byline()}
<div class="narrow">
  <div class="callout"><strong>Act quickly.</strong> A roadside suspension and impoundment start immediately, and court dates follow. Reach out as soon as you can with the paperwork you were given.</div>
  <h2>What counts as stunt driving</h2>
  <ul><li>50 km/h or more over the limit where the posted limit is 80 km/h or higher</li><li>40 km/h or more over the limit where the posted limit is under 80 km/h</li><li>Driving at 150 km/h or more</li><li>Racing and certain other dangerous driving behaviour</li></ul>
  <h2>What can happen</h2>
  <ul><li><strong>At the roadside:</strong> a 30-day licence suspension and a 14-day vehicle impoundment</li><li><strong>On conviction:</strong> a fine of $2,000 to $10,000, up to six months in jail, six demerit points, a long licence suspension, a mandatory driver improvement course and a major insurance impact</li></ul>
  <p>Penalties are set by law and can change, so the current details are confirmed when you get in touch.</p>
  <h2>How the service helps</h2>
  <ol><li>Review of the charge, the paperwork and the dates you must attend.</li><li>Request and review of disclosure, including how the speed or conduct was recorded.</li><li>A frank assessment of the risks, including whether the charge could be resolved on different terms.</li><li>Negotiation with the prosecutor, or representation at trial.</li></ol>
  <div class="callout"><strong>Honest about scope.</strong> If a matter is more serious or complex than a paralegal can properly take, you will be told right away and pointed toward a lawyer.</div>
  {faq_block(st_faq)}
  {related(TRAFFIC_REL)}
</div>
{cta("Facing a stunt driving charge?", "Send the paperwork you were given. Your deadlines, the court and your options are confirmed first.")}'''
page("/stunt-driving-charge-ontario", "Stunt Driving Charge in Ontario | Butler Legal Services",
     "Charged with stunt driving in Ontario? Understand the roadside suspension, penalties and your options, with a licensed paralegal who can represent you.",
     st_body, active="/services", extra=faq_schema(st_faq)+crumbs_schema("/stunt-driving-charge-ontario","Stunt Driving")+service_schema("Stunt driving charge representation","Licensed paralegal representation for stunt driving charges in Ontario.","/stunt-driving-charge-ontario"))

# --- careless ---
cl_faq = [
 ("What are the penalties for careless driving in Ontario?", "Careless driving under section 130 of the Highway Traffic Act carries a fine of $400 to $2,000, up to six months in jail, six demerit points and a licence suspension of up to two years. Careless driving causing bodily harm or death carries much heavier penalties."),
 ("Is careless driving a criminal offence?", "No. It is a Highway Traffic Act offence, not a criminal charge, so a conviction does not create a criminal record. It can still have a major effect on your licence and insurance."),
 ("Will careless driving raise my insurance?", "Very often, yes. A careless driving conviction can raise premiums significantly and may lead insurers to treat you as a higher-risk driver."),
 ("Do I need to go to court?", "Careless driving is a more serious charge than a standard ticket, and court proceedings are usually involved. In many cases a paralegal can appear for you on court dates, but some hearings need you to attend."),
 ("Can a paralegal handle a careless driving charge?", "Yes, careless driving is a Highway Traffic Act offence within a paralegal&rsquo;s permitted scope. Where bodily harm or death is involved, the matter is often serious enough that you should consider a lawyer, and you will be told honestly."),
]
cl_body = f'''{page_hero("Careless Driving", "Careless driving charge in Ontario", "Careless driving carries demerit points, possible jail and a lasting effect on your insurance. Know your options before your first court date.")}
{crumb('<a href="/services">Services</a> / <a href="/traffic-tickets">Traffic Tickets</a> / Careless Driving')}
{byline()}
<div class="narrow">
  <h2>What careless driving means</h2>
  <p>Careless driving is driving without due care and attention, or without reasonable consideration for other road users. It is charged under section 130 of the Highway Traffic Act and often follows a collision.</p>
  <h2>Penalties on conviction</h2>
  <table class="t"><thead><tr><th></th><th>Careless driving</th><th>Causing bodily harm or death</th></tr></thead><tbody>
    <tr><td><strong>Fine</strong></td><td>$400 to $2,000</td><td>$2,000 to $50,000</td></tr>
    <tr><td><strong>Jail</strong></td><td>Up to 6 months</td><td>Up to 2 years</td></tr>
    <tr><td><strong>Demerit points</strong></td><td>6</td><td>6</td></tr>
    <tr><td><strong>Licence suspension</strong></td><td>Up to 2 years</td><td>Up to 5 years</td></tr>
  </tbody></table>
  <p>Penalties are set by law and can change, so the current details are confirmed at intake. A conviction can also raise insurance premiums significantly.</p>
  <h2>How the service helps</h2>
  <ol><li>Review of the charge, the collision details and the dates you must attend.</li><li>Request and review of disclosure, including the officer&rsquo;s notes and any statements.</li><li>Assessment of the strengths and risks, including whether a different charge could be negotiated.</li><li>Negotiation with the prosecutor, or representation at trial.</li></ol>
  <div class="callout"><strong>Honest about scope.</strong> If someone was hurt or the matter is more serious than a paralegal can properly take, you will be told directly and pointed toward a lawyer.</div>
  {faq_block(cl_faq)}
  {related(TRAFFIC_REL)}
</div>
{cta("Charged with careless driving?", "Send the paperwork you were given. Your deadlines, the court and your options are confirmed first.")}'''
page("/careless-driving-charge-ontario", "Careless Driving Charge in Ontario | Butler Legal Services",
     "Careless driving charge in Ontario: penalties, demerit points, insurance impact and your options, with a licensed paralegal who can represent you.",
     cl_body, active="/services", extra=faq_schema(cl_faq)+crumbs_schema("/careless-driving-charge-ontario","Careless Driving")+service_schema("Careless driving charge representation","Licensed paralegal representation for careless driving charges in Ontario.","/careless-driving-charge-ontario"))

# --- been sued ---
SC_REL = [("/small-claims-court","Small Claims Court representation"),("/defend-small-claims-claim-ontario","Defending a Small Claims claim"),("/unpaid-invoice-small-claims-ontario","Collecting an unpaid invoice"),("/limited-scope-services","Limited scope services")]
bs_faq = [
 ("How long do I have to respond to a Small Claims claim?", "Generally 20 days after you are served with the Plaintiff&rsquo;s Claim. You respond by filing a Defence (Form 9A) with the court. Check the date you were served and act quickly."),
 ("What happens if I do nothing?", "The plaintiff can ask the court clerk to note you in default and then obtain a default judgment (Form 11B) without hearing from you. A judgment can lead to garnishment of wages or bank accounts and other enforcement."),
 ("Can I sue them back?", "Often yes. If you have your own claim against the plaintiff arising from the same dispute, it can be filed as a Defendant&rsquo;s Claim (Form 10A) together with your Defence."),
 ("What if I missed the deadline?", "Reach out right away. A motion to set aside the default may be possible, and it is time sensitive."),
 ("Should I make an offer to settle?", "Often it is worth considering. A formal Offer to Settle (Form 14A) can affect who pays costs if the case goes to trial. Whether and when to make one depends on your case, which is part of the strategy conversation."),
]
bs_body = f'''{page_hero("Been Sued?", "Served with a Small Claims claim in Ontario?", "You generally have 20 days to respond. Understand what you were served with, your options, and how to protect your position.")}
{crumb('<a href="/services">Services</a> / <a href="/small-claims-court">Small Claims Court</a> / Defending a Claim')}
{byline()}
<div class="narrow">
  <div class="callout"><strong>Check the date you were served.</strong> You generally have 20 days to file a Defence (Form 9A). Missing it allows the plaintiff to ask for judgment against you.</div>
  <h2>Your options after being served</h2>
  <ul><li><strong>Dispute the claim.</strong> File a Defence (Form 9A) explaining why you do not owe the money, or why you owe less.</li><li><strong>Counterclaim.</strong> If you have your own claim, file a Defendant&rsquo;s Claim (Form 10A) alongside your Defence.</li><li><strong>Settle.</strong> Negotiate, or make a formal Offer to Settle (Form 14A).</li><li><strong>Do nothing.</strong> Not recommended. It can lead to a default judgment (Form 11B) and enforcement.</li></ul>
  <h2>What happens next</h2>
  <ol><li>The Defence is filed and served.</li><li>A settlement conference, where a judge helps the parties try to resolve the matter.</li><li>A trial, if there is no settlement.</li><li>A judgment, and if you lose, enforcement options such as garnishment.</li></ol>
  <h2>What to send first</h2>
  <ul><li>The Plaintiff&rsquo;s Claim exactly as you received it, and the date you were served</li><li>Contracts, invoices, receipts, messages and photos related to the dispute</li><li>Any letters or demands you received before the claim</li></ul>
  <h2>Ways to get help</h2>
  <p>Full representation covers the matter from start to finish. <a href="/limited-scope-services">Limited scope services</a> cover specific tasks, such as preparing your Defence, coaching you for the settlement conference, or appearing once.</p>
  {faq_block(bs_faq)}
  {related(SC_REL)}
</div>
{cta("Been served with a claim?", "Send the claim and the date you were served. Your deadline and your options are confirmed first.")}'''
page("/defend-small-claims-claim-ontario", "Sued in Small Claims Court? Ontario | Butler Legal Services",
     "Served with a Small Claims Court claim in Ontario? You have about 20 days to file a Defence. See your options and how a licensed paralegal can help.",
     bs_body, active="/services", extra=faq_schema(bs_faq)+crumbs_schema("/defend-small-claims-claim-ontario","Defending a Small Claims Claim")+service_schema("Small Claims defence","Licensed paralegal help defending a Small Claims Court claim in Ontario.","/defend-small-claims-claim-ontario"))

# --- unpaid invoice ---
ui_faq = [
 ("What is the maximum I can claim in Small Claims Court?", "Ontario Small Claims Court hears claims up to $35,000, not counting interest and costs. Larger claims must go to Superior Court or be reduced to fit."),
 ("How long do I have to sue for an unpaid invoice?", "Generally two years from when you discovered the claim, with some exceptions. Start before the deadline gets close."),
 ("Do I need to send a demand letter first?", "It is not always required, but it is strongly recommended. A clear written demand can resolve things without court, and it shows the court you gave the other side a fair chance."),
 ("What if they still do not pay after I win?", "A judgment is not the same as being paid. Enforcement options include garnishing wages or bank accounts (Notice of Garnishment, Form 20E), examining the debtor about their finances (Notice of Examination, Form 20H), and filing a Writ of Seizure and Sale against personal property (Form 20C) or land (Form 20D)."),
 ("Can I recover my legal fees from the other side?", "The court may award some costs to a successful party, but the amount recoverable in Small Claims Court is limited. That is considered before you commit, so you know whether the numbers make sense."),
]
ui_body = f'''{page_hero("Unpaid Invoices", "Collect an unpaid invoice in Ontario Small Claims Court", "Owed money by a client, customer or contractor? Here is how to move from a demand letter to a judgment, and how to collect it.")}
{crumb('<a href="/services">Services</a> / <a href="/small-claims-court">Small Claims Court</a> / Unpaid Invoices')}
{byline()}
<div class="narrow">
  <div class="callout"><strong>Time limits apply.</strong> There are generally two years from when you discovered the claim to start it. Do not wait until the deadline is close.</div>
  <h2>Who this is for</h2>
  <ul><li>Contractors, tradespeople and freelancers owed for work done</li><li>Small businesses owed by customers</li><li>People owed an unpaid loan or a deposit</li><li>Anyone owed up to $35,000, not counting interest and costs</li></ul>
  <h2>From demand letter to payment</h2>
  <ol>
    <li><strong>Demand letter.</strong> A clear written demand with the amount, the basis for it and a deadline to pay.</li>
    <li><strong>Plaintiff&rsquo;s Claim (Form 7A).</strong> Filed with the court, then served on the defendant. Proof of service is filed with an Affidavit of Service (Form 8A).</li>
    <li><strong>If there is no defence.</strong> You can ask for the defendant to be noted in default and for a default judgment (Form 11B).</li>
    <li><strong>If it is defended.</strong> A settlement conference, then trial if there is no settlement. A formal Offer to Settle (Form 14A) can affect costs.</li>
    <li><strong>Enforcement.</strong> Garnishment (Form 20E), examination of the debtor (Form 20H), and a Writ of Seizure and Sale (Forms 20C and 20D).</li>
  </ol>
  <h2>Is it worth suing?</h2>
  <p>Three practical questions come first: Can it be proven? Can the other side pay? Is the cost of pursuing it reasonable compared with what could be recovered? Those numbers are reviewed together before any commitment.</p>
  <h2>Ways to get help</h2>
  <p>Full representation covers the claim from start to finish. <a href="/limited-scope-services">Limited scope services</a> cover specific tasks, such as drafting the demand letter, preparing your Plaintiff&rsquo;s Claim, or coaching you for the settlement conference.</p>
  {faq_block(ui_faq)}
  {related(SC_REL)}
</div>
{cta("Owed money? Start with the documents.", "Send the invoice, contract or messages and the amount owed. Your options and deadline are confirmed first.")}'''
page("/unpaid-invoice-small-claims-ontario", "Collect an Unpaid Invoice in Ontario | Butler Legal Services",
     "Owed money in Ontario? Learn how to collect an unpaid invoice in Small Claims Court, from the demand letter to garnishment, with a licensed paralegal.",
     ui_body, active="/services", extra=faq_schema(ui_faq)+crumbs_schema("/unpaid-invoice-small-claims-ontario","Unpaid Invoices")+service_schema("Small Claims collection","Licensed paralegal help collecting unpaid invoices through Ontario Small Claims Court.","/unpaid-invoice-small-claims-ontario"))

# ================= ABOUT =================
about_body = f'''{page_hero("About", f"About {NAME}", "Practical, transparent legal representation across Ontario, from a licensed paralegal who is new to this practice but not to the work.", buttons=False)}
{crumb("About")}
<div class="stat-bar" style="margin-top:0">
  <div class="stat-item">{ic("shield")}<div class="num">LSO Licensed</div><div class="label">Licensed paralegal</div></div>
  <div class="stat-item">{ic("award")}<div class="num">Since 2021</div><div class="label">Serving Ontario clients</div></div>
  <div class="stat-item">{ic("clock")}<div class="num">10+ Years</div><div class="label">In legal and client services</div></div>
  <div class="stat-item">{ic("globe")}<div class="num">Across Ontario</div><div class="label">Virtual and in person</div></div>
</div>
<section class="block white"><div class="meet" style="max-width:1000px">
  <img src="/sierra.jpg" alt="{LICENSEE}, licensed paralegal and founder of {NAME}" width="260" height="260">
  <div><div class="eyebrow">Our story</div><h2>Built on preparation, clarity and getting it right</h2>
  {bio_paragraphs()}</div>
</div></section>
<div class="narrow">
  <h2>Experience behind the practice</h2>
  <ul class="checks">
    <li><strong>Licensed paralegal since April 2021.</strong> Licensed and regulated by the Law Society of Ontario.</li>
    <li><strong>Corporate governance, finance and law firms.</strong> A career built on precision, deadlines and working with clients under pressure.</li>
    <li><strong>Founder of Notable Notary since 2021.</strong> A notary, apostille and translation company serving individuals, families and businesses across Ontario, from Ajax, Pickering, Whitby and Oshawa to clients online province-wide.</li>
    <li><strong>Commissioned Notary Public.</strong> Experience with sworn documents, affidavits and statutory declarations, which come up often in court matters.</li>
    <li><strong>Founder of The Notary Blueprint.</strong> An education venture that trains other notaries, with more than 3,000 hours of teaching.</li>
    <li><strong>Speaker and educator.</strong> Speaks and teaches nearly every week, which means explaining complicated rules plainly is part of the job.</li>
  </ul>
  <h2>How Butler Legal Services works</h2>
  <ul class="checks">
    <li><strong>Personalized legal strategy.</strong> Each matter gets a plan built around your goals and deadlines.</li>
    <li><strong>Transparent communication.</strong> Plain language and regular updates, with no surprises.</li>
    <li><strong>Client-focused commitment.</strong> Every matter is treated with the care it deserves.</li>
    <li><strong>Practical solutions.</strong> Honest advice on what is worth fighting, with the costs in view.</li>
    <li><strong>Clear limits.</strong> Only matters that can be properly handled within a paralegal&rsquo;s scope are taken on.</li>
  </ul>
</div>
<section class="block white">
  <div class="eyebrow">Credentials and affiliations</div>
  <h2>Licensed, regulated and part of the profession</h2>
  <div class="values" style="grid-template-columns:repeat(2,1fr);max-width:820px">
    <div class="value"><div class="ic">{ic("shield")}</div><h4>Law Society of Ontario</h4><p>Licensed and regulated as a paralegal. Any licensee&rsquo;s status can be confirmed in the Law Society&rsquo;s public directory.</p></div>
    <div class="value"><div class="ic">{ic("award")}</div><h4>Ontario Association of Black Paralegals</h4><p>Associated with a professional community supporting Black legal professionals across Ontario.</p></div>
  </div>
</section>
<section class="block">{sister_html()}</section>
<section class="block white"><div class="eyebrow">Our values</div><h2>What guides the work</h2>
  <div class="values">
    <div class="value"><div class="ic">{ic("check")}</div><h4>Accuracy and preparation</h4><p>Courts reward preparation. Every deadline, form and detail is checked before it matters.</p></div>
    <div class="value"><div class="ic">{ic("globe")}</div><h4>Convenience and access</h4><p>Virtual and in-person representation across Ontario, so help is not limited by where you live.</p></div>
    <div class="value"><div class="ic">{ic("compass")}</div><h4>Removing barriers</h4><p>Legal processes should not feel intimidating. Each step is explained in plain language.</p></div>
    <div class="value"><div class="ic">{ic("heart")}</div><h4>Trust and integrity</h4><p>Honest advice, written fees and no promised outcomes. If a matter is outside scope, you will be told.</p></div>
  </div></section>
{cta("Let&rsquo;s talk about your matter.", "Book a free consultation and share a short summary and any dates on your documents.")}'''
page("/about", "Sierra Walker, Licensed Paralegal | Butler Legal Services",
     f"Meet {LICENSEE}, an LSO-licensed paralegal with a background in corporate governance, finance and law firms, and founder of sister company Notable Notary.",
     about_body, active="/about", extra=crumbs_schema("/about","About"))

# ================= FAQ =================
FAQ = HOME_FAQ + [
 ("Am I hiring a lawyer?", "No. Butler Legal Services provides services through a paralegal licensed and regulated by the Law Society of Ontario. Paralegals can represent clients in Small Claims Court, Provincial Offences Court and certain minor criminal matters within the scope of practice the Law Society sets. If a matter needs a lawyer, you will be told."),
 ("What is limited scope representation?", "It means a paralegal handles only specific agreed tasks, such as strategy advice, document preparation, court coaching or a single appearance, while you handle the rest. The scope is confirmed in writing. See <a href=\"/limited-scope-services\">limited scope services</a>."),
 ("What is the difference between the free consultation and the strategy consultation?", "The free consultation (about 15 minutes) is a short conversation to confirm the basics, check for conflicts and flag urgent deadlines. The strategy consultation (30 minutes) is a booked, paid session with a detailed review of your matter and advice on your options and risks. Its fee is credited toward your retainer if you hire Butler Legal Services."),
 ("Which minor criminal matters can a paralegal handle?", "Paralegals may represent clients on summary conviction criminal offences where the maximum penalty is six months in jail or less. Whether a specific charge qualifies is confirmed at the start. If it does not, a lawyer is recommended."),
 ("Do you represent clients across Ontario?", "Yes. Butler Legal Services is based in Ajax and represents clients across Ontario, virtually and in person. The court and how the matter can be handled there are confirmed at intake."),
 ("Will I have to go to court myself?", "Often not, for ticket and charge matters where a paralegal can appear on your behalf, though some hearings need you to attend, for example to give evidence. What applies to your matter is explained up front."),
 ("How much does it cost?", "Fees are confirmed in writing before work starts, and the quote states whether taxes and disbursements are included. Matters are billed as flat fees where the scope is clear. See <a href=\"/services\">services and billing</a>."),
 ("How long do I have to start a Small Claims case?", "Generally two years from when you discovered your claim, with some exceptions. Do not wait until the deadline is close. See <a href=\"/unpaid-invoice-small-claims-ontario\">collecting an unpaid invoice</a>."),
 ("I was served with a Small Claims claim. What now?", "Do not ignore it. There are generally 20 days after being served to file a defence. See <a href=\"/defend-small-claims-claim-ontario\">what to do if you have been sued</a>."),
 ("How many demerit points does a speeding ticket carry?", "None for 1 to 15 km/h over, 3 points for 16 to 29 km/h over, and 4 points for 30 to 49 km/h over. See <a href=\"/speeding-ticket-ontario\">speeding tickets in Ontario</a>."),
 ("What should I send first?", "A photo or scan of the ticket, summons or claim, the date you received or were served with it, and any related documents such as contracts, invoices or messages."),
 ("Is what I share confidential?", "Licensed paralegals are bound by Law Society confidentiality obligations. Until it is confirmed that Butler Legal Services can act for you, please keep your first message to the basics and avoid sending sensitive documents."),
 ("What is the connection to Notable Notary?", "Notable Notary is the sister company of Butler Legal Services, a notary, apostille and translation company serving clients across Ontario. It is a separate business, and its services are not paralegal services."),
]
faq_body = f'''{page_hero("FAQ", "Frequently asked questions", "Straight answers about tickets, charges, Small Claims and working with a paralegal.", buttons=False)}
{crumb("FAQ")}
<section class="block" style="padding-top:26px">{faq_html(FAQ)}</section>
{cta()}'''
page("/faq", "FAQ | Butler Legal Services",
     "Answers about Small Claims, traffic tickets, minor criminal and provincial offences in Ontario, limited scope services and working with a licensed paralegal.",
     faq_body, active="/faq", extra=faq_schema(FAQ)+crumbs_schema("/faq","FAQ"))

# ================= CONTACT =================
contact_info = [f'<p><strong>Email</strong><br><a href="mailto:{EMAIL}">{EMAIL}</a></p>']
if PHONE: contact_info.insert(0, f'<p><strong>Phone</strong><br><a href="tel:{PHONE[1]}">{PHONE[0]}</a></p>')
contact_info.append(f'<p><strong>Location</strong><br>{esc(ADDRESS) if ADDRESS else "Ajax, Ontario"}<br>Representing {SERVICE_AREA}</p>')
contact_body = f'''{page_hero("Contact", "Book a consultation", "Start with a free consultation, or book a strategy consultation for a detailed review of your matter. Any urgent deadline is looked at first.", buttons=False)}
<div class="consult">{consult_cards()}</div>
<div class="contact-grid">
  <div>
    <form class="f" name="consultation" method="POST" action="/thank-you" data-netlify="true" netlify-honeypot="bot-field">
      <input type="hidden" name="form-name" value="consultation">
      <p class="hp"><label>Leave this empty <input name="bot-field"></label></p>
      <label for="name">Your name</label><input id="name" name="name" required autocomplete="name">
      <label for="email">Email</label><input id="email" name="email" type="email" required autocomplete="email">
      <label for="phone">Phone (optional)</label><input id="phone" name="phone" type="tel" autocomplete="tel">
      <label for="kind">What would you like to book?</label>
      <select id="kind" name="consultation_type" required><option value="">Choose one</option><option>Free consultation</option><option>Strategy consultation (paid)</option><option>Not sure yet</option></select>
      <label for="matter">What is this about?</label>
      <select id="matter" name="matter" required><option value="">Choose one</option><option>A traffic ticket or highway offence</option><option>Another provincial offence or by-law charge</option><option>A minor criminal charge</option><option>I want to sue someone (Small Claims)</option><option>I have been sued (Small Claims)</option><option>Not sure</option></select>
      <label for="help">Level of help you are considering</label>
      <select id="help" name="service_level"><option>Not sure yet</option><option>Full representation</option><option>Limited scope (specific tasks)</option></select>
      <label for="date">Important date (optional)</label><input id="date" name="important_date" placeholder="Date on your ticket, or the date you were served">
      <div class="hint">This helps check your deadline first.</div>
      <label for="msg">A short summary</label><textarea id="msg" name="message" required></textarea>
      <div class="hint">Keep it to the basics for now. Please do not attach or paste sensitive documents.</div>
      <label style="font-weight:400;display:flex;gap:10px;align-items:flex-start"><input type="checkbox" name="understand" required style="width:auto;margin-top:4px"> <span>I understand that sending this form does not create a paralegal-client relationship.</span></label>
      <button class="btn btn-primary" type="submit">Send my request</button>
    </form>
  </div>
  <div class="contact-info"><h3>Other ways to reach us</h3>{"".join(contact_info)}<p>If a deadline is close, say so in your message and it will be looked at first.</p></div>
</div>'''
page("/contact", "Book a Free Consultation | Butler Legal Services",
     "Book a free consultation or a strategy consultation with Butler Legal Services, a licensed paralegal in Ajax representing clients across Ontario.",
     contact_body, active="/contact", extra=crumbs_schema("/contact","Contact"))

# ================= PRIVACY =================
privacy_body = f'''{page_hero("Legal", "Privacy Policy", "Last updated October 30, 2026", buttons=False)}
<div class="narrow">
  <p>{NAME} respects your privacy. This policy explains what personal information is collected through this website, why, and how it is handled.</p>
  <h2>What is collected</h2>
  <ul><li>Information sent through the contact form: name, email, phone number (if given), the type of matter, any dates, and your message.</li><li>Basic technical information about visits to the site, such as pages viewed and device type, if website analytics are turned on.</li></ul>
  <h2>Why it is collected</h2>
  <p>Your information is used to reply to your request, check for conflicts of interest, assess deadlines and provide services if you retain {NAME}. It is not sold.</p>
  <h2>Where it is stored</h2>
  <p>Contact form submissions are processed by the site&rsquo;s hosting provider and delivered to the business email account. Email is hosted by Google Workspace. These providers may store data outside Canada.</p>
  <h2>Confidentiality</h2>
  <p>Licensed paralegals are bound by Law Society of Ontario confidentiality obligations. Until it is confirmed that {NAME} can act for you, please do not send sensitive details or documents.</p>
  <h2>Cookies and analytics</h2>
  <p>This site may use analytics cookies to understand how it is used. You can block cookies in your browser settings.</p>
  <h2>How long it is kept</h2>
  <p>Enquiries that do not become a client matter are kept only as long as needed to respond, and then deleted or archived. Client files are kept for the period the Law Society requires.</p>
  <h2>Your rights</h2>
  <p>You can ask to see, correct or delete the personal information held about you, subject to legal and professional obligations. Contact <a href="mailto:{EMAIL}">{EMAIL}</a>.</p>
</div>'''
page("/privacy-policy", "Privacy Policy | Butler Legal Services", "How Butler Legal Services collects, uses and protects personal information.", privacy_body)

terms_body = f'''{page_hero("Legal", "Terms &amp; Conditions", "Last updated October 30, 2026", buttons=False)}
<div class="narrow">
  <h2>General information only</h2>
  <p>The content of this website is general information about Ontario legal processes. It is not legal advice and should not be relied on as advice about your situation.</p>
  <h2>No paralegal-client relationship</h2>
  <p>Using this website, emailing or sending the contact form does not create a paralegal-client relationship. That relationship begins only when you and {NAME} sign a written retainer agreement, after it is confirmed that {NAME} can act for you and that there is no conflict of interest. A free consultation does not create that relationship either.</p>
  <h2>Scope of services</h2>
  <p>{NAME} provides services through a paralegal licensed by the Law Society of Ontario, within the scope of practice permitted for paralegals. Services are provided by a paralegal, not a lawyer. If a matter requires a lawyer, you will be told.</p>
  <h2>Fees and consultations</h2>
  <p>Fees are set out in a written quote and retainer agreement. Strategy consultations are booked and paid in advance, and the consultation fee is credited toward the retainer if you retain {NAME}. Any fee quoted on this website or in correspondence applies only to the services described in the quote, and states whether taxes and disbursements are included.</p>
  <h2>No guarantee of outcome</h2>
  <p>No result can be guaranteed. Descriptions of how matters can unfold are examples of processes, not predictions.</p>
  <h2>Deadlines</h2>
  <p>Legal deadlines are strict. Contacting {NAME} does not stop a deadline from running. {NAME} is responsible for a deadline only once it has agreed in writing to act for you on that matter.</p>
  <h2>Sister company</h2>
  <p>Notable Notary is a separate sister business. Its notary, apostille and translation services, and the reviews of those services, are not paralegal services of {NAME}.</p>
  <h2>Using the website</h2>
  <p>You may use this site for your own personal or business purposes. You may not copy or republish its content without permission. Links to other websites are provided for convenience, and {NAME} is not responsible for their content.</p>
  <h2>Governing law</h2>
  <p>These terms are governed by the laws of Ontario and the federal laws of Canada that apply there.</p>
  <h2>Changes</h2>
  <p>These terms may be updated from time to time. The date at the top shows when they were last changed.</p>
  <h2>Contact</h2>
  <p>Questions about these terms? Email <a href="mailto:{EMAIL}">{EMAIL}</a>.</p>
</div>'''
page("/terms-conditions", "Terms & Conditions | Butler Legal Services", "Terms of use for the Butler Legal Services website, including the limits of general information and when a paralegal-client relationship begins.", terms_body)

notfound_body = f'''{page_hero("404", "That page could not be found", "It may have moved. Try the homepage or one of the links below.", buttons=False)}
<section class="block"><p><a class="btn btn-primary" href="/">Homepage</a> &nbsp; <a class="btn btn-outline" href="/contact">Contact</a></p></section>'''
page("/404", "Page Not Found | Butler Legal Services", "Page not found.", notfound_body, noindex=True)


thanks_body = f'''{page_hero("Thank you", "Your request is in", "It will be reviewed and answered by email. If a deadline is close, that is looked at first.", buttons=False)}
<section class="block"><p><a class="btn btn-primary" href="/">Back to the homepage</a></p></section>'''
page("/thank-you", "Thank You | Butler Legal Services", "Your consultation request has been received.", thanks_body, noindex=True)


# ---------------- write files ----------------
for p in PAGES:
    fn = "index.html" if p["path"] == "/" else p["path"].lstrip("/") + ".html"
    with open(os.path.join(OUT, fn), "w", encoding="utf-8") as f:
        f.write(render(p))

# sitemap
urls = [p for p in PAGES if not p["noindex"]]
sm = ['<?xml version="1.0" encoding="UTF-8"?>','<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
for p in urls:
    loc = SITE + ("/" if p["path"] == "/" else p["path"])
    pri = "1.0" if p["path"] == "/" else ("0.8" if p["path"] in ("/traffic-tickets","/small-claims-court","/provincial-offences","/services","/contact") else "0.5")
    sm.append(f"  <url><loc>{loc}</loc><lastmod>{TODAY}</lastmod><priority>{pri}</priority></url>")
sm.append("</urlset>")
open(os.path.join(OUT,"sitemap.xml"),"w").write("\n".join(sm)+"\n")

open(os.path.join(OUT,"robots.txt"),"w").write(f"User-agent: *\nAllow: /\n\nSitemap: {SITE}/sitemap.xml\n")
open(os.path.join(OUT,"site.webmanifest"),"w").write(json.dumps({"name":NAME,"short_name":"Butler Legal","icons":[{"src":"/android-chrome-192x192.png","sizes":"192x192","type":"image/png"},{"src":"/android-chrome-512x512.png","sizes":"512x512","type":"image/png"}],"theme_color":"#7A1F3D","background_color":"#FAF6F0","display":"standalone"}, indent=2)+"\n")

rd = ["# Clean URLs: /page serves page.html", ""]
for p in PAGES:
    if p["path"] not in ("/", "/404"):
        rd.append(f'{p["path"]:<32}{p["path"]}.html   200')
rd += ["", "# Removed page", "/fees                           /contact   301"]
open(os.path.join(OUT,"_redirects"),"w").write("\n".join(rd)+"\n")

# netlify.toml for 404 + security headers
open(os.path.join(os.path.dirname(OUT.rstrip("/")), "netlify.toml"),"w").write('''[build]
  publish = "site"

[[headers]]
  for = "/*"
  [headers.values]
    X-Content-Type-Options = "nosniff"
    Referrer-Policy = "strict-origin-when-cross-origin"
    X-Frame-Options = "SAMEORIGIN"
''')
open(os.path.join(OUT,"llms.txt"),"w").write(f"""# {NAME}

> {NAME} is a paralegal practice in Ajax, Ontario, run by {LICENSEE}, a paralegal licensed and regulated by the Law Society of Ontario. It represents individuals and small businesses across Ontario, virtually and in person, in Small Claims Court, traffic tickets and highway offences, and minor criminal and provincial offences. Limited scope and full representation are available. It is a sister company of Notable Notary (notary, apostille and translation, {SISTER_URL}).

## Practice areas
- [Small Claims Court]({SITE}/small-claims-court): claims up to $35,000 in Ontario
- [Traffic tickets and highway offences]({SITE}/traffic-tickets)
- [Speeding tickets]({SITE}/speeding-ticket-ontario)
- [Stunt driving charges]({SITE}/stunt-driving-charge-ontario)
- [Careless driving charges]({SITE}/careless-driving-charge-ontario)
- [Minor criminal offences]({SITE}/minor-criminal-offences)
- [Provincial offences]({SITE}/provincial-offences)
- [Limited scope services]({SITE}/limited-scope-services)

## Contact
- [Book a consultation]({SITE}/contact): free consultation (15 minutes) or paid strategy consultation (30 minutes)
- Email: {EMAIL}
""")
print("built", len(PAGES), "pages")
