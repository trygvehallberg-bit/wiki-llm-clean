# VaultOS

A shared knowledge vault. You drop sources; the AI organizes everything else.

Built on Andrej Karpathy's [LLM Wiki pattern](meta/LLM%20Wiki%20-%20Karpathy.md): instead of asking the AI questions about a pile of documents, the AI incrementally builds and maintains a structured wiki between you and the raw sources. The wiki compounds with every source you add.

## First-time setup

**Fastest path:** open the vault in Claude Code (or Codex / Cowork) and say hello — it runs the `first-time.md` wizard and walks you through everything below interactively, then tailors the vault to you. Prefer to do it by hand? The steps:

1. **Open the folder as an Obsidian vault.** File → Open vault → select this folder.
2. **Trust the vault** when prompted (community plugins won't load otherwise).
3. **Install the community plugins.** Settings → Community plugins → Browse, then search and install each.

   *Necessary* — the vault's documented behavior depends on these:
   - **Homepage** — opens `wiki/home.md` as the vault home page.
   - **Style Settings** — UI toggles the CSS snippets rely on (infobox, home grid).
   - **Force note view mode by frontmatter** (`obsidian-view-mode-by-frontmatter`) — honors the `obsidianUIMode: preview` key on `home.md`.

   *Recommended* — quality-of-life, not load-bearing:
   - **Omnisearch** + **Embedded Omnisearch** (`embedded-omnisearch`) — full-text search and inline result blocks.
   - **Dataview** — query-driven views over frontmatter.
   - **Advanced Tables** (`table-editor-obsidian`) — Markdown table editing.
   - **Snipd** (`snipd-official`) — syncs podcast highlights into `raw/Snipd/`, if you ingest podcasts.
   - **Text to Speech** (`obsidian-tts`) — reads notes aloud.
   - **File Explorer Note Count** (`file-explorer-note-count`) — note counts per folder.
4. **Enable them** (Settings → Community plugins → toggle on) and **enable the CSS snippets** (Settings → Appearance → CSS snippets).
5. **Reload** (`Ctrl/Cmd+R`). `home.md` should open as the landing page.

All Obsidian config — plugin list, per-plugin settings, CSS snippets, theme, hotkeys — lives in **Obsidian Sync**, not git: git tracks only what Sync doesn't carry. Collaborators get it through the shared Sync vault, and this README is the fallback for a bare git clone. Optionally install **Obsidian Git** locally for an in-app git UI.

## Web Clipper

The [Obsidian Web Clipper](https://obsidian.md/clipper) saves web pages as Markdown straight into the vault, ready to `ingest`. Point it at the `inbox/Clippings/` folder — that path is gitignored, so raw clips stay local until triage routes them into `raw/`.

**Desktop browser** (Chrome, Edge, Brave, Arc, Firefox, Safari):
1. Install the **Obsidian Web Clipper** extension from your browser's extension store.
2. Open its settings → set the destination **vault** to this vault and the **folder** to `inbox/Clippings/`.
3. On any page, click the extension to clip it, then say `ingest` in Claude Code.

**iPhone / iPad** (Safari):
1. Install the **Obsidian** app and sign into **Obsidian Sync** so this vault is on the device.
2. Add the **Obsidian Web Clipper** Safari extension (App Store → search "Obsidian Web Clipper"), then enable it under Settings → Safari → Extensions.
3. In the extension settings, set the destination vault and the `inbox/Clippings/` folder.
4. While browsing, tap **aA** (or the share button) → **Web Clipper** to clip. It syncs via Obsidian Sync; ingest it later from Claude Code.

## Quick start

1. Drop a file (article, transcript, paper, image) into `inbox/`. Any filename, any format.
2. Open this folder in Claude Code.
3. Say **`ingest`**. The AI triages the file into `raw/` with a canonical name, then builds and links wiki pages from it. End-to-end, hands-off.

To find what's there afterward: open `wiki/home.md`, follow the category cards, or use Omnisearch (`Ctrl/Cmd+Shift+F`).

## Folder layout

```
inbox/    Drop new sources here. Any name, any format.
raw/      Archived sources, sorted by type. Frozen — don't edit.
wiki/     Agent-maintained knowledge layer.
  entities/    People, organizations, products, named things.
  concepts/    Ideas, techniques, themes.
  sources/     One page per ingested source.
  syntheses/   Analyses, comparisons, lint reports.
  index.md, log.md, overview.md, tags.md
meta/     Docs about this vault (design, backlog, source pattern).
```

**Graph view colors**: blue = entities, green = concepts, orange = sources, purple = syntheses, yellow = inbox, gray = raw/meta. For file explorer tints too, enable the CSS snippet under Settings → Appearance.

## What the AI does

| Operation | What it does |
|---|---|
| **Triage** | Renames and routes files from `inbox/` into `raw/<type>/<YYYY-MM-DD>_<slug>.md`. |
| **Ingest** | Reads a source, creates/updates wiki pages, cross-references everything. |
| **Query** | Answers questions from the wiki, with citations. |
| **Lint** | Periodic health check — orphan pages, contradictions, stale claims, missing cross-references, tag proposals. |
| **Re-ingest** | Re-reads old sources with newer models; diffs against existing pages and surfaces what's new. |

You never write to `wiki/` directly. The AI is the sole author there. Humans only add to `inbox/` and ask questions.

## What you do

- Drop sources into `inbox/`.
- Say `ingest` (or `triage` first, if you want to inspect the routing before pages are built).
- Ask questions in chat.
- Periodically say `lint` — once a week is a reasonable cadence.
- Skim `wiki/log.md` to see what the AI has been up to.

## Where to dig deeper

- **`CLAUDE.md`** — the full operational schema. Auto-loaded by Claude Code; you can read it yourself to understand the rules.
- **`meta/vaultos-manifest.md`** — what counts as portable VaultOS vs instance content (the package boundary).
- **`meta/LLM Wiki - Karpathy.md`** — Karpathy's original pattern this vault implements.
- **`wiki/log.md`** — chronological record of every operation the AI has performed.

## Conventions in one breath

Wiki page names are natural-form English (`Ada Lovelace.md`, `Analytical engines.md`, `Lovelace - Analytical engines.md`). Raw files and tags use lowercase, underscore-separated slugs (`ada_lovelace`, `analytical_engines`). Sources prefix with `<Speaker/Author> -` so they don't collide with concept pages of the same name. Wikilinks use the natural form: `[[Ada Lovelace]]`, not `[[ada_lovelace]]`.

Callouts in source pages (`> [!quote]`, `> [!important]`, `> [!warning]`, etc.) are used sparingly — 2–5 per page max, only where they convey semantic type, not as decoration.

## Updates (optional)

This vault runs on **VaultOS** — a portable system layer (CLAUDE.md, the skills, the `meta/` schema docs) maintained in an upstream template repo. Keeping current with VaultOS is **entirely optional**:

- **Skip it.** Your vault works indefinitely without ever updating; your content and config are never touched.
- **Pull it.** Run the `update` operation whenever you like. The agent fetches the latest VaultOS core from upstream, shows a plain-language changelog — big changes explained in prose, small ones as bullets, bugfixes as a brief overview — and you decide each change: **adopt**, **adapt** (take as inspiration and tweak), or **skip**. It only ever touches the system core — never your wiki content, your config, or the onboarding wizard.

Maintainers *push* improvements to the upstream; vaults *pull* them — git is pull-based downstream, so nothing in your vault changes unless you run `update`.

**You're never obligated, and you don't take it wholesale.** `update` is a conversation with your AI tool, not a sync: walk the changelog together, pull in what fits, adapt what's close, skip the rest. Maintaining VaultOS is curating, not merging.

**Knowing an update exists:** git doesn't notify clones. Either run `update` (it checks the upstream when run), *Watch* the repo on GitHub for email on new commits (needs an account), or let a routine check periodically (below). **Pulling** a *private* upstream needs a GitHub account with access granted; a *public* upstream anyone can pull without one.

## Automating ingest (optional)

Prefer not to trigger ingest by hand? Set up a **routine** — a scheduled task in Codex, Claude Code, or Cowork — that runs `ingest` on a cadence (hourly, daily). In automated mode:

- It runs **non-interactively**: no plan-gate, no per-file questions. It works through `inbox/` one file at a time.
- Mind the **token budget**: cap each run, and have it **skip rather than process** anything oversized or ambiguous — leaving those in `inbox/` for you to review and trigger by hand. A sane default: skip single files over ~15k tokens (long transcripts, big exports) and stop after a handful of items per run; everything skipped stays in the inbox with a one-line note in `wiki/log.md`.
- Web clips (Web Clipper → `inbox/Clippings/`) are the ideal feed — small, steady, and they pile up without nagging you.
- A routine can pull double duty: have it also check the VaultOS upstream and tell you if an update exists. It won't apply anything — updates stay curated and on your terms.

