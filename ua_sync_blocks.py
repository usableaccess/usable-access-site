#!/usr/bin/env python3
"""
UA shared-block sync - OG/Twitter block ONLY.

Usage:
    python3 ua_sync_blocks.py <folder>            # dry run, reports and changes nothing
    python3 ua_sync_blocks.py <folder> --write    # apply

SCOPE. This manages the Open Graph and Twitter card block and nothing else.
CLAUDE.md's tooling table describes a wider tool that also owns the footer legal
links and the nav CTA markup and CSS. That tool did not exist when this was
written on 8 August 2026. Do not assume the other blocks are managed here.

The block is defined ONCE in OG_TEMPLATE below. Editing it and re-running with
--write updates every managed page, which is the point: the alternative is 44
hand edits and a slow drift between them.

Inputs come from the page itself: its canonical URL, <title> and meta
description. Nothing is invented.

TWO REFUSALS, both deliberate:

  1. Redirect stubs are skipped. A page carrying <meta http-equiv="refresh">
     is not a destination, and giving it a full social block tells crawlers to
     treat it as one.

  2. A meta description longer than 155 characters is NOT propagated. The page
     is flagged and skipped. Copying it into og:description and
     twitter:description would spread one failing value into three places and
     make the original harder to find. Fix the description, then re-run.
"""
import sys, os, re, glob

SITE = "https://usableaccess.io"
OG_IMAGE = f"{SITE}/og-image.png"
OG_IMAGE_ALT = ("Usable Access &mdash; clarity-first EAA compliance. "
                "Building accessibility that works.")
MAX_DESC = 155

START = "<!-- ua:og:start -->"
END = "<!-- ua:og:end -->"

OG_TEMPLATE = """{start}
  <meta property="og:type" content="{og_type}">
  <meta property="og:title" content="{title}">
  <meta property="og:description" content="{desc}">
  <meta property="og:url" content="{url}">
  <meta property="og:image" content="{image}">
  <meta property="og:image:width" content="1200">
  <meta property="og:image:height" content="630">
  <meta property="og:image:alt" content="{image_alt}">
  <meta property="og:site_name" content="Usable Access">
  <meta name="twitter:card" content="summary_large_image">
  <meta name="twitter:title" content="{title}">
  <meta name="twitter:description" content="{desc}">
  <meta name="twitter:image" content="{image}">
  {end}"""


def attr_escape(t):
    """Make a string safe inside an HTML attribute without double-escaping.

    A bare & is invalid in an attribute value, but an existing entity such as
    &mdash; must be left alone. Escaping blindly produced &amp;mdash; on four
    pages, so the social card rendered a literal "&mdash;" instead of a dash.
    Not escaping at all turned a correct &amp; into a bare & on another. This
    escapes only ampersands that do not already start an entity.
    """
    t = re.sub(r"&(?!(?:[A-Za-z][A-Za-z0-9]{1,31}|#\d{1,7}|#x[0-9A-Fa-f]{1,6});)", "&amp;", t)
    return t.replace('"', "&quot;")


def build_block(title, desc, url, og_type):
    return OG_TEMPLATE.format(start=START, end=END, og_type=og_type,
                              title=attr_escape(title), desc=attr_escape(desc),
                              url=url, image=OG_IMAGE, image_alt=OG_IMAGE_ALT)


def page_facts(h):
    """Return (title, description, canonical) or None for whichever is absent."""
    t = re.search(r"<title>(.*?)</title>", h, re.S | re.I)
    d = re.search(r'name="description"\s+content="([^"]*)"', h, re.I)
    c = re.search(r'rel="canonical"\s+href="([^"]+)"', h, re.I)
    return (" ".join(t.group(1).split()) if t else None,
            d.group(1) if d else None,
            c.group(1) if c else None)


def sync(path):
    """Return (status, detail, new_html_or_None)."""
    h = open(path, encoding="utf-8").read()

    if re.search(r'http-equiv="refresh"', h, re.I):
        return "skip", "redirect stub - a redirect is not a social destination", None

    title, desc, url = page_facts(h)
    missing = [n for n, v in (("title", title), ("description", desc),
                              ("canonical", url)) if not v]
    if missing:
        return "skip", "missing " + ", ".join(missing), None

    if len(desc) > MAX_DESC:
        return "flag", (f"description is {len(desc)} chars (limit {MAX_DESC}) - NOT "
                        f"propagated; fix the description, then re-run"), None

    og_type = "website" if os.path.basename(path) == "index.html" else "article"
    block = build_block(title, desc, url, og_type)

    existing = re.search(re.escape(START) + r".*?" + re.escape(END), h, re.S)
    if existing:
        if existing.group(0) == block:
            return "ok", "already current", None
        return "update", "managed block refreshed", h[:existing.start()] + block + h[existing.end():]

    anchor = re.search(r'([ \t]*)<link rel="canonical"[^>]*>\n', h, re.I)
    if not anchor:
        return "skip", "no canonical <link> to anchor the block to", None
    ins = anchor.end()
    return "insert", "block added", h[:ins] + block + "\n" + h[ins:]


def main():
    folder = sys.argv[1] if len(sys.argv) > 1 else "."
    write = "--write" in sys.argv
    files = sorted(glob.glob(os.path.join(folder, "*.html")))
    if not files:
        print(f"no .html files in {folder!r}")
        return 1

    counts = {}
    print(f"  OG/Twitter block sync {'(WRITING)' if write else '(dry run)'} - {len(files)} files\n")
    for f in files:
        status, detail, new = sync(f)
        counts[status] = counts.get(status, 0) + 1
        if status == "ok":
            continue
        print(f"  {status.upper():<7} {os.path.basename(f):<52} {detail}")
        if new is not None and write:
            open(f, "w", encoding="utf-8").write(new)

    print("\n  " + "  ".join(f"{k}={v}" for k, v in sorted(counts.items())))
    if not write and (counts.get("insert") or counts.get("update")):
        print("  re-run with --write to apply")
    if counts.get("flag"):
        print("  FLAGGED pages were skipped on purpose - the failure is theirs to fix")
    return 0


if __name__ == "__main__":
    sys.exit(main())
