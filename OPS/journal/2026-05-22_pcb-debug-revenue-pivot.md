# 2026-05-22 — PCB Debug Findings + Revenue-First Pivot

**Author:** William Shane Wilkinson
**Topic:** ZKKey Connect Rev A diagnosis, Rev B decision, and shift from acquisition-track planning to revenue-first survival plan
**Status:** Decisions captured — thread to be deleted

---

## 1. ZKKey Connect Rev A — Why the boards don't work

Two PCB files reviewed (`ZKKey_Connect_RevA.kicad_pcb` and `ZKKey_Connect_RevA__1_.kicad_pcb`). The second file is a cosmetic tidy-up only (added comments, justify tags, removed tstamps, newer zone syntax). **None of the electrical faults were fixed between revisions.** Boards were fabbed at JLCPCB and are physically dead.

### Show-stopper faults (board cannot work)

1. **LED current-limit resistors R1–R4 are shorted across themselves.** Both pads of each resistor sit on the same net (e.g. R1 pad1 and pad2 both on `LED_PWR_PA1`). No series resistance — MCU GPIO drives the LED directly. Damages GPIO or LED on power-up. This is the #1 fault. Fix: each resistor needs pad1 on the MCU GPIO net and pad2 on a NEW net (e.g. `LED_PWR_A`) going to the LED anode. Four new nets, four resistors in series.
2. **AMS1117-3.3 has pin 2 defined twice** with different positions/sizes. SOT-223-3 correct pinout: pin1=GND, pin2=Vout (also the tab), pin3=Vin. Footprint is malformed — pick one definition for pin 2.
3. **Power rails are unrouted.** Segments exist only for USB D±, I²C, SWD. No traces for +5V (VBUS→regulator) or +3.3V (regulator→MCU/ATECC). GND zones handle ground, but the board has no path to power up.
4. **STM32 power-pin assignments wrong.** Pin 1 and pin 2 both tied to +3.3V. On LQFP-48, pin 1 = VDD (correct) but pin 2 = PC13, not a power pin. Verify all VDD/VSS pins against the STM32F072CBT6 datasheet before any refab.
5. **Test points TP1–TP7 placed at x=0** — on the board edge (Edge.Cuts 0,0→60,40). They'll be cut off by the router. Move inboard ≥1mm.

### Likely problems
- No bulk cap on VBUS itself (USB spec wants 1–10µF near connector).
- No ferrite/filter on STM32 VDDA analog supply.
- 8MHz crystal may be unnecessary — STM32F072 has internal HSI48 for USB. BOM cost only, not a bug.

### Root cause
The `.kicad_pcb` appears to have been hand-edited with no matching `.kicad_sch` schematic. **KiCad DRC checks geometry, not netlist sanity** — it will NOT catch the LED short or unrouted power, which is why DRC passed and the boards still failed. ERC on a schematic WOULD have caught all of it. **Lesson: build the schematic first, run ERC, then lay out the PCB. Never hand-edit a .kicad_pcb again.**

---

## 2. Rev B decision

**Decision: do NOT rush a Rev B refab.** A bigger board with bigger components inherits the same broken netlist. Spinning Rev B without first building a proper schematic = same dead board.

When Rev B is built (no rush, post-revenue):
- **Use STM32F411 (Black Pill), not F072** — firmware already written, Gate 1 closed on it. Don't change MCUs mid-stride.
- Build `.kicad_sch` schematic FIRST → ERC → then layout.
- 1206 passives, SOIC packages, LQFP not QFN (Whizoo reflow handles all of these fine).
- Bigger board (~80×60mm) for routing headroom — JLCPCB price barely changes.
- Order 5 boards, not 20. ~$35 boards + ~$20 customs + ~$40 shipping = ~$95 for 5.

**Existing Black Pill + ATECC608B prototypes are sufficient for any demo needed right now.** No new PCB required to record a working demo.

---

## 3. The financial reality check (the core pivot)

