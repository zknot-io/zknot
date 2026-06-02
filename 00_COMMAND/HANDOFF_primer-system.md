# THREAD HANDOFF — Primer System (scope: ONLY the primer/context-layer work)

> Paste this into a fresh chat to continue building out the primer system. This is scoped
> deliberately to the primer architecture itself — not the storage work or ATECC provisioning
> that happened in the originating session.

## What the primer system IS
A context-compression layer over the ZKNOT vault so any AI (or future-me after a trip) can be
oriented in minimal tokens. Three layers:
- **Layer 1 — ROOT primer** (`~/ZKNOT/00_COMMAND/CONTEXT.md`): paste-first index + triage.
  The "where do I start" file. One line per project, pointers not detail, critical-path at top.
- **Layer 2 — Project primers** (`~/ZKNOT/00_COMMAND/primers/<project>.md`) + existing
  `km/systems/` (durable how-it-works facts) + `journal/` (dated decisions).
- **Layer 3 — the full vault.** Only read into when a primer points there and the task needs it.

## Core rules (these are what keep it from rotting)
1. **A project earns a primer ONLY while active.** Parked projects = one line in the root, no file.
   This caps maintenance at the 3-4 things actually being touched.
2. **Primer shape fits its phase.** A bring-up blocker → a bench/debug file. A stable thing → a
   thin pointer. Don't write vision docs for things that need a checklist.
3. **Lossy on purpose.** Root holds the ~20% that matters and links the rest. Completeness is the
   enemy of loadable.
4. **Blank over guess.** `>>FILL<<` markers for anything only the operator can confirm. A confidently
   wrong primer is worse than one with honest blanks.
5. **MAINTENANCE IS THE WHOLE GAME.** Update the changed primer + root's "since last session" line as
   the LAST step of each work session (same moment as the journal). A stale primer lies. The system
   pays off on maintenance, not on setup. Win condition: 3 weeks later, after a trip, you open ONE
   file and it's still true.
6. **"Would a diff be useful?"** = the one-question test for what goes in git (text/source) vs. the
   share (binary/archive) vs. neither (secrets).

## To brief an AI: paste ROOT primer → paste relevant project primer → point at vault detail only if needed.

## What's BUILT (as of 2026-06-01)
- `00_COMMAND/CONTEXT.md` — root primer, structured around the real critical path.
- `00_COMMAND/primers/ft260-provisioning.md` — first project primer (now "recipe proven" status).
- Profile preference added: treat pasted primers as session ground truth; prompt if operator starts
  project work without pasting one.

## What's NOT built yet (the open primer work)
- **Project primers for the other active threads.** Current active set (from root): SelfKnot builds +
  content; Commercial provisioning (HSM2 ceremony → ZK#/PUF tracking → sell PowerVerify). Both were
  blocked-on-FT260 and may now be unblocked → may need primers built next.
- **`km/systems/network-storage.md`** — a Layer-2 systems note the root points to but that isn't written.
- **`>>FILL<<` fields in both existing primers** — operator still needs to complete the "what ZKNOT does"
  sentence in root, and the config/understanding notes in the FT260 primer.
- **A repeatable primer template** — the project primers share a shape (what it is / current state /
  next action / blockers / pointers / done-criteria). Worth extracting into a template file so new
  primers are consistent.

## Open question worth resolving in the new thread
With FT260 provisioning now proven, the two downstream projects (SelfKnot, commercial provisioning)
likely shift from "blocked" to "active" — which means re-triaging the root primer and deciding which
of them earns a primer next. Start there.

## The discipline to carry (named honestly in the source session)
The operator tends to react to a new organizing system with high energy and an urge to EXPAND
("I need ten primers!"). The cure built into this system is the opposite: ruthless triage, only-active-
gets-a-primer, update-as-last-step. If a new primer feels like progress, check whether it's replacing
the actual work or capturing it so the actual work can proceed. Building a primer is not doing the thing.

## Anchor facts (so the new thread isn't blind)
- Operator: William Shane Wilkinson, ZKNOT INC. (Salt Lake City). Vault at `~/ZKNOT/`, git-tracked,
  GitHub org zknot-io. Dev: Debian Trixie 13, zsh.
- Primers live in `~/ZKNOT/00_COMMAND/`. Commit them after edits (they're the load-bearing orientation
  layer; vault is single-copy on ~2-day manual backup).
