# 2026-05-03 — Personal Git Infrastructure: Phase 1 (full thread capture)

Consolidated record of the personal file-organization work so the chat thread
can be deleted. Everything needed to resume is here.

## The big picture (why this exists)

Moving toward git as primary personal file organization on Linux (Debian Trixie,
zsh), away from Google/Windows. Three separate workstreams, deliberately split:

- **Thread A — ZKNOT KM-002 execution.** Company file management, git-crypt +
  MANIFEST.md inside the `~/ZKNOT` repo. Handoff doc already exists (the KM-002
  docx). Not this thread.
- **Thread B — Personal git workflow.** THIS thread. Dotfiles, notes, vault.
  CLI-first, GitHub-hosted under personal account.
- **Thread C — Off-Google migration.** Drive, Photos, Docs, Gmail, password
  manager. Deferred to Q3, separate handoff to be written then.

Decisions already locked (do not relitigate):
- Dotfiles: chezmoi
- Notes: plain markdown, no Obsidian/Logseq lock-in
- Vault: git-crypt + GPG key (not transcrypt)
- Hosting: GitHub primary, Codeberg mirror later
- Backups: restic to Backblaze B2, weekly systemd timer (not set up yet)
- SSH: separate `github-personal` alias + key, distinct from `github-zknot`

## What got DONE this thread

### SSH identity
- Generated `~/.ssh/github-personal` (ed25519, passphrase-protected).
- Added `github-personal` host alias to `~/.ssh/config` (HostName github.com,
  IdentityFile ~/.ssh/github-personal, IdentitiesOnly yes).
- Added public key to GitHub account `Shanerbaner24`.
- Verified: `ssh -T git@github-personal` → "Hi Shanerbaner24!"
- Note: passphrase prompts each new shell session. Either `ssh-add` once per
  session, or set up keychain/systemd later. Deferred.

### Git identity separation
- Global identity stays ZKNOT: William Shane Wilkinson / zknot@zknot.io
- Created `~/.gitconfig-personal` with Shane Wilkinson /
  88160439+Shanerbaner24@users.noreply.github.com
- Conditional include in global gitconfig:
  `includeIf "gitdir:~/personal/" → ~/.gitconfig-personal`
- VERIFIED working: repos under `~/personal/` use noreply; ZKNOT keeps
  zknot@zknot.io. This is the load-bearing separation mechanism.
- chezmoi source dir (`~/.local/share/chezmoi`) lives OUTSIDE ~/personal/, so
  its git identity was set per-repo manually to the noreply address.

### home-config repo (chezmoi)
- Installed chezmoi via upstream script to `~/bin` (not in Trixie apt repos):
  `sh -c "$(curl -fsLS get.chezmoi.io)" -- -b ~/bin`. Version 2.70.2.
- `chezmoi init git@github-personal:Shanerbaner24/home-config.git`
- Tracking: .zshrc, .gitconfig, .tmux.conf, .config/nvim/init.lua
- Pushed to github.com/Shanerbaner24/home-config (private).
- Cleanup TODO: duplicate `export PATH="$HOME/bin:$PATH"` lines got appended to
  .zshrc during setup — remove the dupes when convenient.

### SECURITY INCIDENT — Perplexity API key (resolved)
- chezmoi detected a plaintext `PPLX_API_KEY` on line 62 of .zshrc and refused
  to add it. Key was also exposed in an uploaded screenshot + chat log.
- ROTATED: old key revoked in Perplexity dashboard, new key generated.
- New key now lives in `~/.zshrc.local` (chmod 600, untracked, never in git).
- `.zshrc` sources it: `[[ -f ~/.zshrc.local ]] && source ~/.zshrc.local`
- Pattern going forward: machine-local secrets live in ~/.zshrc.local, recreated
  by hand on each new machine from the password store. Never chezmoi-added.

### notes repo
- `~/personal/notes`, git init -b main, pushed to
  github.com/Shanerbaner24/notes (private).
- Structure: journal/YYYY/MM-DD.md, ideas/, projects/, decisions/
- Wrote decisions/2026-05-03_personal-vs-zknot-vaults.md capturing the
  separation rule (see below).
- Wrote projects/personal-infra-setup.md as the running TODO.

## Cross-cutting decision recorded
Personal vault = separate `vault` repo, git-crypt + personal GPG key.
ZKNOT sensitive = `99_SENSITIVE/` inside ZKNOT repo per KM-002. Different keys,
different access lists. Existing `~/ZKNOT_VAULT/sensitive_v3_*.tar.gz.age` stays
as age-encrypted disaster-recovery archive — do NOT migrate it to git-crypt.

## What is NOT done — resume here

### Next session: vault repo (focused 30–45 min, mistakes are expensive)
- [ ] Generate GPG key (lose it = lose the vault forever — back it up properly)
- [ ] Paperkey backup, printed, stored offsite
- [ ] git-crypt init in vault repo (already in Trixie: `sudo apt install git-crypt`)
- [ ] .gitattributes rules for which paths get encrypted
- [ ] Test cycle: encrypt → commit → fresh clone elsewhere → decrypt
- [ ] Add GPG key to GitHub for signed commits
- [ ] Vault repo already created empty on GitHub: Shanerbaner24/vault

### Eventually (Phase 2 / backups)
- [ ] Codeberg mirror for all three repos (git remote add codeberg ...)
- [ ] Create Backblaze B2 account + bucket + app key (prerequisite for restic)
- [ ] restic config backing up ~/personal + local clones
- [ ] systemd timer for weekly restic
- [ ] Quarterly: git clone --mirror to external SSD, store offsite

### Phase 3 (off-Google) — deferred to Q3, separate thread
Order: Bitwarden (in progress, separate thread) → Drive (restic to B2) →
Photos (Takeout export + maybe local Immich) → Docs (markdown, gradual) →
Gmail (last, Fastmail recommended over Proton, 6-month tail).

## Open loops worth not forgetting
- SSH passphrase prompt per session — decide whether to fix.
- .zshrc duplicate PATH lines — clean up.
- Bitwarden migration running in a different thread/window.
- ZKNOT v2 folder migration window — confirm committed before Thread A.
