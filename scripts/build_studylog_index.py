#!/usr/bin/env python3
"""
build_studylog_index.py - regenerate the section index in a study log.

WHAT IT IS FOR
--------------
UA_StudyLog_Notes_CrossCutting_5.md carries an index whose header claimed
"174 numbered sections" beside a table holding 181 rows and 167 distinct
numbers, over a body holding 152. Four figures, none agreeing, because the
header was typed and the table was pasted and nothing recomputed either.

THE ONE RULE THIS SCRIPT EXISTS TO ENFORCE
------------------------------------------
Every number in the generated header is counted from the table generated in
the same run, one function call earlier. There is no constant, no argument
that can set a count, and nothing carried over from a previous run. If the
table has three rows the header says three, whatever the file said before.

WHAT IT DELIBERATELY DOES NOT DO
--------------------------------
It does not resolve collisions. Where two sections carry the same number both
get a row and both are named under COLLISIONS, because a lookup that silently
returns the first of two is worse than one that shows two.

It does not treat a suffixed identifier as a duplicate. Sections 16.2, 16.2a
and 16.20 are three sections. Prefix matching is what produced the wrong
duplicate count in the index this replaces, and --selftest fails against any
parser that reintroduces it.

It does not renumber, reorder or edit the notes. It only rewrites the block
between the two ua:studylog-index markers.

Stdlib only. Dry run by default; --write applies.
"""

import argparse
import datetime
import re
import sys

SCRIPT_PATH = "scripts/build_studylog_index.py"
START = "<!-- ua:studylog-index:start -->"
END = "<!-- ua:studylog-index:end -->"

# The index covers ## and ### headings. Anything else carrying a section
# number is reported rather than dropped, per the no-silent-caps rule.
INDEX_LEVELS = (2, 3)

HEADING_RE = re.compile(r"^(?P<hashes>#{1,6})\s+(?P<text>.*?)\s*#*\s*$")
LOOSE_HASH_RE = re.compile(r"^#{1,6}\S")
SECTION_RE = re.compile(r"§\s*(\d+(?:\.\d+)*[A-Za-z]*)")
FENCE_RE = re.compile(r"^\s*(```|~~~)")
TITLE_STRIP = " \t—–-:.·"


# ---------------------------------------------------------------- parsing

def blank_fenced_code(lines):
    """Blank out fenced code blocks, preserving line numbers.

    A '## §999' inside a python block is a code sample, not a section.
    """
    out, fence = [], None
    for line in lines:
        m = FENCE_RE.match(line)
        if fence is None:
            if m:
                fence = m.group(1)
                out.append("")
            else:
                out.append(line)
        else:
            if m and m.group(1)[0] == fence[0]:
                fence = None
            out.append("")
    return out


def natural_key(ident):
    """Sort key so 16.2 < 16.2a < 16.20 < 17.

    Dotted parts compare numerically, the alpha suffix breaks the tie, and a
    shorter identifier sorts before a longer one sharing its prefix.
    """
    parts = []
    for chunk in ident.split("."):
        m = re.match(r"(\d+)([A-Za-z]*)$", chunk)
        if m:
            parts.append((int(m.group(1)), m.group(2).lower()))
        else:
            parts.append((0, chunk.lower()))
    return parts


def parse(lines):
    """Return every §-carrying heading, plus everything deliberately excluded."""
    scanned = blank_fenced_code(lines)
    rows = []
    off_level = []       # § headings at levels other than ## and ###
    plain_headings = 0   # ## / ### headings carrying no §
    malformed = []       # '##§5' - hashes with no space, not an ATX heading

    for lineno, raw in enumerate(scanned, start=1):
        h = HEADING_RE.match(raw)
        if not h:
            if LOOSE_HASH_RE.match(raw) and SECTION_RE.search(raw):
                malformed.append((lineno, raw.strip()))
            continue

        level = len(h.group("hashes"))
        text = h.group("text")
        ids = SECTION_RE.findall(text)

        if not ids:
            if level in INDEX_LEVELS:
                plain_headings += 1
            continue

        if level not in INDEX_LEVELS:
            off_level.append({"line": lineno, "level": level, "text": text})
            continue

        # The FIRST § in a heading is that heading's identifier. Any further
        # § is a reference to another section - "§46.4a CORRECTION TO §46.4"
        # names two sections and is one section. Later ones never get a row.
        title = SECTION_RE.sub("", text, count=1).lstrip(TITLE_STRIP).strip()
        rows.append({
            "num": ids[0],
            "title": title or "(untitled)",
            "line": lineno,
            "level": level,
            "xrefs": ids[1:],
        })

    rows.sort(key=lambda r: (natural_key(r["num"]), r["line"]))
    return {
        "rows": rows,
        "off_level": off_level,
        "plain_headings": plain_headings,
        "malformed": malformed,
    }


def collisions_of(rows):
    """Section numbers used by more than one heading, compared whole.

    Whole-string comparison is the point. '16.2a'.startswith('16.2') is true
    and means nothing.
    """
    seen = {}
    for r in rows:
        seen.setdefault(r["num"], []).append(r)
    return {n: rs for n, rs in seen.items() if len(rs) > 1}


# ---------------------------------------------------------------- rendering

