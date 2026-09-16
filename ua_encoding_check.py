#!/usr/bin/env python3
"""
ua_encoding_check.py — the same character written two ways.

Usage:  python3 ua_encoding_check.py <folder> [--term "H&M"] [--strict] [--selftest]

THE QUESTION THIS CHECK MUST ANSWER
-----------------------------------
Not "does this page contain HTML entities". That is the easier question and
every page would answer yes. The question is:

    Is a character written BOTH as a literal and as an entity, so that a
    single-form search finds some of the instances and reports success?

WHY IT EXISTS
-------------
Three instances in two days, 12 and 13 September 2026. `H&M` returned 0
against ten written `H&amp;M`. `roughly &euro;880,000` returned 4 against 5,
the fifth written with a literal euro sign. Both sit beside the original trap
in the register, where a literal-euro search was blind to an estate writing
`&euro;`.

The dangerous half is that the search succeeds. Four of five looks like
completion. This check does not care what anyone was searching for: it reports
where both forms exist, so a sweep knows it must cover both.

WHY IT REPORTS RATHER THAN FAILS
--------------------------------
It was first written to fail when one file used both forms of a character.
The first run returned 57 such instances across all 45 pages, most of them em
dashes sitting literal in a <title> and as an entity in body copy. "No page
mixes forms" is not an achievable end state here and it is not a desirable
one, so a gate set there would fail every run and be tuned away or ignored.

So the default is a report and exit 0. The split is the standing condition of
this estate, not a defect in any one file, and the useful output is the map of
which characters are split and where.

--term is the part that does the work. Give it a search string and it expands
it into both forms and counts each, so the discipline is applied at the moment
of the search rather than remembered before it. --strict restores the
per-file failure for anyone who wants to normalise a page.

WHAT IT DOES NOT DO
-------------------
It does not say which form is correct; that is a house-style decision.
It reads the raw file, because a raw grep is the thing being calibrated.
For the bare ampersand it ignores ampersands inside a tag that look like URL
query separators, which is the one place a raw `&` is ordinary.
"""
import re, sys, glob, os

PAIRS = [
    ("euro sign",        "€",   "&euro;"),
    ("pound sign",       "£",   "&pound;"),
    ("em dash",          "—",   "&mdash;"),
    ("en dash",          "–",   "&ndash;"),
    ("non-breaking sp",  " ",   "&nbsp;"),
    ("left dbl quote",   "“",   "&ldquo;"),
    ("right dbl quote",  "”",   "&rdquo;"),
    ("left sgl quote",   "‘",   "&lsquo;"),
    ("apostrophe",       "’",   "&rsquo;"),
    ("middot",           "·",   "&middot;"),
]
ENTITY = re.compile(r"&(?:[A-Za-z][A-Za-z0-9]{1,31}|#\d{1,7}|#[xX][0-9A-Fa-f]{1,6});")
URL_AMP = re.compile(r"<[^>]*?\w=[^>]*?>")

def bare_amp_count(raw):
    """Ampersands that are not entities and not URL query separators inside a tag."""
    masked = ENTITY.sub(lambda m: "\x00" * len(m.group(0)), raw)
    for m in URL_AMP.finditer(masked):
        s, e = m.span()
        masked = masked[:s] + masked[s:e].replace("&", "\x00") + masked[e:]
    return masked.count("&")

def scan_file(raw):
    out = {}
    for name, lit, ent in PAIRS:
        out[name] = (raw.count(lit), raw.count(ent))
    out["ampersand"] = (bare_amp_count(raw), raw.count("&amp;"))
    return out

def files(folders):
    seen = []
    for d in folders:
        seen += sorted(glob.glob(os.path.join(d, "*.html")))
        seen += sorted(glob.glob(os.path.join(d, "insights", "*.html")))
    return sorted(set(seen))

def expand(term):
    """Both forms of a search term: fully literal and fully entity."""
    lit = term
    for _, l, e in PAIRS + [("ampersand", "&", "&amp;")]:
        lit = lit.replace(e, l)
    # Build the entity form FROM the literal form, escaping bare ampersands
    # first. Building it from the raw term re-escapes the "&" of an entity the
    # caller already typed: "&euro;880,000" became "&amp;euro;880,000".
    # Caught by the term fixtures, 16 September 2026.
    ent = lit.replace("&", "&amp;")
    for _, l, e in PAIRS:
        ent = ent.replace(l, e)
    return lit, ent


