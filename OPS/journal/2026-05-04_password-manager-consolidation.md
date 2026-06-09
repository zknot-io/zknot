# Password Manager Consolidation — 2026-05-04

Consolidated three password managers down to Bitwarden as the single source of truth.

## Installs
- Bitwarden desktop + browser extension on Windows
- Bitwarden AppImage on Linux (Debian Trixie) — apt and snap routes both failed; AppImage downloaded from vault.bitwarden.com, made executable, runs from ~/Downloads/Bitwarden.AppImage

## Migration
- Exported LastPass vault → 1,331 entries
- Exported Google Password Manager → 1,015 entries
- Imported both CSVs via Bitwarden web vault (Tools → Import data)
- Total ~2,346 entries with overlap; opted to dedupe opportunistically rather than scripting

## Cleanup
- Shredded both plaintext CSV exports with `shred -vzu -n 3`
- Verified files removed from /home/mt/Downloads/
- Disabled Google Password Manager save prompts and auto sign-in
- Removed LastPass browser extension and Windows desktop app
- LastPass account deletion deferred ~1 week pending confidence in migration

## New conventions for Bitwarden going forward
- Capital One business CC PIN → Card item type
- ZKNOT vault passphrase (age-encrypted file) → Secure Note
- SSH key passphrases → Secure Note, name format `SSH: <key-name>`
- 2FA recovery codes → Secure Note, name format `2FA recovery: <service>`
- Optional folders: SSH, 2FA Recovery, ZKNOT

## Open follow-ups
- Delete LastPass account at lastpass.com/delete_account.php (~1 week)
- Optional: Bitwarden CLI dedupe script if manual cleanup gets tedious