def esc(text):
    return text.replace("|", "\\|")


def build_block(parsed, notes_lines, today, source_name, governs=None):
    """Build the index block. Every count here is derived from parsed['rows'].

    Nothing is passed in as a total and nothing is read back from the file.
    """
    rows = parsed["rows"]
    coll = collisions_of(rows)

    n_rows = len(rows)
    n_distinct = len({r["num"] for r in rows})
    extra = n_rows - n_distinct

    out = []
    out.append("## INDEX")
    out.append("")
    out.append("Generated by `%s` in the usable-access-site repo." % SCRIPT_PATH)
    out.append("Do not hand-edit anything between the two `ua:studylog-index` markers.")
    out.append("To rebuild, from the directory holding this file:")
    out.append("")
    out.append("    python3 %s %s --write" % (SCRIPT_PATH, source_name))
    out.append("")
    out.append("Every figure on the next line is counted from the table below it in the")
    out.append("same run. None of them is a stored constant.")
    out.append("")
    out.append("**%d index rows · %d distinct section numbers · %d lines of notes "
               "outside this block · rebuilt %s**" % (n_rows, n_distinct, notes_lines, today))
    out.append("")

    if extra == 0:
        out.append("Rows and distinct numbers agree, so no section number is used twice.")
    else:
        out.append(
            "The two counts differ by %d because %d section number%s used by more than "
            "one heading. Every one of those keeps a row for each heading, listed under "
            "COLLISIONS below. Suffixed identifiers such as §16.2a are separate "
            "sections rather than collisions, and are counted as distinct."
            % (extra, len(coll), " is" if len(coll) == 1 else "s are")
        )
    out.append("")
    if governs is not None:
        cited = sum(1 for r in rows if r["num"] in governs["column"])
        out.append("**GOVERNS** counts the worksheet rows a section governs, from `%s`, "
                   "sheet `%s`, %d data rows."
                   % (governs["source"].split("/")[-1], governs["sheet"], governs["data_rows"]))
        out.append("")
        out.append("- **Distinct rows, never occurrences.** A row naming a section three "
                   "times is one row. Across the table that is %d row citations from %d "
                   "occurrences." % (governs["row_citations"], governs["occurrences"]))
        out.append("- **Cohort is the row's code prefix**, taken as the whole leading "
                   "alphabetic run: %s. SE, SES and SET are three cohorts."
                   % ", ".join(governs["cohorts"]))
        out.append("- **Ties sort alphabetically ascending**, so a section with several "
                   "single-citation cohorts renders the same way on every run. Insertion "
                   "order would churn them and a sort artefact would read as a change.")
        out.append("- **A dash means no worksheet row cites the section.** That is a fact "
                   "about attachment, not about the section's value, and it is only ever "
                   "written from worksheet data. %d of %d sections carry one."
                   % (len(rows) - cited, len(rows)))
        out.append("")

    if governs is None:
        out.append("| § | Section | Line | |")
        out.append("|---|---|---|---|")
    else:
        out.append("| § | Section | Line | %s | |" % GOVERNS_HEADER)
        out.append("|---|---|---|---|---|")

    for r in rows:
        note = ""
        if r["num"] in coll:
            group = coll[r["num"]]
            note = "⚠ %d of %d" % (group.index(r) + 1, len(group))
        if governs is None:
            out.append("| §%s | %s | %d | %s |"
                       % (r["num"], esc(r["title"]), r["line"], note))
        else:
            out.append("| §%s | %s | %d | %s | %s |"
                       % (r["num"], esc(r["title"]), r["line"],
                          governs["column"].get(r["num"], GOVERNS_DASH), note))

    out.append("")

    if coll:
        out.append("### COLLISIONS — %d section number%s used more than once"
                   % (len(coll), "" if len(coll) == 1 else "s"))
        out.append("")
        out.append("Both rows are kept above. Nothing is resolved in favour of whichever")
        out.append("came first, because a lookup returning one of two and never naming the")
        out.append("other is how a section goes missing.")
        out.append("")
        for num in sorted(coll, key=natural_key):
            lines_ = ", ".join(str(r["line"]) for r in coll[num])
            out.append("- §%s at lines %s" % (num, lines_))
        out.append("")

    xref_rows = [r for r in rows if r["xrefs"]]
    if xref_rows:
        out.append("### CROSS-REFERENCES IN HEADINGS")
        out.append("")
        out.append("These headings name a section other than their own. The first § in a")
        out.append("heading is its identifier; the rest are listed here and never given a")
        out.append("row. Read them if a section seems to be missing from the table.")
        out.append("")
        for r in xref_rows:
            out.append("- §%s (line %d) also names %s"
                       % (r["num"], r["line"], ", ".join("§" + x for x in r["xrefs"])))
        out.append("")

    if parsed["off_level"]:
        out.append("### § HEADINGS OUTSIDE ## AND ### — NOT INDEXED")
        out.append("")
        out.append("Listed rather than dropped, so the table's coverage is visible.")
        out.append("")
        for o in parsed["off_level"]:
            out.append("- line %d, level %d: %s" % (o["line"], o["level"], esc(o["text"])))
        out.append("")

    if parsed["malformed"]:
        out.append("### HASH-PREFIXED LINES CARRYING § THAT ARE NOT HEADINGS")
        out.append("")
        out.append("No space after the hashes, so markdown does not read these as headings")
        out.append("and neither does this script. Fix the spacing if one is meant to be a")
        out.append("section.")
        out.append("")
        for lineno, text in parsed["malformed"]:
            out.append("- line %d: %s" % (lineno, esc(text)))
        out.append("")

    while out and out[-1] == "":
        out.pop()
    return out


