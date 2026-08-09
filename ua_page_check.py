#!/usr/bin/env python3
"""
UA site checker — deterministic pass.
Usage:  python3 ua_page_check.py <folder-of-html-files>
Report-only. Never edits. Judgment items (register, tone, argument quality)
are NOT checked here — those go to the Cowork judgment pass.
"""
import sys, os, re, glob

CLARITY = "xiwyxbc3ze"
GA4 = "G-CWF8FPK9T7"

# --- known factual regressions (from UA_Standing_Corrections) ---
FACT_TRAPS = [
    (r"(?i)(complaint to ComReg|ComReg requests|ComReg investigates|ComReg processes formal complaints|What does ComReg actually do|when ComReg receives)", "ComReg used as a GENERAL Irish EAA authority — it is communications ONLY. Distributed: CCPC (primary/products+general services), Central Bank (financial), Coimisiun na Mean (media), NTA (transport), ComReg (communications). Keep ComReg only in a communications context."),
    # Retargeted 8 Aug 2026. The old pattern matched any euro 10,000, which is
    # ALSO Germany's legitimate BFSG standard-violation figure on two pages. It
    # never fired on either, because it matched only the literal sign while the
    # site writes &euro;. Blind and wrong at the same time. Now it needs the
    # damages claim, not the number.
    (r"(?i)(?:\u20ac\s?10[,.]?000[^.]{0,90}(?:damages|awarded)|"
     r"(?:damages|awarded)[^.]{0,90}\u20ac\s?10[,.]?000|10,000 in provisional)",
     "claims the Caen court awarded 10,000 euro in damages - the figure appears in "
     "vendor summaries only, could not be confirmed in five French sources including "
     "the associations' own communiques, and is marked do-not-publish"),
    # Narrowed 8 Aug 2026. The old pattern fired on any "first EAA ruling", which
    # caught two pages stating DIFFERENT true claims: Lille 5 May 2026 was the
    # first EAA court ruling in the EU, and Caen 4 June 2026 was the first ruling
    # ORDERING COMPLIANCE. Both are correct and both said so. A trap that fires
    # on the corrected position teaches people to ignore it.
    (r"(?i)first EAA (fine|penalty)|first (?:EAA )?fine (?:under|issued)",
     "claims a FIRST EAA fine or penalty — none has been issued in any market, "
     "so nothing can be the first"),
    (r"(?i)(has been|was|were) fined", "claims a fine was ISSUED — no EAA administrative fine exists in any market"),
    (r"(?i)60 webshops", "60 webshops — should be ~100-webshop sample"),
    (r"(?i)partial conformance is not a defence anywhere", "overstates a single referé as settled EU law"),
    # JOB 0q: the ACM prioritises non-reporters for audit. The ACM publishes the
    # opposite basis - user impact, and the largest companies by customer
    # numbers. Found on four pages in five wordings. This trap is a bookmark of
    # those five, so read the note in CLAUDE.md before trusting a green result.
    (r"(?i)(?:front of the (?:ACM(?:'s|’s)? )?audit queue|"
     r"(?:failed to report|did not self-report|missed the deadline|non-report(?:ers?|ing)|"
     r"failure to report)[^.]{0,90}(?:prioritis|audited first|front of|priority target|"
     r"audit queue)|"
     r"prioritis\w+ (?:organisations|companies|businesses|those) (?:that |who )?"
     r"(?:did not|failed to|have not))",
     "claims a regulator prioritises non-reporting organisations for audit - the ACM's "
     "published basis is user impact and company size, not reporting status (JOB 0q)"),
    # Defect A from JOB 0o: an investigative sequence no regulator publishes.
    #
    # Rebuilt 8 Aug 2026, third widening in one day. The previous version was a
    # list of the wordings we had already been burned by, so each widening found
    # instances the last one could not see: 6, then 13, then 17, then 24. The
    # count of a phrasing list is always a floor.
    #
    # Match the CLAIM in either word order, not a phrasing:
    #   the <thing> is <requested>      "the first document requested"
    #   <requested> ... first           "the document requested first"
    # plus the versions that drop "first" and say "at the start of any complaint".
    #
    # A REQUEST VERB is required. Without it the pattern fires on "an absent
    # statement is the first signal", which is a true sentence about what a
    # reader can infer, not a claim about procedure. A DETERMINER before "first"
    # is required for the same reason: bare "First, it requires..." is an
    # enumerator, not a claim that anything is requested first.
    (r"(?i)(?:"
     r"\b(?:the|a|an|its|their|our|that|this)\s+(?:first|initial)\b[^.]{0,60}?"
     r"\b(?:request(?:s|ed|ing)?|asks? for|asked for|asking for|ask(?:s|ed)? to see|"
     r"seeks?|sought|demands?|demanded|wants? to see|looks? for|looked for)\b"
     r"|"
     r"\b(?:request(?:s|ed|ing)?|asks? for|asked for|asking for|ask(?:s|ed)? to see|"
     r"seeks?|sought|demands?|demanded|wants? to see|looks? for|looked for)\b"
     r"[^.]{0,60}?\bfirst\b"
     r"|"
     r"review the accessibility statement first|statement first in any complaint|"
     r"first in any complaint (?:investigation|process)"
     r"|"
     r"(?:at the (?:very )?start of|early in|at the outset of)\s+(?:any|a|the)\s+"
     r"(?:complaint|enforcement|investigation)"
     r"|"
     # 26th instance, found by reading after this trap had been widened twice and
     # reported the page clean. It states the sequence without using "first" and
     # without a standalone request verb near it: "requests documentation
     # starting with the accessibility statement". It was in body copy and in
     # JSON-LD on the same page.
     r"(?:start(?:s|ing)?|begin(?:s|ning)?) with the (?:accessibility )?statement"
     r"|"
     # 27th instance: "where enforcement bodies look first". Bare "look" without
     # "for", so the request-verb list missed it by one word.
     r"\blook(?:s|ed|ing)?\s+first\b"
     r")",
     "claims the accessibility statement is requested FIRST in a complaint investigation - "
     "no regulator publishes this procedure (JOB 0o defect A)"),
]

