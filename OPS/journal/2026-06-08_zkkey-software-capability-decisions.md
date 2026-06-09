---
date: 2026-06-08
topic: ZKKey software capability decisions (v1)
tags: [zkkey, sig, firmware, hardware-selection, patents, decisions]
status: complete
related:
  - SIG-REQ-ZKKEY-001 (ZKKey Software & Firmware Capability Requirements)
  - SIG-DEC-ZKKEY-001 (ZKKey Software Capability Decisions — v1, CANONICAL)
  - PAT-001, PAT-004, PAT-005, PAT-006, PAT-007, PAT-008, PAT-009, PAT-010, PAT-011, PAT-018
---

# 2026-06-08 — ZKKey software capability decisions (v1)

## TL;DR

Drove the ZKKey design the right way round: started from the filed patents, derived a chip-agnostic
software/firmware **requirements** spec, then locked five **decisions** that become canonical for the
v1 build window. The load-bearing move was a constraint reframe — cost is not a gate, devices are built
from the PCB up — which flipped the governing principle to "design the maximum into the board, populate
when firmware/feature need calls for it." Produced two canonical docs (requirements + decisions). Next:
lock the signed-record format (sized against the Air QR ceiling) and write the v1 conformance subset
that maps onto candidate silicon.

## The arc

- Read PAT-001 + supplemental and the full patent summary as ground truth before building anything.
  The ZKKey envelope is defined across PAT-001 (core), PAT-008 (FSM), PAT-009 (optical/Air),
  PAT-010 (short code), PAT-007 (combined session), PAT-011 (dual-SE Ultra), PAT-005 (vendor ledger),
  PAT-004 (LocalChain), PAT-018 (firmware_hash / tamper).
- Built SIG-REQ-ZKKEY-001: core ceremony (receive challenge → validate → arm → human actuation →
  sign → output → reset) + the keystone insight that the **signed output must be a structured,
  versioned, crypto-agile record**, which turns every future version into "populate a field," not a redesign.
- Worked the five Part-V forks into determinations.
- Reframed on cost (build from PCB up) → added D-0 and re-resolved D-1, D-3, D-4 accordingly.
- Identified what a hardware decider still needs (six parameter groups; four need my direct call).

## Decisions (canonical — full rationale in SIG-DEC-ZKKEY-001)

- **D-0 — Provisioning philosophy:** Design the maximum into the PCB; gate population by firmware
  maturity / feature need, NOT cost. Governs everything below. "Reserve for later" now means
  "lay it out on the board, populate when ready."
- **D-2 — Human-presence gate:** Hardware-enforced, **strong form** — the physical actuation state
  conditions the SE's signing op; the MCU can observe but not drive it. Non-negotiable; decided
  before D-1 because it filters the SE shortlist hardest. A firmware-triggered handshake is insufficient.
- **D-1 — Secure-element count:** Board laid out for **dual-SE**; v1 target = dual populated
  (Identity SE + Signing SE). Bring-up path single → dual to de-risk the domain-router firmware.
  Cost no longer argues for single; only firmware-schedule risk stages it. Relies on the
  two-component record (R-10) + role separation (F-03) so verifiers never change.
- **D-3 — Display vs LED:** Display path **designed into the board**; bring up LED-first to de-risk
  FSM/SE/gate, add display before any flagship/display-then-confirm firmware ships. LED stays as the
  always-on FSM-state status layer.
- **D-4 — Replay protection:** **Stateful** rolling consumed-challenge log as default, monotonic
  counter as the always-on floor, timestamp/counter staleness check to close the rolling-window horizon.
  Shares the storage subsystem with D-5.
- **D-5 — Manufacturing ledger:** **Reserve + require genesis self-sign** in v1 (proves on-device key
  origin); reserve hash-chained ledger storage (free-rides on D-4). Build customer-receipt/lifecycle
  flow only when a federal solicitation requires demonstrable provenance. Staged on an external-tooling
  dependency, not cost.

## Why the cost reframe was load-bearing

Before the reframe, three decisions leaned on cost/simplicity (single SE, LED-first board, hybrid
replay). "Build from the PCB up, populate when necessary" removed that axis entirely and replaced it
with "design-in vs populate," gated by firmware maturity. That's a cleaner and more durable rule, and
it's why D-1/D-3/D-4 all moved toward "design it all in." D-2 stays populated-and-proven in v1 on
purpose: the gate isn't a future feature, it's the irreducible core of what the device is.

## Open items / next steps

- **My call needed before a hardware decider can start (four):** challenge max size + accepted formats;
  consumed-challenge log depth; display content spec (incl. QR-or-not for Air); v1 form factor.
- **Cross-constraint to resolve:** if optical-out (Air) is reserved, the artifact must fit a scannable
  QR — sets a compactness ceiling on the record format.
- **Next deliverables:** (1) lock the signed-record format against the QR ceiling; (2) write the v1
  conformance subset — the exact MUST list mapping one-to-one onto candidate silicon.
- **Patent discipline:** keep display-then-confirm firmware and any public/free-build content out of
  circulation until the PAT-001 non-provisional is filed (deadline 2027-01-15; attorney engagement
  precedes public exposure of the moat features).

## Version-control status

Both canonical docs (SIG-REQ-ZKKEY-001, SIG-DEC-ZKKEY-001) and this journal entry are NOT backed up
until committed to the git-tracked vault. Decision docs land in 6_SIG/firmware/; this entry in
3_OPS/journal/.