# ---------------------------------------------------------------- splicing

def marker_positions(lines):
    starts = [i for i, l in enumerate(lines) if l.strip() == START]
    ends = [i for i, l in enumerate(lines) if l.strip() == END]
    if len(starts) != 1 or len(ends) != 1:
        return None, "expected exactly one %s and one %s, found %d and %d" % (
            START, END, len(starts), len(ends))
    if ends[0] < starts[0]:
        return None, "the end marker appears before the start marker"
    return (starts[0], ends[0]), None


def notes_line_count(lines, span):
    """Lines of notes outside the managed block.

    Deliberately not the total file length. The block's own size changes when
    the index changes, so a total would be stale the moment it is written -
    which is the class of defect this script exists to remove.
    """
    if span is None:
        return len(lines)
    return len(lines) - (span[1] - span[0] + 1)



def regenerate(lines, today, source_name, governs=None, max_passes=8):
    """Rebuild until the line numbers reported are the ones the file will have.

    Rewriting the block moves every line beneath it, so a block built in one
    pass describes the file as it stood BEFORE that pass. The first version of
    this script recorded §16.2 at line 16 and then wrote it to line 63, which
    is the same defect it was written to remove: a number describing a prior
    state of the file, presented as current.

    The block's length depends on how many rows there are and not on the
    digits printed in them, so this settles on the second pass. The loop
    guards that assumption rather than trusting it.
    """
    cur = list(lines)
    parsed = block = None
    for n in range(1, max_passes + 1):
        span, err = marker_positions(cur)
        if span is None:
            return None, parse(cur), None, err, n
        parsed = parse(cur)
        block = build_block(parsed, notes_line_count(cur, span), today, source_name, governs)
        new = cur[:span[0] + 1] + block + cur[span[1]:]
        if new == cur:
            return cur, parsed, block, None, n
        cur = new
    return None, parsed, block, "line numbers did not settle in %d passes" % max_passes, max_passes


def verify_line_numbers(final_lines):
    """Read the rendered table back and confirm each row points at its heading.

    Deliberately parses the written markdown rather than reusing the structures
    that produced it. A check fed by the thing it is checking agrees with
    itself by construction and confirms nothing.
    """
    bad = []
    for line in final_lines:
        cells = split_md_row(line)
        if not cells or len(cells) < 3 or not cells[0].startswith("§"):
            continue
        if not cells[2].isdigit():
            continue
        num, lineno = cells[0][1:].strip(), int(cells[2])
        if not 1 <= lineno <= len(final_lines):
            bad.append((num, lineno, "line number out of range"))
            continue
        h = HEADING_RE.match(final_lines[lineno - 1])
        ids = SECTION_RE.findall(h.group("text")) if h else []
        if not ids or ids[0] != num:
            bad.append((num, lineno, final_lines[lineno - 1].strip()[:60] or "(blank line)"))
    return bad


# ---------------------------------------------------------------- governs

# A dash asserts that no worksheet row cites the section. That is a fact about
# attachment, and it can only be stated from data. Where no worksheet is
# supplied the column is omitted entirely rather than filled with dashes,
# because a dash invented from missing data is a fabricated fact.
GOVERNS_DASH = "—"
GOVERNS_HEADER = "Governs"

XL_NS = "{http://schemas.openxmlformats.org/spreadsheetml/2006/main}"
XL_REL = "{http://schemas.openxmlformats.org/officeDocument/2006/relationships}"


def read_xlsx(path, sheet_name=None):
    """Read an xlsx with the standard library. Yields (sheet, rownum, {col: text}).

    openpyxl is not a dependency of anything else in this repo and an xlsx is a
    zip of XML, so it is read directly.
    """
    import zipfile
    import xml.etree.ElementTree as ET

    z = zipfile.ZipFile(path)
    rels = {r.get("Id"): r.get("Target")
            for r in ET.fromstring(z.read("xl/_rels/workbook.xml.rels"))}
    shared = []
    if "xl/sharedStrings.xml" in z.namelist():
        for si in ET.fromstring(z.read("xl/sharedStrings.xml")).iter(XL_NS + "si"):
            shared.append("".join(t.text or "" for t in si.iter(XL_NS + "t")))

    wb = ET.fromstring(z.read("xl/workbook.xml"))
    for sh in wb.iter(XL_NS + "sheet"):
        name = sh.get("name")
        if sheet_name and name != sheet_name:
            continue
        part = "xl/" + rels[sh.get(XL_REL + "id")].lstrip("/").replace("xl/", "", 1)
        if part not in z.namelist():
            part = "xl/" + rels[sh.get(XL_REL + "id")].lstrip("/")
        root = ET.fromstring(z.read(part))
        for row in root.iter(XL_NS + "row"):
            vals = {}
            for c in row.iter(XL_NS + "c"):
                ref = c.get("r") or ""
                col = "".join(ch for ch in ref if ch.isalpha())
                kind = c.get("t")
                if kind == "inlineStr":
                    v = "".join(t.text or "" for t in c.iter(XL_NS + "t"))
                elif kind == "s":
                    el = c.find(XL_NS + "v")
                    v = shared[int(el.text)] if el is not None and el.text else ""
                else:
                    el = c.find(XL_NS + "v")
                    v = el.text if el is not None else ""
                vals[col] = v or ""
            yield name, int(row.get("r")), vals


