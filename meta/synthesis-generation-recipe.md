# Synthesis generation — portable recipe for LLM-maintained wikis

This document describes how to make an LLM-maintained knowledge vault produce **synthesis pages** — wiki pages that combine claims from 3+ sources to argue a position those sources don't argue individually. It is written to be handed to a fresh LLM agent working on a different vault; the agent should read it cold and adapt the conventions to that vault's schema.

A synthesis is **not** a summary of one source, **not** a list of "see also" links, and **not** a topic survey. It is a piece of writing with its own thesis, citing the vault as evidence.

Examples of well-formed syntheses (titles only, to convey shape):
- *Judgment as the new scarce resource* — 9 sources converging on one premise from seven vantages.
- *Robotics six positions on the autonomy problem* — six sources, six stances on the same problem.
- *The Norwegian lice data layer* — three reports + one regulator + one industry body, all data-quality angle.

Two paths produce syntheses. Both depend on the same preconditions. Get the preconditions right and either path fires reliably.

---

## Part 1 — Preconditions: what the vault must have

Most of the work to make syntheses possible happens **during ingest**, not when synthesis is requested. If ingest is mechanical, synthesis generation has nothing to work with. Five things have to be true:

### 1. Source pages name their cluster siblings explicitly

Every source page has a `## Cross-references` section. Not "see also" with bare wikilinks — each link has a **role label**. Working format:

```
## Cross-references
- [[Lai - Framework ergonomics for agents]] — framework-API layer of the same deterministic-scaffolding argument
- [[Olickel - Bedrock runtime]] — runtime layer of the same argument
- [[Mao - CLI as substrate]] — CLI/MCP layer of the same argument
- [[Geewax - Production AI architecture]] — system layer of the same argument
```

The role labels become the synthesis's **spine**. Without them, the survey step finds wikilinks but doesn't know what cluster they belong to. With them, a synthesis writes itself: *"Four sources argue deterministic scaffolding across four layers (framework, runtime, CLI, system)..."*

**Rule for the ingester:** when filing a source page, ask "what is this source the *X-layer* / *Y-position* / *Z-vantage* of?" That phrasing in the cross-reference section is the synthesis seed.

### 2. Concept pages accumulate source bullets

Every concept page maintains a list of which sources argue it, with a one-line gloss per source. When ingest touches a source that argues an existing concept, it **updates** the concept page — adds the new source as a bullet, may also expand the concept's framing if the new source brings a sharper angle.

```
## Argued by
- [[Khurdula]] — model layer: encoder-decoder split makes outputs verifiable
- [[Olickel]] — runtime layer: sentinels and bedrock checks
- [[Cohen]] — trust-boundary layer: per-call authorization
- [[Geewax]] — system layer: deterministic outer loop with LLM inner loop
- [[Tan]] — OS layer: Fence guardrails at the kernel
```

The bullet count is your **cluster tally counter**. When a concept page hits 4–5 source bullets all arguing related variants, the threshold for a synthesis has been crossed. Without this accumulator, you have no signal that a cluster exists.

### 3. The log is narrative, not mechanical

The append-only operations log (e.g. `wiki/log.md`) is a research diary, not an audit trail. Each ingest entry says what was filed, what new entities/concepts were created, **what cluster this source joined or completed, and what synthesis candidates this just put within reach**.

Bad log entry:

```
## [2026-05-21] ingest | Tan transcript
Filed source page. Created entity. Updated index.
```

Good log entry (real, from a working vault):

```
## [2026-05-21] ingest | Jun Yu Tan: Fence and OS-level guardrails
Source page [[Jun Yu Tan...]]. New entities: ... Expanded [[Deterministic scaffolding]] —
Tan supplies the strongest quantitative case so far. Now five sources on the concept
page across five layers. The four-layer agent-agency-and-control subcluster (Mao /
Cohen / Olickel / Tan) is now strong enough that it could be a synthesis page in its
own right — flagging for after one more landing.
```

"Flagging for after one more landing" is a note from past-agent to future-agent. The on-demand survey reads the log tail and picks up these flags. Without them, the survey rediscovers clusters from scratch every time, and often misses them.

### 4. The schema explicitly permits filing syntheses without asking

The default LLM posture is to ask permission before creating anything. For synthesis generation that posture kills the operation — by the time the agent has justified each candidate, the session is spent on meta-discussion.

The schema must say: filing syntheses is part of the job. Suggested clause:

> Creating new wiki pages — entities, concepts, syntheses — is the job, not a violation of "minimum work." Lean toward filing. Cheap to merge later, expensive to discover the omission six months in. When a cluster reaches 3+ sources with a shared diagnosis, file the synthesis; don't ask.

Without an equivalent clause in your schema the agent will gate every synthesis behind "should I write this?" and you'll get nothing.

### 5. The schema defines `kind: synthesis` and a folder for it

- `kind: synthesis` in YAML frontmatter
- A dedicated folder, e.g. `wiki/syntheses/<title in sentence case>.md`
- Frontmatter `sources:` as a list of `[[wikilink]]` to every cited source page
- Each cited source page gets a `## Cross-references` entry pointing back at the synthesis (human-readable counterpart to the machine-readable `sources:` list)

