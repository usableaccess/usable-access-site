# CLAUDE.md — Usable Access site repo

Read this first, every session. It holds the standing rules, the tooling, and the current job queue.

Usable Access is a clarity-first EAA accessibility-compliance consultancy. This repo is the public site (GitHub Pages). **The site is the product demo** — an accessibility consultancy with an inaccessible or broken site has no business. Treat every change accordingly.

---

## THE WORKFLOW — never skip it

```bash
python3 tools/ua_page_check.py .     # CSS classes, facts, CTA wording, meta
python3 tools/ua_a11y_check.py .     # static WCAG checks
python3 tools/ua_orphan_check.py .   # internal link graph — orphans and broken links
```

**Both must report 0 failures before you commit.** After deploy, load the live URL and confirm it renders **styled** — a page can be valid HTML and still render naked if it uses a class that does not exist in `site.css`.

Never hand-author a page from scratch. Copy the canonical template (`eaa-compliance-ireland.html`) or build via a script, then check.

---

## 🔴 THE GENERATOR MUST NOT GRADE ITS OWN WORK

A check run by whatever produced the artefact is not verification. Claude writes the copy, Code applies it, and Code runs the checkers and reports independently. That separation is the reason the site is in good shape, and it is not optional.

Two consequences.

A check result is never a conclusion. PASS means the checker found nothing it knows to look for. Report the result and the limit together, or do not report it. Report what the checker returned and what it is capable of returning.

Prefer designs that fail visibly. Where there is a choice between something a checker confirms and something a human would notice broken, take the second. The skip link is the worked example: a hidden-until-focus link broke twice and passed every automated check.

Recorded 11 August 2026, after a practitioner published an account of Claude green-checking a one-pager whose reading order and heading structure were both broken. Full text in `UA_Standing_Corrections_v3.md`, which lives in the Claude project, not this repo.

### THE DEMONSTRATION, THE SAME DAY, ON THE DEFECT THE RULE WAS WRITTEN ABOUT
**JOB 0s ran all three checkers three times: before the change, after it, and after two fixes. All nine runs returned identical numbers.** 3 failures at root and 0 in `insights/` from `ua_page_check.py`, 0 failures across 44 pages from `ua_a11y_check.py`, 0 orphans and 0 unresolved from `ua_orphan_check.py`.

**Nothing in that sequence confirmed anything.** The skip link moved from hidden to visible, gained a strip, changed its label at one breakpoint, and had two real defects found and fixed in between. The checkers were blind to all of it, and they would have returned the same numbers had it been left invisible.

**What found the two defects was a browser at a stated width.** A skip link starting 60px left of the logo, because the strip was 1080px against a 960px container. A focus ring losing about 4px to the page edge and about 3px to the sticky header, because the strip's padding was smaller than the ring's reach. **Neither is expressible as a rule any of these checkers holds.**

**Read the identical numbers as the finding, not as the reassurance.** Three green runs across a change of this size means the checkers do not cover it, which is information about the checkers. **A number that does not move when the thing it describes has changed is measuring something else.**

---

## 🔴 READ BEFORE THE TOOLING TABLE: MOST OF IT DOES NOT EXIST IN THIS REPO

**Verified 11 August 2026. Five of the ten scripts named in this file are not here.**

| Script | State |
|---|---|
| `ua_page_check.py` | **present** |
| `ua_a11y_check.py` | **present** (needs `beautifulsoup4`; installed 8 Aug) |
| `ua_sync_blocks.py` | **present** — written 8 Aug because it was needed. OG block only |
| `ua_orphan_check.py` | **present** — written 9 Aug because JOB 0j could not be re-derived without it. `--selftest` included |
| `ua_insights_sync.py` | missing |
| `ua_backup.py` | missing |
| `ua_erase.py` | missing |
| `ua_study_export.py` | missing |
| `ua_merge_cowork.py` | missing |
| `ua_volatile_check.py` | **present** — written 8 Aug because a stale prediction shipped. `--selftest` runs 8 fixtures |
| `ua_claim_check.py` | **elsewhere, deliberately for now** — lives in the Claude project. See the gap note below |
| `ua_regulator_facts.json` | **elsewhere** — its data file, same place, same note |

There is no `tools/` directory. The table below describes an intended state, not the repo.

### THE ELEVENTH SCRIPT, WHICH IS IN NEITHER TABLE — RECORDED 15 August 2026
**`ua_claim_check.py` and `ua_regulator_facts.json` were built on 11 August 2026 in the Claude project session and have stayed there.** They were absent from the present-table and the missing-table alike, so the register said nothing about them at all.

**A blank cannot distinguish missing from deliberate**, which is why this note exists rather than a silent absence. Recorded as §22 in the standing corrections, which is on the project side of the split.

**Why it never came here:** the script is stdlib-only, so it ran wherever it was written and never needed the repo. **The facts file is public information**, so there is no reason it cannot be versioned.

**Why it is the sharpest instance of the split rule.** It is the one checker with a fixture pair that means something: **eleven block fixtures and seven pass fixtures**, a known-bad set it must flag and a known-good set it must not. That is the only control that survives its own author, because it does not route through the author's judgement at the time of writing. See JOB 0v, where a harness written to catch summary-blindness was itself summary-blind. **The one checker whose self-test is worth trusting is the one not versioned alongside what it checks.**

**The live consequence, which is not hypothetical.** It has been edited four times since it was written: Norway added, the German claim retired, prohibitions extended twice. **No history, no diff, and no record of what changed when.** That is the same class as the tarball problem, recoverable and invisible.

**This is the first of two instances of a class recorded below**, under THE CLASS: A TOOL AND ITS SUBJECT ON OPPOSITE SIDES. Read that as well, because the part that generalises is the trigger rather than the location.

**Two things to settle, and neither is urgent.** Whether `ua_regulator_facts.json` goes in the repo, and whether the script follows it. **The repo may be the wrong home even though the project session clearly is too**, because the script checks outreach documents rather than site pages, and this repo holds the site. A third location that is version-controlled would satisfy the actual requirement, which is history rather than proximity.

### THE SPLIT, WHICH IS THE ACTUAL RULE
**Scripts belong in this repo.** Versioning a checker alongside what it checks is the point, and two were written here today because a job needed them and they were not available.

**Client-facing documents and locked references live in the Claude project, which is a different filesystem.** `UA_Pricing_Reference_LOCKED.md`, `05_Services_And_Pricing.docx`, the report templates, `UA_Homepage_Hero_DJ_Merge_Brief.md` and the tracker are not reachable from a session working in this repo, and no amount of searching will find them.

**When a job names a file, check which side of the split it is on before planning around it.** A missing script can be written. A missing locked reference cannot be reconstructed, and guessing at its contents is how a €600 service gets quoted at €1,500.

### 🔴 THE CLASS: A TOOL AND ITS SUBJECT ON OPPOSITE SIDES RUNS WHEN SOMEONE REMEMBERS
**Promoted from a note to a class on 20 August 2026, on the second instance.** The first was recorded as a peculiarity of one script. Two is a shape.

| Tool | Lives | Its subject lives |
|---|---|---|
| `ua_claim_check.py` and `ua_regulator_facts.json` | the Claude project | outreach documents, the Claude project, but the site pages it reasons about are here |
| `scripts/build_studylog_index.py` | this repo, and only on the `studylog-index-generator` branch | `UA_StudyLog_Notes_CrossCutting_5.md`, the Claude project |

**The consequence is not that the work cannot be done.** Both are retrievable, and the second is on GitHub, so a project session can pull it. **The consequence is that it is never automatic.** A checker beside the thing it checks can run on every change, in a commit hook, in a job queue, or because someone ran the three checkers before committing. **A checker across the boundary runs when a person remembers it exists**, which is a different reliability class and degrades in a way nothing reports.

**The failure mode is silence.** Nothing goes red when a study log is edited and its index is not regenerated. Nothing goes red when the facts file gains a country and no page is re-checked. **The tool is fine, the subject is fine, and the gap between them holds no state**, so there is no artefact anywhere carrying the fact that they have drifted.

**This is why the §31.2 banner is worth reading as a symptom rather than a one-off.** A generated block inherited a wrong number and cited itself 92 times, which is what a hand-edit produces and a regeneration cannot. **The regeneration was available the whole time.** What was missing was anything that ran it.

### THE TEST, WHICH IS CHEAPER THAN THE FIX
**Before accepting a split, ask what triggers the tool.** If the honest answer is "someone notices", record that in the same breath as recording where the tool lives. **A location note that omits the trigger reads as solved when it is only located.**

**What would actually resolve it is one filesystem, not a better habit.** Either the subject comes to the tool or the tool goes to the subject. **A third versioned location satisfies the requirement for both**, which is the conclusion the eleventh-script note reached about history and which applies unchanged here.

### WHAT THIS BLOCKS
**JOB 0h cannot start.** It audits client documents against `UA_Pricing_Reference_LOCKED.md`, and neither the reference nor the documents are reachable here. **Putting them somewhere reachable is Laura's decision, not a gap for a session to work around.** The guard checker 0h asks for — read the locked reference, flag any euro figure in a client document that is not in it — is buildable in this repo the moment the reference is.

**JOB 0j needs re-deriving, not following.** It lists three under-linked pages. Two changed on 8 August: `insights/eu-ai-act-accessibility.html` gained an OG block, and `insights/invisible-revenue-loss.html` was deleted with its one inbound link repointed. `ua_orphan_check.py` was then written on 9 August and the graph rebuilt, so JOB 0j below now carries real numbers. This paragraph is kept because the reason it was needed still stands.

### 🔴 THE CLASS THE SPLIT PRODUCES: A TOOL SEPARATED FROM ITS SUBJECT RUNS ON MEMORY
**Promoted from a note to a class on 20 August 2026, on the second instance.** One instance is a circumstance. Two with the same mechanism is a class, and this one has no owner by construction, because neither side of the boundary can see the other.

| Tool | Lives | Its subject lives |
|---|---|---|
| `ua_claim_check.py` and `ua_regulator_facts.json` | the Claude project | outreach documents, same side, but nothing versions either |
| `scripts/build_studylog_index.py` | this repo, and only on the `studylog-index-generator` branch | `UA_StudyLog_Notes_CrossCutting_5.md`, the Claude project |

**The property is not distance. It is that nothing fires on change.** A checker sitting beside what it checks still only runs when someone runs it, but the file and the tool arrive in the same session, so the prompt is there. **Split them and the tool runs when somebody remembers**, which is a different and much worse schedule than "when the file changes".

**Both instances have already paid for it.** `ua_claim_check.py` has been edited four times with no diff and no record of what changed when. The study log index went three days with four collisions resolved silently, which is the failure the current generator exists to refuse.

### THE TEST, WHICH IS THE *WHERE* AND *WHETHER* NOTE AGAIN
**Say what the requirement actually is before choosing a location.** The requirement is that the check runs when its subject changes, and that its history is recoverable. **Proximity is one way to get both. It is not the requirement**, and treating it as the requirement is how "not this repo" became "not under version control" in the note above.

**So record two things for any tool whose subject is on the other side:** where the subject lives, and what is supposed to trigger a run. **A tool with neither recorded is not a check. It is a script somebody wrote once.**

### AND THE REASON PUSHING IS PART OF THE FIX
**A tool on the far side of the boundary is retrievable rather than blocking, but only if it was pushed.** `build_studylog_index.py` can be pulled into a Cowork session because it went to GitHub on 19 August. Had it stayed on one machine in a Dropbox folder, the boundary would have been absolute rather than an inconvenience. **One machine and a sync folder is not a copy, and for a split tool it is not a location either.**

### THE COROLLARY ON WHAT AN INDEX MAY SILENTLY DO
**Reporting a collision is correct behaviour and must not be read as a defect in the reporter.** The generated index shows §31.2 at two line numbers with the same GOVERNS figure, because two sections carry that number. **The defect is in the banner. The index is telling the truth about it.**

**An index that resolved the collision silently would have hidden it**, which is what the 16 August one did for four collisions across three days. This is the prefer-visible-failure rule at the top of this file, applied to a generated artefact: **where there is a choice between a clean output and one that shows the mess, take the one that shows the mess.**

---

## TOOLING (all in `tools/`)

| Script | Does | When |
|---|---|---|
| `ua_page_check.py` | Validates every CSS class against `site.css` and hard-fails undefined ones (this is what stops naked pages). Also fact traps, CTA wording, meta length, em-dash count | Before every commit |
| `ua_a11y_check.py` | Static WCAG checks: lang, skip link, landmarks, single h1, heading order, alt text, link/button names, form labels, ARIA validity, duplicate ids, table headers, zoom | Before every commit |
| `ua_sync_blocks.py` | **OG/Twitter block ONLY** (built 8 Aug 2026). Defines it **once** and writes it into every page, taking title, description and canonical from the page itself. Dry-run by default; `--write` applies. **Refuses two things:** redirect stubs, and any description over 155 chars, which it flags and skips rather than propagating | Whenever the OG block changes, or a page is added |
| `ua_orphan_check.py` | Builds the internal link graph. Reports orphans (zero inbound links), under-linked pages, in-sitemap-but-orphaned, and unresolved links. Counts links from `<main>` only — a page reachable solely from nav or footer is still effectively orphaned | Whenever a page is added; before declaring anything published |
| `ua_insights_sync.py` | Drift detector — home cards vs the insights index | Before declaring anything published |
| `ua_backup.py` | Timestamped snapshots of the irreplaceable files | Not repo work, but keep it versioned here |
| `ua_erase.py` | GDPR data-subject find/erase across the tracker | Not repo work, but keep it versioned here |

**`ua_sync_blocks.py` manages the OG block and nothing else.** Edit `OG_TEMPLATE` at the top of the script, run `--write`, run both checkers.

**The register previously described a wider tool that did not exist.** It claimed ownership of the footer legal links and, under JOB 5, the nav CTA markup and CSS. **No such script was ever in the repo.** What exists now covers OG only. **The footer and nav CTA are still hand-edited**, so do not assume a sync will propagate them.

```bash
python3 ua_sync_blocks.py .                  # dry run, changes nothing
python3 ua_sync_blocks.py . --write          # apply
python3 ua_sync_blocks.py insights --write   # the insights folder is separate
```

There is no `--adopt`. It was documented for bringing hand-written OG blocks under management; every OG block on the site is already inside the `ua:og:start` / `ua:og:end` markers, so there was nothing to adopt.

---

## 🔴 THE ONE QUESTION TO ASK OF ANY CHECK

**Before writing or trusting any check, state the question it must answer. Then confirm it is not answering a weaker one.**

A check that answers an easier question does not fail loudly. **It reports PASS**, which is worse than having no check, because it converts a real defect into a green tick and stops anyone looking.

**Four checks on this site did exactly that, and all four were found on 8 August 2026.**

| The check asked | The question it should have asked | What shipped |
|---|---|---|
| Does the class exist somewhere? | **Does it reach this page?** | A page linking no stylesheet passed, with a CTA panel that would render with no teal background and no orange button |
| Does the file mention telecoms? | **Does this sentence?** | The ComReg trap exempted itself on thirteen pages. On one, the word "telecoms" inside the error triggered the bypass that hid the error |
| Does the literal € sign appear? | **Does the figure?** | The site writes `&euro;`, so a currency trap was blind to every page it existed to check |
| Is there an accessible name? | **Is the name right?** | The logo announced "Usable Access comma home" on the accessibility statement page |
| How many footer *names* are there? | **How many footer *shapes* are there?** | "Exactly two footer shapes" went into a commit message and this register. There were seven |
| Is the link inside `<main>`? | **Is the link inside running copy?** | `ua_orphan_check.py`, written to enforce the body-copy distinction, counted 15 listing cards as body copy on its first run |
| What does the CSS text say? | **What does the browser do?** | A nav audit reported five pages with no mobile navigation and a hamburger that expands nothing. There was no defect. All 44 collapse correctly |
| What does a 390px **window** show? | **What does a 390px viewport show?** | Headless Chrome clamps to 500px, so the screenshot was a 500px layout painted onto a 390px canvas. It reads as horizontal overflow on the page |

### THE EIGHTH INSTANCE NAMES WHY THE OTHER SEVEN HAPPEN

**A regex reads text. A browser resolves cascade and viewport.** Those are different questions about the same file, and the first one is always easier to ask.

