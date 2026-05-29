---
date: 2026-05-19
topic: ZKKey Connect Rev 0 + software signer pivot + first ZK signing
workstream: [hw, fw, sw, ip]
status: shipped (Rev 0 software signing operational)
patents: PAT-001, PAT-006, PAT-007
---

# ZKKey Connect Rev 0 + Software Signer Pivot
## 2026-05-19

## TL;DR

Spent the day attempting to provision ATECC608B chips on a Pico 2 breadboard for the ZKKey Connect Rev 0. Bricked two chips during `gen_key` due to power transients on the breadboard (classic CRC Mismatch failure mode). Pivoted to PC-based software signing using Python `cryptography` library. Got the full signing pipeline working end-to-end: ECDSA P-256, ZK number derivation per PAT-007, monotonic counter, verification roundtrip. First ZK number signed and verified: `KAM6-M30B-4JHP`. Device ID `ZK-EW6E-EERX`. The PowerVerify shipping blocker is now unblocked — Rev 0 units ship with software-signed ZK numbers and the free-Rev-1-swap policy.

## Decisions

- **Path C (PC-based software signing) for Rev 0.** Not the patent's full §4 embodiment but covers PAT-006 FSM, PAT-007 ZK number, PAT-001 §§6-7. Marked with `fw: "0.1-pc-keys"` on every artifact for forensic auditability.
- **Stop trying to provision ATECCs on the breadboard.** Wait for MCP2221 + PC-side provisioning via Microchip CryptoAuthLib. Bench setup confirmed marginal due to power transients during gen_key current spikes.
- **NXP SE050 evaluation is a Rev 2 question, not Rev 1.** Patent language ("ATECC608A or equivalent" + "any variations in components") explicitly covers chip substitution. SE050 deferred.
- **Adafruit ATECC breakouts for prototype, SOIC-8 for production.** Keep the 3 remaining breakouts + 20 SOIC-8 chips from DigiKey for Rev 1.
- **Rev 0 units ship with software-signed ZK numbers and the "free Rev 1 swap" policy.** Customers know they're buying pre-1.0 hardware. Standard for security-grade products in early-revision phase.
- **One signing device for all Rev 0 units.** Device ID `ZK-EW6E-EERX`, single PC-resident pubkey. Per-unit ZK numbers derived from per-unit signing.
- **Software-first whenever hardware integration timeline is uncertain.** New rule, journaled separately as a lesson.

## What got built

### Software signer (Path C)

- `~/zkkey-venv/bin/zk_sign.py` — Python signer using `cryptography` library
- `~/zkkey-venv/` — venv with `cryptography` installed
- `alias zksign="~/zkkey-venv/bin/python ~/zkkey-venv/bin/zk_sign.py"` in `.zshrc`
- Commands: `init`, `info`, `sign`, `verify`
- Persists key, counter, device metadata, signed artifacts at `~/.zkkey/`

### Device identity

```
Device ID:   ZK-EW6E-EERX
Label:       ZKNOT-PROD-001
Firmware:    0.1-pc-keys
Created:     2026-05-19T15:37:20Z
Pubkey hex:  9b130211b7439cce0b98a06b3c214d31b04702f03c6d4a64ea34c5720c965cc5ce5243aef65378540b53b76712ded011780381dd81c5b333aaba2e961b0d2743
```

### First signed ZK number

```
ZK Number:   KAM6-M30B-4JHP
Counter:     1
Signed:      "PowerVerify SN12345"
Verifyknot:  https://verifyknot.io/v/KAM6-M30B-4JHP
Artifact:    ~/.zkkey/registry/KAM6-M30B-4JHP.json
```

Verification: `✓ Signature VALID`

### Pico firmware (provisioned, then shelved)

Built three CircuitPython firmware files for the Pico ZKKey Connect path:
- `provision.py` — ATECC provisioning (locks config, generates keypair, locks data)
- `sign.py` — main signing firmware with full PAT-006 state machine
- `host_sign.py` — host-side helper to send challenges and capture artifacts

These work conceptually but blocked by ATECC provisioning failure on breadboard. Reserved for use once MCP2221 + bench fixes are in place. Files are in `~/Downloads/` and `~/zkkey-connect-rev0/` for future deployment.

## How it works

### Signing flow (PC-side)

```
zksign sign --message "PowerVerify SN12345"
   │
   ├─► canonical_validate(challenge_bytes)         # PAT-001 §7
   ├─► priv.sign(challenge, ECDSA(SHA-256))         # PAT-001 §6
   ├─► counter ← counter + 1                        # PAT-002 monotonic
   ├─► canonical = sig|pub|chal|ctr|dev (joined)
   ├─► zk = base32(SHA-256(canonical)[:8])          # PAT-007
   └─► artifact saved → ~/.zkkey/registry/<zk>.json
```

