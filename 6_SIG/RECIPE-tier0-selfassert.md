# Provisioning Recipe — Tier 0 Self-Assertion Signing Oracle (FT260 + ATECC608)

> **Tier 0 (Mini), per SelfKnot/ZKKey product ladder.** Headless FT260 + ATECC608,
> no human gate, no display, no button, self-provisioned. Device-bound signing oracle
> only. Records produced are SELF-ASSERTED and must be badged as such. This is NOT a
> ZKKey and NOT an official ZKNOT product; the official root of trust uses a YubiHSM 2
> in a separate trust domain.
>
> **This recipe contains NO secrets** — it is the reproducible provisioning procedure
> and slot semantics only. Generated private keys never leave the chip and are never
> recorded anywhere.
>
> **Guide-boundary note:** This procedure provisions for *device-bound signing /
> presence-style self-assertion* only. It does NOT implement or describe the
> display-the-challenge-hash-then-confirm step (PAT-001 crown jewel). Keep that out of
> guide text, code comments, and video narration.

## Target hardware
- Bridge: FT260 (UMFT260EV1A), kernel `hid_ft260` → `/dev/i2c-6`
- Device: ATECC608B, SOIC-8 I2C (order code SSHDA), 7-bit addr 0x60 / 8-bit 0xC0
- Config: TFLXTLS-family, preloaded by distributor (NOT blank factory default)

## Pre-lock verified state (read-only confirmed 2026-05-31)
- Both zones UNLOCKED (LockConfig=0x55, LockValue=0x55)
- Slots 0,1,2: P256 ECC private, ExtSign enabled, Lockable
  (decoded SlotConfig 0x2083/0x2087/0x208f, KeyConfig 0x0033)
- Slot 0 = primary signing slot (convention)
- Slots 3-15: data/SHA slots, not used for signing

## Path decision: PATH 1 — lock existing TFLXTLS-family config as-is
Rationale: the preloaded config already exposes P256 ext-sign lockable slots; no need
to author a custom SlotConfig/KeyConfig. We trust the existing layout for the low-threat
self-asserted tier. (HSM-provisioned config-locked path is Tier 2 / ZKKey only — not here.)

## Procedure (irreversible steps marked IRREVERSIBLE)
1. [reversible] Read config zone, confirm both zones unlocked. (readconfig.py)
2. [reversible] Decode slots, confirm slot 0 ext-sign P256 lockable. (slotscan.py)
3. [reversible] Commit THIS recipe to git.
4. [IRREVERSIBLE] Lock CONFIG zone. Gated behind explicit operator confirm.
5. [IRREVERSIBLE] GenKey into slot 0 (device self-generates P256 keypair).
6. [reversible] Read & record the slot-0 PUBLIC key (public only — safe to store/publish).
7. [IRREVERSIBLE] Lock DATA zone. Gated behind explicit operator confirm.
8. [reversible] Verify: sign a test message with slot 0, verify the signature externally.

## Test-article discipline
Provision and fully verify ONE part end-to-end before batching the remaining parts.
Six parts total; do not lock all six to an unverified procedure.

## What is recorded vs. never recorded
- RECORD (safe, may be public/VC'd): device serial, slot-0 PUBLIC key.
- NEVER RECORDED: slot-0 private key (generated on-chip, never extractable by design).

## Per-part provisioning log (fill as you go)
| serial | config locked | slot0 keygen | data locked | pubkey recorded | test sig OK |
|--------|---------------|--------------|-------------|-----------------|-------------|
| 01233571a3172157ee |  |  |  |  |  |
| 01239cb0044cf5d6ee |  |  |  |  |  |
| 01231c0a2fc647cbee |  |  |  |  |  |
| 0123d49d18b8602eee |  |  |  |  |  |
| 01235d49dfdb8e93ee |  |  |  |  |  |
| 0123f0982825efe9ee |  |  |  |  |  |