The nav audit ran three times and was wrong twice. First a flat regex matched the *first* `.nav-links` rule in the file, which is the desktop one, and reported the pattern intact everywhere. Then a "context-aware" version looked for a base-context `display:none` — but five pages are written mobile-last, hiding the nav inside `@media (max-width: 640px)`, so it reported them broken. Both passes were asking *does this text appear in this place*. **Only the third pass asked the real question: evaluate every media query against a concrete viewport width and see what wins.** At 390px, all 44 pages collapse correctly. There was never a defect.

**The correction was worth more than the finding would have been**, because it had already been characterised as a live WCAG 4.1.2 failure on production, and a fix was about to be written for pages that did not need one.

**Three of the nine instances came from the same author error: reading CSS or HTML with a regex that cannot see structure.** That is a specific and correctable class, not general carelessness. **When a question is about what renders, do not answer it by matching text.** Parse with context, resolve the cascade, evaluate the media query at a width, or open a browser. If none of those is available, say the check is textual and therefore provisional.

### THE NINTH INSTANCE: THE BROWSER IS AN INSTRUMENT TOO, AND IT LIES ABOUT WIDTH
**Found 18 August 2026, one line after the remedy above says "or open a browser."**

**Headless Chrome clamps its layout viewport to a 500px minimum.** `--window-size=390,2200` renders the page at 500px and paints it onto a 390px canvas. The right-hand side is cut off, so **it looks exactly like horizontal overflow on the page.** Probed from inside the document, a window asked for 390 reports:

```
client=500  inner=500  dpr=1
```

**Reporting that as a defect would have produced a fix for overflow that does not exist**, on a page that renders correctly. That is the nav audit again, one layer further out: a real defect characterised on production, a fix about to be written, and no defect there.

### THE PRECONDITION, WHICH IS THE POINT
**Before trusting any screenshot as evidence about a width, assert the width from inside the document.** Read `document.documentElement.clientWidth` in the page under test and confirm it is the number you asked for. **This is a precondition, not a workaround**, in the same shape as reading `document.activeElement` before sending a key sequence: the instrument's state has to be established before its output means anything.

**Report the probed width alongside the finding.** A screenshot with no width assertion is not evidence about that width, whatever the filename says.

**The method that works:** render the page in an iframe of the target width inside a window at or above the clamp, and write the measured width into the document so it is visible in the image itself. The 390px checks on `index.html` were done this way and carry a `vw=390` badge in the corner.

### WHAT THIS DOES AND DOES NOT CALL INTO QUESTION
**Only checks run through a headless window inherit it**, and the scope has to be stated rather than assumed, because a widened negative is the failure this register has recorded twice already.

**The 390px nav finding above is not affected.** It evaluated every media query against a concrete viewport width and never opened a window, so the clamp could not reach it. All 44 pages collapse correctly at 390px and that still stands.

**Any past "no overflow at 390px" taken from a screenshot is worth exactly as much as whether the probe ran.** None is recorded in this file, so nothing here needs revisiting. The rule is for the next one.

### WHY IT IS THE THIRD INSTANCE IN ONE SESSION
**The correction that produced it was right.** "What does the CSS text say" was replaced with "what does the browser do", which is the eighth instance's own prescription, and the new instrument had a blind spot the old one did not. **Knowing the general pattern did not prevent the specific error**, which is the 9 August finding holding for the third time in a day, after `:last-child` and after the summary-blind harness in JOB 0v.

**So the remedy list above is not a list of answers. It is a list of instruments**, and each one needs its own calibration reported with its result.


**The sixth is the sharpest, because the check existed for nothing else.** `ua_orphan_check.py` was written on 9 August precisely to separate a body-copy link from a listing card, since that distinction is what the publishing protocol turns on. It classified a card by looking for a class matching `card`, and `insights.html` wraps each entry in `<div class="article-list">`, which contains no such word. **A check whose entire purpose was one distinction could not see that distinction.** Fixing it moved the under-linked count from 8 to 22, so the first run understated the problem by nearly three times. **A checker is not exempt from the rule it enforces. Test a new check against the case it was written for, not against the case that is easy to construct.**

**The fifth is the one to watch for, because no check was involved.** A measurement was taken correctly, for one purpose, and then quoted to answer a different question. An accessible-name comparison normalises whitespace, so it cannot describe markup, and it reported two footer variants where the markup had seven. **A number is only true of the question it was measured for. Carrying it to a neighbouring question is the same failure with no code in it.**

**The tell is that the easier question is always the cheaper one to implement.** Existence is cheaper than reachability. A file scan is cheaper than a sentence scan. A literal character is cheaper than a normalised value. Presence is cheaper than correctness. **When a check was quick to write, that is when to ask what it is actually testing.**

### THE COROLLARY: A TRAP'S COUNT IS A FLOOR, NEVER A TOTAL
A check that answers a weaker question returns a count that is always too low. The JOB 0o instance count went 6, 13, 17, 24, 26, 27. **Only one of those jumps came from reading. Every other came from widening the detector.** Report a green trap as "none of the wordings we have been burned by is present", never as "the page is clean".

### THE SHAPE THAT ESCAPES THIS: CONSISTENCY, NOT QUALITY
**Every trap above failed because it needed to know in advance what wrong looks like.** A consistency check does not. It only needs to know what *different* looks like.

The accessible-name check built for JOB 0r is the model: repeated elements must have identical accessible names across pages, and any page disagreeing with the majority fails. No vocabulary of bad strings, nothing to widen, and no wording it can be blind to. **Where a rule can be expressed as "these should all agree", prefer that over a list of things that are wrong.**

### BUT A CONSISTENCY CHECK CAN AGREE ON A VALUE NOBODY HEARS
**Found 11 August 2026, on the JOB 0s skip link, and not fixed.** The label shortens at 390px, so the link carries two spans and CSS shows one at a time. `ua_a11y_check.py` builds an accessible name from the text it can see and reports `Skip to main content Skip to content` on all 44 pages.

**The vote passes, because all 44 agree.** A browser exposes one name at a time, so the string they agree on is one no user ever hears.

**This is not the easier-question failure.** The check asked its own question and answered it correctly: these pages agree. What it cannot see is whether the agreed value is the one that reaches a reader, because that depends on which rules apply at a given viewport width. It is the eighth instance wearing new clothes, reading text where the answer belongs to the cascade.

**So a consistency check is sound about difference and silent about correctness.** Unanimity is not evidence. **When every page agrees, ask whether the value they agree on is the one a user gets.** A name assembled from a subtree should skip anything the page hides, which is a real fix and not a large one.

Detail and instances: JOB 0f (the first three) and JOB 0r (the fourth, and the consistency check).

---

## 🔴 STANDING RULE: END EVERY SESSION WITH THE SEARCH CONSOLE LIST

**At the end of any session, list the full URLs that need indexing in Search Console, or say explicitly that none do.** Saying "none" is part of the rule. Silence is not the same answer and leaves someone checking.

**Give full URLs, `https://usableaccess.io/...`, never paths**, so they can be pasted straight in.

| Submit for indexing | Do not submit |
|---|---|
| New pages | Prose edits and rewording |
| Changed `<title>` or meta description | CSS, class fixes, rendering fixes |
| Changed canonical | Footer and nav changes |
| Factual corrections to a page's **central claim** | Anything Google will recrawl on its own schedule |

**Say whether the sitemap needs resubmitting.** It does only when entries were **added or removed**, not when a page's content changed.

### AFTER A DELETION, SAY WHETHER THE URL WAS INDEXED
**A 404 is not the whole job.** If the deleted URL was indexed, it needs a removal request as well, otherwise it keeps being served in results and keeps collecting impressions against a page that no longer exists.

**So for every page deleted or redirected, record: the full URL, whether it was indexed, and whether a removal request was raised.** `insights/invisible-revenue-loss.html` was deleted on 8 August with seven impressions in three months, so it was indexed and a removal request applies. **That was not raised at the time**, which is why this rule exists.

**The judgement is about the central claim, not the edit size.** A one-word fix that changes what a page asserts belongs in the list. A full rewrite of the prose around an unchanged claim does not.

---

## HARD RULES (these come from real mistakes; do not relitigate)

1. **Never use a CSS class that is not defined in `site.css`.** A page built on invented classes (`article`, `badge`, `site-header`, `cta-block`, `meta-date`…) renders completely unstyled. This has happened. The checker now blocks it.
2. **Never Unicode text-substitution formatting** (𝗯𝗼𝗹𝗱 characters). Screen-reader hostile. Applies to site and social copy alike.
3. **European English.** organisation, prioritise, behaviour, programme, licence, analyse.
4. **Em dashes sparingly** — 1–2 per page. Heavy use is itself a machine-written tell.
5. **Evidence-first, never alarm-first.** State the fact; let the reader conclude. Compliance is stated as a position and evidence, **never as a "violation"**, and never as certification.
6. **CTA wording:** "covers", never "identifies/tells you/find out whether X applies". Never imply a definitive legal determination. Use "likely in scope", "where gaps may exist", "relative to EAA requirements".
7. **Authority by service type** (Ireland): **CCPC** for products, e-commerce and consumer services generally; **Central Bank** for consumer banking and e-money; **ComReg for electronic communications ONLY**. ComReg appearing as the general authority is a bug — the checker traps it. On a telecoms page ComReg *is* correct.
8. **Ireland leads on criminal sanctions and personal director liability** (S.I. 636/2023, Reg 32–33). The €60,000 is secondary, never the lead.
9. **France:** enforcement is civil-society-led (disability organisations sued directly, Nov 2025). The June 2026 Carrefour outcome is a **court order with a €500/day astreinte, not an administrative fine**. Never state a French administrative fine figure.
10. **Netherlands:** the Oct 2025 reporting deadline is real; **do not state a hard NL fine ceiling** — unverified. Sweden is SEK 10m ≈ €900,000 plus market-ban power. **On 8 August 2026 the site was found asserting TWO different unverified Dutch ceilings: €900,000 on eight pages (borrowed from the Swedish figure) and €300,000 on `eaa-compliance-italy.html`. Neither had a source. Both removed.** That is what an unsourced number does over time: it does not stay wrong in one way, it multiplies into several mutually inconsistent versions on different pages. **The documented Dutch position:** the ACM is the general market surveillance authority with sector regulators alongside it, financial penalties have been legally available since June 2025, none has been issued, and the ACM's published posture is compliance first.
11. **No large administrative fines have been issued yet.** The accurate line is "enforcement is now running", never "fines are being levied".
12. **EN 301 549 currently references WCAG 2.1 AA.** Use that as the conformance target. (v4.1.1 → WCAG 2.2 is expected; when it lands, every page stating a level needs a migration pass.)
13. **Never name a company as a failing example** on a public page. Aggregated and anonymised only. **Carve-out: parties named by a court or by a regulator in its own publication may be named**, because the naming comes from that body rather than from us. This covers parties to public litigation (Auchan, Carrefour, E.Leclerc, Picard Surgel&eacute;s) and organisations a regulator has itself publicly listed. It does **not** extend to anything found in our own testing, and it does **not** permit characterising a listed organisation as failing. **PTS has published 28 names under investigation with no finding against any of them, so they may be named as under supervision and must never be described as non-compliant.** The risk is not the naming. It is implying a finding that does not exist.
14. **Never link a URL you have not confirmed exists.** Presence in `sitemap.xml` is NOT evidence a page exists — two sitemap entries pointed at pages that were never built, and the homepage linked to both. Check the file is in the repo before linking it.
15. **A new page ships orphaned by default.** Zero inbound internal links means almost no crawl priority, and its traffic then tells you nothing. Add body-copy links from topically adjacent pages — a card or a "Related" entry alone is demonstrably not enough (the Sweden article had both and was never fetched).
16. **Every page needs:** canonical, full OG + Twitter block, GA4, Clarity, `tokens.css?v=1` + `site.css?v=2` **or an inline `<style>` block that defines everything the page uses**, skip link, back-to-top, footer with the accessibility statement **and** privacy notice links.

    **The stylesheet clause is not a loophole, it is the current state of the site.** Measured 12 August 2026: **35 of 44 pages link neither `tokens.css` nor `site.css`** and are self-contained. They all render correctly. Read literally, the rule as first written failed 35 pages that have nothing wrong with them, which is the register describing the repo inaccurately.

    **What the clause still forbids is the case that caused it.** `what-happens-if-you-do-nothing.html` arrived on 8 August linking no stylesheet while using `.article-cta`, `.cta-button`, `.related-links` and `.related-list`, which were defined only in `site.css`. Its CTA panel would have rendered with no teal background and no orange button. **Self-contained means every class the page uses is defined where the page can reach it. It does not mean no stylesheet.**

    **This clause becomes unnecessary when JOB 0f step 4 lands** and every page links `site.css` for real. Delete it then.

---

## STANDING NOTE: THE EXPECTED FAILURE COUNT IS 3, NOT 0

**As of 9 August 2026 `ua_page_check.py` reports 3 failures at the repo root and 0 in `insights/`. That is the correct state. Do not try to reach zero.**

It briefly read 17 and 7 on 8 August, when the rule 16 footer check was added and the 21 pages it found were not fixed in the same pass. **Those 21 were fixed on 9 August and the count returned to 3 and 0.** All 44 pages now carry both legal links.

**Do not try to reach zero on the remaining three.**

All three are on `eaa-compliance-telecoms.html`, and all three are the ComReg trap firing on sentences that are right:

- "It is also worth knowing how a complaint reaches ComReg at all."
- "A consumer is expected to raise the problem with the provider first; ComReg comes in when it is not resolved."
- "So a complaint to ComReg is not the only way a requirement gets enforced."

**Why they fire.** The ComReg exemption is scoped to the sentence, deliberately. A page-wide exemption is what silenced the trap on all thirteen pages carrying ComReg, because it fired on any stray mention of telecoms anywhere in the file, including the Swedish regulator's name and the defect's own wording. See JOB 0o. Sentence scoping fixed that and costs these three: on a telecoms page the section carries the context and the individual sentence does not.

**Why they are not fixed.** Rewriting correct copy so a sentence repeats context the reader already has would make the page worse to make a number nicer. **These sentences read well and say true things.**

**How this differs from the redirect stub**, which WAS resolved by deletion: there the checker was enforcing a rule we had overridden, so the failure was the checker being out of date. Here the checker is correctly reporting what it was asked to report. **One was a stale rule, this is a chosen cost.**

### WHAT WOULD LEGITIMATELY CHANGE THE NUMBER
- **Up:** any new ComReg sentence outside a telecoms context, which is the trap working. Read it before assuming it is another false positive.
- **Down to 0:** a smarter scope than the sentence, for example carrying context from the nearest preceding heading. Worth doing only if it does not reintroduce a file-wide bypass.
- **Down by accident:** if someone edits those three sentences for another reason and happens to add a scoping word. Harmless, but the count moving is then not evidence of anything.

**If the count is anything other than 3 and 0, something changed. Find out what before assuming it is noise.**

---

## STANDING NOTE: THE HOMEPAGE HERO CARRIES FOUR EM DASHES IN PROSE, DELIBERATELY

**`ua_page_check.py` warns `4 em dashes in prose` on `index.html`. That is the correct state, and root warnings are 58 rather than 57 because of it. Do not fix it by rewriting the hero.**

**Set 18 August 2026.** Two pairs, both in the hero, and both are interruptions rather than qualifying asides:

- `Ireland and the Netherlands &mdash; insurance quotes, hotel bookings, travel enquiries, retail checkouts &mdash; tested the way a customer would`
- `What the standard element already did &mdash; work with a keyboard, announce what it is, report whether it is selected &mdash; was never rebuilt`

**Commas cannot do this job, because both asides contain commas.** Parentheses can, and were rejected: they read as a technical footnote where the sentence needs to read as speech. The alternative to the second pair is three short sentences, which loses the interruption the sentence is performing on purpose.

### THE GAP THIS SITS IN, WHICH IS THE PART WORTH KEEPING
**Hard rule 4 counts characters. It cannot distinguish an interruption from a qualifying aside**, and the HOW TO WRITE section is built entirely on that distinction. The rule's own reasoning is that a dash is usually the symptom of a main clause with an aside hung off it. **An interruption is not that shape**, and no character count can tell the two apart.

**So this will recur**, on any sentence that needs to break its own stride rather than qualify itself. **Record the decision, do not tune the threshold.** Lowering it makes more of these; raising it stops rule 4 catching the habit it exists to catch.