def cohort_of(code):
    """The row's cohort is the whole leading alphabetic run of its code.

    SE, SES and SET are three cohorts and all three are in the worksheet, with
    SE and SET both at 14 on the largest section. Prefix matching would merge
    them into one bogus SE, which is the same defect as folding §16.2a into
    §16.2 - a partial match treated as identity.
    """
    m = re.match(r"^\s*([A-Za-z]+)", code or "")
    return m.group(1).upper() if m else "?"


def render_governs(total, cohorts):
    """Total distinct rows, then cohort tallies.

    Ties sort alphabetically ascending. Counter.most_common leaves equal counts
    in insertion order, which is arbitrary, so every single-citation cohort
    would reshuffle between runs and a sort artefact would read as a real
    change in the diff.
    """
    if total == 0:
        return GOVERNS_DASH
    pairs = " ".join("%s×%d" % (c, n)
                     for c, n in sorted(cohorts.items(), key=lambda kv: (-kv[1], kv[0])))
    return "%d %s" % (total, pairs)


def compute_governs(path, sheet_name=None, code_col=None, header_row=None):
    """Tally which worksheet rows cite which section.

    Counts DISTINCT ROWS, never occurrences. A row naming §30 three times is
    one row. Verified against UA_Cowork_Worksheet_Vetting_19.xlsx on
    19 August 2026: §30 gives 67 distinct rows from 99 occurrences, matching
    the figure Cowork established.
    """
    rows = list(read_xlsx(path, sheet_name))
    if not rows:
        raise ValueError("no rows read from %s" % path)

    found_sheet, found_col, found_row = sheet_name, code_col, header_row
    if not (found_col and found_row and found_sheet):
        for sname, rnum, vals in rows:
            if found_sheet and sname != found_sheet:
                continue
            for col, v in sorted(vals.items()):
                if (v or "").strip().lower() == "code":
                    found_sheet, found_col, found_row = sname, col, rnum
                    break
            if found_col:
                break
    if not found_col:
        raise ValueError("no 'Code' header cell found; pass --code-column and --header-row")

    occurrences = 0
    distinct = {}
    cohorts = {}
    seen_cohorts = set()
    data_rows = 0

    for sname, rnum, vals in rows:
        if sname != found_sheet or rnum <= found_row:
            continue
        code = (vals.get(found_col) or "").strip()
        if not code:
            continue
        data_rows += 1
        blob = "\n".join(vals.values())
        hits = SECTION_RE.findall(blob)
        occurrences += len(hits)
        pre = cohort_of(code)
        seen_cohorts.add(pre)
        for num in set(hits):          # set() is the distinct-rows rule
            distinct[num] = distinct.get(num, 0) + 1
            cohorts.setdefault(num, {})
            cohorts[num][pre] = cohorts[num].get(pre, 0) + 1

    return {
        "column": {n: render_governs(distinct[n], cohorts[n]) for n in distinct},
        "distinct": distinct,
        "occurrences": occurrences,
        "row_citations": sum(distinct.values()),
        "cohorts": sorted(seen_cohorts),
        "data_rows": data_rows,
        "source": path,
        "sheet": found_sheet,
        "code_col": found_col,
        "header_row": found_row,
    }


def split_md_row(line):
    """Split a markdown table row into cells, honouring escaped pipes.

    Used instead of hunting for a digit-bearing cell with a regex: the GOVERNS
    column starts with a number too, so a positional read is the only safe one.
    """
    if not line.startswith("|"):
        return None
    parts = re.split(r"(?<!\\)\|", line)
    return [c.strip() for c in parts[1:-1]]


def existing_governs(lines):
    """Read the GOVERNS column out of the index already in the file.

    This is the control against Cowork's column: recomputing and comparing says
    whether this script reproduces a value that was established elsewhere,
    which is the only check here that does not route through its own author.
    """
    header_idx = None
    for cells in (split_md_row(l) for l in lines):
        if cells and cells[0] == "§" and any(
                c.strip().lower() == GOVERNS_HEADER.lower() for c in cells):
            header_idx = [c.strip().lower() for c in cells].index(GOVERNS_HEADER.lower())
            break
    if header_idx is None:
        return None
    out = {}
    for line in lines:
        cells = split_md_row(line)
        if not cells or len(cells) <= max(header_idx, 2):
            continue
        # The header row also begins with "§", so identity is not enough. A data
        # row is one whose line cell is a number.
        if not cells[0].startswith("§") or cells[0] == "§" or not cells[2].isdigit():
            continue
        out.setdefault(cells[0][1:].strip(), cells[header_idx].strip())
    return out


# ---------------------------------------------------------------- selftest