# --- CTA overpromise (free tier must orient, not diagnose/rule) ---
CTA_TRAPS = [
    (r"(?i)tells you (which authority|whether the EAA)", "CTA overpromise: claims a definitive scope/authority ruling"),
    (r"(?i)find out whether the EAA applies to your organisation", "CTA overpromise: definitive scope ruling"),
    (r"(?i)where your (key journeys|position) stands?", "CTA overpromise: promises a paid-tier diagnostic"),
]

# --- hard rule 16: the two footer legal links (JOB 0r) ---------------------
#
# THE QUESTION THIS ANSWERS: does this page's footer link BOTH legal documents?
# Not "does the page mention privacy" and not "is there a footer", which are the
# cheaper questions and which 21 pages would pass.
#
# Found 8 August 2026 while measuring accessible-name variation across footers.
# The names split 23/21, and the 21 were not named differently: they had no
# privacy notice link at all. The naming check was the wrong instrument, so this
# is its own check.
#
# WHY IT IS NOT COSMETIC. GDPR Article 14 requires that a person contacted out
# of the blue can find the privacy information. Outreach emails carry the link
# themselves, so sends are covered, but a recipient who lands on any of these
# 21 pages instead has no route to it.
#
# Scoped to <footer> deliberately: a privacy link elsewhere in the body does not
# satisfy rule 16, which is about the footer being the reliable place to look.
FOOTER_LEGAL = [
    ("/accessibility-statement.html", "accessibility statement"),
    ("/privacy.html", "privacy notice"),
]


def _footer_legal_failures(h):
    m = re.search(r"<footer\b.*?</footer>", h, re.S | re.I)
    if not m:
        return ["no <footer> element, so neither legal link can be present (rule 16)"]
    foot = m.group(0)
    out = []
    for href, label in FOOTER_LEGAL:
        if not re.search(r'href\s*=\s*["\']' + re.escape(href), foot, re.I):
            out.append(f"footer has no {label} link ({href}) - hard rule 16. "
                       f"GDPR Article 14 needs the privacy notice reachable from any landing page")
    return out


OG_REQUIRED = [
    'property="og:title"', 'property="og:description"', 'property="og:url"',
    'property="og:image"', 'property="og:image:width"', 'property="og:image:height"',
    'property="og:image:alt"', 'property="og:site_name"',
    'name="twitter:card" content="summary_large_image"', 'name="twitter:image"',
]


