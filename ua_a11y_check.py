#!/usr/bin/env python3
"""
UA static accessibility checker — for UA's OWN site pages.

Why this exists: ua_page_check.py validates CSS classes, fact traps and CTA
wording. None of that is accessibility. The site was manually audited in June;
every page added since (statement, telecoms, overlay, and whatever follows) is
an unguarded regression risk on the one site that must be exemplary.

This encodes the checks from that manual audit so they run on every page, every
time, automatically.

WHAT IT CANNOT DO: this is static analysis. It cannot judge whether an
accessible name is *meaningful*, whether focus order makes sense, whether a
screen-reader announcement is comprehensible, or anything requiring a rendered
page. Those stay manual — the same limitation UA tells clients about. A pass
here means the groundwork is right, not that the page is accessible.

Usage:
    python3 ua_a11y_check.py page.html [more.html ...]
    python3 ua_a11y_check.py /path/to/folder
    python3 ua_a11y_check.py . insights     <- prefer this
    python3 ua_a11y_check.py --selftest     <- consistency-check fixtures
Exit code 1 if any FAIL.

RUN BOTH FOLDERS IN ONE INVOCATION. The accessible-name consistency check votes
across the pages it is given, so the other pages ARE the specification. Checking
`.` and `insights` separately gives it 32 pages and then 12, instead of 44, and
a smaller electorate is a weaker check.
"""
import sys, os, re, glob
from bs4 import BeautifulSoup

FAIL, WARN = "FAIL", "WARN"

# ARIA roles that are valid; a typo here is a silent accessibility bug
VALID_ROLES = {
    "alert","alertdialog","application","article","banner","button","cell","checkbox",
    "columnheader","combobox","complementary","contentinfo","definition","dialog",
    "directory","document","feed","figure","form","grid","gridcell","group","heading",
    "img","link","list","listbox","listitem","log","main","marquee","math","menu",
    "menubar","menuitem","menuitemcheckbox","menuitemradio","navigation","none","note",
    "option","presentation","progressbar","radio","radiogroup","region","row","rowgroup",
    "rowheader","scrollbar","search","searchbox","separator","slider","spinbutton",
    "status","switch","tab","table","tablist","tabpanel","term","textbox","timer",
    "toolbar","tooltip","tree","treegrid","treeitem",
}
INTERACTIVE = {"a","button","input","select","textarea"}


def text_of(el):
    return " ".join(el.get_text(" ", strip=True).split())


def accessible_name(el):
    """Rough accessible-name computation. Deliberately conservative."""
    if el.get("aria-label", "").strip():
        return el["aria-label"].strip()
    if el.get("aria-labelledby"):
        return "(aria-labelledby)"
    t = text_of(el)
    if t:
        return t
    img = el.find("img")
    if img is not None and img.get("alt", "").strip():
        return img["alt"].strip()
    if el.get("title", "").strip():
        return el["title"].strip()
    if el.name == "input" and el.get("value", "").strip() and el.get("type") in ("submit", "button", "reset"):
        return el["value"].strip()
    return ""


# --- JOB 0r: accessible-name consistency across pages ---------------------
#
# THE QUESTION THIS ANSWERS: does this element's accessible name match the name
# the same element has everywhere else? Not "does it have a name", which is what
# every other name check here asks, and which passed the logo announcing
# "Usable Access comma home" on eaa-accessibility-statement.html.
#
# WHY THIS SHAPE IS DIFFERENT. Every trap written for this repo has failed at
# least once because it needed to know in advance what wrong looks like: a list
# of phrasings, a literal currency sign, a set of class names. This one needs to
# know only what DIFFERENT looks like. There is no vocabulary to widen and no
# wording it can be blind to. A single-page corruption of repeated chrome cannot
# hide from it, because the other 30 pages are the specification.
#
# HOW IT DECIDES. For each selector below, collect the accessible name found on
# every page, take the majority, and fail any page that disagrees. A tie means
# there is no majority and nothing is reported: with two variants at 50/50 we
# cannot say which is the corruption, and guessing would be worse than silence.
#
# SCOPE, decided by measuring rather than by assuming. Across 44 pages:
#   site logo    44 pages, 1 name    skip link   44 pages, 1 name
#   back to top  44 pages, 1 name    main nav    44 pages, 1 name
#   nav CTA      26 pages, 1 name
# Those five are chrome with one purpose and no legitimate variation, so a
# disagreement is a defect and they FAIL.
#
#   CTA button   41 pages, 4 names
# The CTA is different. 35 pages say "Book your free assessment today", 4 say
# "Book your free assessment", and 2 legitimately differ because they ask for
# something else ("Book a 20-minute call", "Five questions to check"). A
# majority vote would call all six a defect and be wrong about two, so it WARNS.
#
# Footer links were measured too and deliberately left out. They split 23/21,
# but the difference is that 21 pages omit the privacy notice link entirely.
# That is a missing-link defect under hard rule 16, not a naming inconsistency,
# and reporting it here would describe it wrongly. It needs its own check.
REPEATED_ELEMENTS = [
    ("site logo",    lambda s: s.select("a.site-logo")),
    ("skip link",    lambda s: s.select("a.skip-link")),
    ("back to top",  lambda s: s.select("a.back-to-top, button.back-to-top")),
    ("nav CTA",      lambda s: s.select("a.nav-cta")),
    ("main nav",     lambda s: s.select("nav[aria-label]")),
]
# Same vote, reported as a warning, for elements where variation can be genuine.
REPEATED_SOFT = [
    ("CTA button",   lambda s: s.select("a.cta-button")),
]
# Below this share of pages an element is not "repeated chrome" and a majority
# means little. The logo is on every page; something on three is not a pattern.
MIN_PAGES = 5