### WHY IT IS RECORDED RATHER THAN LEFT TO BE REDISCOVERED
**A warning that is known and accepted looks identical to one nobody has read.** That is the same problem as the three ComReg failures on `eaa-compliance-telecoms.html`, and it has the same answer: say which number is expected, and why, so a session can tell a live defect from a settled one.

**What would legitimately change it. Up:** any new prose dash on the homepage, which is the count working, so read the sentence before assuming it is this note. **Down:** a rewrite of either hero sentence for an unrelated reason, in which case the count moving is not evidence of anything.

---

## STANDING NOTE: SCOPE A BATCH BY CONTENT, NEVER BY FILENAME

**A correction pass that selects its pages by name will miss the pages that are about the subject but not named for it.**

**Found 8 August 2026.** The France corrections covered `eaa-compliance-france.html` and `insights/france-eaa-civil-society-enforcement.html`. `insights/rgaa-and-eaa-france.html` was not in the batch, so it kept an unverified €10,000 damages figure and an unattributed astreinte for the rest of the day. It is named for RGAA. **The batch boundary missed it, not the reading.**

**Before any correction pass, build the page list by grepping for the subject**, not by matching filenames:

```bash
grep -rln "Carrefour\|Caen\|astreinte" --include="*.html" .   # not: ls *france*
```

Grep the raw file rather than rendered text, so JSON-LD and meta descriptions are included. See the structured-data note below.

**The same applies to any subject that appears under more than one name:** the AI Act pages, the Barómetro figures, the Swedish PTS investigations, ComReg. A filename tells you what a page was called when it was created. It does not tell you what the page now says.

---

## 🔴 STANDING NOTE: A BRIEF THAT QUOTES PAGE COPY IS QUOTING A SNAPSHOT

**The working copy of the site outside this repo is a snapshot, not a mirror.** Read it for structure. **Never treat a quotation from it as the current text.**

**When a job brief says "replace X with Y", verify X against the repo and the live page before acting.** If X does not match, the brief was written against an older file, and applying it literally will overwrite whatever changed in between.

**Twice on 9 August:**
- A brief reported the homepage contradicting itself, twenty-two in the hero against thirteen lower down. **The live page was consistent.** The contradiction had been fixed the previous day in `c3ba50e`, and the copy predated it.
- A brief quoted a "before" paragraph and asked for it to be replaced. **The quoted text predated the em-dash pass and omitted a body link added hours earlier for JOB 0j.** Applying it literally would have deleted the homepage's only link to `eaa-revenue-loss`.

**So: match the quoted text against the file first.** If it does not match exactly, say so and show the difference before changing anything. **The instruction is still the instruction — what changes is which text it lands on**, and a brief cannot account for edits made after it was written.

---

## 🔴 STANDING NOTE: A FINDING KEEPS THE DENOMINATOR IT WAS MEASURED ON

**When the study grows, the headline numbers move and the subset findings do not.** A finding measured on part of the sample keeps that part as its denominator. Restating it against the new total silently invents a measurement nobody took.

**Found twice on 9 August**, when the field study went from 28 Irish journeys to 55 across Ireland and the Netherlands:
- **The overlay count.** Three retail sites on the same overlay were found in the **Irish e-commerce batch** — Life Style Sports, Carraig Donn, Home Store + More. No Dutch journey was checked for overlays as a systematic step. Restating it as "three of fifty-five" would understate the rate and overstate the scope in one sentence.
- **The statement counts.** Dutch coverage was 11 of 12 on an **insurance-only** sample and became 12 yes to 14 no once e-commerce was included, which is slightly worse than Ireland. **The finding reversed because the sample changed, not because the market did.** That is a sector effect wearing a market's clothes.

**The cause split has the same property** — the "standard control replaced by a custom one" versus "right element, never labelled" division was counted on the Irish journeys. It currently appears on `index.html` with no numbers attached, which is why it is safe. **If numbers are ever added to it, they need their own denominator.**

### THE RULE
**Before restating any figure against a new total, ask which sample it was measured on.** If the answer is "part of it", the sentence must say so and keep the smaller denominator. **Only figures measured across the whole study take the whole study's total.**

**Both directions of this error happened within an hour**, which is what makes it worth its own note: a global denominator given to a subset finding, and a subset finding quoted as though it were global.

---

## 🔴 STANDING NOTE: A RETRACTION MOVES THE FIGURES AND THE WORDS THAT QUANTIFIED THEM, AND ONLY THE FIGURES ARE GREPPABLE

**Found 19 August 2026, on the P-12 retraction.** The blocked count went 41 to 40, and every affected figure was found by grepping for digits and for word-forms of digits. **One sentence moved with them and no search could have surfaced it**, because the word it turns on is not a number.

`index.html` read *"The cause was usually a standard control replaced by a custom one."* At 17 against 17 that was defensible. The retraction took one custom-control journey out, leaving **16 against 17**, so "usually" was naming the second-largest cause. **Nothing was wrong with the sentence when it was written and nothing touched the file.** Changed to "often", which is true at 16 of 40 and survives the next retraction in either direction.

### WHY NO CHECK WILL EVER CATCH THIS
**A quantifying word has no value to compare.** "Usually", "most", "the majority", "typically", "in about half", "rarely" and "consistently" all assert a proportion and none of them states one, so there is nothing for a trap to match and nothing for a consistency vote to disagree about. **This is not the easier-question failure.** No cheaper question was substituted. There is no question to ask, because the claim lives in the gap between a word and a table that is somewhere else entirely.

**It is the sibling of the elapsed-counter gap in JOB 0v.** There, a wrong month count and a right one produce byte-identical output. Here, a wrong quantifier and a right one produce no output at all.

### THE RULE
**After any figure changes, re-read the sentences around it for words that assert a proportion, not only for the digits.** The digits are findable. The words are not, and they were true when they were typed, which is exactly what makes them invisible on a re-read that is looking for errors.

**Build the list of quantifying words as part of the change**, not as a search afterwards, because the search has nothing to search for. **The pages that carry a study figure are the pages to re-read whole**, and there are only ever a handful.

**Known instances to watch, both current and both correct today:** `index.html` "The cause was often", and `how-we-test.html` "The cause split roughly evenly", which holds at 16 and 17 and is more accurate now than when it was written. **`index.html` also says "In the remaining cases the right element was used and simply never labelled."** The remaining cases are 24, of which 17 were never labelled and 7 were other implementation faults. That imprecision predates the retraction and did not move with it, so it is recorded rather than changed.

---

## 🔴 STANDING NOTE: A CONCLUSION ABOUT *WHERE* READ AS A CONCLUSION ABOUT *WHETHER*

**The sibling of the denominator note above, and the same mechanism on a negative instead of a figure. The scope of a negative gets widened without anyone deciding to widen it.**

**Both instances landed on 15 August 2026.**

| The true, narrow conclusion | What it silently became | Why the difference matters |
|---|---|---|
| The EAA is **not incorporated** into the EEA Agreement | it is **delayed** | Two different states. "Delayed" implies a date exists. None does. See the Norway note below |
| `ua_claim_check.py` does not belong in **the site repo** | it does not belong **under version control** | The first is about one location, the second about a property. The script has been edited four times with no diff |

**The tell is that the narrow conclusion is usually right.** Nobody argued for the wide version, and nobody noticed adopting it. The site repo genuinely may be the wrong home, because it holds the site and deploys to a public server while the script checks outreach documents. **That argues against one location. It says nothing about whether history is needed**, and history was the actual requirement. A third versioned location satisfies it.

### THE TEST
**When a conclusion is a negative, say exactly what it rules out, then read the next sentence and check it does not rule out more.** "Not here" is not "not anywhere". "Not incorporated" is not "not coming". "Not this tool" is not "not any tool".

**Ask what the requirement actually was**, because the widened negative usually drops it. The requirement was history, not proximity. Once that is named, the false choice between two locations dissolves and a third option appears that nobody had to argue for.

---

## 🔴 STANDING NOTE: NORWAY. THE EAA IS NOT IN THE EEA AGREEMENT, AND THE REGULATOR'S OWN SITE SAYS OTHERWISE

**Verified at source 15 August 2026.** The full record is in `ua_regulator_facts.json` under `NO`, which is the source of truth and is on the project side of the split.

**The position.** **Bufdir**, the Norwegian directorate, states it has not been decided that the EAA will enter the EEA Agreement: *"Det er ennå ikke vedtatt at Tilgjengelighetsdirektivet (EAA) skal inn i EØS-avtalen"*, and on timing, *"det er vanskelig å si når dette blir."* **EFTA's EEA-Lex register** lists **32019L0882** as under scrutiny, with a draft Joint Committee Decision under consideration and entry into force pending. **No adopted JCD.**

**So the accurate line is that it is not incorporated, and no date exists.** Not "delayed", which implies a date that has moved. Not "coming", which implies a decision that has been taken.

### THE TRAP, AND IT IS THE WORST KIND
**`uutilsynet.no`, the Norwegian regulator's own site, still carries the EU timetable, "in force June 2025", as though it were Norway's.** It is stale, and **reliance on it is prohibited by name in the facts file.**

**This is worse than the three syndication failures.** Those were third parties repeating something stale. **This is the authority's own domain publishing a timetable that was never its own**, which makes it the most credible-looking wrong answer available on the question. **Anyone checking quickly stops there**, because a regulator's own site is exactly where a careful person expects to land.

**The general lesson, which extends JOB 0q rather than repeating it.** The Netherlands defects came in through English-language vendor summaries, so the rule there was to go to the primary source. **Here the primary source is the one that is wrong.** Being on the regulator's domain is not the same as being the regulator's position on the question you are asking, and a national regulator restating an EU timetable is describing the EU, not itself.

### WHAT THE SITE CURRENTLY SAYS
**One mention, on `eaa-compliance-finland.html` line 220**, in the Nordic enforcement passage. It says Norway *"operates under equivalent EEA obligations rather than the EAA directly"*, which is the careful framing and does not assert the EAA applies. **That half survives.** The rest was checked against `ua_regulator_facts.json` on 15 August 2026 and **neither part has an entry behind it.**

| On the page | State |
|---|---|
| The HelsaMi enforcement detail: December 2025, NOK 50,000 daily, 64 of 119 issues unresolved, 425,000 residents | **Not in the facts file. None of it.** Not the case, not the figure, not the counts |
| "equivalent EEA obligations" | **Names nothing.** No instrument, no source |

**So a live page carries a precisely worded enforcement claim about Norway with nothing behind it, established on the day Norway was confirmed out of EAA scope.** Read that against the precision note in JOB 0q, which was misread earlier the same day to mean the opposite: **precision without a source is the more dangerous shape, not the safer one.**

**Two content decisions, flagged rather than fixed, and neither is a repo change:**
- **The HelsaMi detail comes off the page until it has a primary source.** If it is real it belongs in the facts file first. If it came from a summary, that is the same route as the three claims that dissolved this month.
- **"equivalent EEA obligations" needs replacing or removing.** Norway has domestic accessibility law predating and independent of the EAA, which is plausibly what it means. **Plausibly is not a claim**, and naming the instrument is the whole of the fix if it is right.

---

## STANDING NOTE: STRUCTURED DATA REPEATS PAGE COPY, SO EVERY CORRECTION HAS TWO PLACES TO FIX

**JSON-LD blocks (`<script type="application/ld+json">`) carry page sentences verbatim, and they are invisible to any check that reads rendered text.** BeautifulSoup `get_text()` drops them. A grep of visible copy will not see them. A browser will not show them. Google will read them.

**Found 8 August 2026.** `eaa-compliance-ireland.html` carried the invented complaint procedure from JOB 0o **twice**: once in body copy and once inside its JSON-LD `"text"` field. The same page carried a second sentence in both places. Fixing only the visible one would have left the false claim being served to search engines while the page read correctly to a human.

**The rule: after any factual correction, grep the raw file, not the rendered text.** If the page has a JSON-LD block, assume the sentence you just fixed is in it too.

```bash
grep -l 'application/ld+json' *.html insights/*.html      # which pages have one
python3 -c "import re,sys; [print(m) for m in re.findall(r'<script type=\"application/ld\+json\">(.*?)</script>', open(sys.argv[1]).read(), re.S)]" PAGE.html
```

**This applies to the checkers too.** Anything built on `get_text()` is blind to structured data by construction, so a page can pass every check and still serve a corrected-away claim.

---

## HOW TO WRITE

**Write in plain, direct sentences.**

**Avoid constructions that need an em dash.** The dash is usually a symptom of a main clause with a qualifying aside hung off it. Restructure instead. Two short sentences are almost always better than one sentence with an aside. Em dashes are fine where they genuinely earn their place, at roughly one or two per page.

**Avoid the "it is X, not Y" construction.** It disguises itself as precision, sets up contrasts that often do not need to exist, and makes every statement sound like a correction of something nobody said. Use it only where a reader would genuinely otherwise assume the opposite.

**Say the thing plainly, then say the next thing.** Most qualifying asides are either unnecessary or deserve their own sentence.

**This applies to site copy, commit messages, and replies in the session.**

---

## JOB QUEUE

### 0a. 🔴 CORRECT THE EU AI ACT DATES — TODAY, BEFORE ANYTHING ELSE
`eu-ai-act-accessibility.html`, then grep the whole repo for "2 August 2026" and any claim the AI Act becomes "fully enforceable" on that date. **It is wrong as published, and today is the day after the date it names.**

Verified 3 Aug 2026 across Gibson Dunn, Freshfields, DLA Piper, Jones Walker, Ogletree and Winston Taylor:
- **Digital Omnibus on AI:** Parliament endorsed **16 June 2026**; Council final approval **29 June 2026**.
- **Annex III stand-alone high-risk systems → 2 December 2027** (was 2 August 2026).
- **Annex I embedded high-risk → 2 August 2028** (was 2 August 2027).
- **Article 50 transparency obligations were NOT deferred** and applied from 2 August 2026, with **Article 50(2)** marking/detection for legacy systems deferred to **2 December 2026**.
- National regulatory sandboxes deferred to 2 December 2027.

**Framing:** a deferral, not a repeal — the obligations are unchanged, the clock moved. Do not write it as a weakening of the Act.

**Note for the standing corrections:** the daily EAA enforcement scan would never have caught this. Adjacent regimes (AI Act, EN 301 549 versions, WAD) need their own periodic check.

### 0. From the analytics read (3 Aug) — do these first, they are small and high-return
Full reasoning in `UA_Analytics_Actions_3Aug2026.md`.

**a) Rewrite the meta description on `eaa-video-accessibility.html`.** 16 video queries, ~82 impressions, positions 4.0–27.7, **zero clicks** — a textbook meta-description problem and the largest well-positioned cluster on the site. Use:
> `The video you published since June 2025 is in scope, not just new uploads. What's required, when dubbing applies, and how to prioritise the backlog.` (148 chars)

**Change nothing else on that page**, so the effect is attributable to the meta alone.

**b) First, report the title and meta description of the page ranking for "eaa enforcement".** It is the **only query on the site with any CTR** (1 click from position 63.5). It is the only working snippet we own — read it before finalising (a).

**c) Check fines-vs-sanctions cannibalisation.** `eaa-fines-penalties-*` and `eaa-sanctions.html` may be competing for the same terms; the cluster has slid from "biggest opportunity on the site" in June to positions 49–62. Compare their titles and metas and report whether the territories overlap.

### 1. Site-wide sync — do first
The last pass covered only 14 of ~40 pages. Run `ua_sync_blocks.py . --adopt --write` across the whole repo, then all three checkers.

**The sync script now manages FOUR blocks**, each defined once at the top of the file: the footer legal links, the OG/Twitter block, the **nav CTA markup**, and the **nav CTA CSS**. `--adopt` brings existing hand-written OG blocks under management so future changes propagate.
**Expect it to surface more of what it already found on the pages checked so far:**
- **Missing OG blocks** — found on `eaa-compliance-fintech.html` and `eaa-compliance-saas.html`; likely on others. Any share of those pages renders as a bare link.
- **CTA overpromises** — `eaa-compliance-saas.html` promised "a free 20-minute conversation to find out whether the EAA applies to your organisation", a definitive legal ruling. Corrected to "covering whether your services are likely to be in scope". Check every page's CTA against rule 6.
- **Footers missing the privacy notice link.**
- **Missing nav CTA.** Five of the fourteen pages checked had no "Free assessment" button in the nav at all, so their only ask sat mid-body behind a 46.63% average scroll depth. Expect a similar proportion across the rest — this is the single biggest conversion fix available, and it is mechanical.
- **Broken skip links and missing landmarks.** `eaa-enforcement.html` had no `<main>` element, so its skip link pointed at a target that did not exist, plus a stray closing `</main>` and an undefined `article-nav` class. Check every page for these; a broken skip link on an accessibility consultancy's site is the worst possible defect.

