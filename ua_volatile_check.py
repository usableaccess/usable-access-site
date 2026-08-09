#!/usr/bin/env python3
"""
ua_volatile_check.py — claims that go stale on a schedule.

Usage:  python3 ua_volatile_check.py <folder> [--today YYYY-MM-DD] [--selftest]

THE QUESTION THIS CHECK MUST ANSWER
-----------------------------------
Not "does this page mention a date". That is the easier question and it would
return every page on the site. The question is:

    Does this page state a period as still ahead, when the calendar has
    already passed it?

Written 8 August 2026, after `insights/bfsg-germany-enforcement-abmahnungen.html`
was found saying "formal enforcement decisions are expected in Q2 2026, which
means they could arrive any week now". Q2 2026 ended on 30 June. The sentence
was true when written and became false without anybody touching the file.

WHY THIS IS NOT A FACT TRAP
---------------------------
A FACT trap is a bookmark of wordings we have already been burned by, so its
count is a floor (see the register). This is different in kind. A quarter or a
year that has passed is MECHANICALLY detectable: the check computes the end of
the period and compares it to today. There is no phrasing list to widen and no
claim to verify against a source. It either has passed or it has not.

That also means the failure mode is different. A FACT trap goes stale when
someone invents a new wording. This check goes stale only if the date parsing
misses a format, so new formats are the thing to add.

WHAT IT CANNOT DO
-----------------
- It cannot tell whether a future claim is TRUE. "Sanctions expected in Q4 2026"
  parses fine and may still be unsupportable. That is JOB 0q's rule: never
  attribute a future timeline to a regulator at all.
- It cannot resolve "soon", "shortly", "in the coming months". No end date, so
  nothing to compare. Those are a writing problem, not a parsing one.
- It cannot know when an elapsed counter was last correct. It flags the counter
  and asks for a review date; it does not recompute the number.
- It reads the same surface as ua_page_check: visible text, meta descriptions,
  JSON-LD and accessible names. A stale date in structured data counts.
"""
import sys, os, re, glob, datetime

# --- period vocabulary ------------------------------------------------------
MONTHS = {m.lower(): i for i, m in enumerate(
    ["January", "February", "March", "April", "May", "June", "July", "August",
     "September", "October", "November", "December"], start=1)}
MONTH_RE = "|".join(MONTHS)
ORDINALS = {"first": 1, "second": 2, "third": 3, "fourth": 4}
WORD_NUM = {w: n for n, w in enumerate(
    ["zero", "one", "two", "three", "four", "five", "six", "seven", "eight",
     "nine", "ten", "eleven", "twelve", "thirteen", "fourteen", "fifteen",
     "sixteen", "seventeen", "eighteen", "nineteen", "twenty"])}

# Framing. A period only goes stale if the sentence presents it as still ahead.
# "Letters arrived in Q1 2026" is history and must never be flagged.
FUTURE = re.compile(r"(?i)\b(expected|expects?|expecting|will|due|upcoming|coming|"
                    r"anticipat\w+|forecast\w*|imminent|any week now|any day now|"
                    r"soon|shortly|set to|likely to|projected|planned|scheduled|"
                    r"moving toward|move toward|moves toward|ahead of|no later than)\b")
PAST = re.compile(r"(?i)\b(arrived|issued|took effect|came into force|began|begun|"
                  r"entered|launched|was|were|has been|have been|since|reported|"
                  r"published|found|ruled|ordered|concluded|already)\b")

def _eom(y, m):
    return datetime.date(y + (m == 12), 1 if m == 12 else m + 1, 1) - datetime.timedelta(days=1)