def collect_names(path, elements=None):
    """Return {label: name} for the repeated elements present on this page."""
    soup = BeautifulSoup(open(path, encoding="utf-8", errors="ignore").read(), "html.parser")
    return names_from_soup(soup, elements)


def names_from_soup(soup, elements=None):
    found = {}
    for label, sel in (elements if elements is not None else REPEATED_ELEMENTS):
        els = sel(soup)
        if not els:
            continue
        if label == "main nav":
            found[label] = els[0].get("aria-label", "").strip()
        else:
            found[label] = accessible_name(els[0])
    return found


def name_consistency(per_page):
    """per_page: {path: {label: name}} -> list of (path, label, got, expected, share)."""
    from collections import Counter
    out = []
    labels = {l for names in per_page.values() for l in names}
    for label in sorted(labels):
        seen = {p: n[label] for p, n in per_page.items() if label in n}
        if len(seen) < MIN_PAGES:
            continue
        counts = Counter(seen.values()).most_common()
        if len(counts) == 1:
            continue
        top, n_top = counts[0]
        if len(counts) > 1 and counts[1][1] == n_top:
            continue  # no majority; see the note above
        for path, name in sorted(seen.items()):
            if name != top:
                out.append((path, label, name, top, f"{n_top}/{len(seen)}"))
    return out