### Artifact JSON schema

```json
{
  "zk":      "KAM6-M30B-4JHP",   // PAT-007 short code, on label
  "sig":     "<128 hex chars>",  // ECDSA r||s
  "pub":     "<128 hex chars>",  // device pubkey X||Y
  "chal":    "<hex>",            // what was signed
  "ctr":     1,                  // monotonic per device
  "dev":     "ZK-EW6E-EERX",     // signing device ID
  "ts":      1779205040.6474,
  "iso":     "2026-05-19T15:37:20Z",
  "fw":      "0.1-pc-keys",      // distinguishes from future ATECC artifacts
  "message": "PowerVerify SN12345",
  "label":   "PV1-00001"
}
```

### File locations

| Path | Purpose | Backup? |
|---|---|---|
| `~/.zkkey/signer.pem` | Private key (mode 0600) | Yes → `~/ZKNOT/99_SENSITIVE/zkkey_signer_20260519.pem` |
| `~/.zkkey/device.json` | Pubkey, device ID, firmware version | In git history of registry |
| `~/.zkkey/counter` | Monotonic counter state | Auto-incremented, recoverable from registry |
| `~/.zkkey/registry/<zk>.json` | All signed artifacts | Not yet committed; should add to git or sync to verifyknot.io |
| `~/zkkey-venv/bin/zk_sign.py` | The signer script | In `~/Downloads/zk_sign.py` and committed elsewhere |

## What didn't work

### ATECC provisioning on Pico 2 breadboard

Sequence of failures:

1. **First chip:** Wrote `CFG_TLS` config successfully, locked config zone, then `gen_key` returned `RuntimeError: CRC Mismatch` mid-operation. Chip half-provisioned (config locked, no key, data zone open).

2. **Recovery attempt:** Tried `gen_key` in REPL after `wakeup()`. Got `OSError: [Errno 19] No such device` — USB serial disconnected suggesting Pico browned out or rebooted during the ECC operation.

3. **Second chip lost to handoff error:** During recovery, executed `atecc.lock(1)` without first confirming `gen_key` succeeded. Data zone locked with no key in slot 0. Chip permanently bricked. Cause: I gave Claude-suggested recovery commands as a single code block; should have been separated with explicit "wait for success" gates between irreversible operations.

### Root cause analysis

The CRC Mismatch fault is well-documented for ATECC608 on Pico-class boards:

- **Power transients during ECC operations.** Key generation pulls ~14-20 mA briefly during the curve math. On a breadboard with the Pico's onboard 3.3V regulator feeding two devices (ATECC + OLED) through long parasitic-capacitance traces with no local decoupling, the rail sags. The ATECC's internal state machine resets mid-command; next read returns garbage CRC.

- **I2C clock-stretching strictness.** ATECC stretches SCL during compute. RP2350's busio.I2C does support stretching but the Adafruit library's wake/sleep sequencing may not give it enough recovery time.

- **Pull-up sizing.** Breakout has 10 kΩ pull-ups; with breadboard parasitic capacitance, rise time at 100 kHz is marginal.

### Why Pico software signing was also a dead end

After ATECC failed, attempted on-Pico software ECDSA with `adafruit_ecdsa`. Result: **library is no longer in the CircuitPython bundle.** Adafruit removed it some time after CircuitPython 9.x. So even without ATECC, pure-Python signing on Pico isn't readily available. Confirmed `pip install` of `adafruit_ecdsa` is for desktop Python, not CircuitPython.

This is what triggered the PC-signer pivot. Right answer the whole time.

## What I learned

### Strategic lessons

1. **Software-first when hardware integration timeline is uncertain.** Should have done PC-based software signing from the start as the Rev 0 vehicle. The patent's `fw` field on artifacts gives perfect forensic distinction between rev-eras. Burned two ATECCs and ~6 hours pursuing the hardware path before the obvious software path was tried.

2. **Identify the minimum patent embodiment that unblocks the business goal.** PAT-001 has multiple independent claims. Rev 0 needs *enough* of them to be a legitimate embodiment, not *all* of them. Specifically:
   - PAT-001 §4 (hardware-protected key) is a Rev 1+ claim
   - PAT-001 §§6-7 (signing flow, canonical validation) work in software
   - PAT-006 (FSM, counter, single-use) works in software
   - PAT-007 (ZK number) works in software
   - Rev 0 shipping with these claims is patent-compliant