def _periods(sent):
    """Yield (label, end_date) for every period in the sentence with a real end."""
    for m in re.finditer(r"(?i)\bQ([1-4])\s*(20\d\d)\b", sent):
        q, y = int(m.group(1)), int(m.group(2))
        yield m.group(0), _eom(y, q * 3)
    for m in re.finditer(r"(?i)\b(first|second|third|fourth)\s+quarter\s+of\s+(20\d\d)\b", sent):
        yield m.group(0), _eom(int(m.group(2)), ORDINALS[m.group(1).lower()] * 3)
    for m in re.finditer(r"(?i)\bH([12])\s*(20\d\d)\b", sent):
        yield m.group(0), _eom(int(m.group(2)), int(m.group(1)) * 6)
    for m in re.finditer(r"(?i)\b(first|second)\s+half\s+of\s+(20\d\d)\b", sent):
        yield m.group(0), _eom(int(m.group(2)), ORDINALS[m.group(1).lower()] * 6)
    for m in re.finditer(rf"(?i)\b({MONTH_RE})\s+(20\d\d)\b", sent):
        yield m.group(0), _eom(int(m.group(2)), MONTHS[m.group(1).lower()])
    for m in re.finditer(r"(?i)\b(?:mid|early|late)[- ](20\d\d)\b", sent):
        yield m.group(0), datetime.date(int(m.group(1)), 12, 31)
    # A bare year, only when nothing more specific already covered it.
    for m in re.finditer(r"(?i)\b(?:in|during|throughout|by)\s+(20\d\d)\b", sent):
        yield m.group(0), datetime.date(int(m.group(1)), 12, 31)

# "as of <period>" is a freshness stamp. It does not go false, it goes old.
AS_OF = re.compile(rf"(?i)\bas of\s+((?:mid|early|late)[- ]20\d\d|(?:{MONTH_RE})\s+20\d\d|"
                   rf"Q[1-4]\s*20\d\d|20\d\d)")

# Elapsed counters: "thirteen months", "18 months since". The number is correct
# on the day it is written and wrong later. Watched, never recomputed here.
ELAPSED = re.compile(r"(?i)\b(" + "|".join(WORD_NUM) + r"|\d{1,3})[\s-]+(month|year)s?\b")
ELAPSED_CTX = re.compile(r"(?i)\b(since|so far|to date|have passed|has passed|into|"
                         r"of enforcement|after the deadline|now|already)\b")

STALE_GRACE_DAYS = 0     # a period that has ended is stale the next day
SOON_DAYS = 90           # ends within a quarter: set a review date now
AS_OF_DAYS = 120         # a freshness stamp older than this reads as neglected


def strip_tags(h):
    """Same surface as ua_page_check: visible text plus meta, JSON-LD, alt, aria."""
    jsonld = " ".join(re.findall(
        r'<script[^>]*application/ld\+json[^>]*>(.*?)</script>', h, re.S | re.I))
    metas = " ".join(m.group(2) for m in re.finditer(
        r'<meta[^>]*(?:name|property)="([^"]*(?:description|title)[^"]*)"[^>]*content="([^"]*)"',
        h, re.I))
    names = " ".join(re.findall(r'\b(?:alt|aria-label)="([^"]*)"', h, re.I))
    h = re.sub(r"<script.*?</script>", " ", h, flags=re.S | re.I)
    h = re.sub(r"<style.*?</style>", " ", h, flags=re.S | re.I)
    visible = re.sub(r"<[^>]+>", " ", h)
    return " ".join(" ".join([visible, metas, jsonld, names]).split())


def sentences(text):
    return [s for s in re.split(r"(?<=[.!?])\s+", text) if s.strip()]


def check_text(text, today):
    """Return (fails, warns) as lists of (kind, sentence, detail)."""
    fails, warns = [], []
    for sent in sentences(text):
        forward = FUTURE.search(sent)
        backward = PAST.search(sent)
        seen = set()
        for label, end in _periods(sent):
            key = label.lower()
            if key in seen:
                continue
            seen.add(key)
            days = (today - end).days
            if forward and not backward and days > STALE_GRACE_DAYS:
                fails.append(("STALE", sent, f'"{label}" ended {end.isoformat()}, '
                                             f'{days} days ago, but is stated as still ahead'))
            elif forward and not backward and -SOON_DAYS <= days <= STALE_GRACE_DAYS:
                warns.append(("EXPIRING", sent, f'"{label}" ends {end.isoformat()}, '
                                                f'in {-days} days - set a review date'))
        m = AS_OF.search(sent)
        if m:
            for label, end in _periods(m.group(1)):
                if (today - end).days > AS_OF_DAYS:
                    warns.append(("AS-OF", sent, f'freshness stamp "{m.group(0)}" is '
                                                 f'{(today - end).days} days old'))
                break
        if ELAPSED_CTX.search(sent):
            for m in ELAPSED.finditer(sent):
                warns.append(("COUNTER", sent, f'"{m.group(0)}" is an elapsed count and '
                                               f'changes with the calendar - needs a review date'))
                break
    return fails, warns