FIX_SUFFIXED = """# STUDY LOG

## §16.2 - THE ORIGINAL
Body.

## §16.2a - CORRECTION TO §16.2, SAME EVENING
Body.

## §16.20 - MUCH LATER
Body.
"""

FIX_REPEAT = """# STUDY LOG

## §83 - THE FIRST ONE
Body.

### §83 - THE SECOND ONE, WRITTEN LATER
Body.
"""

FIX_XREF = """# STUDY LOG

## §46.4a - CORRECTION TO §46.4, SAME EVENING
Body.
"""

FIX_STALE_HEADER = """# STUDY LOG

<!-- ua:studylog-index:start -->
## INDEX

**174 numbered sections · 3816 lines · rebuilt 2026-08-16**

| § | Section | Line |
|---|---|---|
| §1 | STALE | 999 |
<!-- ua:studylog-index:end -->

## §1 - ONE
## §2 - TWO
## §3 - THREE
"""

FIX_NOISE = """# STUDY LOG

Prose referring to §12 and §13 in passing.

```
## §999 - INSIDE A CODE FENCE
```

## §7 - REAL
"""

FIX_LEVELS = """# §1 - LEVEL ONE
#### §2.1 - LEVEL FOUR
## §3 - REAL
"""

FIX_PLAIN = """## A PLAIN HEADING WITH NO SECTION NUMBER
## §5 - NUMBERED
"""

FIX_MALFORMED = """##§6 - NO SPACE AFTER THE HASHES
## §7 - FINE
"""


FIX_LINESHIFT = """# STUDY LOG

<!-- ua:studylog-index:start -->
a one-line index that the rebuild will replace with about thirty
<!-- ua:studylog-index:end -->

## §1 - ONE
## §2 - TWO
## §3 - THREE
"""


