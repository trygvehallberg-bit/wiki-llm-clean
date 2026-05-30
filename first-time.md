# First-time setup

**You (the AI) are reading this because a human just opened a fresh VaultOS clone.** Greet them, then conduct the setup conversation below. Run it as a *tracked task* (Phase 0) so it's resumable and so the state layer is live from session one. When you finish, offer to delete this file — nothing depends on it; its absence is the normal steady state.

> Minimal path: a human who wants nothing fancy can skip the wizard, drop a file in `inbox/`, and say `ingest`. But the wizard takes ~5 minutes and tailors the vault to them.

## Phase 0 — Start the tracked task

- Write the phases below into `todo.md` as a checklist.
- Set `handoff.md` to "Onboarding in progress — see todo.md."
- Check items off as you go.

This bootstraps the state layer and demonstrates the loop at the same time. Rules: `meta/handoff-protocol.md`.

## Phase 1 — Ask the setup questions

Conversational, a few at a time, with the suggested options. The first is the only functionally critical one.

1. **Wiki language** — *functional; drives ALL wiki prose and the generated language pack.* Which language should the wiki be written in? (Norwegian / English / other.)
2. **Meta language** — *cosmetic.* Keep the operational docs (CLAUDE.md, skills, meta) in English (recommended — the tested baseline), or translate them to the wiki language? Translation takes a while and has **no practical effect** on how the vault works; purely reading comfort.
3. **Tone** — how should wiki prose read? (Neutral/encyclopedic · Conversational · Academic-dense.)
4. **Purpose** — what is this vault for? (Personal knowledge · Research/field · Work domain · Mixed — free text welcome.)
5. **Solo or shared** — one user, or several colleagues dropping sources? (Affects dedup + multi-author handling.)
6. **Standard categories** — home-page cards + hovedtags. Offer the starter set in `wiki/tags.md`; let them edit/add.
7. **Source types** — what will they mostly feed? (articles / podcasts / papers / books.) Tunes triage defaults.
8. **Personal layer?** — want a private folder the wiki and agent never touch (health, finance, private notes)? Yes/No. If yes: what should it be called? (default `personal`.)
9. **Vault name** — what should this vault be called? (Free text; suggest something from their purpose/categories; fallback "VaultOS".)
10. **License** — how should the vault content be licensed? (MIT · CC BY 4.0 · CC0 · All rights reserved.) Skip if it stays private/personal.
11. **Tufte viz skill?** — interested in a third-party data-visualization skill? If yes, point them to [aref-vc/tufte-claude-skill](https://github.com/aref-vc/tufte-claude-skill) (credit the author) with its install command. It is **not** bundled here.

## Phase 2 — Apply the answers

- Write the answers into `meta/vault-config.md` (wiki language, hovedtags, personal-folder name, vault name, source-type emphasis).
- **If the wiki language is not Norwegian:** generate `meta/vaultos-lang-<xx>.md` from the pattern in `meta/vaultos-lang-no.md` (section headings, infobox labels, mother-tongue prose rules for that language) and update the `@import` line in CLAUDE.md.
- Update `wiki/tags.md` (chosen hovedtags) and the `README.md` title (vault name).
- **If they chose meta translation:** translate CLAUDE.md, the skills, and the meta docs into the wiki language. Flag that this is the slower path.
- **If they want a personal layer:** create the folder under the chosen name with a short README explaining §B.10 (outside wiki ops; one-way `personal → wiki` linking only).
- Set the tone/purpose so it informs how you write wiki prose going forward.

## Phase 3 — Build the home page

- Fill `wiki/home.md` from its skeleton — one category card per chosen category.
- Tell them to install the **Homepage** community plugin and point it at `wiki/home.md` (see README → First-time setup), and to enable the CSS snippets (Settings → Appearance).

## Phase 4 — Close

Offer two paths:

- **Use it as-is** — "You're set. Drop a source in `inbox/` and say `ingest`."
- **Make it your own** — offer to walk them through the schema (CLAUDE.md §B.3), conventions, skills, tone, and categories, and co-develop their clone in dialogue. It's their vault, their rules.

Then set `todo.md` and `handoff.md` back to "No ongoing task" (note onboarding complete), and **offer to delete this `first-time.md`**.