Fix what the checkers flag, in one PR per class of defect, with a short summary of what was found.

### 2. New pages to add
- `privacy.html` — **new, required before outreach sends** (GDPR Article 14: the recipient must be able to find the privacy information). Built and checker-clean.
- `eaa-compliance-telecoms.html` — built this session, **never previously live**. ComReg IS the correct authority on this page (rule 7). No deadline: the accompanying post is postponed indefinitely.
- Add both to `sitemap.xml` with today's `lastmod`; add cards to `insights.html` and `index.html` only if they are being promoted.

### 3. Move the tooling into the repo
`ua_page_check.py`, `ua_a11y_check.py`, `ua_sync_blocks.py`, `ua_insights_sync.py`, `ua_backup.py`, `ua_erase.py` → `tools/`. Versioning the checkers alongside what they check is the point.

### 4. Do NOT recreate these cards
`/insights/ai-agents-need-accessibility.html` and `/insights/eaa-floor-not-ceiling.html` had homepage cards and sitemap entries but **the pages were never built** — visitors clicking them got a 404, and Google queued the URLs without ever fetching them. Cards replaced and sitemap entries removed on 3 Aug 2026. Both pages are on the content build queue with their recovered specs; **restore the cards only when the pages actually exist.** Run `ua_orphan_check.py` when they do, so they do not ship with zero inbound links.

### 4b. THE HOMEPAGE CARD ORDER IS DELIBERATE, NOT CHRONOLOGICAL
**Set 12 August 2026, JOB 0u.** The four `.insight-card`s in `.insights-grid-home` were in date order, newest first, until `what-happens-if-you-do-nothing.html` was added. It is the newest and it does **not** lead.

**`does-the-eaa-apply.html` keeps the lead slot**, dated 4 Aug against the newer card's 12 Aug. A visitor needs to know whether any of this applies to them before they need to know what happens if they ignore it, and the scope check is the homepage's primary funnel entry, linked five other times from the same page.

**Chronological is the right default and this is the case for overriding it.** A comment in `index.html` says so at the point of the edit, because the next person to look will otherwise see one card out of date order and correct it. **If you re-sort these cards by date, you have undone a decision rather than fixed a bug.**

### 5. Move the nav-CTA styling into `site.css` (do early — it is a live rendering bug)
`.nav-cta` and `.nav-cta-slot` are defined **only in `index.html`'s inline `<style>`**. They are NOT in `site.css`. Consequence: the "Free assessment" button renders as a plain blue underlined link on **every page except the homepage** — including pages that have been live for weeks.

Interim fix already applied: `ua_sync_blocks.py` injects the rules as a managed `<style>` block (marked `ua:nav-cta`) into any page that uses the class without defining it. That works, but carries duplicate CSS on every page.

**The proper fix:**
1. Move the rules from the managed block into `site.css` (bump the cache-buster to `site.css?v=3`).
2. Delete the `ua:nav-cta` block from every page and remove `NAV_CTA_CSS` injection from the sync script.
3. Run all three checkers, then confirm on a live non-homepage URL that the button renders orange and right-aligned.

**Related checker gap to fix at the same time:** `ua_page_check.py` reported `nav-cta` as a defined class because it is in the script's embedded fallback list, when `site.css` does not define it. **Trim the fallback list to only classes confirmed present in `site.css`** — a fallback that papers over the exact failure the checker exists to catch is worse than no fallback.

### 6. The Sweden orphan and the site-wide orphan audit
Spec: `UA_JobSpec_Sweden_Orphan_and_Audit.md`. The Sweden fix is done (body links added from the country page and the enforcement hub, plus a homepage card). **The audit is not** — run `ua_orphan_check.py` across the full repo and fix what it finds. Known already: the audit guide (`insights/how-to-audit-eaa-compliance.html`) is buried for lack of inbound links while eight audit queries appear in Search Console; link it from every country page's "what compliance requires" section.

### 7. Coming, not yet
- Overlay page (`/insights/accessibility-overlays-and-the-eaa.html`) — brief exists; copy comes from the content chat.
- Parallel-mechanisms cornerstone — the Arc A hub page.
- Enforcement fact fixes on the France and Ireland pages (rules 9 and 7).

---

## WHAT THIS REPO DOES NOT HOLD
No contacts, no prospect data, no pricing beyond what is published on the site, no client work. Those live in the tracker and in per-client projects. Keep it that way.

---

## HOW TO WORK HERE
Small PRs, one class of change each. Say what you changed and what the checkers reported. If a checker fails and the fix is not obvious, stop and report rather than working around the check — the checks encode mistakes that have already cost real time.
---

---

## 🔴 READ FIRST: `UA_Sources_of_Truth.md`

**For every class of fact, ONE file is authoritative.** Prices, regulatory dates, study numbers, pipeline state, findings, contacts, CSS classes. If a document disagrees with the register, the register wins and the document is wrong.

**The rule:** a fact in two places is a future error. Generate it, reference it, or check it — only type it where it is the source.

**Every document carries a status line.** `STATUS: CURRENT / SUPERSEDED / ARCHIVE` with a date. A stale document that looks current is how ten errors happened this week.


## 🔴 JOB 0e — DO THIS FIRST. TWO REAL CONTRAST FAILURES IN THE TEAL CTA BOX.

**Confirmed by calculation 6 August 2026. Both are on an accessibility consultancy's own call-to-action, on every page that has one.**

### Failure 1 — link text on the teal panel: 1.49:1
Any link inside `.article-cta` that is not the button inherits the browser default blue. Against the teal panel (`#0F6B6B`) that is **1.49:1**. Text needs **4.5:1**. Visited purple is 1.75:1; inherited site teal is **1.00:1**, i.e. invisible.

**Affects 14 pages** — every page with a CTA box except `does-the-eaa-apply.html`, `how-we-test.html` and `accessibility-overlays-eaa.html`, where a white link colour was defined during the build:

`ai-paradox` · `aimac-deep-dive` · `eaa-accessibility-statement` · `eaa-compliance-fintech` · `eaa-compliance-ireland` · `eaa-compliance-saas` · `eaa-compliance-sweden` · `eaa-compliance-telecoms` · `eaa-enforcement` · `eaa-governance` · `eu-ai-act-accessibility` · `services` · `wcag-em-2` · `what-makes-a-good-accessibility-statement`

### Failure 2 — orange button against the teal panel: 1.20:1
`--colour-orange #B05000` against `#0F6B6B`. The colours differ almost entirely in **hue**, not luminance, and WCAG does not count hue. **The boundary is what identifies the button as a control**, so this fails **1.4.11 Non-text Contrast**, which needs 3:1.

### THE FIX — one rule block, added wherever `.article-cta` is defined

```css
.article-cta a:not(.cta-button) {
  color: #ffffff;
  text-decoration: underline;
}
.article-cta a:not(.cta-button):hover,
.article-cta a:not(.cta-button):focus {
  text-decoration-thickness: 2px;
}
.article-cta .cta-button {
  outline: 2px solid #ffffff;
  outline-offset: 0;
}
```

**The underline is not optional.** With every element white, colour alone cannot distinguish a link from body text — that is **WCAG 1.4.1 Use of Colour**. Underline it.

**Do NOT change the orange.** It is a brand colour and it passes everywhere else — 5.26:1 on white. It only fails inside the teal panel, so fix it there only.

**Watch the focus state.** `.cta-button:focus` is already `3px solid white` with a `3px` offset. The resting outline is 2px at offset 0, so the two remain distinguishable — **verify this visually, do not assume it.**

### VERIFY AFTER
1. **Recalculate:** white on teal = 6.30:1 (text, needs 4.5) · white outline vs teal = 6.30:1 (non-text, needs 3)
2. **Look at three page types** — an article page, `services.html`, and one of the three already-fixed pages, to confirm consistency
3. `python3 ua_a11y_check.py .` and `python3 ua_page_check.py .`
4. Confirm no page still has a CTA box without a link colour defined

### WHY THIS IS FIRST
Every other job on this list is invisible to a visitor. **This one is on the element every visitor is asked to click, and it is the failure a knowledgeable prospect could check in ten seconds.** Roughly 30 minutes including verification.


---

---

## 🔴 JOB 0i — BUILD A COLOUR-CONTRAST CHECK INTO `ua_a11y_check.py`

**Why:** `ua_a11y_check.py` checks structure — lang, landmarks, heading order, names, labels, ARIA, duplicate ids. **It does not compute colour contrast at all.** Both teal-box failures in JOB 0e were found by eye, not by tooling, on an accessibility consultancy's own site.

### What to build

**1. Resolve the design tokens.** Read `tokens.css` (and any inline `:root` block) into a map of custom property to hex value — `--colour-teal` to `#0F6B6B`, and so on. Handle `var(--x)` references, including one level of indirection.

**2. Find the foreground/background pairs that matter.** Parse each page's inline `<style>` and `site.css` for rules that set `color` and `background`. Build the pairs that will actually render together:
- A rule that sets `background` on a container, and the `color` of text inside it
- **Descendant rules specifically** — `.article-cta` sets a teal background, `.article-cta a` sets the link colour. That is the pair that failed
- **Unset links inside a coloured container** — where a container sets a background but nothing sets `a` colour, assume the browser default `#0000EE`. **That is exactly the 1.49:1 failure, and it is invisible to any check that only looks at declared colours**

**3. Apply the thresholds.**
| What | Needs |
|---|---|
| Body text | **4.5:1** |
| Large text (18.66px bold, or 24px) | **3:1** |
| UI component boundaries — button borders, focus rings, input outlines | **3:1** (1.4.11) |

**4. Report the pair, the ratio and the requirement**, e.g.
`FAIL contrast: .article-cta a (#0000EE default) on .article-cta background (#0F6B6B) = 1.49:1, needs 4.5:1`

### AND A FOCUS-STATE CHECK, WHICH CONTRAST ALONE WOULD NOT HAVE CAUGHT

**Added 8 August 2026 after a focus indicator we introduced went to production nearly invisible.**

**The failure:** `.article-cta .cta-button` had a 2px white resting outline and a 3px white focus outline, both setting the same `outline` property. **Focus replaced the resting ring rather than adding to it** — a 1px width change in the same colour.

**A contrast check would have passed it.** White on teal is 6.30:1 in both states. **The ratio was never the problem.**

**What to check instead, for every element with both a resting and a focus style:**

1. **Do the two states differ by MORE than width in the same colour?** A change of colour, or an added property such as `box-shadow`, or a change in offset large enough to read as a new band. **Warn if the only difference is the width of the same-coloured outline.**

2. **Do both states set the same property?** If resting and focus both set `outline`, **focus replaces rather than adds.** That is legitimate if the colour changes, and near-invisible if it does not. Flag the combination.

3. **Is the visible band what the CSS suggests?** **Outlines paint above outer box-shadows**, and both start at the border edge — so a 2px outline over a 3px shadow shows **1px** of shadow. **Compute the visible width, not the declared value.**

4. **Is there a focus style at all?** Any interactive element with a resting outline and no `:focus` or `:focus-visible` rule.

**Report the visible widths and the delta**, e.g.
`WARN focus-state: .cta-button resting 2px #ffffff, focus 3px #ffffff — same colour, 1px delta. Focus may be indistinguishable.`

**Reference values, now live and correct:** resting `outline: 2px solid #ffffff`; focus `outline: 2px solid #ffffff` plus `box-shadow: 0 0 0 7px #000000`, giving **5px of visible black.** Different property, different colour, unmistakable.

**Why this matters more than most checks here.** Three defects in one session — unstyled CTA links, a missing `<main>`, and this — **were all found by eye. The tooling actively passed the focus ring.** WCAG 2.4.7 Focus Visible is Level A.

### Also check, in the same pass
- **Colour used alone to convey meaning.** If a rule sets only `color` on a link inside a coloured block with no `text-decoration`, warn — that is 1.4.1.
- **Focus states.** Any `:focus` outline colour against the background it sits on needs 3:1.
- **Custom status colours.** `.in-scope`, `.exempt`, the answer-path borders and the table row tints. These currently pass, but nothing is watching them.

### Known-good values to test against
Use these as fixtures so a regression is obvious:
```
white  #ffffff on teal #0F6B6B  = 6.30:1  PASS text
blue   #0000EE on teal #0F6B6B  = 1.49:1  FAIL text      <- the bug
orange #B05000 on teal #0F6B6B  = 1.20:1  FAIL non-text  <- the bug
body   #2C2C2C on #F4FAFA       = 13.23:1 PASS
orange #B05000 on #FEF6EE       = 7.10:1  PASS
teal   #0F6B6B on #F9F9F9       = 5.98:1  PASS
```

### Scope honestly
**This cannot catch everything.** It will not resolve cascade order, inherited colours through several levels, images behind text, or anything set by JavaScript. **Say so in the script's own output** rather than implying the page is clear. The goal is to catch the declared-colour failures, which is where both of these lived.

### Effort
Roughly 1–1.5 hours, most of it in the token resolution and pair-building. **Worth it:** this is the second time a real accessibility failure on our own site was found by eye rather than by tooling, and it is the category where being wrong costs most.


## 🔴 JOB 0f — CSS IS SCATTERED ACROSS THREE PLACES, AND IT BIT THREE TIMES IN ONE DAY

**The architecture is inconsistent.** Some pages link `/css/site.css`. Most are self-contained with a full inline `<style>` block. The legal shell (`privacy.html`, `accessibility-statement.html`) carries a *subset* — no CTA rules, because it has no CTA.

**Three failures on 4–5 August, all the same root cause:**
1. `.nav-cta` CSS existed only in `index.html`, so the orange button rendered as a plain blue link on every other page
2. `.status-block` was defined only in the article pages, so a homepage block would have rendered unstyled
3. `.article-cta` and `.cta-button` were missing from the legal shell, so both new pages rendered their CTA as a plain link

**Each was caught by eye, not by tooling** — and one shipped to production before it was noticed.

### STEPS 1 TO 3 ARE DONE — 9 August 2026. STEP 4 IS NOT, AND IS DELIBERATELY DEFERRED.

**Done:** the estate was measured, five class-name collisions renamed, the divergences resolved.
- **Measured.** 35 of 44 pages load no external CSS at all; only 9 link `site.css`. Of 2,417 inline rules whose selector also exists in `site.css`, **2,132 are byte-identical to it** once formatting is normalised. **It is a copy-paste estate with drift, not bespoke design per page.**
- **Renamed**, because they were not drift: `.article-title`, `.article-tag`, `.article-date`, `.article-meta` and `.article-market` meant one thing on `insights.html` cards and another on page headers. Now `.card-*` on `insights.html`, which was the only page using them as card classes. Verified pixel-identical before and after.
- **Resolved:** 18 single-property selectors to their strict majority (76 values, 35 pages), `.callout` and `.callout--orange` normalised, `.nav-links` unified to mobile-first on the five pages written mobile-last.
- **Left alone by decision:** `:root` tokens, `.cta-button`, `.article-tag`, `.requirement` and the other multi-property selectors. **Consolidating a design decision is worse than living with two versions.** They want a designer's eye, not a majority vote.

### 🔴 STEP 4 IS ITS OWN JOB: LINK `site.css` EVERYWHERE AND DELETE THE INLINE BLOCKS
**Not started, and not to be started casually.** 35 pages currently load no external CSS. Switching them means every page's styling depends on one file for the first time, and **the gain is maintainability rather than anything a reader sees.**

**THE ORDERING CONSTRAINT, which is the whole risk.** Adding the `<link>` and removing the inline block must happen **together, per page, in one edit**. Any window where a page has neither renders naked. And switching a page silently adopts `site.css`'s value for every selector where the two still disagree, so **that is a rendering change, not a no-op** — which is why steps 1 to 3 came first.

**Verify visually before deleting, not after.** Three page types minimum: a country page, an insights page, and the homepage. **`ua_page_check.py` cannot help**, because it validates classes against `site.css` whether or not the page links it. That is the third fallback failure, recorded below.