def term_report(folders, term):
    lit, ent = expand(term)
    print("=" * 62)
    print(f"term as given : {term!r}")
    print(f"literal form  : {lit!r}")
    print(f"entity form   : {ent!r}")
    if lit == ent:
        print("no mappable characters; one form is the whole search")
    print("-" * 62)
    tl = te = 0
    for f in files(folders):
        raw = open(f, encoding="utf-8", errors="replace").read()
        a, b = raw.count(lit), (raw.count(ent) if ent != lit else 0)
        if a or b:
            print(f"   {f:56} literal {a:>3}  entity {b:>3}")
        tl += a; te += b
    print("=" * 62)
    print(f"TOTAL literal {tl} | entity {te} | combined {tl + te}")
    if tl and te:
        print("Both forms present. A search for either alone would have")
        print(f"reported {max(tl, te)} of {tl + te} and looked like completion.")
    return 0


def run(folders, strict=False):
    per, fails = {}, []
    fs = files(folders)
    for f in fs:
        counts = scan_file(open(f, encoding="utf-8", errors="replace").read())
        per[f] = counts
        for name, (lit, ent) in counts.items():
            if lit and ent:
                fails.append((f, name, lit, ent))
    print("=" * 62)
    print(f"{'character':18}{'literal':>10}{'entity':>10}  files lit / ent / both")
    warns = 0
    for name in list(dict.fromkeys([p[0] for p in PAIRS] + ["ampersand"])):
        L = sum(per[f][name][0] for f in fs)
        E = sum(per[f][name][1] for f in fs)
        fl = sum(1 for f in fs if per[f][name][0] and not per[f][name][1])
        fe = sum(1 for f in fs if per[f][name][1] and not per[f][name][0])
        fb = sum(1 for f in fs if per[f][name][0] and per[f][name][1])
        flag = ""
        if fl and fe:
            flag = "   <- estate split, search BOTH forms"; warns += 1
        print(f"{name:18}{L:>10}{E:>10}  {fl:>3} / {fe:>3} / {fb:>3}{flag}")
    if fails and strict:
        print("\nFAIL (--strict) — one file, both forms of the same character:")
        for f, name, lit, ent in fails:
            print(f"   {f}: {name} literal x{lit}, entity x{ent}")
    print("=" * 62)
    label = "failures" if strict else "files mixing a character (not a defect)"
    print(f"{len(fs)} pages | {len(fails)} {label} | {warns} split characters")
    print("A split character is not a defect in any one file. It is the reason")
    print("a single-form search is a floor rather than a total.")
    return len(fails) if strict else 0

TERM_CASES = [
    ("H&M", "H&M", "H&amp;M"),
    ("&euro;880,000", "\u20ac880,000", "&euro;880,000"),
    ("no mappable chars", "no mappable chars", "no mappable chars"),
]

FIXTURES = [
    ("<p>&euro;5 and €6</p>", "euro sign", (1, 1)),
    ("<p>H&amp;M</p>", "ampersand", (0, 1)),
    ('<a href="/x?a=1&b=2">H&amp;M</a>', "ampersand", (0, 1)),
    ("<p>Tom &amp; Jerry & Co</p>", "ampersand", (1, 1)),
    ("<p>&mdash;</p>", "em dash", (0, 1)),
    ("<p>—</p>", "em dash", (1, 0)),
]

def selftest():
    bad = 0
    for raw, key, want in FIXTURES:
        got = scan_file(raw)[key]
        if got != want:
            print(f"WRONG: {raw!r} {key} = {got}, expected {want}"); bad += 1
    for term, wl, we in TERM_CASES:
        gl, ge = expand(term)
        if (gl, ge) != (wl, we):
            print(f"WRONG: expand({term!r}) = {(gl, ge)!r}, expected {(wl, we)!r}"); bad += 1
    print(f"selftest: {len(FIXTURES)} count fixtures + {len(TERM_CASES)} term cases, {bad} wrong")
    return bad

if __name__ == "__main__":
    argv = sys.argv[1:]
    if "--selftest" in argv:
        sys.exit(1 if selftest() else 0)
    term = None
    if "--term" in argv:
        i = argv.index("--term")
        term = argv[i + 1] if i + 1 < len(argv) else ""
        argv = argv[:i] + argv[i + 2:]
    args = [a for a in argv if not a.startswith("--")]
    if term is not None:
        sys.exit(term_report(args or ["."], term))
    sys.exit(1 if run(args or ["."], strict="--strict" in sys.argv) else 0)
