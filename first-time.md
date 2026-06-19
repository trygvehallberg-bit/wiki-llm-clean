# First-time setup

**You (the AI) are reading this because a human just opened a fresh VaultOS clone.** Greet them, give them the quick feature tour (Phase 1), then conduct the setup conversation **one step at a time**. Run it as a *tracked task* (Phase 0) so it's resumable and so the state layer is live from session one. When you finish, offer to delete this file — nothing depends on it; its absence is the normal steady state.

> [!important] Conduct this step by step. Do not dump.
> Ask **one** question at a time (or a tightly related pair), wait for the answer, reflect it back in a few words, then move to the next. **Never** paste the whole numbered list at once, and never ask everything in one message — that is the failure mode this note exists to prevent. The list in Phase 1 is *your* checklist, not a form to hand the user. Keep it conversational and human-paced.

> Minimal path: a human who wants nothing fancy can skip the wizard, drop a file in `inbox/`, and say `ingest`. But the wizard takes ~5 minutes and tailors the vault to them. Offer it; don't force it.

> [!note] For the human, if you opened this file yourself
> If your agent never mentioned this file or the VaultOS schema and you're reading it by hand to find out why — its working directory is almost certainly the **parent** folder, not the vault folder. `CLAUDE.md` only auto-loads when the vault folder *is* the working directory. `cd` into this folder and start the agent again.

## Phase 0 — Start the tracked task

- Write the phases below into `todo.md` as a checklist.
- Set `handoff.md` to "Onboarding in progress — see todo.md."
- Check items off as you go.

This bootstraps the state layer and demonstrates the loop at the same time. Rules: `meta/handoff-protocol.md`.