3. **Never run irreversible operations from chat-suggested code blocks without explicit success gates between them.** The second-chip loss was because `atecc.lock(1)` was in the same block as the recovery commands, and I ran it before confirming `gen_key` actually succeeded. From now on: any irreversible step gets its own message exchange, with explicit "did X succeed? paste output" verification before proceeding.

### Technical lessons

4. **Adafruit's ATECC library API:** `serial_number` returns a string, not bytes. `version()` returns 24579 (0x6003) for ATECC608B. `counter()` with no args reads (not increments — but the library default behavior in some calls *does* increment, watch the kwarg). `lock(0)` for config zone, `lock(1)` for data zone.

5. **CircuitPython 10.x uses displayio not framebuf.** Generic SSD1306 OLED needs `adafruit_displayio_ssd1306` + `i2cdisplaybus.I2CDisplayBus`, with text via `adafruit_display_text.label`.

6. **STEMMA QT cable colors:** Black=GND, Red=VCC, Blue=SDA, Yellow=SCL. (Standard across SparkFun Qwiic + Adafruit STEMMA QT ecosystems.)

7. **`board.STEMMA_I2C()`** is the canonical way to get the I2C bus on CP 10.x. Works on Pico 2 (mapped to GP4/GP5) and Pico Plus 2 (real Qw/ST socket).

8. **Pico 2 has 2 USB endpoint surfaces:** `/dev/ttyACM0` for CDC serial, `/dev/sdaN` (or `sdbN`) for CIRCUITPY mass storage. Device letter changes between boots — always recheck `lsblk -f | grep CIRCUITPY`.

9. **`circup` and other Python tools on Debian 13 (Trixie) need a venv.** PEP 668 marks system Python as externally-managed. `python3 -m venv ~/zkkey-venv && ~/zkkey-venv/bin/pip install ...` is the path.

10. **DigiKey part number gotchas:** Several MPNs I assumed from memory were obsolete or wrong. **Lesson: always search MPN on DigiKey live, copy the current DK# from the live page.** Don't trust prior chat-suggested DK#s without verification.

## Hardware bench learnings

- **Power decoupling is non-optional for ATECC.** Next attempt needs 10 µF + 100 nF directly on ATECC VCC/GND pins, not just at the Pico's 3V3 output.
- **Saleae will pay for itself** debugging the I2C bus on next provisioning attempt. Capture a working sequence on a known-good chip (Adafruit demo code on a fresh breakout) before troubleshooting the failing path.
- **Breadboard is fine for everything EXCEPT ATECC provisioning.** Runtime signing (which is much less power-hungry than gen_key) probably works on breadboard with the same setup. The brick risk is gen_key + lock specifically.

## Where the patent stands

| Claim | Rev 0 (today) | Rev 1 (planned) |
|---|---|---|
| PAT-001 §4 hardware-protected key | ❌ software key in `~/.zkkey/signer.pem` | ✅ ATECC slot 0 |
| PAT-001 §5 physical actuation | ❌ no button on PC signer | ✅ Pico button-gated |
| PAT-001 §6 cryptographic flow | ✅ | ✅ |
| PAT-001 §7 canonical validation | ✅ | ✅ |
| PAT-006 FSM (single-use challenge) | ✅ | ✅ |
| PAT-006 post-nonce enforcement | ⚠️ partial (no physical button) | ✅ |
| PAT-006 monotonic counter | ✅ (file-based) | ✅ (ATECC counter) |
| PAT-007 short code (ZK number) | ✅ | ✅ |
| PAT-002 transport-agnostic output | ✅ (JSON+stdout) | ✅ (USB+OLED) |

Every artifact has `fw: "0.1-pc-keys"`. When Rev 1 ships, artifacts get `fw: "0.2-atecc-pico"`. Customers can swap Rev 0 → Rev 1 units; the registry can distinguish artifacts from each.

## Materials state

### ATECC chips
- 2× bricked (locked, no key) — kept as bus-testing reference chips
- 3× Adafruit 4314 breakouts — virgin, awaiting MCP2221
- 20× SOIC-8 ATECC608B from DigiKey — virgin, for Rev 1 PCB

### Pico hardware
- 1× Pico 2 (SC1631) — used today, fully working
- 5× Pimoroni Pico Plus 2 (PIM724) — ordered from Adafruit, in transit

### Other
- MCP2221 USB-I2C bridge — on factory special order from Microchip, ETA unknown
- Saleae Logic — on hand
- Adafruit STEMMA QT cables, OLEDs, hookup wire — confirmed in stock

