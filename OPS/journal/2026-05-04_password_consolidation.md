# Password Manager Consolidation

**Date:** 2026-05-04
**Outcome:** Bitwarden is now the single source of truth for credentials across Linux and Windows.

## Context

Three password managers were in active use: LastPass (long-running), Google
Password Manager (browser-default, accumulated by drift), and a partial
Bitwarden install. Continuing this way meant credential search across three
tools, three different 2FA flows, three deletion paths when something went
stale. Decision: consolidate to Bitwarden, retire the other two.

## Installation

Bitwarden desktop and browser extension installed cleanly on Windows.

On Debian Trixie (Linux primary), neither apt nor snap routes worked
reliably — the apt package was missing/stale on this release, and snap
introduced its own friction. Resolved by downloading the AppImage from
vault.bitwarden.com, marking executable, and running from
~/Downloads/Bitwarden.AppImage. Functional but not ideal long-term — a
Flatpak or proper apt source would be more durable.

## Migration

- Exported LastPass vault to CSV: 1,331 entries
- Exported Google Password Manager to CSV: 1,015 entries
- Imported both via Bitwarden web vault, Tools, Import data
- Total ~2,346 entries with significant overlap
- Opted for opportunistic deduplication during normal use rather than
  scripting a full dedupe pass

## Cleanup

- Both plaintext CSV exports shredded with shred -vzu -n 3
- Verified files removed from ~/Downloads/
- Google Password Manager: save prompts and auto sign-in disabled
- LastPass: browser extension and Windows desktop app removed
- LastPass account deletion deferred ~1 week, pending confidence in
  the migration

## New conventions for Bitwarden

| Item type | Stored as | Naming |
|---|---|---|
| Capital One business CC PIN | Card | (default card fields) |
| ZKNOT vault passphrase | Secure Note | "ZKNOT vault passphrase" |
| SSH key passphrases | Secure Note | "SSH: <key-name>" |
| 2FA recovery codes | Secure Note | "2FA recovery: <service>" |

Optional folders: SSH, 2FA Recovery, ZKNOT.

## Open follow-ups

- Delete LastPass account at lastpass.com/delete_account.php (~2026-05-11)
- Optional: Bitwarden CLI dedupe script if manual cleanup gets tedious
- Consider a more durable Linux install path than the AppImage

## Why this is in the journal, not as Taskwarrior tasks

The deletion follow-up went into Taskwarrior as task 60 with due:2026-05-11.
Everything else here is a state-change record — what was true before, what
is true now, what conventions to follow. That belongs in the journal, not
the task list.
