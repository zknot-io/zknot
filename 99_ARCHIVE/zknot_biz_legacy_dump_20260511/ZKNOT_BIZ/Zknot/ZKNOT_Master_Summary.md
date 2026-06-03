# ZKNOT.IO - Master Project Summary
**Last Updated:** February 11, 2026  
**Owner:** William Wilkinson  
**Status:** Active Development - Bootstrap Phase

---

## BUSINESS OVERVIEW

### Core Mission
Build cryptographic event logging system (ZKNOT.IO) for offline evidence collection in environments with unreliable network connectivity.

### Bootstrap Strategy
- **Phase 1 (Now-6mo):** Sell 100+ crypto-authenticated keyboards to fund ZKNOT development
- **Phase 2 (6-12mo):** Launch ZKNOT.IO pilot programs with early customers
- **Phase 3 (12-24mo):** Scale via Axon licensing or Series A funding

### Revenue Model
```
Keyboards (Bootstrap):
- NullKey Corne: $450-550/unit
- Cost: $107/unit
- Margin: $343-443 (76-80%)
- Target: 100 units → $34,300 profit

ZKNOT.IO (Main Product):
- Evidence logger: $200-300/device
- Target market: Law enforcement, corporate forensics, compliance
- SAM: $520M-$1.25B
- Competitive advantage: Only solution with multi-day offline crypto integrity
```

### Key Metrics
- **First 100 keyboards:** March-June 2026 delivery
- **ZKNOT pilot:** Q2-Q3 2026 (10-20 devices)
- **Breakeven:** Month 3-4 (after ~50 keyboard sales)
- **Profitability:** Month 6+ (sustained $7k-15k/month from keyboards)

---

## INTELLECTUAL PROPERTY PORTFOLIO

### Patents Filed (8 Total, $590 Invested)

**Active Provisionals:**
1. **ZKey** - Human-Gated Cryptographic Attestation (physical button required for signatures)
2. **PowerVerify™** - Data-Blocked Power Delivery Interface (charging without data transfer)
3. **TrustSeal** - Tamper-Evident Physical Seal Crypto Binding
4. **ZK-LocalChain** - Device-Signed Evidence Ledger (original filing)
5. **Vendor-Irrevocable** - (details not specified, assumed filed)
6. **Evidence Protocol** - Evidence Integrity Protocol
7. **Offline-First Architecture** - App #63/978,480, filed Feb 9, 2026, expires Feb 9, 2027
8. **(One additional filing)** - Total count: 8 provisionals

**Critical Patent (Most Recent):**
- **App #63/978,480:** "Offline-First Cryptographic Evidence Collection System"
- **Filed:** February 9, 2026
- **Expires:** February 9, 2027 (12 months to convert to non-provisional)
- **Coverage:** Air-gapped architecture, multi-day battery operation, offline verification
- **Status:** This is the CORE competitive moat for ZKNOT.IO

### Defensive Publication Strategy

**White Paper (Ready to Publish):**
- **Title:** "Cryptographic Event Chain Synchronization Protocol for Intermittently-Connected Distributed Systems"
- **Purpose:** Create prior art to block competitors from patenting sync protocol
- **Timing:** Publish AFTER capstone defense (Week 15+, ~June 2026)
- **Targets:**
  - arXiv cs.CR (free, 24-48hr publication)
  - GitHub + Zenodo DOI (free, permanent citation)
  - IP.com (optional $150, strongest legal protection)
- **Strategic Split:**
  - Air-gapped architecture: PATENTED (business moat)
  - Sync protocol: PUBLISHED (blocks competitors, enables research)

### Trademarks
- **ZKNOT™** - Brand name
- **PowerVerify™** - Power-only charging device
- **ZKKey™** - Human-gated signing device
- **Status:** Applications filed or pending

---

## PRODUCT PIPELINE

### Product 1: NullKey Corne Keyboard (Bootstrap - NOW)

**Specifications:**
- Base: Corne 4.1 split keyboard (3x6 layout, 42 keys)
- Controller: RP2040 (NOT Pro Micro)
- Switch: MX hotswap sockets
- Case: Laser-cut acrylic plates (3mm black acrylic, sandwich style)
- Special feature: ATECC608B crypto authentication via ZKAuth module

**ZKAuth Module:**
- ATECC608B secure element (ECDSA P-256 signatures)
- Physical button (human-gated signing)
- LEDs (green/red status indicators)
- Optional: 0.91" OLED display
- Seeed XIAO RP2040 controller
- I2C connection to keyboard via JST-SH connector

**Firmware:**
- **Default:** QMK (pure, no VIA) - appeals to enthusiasts
- **Optional:** VIA build available for download (GUI remapping)
- **Custom keycode:** AUTH key triggers crypto signature workflow
- **Philosophy:** QMK-first positioning at $450 price point