> [!note] Automation layer (Claude Code)
> This clone ships background hooks (`.claude/hooks/`: frontmatter-date bump, protected-file guard, non-Claude skill mirror), wired in `.claude/settings.json` and loaded at session start. They need `python` on the PATH; if it is missing they simply no-op and nothing breaks. Setup does not depend on them — just be aware they exist (e.g. if `updated:` dates stop bumping, that's a missing `python`).

## Phase 1 — Show what they've got, then ask (one step at a time)

**First, give a short, friendly tour** so they know what they're configuring. Present it cleanly (a few grouped lines, not a wall) — adapt the wording, but cover all of it:

> **What this vault does for you**
> - **The loop** — you drop sources in `inbox/`; the AI runs four operations: **ingest** (read a source, build/update wiki pages, cross-reference), **query** (answer questions with citations), **lint** (periodic health check), **synthesis** (connect sources into new pages).
> - **Three layers** — `raw/` (your frozen sources) → `wiki/` (the AI-maintained knowledge layer, the AI is its sole author) → the schema (`CLAUDE.md`, the rules). You read the wiki; the AI writes it.
> - **Specialized skills** (trigger on topic, not by name) — bulk media-log imports (Goodreads/Letterboxd/Kindle), analytical parables. Norwegian-only extras (poem analysis, a Norwegian prose reviewer) ship dormant and activate if you choose Norwegian.
> - **Helpers** — background hooks keep page metadata tidy; `tools/` has scripts (PDF→Markdown, image optimizer, a lint pre-pass).
> - **Language** — English out of the box; you can pick Norwegian or another language and the AI regenerates the language layer for you.
> - **It's your fork.** MIT-licensed. Anything below is a default you can change now or later; nothing here is locked.

**Then ask the questions below — ONE at a time, conversationally.** The first is the only functionally critical one; the rest have sensible defaults you can offer and move past quickly.

1. **Wiki language** — *functional; drives ALL wiki prose and the language pack.* Which language should the wiki be written in? (**English** (default) / Norwegian / other.)
2. **Meta language** — *cosmetic.* Keep the operational docs (CLAUDE.md, skills, meta) in English (recommended — the tested baseline), or translate them to the wiki language? Translation takes a while and has **no practical effect** on how the vault works; purely reading comfort.
3. **Tone** — how should wiki prose read? (Neutral/encyclopedic · Conversational · Academic-dense.)
4. **Purpose** — what is this vault for? (Personal knowledge · Research/field · Work domain · Mixed — free text welcome.)
5. **Solo or shared** — one user, or several colleagues dropping sources? (Sets the **collaboration mode** parameter in `meta/vault-config.md`; governs §B.6 dedup + multi-author handling. Default: solo.)
6. **Primary AI tool / canonical instruction file** — which tool will mostly drive this vault? **Claude Code** → keep `CLAUDE.md` canonical (default). **Codex or another tool that reads `AGENTS.md`** → make `AGENTS.md` canonical instead. The other file becomes a thin pointer. (Sets the **canonical instruction file** parameter; the swap happens in Phase 2.) If unsure, keep the default.
7. **Standard categories** — home-page cards + top-level tags. Offer the starter set in `wiki/tags.md`; let them edit/add.
8. **Source types** — what will they mostly feed? (articles / podcasts / papers / books.) Tunes triage defaults.
9. **Personal layer?** — want a private folder the wiki and agent never touch (health, finance, private notes)? Yes/No. If yes: what should it be called? (default `personal`.)
10. **Vault name** — what should this vault be called? (Free text; suggest something from their purpose/categories; fallback "VaultOS".)
11. **License** — how should the vault content be licensed? (MIT · CC BY 4.0 · CC0 · All rights reserved.) Skip if it stays private/personal.
12. **Tufte viz skill?** — interested in a third-party data-visualization skill? If yes, point them to [aref-vc/tufte-claude-skill](https://github.com/aref-vc/tufte-claude-skill) (credit the author) with its install command. It is **not** bundled here.

## Phase 2 — Apply the answers

- Write the answers into `meta/vault-config.md` (wiki language, collaboration mode, canonical instruction file, top-level tags, personal-folder name, vault name, source-type emphasis).
- **Set the collaboration mode (Q5)** to `solo` or `shared` in `meta/vault-config.md` → "Collaboration mode". No other file changes; §B.1/§B.6 read the parameter.
- **If they chose `AGENTS.md` as the canonical instruction file (Q6):** move the full schema body from `CLAUDE.md` into `AGENTS.md`, then replace `CLAUDE.md` with the pointer stub (the shipped `AGENTS.md`, with the two filenames swapped). Claude Code's `@import` resolves only in `CLAUDE.md`, so in the now-canonical `AGENTS.md` reference the parameter files (`meta/vault-config.md`, the language pack) by path rather than `@import`-ing them. The default (Claude Code → `CLAUDE.md` canonical) needs no change. Update `meta/vault-config.md` → "Canonical instruction file" either way.
- **Wiki-language prose layer.** The shipped default is English — the `meta/vaultos-lang-en.md` pack, the `prose-reviewer` subagent (`.claude/agents/`), and the schema's English section names (`## Key claims` etc.). Leave it if the wiki language stays English. If it differs:
  - **Norwegian:** swap the `@import`/reference to the shipped `meta/vaultos-lang-no.md`; the Norwegian `norsk-prosa` reviewer also ships, so just point §B.13 at it (you can leave `prose-reviewer.md` in place or remove it); then correct the schema's wiki-language references (below) and regenerate the seed (below) in Norwegian.
  - **Any other language:** generate `meta/vaultos-lang-<xx>.md` from the pattern in `meta/vaultos-lang-en.md` (section headings, infobox labels, and the mother-tongue idiom anti-patterns for that language); copy `.claude/agents/prose-reviewer.md` to `<xx>-prosa.md` and rewrite its language-specific idiom checks (the §A.6 patterns carry over verbatim); point the `@import` and §B.13 at the new files.
  - **Schema references to the wiki language:** correct the spots that name the wiki language so they point at the right pack/agent — the §B.1 wiki-language premise, the §A.6 language-specific parenthetical, the four-bucket names / "canonical names" / infobox-labels notes in §B.3, and the §B.13 prose-reviewer line. (If meta translation is off, just fix the language name; leave the surrounding English.)
- **Regenerate the Karpathy seed in the chosen language.** The shipped seed (`wiki/sources/Karpathy - LLM Wiki.md` + the `Andrej Karpathy` entity) is in English. If the wiki language differs, re-ingest `raw/articles/2026-05-22_llm_wiki_karpathy.md` into the chosen language, replacing those two pages — and let the user watch: it doubles as their first live `ingest` demo.
- Update `wiki/tags.md` (chosen top-level tags) and the `README.md` title (vault name).
- **If they chose meta translation:** translate CLAUDE.md, the skills, and the meta docs into the wiki language. Flag that this is the slower path.
- **If they want a personal layer:** create the folder under the chosen name with a short README explaining §B.10 (outside wiki ops; one-way `personal → wiki` linking only).
- Set the tone/purpose so it informs how you write wiki prose going forward.

## Phase 3 — Build the home page

- Fill `wiki/home.md` from its skeleton — one category card per chosen category.
- Tell them to install the **Homepage** community plugin and point it at `wiki/home.md` (see README → First-time setup), and to enable the CSS snippets (Settings → Appearance).

## Phase 4 — Close

Offer two paths:

- **Use it as-is** — "You're set. Drop a source in `inbox/` and say `ingest`."
- **Make it your own** — offer to walk them through the schema (CLAUDE.md §B.3), conventions, skills, tone, and categories, and co-develop their clone in dialogue. It's their fork: their language, their rules, their schema — change anything, now or later.

Also mention, briefly: **VaultOS updates are optional.** They can run the `update` operation anytime to pull improvements from upstream — curated, adopt/adapt/skip per change, never touching their content — or ignore updates forever; the vault works either way. Details in README → Updates. And if they'd rather not trigger ingest by hand, point them to README → Automating ingest (a scheduled routine).

Then set `todo.md` and `handoff.md` back to "No ongoing task" (note onboarding complete), and **offer to delete this `first-time.md`**.