# --- EU-wide ranking claims (JOB 0p) ---
_RANK_PAT = re.compile(r"(?i)\b(among the (?:highest|strictest|toughest|most severe|most significant)|"
                       r"one of the (?:highest|strictest|toughest)|at the upper end|places it alongside|"
                       r"(?:highest|strictest|toughest|most severe) (?:maximum )?(?:fine |penalty |)"
                       r"(?:ceiling|ceilings|penalties|fines|regime)s? in)")
_RANK_LEGAL = re.compile(r"(?i)fine|penalt|ceiling|sanction|enforcement|liability")
_RANK_EUWIDE = re.compile(r"(?i)\b(the EU|Europe|European Union|member states?)\b")
_RANK_BOUNDED = re.compile(r"(?i)of the three|of the (?:two|four|five)|Phase 1 markets|of those three")

def strip_tags(h):
    """Text surface for the FACT and CTA traps.

    Includes regions a rendered-text strip would drop. Every trap was blind to
    five of them until 8 August 2026, which is why two claims were structurally
    uncatchable: the 900,000 euro Dutch ceiling lived in a meta description, and
    the JOB 0o complaint procedure lived in a JSON-LD "text" field on a page
    whose visible copy had already been corrected. No pattern could reach either.
    """
    # JSON-LD repeats page copy verbatim. Capture it before <script> is dropped.
    jsonld = " ".join(re.findall(
        r'<script[^>]*application/ld\+json[^>]*>(.*?)</script>', h, re.S | re.I))
    jsonld = jsonld.replace("\\u20ac", "€").replace('\\"', " ")
    # description/title metadata lives in attributes, invisible after tag stripping.
    metas = " ".join(m.group(2) for m in re.finditer(
        r'<meta[^>]*(?:name|property)="([^"]*(?:description|title)[^"]*)"[^>]*content="([^"]*)"',
        h, re.I))
    # accessible names can carry claims too
    names = " ".join(re.findall(r'\b(?:alt|aria-label)="([^"]*)"', h, re.I))

    h = re.sub(r"<script.*?</script>", " ", h, flags=re.S | re.I)
    h = re.sub(r"<style.*?</style>", " ", h, flags=re.S | re.I)
    visible = re.sub(r"<[^>]+>", " ", h)
    # &euro; is how this site writes the sign. Without decoding it, every
    # currency trap is blind to the pages it exists to check.
    visible = visible.replace("&euro;", "\u20ac").replace("&pound;", "\u00a3")
    return " ".join([visible, metas, jsonld, names])


# --- CSS class validation (prevents the "naked page" failure: invented classes not in site.css) ---
_SITE_CSS_CANDIDATES = [
    "site.css", "css/site.css", "./css/site.css",
    os.path.join(os.path.dirname(__file__), "site.css"),
    os.path.join(os.path.dirname(__file__), "css", "site.css"),
    "/mnt/user-data/uploads/site.css", "/mnt/project/site.css",
]

def _report_css_source():
    """Say which site.css was used, or warn loudly that we are guessing.

    Three real failures in one day (nav-cta, status-block, article-cta) passed
    this checker because the embedded fallback vouched for classes it could not
    see. A fallback that says PASS when it means 'probably' is worse than none.
    """
    for c in _SITE_CSS_CANDIDATES:
        if os.path.exists(c):
            print(f"  css: validating against {c}")
            return c
    print("  css: !! site.css NOT FOUND - falling back to the embedded class list.")
    print("       Classes may pass here and render unstyled in the browser.")
    print("       Run from the repo root, where css/site.css exists.")
    return None
# Embedded fallback = the real vocabulary defined in site.css (keep in sync if site.css gains classes).
_REAL_CLASSES = {
    "container","article-container","skip-link","sr-only","site-logo","logo-usable","logo-access",
    "nav-inner","nav-toggle","nav-toggle-bar","nav-links","is-open","nav-cta-slot","nav-cta",
    "page-header","section-label","deck","breadcrumb","page-body","callout","callout--orange",
    "callout--gain","callout--amber","article-cta","cta-button","related-links","related-list",
    "back-link-section","back-link","back-to-top","is-visible",
}
def _load_site_classes():
    classes = set(_REAL_CLASSES)
    for cand in _SITE_CSS_CANDIDATES:
        try:
            with open(cand, encoding="utf-8") as f:
                css = f.read()
            for m in re.findall(r"\.([A-Za-z0-9_-]+)", css):
                classes.add(m)
            break  # first found wins (authoritative)
        except Exception:
            continue
    return classes