def selftest():
    failures = []

    def check(name, cond, detail=""):
        if cond:
            print("  ok    %s" % name)
        else:
            print("  FAIL  %s%s" % (name, (" - " + detail) if detail else ""))
            failures.append(name)

    def parsed_of(text):
        return parse(text.splitlines())

    print("FIXTURE 1: suffixed identifiers are distinct sections")
    print("  fails against: a parser comparing numbers by prefix")
    p = parsed_of(FIX_SUFFIXED)
    nums = [r["num"] for r in p["rows"]]
    check("three rows", len(p["rows"]) == 3, str(nums))
    check("three distinct numbers, not one", len(set(nums)) == 3, str(nums))
    check("no collision reported", collisions_of(p["rows"]) == {},
          str(list(collisions_of(p["rows"]))))
    check("sorted 16.2 < 16.2a < 16.20", nums == ["16.2", "16.2a", "16.20"], str(nums))
    check("16.2a keeps its own title",
          p["rows"][1]["title"] == "CORRECTION TO §16.2, SAME EVENING",
          p["rows"][1]["title"])

    print("FIXTURE 2: a genuine repeat gets two rows AND a flag")
    print("  fails against: a parser resolving collisions to whichever it saw first")
    p = parsed_of(FIX_REPEAT)
    coll = collisions_of(p["rows"])
    check("two rows", len(p["rows"]) == 2, str(len(p["rows"])))
    check("one distinct number", len({r["num"] for r in p["rows"]}) == 1)
    check("83 flagged as a collision", "83" in coll)
    check("both line numbers recorded",
          "83" in coll and [r["line"] for r in coll["83"]] == [3, 6],
          str([r["line"] for r in coll.get("83", [])]))
    block = "\n".join(build_block(p, 10, "2026-08-19", "STUDY.md"))
    check("both titles reach the rendered table",
          "THE FIRST ONE" in block and "THE SECOND ONE, WRITTEN LATER" in block)
    check("rendered rows are marked 1 of 2 and 2 of 2",
          "⚠ 1 of 2" in block and "⚠ 2 of 2" in block)

    print("FIXTURE 3: a section named in a title is not a section")
    print("  fails against: a parser taking every § in a heading")
    p = parsed_of(FIX_XREF)
    nums = [r["num"] for r in p["rows"]]
    check("one row", len(p["rows"]) == 1, str(nums))
    check("the row is 46.4a", nums == ["46.4a"], str(nums))
    check("46.4 got no row of its own", "46.4" not in nums)
    check("46.4 recorded as a cross-reference", p["rows"][0]["xrefs"] == ["46.4"])

    print("FIXTURE 4: the header counts the table, not the file")
    print("  fails against: any header carried over from a previous run")
    lines = FIX_STALE_HEADER.splitlines()
    span, err = marker_positions(lines)
    check("markers found", span is not None, err or "")
    p = parse(lines)
    block = "\n".join(build_block(p, notes_line_count(lines, span), "2026-08-19", "STUDY.md"))
    check("says 3 index rows", "**3 index rows" in block)
    check("the stale 174 is gone", "174" not in block)
    check("the stale rebuild date is gone", "2026-08-16" not in block)
    check("the stale 3816 is gone", "3816" not in block)

    print("FIXTURE 5: body references and fenced code are not sections")
    print("  fails against: a parser matching § anywhere in a line")
    p = parsed_of(FIX_NOISE)
    nums = [r["num"] for r in p["rows"]]
    check("one row", len(p["rows"]) == 1, str(nums))
    check("the row is 7", nums == ["7"], str(nums))

    print("FIXTURE 6: § headings outside ## and ### are reported, not dropped")
    p = parsed_of(FIX_LEVELS)
    check("one indexed row", len(p["rows"]) == 1, str([r["num"] for r in p["rows"]]))
    check("two headings reported as off-level", len(p["off_level"]) == 2,
          str(p["off_level"]))

    print("FIXTURE 7: headings with no § are counted, so coverage is visible")
    p = parsed_of(FIX_PLAIN)
    check("one indexed row", len(p["rows"]) == 1)
    check("one plain heading counted", p["plain_headings"] == 1, str(p["plain_headings"]))

    print("FIXTURE 8: hashes with no space are reported rather than lost")
    p = parsed_of(FIX_MALFORMED)
    check("one indexed row", len(p["rows"]) == 1, str([r["num"] for r in p["rows"]]))
    check("the malformed line is reported", len(p["malformed"]) == 1, str(p["malformed"]))

    print("FIXTURE 9: the line numbers written are the line numbers in the file")
    print("  fails against: a single-pass build, which numbers the file it replaced")
    lines = FIX_LINESHIFT.splitlines()

    # One pass, which is what the first version of this script did.
    span, _ = marker_positions(lines)
    p1 = parse(lines)
    b1 = build_block(p1, notes_line_count(lines, span), "2026-08-19", "S.md")
    once = lines[:span[0] + 1] + b1 + lines[span[1]:]
    check("a single pass is provably wrong, so this fixture discriminates",
          len(verify_line_numbers(once)) > 0,
          "single pass produced no mismatch, the fixture is not testing anything")

    final, pf, bf, err, passes = regenerate(lines, "2026-08-19", "S.md")
    check("the rebuild settles", final is not None and err is None, str(err))
    check("it settles in more than one pass, as expected", passes > 1, str(passes))
    check("no row points at the wrong line", final is not None
          and verify_line_numbers(final) == [], str(verify_line_numbers(final or [])))
    check("writing twice changes nothing",
          final is not None and regenerate(final, "2026-08-19", "S.md")[0] == final)

    def tally(rows):
        """The GOVERNS tally, over (code, text) pairs rather than a workbook."""
        distinct, cohorts = {}, {}
        occ = 0
        for code, blob in rows:
            hits = SECTION_RE.findall(blob)
            occ += len(hits)
            pre = cohort_of(code)
            for num in set(hits):
                distinct[num] = distinct.get(num, 0) + 1
                cohorts.setdefault(num, {})
                cohorts[num][pre] = cohorts[num].get(pre, 0) + 1
        return distinct, cohorts, occ

    print("FIXTURE 10: GOVERNS counts distinct rows, not occurrences")
    print("  fails against: a tally that counts every § it sees")
    d, c, occ = tally([("P-1", "§30 and again §30 and §30"), ("SE-1", "§30")])
    check("two rows cite §30", d["30"] == 2, str(d))
    check("four occurrences, which is NOT the number reported", occ == 4)
    check("renders the row count", render_governs(d["30"], c["30"]).startswith("2 "),
          render_governs(d["30"], c["30"]))
    check("each cohort counted once for the row",
          render_governs(d["30"], c["30"]) == "2 P×1 SE×1",
          render_governs(d["30"], c["30"]))

    print("FIXTURE 11: cohort is the whole leading run, so SE, SES and SET differ")
    print("  fails against: a cohort matched by prefix, which merges them into SE×3")
    d, c, _ = tally([("SE-1", "§5"), ("SES-2", "§5"), ("SET-3", "§5")])
    check("three distinct cohorts", len(c["5"]) == 3, str(c["5"]))
    check("renders all three", render_governs(d["5"], c["5"]) == "3 SE×1 SES×1 SET×1",
          render_governs(d["5"], c["5"]))
    check("SE did not absorb SES or SET", c["5"].get("SE") == 1, str(c["5"]))

    print("FIXTURE 12: ties sort alphabetically ascending")
    print("  fails against: Counter.most_common, which keeps insertion order")
    from collections import Counter
    tied = Counter()
    tied["NL"] += 1
    tied["ITT"] += 1
    most_common = " ".join("%s×%d" % (k, v) for k, v in tied.most_common())
    check("most_common gives NL first, so this fixture discriminates",
          most_common == "NL×1 ITT×1", most_common)
    check("rendered alphabetically", render_governs(2, dict(tied)) == "2 ITT×1 NL×1",
          render_governs(2, dict(tied)))
    check("count still leads on ties",
          render_governs(3, {"NL": 2, "ITT": 1}) == "3 NL×2 ITT×1",
          render_governs(3, {"NL": 2, "ITT": 1}))

    print("FIXTURE 13: a dash is only ever written from worksheet data")
    print("  fails against: filling the column with dashes when no worksheet is supplied")
    check("zero citing rows renders a dash", render_governs(0, {}) == GOVERNS_DASH)
    p_noise = parse(FIX_NOISE.splitlines())
    without = "\n".join(build_block(p_noise, 10, "2026-08-19", "S.md"))
    check("no worksheet means no GOVERNS column at all",
          GOVERNS_HEADER not in without)
    check("and no dash is invented", GOVERNS_DASH not in without)
    withdata = "\n".join(build_block(
        p_noise, 10, "2026-08-19", "S.md",
        {"column": {}, "row_citations": 0, "occurrences": 0, "cohorts": ["P"],
         "data_rows": 1, "source": "w.xlsx", "sheet": "S"}))
    check("with a worksheet, an uncited section does get a dash",
          GOVERNS_HEADER in withdata and GOVERNS_DASH in withdata)

    print("FIXTURE 14: the line number is read positionally, not by hunting digits")
    print("  fails against: a regex taking the last number-only cell in the row")
    p_rep = parse(FIX_REPEAT.splitlines())
    gov = {"column": {"83": "2 P×1 SE×1"}, "row_citations": 2, "occurrences": 2,
           "cohorts": ["P", "SE"], "data_rows": 2, "source": "w.xlsx", "sheet": "S"}
    rows_md = [l for l in build_block(p_rep, 10, "2026-08-19", "S.md", gov)
               if (split_md_row(l) or [""])[0].startswith("§")
               and (split_md_row(l) or ["", "", ""])[2].isdigit()]
    check("a GOVERNS cell is present to be confused with the line number",
          any("2 P×1" in l for l in rows_md))
    cells = split_md_row(rows_md[0])
    check("the header row is not mistaken for data", len(rows_md) == 2, str(len(rows_md)))
    check("the third cell is the line number", cells[2] == "3", str(cells))
    check("the fourth is GOVERNS", cells[3] == "2 P×1 SE×1", str(cells))

    print("")
    if failures:
        print("SELFTEST FAILED: %d of the assertions above" % len(failures))
        return 1
    print("SELFTEST PASSED")
    return 0