### Bench
- Breadboard, Pico 2, ATECC breakout, SSD1306 OLED, 4 LEDs, button, hookup wire — wired, working
- LED color mapping confirmed: GP10=green, GP11=yellow, GP12=blue, GP13=red, GP15=button

## What's next (not done today)

### Immediate (today / tomorrow)
- [ ] Sign 4 already-shipped PowerVerify units (PV1-00001, PV-2026-00042, PV1-00043, PV1-00044) to populate registry
- [ ] Map physical unit serials to per-unit ZK numbers in a text file
- [ ] Commit registry to git or sync to verifyknot.io storage

### Short-term (this week)
- [ ] verifyknot.io endpoint design — how does `/v/<zk-number>` resolve? Static files? DB? Cloudflare?
- [ ] Decide registry storage model: public static files vs. private backend
- [ ] Continue signing PowerVerify units as they're built

### Medium-term (when parts arrive)
- [ ] MCP2221 arrives → ATECC provisioning script using Microchip CryptoAuthLib on PC
- [ ] Pimoroni Pico Plus 2 arrive → migrate Pico firmware path with proper decoupling
- [ ] First Rev 1-firmware artifact signed → `fw: "0.2-atecc-pico"`
- [ ] Build ATECC provisioning jig PCB (pogo-pin fixture)

### Long-term
- [ ] Connect Rev 1 PCB design + fab order
- [ ] PowerVerify Rev 1 formalization (capture as-built design)
- [ ] ZKKey Air Rev 0 breadboard validation
- [ ] Rev 0 → Rev 1 swap program logistics for early customers

## Hardware folder structure (set up in parallel thread)

Per the reconciled plan from the other thread:

```
~/ZKNOT/7_ENG/hw/
├── kicad-libs/               ← path vars: ZKNOT_SYMBOLS, ZKNOT_FOOTPRINTS, ZKNOT_3DMODELS
├── kicad-templates/
├── design-rules/
├── datasheets/
├── fab-output/
├── zkkey-connect/
│   ├── rev0-breadboard/      ← this thread's work goes here
│   └── rev1-pico-carrier/    ← future PCB
├── powerverify/
│   └── rev0-shipped/         ← capture what's already in customers' hands
├── zkkey-air/
└── tooling/
    └── atecc-provisioning-jig/rev1/
```

PowerVerify pigtail symbol + footprint already added to `kicad-libs/` in the other thread.

## Concepts and terms to understand

- **Canonical validation** — bounded length challenge bytes (16-64 bytes), rejects malformed input before signing. PAT-006 §4.2.
- **Post-nonce enforcement** — actuation (button) only valid AFTER challenge received. Prevents pre-signed signatures.
- **Single-use challenge consumption** — once signed, that challenge cannot be re-signed. State machine clears `challenge_buf`.
- **Monotonic counter** — strictly increasing value, prevents artifact replay across time. In hardware: ATECC slot counter. In software: file-based.
- **ZK number / short code** — 12-char base32 (Crockford alphabet) derived from SHA-256 of canonicalized artifact. Format XXXX-XXXX-XXXX. PAT-007.
- **Device ID** — 8-char base32 derived from SHA-256 of pubkey. Format ZK-XXXX-XXXX. Constant per device.
- **Canonical artifact** — pipe-separated string: `sig|pub|chal|ctr|dev`. Used for ZK number derivation. Same algorithm in firmware and host = same ZK number from same inputs.
- **CRC Mismatch** — ATECC error indicating I2C bus desync or power interruption. Recoverable with retry IF chip state is reachable.
- **TrustCUSTOM (-SSHDA)** — blank ATECC variant, we provision keys.
- **TrustFLEX (-SSHCZ)** — pre-provisioned ATECC variant, Microchip loaded keys at factory. Wrong for our use case.
- **CFG_TLS** — Adafruit's standard ATECC config. Slot 0 as ECDSA private key, signable, not readable. Default for first provisioning.
- **`fw` field on artifacts** — versioning string in every signed artifact distinguishing rev-eras. `0.1-pc-keys`, `0.2-atecc-pico`, `1.0-atecc-pcb`.

## Related journal entries (committed earlier today)

- `2026-05-19_first_zk_signing.md` — milestone of first ZK number signed
- `2026-05-19_lessons_software_first.md` — the "software-first when hardware uncertain" rule

## Bottom line

Tuesday well spent despite the chip losses. Real progress:
- PowerVerify shipping unblocked
- Patent embodiment validated in software
- Hardware path diagnostics complete (we know exactly what to fix)
- Folder structure ready for next PCB work
- 6 reusable lessons captured

Two ATECCs lost. Worth it for the lessons and the unblocked shipping.
