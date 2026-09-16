#!/usr/bin/env python3
"""
ua_lastmod_check.py — every <lastmod> against the file's last commit.

Usage:  python3 ua_lastmod_check.py [folder] [--selftest]

THE QUESTION THIS CHECK MUST ANSWER
-----------------------------------
Not "does the sitemap have a lastmod". The question is:

    Does each entry's <lastmod> equal the date of the last commit that
    touched the file it points at?

WHY IT EXISTS
-------------
The rule was written on 30 August 2026 after 43 of 45 entries were found
carrying a date older than the page, some by seven weeks. It then held on
five consecutive batches and lapsed on 47b9574, the one commit where the job
was about wording rather than dates. A rule that depends on being remembered
fails on the task that does not cue it. This does not depend on that.

SCOPE, STATED HONESTLY
----------------------
It compares against the last COMMIT, so a page edited but not yet committed
compares against its previous state and is reported separately as not
comparable. Run it after committing, which is where the gate belongs: the
question "what am I committing" is the one that always gets asked.

It does not check whether the page should have changed, only whether the
sitemap agrees with git about when it did.
"""
import re, sys, os, subprocess

SITE = "https://usableaccess.io/"

def url_to_path(loc):
    """The one mapping that trips a naive sweep: the bare origin is index.html."""
    p = loc.strip()
    if p.startswith(SITE):
        p = p[len(SITE):]
    return p or "index.html"

def last_commit(path, cwd="."):
    r = subprocess.run(["git", "log", "-1", "--date=short", "--pretty=%ad", "--", path],
                       capture_output=True, text=True, cwd=cwd)
    return r.stdout.strip() or None

def dirty(path, cwd="."):
    r = subprocess.run(["git", "status", "--porcelain", "--", path],
                       capture_output=True, text=True, cwd=cwd)
    return bool(r.stdout.strip())

def run(folder="."):
    sm = os.path.join(folder, "sitemap.xml")
    if not os.path.exists(sm):
        print(f"no sitemap.xml in {folder}"); return 1
    raw = open(sm, encoding="utf-8").read()
    fails, missing, uncommitted, ok = [], [], [], 0
    for block in re.findall(r"<url>.*?</url>", raw, re.S):
        loc = re.search(r"<loc>(.*?)</loc>", block)
        if not loc:
            continue
        path = url_to_path(loc.group(1))
        lm = re.search(r"<lastmod>(.*?)</lastmod>", block)
        lm = lm.group(1).strip() if lm else None
        full = os.path.join(folder, path)
        if not os.path.exists(full):
            missing.append((path, lm)); continue
        if dirty(path, folder):
            uncommitted.append(path); continue
        git = last_commit(path, folder)
        if git is None:
            uncommitted.append(path + " (untracked)"); continue
        if lm != git:
            fails.append((path, lm, git))
        else:
            ok += 1
    print("=" * 62)
    if fails:
        print("FAIL — sitemap lastmod does not match the last commit:")
        for p, lm, g in fails:
            print(f"   {p:52} {lm} -> {g}")
    if missing:
        print("FAIL — in sitemap, not in the repo (hard rule 14):")
        for p, lm in missing:
            print(f"   {p}")
    if uncommitted:
        print("NOT COMPARABLE — uncommitted changes, run again after committing:")
        for p in uncommitted:
            print(f"   {p}")
    print("=" * 62)
    n = len(fails) + len(missing)
    print(f"{ok} entries agree | {len(fails)} stale | {len(missing)} missing | "
          f"{len(uncommitted)} not comparable")
    print("Regenerate with git log, never by typing the date.")
    return n

CASES = [
    ("https://usableaccess.io/", "index.html"),
    ("https://usableaccess.io/index.html", "index.html"),
    ("https://usableaccess.io/eaa-compliance-sweden.html", "eaa-compliance-sweden.html"),
    ("https://usableaccess.io/insights/ai-paradox.html", "insights/ai-paradox.html"),
    ("  https://usableaccess.io/privacy.html  ", "privacy.html"),
]

def selftest():
    bad = 0
    for loc, want in CASES:
        got = url_to_path(loc)
        if got != want:
            print(f"WRONG: url_to_path({loc!r}) = {got!r}, expected {want!r}"); bad += 1
    print(f"selftest: {len(CASES)} mapping cases, {bad} wrong")
    return bad

if __name__ == "__main__":
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    if "--selftest" in sys.argv:
        sys.exit(1 if selftest() else 0)
    sys.exit(1 if run(args[0] if args else ".") else 0)