# ---------------------------------------------------------------- main

def main():
    ap = argparse.ArgumentParser(
        description="Regenerate the section index in a study log markdown file.")
    ap.add_argument("file", nargs="?", help="the study log markdown file")
    ap.add_argument("--write", action="store_true",
                    help="apply the rebuilt index to the file (default is a dry run)")
    ap.add_argument("--check", action="store_true",
                    help="exit 1 if the index in the file differs from a fresh build")
    ap.add_argument("--today", default=None, help="override the build date, YYYY-MM-DD")
    ap.add_argument("--worksheet", help="xlsx supplying the GOVERNS column")
    ap.add_argument("--sheet", help="worksheet sheet name (default: the one with a Code header)")
    ap.add_argument("--code-column", help="column letter holding the row code, e.g. A")
    ap.add_argument("--header-row", type=int, help="1-based row number of the header")
    ap.add_argument("--all-dangling", action="store_true",
                    help="list every worksheet citation with no matching section")
    ap.add_argument("--verify-governs", action="store_true",
                    help="compare a fresh GOVERNS against the column already in the file")
    ap.add_argument("--selftest", action="store_true", help="run the fixtures and exit")
    args = ap.parse_args()

    if args.selftest:
        return selftest()
    if not args.file:
        ap.error("a file is required unless --selftest is given")

    today = args.today or datetime.date.today().isoformat()

    with open(args.file, encoding="utf-8") as fh:
        text = fh.read()
    lines = text.splitlines()

    source_name = args.file.split("/")[-1]
    governs = None
    if args.worksheet:
        governs = compute_governs(args.worksheet, args.sheet,
                                  args.code_column, args.header_row)
    span, marker_err = marker_positions(lines)
    final, parsed, block, conv_err, passes = regenerate(lines, today, source_name, governs)
    if block is None:
        parsed = parse(lines)
        block = build_block(parsed, notes_line_count(lines, span), today, source_name)
    notes_lines = notes_line_count(final if final else lines, span)
    coll = collisions_of(parsed["rows"])

    # The run report prints per-item lines under named headings, not five
    # summary integers. A count is a summary of what this script chose to
    # count, and that is not the same set as what it found.
    print("build_studylog_index.py")
    print("file: %s" % args.file)
    print("")
    print("COUNTS, ALL DERIVED FROM THE TABLE BUILT THIS RUN")
    print("  index rows                          %d" % len(parsed["rows"]))
    print("  distinct section numbers            %d" % len({r["num"] for r in parsed["rows"]}))
    print("  section numbers used more than once %d" % len(coll))
    print("  headings with a § outside ## / ###   %d" % len(parsed["off_level"]))
    print("  ## / ### headings carrying no §      %d" % parsed["plain_headings"])
    print("  hash lines with no space after #    %d" % len(parsed["malformed"]))
    print("  lines of notes outside the block    %d" % notes_lines)
    print("  total lines read                    %d" % len(lines))

    if coll:
        print("")
        print("COLLISIONS")
        for num in sorted(coll, key=natural_key):
            for r in coll[num]:
                print("  §%-10s line %-6d %s" % (num, r["line"], r["title"]))

    if parsed["off_level"]:
        print("")
        print("NOT INDEXED, HEADING LEVEL OUTSIDE ## AND ###")
        for o in parsed["off_level"]:
            print("  line %-6d level %d  %s" % (o["line"], o["level"], o["text"]))

    if parsed["malformed"]:
        print("")
        print("NOT INDEXED, NOT A VALID HEADING")
        for lineno, t in parsed["malformed"]:
            print("  line %-6d %s" % (lineno, t))

    by_line = [r["num"] for r in sorted(parsed["rows"], key=lambda r: r["line"])]
    by_num = [r["num"] for r in parsed["rows"]]
    print("")
    print("ORDER")
    print("  file order matches numeric order:   %s" % ("yes" if by_line == by_num else "NO"))
    if by_line != by_num:
        print("  the table is sorted numerically, so a section written out of order")
        print("  still sits beside its neighbours in the index")

    if governs is not None:
        print("")
        print("GOVERNS")
        print("  source                    %s" % governs["source"])
        print("  sheet / code column / hdr %s / %s / row %d"
              % (governs["sheet"], governs["code_col"], governs["header_row"]))
        print("  worksheet data rows       %d" % governs["data_rows"])
        print("  distinct row citations    %d" % governs["row_citations"])
        print("  raw § occurrences         %d" % governs["occurrences"])
        print("  cohorts found             %s" % ", ".join(governs["cohorts"]))
        indexed = {r["num"] for r in parsed["rows"]}
        dangling = sorted(set(governs["distinct"]) - indexed, key=natural_key)
        dashes = sorted(indexed - set(governs["column"]), key=natural_key)
        print("  sections with no citing row (dash)  %d" % len(dashes))
        if dangling:
            print("  CITED BY THE WORKSHEET BUT NOT IN THE STUDY LOG: %d" % len(dangling))
            for n in (dangling if args.all_dangling else dangling[:20]):
                print("    §%s cited by %d row(s)" % (n, governs["distinct"][n]))
            if len(dangling) > 20 and not args.all_dangling:
                print("    ... and %d more, not listed. Rerun with --all-dangling."
                      % (len(dangling) - 20))

    if governs is not None and args.verify_governs:
        prior = existing_governs(lines)
        print("")
        print("GOVERNS VERIFICATION against the column already in the file")
        if prior is None:
            print("  no GOVERNS column found in the existing index, nothing to compare")
        else:
            diff = [(n, prior[n], governs["column"].get(n, GOVERNS_DASH))
                    for n in prior
                    if prior[n] != governs["column"].get(n, GOVERNS_DASH)]
            print("  rows compared %d, identical %d, different %d"
                  % (len(prior), len(prior) - len(diff), len(diff)))
            for n, was, now in diff[:25]:
                print("    §%-8s was: %-34s now: %s" % (n, was, now))
            if len(diff) > 25:
                print("    ... and %d more not listed" % (len(diff) - 25))
            if not diff:
                print("  reproduces the established column exactly.")

    if final is not None:
        bad = verify_line_numbers(final)
        print("")
        print("LINE NUMBER VERIFICATION")
        print("  settled after %d pass%s" % (passes, "" if passes == 1 else "es"))
        if bad:
            print("  MISMATCHED, the table points at %d line(s) that are not that heading:" % len(bad))
            for num, lineno, got in bad:
                print("    §%-10s says line %-6d found: %s" % (num, lineno, got))
        else:
            print("  every row points at its own heading in the file as it will be written")

    print("")
    print("WHAT THIS DOES NOT ANSWER")
    print("  Whether a section number is the right one. It reads what is there.")
    print("  Whether a heading without a § should have one. It counts them and stops.")
    print("  Whether two sections sharing a number should be merged. It shows both.")

    if len(parsed["rows"]) == 0:
        print("")
        print("REFUSING TO WRITE: no § headings found, so the index would be blanked.")
        return 1

    rebuilt = "\n".join(block)

    if span is None:
        print("")
        print("NO MANAGED BLOCK IN THIS FILE: %s" % marker_err)
        print("Put these two lines around the existing index, once, by hand, then rerun:")
        print("  %s" % START)
        print("  %s" % END)
        print("")
        print("The rebuilt index follows. Nothing was written.")
        print("")
        print(rebuilt)
        return 1

    if final is None:
        print("")
        print("REFUSING TO WRITE: %s" % conv_err)
        return 1

    if governs is None and args.write:
        print("")
        print("REFUSING TO WRITE: no worksheet supplied, so the GOVERNS column cannot be")
        print("computed. A dash in that column asserts that no row cites the section, and")
        print("asserting it from missing data would be a fabricated fact. Pass --worksheet.")
        return 1

    if verify_line_numbers(final):
        print("")
        print("REFUSING TO WRITE: the table's line numbers do not match the file.")
        return 1

    up_to_date = final == lines

    if args.check:
        print("")
        if up_to_date:
            print("CHECK: the index in the file matches a fresh build.")
            return 0
        print("CHECK FAILED: the index in the file differs from a fresh build.")
        print("Run with --write to update it.")
        return 1

    if not args.write:
        print("")
        print("DRY RUN, nothing written. The rebuilt index follows.")
        print("")
        print(rebuilt)
        print("")
        print("It is already what the file contains." if up_to_date
              else "It differs from what the file contains.")
        return 0

    with open(args.file, "w", encoding="utf-8") as fh:
        fh.write("\n".join(final) + ("\n" if text.endswith("\n") else ""))
    print("")
    print("WRITTEN: %d lines between the markers, replacing %d."
          % (len(block), span[1] - span[0] - 1))
    return 0


if __name__ == "__main__":
    sys.exit(main())