**When it becomes worth doing:** the next time the CSS needs a site-wide change. At that point it is 44 hand edits either way and the consolidation pays for itself immediately. Same reasoning as the managed footer block in JOB 0r.

### THE NARROW RULE THIS JOB PRODUCED: RESOLVE BOTH CSS SOURCES, ALWAYS
**While this site has two CSS sources, any question about what a page has must resolve both.** Not the inline block. Not `site.css`. Both, for that page.

**This is narrower than the easier-question rule and it is the one that would have prevented both of 9 August's instances.** A class check asked "is this class defined anywhere" rather than "does the definition reach this page". A reduced-motion check asked "does the inline block contain it" rather than "does the page get it" — and nearly added a duplicate block to the nine pages that already had it from `site.css`.

**Knowing the general pattern does not prevent the specific error.** The second instance was written about an hour after the eighth was recorded. **Only resolving both sources prevents it.** Step 4 removes the problem at source by making there be one source, which is the strongest argument for eventually doing it.

**Two things to do:**
- **Consolidate.** Move the shared vocabulary into `site.css`, keep only genuinely page-specific rules inline, and link `site.css` from every page. Verify nothing regresses visually before deleting the inline duplicates.
### THE THIRD FALLBACK VARIANT, FOUND 8 August 2026
**`ua_page_check.py` validates classes against `css/site.css` whether or not the page links it.** A page that loads no stylesheet at all still passes, because the definitions exist somewhere.

`what-happens-if-you-do-nothing.html` arrived with no `<link>` to any stylesheet, an inline `<style>` defining 18 classes, and four classes used but defined only in `site.css`: `.article-cta`, `.cta-button`, `.related-links`, `.related-list`. **The CTA panel would have rendered with no teal background, no orange button and no focus ring**, and it passed both checkers. It was built from `does-the-eaa-apply.html` with the CTA rules dropped.

**The rule: a page that links no stylesheet must not pass by inheriting one.** Resolve which stylesheets a page actually loads, and validate only against those plus its own inline `<style>`.

**This was the third failure of this shape in one day**, and a fourth followed the same afternoon. **The shape, the four instances and the corollary about counts now live in one place: THE ONE QUESTION TO ASK OF ANY CHECK, near the top of this file.** Read that rather than this list. What belongs here is only the class-check instance itself, above.

- **Trim the checker's fallback list.** `ua_page_check.py` passed all three of the above, because `nav-cta`, `status-block`, `article-cta` and `cta-button` are all in its embedded fallback vocabulary. **A fallback that vouches for classes it cannot see is worse than no fallback** — it converts a real failure into a green tick. Either point the checker at the real `site.css` and fail when it is absent, or make it warn loudly that it is guessing.
---

## JOB 0g — RE-TAG THE INSIGHTS FILTERS AROUND THE READER'S QUESTION, NOT OUR CATEGORIES

**Current filters:** Country · Guide · Intelligence · Revenue · Sector guide.

**Two problems.** `Guide` holds 15 of 37 pages — it has become the everything-else bucket. `Revenue` holds one, and a filter returning a single result teaches people the filters are not useful.

**The deeper problem:** these describe how we organise content. A business owner arrives with a question, not a content-type preference.

### The replacement, mapped to the four-question journey the site is now built around

| Filter | The question it answers | Pages that belong |
|---|---|---|
| **Does it apply to me?** | scope, eligibility, exemptions | scope check, country pages, sector pages, SaaS/B2B |
| **What does it require?** | the obligation itself | statements, WCAG-EM, video, standards, audit guide |
| **What happens if I don't?** | consequence and proportion | enforcement, country enforcement, governance, revenue loss |
| **How do I fix it?** | sequencing and method | how-we-test, overlays, prioritisation, remediation |

**Four roughly even buckets**, every page has an obvious home, and it matches the journey architecture in `UA_Channel_Architecture_Rethink.md`.

### How to do it
1. **Add a second data attribute** rather than replacing `data-type` — e.g. `data-question="applies|requires|consequence|fix"`. Keeps the existing type styling intact and makes the change reversible.
2. **Rewrite the filter bar** to drive off `data-question`.
3. **Re-tag all 37 cards.** A page may legitimately belong to two; pick the one a reader would look under first.
4. **Keep the card tag text as the content type** (Guide, Intelligence, Country guide, Sector guide) — it is useful descriptive text and it no longer needs to match a filter.

### Also fix while in there
**Every `data-type` must have a matching `data-filter`.** Two cards were `data-type="Insight"` with no Insight filter and were unreachable by any filter for weeks. **Add this as a check to `ua_page_check.py`:** parse the filter values and the card types on any page carrying `data-filter`, and fail if a type has no filter.

### Do not
Do not delete `data-type`. The card styling depends on it, and the type is still worth showing.
---

## STANDING RULE — CROSS-LINK EVERY NEW PAGE BEFORE IT IS CALLED PUBLISHED

**A new page ships orphaned by default.** The Sweden enforcement article sat live and in the sitemap and was never fetched, because nothing pointed at it — and a market was nearly written off on the basis of a page Google had never served.

**Before any new page is treated as published:**
- **Three to six inbound links**, chosen by where the reader is in the journey, not by topic similarity
- **At least two must be body-copy links** inside a sentence, not Related-list entries
- Card on `insights.html` with a `data-type` that has a matching `data-filter`
- Sitemap entry, and the page must be in the same upload batch
- `ua_orphan_check.py` run afterwards

**Do not link from pages whose reader is past that question.** Someone reading about statement quality already knows they are in scope; sending them to "does it apply to you?" is backwards.

### AND SET THE DATE IN THE SHIPPING COMMIT, NOT WHEN THE PAGE IS WRITTEN

**Nothing checks that a publication date matches the day a page actually went live.** `ua_volatile_check.py` catches a period that has already passed. It cannot catch a date that was correct when typed and wrong by the time the file shipped.

**The date lives in three places and all three drift together:** the page's own meta line, its card on `insights.html`, and its `<lastmod>` in `sitemap.xml`. Written on the 8th, shipped on the 12th, all three say the 8th.

**And all three use a different form, so a find-and-replace on the date will not catch them:**

| Where | Form | Example |
|---|---|---|
| Page badge | `Updated D Mon YYYY` | `Updated 12 Aug 2026` |
| `insights.html` card | `Published D Mon YYYY` | `Published 12 Aug 2026` |
| `sitemap.xml` | ISO `YYYY-MM-DD` | `2026-08-12` |

Searching for `8 Aug 2026` finds two of the three and misses the sitemap entirely. **Change all three by hand and check each one.**

**This will recur, because writing ahead of shipping is now the normal pattern rather than the exception.** `what-happens-if-you-do-nothing.html` was written on 8 August and ships on the 12th, and the mismatch was caught by reading rather than by any check.

**The rule: update all three dates in the shipping commit.** Not when the page is written.

**And mind that the two places use different words.** `ua_page_check.py` requires the page's own badge to read `Updated D Mon YYYY` and warns if it does not, while the `insights.html` card reads `Published D Mon YYYY` like every other new card. Writing `Published` on the page badge produces a warning, which is how this was caught.

**Add this to `UA_Publishing_Protocol.md`, which is in the Claude project rather than this repo** — see the split note at the top. Recorded here so a session working in the repo sees it.

Full procedure and checklist: `UA_Publishing_Protocol.md`.
---

## 🔴 JOB 0h — PRICING HAS DRIFTED ACROSS THE CLIENT-FACING DOCUMENTS. AUDIT AND REBUILD.

**Found 6 August 2026.** `05_Services_And_Pricing.docx` conflicts with `UA_Pricing_Reference_LOCKED.md` on nearly every line. **Sending it would quote a €600 service at €1,500.**

**The single source of truth is `UA_Pricing_Reference_LOCKED.md` (26 July 2026).** Nothing else may state a price that disagrees with it.

### Step 1 — audit every client-facing document against the locked reference
Check each for prices, service names, and services that no longer exist:

- `05_Services_And_Pricing.docx` — **confirmed drifted**, rebuild required
- `04_Service_Overview.docx`
- `UA_Proposal_Template_v3.docx` and `05_Proposal_Template.docx`
- `23_Engagement_Agreement.docx`
- Report templates `50`, `51`, `52`, `55`
- `services.html` and `index.html` — **verified correct as of 6 Aug**, use them as the reference for wording

**Report what disagrees before changing anything.** Some differences may be deliberate.

### Step 2 — rebuild `05_Services_And_Pricing` rather than patching it
It carries services that no longer exist (Quick Compliance Audit, UX-Enhanced Audit, Compliance Framework Starter, the Complete Packages bundles) and is missing two that do (Rapid Exposure Check €350, Remediation Re-test from €750). **A clean rewrite from the locked reference is faster and safer than an edit.**

### Step 3 — bake in the recurring-revenue changes while rebuilding
Full detail and exact wording in `UA_Recurring_Revenue_DocChanges.md`:
- **The 90-day re-check** as part of audit scope — the mechanism that makes the retainer a continuation, not a second sale
- **Retainer tiers restructured by KIND, not volume:** Maintain €1,200 · Protect €1,800 · Partner €3,600
- **A "what changes next" section** in the report templates

### Step 4 — three phrases to remove wherever they appear
- **"So you know where you stand legally"** — we do not give legal advice
- **Any claim that a service delivers "compliance"** — we assess and document; we do not confer conformance
- **Bare "WCAG 2.1 AA"** without noting that v4.1.1 incorporating **WCAG 2.2** is expected during 2026

### Step 5 — add a guard so this cannot recur
**A checker that reads `UA_Pricing_Reference_LOCKED.md`, extracts every price, and flags any client-facing document containing a euro figure that is not in the reference.** Roughly twenty lines, and it would have caught this months ago.

**Note the filename trap:** there are three copies of the pricing reference and the clean filename is not always the current one. The checker should read the one with the latest internal date, and say which file it used.
---

## JOB 0j — TWENTY-TWO UNDER-LINKED PAGES. REWRITTEN 9 August 2026 FROM THE REAL GRAPH.

**The previous version of this job was wrong in scope, in paths and in counts, and following it would have produced a confident report of success after editing almost nothing.** It listed three pages. There are twenty-two. It named `insights/eaa-video-accessibility.html`, **which does not exist** — the page is `eaa-video-accessibility.html` at the repo root. And it described each page's inbound link "from `insights.html`" as a link, when every one of those is a **listing card**, so the pages it listed had zero body-copy links rather than one or two.

**It was written on 7 August from a run of `ua_orphan_check.py` that no longer existed in the repo.** Numbers in this file need re-deriving before use whenever the tool that produced them is gone. See the fifth entry in the easier-question table: a measurement is only true of the question and the moment it was taken.

### THE NUMBERS, 9 August 2026, from `python3 ua_orphan_check.py .`
44 pages, 1 orphan, 22 under-linked, 0 unresolved. The protocol wants **three or more inbound with at least two in body copy**. Links are counted from `<main>` only; nav and footer never count.

### GROUP A — THIN. Under three inbound. Mechanical.
| Page | total | body |
|---|---|---|
| `what-happens-if-you-do-nothing.html` | 0 | 0 |
| `eaa-compliance-uk.html` | 1 | 0 |
| `eaa-video-accessibility.html` | 1 | 0 |
| `insights/arcom-france-public-sector-enforcement.html` | 1 | 0 |
| `insights/eu-ai-act-accessibility.html` | 1 | 0 |
| `insights/rgaa-and-eaa-france.html` | 1 | 0 |
| `eaa-compliance-telecoms.html` | 2 | 1 |

Five of these have a single listing card and nothing else. **These need links, and the targets are the ones the old job already suggested for telecoms and the AI Act page.**

`what-happens-if-you-do-nothing.html` ships Wednesday and is a separate batch: **the page, its `sitemap.xml` entry and its inbound links must be committed together.** The sitemap entry is already written and uncommitted, and committing it alone would publish a sitemap pointing at a 404, which is hard rule 14.

### GROUP B — BODY-STARVED. Reachable, never argued for.
| Page | total | body | related | card |
|---|---|---|---|---|
| `eaa-compliance-france.html` | 10 | **0** | 9 | 1 |
| `eaa-compliance-checklist.html` | 6 | **0** | 5 | 1 |
| `insights/wcag-em-2.html` | 5 | **0** | 3 | 2 |

**This is the Sweden failure mode at scale, and it is not solved by adding links.** France has ten inbound and not one inside a sentence. A page with nine Related entries is not short of links; it is short of a reason for anyone to follow one. **These need a judgement about where an argument naturally reaches for the page, which is content work, not graph work.**

### GROUP C — ONE BODY LINK. The same shape, one notch less severe.
Thirteen pages sit at exactly one body-copy link with heavy Related counts: `eaa-compliance-netherlands` (19 inbound), `eaa-sanctions` (16), `eaa-compliance-sweden` (15), `eaa-revenue-loss` (15), `eaa-compliance-ecommerce` (11), `bfsg-germany-accessibility-compliance` (7), `eaa-compliance-italy` (5), `eaa-compliance-saas` (5), `eaa-compliance-travel` (4), `insights/what-eaa-compliance-actually-requires` (4), `eaa-compliance-finland` (3), `insights/bfsg-germany-enforcement-abmahnungen` (3), `what-is-digital-accessibility` (3).

**The pattern across B and C is one fact: the site links by topic adjacency, through Related lists, and almost never from inside an argument.** Sixteen of forty-four pages have one body link or none. Fixing them one at a time treats the symptom.

### THE RULE THAT GOVERNS ALL OF IT
**Choose by where the reader is in the journey, not by topic similarity.** A link that arrives at the wrong moment is ignored, and enough of them teach the reader our links are not worth following. Do not link from pages whose reader is past that question.

### THE CHECKER FIXES FROM THE OLD JOB ARE DONE
`index.html` is excluded from the under-linked report with the reason in the code. `privacy.html` and `accessibility-statement.html` report as a footer-pages category rather than as orphans. Run it from the repo root: `python3 ua_orphan_check.py .` includes `insights/` automatically.

---

## 🔴 JOB 0o — AN UNSUPPORTED ENFORCEMENT PROCEDURE, AND ComReg CAST TOO WIDE, ON ELEVEN PAGES

**Found 8 August 2026 during the JOB 0n writing pass. Two separate factual defects, both repeated across the site. This is a hard rule 7 breach in the wild, and rule 7 exists because of it.**

The claim was removed from `eaa-compliance-telecoms.html` on 4 August for exactly these reasons. **It was never removed from anywhere else.**

### DEFECT A — a procedure no regulator publishes
**"The accessibility statement is requested first in any complaint investigation."** Nothing ComReg publishes supports this. It describes an investigative sequence we have invented, stated as settled procedure.

**FINAL COUNT: 13 pages. All deleted 8 August 2026.**

### THE DETECTION HISTORY IS THE POINT: 6, THEN 8, THEN 13
| Stage | Found | Why the earlier number was wrong |
|---|---|---|
| Manual grep on one phrasing | **6** | Searched for the wording seen on the first page |
| After the checker trap was written | **8** | The trap matched more phrasings than the grep |
| After deleting those and re-grepping | **13** | Five more in variants the trap still missed |

The five late finds were attributed differently every time: **"the competent authority"** (`eaa-compliance-ireland.html`, twice, once inside JSON-LD), **"a competent authority"** (`eaa-governance.html`), **"the Central Bank"** (`eaa-compliance-fintech.html`), **"a supervisory authority"** (`eaa-compliance-finland.html`, hedged with "typically"). **The claim had been reworded for each page while the invented procedure travelled unchanged.** Attribution drifted from ComReg to Irish regulators to the competent authority to the Central Bank, so no single search term could find them all. **Assume any invented framing has spread further than the phrasing you first searched for**, and re-grep after each deletion round until a round finds nothing.

The trap now covers the variant wordings. It found none on the final pass.

### WHERE IT CAME FROM, AND WHY IT WORE FOUR DIFFERENT ATTRIBUTIONS
**The claim was in four project markdown files, and two of them taught it as a house pattern.** That is why it appeared on 13 pages under four attributions rather than being copied verbatim: each page was written from a source that presented the procedure as established, and each author attributed it to whichever authority that page was about. **The site was not the origin. It was the symptom.**

Those source files are being removed at source, and the client-facing documents were checked and are clean.

**The general lesson for the register: when a false claim appears in more than two or three places under varying wording, look for a source document that taught it.** Deleting the instances without removing the source leaves it to be rewritten.