def check(path):
    issues = []
    html = open(path, encoding="utf-8", errors="ignore").read()
    soup = BeautifulSoup(html, "html.parser")

    def add(sev, code, msg):
        issues.append((sev, code, msg))

    # --- 3.1.1 language of page ---
    htmltag = soup.find("html")
    if htmltag is None or not htmltag.get("lang", "").strip():
        add(FAIL, "3.1.1", "<html> has no lang attribute")

    # --- page title ---
    title = soup.find("title")
    if title is None or not text_of(title):
        add(FAIL, "2.4.2", "page has no <title>")

    # --- 1.3.1 / 2.4.1 landmarks and skip link ---
    if soup.find("main") is None and not soup.find(attrs={"role": "main"}):
        add(FAIL, "1.3.1", "no <main> landmark")
    if soup.find("nav") is None and not soup.find(attrs={"role": "navigation"}):
        add(WARN, "1.3.1", "no <nav> landmark")
    skip = None
    for a in soup.find_all("a", href=True):
        if a["href"].startswith("#") and re.search(r"skip", text_of(a), re.I):
            skip = a
            break
    if skip is None:
        add(WARN, "2.4.1", "no skip link found")
    else:
        target = skip["href"][1:]
        if target and not (soup.find(id=target) or soup.find(attrs={"name": target})):
            add(FAIL, "2.4.1", f"skip link points to #{target}, which does not exist")

    # --- 1.3.1 headings: exactly one h1, no skipped levels ---
    h1s = soup.find_all("h1")
    if len(h1s) == 0:
        add(FAIL, "1.3.1", "no <h1>")
    elif len(h1s) > 1:
        add(FAIL, "1.3.1", f"{len(h1s)} <h1> elements (expected exactly 1)")
    levels = [int(h.name[1]) for h in soup.find_all(re.compile(r"^h[1-6]$"))]
    prev = None
    for lv in levels:
        if prev is not None and lv > prev + 1:
            add(FAIL, "1.3.1", f"heading level skips h{prev} to h{lv}")
            break
        prev = lv
    for h in soup.find_all(re.compile(r"^h[1-6]$")):
        if not text_of(h):
            add(FAIL, "1.3.1", f"empty <{h.name}>")

    # --- 1.1.1 images ---
    for img in soup.find_all("img"):
        if img.get("alt") is None:
            src = (img.get("src") or "?")[:60]
            add(FAIL, "1.1.1", f"<img> without alt attribute: {src}")
    # decorative svg should be hidden or labelled
    for svg in soup.find_all("svg"):
        if not (svg.get("aria-hidden") or svg.get("aria-label") or svg.get("role") or svg.find("title")):
            add(WARN, "1.1.1", "inline <svg> with no aria-hidden, aria-label, role or <title>")

    # --- 2.4.4 / 4.1.2 links and buttons must have accessible names ---
    for a in soup.find_all("a"):
        if a.get("href") is None:
            continue
        if not accessible_name(a):
            add(FAIL, "2.4.4", f"link with no accessible name (href={a.get('href','')[:50]})")
    for b in soup.find_all("button"):
        if not accessible_name(b):
            add(FAIL, "4.1.2", "<button> with no accessible name")

    # --- 3.3.2 form inputs need labels ---
    for inp in soup.find_all(["input", "select", "textarea"]):
        itype = (inp.get("type") or "").lower()
        if itype in ("hidden", "submit", "button", "reset", "image"):
            continue
        named = bool(inp.get("aria-label", "").strip() or inp.get("aria-labelledby"))
        if not named and inp.get("id"):
            named = soup.find("label", attrs={"for": inp["id"]}) is not None
        if not named and inp.find_parent("label") is not None:
            named = True
        if not named and inp.get("title", "").strip():
            named = True
        if not named:
            add(FAIL, "3.3.2", f"<{inp.name}> has no associated label (id={inp.get('id','none')})")

    # --- 4.1.2 ARIA sanity ---
    for el in soup.find_all(attrs={"role": True}):
        for role in el["role"].split():
            if role not in VALID_ROLES:
                add(FAIL, "4.1.2", f"invalid ARIA role '{role}' on <{el.name}>")
    for el in soup.find_all(attrs={"aria-labelledby": True}):
        for ref in el["aria-labelledby"].split():
            if not soup.find(id=ref):
                add(FAIL, "4.1.2", f"aria-labelledby points to missing id '{ref}'")
    for el in soup.find_all(attrs={"aria-describedby": True}):
        for ref in el["aria-describedby"].split():
            if not soup.find(id=ref):
                add(WARN, "4.1.2", f"aria-describedby points to missing id '{ref}'")
    for el in soup.find_all(attrs={"aria-expanded": True}):
        if el["aria-expanded"] not in ("true", "false"):
            add(FAIL, "4.1.2", f"aria-expanded must be true/false, got '{el['aria-expanded']}'")
    # interactive elements hidden from AT
    for el in soup.find_all(attrs={"aria-hidden": "true"}):
        if el.name in INTERACTIVE or el.find(list(INTERACTIVE)):
            add(FAIL, "4.1.2", f"aria-hidden='true' on or around an interactive element (<{el.name}>)")

    # --- 4.1.1 duplicate ids (breaks label and aria references) ---
    seen, dupes = set(), set()
    for el in soup.find_all(id=True):
        i = el["id"]
        if i in seen:
            dupes.add(i)
        seen.add(i)
    for d in sorted(dupes):
        add(FAIL, "4.1.1", f"duplicate id '{d}'")

    # --- 1.3.1 tables need headers ---
    for tbl in soup.find_all("table"):
        if tbl.find("th") is None:
            add(FAIL, "1.3.1", "<table> with no <th> header cells")
        else:
            for th in tbl.find_all("th"):
                if not th.get("scope") and not th.get("id"):
                    add(WARN, "1.3.1", "<th> without scope attribute")
                    break

    # --- 1.4.4 zoom must not be disabled ---
    vp = soup.find("meta", attrs={"name": "viewport"})
    if vp and vp.get("content"):
        c = vp["content"].replace(" ", "").lower()
        if "user-scalable=no" in c or re.search(r"maximum-scale=1(\.0)?\b", c):
            add(FAIL, "1.4.4", "viewport disables zoom (user-scalable=no or maximum-scale=1)")

    # --- 2.4.4 vague link text ---
    for a in soup.find_all("a", href=True):
        t = accessible_name(a).strip().lower().rstrip(" .>»→")
        if t in ("click here", "here", "read more", "more", "link", "this"):
            add(WARN, "2.4.4", f"vague link text: '{t}'")

    # --- positive signals worth confirming ---
    css = html.lower()
    notes = []
    if "prefers-reduced-motion" not in css:
        notes.append("no prefers-reduced-motion handling found (check site.css)")
    if ":focus-visible" not in css and "focus-visible" not in css:
        notes.append("no focus-visible styling found in-page (check site.css)")
    return issues, notes


