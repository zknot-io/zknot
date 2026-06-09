# 2026-05-19 — Thread capture: AI stack, market discovery, social strategy, product decisions

## Purpose

Capturing everything from an extended working session before deleting the chat
and going on a trip. Covers: AI account division of labor, the four-chat / three-bucket
operating system, market-discovery intelligence from Reddit (the most valuable part),
product decisions (Pico-first, camera choice), social presence tactics, and a running
list of relationships worth maintaining. Nothing here should be lost.

---

## PART 1 — THE OPERATING SYSTEM (carry forward, this is the backbone)

### Three buckets (time allocation model)

- **Foundation** — 30 min/week, Friday, never gets pushed. Patent clock, SAM.gov
  renewal (2027-03-17, remind at 2026-12-01), infrastructure uptime, runway math.
- **Compounding** — 45-60 min daily mornings. Personal Reddit, r/ATECC608 mod work,
  defending live posts, weekly technical writeup, weekly LinkedIn post. The unsexy engine.
- **Adventure** — everything else, no guilt. Product design, engineering, new ideas,
  rabbit holes. Where the brain wants to live. ~30+ hrs/week.

Key insight: the single-founder bottleneck is NOT time, it's context-switching cost
("blending"). Lanes solve that. Foundation/Compounding done first each day, then
Adventure is guilt-free.

### Four-chat structure (AI stack division of labor)

8 paid AI accounts, 8 jobs, no overlap:

| Account | Job |
|---|---|
| Claude Max | Operations & Strategy — Friday review, runway, patent decisions, cross-cutting calls. The brain. Don't migrate context out of it. |
| Claude Pro | Engineer + r/ATECC608 — daily comments, technical writeups, sub mod work. Voice consistency. |
| ChatGPT #1 | ZKNOT Official — u/zknot_io, LinkedIn, paid ads, customer emails. Build "ZKNOT Voice" Custom GPT. |
| ChatGPT #2 | Adventure/Creative — brainstorms, naming, packaging, image gen, voice mode while soldering. |
| Gemini #1 | Patent & Document Workshop — long-context reads of patents, datasheets, SOWs. Drive integration. |
| Gemini #2 | Inbox & Calendar — Gmail drafting, Calendar (patent clock, SAM renewal), Drive org. Workspace glue. |
| Perplexity | Research & Govcon Intel — FPDS/sam.gov, JOFOC analysis, NSTXL/AFWERX, competitive landscape, citations. |

Cheat sheet generated and (should be) printed/pinned at workbench.
ZKNOT Voice Custom GPT spec written — paste into ChatGPT GPT builder, upload the 3
social presence docs as knowledge files, set to "Only me."

### Document canon (social presence)

Three-doc set: Handoff + Addendum + Week1_Progress brief. The progress brief was
generated this session, covers the 5-day timeline, buckets, four chats, 7/30/90-day path.

---

## PART 2 — MARKET DISCOVERY (THE MOST VALUABLE PART — read this first when back)

Two weeks of Reddit engagement accidentally produced a go-to-market thesis. The
convergence is real and worth trusting.

### The customer profile that emerged

NOT consumer. NOT the cheapest devices. The market is:

**High-value, unattended field assets in adversary-accessible locations, operated
by integrators who own the device-to-cloud relationship.**

Examples named in conversation: agricultural sensors (Arable-style — solar field
sensors, sit for years, cellular uplink, integrator owns the fleet, end-farm just
consumes data), utility meters, telecom infrastructure, commercial drones, pipeline/
water/environmental monitoring.

The threat model that justifies the hardware: not "remote network attacker" but
"someone with screwdrivers and time." Physical access to unattended devices is THE
condition where on-die key generation + tamper resistance stop being a checkbox and
start being the actual reason the product exists.

### The two-lens validation (from r/OTSecurity)

- **sk3tchcom (OT practitioner):** bottom-of-stack reality. Most clients are "neck
  deep in default passwords." Zero trust is a pipe dream. Secure elements are a luxury
  problem most of the field isn't asking about yet. → The floor is much lower than assumed.
- **hiddentalent (security reviewer):** top-of-stack reality. Where unit economics AND
  threat model justify it (field devices $1000+, aerospace, utilities), secure elements
  DO get deployed. Consumer IoT = failed (price-sensitive, nobody cares). The friction
  is provisioning infrastructure, not the chip.