| Page | Line | Attributed to |
|---|---|---|
| `eaa-compliance-checklist.html` | 275 | ComReg |
| `eaa-compliance-ecommerce.html` | 131 | ComReg |
| `eaa-compliance-ireland.html` | 181 | Irish regulators |
| `eaa-accessibility-statement.html` | 252 | Irish regulators |
| `eaa-fines-penalties-ireland-netherlands-sweden.html` | 341 | Irish regulators |
| `insights.html` | 730 | Irish regulators |
| `services.html` | 126 | "an authority" |
| `insights/what-eaa-compliance-actually-requires.html` | 245 | Irish regulators |
| `eaa-compliance-ireland.html` | 79, 244 | the competent authority (one inside JSON-LD) |
| `eaa-governance.html` | 288 | a competent authority |
| `eaa-compliance-fintech.html` | 176 | the Central Bank |
| `eaa-compliance-finland.html` | 212 | a supervisory authority |

**Delete the procedural claim.** The defensible point survives without it: an accessibility statement is a mandatory EAA requirement, and an absent or inadequate one is visible to anyone who looks. Do not replace one invented procedure with another.

### DEFECT B — ComReg presented as the general authority
**Hard rule 7: CCPC for products, e-commerce and consumer services generally. Central Bank for consumer banking and e-money. ComReg for electronic communications ONLY.**

| Page | Line | What it says | Correct authority |
|---|---|---|---|
| `eaa-compliance-travel.html` | 133 | "ComReg enforces the EAA for digital travel services" | CCPC |
| `eaa-compliance-ecommerce.html` | 113 | "ComReg is the enforcement authority for digital services" | CCPC |
| `eaa-compliance-saas.html` | 266 | "ComReg enforcement ... apply to SaaS companies" | CCPC |
| `eaa-enforcement.html` | 229 | "ComReg enforces for electronic communications **and digital services**" | drop the second half |
| `eaa-fines-penalties-ireland-netherlands-sweden.html` | 288 | "ComReg (telecoms/**digital services**)" | drop the second half |
| `eaa-compliance-france.html` | 282 | link titled "criminal liability and ComReg enforcement" | retitle |

### CORRECT AND NOT TO BE TOUCHED
`eaa-compliance-telecoms.html`, `eaa-compliance-ireland.html` lines 223 to 224, `eaa-sanctions.html` line 206, and the `insights.html` telecoms card all reference ComReg on electronic communications, which is right. `eaa-compliance-fintech.html` line 147 explicitly corrects the error and should be left as the model.

### THE CHECKER GAP: A TRAP THAT EXEMPTED ITSELF WHEN THE DEFECT WAS PRESENT

**Diagnosed 8 August 2026. `ua_page_check.py` traps ComReg as the general authority and reported nothing on any of the thirteen pages carrying the word.** Two independent causes, and the first is the one worth remembering.

**1. The bypass was page-wide and fired on unrelated text.** The check computed `comms_scoped` by scanning the **whole file** for `telecom|electronic communications|communications regulation`, and skipped the ComReg trap entirely on any hit.

- On `eaa-compliance-ecommerce.html` the only match in the file was **"PTS (Post and Telecom Authority)"**, the Swedish regulator. Mentioning Sweden disabled the Irish trap. That page **did** match the trap pattern and was silenced anyway.
- On `eaa-fines-penalties-ireland-netherlands-sweden.html` the offending cell read **`ComReg (telecoms/digital services)`**. The word "telecoms" inside the error triggered the bypass that hid the error. **The defect exempted itself.**

**2. The pattern matched six fixed phrasings**, none of which was how the copy was actually written. `ComReg enforces the EAA for digital travel services`, `ComReg is the enforcement authority for digital services` and `ComReg enforcement ... apply to SaaS companies` all passed.

### The fix, applied
**The exemption is now scoped to the sentence, never to the page**, and the check matches **every** sentence containing ComReg rather than six phrasings. A sentence is clean only if it scopes itself to electronic communications, and it still fails if it widens to "digital services" in the same breath. **False positives are accepted as the cheaper error**, and the telecoms page now produces three: legitimate sentences where the surrounding section carries the context and the sentence does not.

A trap for defect A was added at the same time.

**After the fix: 14 pages report, against 0 before.**

### THE GENERAL LESSON: AUDIT THE OTHER TRAPS FOR THIS SHAPE
**A check that switches itself off when it sees the thing it is looking for is worse than no check**, because it reports PASS. The ComReg trap was the only one with a page-level bypass, so no other trap has this exact defect today. **But the shape is what matters: any exemption computed over a whole file can be triggered by text unrelated to the claim being checked.** Before adding a bypass to any future trap, scope it to the sentence.

---

## 🔴 JOB 0r — A SCREEN READER ANNOUNCED "USABLE ACCESS COMMA HOME". BOTH CHECKERS PASSED IT.

**Found 8 August 2026 by reading, on `eaa-accessibility-statement.html`.** The site logo's accessible name was:

```html
<a href="/" class="site-logo" aria-label="Usable Access , home">
```

**A screen reader announced our own company name with a comma in the middle of it, on the accessibility statement page.** Every other page carries `aria-label="Usable Access &mdash; home"`. An em-dash conversion had turned the dash into ` , ` on this one page. Fixed the same day.

### WHY BOTH CHECKERS PASSED IT, WHICH IS THE POINT
**`ua_a11y_check.py` checks that links and buttons HAVE an accessible name. It does not check what the name SAYS.** `ua_page_check.py` reads `aria-label` into its trap surface, so it could see the text, but no trap looks at name quality.

**This is the easier-question failure in its purest form yet:** does an accessible name exist, rather than does the accessible name read correctly aloud. Presence is trivial to test and it is not the thing that matters. **It is the fourth instance in the table under THE ONE QUESTION TO ASK OF ANY CHECK, near the top of this file. Read that for the shape.**

**It is also the fourth defect found by eye on our own site while the tooling reported clean**, after the unstyled CTA links, the missing `<main>` and the near-invisible focus ring.

### THE CHECKER GAP TO CLOSE
**Validate accessible-name CONTENT, not only presence.** In `ua_a11y_check.py`, across every `aria-label`, `alt` and link text:
1. **Punctuation a screen reader will announce.** A comma, semicolon or colon surrounded by spaces (` , `), doubled punctuation, or a name ending in a stray separator. **` , ` is the defect actually found and it must FAIL, not warn.**
2. **Names that are the same across pages must BE the same.** The logo, the skip link, the back-to-top control and the nav CTA appear on every page. Build the set of accessible names per repeated element and **fail on any page that disagrees with the majority.** That one rule would have caught this, and it needs no vocabulary of bad strings.
3. **Empty-after-normalisation names**, and names that are only punctuation or entities.
4. **`alt` text duplicating adjacent visible text**, which doubles the announcement.

### RULE 2 IS BUILT — 8 August 2026
In `ua_a11y_check.py`. It collects the accessible name of each repeated element on every page given to it, takes the majority, and fails any page that disagrees. **The other pages are the specification**, so it needs no vocabulary of bad strings.

**Run it as `python3 ua_a11y_check.py . insights`, in one invocation.** The vote is taken across the pages it is given, so checking the two folders separately gives it 32 pages and then 12 instead of 44. A smaller electorate is a weaker check.

**Scope was decided by measuring, not by assuming.** Across 44 pages the site logo, skip link, back-to-top and main nav each have exactly one name on 44 pages, and the nav CTA one name on 26. Those five FAIL on disagreement, with no false positives available to them.

**The CTA button WARNS instead.** It has four names across 41 pages: 35 say "Book your free assessment today", 4 say "Book your free assessment", and 2 legitimately differ because they ask for something else. A majority vote there would be right about four and wrong about two, so it is a warning.

**A tie reports nothing.** With two variants at 50/50 there is no majority, neither side is the specification, and guessing would be worse than silence.

**Verified against the real defect**, not only against fixtures: reintroducing ` , ` into the logo on a copy of the site produces `FAIL 4.1.2 site logo accessible name is 'Usable Access , home' but 31/32 pages use 'Usable Access — home'`. `--selftest` covers five cases including the tie and the below-threshold case.

### THE FOOTER CHECK IS BUILT AND THE 21 PAGES ARE FIXED — 8 and 9 August 2026
In `ua_page_check.py`. **The question it answers:** does this page's footer link BOTH legal documents? Not "does the page mention privacy" and not "is there a footer", which are the cheaper questions all 21 pages would pass. **A privacy link elsewhere in the body does not satisfy rule 16**, and a fixture covers that, because the rule is about the footer being the reliable place to look.

**Fixed 9 August.** All 21 were missing `/privacy.html` only. Each had its single `<p>` split so the legal links sit in their own second `<p>`, matching the majority shape, with the `aria-hidden` middot separator between them. **All 44 pages now carry both links, and the footer link sequence is one distinct value across the whole site.** The check reports 0.

### CORRECTION: "EXACTLY TWO FOOTER SHAPES" WAS WRONG
**The 8 August note said there were two footer shapes. There were seven.** That claim came from the accessible-name measurement, which normalises whitespace, so it collapsed markup differences that a name comparison cannot see. Reading the raw markup before editing found: two variants of the broken shape differing by a stray space, four variants of the good shape, and one page carrying both links inline in a single `<p>` rather than in a second one.

**The measurement was right about names and wrong about markup, and it was quoted as though it were about markup.** Five cosmetic shapes remain, all whitespace except `eaa-compliance-telecoms.html`, which keeps its links inline, and `what-happens-if-you-do-nothing.html`, which uses `&mdash;` separators instead of middots. **Neither affects what a reader or a screen reader gets**, so both were left alone.

**The general point, which is the same as everything else in this file:** a measurement answers the question it was built for. Quoting it for a different question is how "two shapes" got into a commit message. It is the fifth instance in the table at the top of this file.

### IF YOU BUILD A MANAGED FOOTER BLOCK LATER, THESE TWO ARE THE ONLY REAL OUTLIERS
**Not built, deliberately.** The check now guarantees the thing that matters, the five remaining shapes differ only in whitespace, and a second managed block in `ua_sync_blocks.py` is a bigger commitment than this register accounts for. **Build it when the footer next needs to change** — a third legal link, a company registration line, a cookie notice — because at that point it is 21 hand edits again and the block pays for itself immediately.

**The two that are not whitespace, and will need a decision rather than a reformat:**
- **`eaa-compliance-telecoms.html`** carries both legal links **inline in the first `<p>`**, not in a second one. It passes the check and reads identically. A managed block would restructure it.
- **`what-happens-if-you-do-nothing.html`** uses **`&mdash;` separators** where every other page uses `<span aria-hidden="true"> &middot; </span>`. It is still untracked and ships Wednesday, so it will need bringing into line then whether or not a block exists.

### HOW THE FOOTER LINKS WERE MEASURED, AND WHY THEY ARE NOT IN THE NAME VOTE
Footer link names split 23/21 across 44 pages. **The difference is that 21 pages omit the privacy notice link entirely.** That is hard rule 16 ("footer with the accessibility statement **and** privacy notice links") and JOB 1 already lists it as expected.

**It is a missing-link defect, not a naming inconsistency**, so putting it through the name vote would describe it wrongly and it was excluded. **Nothing currently enforces rule 16.** A separate check is warranted, and it is close to trivial: every page's footer must contain a link to `/accessibility-statement.html` and one to `/privacy.html`. **This matters beyond tidiness because `privacy.html` is required before outreach sends** under GDPR Article 14, per JOB 2.

### IT BELONGS IN THE SKIP-LINK POST, WHICH IS NOT IN THIS REPO
The piece arguing that automated tools confirm presence while only a person confirms function should use this as its example. **It beats any hypothetical**: our own site, our own name, both checkers green, and the failure audible only to someone actually listening.

**Checked 8 August 2026: that post is not on this side of the split.** Every `skip link` string in the repo is either CSS or the boilerplate link itself, and no page carries the presence-versus-function argument. The nearest thing is `index.html`, which says findings come from going through the journey rather than from an automated pass. **The post is in the content project, so the example has to be added there.**

---

## JOB 0q — A PROCEDURE PUT IN THE ACM'S MOUTH. CHECKED AGAINST SOURCE 8 August 2026 AND IT FAILS.

**Its own item, not part of JOB 0o.** Defect A is a procedure nobody published. **This is a procedure attributed to a named regulator that the regulator's own publications contradict.** The attribution makes it worse, not better: an unattributed claim is ours to withdraw, and this one puts words in the ACM's mouth.

**The sentence, on `eaa-compliance-netherlands.html` line 164, inside an orange callout:**
> Failure to report does not make an organisation invisible to enforcement. It makes it a priority target. **The ACM has been explicit that non-reporting organisations will be audited first.**

**What the ACM actually publishes.** Four of its own pages were read.
- **Meldplicht page** — states the obligation and nothing about consequences for not reporting. On what follows a report: *"We nemen geen contact op na uw melding, behalve als we nog vragen hebben."* No prioritisation of non-reporters anywhere.
- **"ACM roept bedrijven op…"** — the stated first-period priority is the **opposite** basis: *"De ACM richt zich in de eerste periode vooral op kritieke toegankelijkheidsproblemen die veel negatieve impact hebben op gebruiksmogelijkheden door mensen met een beperking."* Selection by user impact, not by who filed.
- **English supervision page** — *"Our enforcement actions depend on the magnitude of the problems, and on what steps companies are taking to solve those problems."*
- **The large-webshop investigation** — selection criterion stated as **"de grootste bedrijven met de meeste klanten"**, and next steps as *"De ACM wijst de grootste bedrijven die het slechtst presteren op de verbeterpunten."* Size and performance. Reporting status is not mentioned as a criterion.

### THE FOUR ACM SOURCES — READ THESE, DO NOT REPEAT THE SEARCH
| What it settles | URL |
|---|---|
| The meldplicht itself, and that nothing follows a report except questions | `https://www.acm.nl/nl/toegankelijkheid/toegankelijkheid-van-e-handelsdiensten-en-elektronische-communicatiediensten/meldplicht-bij-niet-voldoen-aan-toegankelijkheid` |
| The stated first-period priority, by user impact | `https://www.acm.nl/nl/publicaties/acm-roept-bedrijven-op-zich-voor-te-bereiden-op-regels-toegankelijkheid-websites-en-apps` |
| Enforcement scaled to problem magnitude and to what the company is doing | `https://www.acm.nl/en/accessibility/accessibility-e-commerce-services-and-electronic-communications-services` |
| The ~100 webshop study: selection criterion, the 61%, the 33% | `https://www.acm.nl/nl/publicaties/acm-klant-met-beperking-kan-bij-merendeel-grote-webwinkels-niet-terecht` |

### THE NETHERLANDS PAGE IS A KNOWN ROUTE FOR VENDOR-SUMMARY CLAIMS
**The claim is in vendor blog summaries in almost our wording. Same provenance as the Carrefour €10,000 damages figure**: present in secondary commentary, absent from the primary source. **Two of the three defects on this page now share that origin**, and the third was the €900,000 ceiling borrowed from Sweden.

**That is a property of the page, not a coincidence.** Dutch primary sources are in Dutch, so an English-language vendor summary is the path of least resistance and it is where the wording came from. **Treat anything on this page that attributes a position to the ACM as unverified until it is read against acm.nl directly.**

**Verified against source while here, and correct:** approximately 100 of the largest Dutch webshops tested, ordering impossible with assistive technology in **61%** (*"bij 61% onmogelijk is om een bestelling te plaatsen met hulpapparatuur"*), serious problems in a further 33%. That figure is in the meta description too and is safe.

### THE OTHER THREE, CHECKED 8 August 2026: TWO FAIL, ONE HOLDS