SITE_CLASSES = _load_site_classes()
# Known INVENTED classes (from repeated naked-page failures) -> the real class to use instead.
INVENTED_CLASSES = {
    "article": "page-body (wrap content in .page-header + .page-body, not .article)",
    "article-header": "page-header",
    "meta-date": "the badge date span (inline-styled), not a .meta-date class",
    "badge": "section-label (or the inline-styled badge span)",
    "badge--guide": "section-label",
    "cta-block": "article-cta",
    "cta-primary": "cta-button",
    "site-header": "bare <header> (no .site-header class)",
    "site-nav": "bare <nav> (no .site-nav class)",
    "site-footer": "bare <footer> (no .site-footer class)",
}



def _count_prose_dashes(h):
    """Return (prose_count, excluded_count) of em dashes.

    Prose means text a reader meets as a sentence, inside <main>. Excluded:
    <style>, <script> (which includes JSON-LD), HTML and CSS comments, <title>,
    every <meta>, headings h1-h6, section-label <span>s, and related-link
    <li><a> titles. Those last three are JOB 0n exceptions 1 and 4: a dash used
    as a title or label separator, not as an aside hung off a main clause.
    """
    def _n(t):
        return t.count("\u2014") + t.count("&mdash;")

    total = _n(h)

    body_m = re.search(r"<main\b[^>]*>(.*?)</main>", h, re.S | re.I)
    region = body_m.group(1) if body_m else h

    # strip everything a reader never meets as prose
    region = re.sub(r"<script.*?</script>", " ", region, flags=re.S | re.I)
    region = re.sub(r"<style.*?</style>", " ", region, flags=re.S | re.I)
    region = re.sub(r"<!--.*?-->", " ", region, flags=re.S)
    region = re.sub(r"/\*.*?\*/", " ", region, flags=re.S)

    # exception 1: headings, section labels, related-link titles
    region = re.sub(r"<h[1-6]\b[^>]*>.*?</h[1-6]>", " ", region, flags=re.S | re.I)
    # label spans: .section-label, and page-local variants such as
    # .requirement-number used for the "Checklist - Governance" headings
    region = re.sub(r"<span[^>]*class=\"[^\"]*(?:section-label|requirement-number|"
                    r"article-tag|insight-tag|badge)[^\"]*\"[^>]*>.*?</span>",
                    " ", region, flags=re.S | re.I)
    region = re.sub(r"<li>\s*<a\b.*?</a>", " ", region, flags=re.S | re.I)
    # the inline-styled badge span used in place of .section-label on article pages
    region = re.sub(r"<span[^>]*text-transform:\s*uppercase[^>]*>.*?</span>",
                    " ", region, flags=re.S | re.I)

    prose = _n(re.sub(r"<[^>]+>", " ", region))
    return prose, max(0, total - prose)

