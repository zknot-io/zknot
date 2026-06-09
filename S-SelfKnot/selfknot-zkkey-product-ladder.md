# SelfKnot / ZKKey — Product Ladder & Give-Away Boundary

> **Systems reference.** Governs which builds are free vs. proprietary, and the single
> line that must never cross into free/CC content or public video narration.
>
> **Sources:** PAT-001 non-provisional spec draft (2026-03-28); supplemental comms spec
> (2026-01-22); NonProv Master Guide Vol 1–2 (2026-04-16).
> **Last reviewed:** 2026-05-30.
> **Caveat:** Claim-scope reads below are the inventor's working interpretation, **not legal
> advice**. Claims can change in prosecution. Confirm the boundary with patent counsel before
> any public guide or video ships the relevant content.

---

## TL;DR

- **The business** = the patented *display-the-hash-then-physically-confirm* step
  (content confirmation) + HSM-provisioned, config-locked keys + the verifyknot.io
  verification authority. None of these appears in free content.
- **Free builds** may demonstrate **human presence** (press-to-sign) but must never
  **build *or* describe** the display-confirm step.
- **Three-tier ladder:** Mini (signing oracle) → SelfKnot (presence) → ZKKey
  (content-confirmation, forensic).

---

## The give-away line (the one rule)

PAT-001 Claim 1 requires, in order: receive challenge → compute hash → **display the hash**
→ **detect physical actuation after the display** → sign only upon that actuation. Per
Master Guide §5.2, the element distinguishing the invention from *all* cited prior art
(YubiKey / FIDO2 / HSM / PIV) is the **display-then-confirm content step** — not the button.
Button-press-to-sign alone is close to FIDO2 prior art.

The line therefore has **two facets**:

1. **Don't practice it** in free builds — omit the display-the-challenge-hash-then-confirm
   step. Keeps free products outside Claim 1 and preserves the ZKKey product distinction.
2. **Don't teach/describe it** in free, public, CC content (guides *and* video narration) —
   describing the method publicly is a disclosure regardless of whether the free build does
   it, and can affect foreign / absolute-novelty rights before the non-provisional is filed
   (target 2026-09-30; deadline 2027-01-15; engage counsel by 2026-07-01, per Master Guide Vol 2).

**Output displays are fine.** Per the supplemental comms spec, a display that only presents
the *output* artifact (e.g., a verify QR code) is mere transport — interchangeable with USB —
and is **not** the crown jewel. The crown jewel is display of the *challenge hash, before
signing, for human confirmation.*

---

## The ladder

| Tier | Build | Human gate | Content confirmation | Provisioning | Assurance | Distribution |
|---|---|---|---|---|---|---|
| **0 — Mini** | FT260 + ATECC, headless | none (host-driven) | none | self | device-bound signature only | sell / give freely |
| **1 — SelfKnot** | MCU board (Pico, Black/Blue Pill, Pi, Arduino, ESP32) + ATECC + button, **no OLED** | MCU-enforced press-to-sign (presence) | none | self | self-asserted presence | sell / give freely; **flagship DIY** |
| **2 — ZKKey** | MCU + ATECC + **OLED challenge-hash display** + FSM | yes | **yes (display-then-confirm)** | **HSM-provisioned, config-locked** | forensic | **proprietary — never in free guides** |

**Platform nuance:** on an MCU (Tier 1) the press is **hardware-gated** in firmware. On the
FT260 (Tier 0) any "button" is **host-read** — gating is theater. Tier 0 is a signing oracle
regardless; never market a Tier-0 button as a gate.

---

## Component → claim-element map

| Component | In PAT-001 claims? | Free-build status |
|---|---|---|
| LED (status) | No | Drop, or trivial optional |
| Push-button / actuation | Yes (Claims 1, 10) — but presence-gating ≈ FIDO prior art | OK to include (Tier 1); demonstrates the human gate without the novel step |
| **OLED showing challenge hash *before* signing** | **Yes — the crown jewel** (Claim 1 "displaying…subsequent…actuation"; Claim 8 "while…displaying") | **Never in free builds or free content** |
| Display showing output artifact / verify QR | Transport only (supplemental comms spec) | OK anywhere |
| HSE / ATECC | Yes (generic "hardware secure element"; Claim 2 names ATECC) | OK — commodity chip |
| MCU running FSM gate | Yes (Claim 8 mechanism) | OK to gate on *actuation*; do **not** gate on display-confirm |
| HSM provisioning + config-lock | Spec §9; the forensic distinction | Proprietary — Tier 2 only |

---

## Why the ecosystem works (the funnel)

- Tiers 0–1 get people **into the verifyknot system** producing self-asserted records —
  badged `SELF-ASSERTED` so they never imply ZKNOT vouching.
- Many cheap/free builds + videos across the board series = category-building, demos, a
  community, and **defensive prior art for the presence layer** (which you don't need to own).
- The thing you *sell* — content-confirmation + forensic provisioning + the verification
  authority you operate — never appears in free content. **Ecosystem grows; business stays whole.**
- **Personal-monopoly note:** the moat is *not* "an attestation device" (anyone can ship that).
  It is the **specific human-content-confirmation method + the verification authority only you
  run.** Guard exactly that. Give away everything around it.

---

## The narration trap (operational discipline for videos)

You can build a button-only SelfKnot perfectly and still leak the moat by *saying*, on camera,
"…and the real one shows you the hash so you confirm it before signing." That sentence is the
disclosure. **Scripts get the same review as schematics.** Free content describes presence
("press to attest"); it never describes content-confirmation.
