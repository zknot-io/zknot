<!--
ROOT PRIMER — how to use
- FIRST thing you open after a gap; FIRST thing you paste to any AI.
- INDEX + TRIAGE, not a summary. One line per project. Pointers, not detail.
- Detail -> product primers (primers/<product>.md), platform primers (primers/platform-<layer>.md),
  km/systems/ (durable how-it-works), journal/ (dated decisions).
- PRIMER ARCHITECTURE (max 3 layers, never more than 3 primers per project):
    concept/system notes -> platform primer (hw / fw / sw / web integration) -> THIS root.
    Each PRODUCT gets one primer: WitnessMark, Redoubt, PowerVerify, TrustSeal, verifyknot, SelfKnot.
- MAINTENANCE: update the changed row + NEW section as the LAST step of each work session. A stale primer lies.
- >>FILL<< = still needs operator input. Blank over guess.
-->

# ZKNOT — ROOT CONTEXT PRIMER (v2)

**Operator:** William Shane Wilkinson — founder/operator, ZKNOT, INC. (Salt Lake City, UT)
**What ZKNOT does:** ZKNOT builds hardware-rooted, human-gated cryptographic attestation — devices that
prove a real person saw and approved a specific artifact at a knowable time, verifiable by anyone
without trusting ZKNOT. Flagship: WitnessMark (working name, trademark knockout pending); shipping now:
PowerVerify; public verification authority: verifyknot.io; SelfKnot = open/DIY education line (benched).
**Federal status:** SDVOSB-certified. Active SAM.gov (UEI C4SKW13JPEL5, CAGE 1AHZ4) through 2027-03-17.
SBIR is NOT an on-ramp — do not treat it as a milestone.

---

## THE CRITICAL PATH (one spine + one parallel track + two gates)

```
BUILD SPINE:  CubeMX .ioc (QII6Q, TZ/GTZC) ──> KiCad 4-layer ──> Rev-A board ──> jig: provision+lock ──> pot
PARALLEL SW:  TS client-side verifier + 1 real signed record ──> honest CO demo ──> transparency log (TL-01..07)
GATE (IP):    file PAT-020 (locks priority) · July 1 attorney: PAT-021 + counsel note + portfolio Qs
GATE (BRAND): WitnessMark + Redoubt trademark knockout BEFORE any public use
```
The spine is gated by the `.ioc`; the software track is fully ungated — push it whenever hardware waits.

## ON FIRE / DO NEXT

- **CubeMX `.ioc` on B-U585I-IOT02A** — pin/TZ source of truth; drives KiCad. -> SIG-FW-002 primer (fix
  header to QII6Q first), hw-design-reference §7 driving order.
- **TS client-side verifier + 1 real signed record** — live verifyknot verdict is server-asserted over
  placeholder data; no "math verified it" demo line until this ships. -> km/systems/verifyknot-primer.md §0/§7.
- **File PAT-020** — drafted, filing-ready. Filed? >>FILL: yes/no + date<<
- **Commit the canonical set to the vault** — v6 spec, PAT-021 draft, HW resolution, spike runbook,
  hw-design-reference still live only in outputs/INBOX. Mark v5 (and v4) superseded.

## NEW SINCE LAST SESSION (2026-06-08/09)

- Flagship architecture LOCKED: mechanism B (secure-MCU enclave), split-domain populated (AP-4),
  **STM32U585QII6Q + OPTIGA Trust M (EAL6+)** under the YubiHSM civilian root. Content-binding
  (shown == signed) is the moat and a firmware MUST (C-G4). Canonical spec now **SIG-SPEC-006**.
- Lab-grade signing-key extraction = OUT of v1 scope (PSA-L3 + secret-erase, stated honestly).
  Hardened SKU = **WitnessMark Redoubt**: rotating keys + tamper-responsive potting (PAT-018). MCU is not the lever.
- Time basis decided: **RFC-3161 TSA-anchored LocalChain transparency log** (VER-18′ fail-closed).
  PAT-021 drafted on the combination; **Sigstore = closest prior art** — counsel note ready (NOTE-001).
