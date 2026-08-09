#!/usr/bin/env python3
"""
ua_orphan_check.py — the internal link graph.

Usage:  python3 ua_orphan_check.py [root]   (default ".", always includes insights/)
        python3 ua_orphan_check.py --selftest

THE QUESTION THIS ANSWERS
-------------------------
Not "is this page linked from anywhere", which every page passes because the
global nav and the footer link several pages from all 44. The question is:

    Can a reader reach this page from inside somebody's argument?

So links are counted from <main> only, and links from <main> are further split
by what kind of link they are. A page whose only inbound links are a card on
insights.html and a Related entry is, for crawl and for readers, close to
unreachable. The Sweden article had exactly that and was never fetched.

  body     inside a sentence in running copy. What the protocol wants.
  related  inside .related-links / .related-list. Cheaper and weaker.
  card     inside a listing card on index.html or insights.html.
  chrome   nav, header, footer. Counted separately and never toward the total,
           because being in the nav tells you nothing about a deep page.

UA_Publishing_Protocol.md: three to six inbound, at least two of them body.

KNOWN-ACCEPTABLE, NOT DEFECTS
-----------------------------
index.html is excluded from the under-linked report. It is linked from the
global nav on all 44 pages and is the target of every external link, so it is
the most-linked page on the site; JOB 0j records it as a false positive.
privacy.html and accessibility-statement.html are footer pages by design and
are reported in their own category rather than as orphans.

WHAT IT CANNOT DO
-----------------
It cannot judge whether a link arrives at the right moment for the reader,
which is the thing that actually decides whether a link works. See JOB 0j: do
not link from pages whose reader is past that question. It also does not see
links added by JavaScript, and it treats a sitemap entry as a claim rather than
as evidence a page exists (hard rule 14).
"""
import sys, os, re, glob
from collections import defaultdict
from bs4 import BeautifulSoup

NAV_EXCLUDED = {"index.html"}
FOOTER_PAGES = {"privacy.html", "accessibility-statement.html"}
WANT_TOTAL, WANT_BODY = 3, 2

RELATED_CLASS = re.compile(r"related", re.I)
# Listing containers. "card" alone was not enough: the insights.html index wraps
# each entry in <div class="article-list"> with no "card" anywhere, so 15 listing
# entries counted as body copy on the first run. That is this checker committing
# the easier-question error in its own first hour - is the link inside <main>,
# rather than is the link inside running copy.
CARD_CLASS = re.compile(r"card|article-list|insights-grid|grid|listing", re.I)


def classify(a):
    """body | related | card, for a link already known to be inside <main>."""
    # An <a> that wraps a heading is a listing entry, whatever its container is
    # called. A link inside a sentence never contains an <h2>.
    if a.find(["h1", "h2", "h3", "h4"]) is not None:
        return "card"
    for parent in a.parents:
        cls = " ".join(parent.get("class", []) or [])
        if RELATED_CLASS.search(cls):
            return "related"
        if CARD_CLASS.search(cls):
            return "card"
        if parent.name == "main":
            break
    return "body"


def resolve(href, from_page):
    """Return a repo-relative .html path, or None if this is not an internal page link."""
    href = href.strip()
    if not href or href.startswith(("mailto:", "tel:", "#", "javascript:")):
        return None
    if re.match(r"^[a-z]+://", href, re.I):
        return None
    href = href.split("#", 1)[0].split("?", 1)[0]
    if not href:
        return None
    if href in ("/", ""):
        return "index.html"
    if href.startswith("/"):
        path = href.lstrip("/")
    else:
        path = os.path.normpath(os.path.join(os.path.dirname(from_page), href))
    if path.endswith("/"):
        path += "index.html"
    if not path.endswith(".html"):
        return None
    return path.replace(os.sep, "/")


def build(root="."):
    pages = sorted(
        [os.path.relpath(p, root).replace(os.sep, "/")
         for p in glob.glob(os.path.join(root, "*.html"))] +
        [os.path.relpath(p, root).replace(os.sep, "/")
         for p in glob.glob(os.path.join(root, "insights", "*.html"))])
    inbound = {p: defaultdict(list) for p in pages}
    unresolved = []
    for page in pages:
        soup = BeautifulSoup(open(os.path.join(root, page), encoding="utf-8",
                                  errors="ignore").read(), "html.parser")
        main = soup.find("main")
        seen_pairs = set()
        for scope, area in (("main", main), ("chrome", soup)):
            if area is None:
                continue
            for a in area.find_all("a", href=True):
                if scope == "chrome" and main is not None and a.find_parent("main") is not None:
                    continue
                target = resolve(a["href"], page)
                if target is None:
                    continue
                if target not in inbound:
                    unresolved.append((page, a["href"], target))
                    continue
                if target == page:
                    continue
                kind = "chrome" if scope == "chrome" else classify(a)
                if (page, target, kind) in seen_pairs:
                    continue
                seen_pairs.add((page, target, kind))
                inbound[target][kind].append(page)
    return pages, inbound, unresolved