Without a defined `kind`, the agent doesn't know where to put it, what frontmatter to use, or that the back-link convention exists. Synthesis pages without back-links from the source side become orphans the next survey can never find.

---

## Part 2 — Path A: mid-ingest threshold crossing

This is the spontaneous path. Synthesis emerges as a side effect of ingesting a source that completes a cluster.

The ingest procedure (extended from a normal source-page write):

1. **Read raw source.** Parse the new material.
2. **Read existing wiki state.** Open the index, follow wikilinks one hop into related concept pages and 2–3 sibling source pages. **This step is the one most-likely missing in vaults that don't produce syntheses.** Without reading the existing wiki, the ingester treats every source as an island.
3. **Write the source page.** Standard structure (key claims, context, open questions, cross-references). The cross-references section names sibling sources by their **role** in the shared argument.
4. **Update touched concept pages.** Add the new source as a bullet to any concept page the new source argues. Expand the concept's framing if the new source brings a sharper angle.
5. **Post-ingest reflection — the critical step.** Before closing the operation, ask three questions:
   - *Did this source complete a 3+ source cluster?* (Check concept page tallies, scan cross-references for repeated co-occurrences.) If yes → **file the synthesis now, in the same operation.**
   - *Did this source add a new domain to an existing synthesis?* (e.g., a new source might add an "indie product craft" row to an existing synthesis on creative judgment.) If yes → **update the synthesis.**
   - *Is there a cluster that's close but not yet at threshold?* If yes → **flag it in the log entry.** *"Now four sources; one more landing and this becomes a synthesis."* That flag is what Path B picks up later.
6. **Write the log entry.** Narrative form. Name clusters joined, candidates flagged, syntheses filed or updated.

The threshold heuristic: **3 sources is the minimum, 4–5 is the sweet spot.** Below 3, it's a cross-reference, not a synthesis. Above 7–8 with no clear shared argument, the synthesis becomes a list — split into two narrower syntheses.

---

## Part 3 — Path B: on-demand survey ("make synthesis")

The user prompt is open: "make synthesis", "what new syntheses are writable now", "scan the vault for synthesis candidates." No topic, no question. This is a **survey operation**, distinct from ingest and from question-answering.

The procedure:

1. **Read the log tail.** Last ~50 entries, or back to the previous synthesis filing if recent. Pick up:
   - Explicit candidate flags ("flagging for after one more landing")
   - Recent ingests that mention joining an existing cluster
   - Any "this would be a synthesis if X" notes

2. **List the syntheses folder.** Read titles and frontmatter `sources:` lists. Now you know:
   - What's already been written (don't re-propose)
   - Which sources are already cited where (helps spot **adjacent** angles — same cluster, different axis)

3. **Scan source pages' cross-references.** Pull the cross-reference sections of source pages from the last N ingests. Look for:
   - Repeated co-occurrences (same 3–5 sources cross-referencing each other across multiple pages)
   - Repeated role labels (multiple sources marked as "X-layer of Y argument")
   - Clusters that span source pages from different folders/topics — those are the highest-payoff syntheses because they bridge material that doesn't yet talk to itself

4. **Generate candidates.** For each candidate, three things:
   - **Source basis** — the 3+ wikilinks
   - **Story** — one sentence: *what position do these sources, taken together, argue?* Not "what topic do they cover" — what *position*. If the story is "these sources are all about X," it's a topic list, not a synthesis. Reject.
   - **Why now / why this** — what makes it writable now (just crossed threshold? bridges existing syntheses?) and what makes it different from adjacent existing pages

5. **Propose 3–5 candidates. Wait for the human to pick.** Do not auto-file from a survey. The human picks 1–2; you write those.

6. **Write the picked syntheses.** Each one as its own operation: source page back-links updated, frontmatter `sources:` complete, log entry filed.

The candidate generation step is where judgment lives. Rules of thumb for **good** candidates:

- **Same diagnosis, different prescriptions.** Multiple sources agree on the problem but propose different solutions. Synthesis names the agreement and maps the disagreements. (*Robotics six positions* is this shape.)
- **Same prescription, different vantages.** Multiple sources arrive at the same recommendation from different angles. Synthesis names the recommendation and shows the convergence. (*Judgment as the new scarce resource* is this shape — seven layers, same conclusion.)
- **Same domain, contested.** Sources argue against each other. Synthesis maps the disagreement and what each side commits to. (Conflict-shaped synthesis; rarer but high-value.)
- **Causal axis on an observational pattern.** A descriptive synthesis already exists; the new one explains the mechanism behind it. (E.g. an existing *Regional status comparison* is observational; a new *Climate as the regional-status multiplier* is causal.)

Rules for **bad** candidates to reject:

- "All these sources are about AI." → topic list, not synthesis.
- 3 sources where only 1 actually argues the position; the other 2 just mention it. → not a real cluster.
- The synthesis would just restate one source's argument with two others as footnotes. → it's that source's own page, not a synthesis.
- The same cluster is already covered by an existing synthesis. → unless you have a genuinely different axis, skip.

---

## Part 4 — What makes a written synthesis good