Reviewed `ZKNOT_DOC-003_SpendTracker`. Findings:

- Total posted spend Jan–Apr 2026: **~$9,200**
- **$0 revenue.** Not "pre-revenue" — actually zero.
- Whizoo Controleo3 loan (was $1,395 @ 35.99% APR) — **NOW PAID OFF.** Biggest bleeder gone.
- Bambu P1S loan (~$89/mo, 6mo) presumably continuing.

### Current credit position (as of this thread)
- CapOne ···1867: ~**$1,500 available** of $5,000
- PayPal CC ···8937: ~**$4,000 available** of $5,000
- ~**$5,500 total available credit**
- Can cover all debt payments comfortably for **~4 months**
- Goal: a couple hundred $/week → debt-free fairly quickly

### Spending pattern flagged (the real risk)
Not a budget problem — a **purchase-trigger problem**. Every problem felt solvable by buying a tool:
- 27 Namecheap domains (need 1–2, not 27)
- $1,585 Saleae Logic Pro 16 (Logic 8 at $400 does I²C debug fine)
- $693 Andonstar AD409 microscope + Godox light
- $216 GetFPV drone parts (future vertical, premature)
- $4,173 of lab gear in 7 weeks, none of which ships product
- 23 line items flagged "identity TBD" — orders not remembered

Lab + 14 provisional patents are real and valuable. The lab is premature; most of it duplicates what a multimeter + $25 USB scope + hot air station can do. **The pattern, continued, ends with running out of runway debugging things that didn't need debugging.**

---

## 4. The strategic corrections (all confirmed)

These were all the operator's own instincts, validated:

- **Acquisition plan dates were arbitrary** and assumed a budget that doesn't exist. Do NOT email Axon/Cellebrite/Motorola yet — pre-revenue + no SDVOSB + no issued patent + no pilot customer = archived email + wasted first impression. Right time is post-issued-patent AND with ≥1 pilot customer logo.
- **Verticals (journalism, LEO chain-of-custody, manufacturing, election integrity) not yet built** — don't chase all of them. Pick one. PowerVerify copy already implicitly chose: travelers / journalists / lawyers. Win by depth, not breadth.
- **SDVOSB still pending**, taking longer than wanted — out of operator's control. Stop optimizing around it.
- **Don't rewrite the business plan.** Rewriting strategy docs feels like progress but isn't. Already too many strategy docs. The fix isn't new aspirational dates.

### Patent timeline correction
PAT-001 (App 63/960,933) filed **Jan 15, 2026** → non-provisional due **Jan 15, 2027** (~9 months runway), NOT June 2026. Most provisionals get abandoned. Convert only the 2–3 strongest (likely PAT-001 ZKKey, PAT-002 PowerVerify, maybe PAT-005 TrustSeal) at ~$5–8K each with a real attorney. Don't convert all 14.

---

## 5. THE PLAN — revenue first

**The only question that matters: how to make $200–300/week, sustained, until debt-free.**

### PowerVerify AirGap math ($39 unit)
- ~$5 BOM + ~$4 ship/packaging = ~$9 cost → ~$30 net/unit
- 7 sales/week = $210/wk = debt-free pace (the floor)
- 10 sales/week = $300/wk = debt-free + patent savings
- Parts already on hand (Jan 27 DigiKey BOM: LEDs, PTC fuses, 1N5822 Schottky, resistors)

### Current state of the funnel
- PowerVerify boards **printed, awaiting DHL pickup in China** — ETA guess **Wed**, confirm on tracking number.
- Shopify page exists but says "Pre-Order, ships June 30" — **kills conversion.** Change to a specific near-term ship date once tracking lands.
- Gumroad guides **already listed** (6 guides: free Black Pill front door, $9 each others, $29 bundle). Not selling — expected, they need traffic, don't sell themselves.
- Reddit: posting karma-builder content on **personal account**. ZKNOT account too new (auto-filtered on r/privacy, r/cybersecurity, r/digitalnomad — need 30+ day age, 50+ karma).

