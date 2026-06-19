# Bundled attribution data

This folder holds **accumulated knowledge that the skill reads as a starting point and
the LLM extends in-session.** It is data, not a frozen authority. The whole reason the
skill is lean (mechanical scripts) plus this data (judgment), rather than one big baked
pipeline, is so attribution can grow without rewriting code. See the parent `SKILL.md`.

## `directors.json`

Film → director attribution for Letterboxd ingest, carried over from the original
hand-built run (209 directors, ~410 films).

- `directors`: `{ "Director Name": ["Film Title (YYYY)", ...] }`
- `tv_or_nonfeature`: titles that are TV / not feature films (skip director attribution)
- `uncertain`: titles whose director was never resolved

**How to use it:** when ingesting a new Letterboxd export, load this map, attribute the
films it already covers for free, and have the LLM resolve only the titles that aren't in
it yet. Then write the newly resolved titles back into `directors.json` so the next run
starts further ahead. New films are an LLM reasoning step, not a script step.

Books need no equivalent file: author lives in each Goodreads card's frontmatter already.

## What does **not** live here

Cover caches (`covers.json` and the like) are working files, not skill assets, because
they go stale (covers re-fetch, ratings change). Keep them in a working dir. A warm cache
from a previous run is at `tools/media-log-digest/covers_films.json` in the repo if you
want to seed `fetch_covers.py` instead of re-fetching from scratch.