Both true. Different market segments. ZKKey serves the INTERSECTION: high-value
unattended assets in environments mature enough to provision them, where the customer
runs (or trusts a third party to run) the infrastructure rather than the OEM.

That intersection is **critical infrastructure**: utilities, telecom, transportation,
agriculture-at-scale, oil/gas, water. ALSO where OTA/CSO/govcon funding flows. The
Reddit threads + the r/govcon conversation + federal procurement all point at the
SAME market. Trust the convergence.

### FIDO Device Onboarding (FDO) — must understand deeply

- Solves "device-knows-nothing-at-manufacturing-time" — device gets identity at
  first-boot rendezvous, NOT at the factory. Moves trust anchor off the contract
  manufacturer's line. Clever architectural inversion.
- Operator pattern: whoever manages/maintains the devices runs the FDO servers.
  Rarely the end customer; usually an integrator or OEM the customer contracts with.
  (Arable-style company, not the individual farm.)
- "Winning by default, not by enthusiasm" — stuck on political infrastructure problems
  but there's little better alternative, so companies use it. KEY INSIGHT: when a standard
  succeeds because it's the only option rather than because it's loved, there's product
  space underneath it (build the better alternative, OR build tooling that makes the
  rough edges livable).
- FDO "political problem" only really bites when the device must outlive its relationship
  with the integrator. Consumer IoT has that problem. Field-device-as-a-service mostly
  doesn't — device and service sold together, end of one = end of the other. Trust
  boundaries line up with commercial boundaries.

ACTION: Read the FDO spec (fidoalliance.org, ~80 pages). Audit Linux Foundation FDO
reference implementation + FIDO Alliance certified-products list. Figure out if FDO is
compatible with or competitive to ZKKey architecture. 4-6 hrs Adventure work.

### The OT culture insight (relationship lens)

OT/IoT/IIoT security practitioners are professionally lonely — can't discuss security
publicly, tight-lipped unless under NDA, "like IT in the '90s, all risk no reward."
CISA was publishing anonymized case studies (one of the few peer-learning mechanisms)
but has been gutted by the current administration; proactive work halted. The reason
the r/OTSecurity thread got engagement at all: it gave practitioners a place to
commiserate without violating NDA. Being a good public interlocutor in this space is
genuinely valuable because there's nowhere else for the conversation to happen.

### Companies-like-Arable list (build this out when back)

8-12 companies across ag-sensing, water monitoring, environmental sensing, energy
meter networks, last-mile telecom. Each is a potential ZKKey customer in 18-24 months.
Arable is the archetype (precision ag, the "Mark" sensor, sells to Driscoll's/vineyards/
row-crop, owns device-to-cloud). Research their profiles, advisory boards, public
security materials. Don't act yet — just know what a successful customer looks like.

---

## PART 3 — PRODUCT DECISIONS

### ZKKey line — Pico-first strategy (reaffirmed/pivoted)

- **ZKKey Connect:** build first on RP2040 Pico. KiCad → JLCPCB order.
- **ZKKey Air v1:** ALSO Pico-based, not STM32 (pivot). Same infra as Connect, faster
  to feedback, meets patent intent. BOM: RP2040 + single ATECC608B + SSD1306 OLED +
  button + battery + LEDs + optical ingestion module.
- **STM32 deferred** until both Pico variants are designed, ordered, and have customer
  feedback. STM32 is a post-PMF decision, not v1.
- **Single ATECC608B** confirmed (was considering two — simplification is correct, one
  chip + careful slot planning meets patent intent).
- **Skip cellular on Air v1.** Doubles BOM, adds recurring data cost, regulatory
  certification landmine per country. USB-only or BLE ships in ~6 weeks vs ~6 months
  with cellular. Save cellular for v2 when customers ask. (The "GSM65" was a
  misremembered part — the actual need was the camera/scanner, not cellular.)

### Camera / optical ingestion decision

Use case: capture QR/serial/document/seal and sign an attestation. Need legible, not
photographic.

**Decision: Arducam Mega 5MP autofocus ($34.99), SPI-only.** Reasoning: SPI saves GPIO
budget (4 wires vs 12 for parallel), autofocus matters for variable-distance handheld
capture, Arducam publishes RP2040 example code, ports to STM32 later. Ordered.
Plus mitreapel silicone mold release spray ($11.99) for Graip potting.