def check(path):
    name = os.path.basename(path)
    h = open(path, encoding="utf-8", errors="ignore").read()
    body = strip_tags(h)
    fails, warns, notes = [], [], []

    # --- infrastructure ---
    if 'rel="canonical"' not in h:
        fails.append("no canonical")
    else:
        m = re.search(r'rel="canonical"\s+href="([^"]+)"', h)
        if m and not m.group(1).rstrip("/").endswith(name.replace(".html", "")) \
           and not m.group(1).rstrip("/").endswith(name):
            warns.append(f"canonical may not be self-referencing: {m.group(1)}")
    if CLARITY not in h: fails.append("no Clarity snippet")
    if GA4 not in h: fails.append("no GA4")
    if 'id="main" tabindex="-1"' not in h: fails.append('missing <main id="main" tabindex="-1">')
    if 'class="skip-link"' not in h: fails.append("no skip link")
    if 'id="back-to-top"' not in h and 'class="back-to-top"' not in h: fails.append("no back-to-top element")
    elif "back-to-top" not in h.split("</body>")[0].split("<script")[-1] and \
         "getElementById('back-to-top')" not in h:
        warns.append("back-to-top element present but JS not found")

    # --- social preview block ---
    # A redirect stub is not a social destination. Giving it a full OG block
    # tells crawlers to treat a page that immediately leaves as somewhere to
    # land, so ua_sync_blocks.py deliberately skips them. Without this exemption
    # the checker would fail such a page forever, and a permanent known failure
    # trains people to ignore the count.
    is_redirect_stub = bool(re.search(r'http-equiv="refresh"', h, re.I))
    missing_og = [] if is_redirect_stub else [t for t in OG_REQUIRED if t not in h]
    if is_redirect_stub:
        notes.append("redirect stub - OG block not required")
    if missing_og:
        fails.append("OG block incomplete: " + ", ".join(
            t.split('"')[1] if '"' in t else t for t in missing_og))
    if 'content="summary"' in h:
        fails.append('twitter:card is "summary" — must be summary_large_image')

    # --- meta description ---
    m = re.search(r'name="description"\s+content="([^"]*)"', h)
    if not m:
        fails.append("no meta description")
    else:
        n = len(m.group(1))
        if n > 155: fails.append(f"meta description {n} chars (limit 155)")
        else: notes.append(f"meta {n} chars")

    # --- related links ---
    if "/eaa-enforcement.html" not in h: warns.append("related-links missing enforcement hub")
    if "how-to-audit-eaa-compliance" not in h: warns.append("related-links missing audit guide")
    cs = set(re.findall(r"/eaa-compliance-[a-z]+\.html|/bfsg-germany[a-z-]*\.html", h))
    cs = {c for c in cs if name.replace(".html", "") not in c}
    if len(cs) < 2: warns.append(f"only {len(cs)} related country/sector page(s), standard wants 2+")

    # --- markup integrity ---
    if h.count("<a ") != h.count("</a>"):
        fails.append(f"anchor imbalance: {h.count('<a ')} open / {h.count('</a>')} close")

    # --- FAQ block + schema (SEO: eligible for rich results) ---
    has_faq = bool(re.search(r'(?i)(frequently asked|<h2[^>]*>\s*FAQ|class="faq)', h))
    has_faq_schema = "FAQPage" in h
    if has_faq and not has_faq_schema:
        warns.append("FAQ section present but no FAQPage schema (missing rich-result eligibility)")
    elif not has_faq:
        notes.append("no FAQ block")
    else:
        notes.append("FAQ + schema")

    # --- date badge ---
    if not re.search(r"Updated \d{1,2} [A-Z][a-z]{2} 20\d\d", h):
        warns.append("no 'Updated D Mon YYYY' badge found")
    else:
        notes.append(re.search(r"Updated \d{1,2} [A-Z][a-z]{2} 20\d\d", h).group(0))

    # --- em dashes: PROSE ONLY (JOB 0m) ---
    # The old count was every dash in the file, which measured the wrong thing.
    # It included HTML and CSS comments, <title>, meta descriptions, headings,
    # section labels and related-link titles - all of them legitimate separators
    # under the JOB 0n exceptions. index.html reported 36 when 7 were code-comment
    # banners no reader sees, and six finished pages reported as unfinished because
    # their only remaining dashes were related-link titles.
    n_prose, n_excl = _count_prose_dashes(h)
    if n_prose > 2:
        warns.append(f"{n_prose} em dashes in prose ({n_prose + n_excl} in file, "
                     f"{n_excl} outside prose) - check they are sparing and appropriate")
    else:
        notes.append(f"{n_prose} em dashes in prose ({n_prose + n_excl} in file, "
                     f"{n_excl} outside prose)")

    # --- fact + CTA traps ---
    # ComReg is checked SENTENCE BY SENTENCE, not page-wide. The old page-wide
    # bypass scanned the whole file for telecom/electronic communications and
    # skipped the trap if it found any, which silenced all 13 pages carrying
    # ComReg. On eaa-compliance-ecommerce.html the only match was the Swedish
    # regulator's name, "PTS (Post and Telecom Authority)", so mentioning Sweden
    # disabled the Irish trap. On eaa-fines-penalties the offending cell itself
    # read "ComReg (telecoms/digital services)", so the defect exempted itself.
    # The exemption is scoped to the SENTENCE, never to the page. A page-wide
    # bypass is what silenced all 13 pages: it scanned the whole file for
    # telecom/electronic communications and skipped the trap on any hit. False
    # positives on genuine telecoms copy are accepted as the cheaper error.
    for m in re.finditer(r"[^.!?]*\bComReg\b[^.!?]*[.!?]?", body):
        sent = m.group(0).strip()
        if re.search(r"(?i)not ComReg", sent):
            notes.append("ComReg appears in a corrective 'not ComReg' construction")
            continue
        # Correct only where the SAME sentence scopes it to electronic communications.
        # A named operator or a bare "operator" supplies the telecoms context just
        # as well as the phrase "electronic communications". Not recognising that
        # fired on two correct sentences: one naming Three Ireland, one about what
        # an operator has to show.
        if re.search(r"(?i)electronic communications|communications regulation|"
                     r"Commission for Communications|\boperators?\b|telecoms?\b|"
                     r"Three Ireland", sent):
            # ...unless that sentence also widens it past communications.
            if re.search(r"(?i)and digital services|/digital services|telecoms/digital", sent):
                fails.append("FACT: ComReg scoped to communications AND widened to "
                             "'digital services' in the same breath - rule 7 allows "
                             "electronic communications ONLY: " + sent[:120])
            continue
        fails.append("FACT: ComReg used outside an electronic-communications context - "
                     "rule 7: CCPC for products/e-commerce/general services, Central Bank "
                     "for financial, ComReg for electronic communications ONLY: " + sent[:120])
    for m in re.finditer(r"[^.!?]*\bComReg\b[^.!?]*[.!?]?", body):
        sent = m.group(0).strip()
        if re.search(r"(?i)and digital services|/digital services|telecoms/digital", sent):
            fails.append("FACT: ComReg widened past electronic communications to "
                         "'digital services' - rule 7 allows electronic communications "
                         "ONLY: " + sent[:120])
    # --- "first EAA ruling" must carry its qualifier ---
    # Saying a ruling was the first is fine. Saying it without noting WHICH first
    # it was is the error: Auchan (Lille, 5 May 2026) came first and was dismissed
    # on a procedural threshold; Carrefour (Caen, 4 June 2026) was the first
    # ordering compliance. A bare claim collapses the two.
    for m in re.finditer(r"[^.!?]*first[^.!?]{0,40}(?:EAA )?(?:court )?ruling[^.!?]*[.!?]?",
                         body, re.I):
        sent = m.group(0)
        # The qualifier can be phrased many ways. "ordering compliance" was the
        # only form anticipated first time, and it missed "the first EAA ruling
        # ORDERING AN ORGANISATION to make its digital services accessible" -
        # the same paraphrase problem JOB 0p records, in a trap written to fix it.
        if re.search(r"(?i)dismiss|procedural|threshold|order(?:ing|ed)|"
                     r"defendant|in the EU|in Europe|compliance order", sent):
            continue
        fails.append("FACT: bare 'first EAA ruling' claim - say which first. Lille "
                     "5 May 2026 was first overall and was DISMISSED on a procedural "
                     "threshold; Caen 4 June 2026 was first ORDERING COMPLIANCE: "
                     + " ".join(sent.split())[:120])

    # --- Barometro figures: criteria are not outcomes ---
    # BOTH figures are real and neither is wrong. 18% is legal non-conformity;
    # 32% is technical inadequacy against WCAG criteria. The error is using
    # either as an OUTCOME claim, because failing a criterion does not establish
    # that a specific transaction is impossible. The old trap matched a bare
    # "32%" and fired on E.Leclerc's RGAA conformance score, an unrelated number.
    for m in re.finditer(r"[^.!?]*\b(?:32|18)%[^.!?]*[.!?]?", body):
        sent = m.group(0)
        if not re.search(r"(?i)Bar.metro|financial services|WCAG|conformity|non-conform", sent):
            continue
        if re.search(r"(?i)cannot complete|unable to complete|fail to support|"
                     r"fail at (?:exactly )?these journeys|prevents? users from completing|"
                     r"means users cannot", sent):
            fails.append("FACT: a Barometro figure used as an OUTCOME claim. 18% is legal "
                         "non-conformity and 32% is technical inadequacy against WCAG "
                         "criteria; failing a criterion does not establish that a "
                         "transaction is impossible: " + " ".join(sent.split())[:120])

    # --- EU-wide ranking claims (JOB 0p) ---
    # Any claim that a market's penalties rank highest/strictest in the EU is
    # unsupportable by construction: nobody here has surveyed 27 transpositions.
    # That makes a pattern match a complete test rather than an approximation.
    # BOUNDED comparisons are exempt. "the sharpest regime of the three" compares
    # three surveyed markets and is the standing corrections' own wording.
    for m in _RANK_PAT.finditer(body):
        w = body[max(0, m.start() - 220):m.start() + 240]
        if not (_RANK_LEGAL.search(w) and _RANK_EUWIDE.search(w)):
            continue
        if _RANK_BOUNDED.search(w):
            continue
        fails.append("FACT: unsupportable EU-wide ranking claim - nobody has surveyed "
                     "27 transpositions, so no market can be placed highest or strictest: "
                     + " ".join(w[200:360].split()))
    for pat, msg in FACT_TRAPS:
        if "ComReg" in msg:
            continue  # handled above
        seen = set()
        for m in re.finditer(pat, body):
            # Report the sentence, not only the rule. A trap that prints its own
            # message and nothing else says a page is dirty without saying where,
            # and every widening of the JOB 0o trap needed the matched text to
            # tell a real hit from a false one. Dedupe: a meta description is
            # repeated in og: and twitter:, so one claim would report three times.
            s = body.rfind(".", 0, m.start()) + 1
            e = body.find(".", m.end())
            snippet = " ".join(body[s:e + 1 if e != -1 else len(body)].split())[:200]
            if snippet in seen:
                continue
            seen.add(snippet)
            fails.append(f"FACT: {msg}: {snippet}")
    for pat, msg in CTA_TRAPS:
        if re.search(pat, body): fails.append("CTA: " + msg)

    # --- hard rule 16: both legal links in the footer ---
    for msg in _footer_legal_failures(h):
        fails.append("FOOTER: " + msg)


    # --- pronoun misuse: "us/we/our" must mean Usable Access, never the reader ---
    for _tag, _pat in [("H1", r"<h1[^>]*>(.*?)</h1>"),
                       ("title", r"<title>(.*?)</title>"),
                       ("meta description", r'<meta name="description" content="([^"]*)"')]:
        for _m in re.finditer(_pat, h, re.S):
            _t = re.sub(r"<[^>]+>", "", _m.group(1))
            if re.search(r"\b(apply to us|for us|do we|are we|should we|our (business|organisation|company|obligations))\b", _t, re.I):
                fails.append(f"PRONOUN: {_tag} uses we/our/us to mean the READER "
                             f"(\"{_t.strip()[:60]}\") \u2014 on UA content we/our always means Usable Access. Use you/your.")
    # slug: "-to-us" reads as the United States in a URL
    if re.search(r"-to-us\.html$", os.path.basename(path)):
        fails.append("PRONOUN: filename ends '-to-us.html' \u2014 reads as US (United States) in a slug. Rename.")

    # --- class validation: every class used must be defined in site.css OR the page's own <style> ---
    inline_defined = set()
    for style in re.findall(r"<style[^>]*>(.*?)</style>", h, re.S):
        for m in re.findall(r"\.([A-Za-z0-9_-]+)", style):
            inline_defined.add(m)
    used = set()
    for attr in re.findall(r'class="([^"]+)"', h):
        for c in attr.split():
            used.add(c)
    defined = SITE_CLASSES | inline_defined
    for c in sorted(used - defined):
        # A BEM modifier (base--mod) is fine if its BASE class is defined — it just falls back to base styling.
        # The naked-page failure is an undefined BASE, so only fail when the base itself is undefined.
        base = c.split("--")[0]
        if "--" in c and base in defined:
            continue
        if c in INVENTED_CLASSES:
            fails.append(f"CSS: invented class '{c}' is not in site.css — use {INVENTED_CLASSES[c]}")
        else:
            fails.append(f"CSS: class '{c}' is not defined in site.css or an inline <style> (page would render unstyled)")

    return name, fails, warns, notes

def main():
    _report_css_source()
    folder = sys.argv[1] if len(sys.argv) > 1 else "."
    files = sorted(glob.glob(os.path.join(folder, "*.html")))
    if not files:
        print("No .html files found in", folder); return
    tot_f = tot_w = 0
    for f in files:
        name, fails, warns, notes = check(f)
        status = "FAIL" if fails else ("WARN" if warns else "PASS")
        print(f"\n{'='*62}\n{name}   [{status}]")
        for x in fails: print("   FAIL  " + x)
        for x in warns: print("   warn  " + x)
        if notes: print("   ok    " + "; ".join(notes))
        tot_f += len(fails); tot_w += len(warns)
    print(f"\n{'='*62}\n{len(files)} pages | {tot_f} failures | {tot_w} warnings")

if __name__ == "__main__":
    main()
