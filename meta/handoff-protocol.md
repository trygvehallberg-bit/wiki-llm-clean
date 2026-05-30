# Handoff protocol

## Purpose

Keep session continuation reliable without turning `handoff.md` into a long history file.

## Files

- `handoff.md` = short re-entry prompt for the next agent.
- `todo.md` = active work queue in priority order.
- `meta/handovers/` = detailed narrative handovers after substantial work.
- `wiki/log.md` = append-only operation history.
- Lint reports = dated audit/checklists, not runtime state.
- `meta/backlog.md` = deferred system/workflow ideas, not active task state.

## Mid-session rule

Update `handoff.md` and `todo.md` mid-session, not only at session end, whenever:

- A task completes or becomes blocked.
- Vault state changed in a way that would matter if the session paused right now.
- You hand off to a remote run or another agent (different model, `/loop`, scheduled task).
- A long-running or risky operation is about to start where mid-flight interruption would lose context.

The bar: if your session were interrupted in the next minute, would the next agent need this state? If yes, write it now. The end-of-session rule below is the *minimum* cadence, not the only one.

## End-of-session rule

Before ending a non-trivial session:

1. Update `handoff.md`.
2. Update `todo.md`.
3. Append or verify `wiki/log.md` if an operation changed the wiki.
4. Create a detailed handover in `meta/handovers/` only if the work was substantial.

## When to create a detailed handover

Create a detailed handover only when at least one is true:

- The work changed many files.
- The work changed schema/workflow decisions.
- The work left unfinished or risky state.
- There are decisions a future agent would otherwise rediscover.
- There are failed/rejected approaches that should not be repeated.
- A future agent needs a substantial situational report.

## `handoff.md` must contain

- current state;
- last important completed work;
- handoff receipt;
- next safe action;
- live-state recheck instructions before writing;
- do-not-do warnings;
- links to deeper context.

Keep it short. Link to details instead of copying them.

## `todo.md` must contain

- 3–10 active tasks;
- ordered by priority;
- one-line reason/source when helpful;
- no long history;
- no backlog dump.

## Detailed handover must contain

Use only after substantial work:

- purpose;
- handoff receipt;
- current state;
- completed work;
- decisions made;
- failed or rejected approaches;
- files created or materially changed;
- verification status;
- open work;
- resumption instructions;
- critical cautions;
- source pointers.

## Default read order for incoming agent

1. `handoff.md`
2. `todo.md`
3. detailed handover linked from `handoff.md`, if doing substantial follow-up
4. latest relevant lint report, if working on lint follow-up
5. tail of `wiki/log.md`, if operation history matters
6. `meta/backlog.md`, only if doing workflow/schema/deferred-design work
