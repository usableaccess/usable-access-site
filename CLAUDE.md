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
16. **Every page needs:** canonical, full OG + Twitter block, GA4, Clarity, `tokens.css?v=1` + `site.css?v=2`, skip link, back-to-top, footer with the accessibility statement **and** privacy notice links.

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

**Two things to do:**
- **Consolidate.** Move the shared vocabulary into `site.css`, keep only genuinely page-specific rules inline, and link `site.css` from every page. Verify nothing regresses visually before deleting the inline duplicates.
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

## JOB 0j — THREE UNDER-LINKED PAGES NEED BODY-COPY INBOUND LINKS

**Found by `ua_orphan_check.py` on 7 August 2026.** Three pages have one or two inbound links, and in two cases the only link is from `insights.html` — a listing page, which carries far less weight than a link inside an argument.

| Page | Inbound now | Linked only from |
|---|---|---|
| `eaa-compliance-telecoms.html` | 2 | `does-the-eaa-apply.html`, `insights.html` |
| `insights/eaa-video-accessibility.html` | 1 | `insights.html` |
| `insights/eu-ai-act-accessibility.html` | 1 | `insights.html` |

**Target: three to six inbound each, with at least two in body copy.** Per `UA_Publishing_Protocol.md`.

### The rule that governs this — do not link from everywhere
**Choose by where the reader is in the journey, not by topic similarity.** A link that arrives at the wrong moment is ignored, and enough of them teach the reader our links are not worth following.

### Suggested targets, to be confirmed against the live pages

**`eaa-compliance-telecoms.html`** — the reader is a telecoms operator working out what applies to them.
- `eaa-compliance-ireland.html` — where sectors and their authorities are discussed. **ComReg is correct on this page only**, so it is the natural place to say "telecoms is the one sector ComReg handles" and link across
- `eaa-enforcement.html` — where authorities by market are covered
- `eaa-accessibility-statement.html` — telecoms statements carry the Real Time Text and third-party nomination requirements, which no other sector has

**`insights/eaa-video-accessibility.html`** — the reader has video in a consumer journey.
- `eaa-compliance-ecommerce.html` — product video is common in retail
- `eaa-compliance-travel.html` — destination and property video
- `wcag-em-2.html` or the audit guide — where evaluation scope is discussed and video is a scope question people miss

**`insights/eu-ai-act-accessibility.html`** — the reader is deploying AI in a consumer journey.
- `ai-paradox.html` — **the strongest candidate.** Same subject area, already argues about AI and accessibility, and the AI Act phasing is directly relevant to its argument
- `eaa-governance.html` — governance obligations overlap
- `aimac-deep-dive.html` — AI and accessibility measurement

### How to write the links
**Body copy, inside a sentence, where the argument naturally reaches for it.** Written so it makes sense to someone who never clicks. Not a Related-list entry — those are cheaper and weaker, and two of these pages already have one.

### Also fix while in there
**`ua_orphan_check.py` flags `index.html` as under-linked. That is a false positive.** The homepage is linked from the global nav on every page and is the target of every external link — it is the most-linked page on the site. **Add an exception excluding `index.html` from the under-linked report, with a comment explaining why.**

**`privacy.html` and `accessibility-statement.html` show as orphans. Also expected** — they are footer pages by design. Either exclude them or mark them as a known-acceptable category rather than an error.

### Verify
Re-run `python3 ua_orphan_check.py .` **against the full repo, not the working folder** — the working folder produces 88 unresolved links because most of the site is not in it.
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
The draft says **twenty-eight journeys, twenty-two barriers**. **These have moved twice this month.** Run `python3 ua_study_export.py` and use its output. Same for "thirteen months" — correct as of August 2026, and watched by `ua_volatile_check.py`.

### After
**Read the whole homepage top to bottom.** The hero, the reframe, the ladder and the CTA have to read as one argument, and edits to one section have twice left another stranded.