Once a candidate is picked and you commit to writing it, structural guidance:

**Lead with the thesis, not the topic.** First line states the position the sources collectively argue. *"Nine talks accept the same premise and arrive at the same conclusion from seven different vantages: judgment is what doesn't get cheaper."* Not: *"This synthesis explores how multiple sources discuss the role of judgment in AI."*

**Name the shared diagnosis early.** Before the divergences, the agreements. One section, maybe titled "The premise the cluster accepts" or "What unifies the sources." Bullet list with one line per source naming what each contributes to the shared diagnosis.

**Then map the divergences with clear labels.** Each source gets its own subsection under a labeled axis (layer / position / vantage / domain). The label is load-bearing: *"Org-design judgment ([[Huntley]])"* is doing more work than *"Huntley's view."* The label tells the reader *where in the conceptual space* this source sits.

**Pull quotes for the strongest claims.** Use `> [!quote]` callouts (or equivalent in your vault's callout system) for verbatim quotes that anchor the argument. Use `> [!important]` for load-bearing claims you're paraphrasing. Don't over-callout — 3–5 per synthesis is the ceiling.

**Include a "where the cluster is silent" section.** Every synthesis should name what its sources collectively *don't* address. This does three things: keeps the synthesis honest, surfaces future ingest priorities, and gives lint something to flag if a later source fills the gap.

**Close with adjacencies.** Wikilinks to sister syntheses, sister concepts, sources that almost-belong. This is what makes the synthesis a hub rather than a dead-end.

**Update every cited source page.** Each cited source page gets a new entry under its `## Cross-references` section: `- [[<synthesis>]] — <one-line role of this source in the synthesis>`. This is what makes the synthesis discoverable from the source side, and what feeds the next survey's "what's already covered" pass.

---

## Part 5 — Failure modes and diagnostics

When a vault isn't producing syntheses, the failure is almost always in the preconditions, not in the trigger. Diagnostic order:

1. **Open three random source pages. Look at `## Cross-references`.** If empty or just bare wikilinks without role labels, that's the primary failure. Fix during ingest going forward; retrofit a few pages by hand to seed the pattern.
2. **Open three random concept pages. Look for source bullet lists.** If concept pages are essay-form with no enumerated sources, the cluster tally is invisible. The agent has no signal of "this concept has 5 arguers now." Refactor concept pages to keep an `## Argued by` section.
3. **Read the last 20 log entries.** If they're all one-liners ("ingested X, created Y, updated Z"), the log isn't carrying signal. Rewrite the ingest skill/procedure to require narrative log entries that flag cluster joins and candidates.
4. **Read the schema doc.** Find the clause that says "filing new pages is the job, lean permissive." If it's absent, the agent is gating every synthesis behind permission requests. Add the clause.
5. **Check that `kind: synthesis` is defined.** If the schema doesn't formalize the synthesis page type, the agent might be writing them as concept pages, query-response chat replies, or not at all.

When the trigger fails (preconditions are met but "make synthesis" still produces nothing):

- The agent might be skipping the log-tail read. The schema's "where to start" section should explicitly say: *for synthesis surveys, read the log tail before scanning sources.*
- The agent might be searching for *new* syntheses without reading the existing ones first, causing it to skip candidates because they look "already done" — even though the existing one is on a different axis. Schema should encourage *adjacent* syntheses, not just new clusters.

---

## Part 6 — One-page summary

The minimum knowledge a fresh agent needs to start producing syntheses in this vault:

> Syntheses are wiki pages combining claims from 3+ sources to argue a position those sources don't argue individually. Filed at `wiki/syntheses/<title>.md` (or vault-equivalent) with `kind: synthesis` frontmatter and a `sources:` list of wikilinks.
>
> **Two paths produce them:**
>
> **Path A — mid-ingest threshold crossing.** During fresh ingest, when the new source completes a 3+ source cluster (concept page tally crosses 3–5, or cross-reference sibling pattern recurs), file the synthesis in the same operation. Also update existing syntheses when the new source adds a domain.
>
> **Path B — on-demand "make synthesis" survey.** User prompt with no topic. Procedure: (1) read the log tail, (2) list the syntheses folder to know what's covered, (3) scan recent source pages' `## Cross-references` for cluster patterns, (4) propose 3–5 candidates with source basis + one-line story, (5) wait for human to pick before filing.
>
> **Preconditions for either path to work:**
> - Source pages name cluster siblings explicitly in `## Cross-references`, with role labels per sibling (not just bare wikilinks).
> - Concept pages maintain an `## Argued by` list of source bullets — this is the cluster tally counter.
> - Log entries are narrative, flag candidates ("flagging for after one more landing"), name clusters joined.
> - Filing new wiki pages is the job, not a violation — lean permissive.
> - `kind: synthesis` and a syntheses folder are formally defined in the schema.
>
> **When filing:** lead with the thesis (not the topic), map divergences under labeled axes, include a "where the cluster is silent" section, update every cited source page's `## Cross-references` with a back-link to the synthesis.

That's the whole recipe. Adapt the slugs, folders, and callout syntax to your vault's conventions; the mechanics carry over.
