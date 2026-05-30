# VaultOS manifest — the package boundary

> **Not a wiki page.** This file is the single source of truth for what counts as *portable VaultOS* versus *this instance's content*. It drives generation of the distributable template (`wiki-llm-clean`). Regenerating the template = "copy what this manifest lists, apply the neutralisation rules, exclude everything else." Keep this file in sync when the schema or skills evolve.

## Why this exists

In a live vault, portable system files and instance content are interleaved in the same folders (`CLAUDE.md` next to `handoff.md`; `meta/` schema-docs next to handovers; `wiki/` structure-pages next to content). You cannot separate them physically without breaking Obsidian. This manifest formalises the boundary so template generation is **mechanical and repeatable**, not hand-picked.

## Build procedure

1. Create a staging directory **outside** the live vault (the live vault is never mutated).
2. Copy every path under **INCLUDE (verbatim)** as-is.
3. Copy every path under **INCLUDE (neutralised)** and apply its rule.
4. Create every file under **GENERATE / STUB**.
5. Add `.gitkeep` to the empty structural folders.
6. `git init` in staging → commit → push to the private `wiki-llm-clean` repo.
7. Everything under **EXCLUDE** never leaves the live vault.

The live vault stays on `obsidian-vault-2.0`; the template is a separate private repo. Build is purely additive — zero risk to this vault.

---

## INCLUDE (verbatim)

Copied unchanged — these are pure portable VaultOS.

- `AGENTS.md`
- `.gitattributes`
- `.claude/skills/wiki-ingest/`
- `.claude/skills/wiki-lint/`
- `.claude/skills/wiki-query/`
- `.claude/skills/wiki-synthesis/`
- `meta/handoff-protocol.md`
- `meta/synthesis-generation-recipe.md`
- `meta/LLM Wiki - Karpathy.md`        ← Karpathy pattern doc (foundation/context)
- `meta/vaultos-lang-no.md`            ← Norwegian language pack = worked example; wizard generates `vaultos-lang-<xx>.md` for other languages from this pattern
- `meta/vaultos-manifest.md`           ← this file (so recipients can understand/regenerate the boundary)
- `.obsidian/snippets/`                ← rendering DNA (infobox/home-grid/figures); recipients have no shared Obsidian Sync, so the template MUST carry these

### Karpathy seed (the single example across all layers)

- `raw/articles/2026-05-22_llm_wiki_karpathy.md`
- `raw/assets/speakers/andrej-karpathy.jpg`   ← only if referenced by the entity infobox
- `wiki/sources/Karpathy - LLM Wiki.md`

## INCLUDE (neutralised)

Copied, then edited per rule. **Edits happen in the staging copy only — never in the live vault.**

- **`CLAUDE.md`**
  - §B.0: drop the `[[meta/plan]]` and dated `[[Lint - YYYY-MM-DD]]` pointers; **keep** the `[[Karpathy - LLM Wiki]]` pointer (origin for structural/schema decisions); keep the `handoff.md`/`todo.md` and `first-time.md` pointers.
  - §B.2 layout: rename the tree root label `Personal Notes 2/` → generic `<vault-root>/`.
  - Personal layer (§B.2 / §B.10 / §B.12): replace hard-coded `personal/` with a reference to the `vault-config` parameter (default name `personal`; the layer rules apply whatever it is named).
  - Plugin-sync roots (§B.2): keep the *concept*; drop the Snipd-specifics (they live in `vault-config`, which is reset).
  - Full instance-scan: neutralise any remaining instance-only mention.
- **`meta/vault-config.md`** — reset to template values:
  - Language, hovedtags, personal-layer folder name → wizard-filled placeholders.
  - Remove the Snipd plugin-sync-root block (instance).
  - Keep generic defaults: reserved Vault DNA names, source-type folders, model-id baseline.
- **`README.md`**
  - Generic title (drop `Personal Notes 2`).
  - Fix the dead `meta/plan.md` / `meta/backlog.md` links (those are excluded).
  - Keep: necessary/recommended plugin split, Web Clipper (desktop + iPhone), the four-operation descriptions.
  - Download-link in Quick start stays a placeholder until provided.
- **`.claude/skills/dikt-analyse-norsk/SKILL.md`**
  - Drop the `[[meta/ideas/SNL API integrasjon]]` wikilink (instance page).
  - Generalise the skeleton tags (`kultur`/`litteratur` → pointer to `wiki/tags.md`).
  - Fix the "§B.7-format" log reference (B.7 is Commits; the format is given inline).
  - Keep the Norwegian examples (Hardanger/Aasen/Vinje etc.) — illustrative, not vault-specific. Shipped always, clearly labelled "norsk lyrikk".
- **`wiki/entities/Andrej Karpathy.md`** — trim source-list/body to reference only the LLM Wiki seed; drop references to Karpathy sources not shipped.
- **`.gitignore`** — template variant: `.obsidian/*` + `!.obsidian/snippets/` (keep snippets, unlike the live vault); keep the `raw/` binary and `inbox/Clippings/` rules.