**Production:**
- **Quantity:** 100 units (first batch)
- **PCBs:** JLCPCB, panelized 100x100mm (2 keyboards + 4 auth modules per panel)
- **Cases:** Ponoko laser-cut acrylic OR Craftcloud 3D printed
- **Timeline:** 
  - Design PCB: Tonight (Feb 11)
  - Order PCBs: Tomorrow (Feb 12)
  - Receive: March 2026
  - Ship to customers: March-June 2026

**Economics:**
- Cost: $107/keyboard (PCBs $35, switches/caps $29, case $15-20, misc $28)
- Price: $450-550
- Profit: $343-443 per unit
- Total profit (100 units): $34,300

### Product 2: ZKNOT.IO Evidence Logger (Main Product - Q2 2026)

**Hardware:**
- Platform: Raspberry Pi Zero 2 W
- Secure element: ATECC608B (same as keyboards)
- Custom PCBs: PowerVerify™ (charging), ZKKey™ (signing)
- Battery: 10,000 mAh (72+ hour operation validated)
- Storage: 32GB microSD (3.2M events capacity)

**Capabilities:**
- **Offline operation:** 72-78 hours on battery (exceeds 72hr requirement by 8%)
- **Cryptographic integrity:** SHA-256 hash chaining + ECDSA P-256 signatures
- **Tamper detection:** 100% (325/325 attacks detected in testing)
- **Synchronization:** Peer-to-peer, deterministic conflict resolution
- **Verification:** Offline, no network required

**Software:**
- 6 Python modules (~5,000-7,000 LOC)
- Testing: 247 unit tests, 90% coverage, 100% crypto module coverage
- Performance: 312 events/sec write (3x requirement)

**Compliance:**
- NIST SP 800-53 AU-9: Full compliance
- PCI-DSS 10.3.4: Full compliance
- HIPAA 164.312(b): Full compliance
- GDPR Article 32: Full compliance

**Target Market:**
- Rural law enforcement (evidence collection without network)
- Air-gapped secure facilities (classified, manufacturing)
- Compliance auditing (distributed organizations)
- International operations (hostile network environments)

**Competitive Advantage:**
- Only solution with cryptographic integrity during multi-day offline operation
- 10-100x longer offline duration than competitors (days vs hours)
- 50-350x lower TCO than commercial solutions (Splunk, Axon)
- Hardware security (ATECC608 vs software-only keys)

---

## HARDWARE TIMELINE

### JLCPCB Production Status

**Current Orders (In Production):**
- **PowerVerify™ PCBs:** 3-10 units, delivery March-April 2026
- **ZKKey™ PCBs:** 3-10 units, delivery March-April 2026
- **ATECC608 chips:** Integrated into above boards
- **Status:** Post-Chinese New Year production, expected Q1 2026

**Upcoming Orders (This Week):**
- **NullKey Corne PCBs:** 100 keyboards worth (200 halves)
- **ZKAuth modules:** 100-200 units (panelized with keyboards)
- **Order date:** February 12, 2026
- **Delivery:** March 10-20, 2026
- **Cost:** ~$1,250 for panelized PCBs

### Other Components (To Order This Week)

**Keyboards (100 units):**
- Switches: Gateron (AliExpress) - $1,400
- Keycaps: Blank PBT (AliExpress) - $1,500
- Cases: Ponoko acrylic plates - $1,500 (order in batches of 30)
- Cables: TRRS + USB-C (Amazon) - $500
- Hardware: M2 screws, standoffs, feet (AliExpress) - $125
- **Total:** ~$5,000 + $1,250 PCBs = $6,250 for 100 units

**Total Investment Required:** $6,250-7,000 (generates $34,300 profit)

---

## TECHNICAL DECISIONS & SPECIFICATIONS

### Corne Keyboard Design