def sitemap_urls(root="."):
    path = os.path.join(root, "sitemap.xml")
    if not os.path.exists(path):
        return set()
    xml = open(path, encoding="utf-8").read()
    out = set()
    for loc in re.findall(r"<loc>(.*?)</loc>", xml, re.S):
        p = re.sub(r"^https?://[^/]+/", "", loc.strip())
        out.add("index.html" if p in ("", "/") else p)
    return out


def report(root="."):
    pages, inbound, unresolved = build(root)
    smap = sitemap_urls(root)
    orphans, under, footer_pages = [], [], []
    for p in pages:
        counted = {k: v for k, v in inbound[p].items() if k != "chrome"}
        total = sum(len(v) for v in counted.values())
        body = len(counted.get("body", []))
        if p in FOOTER_PAGES:
            footer_pages.append((p, total, body)); continue
        if p in NAV_EXCLUDED:
            continue
        if total == 0:
            orphans.append((p, inbound[p]))
        elif total < WANT_TOTAL or body < WANT_BODY:
            under.append((p, total, body, counted))

    print("=" * 66)
    print(f"UA LINK GRAPH — {len(pages)} pages, links counted from <main> only")
    print("=" * 66)

    if unresolved:
        print(f"\nUNRESOLVED LINKS ({len(unresolved)}) — hard rule 14, the target file is not in the repo")
        for src, href, target in unresolved:
            print(f"   {src} -> {href}   (resolves to {target})")

    print(f"\nORPHANS ({len(orphans)}) — zero inbound links from any page's <main>")
    for p, kinds in orphans:
        chrome = len(kinds.get("chrome", []))
        extra = f"  (reachable only from chrome on {chrome} pages)" if chrome else ""
        print(f"   {p}{extra}")
        if p in smap:
            print(f"      ! in sitemap.xml and orphaned: crawled with no signal of importance")

    print(f"\nUNDER-LINKED ({len(under)}) — protocol wants {WANT_TOTAL}+ inbound, {WANT_BODY}+ in body copy")
    for p, total, body, kinds in sorted(under, key=lambda x: (x[2], x[1])):
        detail = ", ".join(f"{k}:{len(v)}" for k, v in sorted(kinds.items()))
        print(f"   {p}   total {total}, body {body}   ({detail})")
        for k in ("body", "related", "card"):
            for src in kinds.get(k, []):
                print(f"      {k:<8} from {src}")

    if footer_pages:
        print(f"\nFOOTER PAGES ({len(footer_pages)}) — known-acceptable, linked from the footer by design")
        for p, total, body in footer_pages:
            print(f"   {p}   main-copy inbound: {total}")
    print(f"\nEXCLUDED: {', '.join(sorted(NAV_EXCLUDED))} — linked from the global nav on every page")

    missing = sorted(u for u in smap if u not in inbound)
    if missing:
        print(f"\nIN SITEMAP BUT NOT IN THE REPO ({len(missing)}) — hard rule 14")
        for u in missing:
            print(f"   {u}")

    print("\n" + "=" * 66)
    print(f"{len(pages)} pages | {len(orphans)} orphans | {len(under)} under-linked | "
          f"{len(unresolved)} unresolved")
    print("Cannot judge whether a link arrives at the right moment. See JOB 0j.")
    print("=" * 66)
    return len(orphans) + len(unresolved)


def selftest():
    cases = [
        ("/foo.html", "index.html", "foo.html"),
        ("foo.html", "insights/a.html", "insights/foo.html"),
        ("../foo.html", "insights/a.html", "foo.html"),
        ("/insights/foo.html", "index.html", "insights/foo.html"),
        ("/", "insights/a.html", "index.html"),
        ("/foo.html#section", "index.html", "foo.html"),
        ("mailto:x@y.z", "index.html", None),
        ("https://example.com/foo.html", "index.html", None),
        ("#main", "index.html", None),
        ("/og-image.png", "index.html", None),
    ]
    bad = 0
    for href, src, want in cases:
        got = resolve(href, src)
        if got != want:
            print(f"WRONG: resolve({href!r}, {src!r}) = {got!r}, expected {want!r}"); bad += 1
    print(f"resolve selftest: {len(cases)} cases, {bad} wrong")
    return bad


if __name__ == "__main__":
    if "--selftest" in sys.argv:
        sys.exit(1 if selftest() else 0)
    sys.exit(1 if report(sys.argv[1] if len(sys.argv) > 1 else ".") else 0)