**Backup ordered/considered:** OV2640 Mini Module ($25.99, 198 reviews, proven path)
as bench insurance in case the Mega 5MP is flaky on Pico. Cheap insurance against being
blocked waiting for a part.

RP2040 has no native camera interface (no DCMI/CSI). Parallel sensors need PIO bit-bang.
SPI modules (Arducam Mega) sidestep this entirely. USB UVC host path rejected (TinyUSB
UVC host not production-grade — rabbit hole).

Patent note: "optical ingestion module" is broad enough in claims to cover any sensor
choice. Don't narrow provisional language to "CMOS parallel-interface sensor."

### Graip (backburner adventure)

Consumer/novelty AirGap variant. Grape-themed, translucent purple potting, silicone
"vine" pigtail. Smaller board, cheaper SKU, same patent claims. Translucent purple
(not opaque) preserves the see-through trust property. Silicone/TPU pigtail jacket
warmer/grippier than PVC. Mold release spray already bought. Cure-test purple urethane
dye loads on dummy boards before committing. Stays backburner until AirGap is in motion.

### PowerVerify AirGap

First board arrived, potting in progress. Photograph (no bubbles, white background,
6-10 keeper shots), post Show & Tell to r/printedcircuitboard from personal account.
$39 pre-order, ships June 30.

---

## PART 4 — SOCIAL PRESENCE TACTICS (lessons learned)

### Account hygiene

- **u/zknot_io original DELETED** — kept getting shadowbanned, likely account-level
  flagged, unrecoverable. Rebuild as a legitimate paying business account when launch
  timing supports it. No rush.
- **Personal account (DistinctTradition200 / "sl33per")** carries the load. Bio updated
  to engineer-voice (removed the founder/CEO bio that was triggering self-promo flags
  across subs). The dual-bio mistake was real and was hurting post reception.

### Sub-by-sub lessons

- **r/AskElectronics:** works for CONCRETE technical questions (pull-up sizing), NOT
  architectural/philosophy posts (secure-element design). The "secure element" framing
  pulls the right audience for concrete questions. Hobby/repair register wins; over-
  polished posts get scrolled. The "50yo vet new to electronics" comment hit 7 upvotes —
  authenticity beats polish.
- **r/embedded:** the right home for MCU+peripheral architecture, firmware, real-time
  tradeoffs. Save deep technical posts for here. NEVER crosspost own content here from
  another sub (sub-farming flag).
- **r/cryptography:** hostile to anything resembling product validation. Removed the
  Juniper post. The ECDSA/nonce draft must drop questions that read as "evaluating a
  chip" — keep only the deterministic-vs-probabilistic ECDSA theoretical angle.
- **r/IOT, r/OTSecurity, r/digitalforensics, r/selfhosted:** these are where the
  RELATIONSHIP and MARKET conversations live. Engineer-curious voice, never pitch.
- **r/ATECC608:** founded (note: profile shows "r/ATECC608B" with 1 member — verify exact
  name). Welcome post, 8 rules, 8 flairs, AutoMod, 10 staggered seed posts planned.
  Wake-sequence content reserved for the founding post once the sub has 50+ subs. Do NOT
  cannibalize by also posting wake-sequence to r/embedded.

### Reddit metrics lesson (important)

Don't read early metrics as fate. Called the pull-up post "dead" twice (115 views, 2
downvotes early) — it ended at 2.2k views, 5 upvotes, 9 comments, 6 engaged engineers.
Reddit takes 2-3 days to bake. A post is alive for 24-48 hrs before scoring it.

### Voice principle (the meta-lesson)

Answer as if the PERSON matters, not as if the THREAD matters. Most replies optimize for
the lurking audience; the high-value ones optimize for the specific person. That builds
relationships, not karma. Do this only for people worth a relationship — go deep when
picked, ignore bots and one-liners.

Two voices in practice:
- With peer engineers (Ard-War): sharp, doing synthesis, "I was asking the wrong question."
- With domain practitioners (sk3tchcom, hiddentalent): curious outsider learning their
  world, never the expert, concede ground, ask bounded multiple-choice questions that
  are easy to answer.

### Technical correction handling

When a commenter corrects you and they're right (DuckOnRage on open-drain idle current),
acknowledge it FIRST and clearly before defending anything else. Engineers respect "you're
right, I had this backwards." It's a credibility builder, not a loss.

---

## PART 5 — TECHNICAL LEARNINGS BANKED (from the threads)

### I2C / pull-up / power (the pull-up thread)

