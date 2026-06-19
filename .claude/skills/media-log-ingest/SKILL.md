---
name: media-log-ingest
description: Ingest a structured media-log export (Goodreads books, Letterboxd films, Kindle highlights) into the wiki as aggregate source/entity pages. Triggers on "ingest the Goodreads/Letterboxd/Kindle export", a drop under raw/media_logs/ or inbox/ that is an item-card export, or a request to (re)generate the aggregate film/book pages. Packages the mechanical stages (parse, cover-fetch) as scripts; attribution and page-writing stay LLM-in-the-loop. Do NOT use for single-source article/paper/transcript ingest (that is /wiki-ingest).
---

# media-log-ingest

Turn a bulk media-log export into wiki pages. Media-log exports are different from ordinary
sources: hundreds of tiny item cards, not one document. Per CLAUDE.md §B.3 ("Media logs and
intent lists") the vault prefers **aggregate** source/synthesis pages over one wiki page per
book or film, and treats statuses as epistemic layers (`read`/`watched` = experience data;
`to-read`/watchlist = possibility data; `currently-reading` = provisional).

This skill is **lean by design**: the mechanical, generic stages are scripts you run; the
judgment-heavy stages (attribution, which entities get pages, prose) are done in-session by
the model. Accumulated attribution lives as data the model reads and extends, not as frozen
code (see `data/README.md`). Rationale for the split is in the project history; do not bake
attribution back into the scripts.

## When to use / not use

- **Use** for `raw/media_logs/**` exports: Goodreads books, Letterboxd films, Kindle highlights.
- **Do not use** for a single article/paper/transcript: that is `/wiki-ingest`.
- The `read`/`watched` vs `to-read`/watchlist distinction is load-bearing. Never let possibility
  data support claims about taste, knowledge, or influence (§B.3).

## Layout

```
.claude/skills/media-log-ingest/
  SKILL.md            <- this file
  scripts/
    parse.py          <- stage 1: item cards -> aggregate JSON (mechanical)
    fetch_covers.py   <- stage 4: Wikipedia cover thumbnails, cached (mechanical)
  data/
    directors.json    <- accumulated film->director attribution (LLM reads + extends)
    README.md
```

Original one-shot scripts and a warm cover cache are archived at `tools/media-log-digest/`
(reference only; the canonical scripts are the two above).

## Running the scripts (Windows note)

Both scripts take `--vault` (defaults to `$CLAUDE_PROJECT_DIR`, then cwd). On Windows, prefix
runs with `PYTHONIOENCODING=utf-8` so console prints don't mangle Norwegian characters. The
output files are always written as UTF-8 regardless; the prefix only fixes terminal display.
Use a working dir like `work/` for intermediate JSON; it is not a vault asset, do not commit it.

## Workflow

### Stage 1 — Triage (LLM, only if the export is still in inbox/)

Plugin-synced roots (e.g. `raw/Snipd/`) skip triage. For a fresh export sitting in `inbox/`:
route the item cards into `raw/media_logs/<export-name>/`, preserving the import filenames
(§B.3: the folder is the canonical raw unit, not each item file). Kindle highlights need title
cleaning (strip edition/marketing subtitles) before they land; see the archived `triage_kindle.py`
for the original heuristic, but route deliberately rather than trusting it blindly.

### Stage 2 — Parse (script)

```
PYTHONIOENCODING=utf-8 python .claude/skills/media-log-ingest/scripts/parse.py \
  --subdir media_logs/letterboxd_films --out work/films.json
PYTHONIOENCODING=utf-8 python .claude/skills/media-log-ingest/scripts/parse.py \
  --subdir media_logs/goodreads_books   --out work/books.json
```

Emits a flat JSON list per export: every frontmatter field plus the first cover image and
outbound link from each card. Pure mechanical, no judgment.

### Stage 3 — Attribute (LLM, reads + extends data)

Books need no attribution step: author is already in each card's frontmatter.

Films do. Load `data/directors.json`, attribute every film it already covers for free, and
resolve **only** the titles not yet in it (and not in `tv_or_nonfeature` / `uncertain`). New
films are a reasoning step, not a script step. **Write newly resolved titles back into
`directors.json`** so the next run starts further ahead. Flag genuinely uncertain ones rather
than guessing.

### Stage 4 — Fetch covers (script)

```
PYTHONIOENCODING=utf-8 python .claude/skills/media-log-ingest/scripts/fetch_covers.py \
  --in work/films.json --out work/covers.json --suffix film
```

Threaded, incremental, safe to re-run. Seed `--out` with `tools/media-log-digest/covers_films.json`
to reuse the warm cache instead of re-fetching ~400 covers. Covers can also come from card
frontmatter (Goodreads cards already carry a `cover` URL from stage 1); prefer those when present.

### Stage 5 — Generate pages (LLM)

Write **aggregate** pages, not one page per item:

- **Aggregate source page** per export (e.g. `wiki/sources/Letterboxd export.md`,
  `wiki/sources/Goodreads-bibliotek.md`): the export as a single `kind: source`, with
  `source_path:` listing the `raw/media_logs/<export>/` folder, ratings tables, top items,
  status breakdown. Honor the experience/possibility/provisional layers.
- **Entity pages** for directors/authors that clear the bar (multi-work, or a standout single
  work worth a hub) per the normal §B.3 + §B.5 "lean toward a page when in doubt" judgment.
  Use the attribution from stage 3 and covers from stage 4 in the infobox.
- **Index + tag entries** per §B.3. Insert into `wiki/index.md` under the right sections; do
  not regenerate the whole index.

All pages follow the standard frontmatter (§B.3), the four-bucket writing standard
(`meta/vaultos-lang-no.md`), and the infobox rule. The PostToolUse frontmatter hook will
bump `updated:` and flag missing fields as you write.

## Scope discipline

Touch only pages this export is genuinely relevant to (§B.5). No drive-by edits to unrelated
wiki content. For a large export (hundreds of new pages would be unusual; aggregate pages keep
it small), present the plan-before-run paragraph first per §B.4.0.
