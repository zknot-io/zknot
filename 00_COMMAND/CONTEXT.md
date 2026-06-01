<!--
ROOT PRIMER — how to use
- FIRST thing you open after a gap; FIRST thing you paste to any AI.
- INDEX + TRIAGE, not a summary. One line per project. Pointers, not detail.
- Detail -> 00_COMMAND/primers/<project>.md, km/systems/, journal/.
- MAINTENANCE: update the changed row + NEW section as the LAST step of each work session. A stale primer lies.
- >>FILL<< = still needs your input.
-->

# ZKNOT — ROOT CONTEXT PRIMER

**Operator:** William Shane Wilkinson — founder/operator, ZKNOT, INC. (Salt Lake City, UT)
**What ZKNOT does:** >>FILL: 1-2 plain sentences for a stranger. Draft: "ZKNOT builds hardware-rooted, human-gated cryptographic attestation — devices that prove a real person performed a real action at a real time, backed by a secure element and PUF evidence. Products: PowerVerify, ZKKey Connect/Air; SelfKnot = the open/DIY education line."<<
**Federal status:** SDVOSB-certified (SBA VetCert ~May 2026). Active SAM.gov (UEI C4SKW13JPEL5, CAGE 1AHZ4). SBIR NOT pursued (no topic fit).

---

## THE CRITICAL PATH (read this first — it's mostly one chain, not 5 parallel things)

```
FT260 ATECC provisioning  --+-->  SelfKnot builds (Pico/Arduino/ESP32) --> video + guides --> audience
   <- THE UNBLOCKER ->       +-->  HSM2 provisioning ceremony --> ZK# + PUF tracking --> SELL PowerVerify
```
Almost everything is blocked on FT260 provisioning working. Do that first; two branches open behind it.

## ON FIRE / DO NEXT

- **FT260 provisioning** — wired up, no working script yet. THIS is the unblocker. -> `primers/ft260-provisioning.md`

## BLOCKED ON FT260 (don't start until provisioning works)

- **SelfKnot builds + content** — Pico/Arduino/ESP32 reference builds -> record video -> post guides ("protect your ideas").
- **Commercial provisioning** — YubiHSM2 ceremony -> official ZKNOT/verifyknot ZK-number + PUF-evidence tracking -> sellable PowerVerify with real ZK numbers.

## NEW SINCE LAST SESSION

- 2026-06-01: Centralized storage live — `~/ZKNOT` is an SMB share, Windows `Z:` via `\\mt\share`; `99_SENSITIVE`+`01_PATENTS` veto'd off network. NAS deferred (build-as-income). Primer system started. See journal 2026-06-01.

---

## PROJECTS (status: HOT / WARM-blocked / PARKED)

| Project | Status | One-line state | Next action | Primer |
|---|---|---|---|---|
| **FT260 provisioning** | HOT | Wired, no working script; SW bottleneck (I2C + TFLXTLS slot config) | Get first chip reading/provisioning via FT260 | `primers/ft260-provisioning.md` (built) |
| **SelfKnot builds + content** | WARM blocked | Pico/Arduino/ESP32 builds -> video -> guides | (after FT260) build Pico reference first | `primers/selfknot.md` (later) |
| **Commercial provisioning** | WARM blocked | HSM2 ceremony -> ZK#/PUF tracking -> sell PowerVerify | (after FT260) design ceremony | `primers/commercial-provisioning.md` (later) |
| **Federal / gov** | PARKED-light | SDVOSB done, no SBIR. Two to-dos only | Build LynxConnect.io profile; work APEX + conferences | (no primer — parked) |
| **Patents** | PARKED | 6 provisionals; conversions due 2027-03-01 (long fuse) | none now | (no primer — parked) |
| **NAS / infra** | PARKED-stable | Storage live; NAS deferred parts-as-income | offsite backup; INFRA-002 forks (someday) | (folded into infra notes) |

---

## STABLE FACTS (pointers, not detail)

- **Legal name (all filings/signatures):** William Shane Wilkinson (never "Shane Wilkinson" alone)
- **Federal email:** shane.systems@gmail.com  ·  **Address:** 1884 W Sir Charles Dr, Salt Lake City, UT 84116-4652
- **Vault:** `~/ZKNOT/` git-tracked. Repos: `~/zknot-api` (FastAPI/Railway, api.zknot.io), `~/verifyknot-site`. GitHub org: zknot-io.
- **Storage:** `~/ZKNOT` = SMB share, Windows `Z:` via `\\mt\share`. How-it-works -> `km/systems/network-storage.md` (to write)
- **Backup:** INTERIM — manual upload to ops@zknot.io + shane.systems@gmail.com Drives every ~2 days. restic->SSD+B2 at NAS arrival. Vault otherwise single-copy.
- **Patent backup:** `01_PATENTS/` off-repo — >>VERIFY exists + restorable<<
- **Dev:** Debian Trixie 13, zsh, Taskwarrior+Timewarrior (`task next/ready/blocked/stream`).

---

## BRIEF AN AI: paste this -> paste the relevant project primer -> then point at vault detail only if needed.

**Last verified:** 2026-06-01 (Shane, partial — >>FILL<< fields open)
Page 1 of 1