- Open-drain pull-ups only sink current when something actively pulls the line LOW.
  Idle draw is ~zero (just leakage). The 1.5mA/line was PEAK during ACK bits, not idle.
  Real cost is per-transaction, not idle. I had this fundamentally backwards.
- For button-press-event-driven signing (bus idle 99%+), pull-up energy is a rounding
  error. Real battery budget killers: MCU sleep current, ATECC608B standby, wake/sleep
  transitions. CR2032 ≈ 220mAh; ~2µAh/day for the bus is 0.0009%/day. Pull-ups not in
  top 3 power concerns.
- Slower clock (50kHz) is NOT automatically lower power — wider bits = longer LOW time
  per byte. Likely correct: faster clock + stronger pulls (2.2k) within chip tolerance.
- Active buffers (TCA9617B, PCA9306) can be WORSE than fixed pulls — "hundreds of µA
  standby" kills a CR2032 budget. LTC4311 is better (<5µA shutdown, auto-detect, slew-
  limited) but probably unnecessary at low duty cycle. Switched-pull-up idea
  (pull-ups tied to MCU GPIO, parked low when bus idle) is clever and well-suited to the
  duty cycle — breadboard it. Watch GPIO sourcing (~3mA both lines low), startup ordering
  (drive GPIO high before wake), and absolute-max-ratings during wake.
- **Landing:** 2.2k fixed pulls, no active buffer, faster clock, stop optimizing the I2C
  lines because they're a rounding error.
- ACTION/AUDIT: review all ZKKey product copy for accuracy on idle-current / low-power
  claims given the open-drain correction.

### ATECC608B wake sequence (the saved content)

- Wake = deliberate I2C violation: hold SDA low ≥60µs (tWLO), release, wait ≥1500µs
  (tWHI) before addressing. Chip detects the long SDA-low pulse, not a byte.
- The "send 0x00 byte" trick is marginal — needs CONTIGUOUS SDA-low; SCL toggling
  releases SDA between bits. At 400kHz it's ~25µs (below 60µs threshold) and fails.
  Bit-bang the wake (deinit I2C, drive SDA as GPIO, hold ~80µs, release, wait ~2ms,
  reinit). Verify with logic analyzer.
- Gotchas: RTOS tick can preempt the 1500µs delay to 1499µs; breakpoints let the chip
  auto-sleep (~1.3s) mid-transaction; weak pull-ups + high capacitance = slow rise after
  wake; some ESP32 I2C peripherals don't fully release SDA on deinit; cold-boot tWHI can
  exceed 1500µs (measured up to ~1.8ms).
- This is reserved as the r/ATECC608 FOUNDING POST. Don't burn it on r/embedded.

### IoT identity architecture (the PaulHolland18 / r/IOT thread)

- His model: cloud-managed fleet, last-stage identity injection, NFC/QR sticker as
  physical anchor, single signed firmware update gated by revocation list, sticker
  irrelevant after user claims device. In production since 2014, large numbers.
- My model (opposite extreme): user-held device, identity generated on-die at first
  power-on, never leaves secure element, attestation via physical presence. Different
  threat domain — his defends a fleet against scaled compromise, mine defends individual
  signing events against firmware-level adversaries. COMPLEMENTARY, not competing.
- **Chip-swap attack answer (= the ZK-LocalChain elevator pitch, SAVE THIS):** if an
  attacker desolders the ATECC from PCB1 to PCB2, the chip happily signs for PCB2 (valid
  signature, same key — the chip doesn't know it moved). Defense lives ABOVE the chip:
  every signature anchored into a hash chain including prior device state, readings,
  timestamps, monotonic counter. PCB2 can produce a valid signature but not a valid
  CHAIN connecting back to PCB1's history — the gap is detectable by any verifier with
  the chain head. Chip-swap yields a new device starting its own chain from zero
  (observable), not forged history.
- TOFU is situationally (not categorically) dangerous — wrong for million-device fleets,
  fine for single-user devices where "first use" is a human pressing a button.
- Symmetric-vs-asymmetric: symmetric primitives have tighter security proofs, but "more
  secure" overstates it — they solve different problems (symmetric needs shared secret;
  asymmetric enables public verification without signing capability). Replay attacks are
  a PROTOCOL-layer issue (need nonce/timestamp/sequence), independent of which primitive
  — both fail to replay without them. Hash-chain link provides replay resistance here.