**"The ACM has stated publicly that fines are not its primary goal." HOLDS.** The [ACM Toezichtvisie](https://www.acm.nl/system/files/documents/acm-toezichtvisie.pdf) describes the ACM as a mission-driven supervisor, says supervision is more than imposing a fine when a company breaks the law, and says it prioritises preventing further harm over punishing past behaviour. **The two sentences that followed it did not hold.** "Contributing to equal access rather than punishing non-compliance" grafted the accessibility mission onto a general supervision vision whose mission is well-functioning markets. "Except in cases of egregious or wilful non-compliance" was our own carve-out with no source. Both replaced with what the sources support, including the ACM spokesperson in [NOS](https://nos.nl/artikel/2607639-veel-grote-webwinkels-niet-toegankelijk-voor-mensen-met-beperking): companies get *"een redelijke termijn"*, and if they still do not comply *"dan volgen er sancties. Bijvoorbeeld een boete of last onder dwangsom."*

**"As of June 2026 the ACM has moved from information-gathering toward formal sanctions." FAILS.** No ACM publication describes a phase transition. Deleted from four pages, in three wordings: "moved from the information-gathering phase … toward formal sanctions", "has shifted from information-gathering to formal sanctions" twice, and "is moving toward formal sanctions".

**"Formal sanctions are expected in the second half of 2026." FAILS, and differently.** Deleted from five places including a JSON-LD field and a comparison-table cell.

### THE NEW RULE: A PREDICTED TIMELINE CANNOT BE ATTRIBUTED

**A published intention is checkable. A predicted timeline is not, because the period is not over.** Attributing a prediction to a regulator is therefore a stronger claim than making it ourselves, and it is unfalsifiable until the moment it is simply wrong.

**The rule.** Never attribute a future timeline to a regulator. If we believe sanctions are coming in a given period, **say that we expect it and why**, or say nothing. The NOS quote shows what a regulator will actually commit to: a reasonable period, then sanctions. No date. **If the regulator would not put a date on it, we cannot put one in its mouth.**

**This extends rule 10 twice over.** Rule 10 covered unverified figures. JOB 0q extended it to unverified regulator *intentions*. This extends it again to regulator *predictions*, which are worse, because no amount of checking can confirm one.

### THE SECOND HALF OF THE RULE: ANY STATED FUTURE PERIOD NEEDS A REVIEW DATE

**The attribution rule is not enough, because the mechanism is not about regulators.** A future period becomes wrong **by the calendar, not by any change in the world**. The sentence was true when written and nothing touched the file. That is the same mechanism as "thirteen months" and the Navigator trial deadline, and it is the fourth instance of stale framing found today.

**So: any future period stated anywhere needs a review date attached.** Not only the ones attributed to a regulator.

**This belongs in tooling, not in a FACT trap, and the distinction matters.** A FACT trap is a bookmark of wordings we have been burned by, so its count is a floor. **A quarter or a year that has passed is mechanically detectable** — compute the end of the period, compare to today. There is no phrasing list to widen and no source to check. It has passed or it has not.

**`ua_volatile_check.py`, written 8 August 2026.** It answers one question: *does this page state a period as still ahead when the calendar has passed it?* It parses `Q2 2026`, `second half of 2026`, `H1 2026`, `June 2026`, `mid-2026` and bare years, computes the end, and requires future framing (`expected`, `due`, `set to`, `any week now`) with no past framing (`arrived`, `entered`, `since`) in the same sentence. **History is never flagged.** It also warns on `as of <period>` stamps older than 120 days, on periods ending within 90 days, and on elapsed counters such as "thirteen months".

```bash
python3 ua_volatile_check.py .            # today
python3 ua_volatile_check.py . --today 2027-01-04   # see what goes stale
python3 ua_volatile_check.py --selftest   # 8 fixtures, including the real one
```

**It found a second instance on its first run**, on `bfsg-germany-accessibility-compliance.html`, the country page. The same "expected in Q2 2026" sentence that had just been deleted from the insights page. Both now gone. Root reports 0 failures and 3 warnings, insights 0 and 0.

**What it cannot do, and this is in its own output:** it cannot tell whether a future claim is TRUE, cannot resolve "soon" or "in the coming months", and does not recompute elapsed counters.

### PRECISION IS A WRITING RULE, NOT ONLY A CHECKING ONE

**The one ACM claim that survived was the most precisely worded one.** Stated sample, stated failure mode, stated figure: approximately 100 of the largest Dutch webshops, ordering impossible with assistive technology, 61%. **Every claim that failed was loosely worded**, and the looseness is what let it drift from a source it never had.

**A precisely worded claim is harder to fabricate, because the precision has to come from somewhere.** "The ACM has been explicit that non-reporting organisations will be audited first" names no document, no date and no number, and it cost nothing to write. **Vagueness is not caution. It is where invented claims hide.**

**Write the sample, the date, the figure and the source into the sentence.** If they cannot be written, the claim is not ready.

#### 🔴 BUT PRECISION IS NOT EVIDENCE, AND THIS SECTION HAS ALREADY BEEN MISREAD ONCE
**Added 15 August 2026, after this section produced exactly the wrong inference.** Asked whether an unverified enforcement claim on the Norway passage should be trusted, a session reasoned that it was "precisely worded, which by the register's own ratio is a good sign." **That is a misreading of this section and it needs saying here rather than being left to be repeated.**

**The ratio above was measured on claims that had already been checked against source.** Precision predicted which of the nine ACM claims survived checking. **It says nothing about a claim nobody has checked yet.**

**An unverified precise figure is not the safe shape. It is the more dangerous one**, because it carries every signal of having a source and none of the fact. **That is what the invented complaint procedure looked like** before anyone went looking: stated actor, stated sequence, stated document, and no publication behind any of it. See JOB 0o.

**So the rule is a writing rule, exactly as the heading says.** Precision is what you owe a reader when you have a source. **It is never the reason to believe a sentence, and a precise claim with no entry in the facts file is a claim with no source, not a well-made one.**

### THE PREDICTION RULE IMMEDIATELY CAUGHT ONE OUTSIDE THE NETHERLANDS
A sweep for any future period attributed to a regulator found one more, on `insights/bfsg-germany-enforcement-abmahnungen.html`: *"formal enforcement decisions are expected in Q2 2026, which means they could arrive any week now."*

**It had also gone stale.** Q2 2026 ended in June and today is 8 August, so the page was telling a reader that a passed quarter is imminent. **A predicted timeline does not merely fail to be sourceable. It rots on a known date and nothing on the site was watching.** Deleted.

**The MLBF January 2026 claim, checked 8 August 2026: a third verdict, and it is not "fails".** It is on both German pages: *"The market surveillance authority (MLBF) entered its active enforcement phase in January 2026."*

- **The MLBF's own site does not date it.** Neither the [homepage](https://www.mlbf-barrierefrei.de/) nor the [Marktüberwachungsstrategien page](https://www.mlbf-barrierefrei.de/Markt%C3%BCberwachungsstrategien) gives a date for the strategies or for an enforcement phase.
- **Several independent German sources do**, agreeing that the MLBF adopted its market surveillance strategies on 29 January 2026 and has been in the active control phase since.
- **Nothing contradicts it.** That is the difference from the ACM claims, where the regulator published the opposite basis.

**So it is unverified against primary, corroborated in secondary, and uncontradicted. Left in place.** Recording the three verdicts as distinct matters more than the individual call: **contradicted by source** (delete), **unsourceable in principle** (delete, and never attribute), **undated by the source but corroborated elsewhere** (ordinary sourcing, keep and note).

**What the MLBF does publish is worth using**, and it echoes the ACM: *"Wir fokussieren uns dort, wo der Handlungsbedarf am größten ist"*, with consumer submissions, risk assessment, technological change and emerging trends as the indicators. **Two authorities, in two countries, both selecting by need and impact.** Neither selects by who filed a report.

### THE RATIO IS THE ARGUMENT FOR CHECKING
**Nine ACM claims checked. Eight wrong, one right.** The one that held is the 61%, and it held because it was precisely worded: a stated sample size, a stated failure mode, a stated figure. **Every claim that failed was loosely worded**, and the looseness is what let it drift from a source it never had.

**Read that ratio as the case for checking, not against it.** Eight of nine were removable in an afternoon against four public URLs.

**Done 8 August 2026.** The two unsupported sentences deleted and the sourced replacement approved and live:
> If you have not yet reported to the ACM, this is urgent. Failure to report does not make an organisation invisible to enforcement. The ACM inspects on its own initiative. It began with the largest companies by customer numbers, and its published focus for the first period is the problems with the most impact on disabled users.

**It replaces a claim that told a small company the wrong thing.** "Non-reporters get audited first" reads as safety to anyone small. Largest companies and biggest user impact is the truth about where attention has gone, and a reader can check it.

### IT WAS ON FOUR PAGES IN FIVE WORDINGS, NOT ON ONE
**The first search found one sentence. Two further rounds found eight, and the page it was "about" held only four of them.**

| Round | Where | Wording |
|---|---|---|
| 1 | `eaa-compliance-netherlands.html` callout | "The ACM has been explicit that non-reporting organisations will be audited first" |
| 2 | same page, lines 160, 204 **and JSON-LD line 72** | "have moved to the front of the ACM('s) audit queue" |
| 3 | `eaa-compliance-ecommerce.html` | "Failure to report puts an organisation at the front of the audit queue" |
| 3 | `eaa-compliance-ecommerce.html` | "prioritising organisations that did not self-report by the October 2025 deadline" |
| 3 | `eaa-fines-penalties-ireland-netherlands-sweden.html` | "conducting active audits of organisations that failed to report" |
| 3 | `eaa-fines-penalties-ireland-netherlands-sweden.html` | "prioritising organisations that did not self-report" |
| 3 | `eaa-fines-penalties-ireland-netherlands-sweden.html` | "Failure to report, or submitting an incomplete report, prioritises an organisation for audit" |
| 3 | `insights.html` card excerpt | "Non-reporters have been moved to the front of the audit queue" |

All deleted. Round 4 found nothing. **The "ACM is moving toward formal sanctions in the second half of 2026" half of two sentences was kept**, because that is a separate claim and it is in the not-yet-checked list above.

**Every lesson from JOB 0o reappeared here, on a defect of a different class.** One deletion round is never enough. The rewording travels within a single page as readily as across pages. The JSON-LD carried a copy. **And scoping by filename would have found four of eight**, because a claim about the ACM lives on the e-commerce and fines pages too.

**A trap now covers all five wordings** (`ua_page_check.py`, JOB 0q). **It is a bookmark of the five we know**, exactly as JOB 0p describes, so a green result means those five are absent and nothing more.

**The general rule this adds.** Rule 10 says do not state an unverified Dutch figure. **Extend it: do not state an unverified regulator *intention* either.** "The ACM has been explicit that" is a citation in the shape of a sentence, and it is checkable in ten minutes. **If a claim says a named regulator said something, either link what it said or do not attribute it.**

---

## JOB 0p — READ THE FACT TRAPS, DO NOT COUNT THEM — AUDITED 8 August 2026

### FINDING 1: THE TRAP SET IS A BOOKMARK OF KNOWN ERRORS, NOT A CHECK
Each trapped claim was reworded three ways. **18 of 22 paraphrases were missed.**

| Trap | Catches | Misses |
|---|---|---|
| `32%` | `32%` | "thirty-two per cent", "32 percent" |
| Carrefour damages | `€10,000` | "10.000 euro", "ten thousand euros in damages" |
| first EAA ruling | "first EAA ruling" | "the EU's first EAA judgment", "the first ruling under the Act" |
| a fine was issued | "was fined" | "a fine has been issued", "regulators have imposed fines" |
| 60 webshops | "60 webshops" | "sixty webshops", "60 online shops" |
| partial conformance | the exact sentence | "partial compliance is no defence in the EU" |

**This is not a reason to remove them.** It changes what a passing trap set means. **A green FACT result says "none of the specific wordings we have already been burned by is present." It does not say the page is factually sound.** Do not report it as though it does.

### FINDING 2: A SOURCE CHECK MUST BE PER-MARKET OR NOT AT ALL
The proposed unsourced-ceiling trap was tested against the two Dutch ceilings it was designed to catch. **It caught one and missed the other.**

`eaa-compliance-italy.html` carried the €300,000 Dutch figure and **passed**, because the page cites "Decreto" for its own Stanca Law figures. **A citation for one market's numbers vouched for a different market's number sitting in the same paragraph.** That is not a bug to fix. It is a property of any page-scoped or paragraph-scoped source test, and it is exactly how the second ceiling survived.

Any future source check has to pair each figure with the market named nearest it and require a citation for **that** market. Not built.

### WHAT WAS BUILT
**1. The blindness fix, done first.** `strip_tags` now includes meta descriptions, `og:description`, JSON-LD, alt text and aria-label. Before this, **every trap was blind to all five**, which is why the €900,000 Dutch ceiling in a meta description and the JOB 0o procedure in an Ireland JSON-LD field were structurally uncatchable. Image URLs stay excluded so no noise enters. No count changed on the day, because those instances had already been cleaned by hand: this is regression-proofing, and it makes every future trap more effective.

**2. The EU-wide ranking trap.** Any claim that a market ranks highest or strictest in the EU is unsupportable by construction, so a pattern match is a complete test rather than an approximation. **Bounded comparisons are exempt** — "the sharpest regime of the three" compares three surveyed markets and is this file's own wording. Requires a penalty context and EU-wide scope. **1 hit, 0 false positives**, and the hit was a live defect: a second ranking in the `eaa-compliance-italy.html` deck, in different wording from the callout deleted earlier the same day. Now fixed; the trap reports 0.

### WHAT WAS NOT BUILT, AND WHY
**The unsourced-ceiling trap. Do not ship it in either form.** At sentence level it produced **50 hits, essentially all legitimate** — Ireland's €60,000 from S.I. 636/2023, Italy's Stanca table, France's per-offence model, and our own service prices. A 170-character window cannot see a citation in a table caption or an earlier paragraph. At page level it produced 1 flag but failed the Italy case above.

### THE LIMIT, WHICH IS THE POINT OF THIS JOB
**A trap can only catch a claim someone already knew was wrong.** Everything here reduces the surface. **None of it would have found either Dutch ceiling first.** Both were found by reading, and the second only while chasing the first. **The FACT set will never be complete, and saying so matters more than the number of traps in it.**

---

## JOB 0l — A SITEMAPPED PAGE THAT CANONICAL-DEFERS AND REDIRECTS AWAY — CLOSED 8 August 2026

**Resolved by deleting the page.** `insights/invisible-revenue-loss.html` carried three signals that did not agree: a sitemap entry, a canonical naming `/eaa-revenue-loss.html`, and a zero-delay meta refresh to the same URL.

**What was done, in order.** The sitemap entry went first (`7f22518`). Then the page itself, once it was confirmed that nothing linked to it: one inbound link remained, a related-links entry on `insights/aimac-deep-dive.html`, repointed to `/eaa-revenue-loss.html`. The link text, "Inaccessible design is invisible revenue loss", is that page's own title, so it needed no rewording.

**Why deletion rather than keeping the redirect.** Seven impressions in three months and zero clicks. The redirect was preserving almost nothing, and it was accumulating checker exemptions: it needed one for the OG block, and would have needed further ones for the missing back-to-top element and a 168-character description. **Each exemption is a rule someone has to understand later.** Three of them to keep a page nobody reaches is a bad trade.

**One exemption was kept**, because it is right in general rather than for this page: `ua_page_check.py` no longer requires an OG block on a page carrying a meta refresh. A redirect is not a social destination.

---

## JOB 0m — THE EM DASH COUNT MEASURES THE WRONG THING — DONE 8 August 2026

**Fixed. The count is now prose only.** `ua_page_check.py` reports, for example:
`ok  0 em dashes in prose (14 in file, 14 outside prose)`

**Excluded from the prose count:** everything outside `<main>`, `<style>`, `<script>` (which covers JSON-LD), HTML and CSS comments, `<title>`, every `<meta>`, headings `h1`-`h6`, label spans (`.section-label`, `.requirement-number`, `.article-tag`, `.insight-tag`, `.badge`) and related-link `<li><a>` titles. Those are the JOB 0n exceptions.

**Threshold lowered from 8 to 2**, matching what hard rule 4 actually asks for. It was set at 8 because the old count was inflated by exceptions.

**Effect:** six pages that reported as unfinished now report 0 in prose, because their only dashes were related-link titles and section labels. `eaa-compliance-fintech.html` went from reporting 10 to reporting 0 of 14. Root warnings fell from 69 to 58, insights from 27 to 23, with failures unchanged.

**Ten fixtures cover it**, including the case that matters most: a prose aside is still counted. Run them before changing the helper.

---

## JOB 0n — SENTENCE-CONSTRUCTION PASS ACROSS THE REST OF THE SITE

**`index.html` is done, in commit `c2d1f64`. Every other page still needs it.**

Apply the **HOW TO WRITE** section above to all 43 remaining pages. Same standard as `c2d1f64`.

### The standard
**Restructure, do not repunctuate.** Swapping a dash for a comma leaves the aside in place and misses the point. Where a dash holds a qualifying aside, split the sentence in two or drop the aside.

**Catch the "X, not Y" construction in the same pass.** It travels with the dash and is the same habit.

### The size of it, measured 8 August 2026
| | |
|---|---|
| Pages needing the pass | **43** |
| Em dashes in prose, inside `<main>` | **531** |
| "X, not Y" constructions | **178** |
| Pages at 3 or more prose dashes | **35** |
| Pages already at 2 or fewer | **8** |

Heaviest first: `eaa-compliance-checklist.html` (36), `insights.html` (34), `eaa-compliance-travel.html` (25), `insights/ai-paradox.html` (25), `eaa-enforcement.html` (24), `insights/france-eaa-civil-society-enforcement.html` (24).

**Those counts are prose only**, taken from text inside `<main>` with `<style>` and `<script>` removed. They will not match what `ua_page_check.py` reports until JOB 0m is done, because that count still includes comments, `<title>` and meta.

### EXCEPTIONS AND CONVERSIONS: CHECK EACH INSTANCE
1. **Card and article headings using a dash as a title separator.** `Sweden's PTS — proactive inspections` reads as a subtitle, not an aside. A colon is often better, but this is a judgement call per heading and never a mechanical replacement.
2. **The `<title>` brand separator.** `Usable Access — Clarity-first EAA Compliance`. Leave it.
3. **Any dash where the contrast genuinely earns its place**, meaning a reader would otherwise assume the opposite. From the `index.html` pass, `not a full audit and never a compliance certificate` and `tested by a person, not a scan` were both kept. Both correct a reasonable wrong assumption. `not because it resolves compliance, but because it tells you` was removed, because nobody assumed it resolved compliance.
4. **Term-and-definition labels in body copy: CONVERT THE DASH TO A COLON.** This is a conversion rule, **not an exemption.** The pattern is a label followed by its definition, rendered as a paragraph or list item rather than a real definition list: `<strong>Published accessibility statement</strong> &mdash; a public document describing...`, `<strong>Netherlands</strong> &mdash; the ACM enforces...`, `<strong>Track 1 &mdash; Regulatory enforcement.</strong>`. The dash is doing a separator's job, so the sentence does not need restructuring, but the character still goes. **Roughly 24 instances of the `<strong>Label</strong>` form across 8 pages, plus 13 country and track labels.**

   **Check the capitalisation after every colon, on every converted instance and not only the ones that look wrong.** Three cases, and they differ:
   - **Continuing prose: lowercase.** `Netherlands: the ACM enforces`, not `Netherlands: The ACM enforces`.
   - **Proper noun or acronym: keep the capital.** `Ireland: ComReg enforces`. A blanket lowercase pass would break exactly the instances where being wrong looks worst.
   - **A titled unit that ends in a full stop: keep the capital.** `Step 1: First contact.` and `Track 1: Regulatory enforcement.` The phrase after the colon is a heading in its own right, not the start of a clause.

   This is easy to miss because the word was correctly capitalised when it followed a dash. Run the sweep across every colon on the page, treat the output as a review flag rather than an automatic change, and keep the proper-noun list current. Names seen so far that a sweep will flag wrongly: Sanktionsavgift, Systembolaget, IKEA, H&M, Univ&eacute;, faire-face, Int&eacute;r&ecirc;t &agrave; Agir, F&eacute;d&eacute;ration, ApiDV, Droit Pluriel, Traficom, AgID, DGCCRF, ARCOM, Abmahnung, LOI.
5. **Metadata separators between two items of equal weight: LEAVE THE DASH.** `Published 11 Jun 2026 &mdash; Updated 30 Jun 2026`. This is not a label and its definition, so **a colon would misrepresent the relationship**, implying the update is a property of the publication date rather than a second fact of the same kind. Distinguish it from exception 4 by asking whether the two sides could swap without nonsense: with a label and definition they cannot, with two metadata items they can. **One instance, on `insights/france-eaa-civil-society-enforcement.html`.** Found 8 August 2026 when a conversion script wrongly rewrote it; reverted the same day.
6. **Card and preview copy: TITLES ONLY, not excerpts.** A card title such as `Accessibility statements &mdash; what a credible one contains` is a subtitle, and the dash belongs there. **The excerpt below it is ordinary prose and is in scope.** This exception was added on 8 August 2026 after a first pass stripped the card copy on `insights.html` wholesale; that was reverted. Two excerpt changes on `index.html` were kept, because both were genuine asides.

**Target is one or two per page, not zero.** A page that reaches zero has probably lost a dash that was working.

### Method
**One page at a time.** Do not run a scripted replacement across the site. The exceptions above need a judgement on each instance, and a find-and-replace cannot make one.

**Show the diff for the first three pages before continuing**, so the exception handling can be checked before it runs across the rest.

### Verify per page
`ua_page_check.py` and `ua_a11y_check.py`, and read the page top to bottom. Splitting a sentence changes the rhythm of the paragraph around it, and on `index.html` one connective had to be rewritten because its antecedent moved.
---

## JOB 0k — HOMEPAGE HERO: APPLY THE APPROVED DJ MERGE (content, NOT a judgement call)

**⚠ DO NOT REWRITE ANYTHING. This job is a paste, not an edit.**

**Background:** DJ Johnston reviewed the homepage hero and returned a rewrite. About half of it improves the page and half breaks standing rules — it claimed barriers are "illegal", said businesses are "about to be examined and fined" (**no company has been fined under any EAA transposition anywhere**), and closed on "don't be caught unawares".

**A merged version exists in `UA_Homepage_Hero_DJ_Merge_Brief.md`**, keeping his imagery and structure and removing the unsupportable claims.

### The job
1. **Read `UA_Homepage_Hero_DJ_Merge_Brief.md` in full**, including the "what cannot ship" section — it explains WHY, and the reasons matter more than the edit
2. **Replace the reframe section's opening in `index.html`** with the merged draft **exactly as written in the brief**
3. Leave the "Two ways to start" block, the services ladder and the CTA untouched
4. Verify with `ua_page_check.py` and `ua_a11y_check.py`

### Why this is a paste and not an authoring task
**The wording has been through voice review.** Every phrase in the merged draft is either DJ's, already on the site, or was chosen to avoid a specific rule breach. **Improving it independently will reintroduce the problems it was written to solve.**

If something in it reads wrong, **flag it and stop.** Do not fix it.

### Numbers to regenerate rather than trust
The draft says **twenty-eight journeys, twenty-two barriers**. **Do not use those. They are three revisions stale, and the draft predates two markets being in the sample.**

**`ua_study_export.py` does not exist and never has.** It is one of the five scripts in the missing-scripts table near the top of this file, so the old instruction here resolved to nothing. **The numbers come from a derivation against the tracker, which is in the Claude project and not in this repo.** Re-run it there whenever the frozen sample changes, rather than copying figures out of any document including this one.

**The query. Run it where the tracker is, which is the Claude project session, not this repo.**

```python
import openpyxl
from collections import Counter

w = openpyxl.load_workbook("UA_Global_Outreach_Tracker.xlsx")
sc = w["Site Checks (A)"]
hdr = [sc.cell(row=2, column=c).value for c in range(1, sc.max_column + 1)]
i = {h: k + 1 for k, h in enumerate(hdr) if h}

# latest row per code — a prospect may be crawled more than once
# counting both rows inflates the denominator
best = {}
for r in range(3, sc.max_row + 1):
    code = sc.cell(row=r, column=1).value
    if not code:
        continue
    d = str(sc.cell(row=r, column=i["Test date"]).value)[:10]
    if code not in best or d >= best[code][0]:
        best[code] = (d, {h: sc.cell(row=r, column=i[h]).value for h in i})

# "in-denominator" is the filter. Excluded journeys still sit in the sheet,
# so the denominator is never the row count.
den = [r for c, (d, r) in best.items()
       if str(r.get("Exclusion type", "")).startswith("in-denominator")]

# blocked is derived from the stage field, not from a boolean column.
# "n-a-no-block" is the clean value.
def blocked(r):
    s = str(r.get("Stage of first block", "")).lower()
    return s not in ("n-a-no-block", "", "none", "n/a", "nan")

print("TOTAL:", len(den), "journeys |", sum(1 for r in den if blocked(r)), "blocked")

mk = Counter()
for r in den:
    m = str(r.get("Market", ""))
    m = "Ireland" if m.startswith("Ire") else ("Netherlands" if "ether" in m else m[:12])
    mk[(m, blocked(r))] += 1
for m in ["Ireland", "Netherlands"]:
    print(f"{m}: {mk[(m,True)]+mk[(m,False)]} journeys, {mk[(m,True)]} blocked")

print("STAGE:", Counter(str(r.get("Stage of first block")) for r in den))
print("BARRIER TYPE:", Counter(str(r.get("Barrier type")) for r in den if blocked(r)))
print("CAUSE:", Counter(str(r.get("Cause of failure")) for r in den if blocked(r)))
```

**The three steps that are not obvious are commented in the code, and all three change the answer if dropped.** Counting every row rather than the latest per code inflates the denominator. Taking the row count rather than filtering on `in-denominator` counts journeys that were excluded on purpose. And `blocked` has no boolean to read, so it is derived from the stage field against the clean value `n-a-no-block`.

**As of 19 August 2026 it returns:**

| Axis | Values | Denominator |
|---|---|---|
| Headline | 58 journeys, 40 blocked, 17 clean | all 58 |
| Market | Ireland 31 journeys, 24 blocked. Netherlands 27, 16 | all 58 |
| Where it stopped | selecting 37, entry 2, checkout 1, no block 17 | all 58 |
| Barrier type | labelling 14, name-role-value 13, keyboard-operability 10, focus-trap 1, other 2 | the 40 blocked |
| Cause | custom-control substitution 16, native not labelled 17, other implementation 7 | the 40 blocked |

**The previous derivation, 15 August 2026, read 41 blocked and Ireland 25.** P-12 was retracted on 19 August and the site was corrected the same day. **Read the 15 August figures as superseded, not as a second measurement**, and take this table rather than any figure quoted in prose elsewhere in this file.

### 40 AND 17 DO NOT SUM TO 58, AND THAT IS THE CORRECT STATE
**P-12 leaves the blocked count without joining the clean one.** It was retracted rather than re-run end to end, so it is in the denominator as tested and in neither bucket. **A retraction is not a pass.** The evidence never met the bar: a component fingerprint was read as sufficient with no `.focus()` test, which is the tooling-summary failure this study already records six of.

**One journey came out of exactly one cell on each axis**, which is why only four cells moved. It was a loan-amount slider, so it leaves **selecting** on the stage axis, **custom-control substitution** on cause, and **keyboard-operability** on type. **Ireland loses it, the Netherlands does not.** Any future retraction moves the same four axes and has to be worked through one at a time, because no axis can be inferred from another.

**The site does not state 40 and 17 adjacently**, so nothing reads as contradictory today. **A reader can still subtract**, and there is no line on any page explaining the gap. Worth writing when the study is next written up.

**Barrier type and cause are different axes and must not be read across.** Type is *what* fails, cause is *why*. Reading `labelling 14` as the native-not-labelled cause would say the cause split is 14 against 26 and prompt a correction to the site's "split roughly evenly" wording. **The cause split is 16 and 17, so that wording is right and is now almost exactly even.** This is the neighbouring-question failure from the table at the top of this file, and it is available here on a plate: two axes, similar vocabulary, and an inference that looks sound.

**But the homepage says more than "roughly evenly", and the retraction has caught it.** `index.html` reads "The cause was usually a standard control replaced by a custom one", which was defensible at 17 against 17 and is now the smaller of the two at **16 against 17**. **It is a word, not a figure, so no count will ever flag it.** Flagged 19 August 2026 and left for a copy decision. `how-we-test.html` says "split roughly evenly" and needs nothing.

**They come from two different columns and they carve the same 40 into different shapes**, five buckets by type and three by cause, so no bucket in one corresponds to a bucket in the other. `Barrier type` and `Cause of failure` are separate fields in the sheet, which is the thing to check before quoting either. **The totals matching is what makes the mistake easy**, because a figure from the wrong axis still adds up.

**The entry-stage pair is named as an exception rather than folded in**, because the location claim is that barriers cluster mid-journey and two of fifty-eight is a genuine tail.

**"Thirteen months" is elapsed and rots by the calendar.** Fourteen months as of August 2026. `ua_volatile_check.py` flags the shape of an elapsed counter and **never its value**, so a wrong month count and a right one produce identical output. **Nothing anywhere confirms an elapsed counter is currently true.** Recompute it by hand against June 2025. See JOB 0v.

### After
**Read the whole homepage top to bottom.** The hero, the reframe, the ladder and the CTA have to read as one argument, and edits to one section have twice left another stranded.


---

## 🔴 JOB 0v — THE GATE MUST NOT BE BUILT ON THE FIVE SUMMARY INTEGERS

**Written 15 August 2026, from a capability test rather than from reasoning.** The four checkers had never been shown capable of returning anything other than their expected numbers, so a deliberate defect of each class was pushed against a throwaway copy of the working tree and each checker was watched to see whether it went red.

**All four can fail.** Three went red on a first-attempt realistic defect. What the test found is not that the checkers are broken. It is that **three real defect classes are invisible to the summary line the gate was going to be built on.**

### THE RESULT
Baseline: `ua_page_check` 3 failures at root and 0 in insights, `ua_a11y_check` 0 failures across 44 pages, `ua_orphan_check` 0 orphans and 0 unresolved, `ua_volatile_check` 0 failures.

| Injected defect | Checker | Verdict |
|---|---|---|
| Skip-link target removed (`id="main"` deleted) | a11y | **RED**, 0 to 1 failure, and `ua_page_check` moved 3 to 4 |
| Body-copy link to a page that does not exist | orphan | **RED**, unresolved 0 to 1 |
| Stale future period, "Q2 2026 ... any week now" | volatile | **RED**, 0 to 1 failure |
| Three em dashes in prose | page | **Warn only.** 57 to 58 warnings, failures unmoved |
| Sitemap entry for a file that does not exist | orphan | **Reported and uncounted** |
| Elapsed counter changed from fourteen months to three | volatile | **Shape flagged, value not** |

### 1. PARSE SECTION HEADINGS AND PER-PAGE LINES, NEVER THE FIVE INTEGERS
**The reason is that the harness built to test this was itself summary-blind.** It read only the summary lines, so it reported two of the six defects as "not detected" when both were reported plainly in the output body. **The tool testing for summary-blindness had the defect it was testing for**, which is the easier-question failure inside the check written to catch it. It is the third instance of that shape in one session, after a stray-text sweep that flagged 176 HTML comments and a close script that was correct but partial.

**So the gate reads the output body.** A count is a summary of what a checker chose to count, and what it chose to count is not the same set as what it found.

### 2. PROMOTE `IN SITEMAP BUT NOT IN THE REPO` INTO THE ORPHAN COUNT
**Highest-value single change in this job.** `ua_orphan_check.py` detects a sitemap entry pointing at a file that is not in the repo, and prints it under its own heading naming hard rule 14. **It does not appear in `0 orphans | 6 under-linked | 0 unresolved`.**

**A gate on those integers would pass the exact defect hard rule 14 exists for, and that defect has shipped here before.** Two sitemap entries once pointed at pages that were never built, and the homepage linked to both. See JOB 4.

### 3. HARD RULE 4 CANNOT FAIL A BUILD, BY CONSTRUCTION
The em-dash check calls `warns.append`, never `fails.append`. Three em dashes in a prose paragraph moved the warning count and left the failure count untouched. **A rule that cannot fail a build is not a rule.** Decide whether hard rule 4 is enforced or advisory, and make the code say which. Do not leave it looking enforced.

### 4. THE ELAPSED COUNTER FLAGS SHAPE AND NEVER VALUE
`ua_volatile_check.py` warns that an elapsed count needs a review date. **"Fourteen months on" and "Three months on" produce byte-identical output**, so the warning fires whether the number is right or wrong and cannot separate them. That is documented scope rather than a bug, and it means **no check anywhere confirms an elapsed counter is currently true.**

**A number that does not move when the thing it describes has changed is measuring something else.** The gate should treat this warning as a prompt to read, not as coverage.

### THE HARNESS
`scratchpad/captest.py` against a copy of the working tree. Copying rather than branching was deliberate, because the work under test was uncommitted. **Rebuild it to parse the output body before extending it**, since its summary-reading is the thing this job exists to fix.