- Software stack locked: COSE/CBOR records (multi-signer, not COSE_Sign1) · CubeIDE-first (WitnessMark),
  CLI/CMake+TF-M (Redoubt) · CT-modeled transparency layer · TS (client) + Python (reference) verifiers.
- Found live verifyknot gap: verdict server-asserted over mock data — caught before any CO demo.
- Vault: reorg audit complete (1 file restored, nothing lost); CONTEXT.md moved to repo root; pushed @914ab20.

---

## PROJECTS (HOT / WARM-blocked / PARKED)

| Project | Status | One-line state | Next action | Primer |
|---|---|---|---|---|
| **WitnessMark (flagship)** | HOT | Architecture + silicon + specs locked (SIG-SPEC-006, FW-001, VER-001+ADD); board not started | CubeMX .ioc on dev kit -> KiCad | primers/witnessmark.md >>FILL: build<< |
| **verifyknot.io** | HOT | Frontend live; verdict is server-asserted over placeholder data — NOT demo-ready | TS client verifier + 1 real record; /v/ canonical + redirect | km/systems/verifyknot-primer.md (v2, current) |
| **Patents / IP** | HOT | 18 filed provisionals; PAT-020 fileable (filed? >>FILL<<); PAT-021 + Sigstore note ready | File PAT-020; July 1 attorney engagement | 01_PATENTS/ + DOC-001 tracker |
| **PowerVerify (PV-C)** | WARM | Selling $39; units PV1-00055..59 blocked on `zksign sign` before labels | Run zksign on the 5 units | primers/powerverify.md >>FILL: build?<< |
| **TrustSeal** | WARM | #2 in build order; A002 sellable run gated on live verify route confirm | Confirm verifyknot /seal/{serial} route before stock buy | km/systems/trustseal-production-and-fulfillment.md |
| **Redoubt** | PARKED-design | Defined (rotating keys + tamper mesh); rides WitnessMark board (footprints now, populate later) | none until WitnessMark Rev-A | folds into witnessmark primer |
| **SelfKnot** | PARKED | Benched until WitnessMark ships; zknot.org only | none | primers/selfknot.md (later) |
| **Federal / gov** | PARKED-light | SDVOSB done; no SBIR | capabilities surface when products ship | — |

---

## STABLE FACTS (pointers, not detail)

- **Legal name (all filings/signatures):** William Shane Wilkinson (never "Shane Wilkinson" alone)
- **Federal email:** shane.systems@gmail.com · **Ops:** ops@zknot.io · 1884 W Sir Charles Dr, SLC UT 84116-4652
- **Vault:** `~/ZKNOT/` git (org zknot-io, alias github-zknot). Repos: `~/zknot-api` (FastAPI/Railway,
  api.zknot.io), `~/verifyknot-site` (Cloudflare Pages). Reorg in flight: old 0–9 scheme + new 0X_ dirs coexist.
- **Backend live:** POST /v1/attest · GET /v1/verify/{code} · ZK-LocalChain in prod. URL form: /v/{code} canonical.
- **Patent ground rules:** `01_PATENTS/` gitignored BY DESIGN — off-repo backup is the safety net.
  >>VERIFY backup exists + current through PAT-020/021<<. Deadlines: PAT-003 2027-01-15 (tightest),
  general 2027-03-01, PAT-019 2027-04-14. Attorney target 2026-07-01; non-prov target 2026-09-30.
- **Honesty invariants (never violate in any copy/claim):** signing key = PSA-L3 (not EAL6+); EAL6+ =
  identity custody only; gate = immutable-firmware-enforced, not silicon-impossible; no FIPS claim
  without live CMVP check; verifier states exactly what was proven and no more (VER-04).
- **Dev:** Debian Trixie 13, zsh, Taskwarrior+Timewarrior. Windows `Z:` via `\\mt\share`.
- **Backup:** INTERIM manual Drive uploads ~2 days; restic->SSD+B2 at NAS arrival. Vault otherwise single-copy.

---

## BRIEF AN AI: paste this -> paste the relevant product/platform primer -> point at vault detail only if needed.

**Last verified:** 2026-06-09 (rebuilt from session ground truth; >>FILL<< fields need operator)
Page 1 of 1