**Layout:**
- 3x6 matrix (42 keys total, 21 per hand)
- NOT 3x5 (use all columns, don't leave keys unpopulated)

**Controller:**
- RP2040 (modern, cheaper, better than Pro Micro)
- USB-C on BOTH halves
- I2C over TRRS cable for half-to-half communication

**Case Construction:**
- **DECISION:** Laser-cut acrylic plates (NOT 3D printed)
- **Reasoning:** Premium feel at $450 price point, industry standard
- **Material:** 3mm black acrylic
- **Construction:** Sandwich style (top plate → PCB → bottom plate)
- **Hardware:** 8× M2 screws + standoffs per keyboard

**Firmware:**
- **Default:** Pure QMK (no VIA bloat)
- **Optional:** VIA build available for download
- **Positioning:** QMK-first appeals to target market (security-conscious enthusiasts)
- **Custom features:** AUTH keycode triggers ZKAuth module via I2C

### ZKAuth Module Design

**Connectivity:**
- I2C bus (shared with TRRS half-to-half connection)
- JST-SH 4-pin connector (STEMMA QT compatible)
- Pinout: GND, VCC, SDA, SCL

**Components:**
- ATECC608B: I2C address 0x60
- Seeed XIAO RP2040: Handles button, LEDs, I2C bridge
- Button: 6mm tactile, GPIO with 10kΩ pull-up
- LEDs: Green (ready), Red (signing)
- OLED: Optional 0.91" I2C display (address 0x3C)

**Authentication Flow:**
1. User presses AUTH key on keyboard
2. Keyboard sends I2C command to ZKAuth module
3. Module lights green LED, waits for button press
4. User presses physical button on module
5. Module lights red LED, generates ECDSA signature via ATECC608
6. Signature sent back to keyboard via I2C
7. Keyboard outputs signature as USB HID packet

**PCB Size:** 45mm × 22mm (fits in palm rest or external enclosure)

---

## CAPSTONE PROJECT STATUS

**Project:** Cryptographic Event Chain Synchronization for Systems with Unreliable Network Connectivity  
**Institution:** Western Governors University (WGU)  
**Program:** BS Cybersecurity and Information Assurance  
**Timeline:** February 10 - July 31, 2026 (20 weeks)  
**Status:** Documentation complete, ready for defense

### Deliverables Completed

**Documentation:** 158 pages total
- Phase 1 (A-A3): Problem definition - 15 pages
- Phase 2 (B-C): Stakeholders, historical data - 18 pages
- Phase 3 (D-D3): Implementation, rollout, risks - 28 pages
- Phase 4 (E-G1): Training, resources, deliverables, timeline - 43 pages
- Phase 5 (H-H4): Testing, evaluation, results, sign-off - 54 pages

**Technical Achievements:**
- ✅ 100% tamper detection (325/325 attacks detected)
- ✅ 78-hour battery life (exceeds 72hr requirement by 8%)
- ✅ 312 events/sec write performance (3x requirement)
- ✅ 98% usability success rate (exceeds 90% target)
- ✅ Full regulatory compliance (NIST, PCI-DSS, HIPAA, GDPR)
- ✅ 247 unit tests, 90% coverage

**Defense Date:** Late July 2026  
**Next Steps:** Defensive publication after defense approval

---

## IMMEDIATE ACTION ITEMS

### Tonight (Feb 11, 2026)
- [ ] Design NullKey Corne PCB (RP2040 + I2C + JST connector)
- [ ] Design ZKAuth module PCB (ATECC608 + button + LEDs)
- [ ] Panelize both into 100x100mm panel
- [ ] Generate Gerbers

### Tomorrow (Feb 12, 2026)
- [ ] Upload Gerbers to JLCPCB (order 5-10 panels)
- [ ] Upload BOM and CPL for assembly
- [ ] Order switches, keycaps, cables from AliExpress
- [ ] Order acrylic plates from Ponoko (first batch: 30 sets)

### Week 2-4 (Feb 17 - Mar 8)
- [ ] Set up QMK development environment
- [ ] Create custom keymap with AUTH key
- [ ] Write Arduino firmware for ZKAuth module
- [ ] Design laser-cut case files (.dxf)
- [ ] Create product page and marketing copy

### Week 5-6 (Mar 10 - Mar 23)
- [ ] Receive PCBs from JLCPCB
- [ ] Receive switches, keycaps, cables
- [ ] Assemble first prototype
- [ ] Flash firmware, test AUTH workflow
- [ ] Validate full crypto signature flow

### Week 7-8 (Mar 24 - Apr 6)
- [ ] Assemble 10 beta units
- [ ] Ship to early adopters / reviewers
- [ ] Collect feedback
- [ ] Launch on r/mechanicalkeyboards, r/olkb

### Month 3-6 (Apr - Jun 2026)
- [ ] Assemble and ship remaining 90 keyboards
- [ ] Bank profits ($30,000+)
- [ ] Use profits to fund ZKNOT.IO development
- [ ] Consider QIDI Max4 printer after 50+ sales ($1,199)

---

## KEY DECISIONS MADE

### Business Strategy
✅ Bootstrap with keyboards (NOT investors, NOT unrelated products like BadUSB)  
✅ Focus on products using same tech stack (ATECC608, crypto, PCB design)  
✅ Target: 100 keyboard units → $34k profit → fund ZKNOT  
✅ Raise angel round AFTER proving demand (Month 6+, better terms)

### Product Design
✅ Use Corne 4.1 as base (proven, MIT license, open source)  
✅ Laser-cut acrylic cases (NOT 3D printed for first 100)  
✅ QMK-first firmware (VIA available as optional download)  
✅ Panelized PCB production (100x100mm = 2 keyboards + 4 modules)  
✅ MX switches, 3x6 layout, hotswap sockets

### Manufacturing
✅ JLCPCB for PCBs (already have relationship, proven quality)  
✅ Ponoko for acrylic cases (professional quality, fast turnaround)  
✅ AliExpress for switches/keycaps (bulk pricing, acceptable quality)  
✅ No printer purchase until Month 6+ (after 50+ sales)

### Positioning
✅ Price: $450-550 (premium tier, justifies crypto features)  
✅ Target: Security-conscious enthusiasts + QMK purists  
✅ USP: "Only keyboard with cryptographic authentication"  
✅ Brand: "NullKey" (edgy, memorable, hacker aesthetic)

---

## LONG-TERM ROADMAP

### Phase 1: Bootstrap (Months 1-6, Feb-Jul 2026)
- Sell 100 NullKey keyboards
- Revenue: $45,000
- Profit: $34,300
- Outcome: Fully funded ZKNOT development, zero dilution

### Phase 2: ZKNOT Pilot (Months 6-12, Jul 2026-Jan 2027)
- Launch ZKNOT.IO with 10-20 pilot devices
- Target customers: 2-3 law enforcement agencies, 1-2 corporate forensics teams
- Collect testimonials and case studies
- Refine product based on feedback

### Phase 3: Growth (Months 12-24, Jan-Dec 2027)
- Option A: Axon licensing deal (preferred, maintains control)
- Option B: Series A funding ($1-3M at $10-20M valuation)
- Option C: Continue bootstrapping with direct sales
- Decision based on: Market response, cash needs, strategic opportunities

### Phase 4: Scale or Exit (Months 18-36)
- Acquisition by Axon or competitor ($10-50M range)
- OR: Scale independently with VC backing
- OR: Profitable niche business (bootstrapped forever)

---

## LESSONS LEARNED & PRINCIPLES

### IP Strategy
- Patent the MOAT (air-gapped architecture), publish the COMMODITY (sync protocol)
- Defensive publication blocks competitors, enables research community
- Provisional patents buy 12 months, convert only what's essential to business model

### Product Development
- Test-driven development for security-critical code (100% crypto test coverage)
- Hardware simulation enables development before physical devices arrive
- Battery life requires measurement, not estimation (theoretical vs actual: 4.0d vs 3.25d)

### Business Building
- Bootstrap with focused products (same tech stack, same customers)
- Don't buy equipment before proving demand
- QMK-first positioning differentiates at premium price points
- VIA optional = capture both markets without compromising vision

### Market Understanding
- $450 customers are tech-savvy (can handle QMK if needed)
- Security-conscious buyers appreciate hardware crypto (ATECC608 is the draw)
- Premium keyboards use acrylic plates, not 3D printed cases
- "Maker-friendly" positioning works for split keyboards (caseless editions viable)

---

## CONTACT & RESOURCES

### GitHub Repositories
- QMK Firmware: https://github.com/qmk/qmk_firmware
- Corne Base: https://github.com/foostan/crkbd
- (Your repos to be created after PCB design)

### Suppliers
- **PCBs:** JLCPCB.com (China, 2-3 week delivery)
- **Cases:** Ponoko.com (laser-cut acrylic) OR Craftcloud3D.com (3D printing)
- **Switches/Keycaps:** AliExpress (bulk pricing)
- **Secure Elements:** LCSC.com or Mouser.com (ATECC608B)

### Community
- r/mechanicalkeyboards (130k+ members)
- r/olkb (20k+ members, QMK enthusiasts)
- r/ErgoMechKeyboards (40k+ members, split keyboard users)

---

## NOTES FOR FUTURE CLAUDE CHATS

**When starting a new chat, provide this context:**
- "I'm building ZKNOT.IO, a crypto evidence logger"
- "Currently bootstrapping with NullKey keyboards (Corne + ATECC608 auth)"
- "Here's my master summary [upload this doc]"
- "I need help with [specific task]"

**This summary covers:**
✅ Business strategy (keyboards → ZKNOT)  
✅ IP portfolio (8 patents, defensive pub plan)  
✅ Technical specs (hardware, firmware, design decisions)  
✅ Timeline (tonight: design, tomorrow: order, March: ship)  
✅ Economics (cost, pricing, profit margins)

**Update this doc when:**
- Major decisions change (e.g., pivot to VIA-first firmware)
- New products added to pipeline
- IP filings or publications occur
- Timeline shifts significantly

**Last Updated:** February 11, 2026

---

*This document represents the complete strategic and technical context for ZKNOT.IO and NullKey keyboard development. Use it to quickly onboard AI assistants, team members, or advisors without re-explaining the entire business from scratch.*