- "selfhosted" thread phrase worth keeping for ZKKey copy: hardware-bound keys change the
  outcome from "key is stolen and reused later" to "access is limited to the period of
  control."

---

## PART 6 — RELATIONSHIPS WORTH MAINTAINING

| Who | Where | Why | Status |
|---|---|---|---|
| contracting-bot | r/govcon | OTA/CSO/6.302-3 govcon path. Top 1% commenter. | Engaged, thread cooled |
| Character_Project715 | r/govcon | Federal CO, calibrated the sole-source reality. | Asked follow-up Qs |
| Fit_Tiger1444 | r/govcon | CSO suggestion. | Replied |
| PaulHolland18 | r/IOT | IoT identity, in-production since 2014, complementary architecture. Enjoys the convo. | Active, deep |
| Ard-War | r/AskElectronics | Top 1% Commenter, best technical answer on pull-ups. Peer-engineer vouching value. | Reply drafted, owed |
| sk3tchcom | r/OTSecurity | OT practitioner, bottom-of-stack reality. Bridge into OT domain. | Reply posted, awaiting |
| hiddentalent | r/OTSecurity | Security reviewer, top-of-stack reality + FDO + market profile. GOLD. | Reply drafted, owed |
| thenewestnoise | r/AskElectronics | Gave the switched-pull-up idea. | Engaged |
| DuckOnRage | r/AskElectronics | Corrected the open-drain premise (rightly). | Acknowledged |

Note: don't DM anyone first. Let them find the (now engineer-voiced) profile if curious.
hiddentalent may DM at some point — treat as separate thread if it happens.

---

## PART 7 — OPEN ACTIONS / NEXT STEPS

### Immediate (post-trip)
1. Post the owed replies (Ard-War first — r/AskElectronics decays fast; hiddentalent
   has more breathing room; both drafted in the deleted chat — reconstruct from Part 5/6
   notes if needed).
2. Photograph potted AirGap, post Show & Tell to r/printedcircuitboard.
3. Begin KiCad for ZKKey Connect Pico.
4. Test Arducam Mega 5MP on Pico with example code (capture a QR cleanly in <1hr = it's
   the part; else fall back to OV2640).

### Research (Adventure)
5. Read FDO spec (~80 pages). Audit reference impl + certified products. FDO vs ZKKey:
   compatible or competitive?
6. Build the "companies-like-Arable" list (8-12 across ag/water/environmental/energy/telecom).
7. Subscribe to r/OTSecurity, lurk 2 weeks, learn vocabulary (ICS, SCADA, PLC, HMI, DCS,
   IT/OT convergence, IEC 62443, NERC CIP, Purdue Model).

### Foundation (the only non-recoverable deadline)
8. Patent review: which of 19 provisionals convert vs lapse vs PCT. 12-month clock.
   Block 4 hrs. Add ZKKey Air optical-ingestion claim to next provisional batch.
9. SAM.gov renewal reminder for 2026-12-01.

### Build / setup
10. Build ZKNOT Voice Custom GPT (spec written, upload 3 docs, "Only me").
11. Print AI Stack cheat sheet, pin at workbench.
12. Open the four-chat bookmarks with templates pasted.

### Content (compounding, saved drafts)
13. Rework r/cryptography draft to deterministic-ECDSA-only, post when account-age is right.
14. Polish r/AskElectronics pull-up draft (already posted — this was the source thread).
15. Possible future post: "What I got wrong about I2C idle current" — authentic-voice
    retrospective, 7-10 days out.
16. Possible future post (30 days): "What I learned posting on r/OTSecurity for two weeks."

---

## PART 8 — THE CONVERGENCE (the one thing to remember)

Three independent threads — the r/govcon contracting conversation, the r/OTSecurity
market discovery, and the federal procurement landscape — are all pointing at the SAME
market: **critical infrastructure** (utilities, telecom, transportation, agriculture-at-
scale, oil/gas, water). High-value unattended assets, integrator-operated, physical-
access threat model, govcon-funded.

ZKKey's market is not consumer and not the cheapest devices. It's the intersection of
"threat model justifies the hardware" and "operator is mature enough to provision it."
That intersection is critical infrastructure, and it's also where OTA/CSO/SBIR money
flows. The patents + the products + the govcon path + the Reddit market signals all
converge here. Trust the convergence. Build toward it.

Tagline holds: Physics enforces. Math proves. You verify.