def selftest_consistency():
    """Prove the check catches the real defect and stays quiet where it should.

    The real defect: on 8 Aug 2026 one page carried
    aria-label="Usable Access , home" while 43 carried the em dash. A screen
    reader announced "Usable Access comma home". Every other name check here
    passed it, because they ask whether a name exists.
    """
    GOOD, BAD = "Usable Access — home", "Usable Access , home"
    cases = [
        ("the real defect: 1 page differs from 43",
         {f"p{i}.html": {"site logo": GOOD} for i in range(43)} | {"bad.html": {"site logo": BAD}},
         [("bad.html", "site logo", BAD, GOOD)]),
        ("all pages agree", {f"p{i}.html": {"site logo": GOOD} for i in range(44)}, []),
        ("a 50/50 tie reports nothing, because neither side is the specification",
         {f"a{i}.html": {"site logo": GOOD} for i in range(6)} |
         {f"b{i}.html": {"site logo": BAD} for i in range(6)}, []),
        ("under MIN_PAGES the vote is not meaningful",
         {f"p{i}.html": {"site logo": GOOD} for i in range(3)} | {"bad.html": {"site logo": BAD}}, []),
        ("two odd pages out of many are both reported",
         {f"p{i}.html": {"site logo": GOOD} for i in range(20)} |
         {"x.html": {"site logo": BAD}, "y.html": {"site logo": "Usable Access, home"}},
         [("x.html", "site logo", BAD, GOOD),
          ("y.html", "site logo", "Usable Access, home", GOOD)]),
    ]
    bad = 0
    for why, per_page, expected in cases:
        got = [(p, l, g, e) for p, l, g, e, _ in name_consistency(per_page)]
        if sorted(got) != sorted(expected):
            print(f"WRONG ({why})\n   expected {expected}\n   got      {got}")
            bad += 1
    print(f"consistency selftest: {len(cases)} cases, {bad} wrong")
    return bad


def main():
    args = sys.argv[1:]
    if "--selftest" in args:
        sys.exit(1 if selftest_consistency() else 0)
    if not args:
        print(__doc__)
        sys.exit(0)
    files = []
    for a in args:
        if os.path.isdir(a):
            files += sorted(glob.glob(os.path.join(a, "*.html")))
        else:
            files.append(a)

    total_fail = total_warn = 0
    print("=" * 62)
    print("UA STATIC ACCESSIBILITY CHECK")
    print("=" * 62)

    # Cross-page pass first, so its findings attach to the pages below.
    cross = {}
    if len(files) >= MIN_PAGES:
        for elements, sev in ((REPEATED_ELEMENTS, FAIL), (REPEATED_SOFT, WARN)):
            per_page = {f: collect_names(f, elements) for f in files}
            for path, label, got, expected, share in name_consistency(per_page):
                cross.setdefault(path, []).append(
                    (sev, "4.1.2", f"{label} accessible name is {got!r} but {share} pages "
                                   f"use {expected!r} — repeated elements must announce identically"))

    for f in files:
        issues, notes = check(f)
        issues += cross.get(f, [])
        fails = [i for i in issues if i[0] == FAIL]
        warns = [i for i in issues if i[0] == WARN]
        total_fail += len(fails)
        total_warn += len(warns)
        status = "FAIL" if fails else ("warn" if warns else "PASS")
        print(f"\n{os.path.basename(f)}  [{status}]")
        for sev, code, msg in fails:
            print(f"   FAIL  {code}  {msg}")
        for sev, code, msg in warns:
            print(f"   warn  {code}  {msg}")
        for n in notes:
            print(f"   note        {n}")
    print("\n" + "=" * 62)
    print(f"{len(files)} pages | {total_fail} failures | {total_warn} warnings")
    print("Static checks only. Keyboard order, screen-reader comprehensibility and")
    print("visual focus still require a manual pass before publishing.")
    print("=" * 62)
    sys.exit(1 if total_fail else 0)


if __name__ == "__main__":
    main()