## GENERATE / STUB

Created fresh in the template.

- **`first-time.md`** — the onboarding wizard (replaces the live vault's checklist). Language-agnostic; runs **as a tracked task** (seeds `todo.md`/`handoff.md`, checks off, finishes by resetting them + "safe to delete"). Asks: wiki-language (functional, first/foremost — drives all wiki prose + generated language pack) · meta-language (English default; optional cosmetic translation, "takes a bit longer, no practical effect on the wiki") · tone · purpose · solo/shared · standard categories · source types · personal layer? (+ custom folder name) · vault name (free text + suggestions) · vault license (suggestions: MIT / CC BY 4.0 / CC0 / All rights reserved) · interest in the third-party Tufte viz skill (→ points to [aref-vc/tufte-claude-skill](https://github.com/aref-vc/tufte-claude-skill) with attribution + install command, not bundled). Creates `home.md` from the chosen categories + Homepage-plugin install instruction. Closing branch: **use as-is** vs **make it your own** (co-develop schema/skills/conventions with the agent). Deletable when done.
- **`wiki/log.md`** — header only.
- **`wiki/index.md`** — seed listing only the Karpathy source.
- **`wiki/overview.md`** — empty placeholder.
- **`wiki/tags.md`** — reset to template hovedtags (wizard fills).
- **`wiki/home.md`** — commented skeleton the wizard fills (not generated from scratch).
- **`handoff.md`** / **`todo.md`** — `No ongoing task.`
- **`.claude/settings.json`** — empty `{}` (no platform assumption).
- **`.gitkeep`** in: `inbox/`, `wiki/concepts/`, `wiki/syntheses/`, `raw/papers/`, `raw/transcripts/`, `raw/media_logs/` (and any structural folder left empty after seeding).

## EXCLUDE

Never leaves the live vault — instance, personal, or session state.

- `personal/**` — health/finance/private (the wizard creates a fresh personal layer on demand if the recipient wants one).
- `ARCHITECTURE.md` — architecture working doc (instance).
- `meta/plan.md`, `meta/backlog.md` — this vault's history/deferred work.
- `meta/handovers/`, `meta/ideas/`, `meta/history/`, `meta/plan archive/`, `meta/telegram-mvp/`, `meta/feedback/` — session journals, working notes, idea drafts, architecture proposals. The durable patterns already live in `CLAUDE.md` + skills, so nothing of value is lost.
- `.claude/skills/tufte-claude-skill/` — third-party; offered via the wizard, not bundled.
- `.claude/settings.local.json` — already untracked (machine-local).
- All `wiki/**` content except the Karpathy seed + the structural stubs above.
- All `raw/**` content except the Karpathy LLM Wiki source (incl. `raw/Snipd/`, other Karpathy sources, all other articles/transcripts/media_logs/assets).
- `wiki/log.md` history (reset to stub).

## Two-license note

The **template repo itself** governs whether people may use VaultOS; the **recipient's vault** is licensed via the wizard. Current decision: keep `wiki-llm-clean` **private** and share access deliberately — this defers any license choice with no downside. Revisit if it ever goes public.

## Update model (future meta-vault phase)

Once an upstream VaultOS repo exists, established vaults receive patches through an **agent-mediated, user-curated `update` operation** — never a blind `git pull` / sync. Every file carries an update policy:

- **`core`** (refreshed by updates): `CLAUDE.md`, `.claude/skills/**`, `meta/handoff-protocol.md`, `meta/synthesis-generation-recipe.md`, `meta/LLM Wiki - Karpathy.md`, `meta/vaultos-manifest.md`, `.obsidian/snippets/`. The portable system that improves over time.
- **`seed`** (template-only — **never pulled** into an established vault, which already has its own real versions): `first-time.md`, the `wiki/{home,index,overview,tags,log}.md` stubs, the `handoff.md` / `todo.md` stubs, `.claude/settings.json`, `meta/vault-config.md`, `meta/backlog.md`, `.gitignore`, the `.gitkeep`s, and the Karpathy seed pages.
- **`instance`** (never in the template, never pulled): `wiki/**` content, `raw/**`, `personal/**`, and the *values* in `vault-config.md` / the chosen language pack.

**How the `update` skill behaves:** fetch the upstream `core`, show per-file diffs, and decide each change in dialogue — **adopt** (apply as-is), **adapt** (take as inspiration; modify to fit, including re-applying changes in the vault's meta language if it was translated), or **skip** (keep local). It touches only `core`; `seed` and `instance` are never overwritten. This is precisely why `first-time.md` (the onboarding wizard, a `seed` file) never returns to a vault that has finished setup.

**How updates are presented** (before any adopt/adapt/skip decision): the user sees a plain-language changelog, tiered by significance, not raw diffs —
- *Larger changes, additions, and new features* — explained in plain, non-technical prose (technical detail only if asked).
- *Small changes* — a short bullet list.
- *Bugfixes* — a brief, general "small fixes" overview, not itemised.

Raw diffs stay available on request; the default is the digested, readable summary.
