---
title: WitnessMark — STM32CubeMX / CubeIDE TrustZone Setup Primer
doc_id: SIG-FW-ZKKEY-002 (working primer)
status: WORKING PRIMER — bring-up guide, not a canonical spec
parent: SIG-FW-ZKKEY-001 (firmware/secure-config enforcement)
author: William Shane Wilkinson (ZKNOT, INC.)
date: 2026-06-09
target: STM32U585AII6 (UFBGA132) · dev on B-U585I-IOT02A · STM32CubeIDE first
goal: a TrustZone-split project with GTZC isolation + the signing-ceremony skeleton running.
  NOT full OEMiRoT/SBSFU hardening — that is the later refactor (and Redoubt's CLI/CMake+TF-M build).
sources: AN5394 (CubeIDE TrustZone getting-started, L5/U5) · AN5347 (GTZC) · RM0456 (U5 ref manual,
  regions + option bytes) · STM32Cube_FW_U5 SBSFU/TF-M examples (for the refactor)
---

# WitnessMark — CubeMX / CubeIDE TrustZone Setup Primer

## 0. What "get it working" means today (the stop line)

The milestone for this thread is a **TrustZone-split project that boots, where the non-secure app calls a secure veneer, and the secure side drives the OLED, reads the button on a secure GPIO, signs a fixed challenge with a key held in secure storage, and returns it.** That proves the partition and the content-binding path. **Explicitly deferred to the refactor:** OEMiRoT/SBSFU secure boot, anti-rollback, OPTIGA cross-cert, RDP2 lock. Don't let the hardening pull you off the bring-up.

You can do all of this **on the B-U585I-IOT02A dev kit now** — it is a U585, so you are not blocked on your 4-layer board.

## 1. Prerequisites

- STM32CubeIDE (current) + **STM32Cube_FW_U5** firmware pack installed.
- **STM32CubeProgrammer** (sets the `TZEN` option bit and RDP — TrustZone is enabled via option bytes, not just CubeMX).
- B-U585I-IOT02A board + ST-LINK.
- Reference open in a tab: **AN5394** (TrustZone project workflow) and **AN5347** (GTZC). Follow these for exact menu paths — they are the authority; this primer is the map.

## 2. The target partition (from SIG-FW-001 §1)

| Secure world (S) | Non-secure world (NS) |
|------------------|------------------------|
| Signing key + signing FSM | USB (OTG_FS) device stack |
| OLED bus + driver + framebuffer | Host relay |
| Button GPIO (+ EXTI) | Housekeeping |
| Monotonic counter, consumed-challenge log store | |
| OPTIGA I²C | |
| RNG, AES/SAES, PKA, HASH | |

NSC veneers (the only NS→S calls): **`submit_challenge()`** and **`collect_artifact()`**. Nothing that signs, displays, or reads the button.

## 3. CubeMX configuration, in order

**3.1 Create the project, enable TrustZone.** New project on `STM32U585AII6` (or the B-U585I-IOT02A board). In Project Manager, set **TrustZone activated**. CubeMX will generate a **Secure project + a Non-Secure project under one superproject** — your code lives in both, with shared HAL.

**3.2 Clock + power (match the locked HW decisions).** Configure the **HSE crystal** as the clock source → PLL. In Power, set the **SMPS** regulator (your chosen SMPS variant) — this is a deliberate locked decision, not a default. Confirm the exact U585 SMPS/`xQ` package config against RM0456 at BOM time.

**3.3 Memory partition — SAU/IDAU.** Define the secure / non-secure-callable (NSC) / non-secure regions for flash and SRAM. **This is the step everything else must agree with.**

**3.4 Assign peripherals to zones (Security view / GTZC TZSC).** Per §2: USB → NS; OLED bus, button GPIO, OPTIGA I²C, RNG, AES/SAES, PKA, HASH → S. (In ST's TZ examples, a secure-controlled GPIO like an LED is explicitly placed on the secure side while others stay NS — same pattern for your button + OLED-control pins.)

**3.5 GTZC (Security ▸ GTZC_S).** Configure the submodules:
- **TZSC — securable peripherals:** set each secure peripheral above to `SEC`. Generated as `HAL_GTZC_TZSC_ConfigPeriphAttributes(GTZC_PERIPH_xxx, GTZC_TZSC_PERIPH_SEC|...)` in `MX_GTZC_Init()` in the **Secure** project's `gtzc_s.c`.
- **MPCBB — block-based SRAM** (512-byte pages): mark the SRAM pages holding secure data (key material, framebuffer, log buffers) secure.
- **MPCWM — watermark memory:** mark the flash region holding the key/log/cert store secure.
- **TZIC — illegal-access interrupt:** **enable it** and route `GTZC_IRQn` to a safe ERROR/reset handler (this is SIG-FW-001 FW-I-05 — an NS touch of a secure resource must trap, not be ignored).

**3.6 NSC veneers.** Define the non-secure-callable region; implement the two secure gateway stubs (`submit_challenge`, `collect_artifact`) — compiled into the secure-gateway import library the NS project links against.

**3.7 Generate code.** You get the Secure + Non-Secure projects. Secure boots first, configures GTZC, then branches to NS.

## 4. The gotchas that eat days (pre-empt them)

1. **SAU/IDAU must match GTZC (MPCBB/MPCWM).** A mismatch gives "read-as-zero" / secure faults when secure tries to reach NS, or NS faults reaching shared memory. If something reads as zero or faults across the boundary, this is almost always why. (3.3 ⇄ 3.5 must agree.)
2. **`RCC_GTZC` clock enable** is sometimes **omitted by CubeMX's generated `MX_GTZC_Init()`** — verify the GTZC peripheral clock is actually enabled, or your GTZC config silently does nothing.
3. **Crypto-in-secure quirks.** AES/SAES with shared keys in a TZ project has known timing/handling traps — bring crypto up in isolation in the secure app before wiring it into the ceremony.
4. **`TZEN` is sticky.** It's an option byte set via CubeProgrammer; reversing it on the dev board is a regression-unlock sequence (fine on the kit, reversible). On production it lives behind RDP2 — irreversible, which is the point, but don't lock the dev kit.
5. **Lock GTZC last.** `HAL_GTZC_TZSC_Lock()` freezes the config until reset — call it only once the partition is proven, or you'll be resetting constantly during bring-up.

## 5. Maps SIG-FW-001 → CubeMX (so the spec and the project agree)

| Spec req | CubeMX action |
|----------|---------------|
| FW-I-01 OLED secure | OLED bus + control GPIO → SEC (TZSC + GPIO security) |
| FW-I-02 button secure | button GPIO + EXTI → SEC |
| FW-I-03 OPTIGA secure | OPTIGA I²C → SEC |
| FW-I-04 crypto/RNG/log secure | AES/SAES/PKA/HASH/RNG → SEC; log flash/SRAM → MPCWM/MPCBB SEC |
| FW-I-05 illegal-access trap | TZIC enabled → GTZC_IRQn → ERROR/reset |
| FW-C ceremony | secure-app state machine + the two NSC veneers |
| FW-S secure boot, FW-L lock/anti-rollback, FW-P cross-cert | **deferred** to the refactor / Redoubt build |

## 6. This thread feeds KiCad — do it in this order

The CubeMX **pinout is the input to your schematic**, not the reverse. Once peripherals are assigned (which pins carry the OLED bus, button, OPTIGA I²C, USB D±, HSE crystal, SWD), **export the pinout** and use it as the KiCad pin-assignment constraint. Settle the pinmux here *before* you commit copper, or you'll route to pins the peripheral config can't honor.

## 7. Verify-before-claim (feeds best-mode later)

Pin the exact part **STM32U585AII6 / UFBGA132**; the as-built TrustZone + GTZC + secure-display config is the PAT-020 Embodiment-3 best-mode detail — keep as-built = as-disclosed. Exact option-byte/RDP specifics and the SMPS config: confirm against **RM0456** as you go (carries the SIG-FW-001 §9 items).

## 8. Backup / version control

Commit the **`.ioc` + both generated projects** as the bring-up baseline. **Do not commit secrets** — OEM signing keys and the OEM2 password are HSM-custodied (that's the refactor/provisioning step, not this one). The `.ioc` is the reproducible source of truth for the pin/peripheral/GTZC config; treat it as the canonical artifact.

---

*Working primer under SIG-FW-ZKKEY-001. Bring-up scope only; secure-boot/anti-rollback/cross-cert/RDP2 are the hardening refactor (and Redoubt's CLI/CMake+TF-M build). ST workflow grounded against AN5394 / AN5347 / RM0456 + community-confirmed gotchas (SAU↔GTZC match; RCC_GTZC clock) on 2026-06-09.*