def run(folder, today):
    files = sorted(glob.glob(os.path.join(folder, "*.html")))
    nf = nw = 0
    print(f"  volatile check, today = {today.isoformat()}")
    for path in files:
        with open(path, encoding="utf-8") as fh:
            fails, warns = check_text(strip_tags(fh.read()), today)
        if not fails and not warns:
            continue
        print(f"\n{os.path.basename(path)}   [{'FAIL' if fails else 'warn'}]")
        for kind, sent, detail in fails:
            print(f"   FAIL  {kind}: {detail}")
            print(f"         {sent[:170]}")
            nf += 1
        for kind, sent, detail in warns:
            print(f"   warn  {kind}: {detail}")
            nw += 1
    print("\n" + "=" * 62)
    print(f"{len(files)} pages | {nf} failures | {nw} warnings")
    print("Scope: parses periods with a computable end. It cannot judge whether a")
    print("future claim is TRUE, cannot resolve \"soon\" or \"in the coming months\",")
    print("and does not recompute elapsed counters. See the docstring.")
    print("=" * 62)
    return nf


FIXTURES = [
    # (text, today, expect_fail, why)
    ("Formal enforcement decisions are expected in Q2 2026, which means they could arrive any week now.",
     "2026-08-08", True, "the real one: passed quarter stated as imminent"),
    ("Penalty decisions are expected in the second half of 2026.",
     "2026-08-08", False, "H2 2026 has not ended, so it is a live prediction"),
    ("Penalty decisions are expected in the second half of 2025.",
     "2026-08-08", True, "H2 2025 ended, still framed as expected"),
    ("The first Abmahnungen arrived in Q1 2026.",
     "2026-08-08", False, "history, never flag"),
    ("The market surveillance authority entered its active enforcement phase in January 2026.",
     "2026-08-08", False, "past framing, a source question not a staleness one"),
    ("Sweden's first penalty decisions are expected throughout 2026.",
     "2027-01-04", True, "a bare year goes stale too"),
    ("The BFSG came into force on 28 June 2025.",
     "2026-08-08", False, "a fixed historical date is not volatile"),
    ("Enforcement has been running for thirteen months since the deadline.",
     "2026-08-08", False, "warns as a COUNTER, does not fail"),
]


def selftest():
    bad = 0
    for text, day, expect_fail, why in FIXTURES:
        today = datetime.date.fromisoformat(day)
        fails, warns = check_text(text, today)
        got = bool(fails)
        if got != expect_fail:
            print(f"WRONG ({why}): expected fail={expect_fail}, got {got}")
            print(f"   {text}")
            for k, s, d in fails + warns:
                print(f"   -> {k}: {d}")
            bad += 1
    counter = check_text("Enforcement has been running for thirteen months since the deadline.",
                         datetime.date(2026, 8, 8))[1]
    if not any(k == "COUNTER" for k, _, _ in counter):
        print("WRONG: elapsed counter not warned"); bad += 1
    print(f"selftest: {len(FIXTURES)} fixtures, {bad} wrong")
    return bad


if __name__ == "__main__":
    args = sys.argv[1:]
    today = datetime.date.today()
    if "--today" in args:
        i = args.index("--today")
        today = datetime.date.fromisoformat(args[i + 1])
        del args[i:i + 2]
    if "--selftest" in args:
        sys.exit(1 if selftest() else 0)
    sys.exit(1 if run(args[0] if args else ".", today) else 0)