### Reddit decision
**Post product content from the personal account.** Founder posting their own product from a personal account is more authentic and outperforms a corporate account anyway. Reddit hates corporate accounts, loves builder stories. Age the ZKNOT account in parallel if wanted (comment in r/embedded, r/electronics for 30 days) but don't block on it.

### Asset liquidation (bridge to debt-free in ~2 weeks)
**Will NOT sell ZKNOT lab assets** (Saleae, AD409, Bambu, NUCLEO, etc.) — guaranteed future use, real leverage. Correct discipline.
**Selling personal collectibles instead:** fountain pens, comic books, cybersecurity gear (Ethernet tap, etc.). Faster cash, smaller emotional cost. List on eBay/Mercari this weekend.

### OMG cable for demo — cautions
- Buying an O.MG cable (~$120) for the demo. Real money in this situation — consider whether Hak5's existing explainer/marketing content suffices instead.
- **Don't need it to fire a live attack** — only need to show a normal-looking cable COULD be malicious and PowerVerify physically blocks it.
- **Don't post live-attack video** (keystroke injection/exfil) — YouTube etc. demonetize/remove offensive-tool footage. Stick to threat-model framing.

---

## 6. Product launch sequence (discipline: one product validates before the next launches)

1. **PowerVerify AirGap ships → first 5 sales.** Proves the funnel (pricing, conversion, fulfillment time, copy).
2. **Then add ZKKey Connect pre-order** — pick ONE platform (Black Pill for product since firmware exists; Pico2 is the better DIY-guide front door). Don't offer both — choice paralysis kills small-shop conversion. 3D-printed case: matte black PETG, recessed SIGN button, laser-engraved logo plate → looks $79 not $39. Design matters more than the printer.
3. **Then add ZKKey Air pre-order** if Connect validates. Aluminum case: use **stock Hammond 1455-series ($15–20)**, NOT custom-machined ($30–60/unit kills margin at qty 1).
4. **Gumroad guides** can run in parallel (free/low-cost, serve as email capture for the hardware funnel).
5. **Own-website storefront** = future ops program, not now.

**Do NOT launch all three SKUs at once.** A store that's done $0 can't support three simultaneous launches; none get the focus to actually sell.

---

## 7. Strongest marketing asset (don't bury it)
The single best line across all docs:
> "Look through the clear heatshrink. You can see there are no data lines."
That transparency/verifiability hook IS the story. Veteran-owned + made-in-USA + "verify, don't trust" + the FBI juice-jacking warning = a real, postable narrative. Lead with it. Don't bury it under acquirer-pitch language.

---

## 8. Immediate next actions (ranked)

1. **Confirm board ETA** on tracking number (drives everything).
2. **List fountain pens + comics** on eBay/Mercari this weekend (faster cash than the cyber gear).
3. **Update Shopify** to a specific near-term ship date the moment tracking lands — kill the "Pre-Order June 30" friction.
4. **Draft Reddit post for personal account** — founder voice, real story, photo of transparent heatshrink, soft CTA. Do NOT fire until product is in hand and shippable within 24h of order.
5. **Build 10 PowerVerify units** the weekend boards arrive.
6. **One Hacker News Show HN** once photos + page + fulfillment are solid. One shot.
7. **For 30 days: nothing else.** No new patents, no PCB rev, no acquirer outreach, no strategy-doc rewrites, no new DigiKey/Amazon orders, no new domains.

**30-day signal test:** $800–1,200 revenue = a business with a heartbeat, keep going. ~$200 = the offer/price/story needs work (not more inventory, not more planning).

---

## 9. Emergency-capital note (psychological backstop, not an action)
If ever truly cornered, ZKNOT lab gear is ~$2,000 of liquid emergency capital (Saleae ~$1,200, AD409 ~$400, Bambu ~$400 used). Not selling it — but knowing it's there means the situation is less cornered than the loan payments feel. Don't price-pressure PowerVerify out of panic.
