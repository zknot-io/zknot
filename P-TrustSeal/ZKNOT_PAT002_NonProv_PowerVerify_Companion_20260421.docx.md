**ZKNOT, INC.**

**PAT-002 NON-PROVISIONAL**

**POWERVERIFY COMPANION**

The PowerVerify-Specific Playbook

*Supplement to ZKNOT\_PAT001\_NonProv\_MasterGuide Vol 1 & 2*

App\# 63/961,118  |  Filed 2026-01-15  |  Priority Date: 2026-01-15

**NON-PROVISIONAL DEADLINE: January 15, 2027**

Strategic target: July 31, 2026 · Attorney engagement: June 30, 2026

Inventor: William Shane Wilkinson

ZKNOT, INC.  |  UEI: C4SKW13JPEL5  |  CAGE: 1AHZ4  |  EIN: 36-5165991

Veteran-Owned Small Business  |  SDVOSB  |  ops@zknot.io

Document Date: 2026-04-21

# **SECTION 1: HOW TO USE THIS COMPANION**

This document is the PowerVerify-specific supplement to the PAT-001 Non-Provisional Master Guide (Vols 1 and 2, April 16, 2026). It does NOT repeat the general patent-law content — for that, refer to the PAT-001 guide directly.

## **1.1 What this Companion covers (PAT-002 specific)**

| Section | Covers | Parallel to PAT-001 guide |
| :---- | :---- | :---- |
| **2** | Status, deadlines, fee math for PAT-002 | Vol 1 §1.3, Vol 2 §9 |
| **3** | The PowerVerify invention in depth — three-layer architecture | Vol 2 §6 (ZKKey) — different invention |
| **4** | Prior art landscape for power-only USB devices | Vol 2 §5.2 (ZKKey) — completely different space |
| **5** | Sample claims for PAT-002 with analysis | Vol 1 §4.8 (ZKKey sample claims) |
| **6** | PAT-018 CIP strategy — PowerVerify Plus | New; no PAT-001 equivalent |
| **7** | Prosecution-risk differences: §101 Alice, §103 obviousness vs. juice-jacking prior art | Vol 2 §7.4 (ZKKey scenarios) — different risk profile |
| **8** | The PowerVerify portfolio role | Vol 2 §10 — updated |

## **1.2 What to read in the PAT-001 guide**

For these topics, the PAT-001 guide applies to PAT-002 without modification:

* Vol 1 §2: U.S. patent law fundamentals (35 U.S.C. § 101/102/103/112/119(e))  
* Vol 1 §3: anatomy of a non-provisional (specification, claims, abstract, drawings, ADS, IDS, fees)  
* Vol 1 §4: claim drafting rules (comprising vs. consisting, independent/dependent, apparatus/method/system)  
* Vol 2 §5.1, 5.3, 5.4: prior art fundamentals and search methodology  
* Vol 2 §7: prosecution timeline and Office Action mechanics  
* Vol 2 §8: working with your attorney  
* Vol 2 §9: USPTO fees and Patent Center filing mechanics  
* Vol 2 §11: pro se practice  
* Vol 2 §12: glossary

This Companion writes only what is different about PAT-002. If a topic isn't here, look in the PAT-001 guide.

# **SECTION 2: PAT-002 STATUS AND DEADLINES**

## **2.1 Where PAT-002 stands as of April 21, 2026**

| Item | Value |
| :---- | :---- |
| **Application number** | 63/961,118 |
| **Filing date / priority date** | January 15, 2026 |
| **Title** | Power-Delivery Interface With Physical Data-Path Elimination and Verified Power-Only Operation |
| **Short name** | PowerVerify |
| **Non-provisional deadline (absolute)** | January 15, 2027 |
| **Strategic target date** | July 31, 2026 |
| **Attorney engagement target** | June 30, 2026 |
| **Non-provisional draft status** | COMPLETE as of March 28, 2026 |
| **Prior art search status** | COMPLETE as of March 28, 2026 |
| **Related continuation** | PAT-018 (PowerVerifyPlus) filed March 17, 2026 as a CIP extension |
| **Budget allocated** | $3,000 (attorney-assisted conversion) |

## **2.2 Critical dates for PAT-002**

| Date | Event | Consequence of missing |
| :---- | :---- | :---- |
| **2026-06-30** | STRATEGIC: engage patent attorney for PAT-002 | Compresses July 31 target; may push to October |
| **2026-07-31** | STRATEGIC TARGET: non-provisional filed | Acquisition data room weakened; Axon pitch loses 'recently converted' claim |
| **2027-01-15** | ABSOLUTE DEADLINE: non-provisional on file | UNRECOVERABLE. Priority date lost forever. PAT-018 CIP also becomes unmoored. |

The January 15, 2027 deadline is statutory under 35 U.S.C. § 119(e) and is not extendable. See Vol 1 §2.2.

## **2.3 Fee math for PAT-002 (micro entity)**

Same fee structure as PAT-001. Confirm micro-entity status (§9 of Vol 2\) has not changed since the January 15, 2026 provisional filing — specifically, that ZKNOT revenue has not crossed the gross-income threshold (\~$216,000 as of 2025, adjusted annually).

| Fee | Micro entity |
| :---- | :---- |
| **Basic filing** | $64 |
| **Search fee** | $280 |
| **Examination fee** | $320 |
| **Total at filing** | $664 |
| **Typical attorney cost (draft review \+ prosecution)** | $3,000 |
| **Pro-se total (first filing only, no prosecution)** | $664 \+ \~40-80 hours of your time |

# **SECTION 3: POWERVERIFY — THE INVENTION IN DEPTH**

This section mirrors Vol 2 §6 of the PAT-001 guide but covers PowerVerify instead of ZKKey. If you're using the claim set, prior art arguments, or attorney brief from this doc — start here.

## **3.1 The core insight — why PowerVerify is novel**

Every USB data blocker on the market today uses one of two approaches: (a) physically cut D+/D- lines, or (b) use resistors or ICs to present as a 'charger' without enabling data. In both cases, the approach is reactive: the device stops data from flowing, but produces no evidence that data did not flow, no record of what power was delivered, and no cryptographic assurance that the device was not tampered with or bypassed.  
PowerVerify's novelty is the combination of three elements, none of which individually is new but together constitute a system no prior product or patent covers:

* Physical elimination of data-capable conductors (not switched, not gated, not filtered — absent from the circuit)  
* Power Delivery negotiation preserved on CC lines so fast charging (up to 100W USB-PD) is not sacrificed  
* Verified power-only operation — the absence of USB enumeration itself serves as proof, and optional cryptographic session logging extends this proof to a signed, third-party-verifiable record

No commercial product and no published patent (as of the April 2026 prior art search) combines all three. Products like PortaPow, Plugable USB-MC1, and the generic 'USB condom' achieve element 1 and sometimes element 2 — none achieve element 3\.

## **3.2 The three-layer architecture**

### **Layer 1 — Physical Elimination (the hardware gate)**

The foundational claim. D+, D−, TX1±, TX2±, RX1±, RX2±, SBU1, and SBU2 conductors are not present between the source connector and the device connector. This is stronger than 'disconnected' because a disconnected conductor can, in principle, be reconnected by a switch, a relay, or a solid-state multiplexer. An absent conductor cannot be enabled by firmware, malware, software configuration, or adversarial actuation. There is no path to enable.  
Physical implementation options documented in the provisional:

* USB-C: use a 6-pin power-only USB-C receptacle (GCT USB4135 or equivalent) where the data pins do not exist in the connector housing at all  
* USB-C: standard 24-pin receptacle with data pins physically unconnected to any trace on the PCB  
* USB-A: two-pin or three-pin (VBUS, GND, optionally shield) footprint with D+/D- not routed  
* Lightning / proprietary: analogous removal of data-carrying pins

### **Layer 2 — Power Negotiation Preservation (the PD layer)**

A dumb USB data blocker — two wires, VBUS and GND — typically charges at 500mA or less because the device cannot negotiate a higher power profile. This is the commercial complaint with 'USB condoms': they kill fast charging. PowerVerify preserves full USB Power Delivery by including CC-line management:

* CC1 and CC2 from the source connector are routed to a PD controller IC (WCH CH224K or equivalent)  
* The PD controller negotiates a specific voltage profile (5V/9V/12V/15V/20V) via the CC lines  
* VBUS and GND pass through to the device at the negotiated voltage  
* At no point do CC-line messages cross into D+/D- or any other data-capable channel

The PD protocol itself uses only CC lines for negotiation — no data is carried on CC. This is by design in the USB-C specification. PowerVerify exploits this architectural separation to allow full fast-charging while maintaining the data-absence property.

### **Layer 3 — Verified Power-Only Operation (the proof layer)**

The distinguishing claim relative to all prior data blockers. Two sub-embodiments:

* Passive: the absence of USB enumeration itself serves as proof of power-only operation. A connected device cannot enumerate without D+/D- — if no enumeration occurs (observable via the device's USB state or via host-side logs), data could not have flowed  
* Active (PAT-018 CIP): the device includes a microcontroller and secure element (ATECC608B) that signs a session record including power parameters, tamper state, and absence-of-enumeration attestation. Verifiable offline by any third party via the device public key.

The passive embodiment is what every $10 AirGap-style consumer unit ships with. The active embodiment is the PowerVerify Pro / PowerVerify Plus forensic-tier product, and is the subject of PAT-018.

## **3.3 The inventive step — what the examiner will focus on**

During examination, the USPTO examiner will probe the boundary between PowerVerify and prior-art USB data blockers. Here is what the examiner will almost certainly say, and what the defense is:

| Examiner likely rejection | PowerVerify defense |
| :---- | :---- |
| **'PortaPow et al. already disconnect D+/D- while charging. Your claim is anticipated.'** | PortaPow does NOT negotiate USB-PD — it provides fixed 5V only (or uses resistor networks for Apple/Samsung fast-charge signaling, not USB-PD). PowerVerify claims BOTH physical absence AND full PD negotiation. Cite specific CC-line architecture in claim language. |
| **'Plugable USB-MC1 charges faster than 500mA with resistor signaling. That's enough.'** | Resistor-based charge signaling (the Plugable approach) caps at \~2.4A and does not implement USB-PD. PowerVerify claims USB-PD up to 100W via a controller IC managing CC1/CC2. Qualitatively and quantitatively different. |
| **'Combining a PD controller with a USB data blocker is obvious to a PHOSITA.'** | No published combination before January 15, 2026\. The prior art universally treats 'USB data blocker' and 'USB-PD fast charger' as separate products. The combination is not merely additive — it required recognizing that CC lines can be managed without crossing into any data channel. |
| **'§101 Alice: this is an abstract idea (data blocking).'** | Alice does not apply to hardware claims. PowerVerify claims a physical interconnect topology (claim 1: 'a primary connection interface... such that no electrical path exists'). This is a device, not an algorithm. Alice targets abstract software methods. |
| **'§112(a): the specification doesn't enable a PHOSITA to build this.'** | The provisional describes D+/D- routing options, CC-line management via CH224K or equivalent, and the GCT USB4135 6-pin receptacle approach. Supplement with ZKNOT Rev 1 KiCad files in the IDS if needed. |

## **3.4 The commercial embodiment — AirGap / PowerVerify Rev 1**

The commercial embodiment shipping under the consumer name 'AirGap' implements the passive (Layer 1 \+ Layer 2\) version:

* Board: 30mm × 90mm through-hole prototype, fitting a 1.5" clear heatshrink enclosure  
* Source-side connector: GCT USB4135 6-pin power-only USB-C receptacle (SMT, data pins not present in housing)  
* Device-side pigtail: short hardwired USB-C cable (4 wires: VBUS, GND, CC1, CC2 only — no D+/D-/SBU wires)  
* PD controller: WCH CH224K SOIC-8, configured via CFG1/2/3 jumpers for 5V/9V/12V/15V/20V selection  
* Power protection: TVS (P6KE5V6A), ferrite bead (BLM21PG600SN1D), Schottky diode (1N4007)  
* Status indication: two LEDs (green PWR, blue PG)  
* Visible proof: clear heatshrink enclosure, silkscreen labeled 'D+ / D− / SBU · NOT CONNECTED' with outline of absent traces

The PowerVerify Plus forensic embodiment (ATECC608B \+ session signing \+ tamper evidence) is PAT-018 and is covered in §6 below.

## **3.5 How to explain PowerVerify to different audiences**

### **To a journalist**

PowerVerify is a USB cable you can verify. Every other data blocker on the market asks you to trust that it works — you plug it in, and hope. PowerVerify lets you see the gap. The clear enclosure shows there are no data wires. The connector itself has no data pins. Data physically cannot flow. And the enterprise version cryptographically signs a record of every charging session so a journalist or investigator can prove, later, that their device wasn't compromised during a specific charging event.

### **To an investor**

The USB data blocker market is $30-50M annually and commoditized — every unit is a $5-10 plastic dongle with indistinguishable internals. PowerVerify patents a three-element combination that none of the existing vendors can replicate without a license: physical data absence, preserved USB-PD fast charging, and optional cryptographic session attestation. Base consumer units sell at $29-49; forensic-tier units with signing capability sell at $149+. Total addressable: every enterprise, government, and compliance-driven customer who has read an FBI/FCC/TSA juice-jacking warning and wants a defensible tool.

### **To an acquirer (Axon, Cellebrite, Motorola Solutions)**

PowerVerify is the hardware foundation of a verifiable-evidence chain of custody. Every chain-of-custody standard (FBI, DoD, Federal Rules of Evidence) treats power integrity as an evidentiary gap — 'we can't prove the device wasn't tampered with during charging.' PowerVerify closes that gap at the hardware level. The CIP extension (PAT-018) adds tamper-evident housing, multi-layer integrity attestation, and a sealed secondary verification interface, producing signed session records admissible as evidence. This is protocol-level, not product-level: any device that combines physical data absence with cryptographically signed power sessions is covered.

### **To a patent examiner (through your attorney)**

Prior art of record discloses physical D+/D- disconnection (PortaPow, Plugable USB-MC1, generic USB condoms). Prior art of record discloses USB-PD negotiation ICs (Cypress CCG, TI TPS65982, WCH CH224K). No prior art combines these with the specific architectural constraint that CC-line negotiation is preserved while all data-capable conductors are physically eliminated from the circuit. The claim language (Claim 1: 'a primary connection interface with physical elimination of all data-capable conductors, such that no electrical path exists between power source and powered device on any data conductor; a Power Delivery subsystem that negotiates voltage and current levels via CC lines only') captures this combination. The dependent claims and continuation CIP (PAT-018) add the cryptographic session logging and tamper-evidence elements that further distinguish from prior art.

# **SECTION 4: PRIOR ART LANDSCAPE FOR PAT-002**

This section is parallel to Vol 2 §5.2 of the PAT-001 guide, but PowerVerify lives in a completely different prior-art space than ZKKey. The relevant universe is USB security devices, power-delivery controllers, and physical data blockers — not cryptographic attestation.

## **4.1 The four families of prior art**

| Prior art family | Representative examples | Relevance to PAT-002 |
| :---- | :---- | :---- |
| **Consumer USB data blockers (commercial products)** | PortaPow USB Data Blocker; Plugable USB-MC1; USB Condom (int3.cc); JSAUX, BUISAMG, Rixmie (Amazon generics) | Closest prior art. Discloses D+/D- physical disconnection. Does NOT disclose USB-PD negotiation preservation. |
| **USB power-delivery controller ICs** | WCH CH224K (used in PowerVerify Rev 1); Cypress CCG series; TI TPS65982; Infineon USB-PD controllers | Commodity components. Not prior art for the SYSTEM, but prior art for the controller function. Claim 1 distinguishes because none of these controllers alone achieves physical data-path elimination. |
| **USB security research (academic and trade literature)** | Krebs 2011 juice-jacking story; Mactans 2013 (Georgia Tech); Wall of Sheep DEFCON 2011-2024; Symantec Trustjacking 2018; DOE 2016 DEFCON charging station incident | Establishes the problem (the motivation). Not prior art for the claim itself — these are attacks, not defenses. |
| **Granted patents in the USB-power / USB-security space** | See §4.3 below — specific patents to distinguish | Most important category for legal prior-art defense. Each must be distinguished in the IDS and potentially during prosecution. |

## **4.2 The critical distinction — what no prior art does**

In the March 2026 prior art search, no single prior-art reference discloses:

* All three elements (physical data absence \+ CC-line PD preservation \+ verifiable power-only operation) in a single device  
* Physical data-path ELIMINATION (absence, not disconnection or gating) combined with CC-line PD negotiation  
* Signed session records attesting to power-only operation (this is the PAT-018 CIP territory)

This is what your patent claims. Every examiner rejection and every invalidity challenge must be answered by returning to this combination.

## **4.3 Relevant patents to know and distinguish**

The following are patents and patent applications your attorney should include in the IDS for PAT-002. This list is not exhaustive — it reflects the searches I was able to perform from public sources as of April 2026\. Your attorney should perform a formal prior-art search via commercial tools (LexisNexis PatentAdvisor, Questel Orbit, or equivalent) before filing.

### **4.3.1 US Patent on USB write-blocking (MyKey Technology)**

MyKey Technology holds patents related to USB write blocking — i.e., preventing writes to a USB mass storage device while allowing reads. This is a different invention (forensic read-only access to storage) but sits adjacent in the 'USB security hardware' taxonomy. Your attorney should identify the specific MyKey patents (CyberGate, WriteProtect, etc.) and distinguish: your claim is about power-only, not about read-only storage access.

### **4.3.2 Plugable USB-MC1 and the 'resistor network' approach**

Plugable's product documentation describes an 'IC-free design by adding a series of resistors in between the data lines to allow for up to 1A charging.' This appears to be unpatented (product documentation, not a claim), but the approach is public prior art as of \~2020. Distinguish: Plugable uses a resistor network ON the data lines (D+/D- partially connected through resistors to signal Apple/Samsung charge modes). PowerVerify ELIMINATES D+/D- entirely and uses CC lines (separate conductors) for PD negotiation.

### **4.3.3 USB-PD controller IC patents (Cypress, TI, Infineon, Renesas)**

Each major semiconductor vendor holds patents on their specific USB-PD controller IC architecture. These are relevant as background prior art but do not read on PowerVerify because PowerVerify's claim is a system-level combination, not a controller-IC architecture. Claim language should be careful not to claim the controller design itself, only its use in a system where data lines are eliminated.

### **4.3.4 'Secure USB' and USB hub filtering patents**

A class of patents exists around USB hubs that inspect USB traffic for malicious behavior (USBKill-style defense products, Honeywell SMX products, etc.). These are anti-juice-jacking in intent but operate by INSPECTING data traffic. PowerVerify is categorically different: there is no data traffic to inspect because the conductors are absent. Distinguish cleanly — 'PowerVerify does not inspect; PowerVerify eliminates.'

### **4.3.5 USB-C power-only receptacle patents (GCT, Amphenol, TE)**

The 6-pin power-only USB-C receptacle (GCT USB4135 used in PowerVerify) is itself a patented connector. This is NOT prior art against PowerVerify's claim — your claim uses the connector as a component; the connector's own patents cover its internal design. Your product may need to license the connector from GCT; that's a commercial concern, not a patent-prosecution concern.

## **4.4 How to distinguish in prosecution**

See Vol 2 §5.4 for general prior-art distinguishing techniques. The PowerVerify-specific playbook:

* Reject §102 anticipation by showing the cited reference is missing at least one of the three layers (absence OR PD preservation OR verified operation)  
* Reject §103 obviousness by showing the cited combination would not have been obvious because prior art universally treats 'data blocker' and 'fast charger' as separate products. The integration is not motivated by anything in the prior art.  
* If the examiner cites juice-jacking research (Krebs, Mactans, DEFCON) — respond that this is the problem statement, not a solution, and does not teach the claimed combination  
* If the examiner cites consumer data blockers — distinguish on PD preservation, which none of them have  
* If the examiner cites PD controllers — distinguish on the absence of data paths, which no PD reference design has

# **SECTION 5: SAMPLE CLAIMS FOR PAT-002**

These claims are illustrative. Your attorney will produce the final filed claims. They are provided here so you can (a) evaluate the claims your attorney drafts by comparison, (b) direct your attorney toward the broadest defensible scope, and (c) have a working claim set to discuss with potential investors and acquirers before filing.  
See Vol 1 §4 for claim-drafting rules, transition words, and scope strategy.

## **5.1 Independent apparatus claim (Claim 1 — broadest)**

Claim 1An inline power delivery device comprising:a first connection interface configured to receive electrical power from a power source;a second connection interface configured to deliver electrical power to a powered device;power-carrying conductors electrically connecting the first connection interface to the second connection interface to convey electrical power from the source to the device;wherein all data-capable conductors that would otherwise be present in a standard interface of the type used for the first or second connection interface are physically absent from the electrical path between the first connection interface and the second connection interface, such that no electrical path exists between the power source and the powered device on any data-capable conductor; anda power delivery negotiation subsystem coupled to one or more power-negotiation conductors of the first connection interface and configured to negotiate a voltage and current profile with the power source without bridging the power-negotiation conductors to any data-capable conductor.

### **Analysis of Claim 1**

* 'An inline power delivery device' — preamble. Generic. Covers the AirGap pigtail and the PowerVerify Pro enclosure equally.  
* 'comprising' — open-ended. Standard. See Vol 1 §4.4.  
* 'first connection interface... second connection interface' — generic terminology. Captures USB-A, USB-C, Lightning, proprietary, future connectors. The specification should explicitly enumerate these as embodiments (§5 of provisional does this).  
* 'physically absent from the electrical path' — THE KEY INVENTIVE LANGUAGE. Stronger than 'disconnected' (which implies a reversible state) or 'blocked' (which implies an active blocking element). 'Absent' means there is no path to enable.  
* 'power delivery negotiation subsystem' — covers CH224K, Cypress CCG, TI TPS65982, or any future PD controller. Does not limit to any specific chip.  
* 'without bridging... to any data-capable conductor' — forecloses the design-around where a clever competitor routes CC through a multiplexer that could, in principle, reach D+/D-. This is the language that makes the claim defensible against design-arounds.

## **5.2 Dependent claims (2-7) adding specificity**

Claim 2\. The device of claim 1, wherein the first and second connection interfaces are USB Type-C interfaces, and wherein the data-capable conductors comprise D+, D-, TX1+, TX1-, TX2+, TX2-, RX1+, RX1-, RX2+, RX2-, SBU1, and SBU2.Claim 3\. The device of claim 1, wherein the first connection interface comprises a USB Type-C receptacle having only six electrical contacts corresponding to VBUS (×2), GND (×2), CC1, and CC2, and wherein said receptacle does not contain electrical contacts corresponding to any data-capable conductor.Claim 4\. The device of claim 1, wherein the power delivery negotiation subsystem comprises a Power Delivery controller integrated circuit coupled to CC1 and CC2 conductors of the first connection interface and configured to negotiate a USB Power Delivery voltage profile selected from the group consisting of 5V, 9V, 12V, 15V, and 20V.Claim 5\. The device of claim 1, further comprising surge protection circuitry, electromagnetic interference filtering circuitry, and reverse-polarity protection circuitry disposed in the electrical path between the first connection interface and the second connection interface.Claim 6\. The device of claim 1, further comprising an enclosure that is at least partially transparent, wherein the enclosure permits visual inspection of the electrical path between the first and second connection interfaces to confirm the absence of data-capable conductors.Claim 7\. The device of claim 1, wherein the powered device, when connected via the second connection interface, does not enumerate as a USB device, and wherein the absence of USB enumeration constitutes evidence of power-only operation during a connection session.

### **Notes on the dependent set**

* Claim 2 narrows to USB-C specifically and enumerates every data conductor. This claim is nearly certain to survive prior-art challenge because it calls out the exact physical topology.  
* Claim 3 is the 6-pin power-only receptacle claim — this is what distinguishes from Plugable and PortaPow at the connector level. Both of those products use standard 24-pin or 4-pin USB connectors with data pins disabled; PowerVerify uses connectors where the data pins physically do not exist.  
* Claim 4 explicitly claims USB-PD negotiation. This defeats the 'resistor network' prior art (Plugable) which is not USB-PD.  
* Claim 5 claims the power protection chain. Not core to novelty but establishes the commercial embodiment as a complete product.  
* Claim 6 is the transparent-enclosure visual-verification claim. Powerful marketing and potentially defensible against opaque data blockers.  
* Claim 7 is the 'absence of enumeration as evidence' claim. This is what bridges to PAT-018's cryptographic session logging (see §6).

## **5.3 Independent method claim (Claim 8\)**

Claim 8A method for delivering electrical power from a power source to a powered device while physically preventing data communication, the method comprising:receiving, at a first connection interface of an inline power delivery device, electrical power from a power source;negotiating, by a power delivery negotiation subsystem of the inline power delivery device, a voltage and current profile with the power source via one or more power-negotiation conductors of the first connection interface, wherein the negotiation does not cause any signal to be present on any data-capable conductor;conveying the negotiated electrical power from the first connection interface to a second connection interface of the inline power delivery device via power-carrying conductors;delivering, via the second connection interface, the negotiated electrical power to the powered device;wherein, during performance of the method, no electrical path exists between the power source and the powered device on any data-capable conductor, and wherein the powered device does not enumerate as a data-capable peripheral.

### **Analysis of Claim 8**

Method claims cover the process regardless of which device implements it. A competitor who builds a different device but performs the same steps infringes the method claim. This is why your filing needs both apparatus and method claims — see Vol 1 §4.5.

## **5.4 Independent system claim (Claim 15 — complete ecosystem)**

Claim 15A system for verifiable power-only charging, the system comprising:a power source having a standard power delivery interface;an inline power delivery device comprising the device of any of claims 1-7, coupled to the power source at its first connection interface;a powered device coupled to the inline power delivery device at its second connection interface, wherein the powered device receives electrical power from the inline power delivery device and does not enumerate as a data-capable peripheral during connection;wherein the system provides verifiable evidence of power-only operation through at least one of: (a) visual inspection of the inline power delivery device confirming physical absence of data-capable conductors, (b) absence of USB enumeration event in the powered device's operating system logs, and (c) a cryptographically signed session record generated by the inline power delivery device attesting to power parameters and absence of data-capable activity during the connection session.

This system claim captures the full PowerVerify \+ verifyknot.io ecosystem. Element (c) bridges into PAT-018 territory and ensures the acquirer is buying a protocol moat, not just a device moat.

# **SECTION 6: PAT-018 CIP STRATEGY — POWERVERIFY PLUS**

PAT-018 (Application 64/007,940, filed March 17, 2026\) is a provisional application that extends PAT-002 with four additional inventive elements. It is designated as a continuation-in-part (CIP) of PAT-002 in your patent tracker. This section covers how to structure the relationship between PAT-002 and PAT-018 during non-provisional conversion.

## **6.1 What PAT-018 adds to PAT-002**

| PAT-018 new element | What it claims |
| :---- | :---- |
| **Multi-layer tamper evidence** | Three or more independent physical tamper-detection mechanisms (housing seal, conductive trace loop, optical tamper detection) whose composite state is signed into session records |
| **Session recording subsystem** | Microcontroller \+ ATECC608B or equivalent secure element; time-series voltage/current log; hash-chained prior\_session\_hash field; ECDSA P-256 signature |
| **Sealed secondary verification interface** | Physically isolated secondary interface (NFC, BLE, or isolated USB CDC) for session record retrieval without signal exposure to primary connection path |
| **CC-line interaction attestation** | Active monitoring of CC-line traffic for data-capable protocol messages, with signed attestation of whether any were detected |

## **6.2 CIP filing strategy — three options**

A continuation-in-part extends the parent application by adding new matter. Claims that rely on new matter get the CIP filing date, not the parent filing date. Claims that rely only on parent matter get the parent's priority date. This creates strategic choices:

| Option | Action | Pros | Cons |
| :---- | :---- | :---- | :---- |
| **A** | File PAT-002 as non-provisional. File PAT-018 separately as its own non-provisional. Do NOT consolidate. | Maximum priority-date protection. PAT-002 core claims get Jan 15, 2026 date; PAT-018 claims get March 17, 2026 date. | Two attorney engagements. Two sets of fees. Two prosecution streams. |
| **B** | File PAT-002 as non-provisional. Then file PAT-018 as a CIP of PAT-002, claiming priority to both Jan 15 and March 17\. | Claims that rest on PAT-002 matter get Jan 15 date; new-matter claims get March 17 date. Single prosecution family. | Complex. Risk of inadvertently narrowing PAT-002 if CIP language bleeds back. |
| **C** | Consolidate — file a single non-provisional covering both, claiming priority to both provisionals. | Simplest. Single filing fee. Single prosecution. | Claims that rely on PAT-018 new matter get March 17 date. Must clearly demarcate which matter came from which provisional. |

## **6.3 Recommendation**

Option B is the conventional and defensive strategy. You keep PAT-002 as a standalone non-provisional with the broadest possible claims locked to January 15, 2026 priority. You file PAT-018 as a CIP later (its own non-provisional deadline is March 17, 2027), after PAT-002 is filed, so you know what claim language survived and you can extend from a firm base.  
Option A is the maximally cautious and maximally expensive option. Consider only if you anticipate a challenger invalidating PAT-018 and you want PAT-002 to survive independently with zero shared prosecution history.  
Option C is the budget option but risks diluting PAT-002's priority date if courts later reach that conclusion. Not recommended unless budget forces it.

## **6.4 Interaction with your existing tracker**

Your DOC-001 patent tracker lists PAT-018 as 'filed today with ADS \+ spec \+ SB15A' on March 17, 2026 and notes 'Convert within 12 months.' This means PAT-018 has its own January-2027 statutory deadline (March 17, 2027 actually, per the tracker). For Option B to work, PAT-002 non-prov must be on file BEFORE PAT-018 non-prov. Your July 31, 2026 target for PAT-002 accomplishes this comfortably.

## **6.5 What PAT-018-only matter looks like in claim language**

Claims that are ONLY supported by PAT-018's specification (i.e., would NOT be entitled to January 15, 2026 priority date) are those explicitly tied to the four new elements:

* Any claim mentioning 'hash-chained session records' or 'prior\_session\_hash' — PAT-018 only  
* Any claim mentioning 'multi-layer tamper evidence' or 'three independent physical tamper-detection mechanisms' — PAT-018 only  
* Any claim mentioning 'sealed secondary verification interface' or 'NFC' or 'physically isolated secondary interface' — PAT-018 only  
* Any claim mentioning 'CC-line interaction attestation' or 'detection of data-capable protocol messages on CC lines' — PAT-018 only

Claims that are in BOTH PAT-002 and PAT-018 (and therefore get PAT-002's earlier priority date) are the physical data-path elimination \+ PD negotiation \+ optional cryptographic session logging (high level). Your attorney drafts the CIP specification to make this demarcation explicit.

# **SECTION 7: PROSECUTION-RISK DIFFERENCES FROM PAT-001**

PAT-001 (ZKKey) faces primary risk from FIDO2/YubiKey/CTAP2 prior art and from §101 Alice rejections on the cryptographic attestation method. PAT-002 (PowerVerify) faces a different risk profile.

## **7.1 §101 Alice risk — LOW for PAT-002**

Alice Corp. v. CLS Bank (2014) established a two-step test for patent-eligible subject matter. Abstract ideas implemented on a computer are unpatentable. This is a serious risk for software/cryptographic claims (PAT-001, PAT-004, PAT-006, etc.).  
PAT-002 is much less exposed to Alice. The claims are directed to a physical interconnect topology — a device with specific electrical and mechanical characteristics. A hardware apparatus with a specific physical architecture is not an 'abstract idea' under any reading of Alice. The examiner is unlikely to raise §101 against PAT-002 claim 1\.  
However, Alice risk increases for PAT-018's cryptographic signing claims. Those claims should be drafted with explicit reference to the hardware secure element and the specific physical architecture (secure element \+ MCU \+ secondary interface), not purely as a software method. See Vol 2 §7.4 for general Alice-response strategy.

## **7.2 §103 obviousness risk — MEDIUM-HIGH for PAT-002**

This is PAT-002's biggest prosecution risk. The examiner will probably say: 'USB data blockers exist (Plugable). USB-PD controllers exist (TI, Cypress). Combining them would be obvious.' Your attorney must be prepared with:

* Evidence that the combination was not made commercially available before January 15, 2026\. A quick product search should confirm: no existing consumer USB-PD data blocker.  
* Teaching away: prior-art documentation (Plugable's own statement: 'IC-free design by adding a series of resistors') teaches away from using a PD controller IC on CC lines in a data-blocking context.  
* Unexpected results: the combination enables 100W fast charging with full data elimination, which neither element alone provides.  
* Commercial success and long-felt need: FBI/FCC/TSA warnings about juice-jacking span 2011-2026. If a data blocker \+ fast charger combination had been obvious, it would have been built and sold. It hasn't been.

## **7.3 §102 anticipation risk — LOW-MEDIUM for PAT-002**

For anticipation, the examiner must cite a SINGLE reference that discloses EVERY element of your claim. As of April 2026, no single reference discloses physical data-path elimination AND USB-PD negotiation AND verified power-only operation. Anticipation rejections are more likely to cite one of these elements and then combine with obviousness — which becomes a §103 challenge, not §102.

## **7.4 §112(b) indefiniteness risk — LOW**

The provisional uses reasonably clean technical language. 'Data-capable conductors' is defined by enumeration (D+, D−, SBU, SS pairs). 'Power delivery negotiation subsystem' is defined by function. 'Physical elimination' is crisp — either the conductor is in the circuit or it isn't. No serious indefiniteness risk.

## **7.5 §112(a) enablement risk — LOW**

The provisional describes specific implementations (USB-C, USB-A, Lightning variants; CH224K controller; 6-pin receptacle option). A PHOSITA in USB hardware design can build PowerVerify from the provisional specification without undue experimentation. The commercial embodiment (ZKNOT AirGap Rev 1\) strengthens enablement by providing KiCad files and BOM that can be incorporated in the IDS if helpful.

## **7.6 Typical PAT-002 prosecution scenario**

| Milestone | Likely outcome | Response |
| :---- | :---- | :---- |
| **First Office Action (12-18 months post-filing)** | Non-final rejection citing PortaPow / Plugable / generic data blocker \+ TI/Cypress PD controller, combined under §103 | Argue teaching-away (Plugable's 'IC-free' statement), unexpected results (fast charge \+ data absence), and long-felt need (juice-jacking warnings since 2011\) |
| **Response filed (within 3 months, extendable to 6\)** | Amended claims narrowing to emphasize the no-bridging language in Claim 1 | Keep core 'physical elimination' language intact. Add specificity only where required. |
| **Second Office Action** | Either allowance or final rejection | If final: RCE (Request for Continued Examination) to continue prosecution; or appeal to PTAB |
| **Allowance (expected: 18-30 months post-filing)** | Some claims allowed, possibly with narrower scope than initially filed | Accept narrowest claims that still cover the commercial embodiment; file continuation to pursue broader claims |

# **SECTION 8: POWERVERIFY'S ROLE IN THE ZKNOT PORTFOLIO**

This section updates Vol 2 §10 of the PAT-001 guide with PAT-002 specifics.

## **8.1 Portfolio architecture — PAT-002's position**

PAT-002 is one of the five 'highest conversion priority' patents identified in your tracker (alongside PAT-001 ZKKey, PAT-007 CombinedSession, PAT-005 VendorAttest, and PAT-006 EvidenceProtocol). It occupies a specific architectural role:

* ZKKey (PAT-001) is the signing device — it says 'a human authorized this.'  
* PowerVerify (PAT-002) is the power-integrity device — it says 'no data flowed during this charging event.'  
* CombinedSession (PAT-007) binds ZKKey signatures to PowerVerify session records — it says 'both conditions held simultaneously.'  
* ZK-LocalChain (PAT-004) chains all of the above — it says 'here's the full history.'  
* EvidenceProtocol (PAT-006) is the workflow that integrates them into chain of custody.

PAT-002 is the hardware floor that makes the whole story credible. Without PowerVerify, every signed evidence record carries an implicit asterisk: 'this device may have been compromised during a charging event we cannot rule out.' With PowerVerify, that asterisk disappears.

## **8.2 PAT-002's value to each acquirer category**

| Acquirer category | PAT-002's specific value |
| :---- | :---- |
| **Forensic / legal tech (Axon, Cellebrite, Magnet)** | Forensic devices are charged constantly in the field. Currently no defensible way to prove charging didn't compromise evidence. PowerVerify closes this gap — critical for admissibility. |
| **Cybersecurity hardware (Yubico, CrowdStrike, Palo Alto)** | USB security is a known gap in endpoint protection. PowerVerify \+ DataGap (PAT-015) \+ TrustMeter (PAT-016) is a three-patent moat on the USB security category. |
| **Government / defense** | DoD and NSA have long-standing concerns about USB-based data exfiltration. PowerVerify is the physical-enforcement answer that satisfies air-gap policy literally. |
| **Journalism / media tech (AP, Reuters, Bellingcat tech stack)** | Journalists in hostile environments need defensible charging. PowerVerify \+ AirGap commercial product seeds this market. |
| **Supply chain / IoT** | Any device that charges via USB in a manufacturing or supply-chain context can be compromised during charging. PowerVerify is the power-integrity layer for verified supply chains. |

## **8.3 PAT-002 as a standalone licensing asset**

Unlike some patents in the portfolio that only make sense as part of the ZKNOT ecosystem, PAT-002 has standalone licensing value. Any company selling a USB data blocker (Plugable, PortaPow, Amazon generics, etc.) that wants to add USB-PD fast-charging capability without licensing PAT-002 is exposed to infringement claims.  
This is a potential revenue lever before acquisition: license PAT-002 to one or two consumer USB blocker manufacturers at a per-unit royalty. This monetizes the patent and establishes commercial precedent that the patent IS valid and IS enforced — which raises acquirer valuation.

## **8.4 Relationship to PAT-015 and PAT-016**

Your tracker also lists PAT-015 (DataGapUSBDetect) and PAT-016 (TrustMeter) filed March 17, 2026\. These are in the same USB-security family as PAT-002 but cover different inventions:

* PAT-015 DataGap: passive detection of D+/D- signaling activity for tamper-witness evidence. ORTHOGONAL to PAT-002 — PAT-002 eliminates data paths; PAT-015 detects when someone is trying to use them.  
* PAT-016 TrustMeter: active measurement of electrical behavior (current, voltage, impedance) for anomaly detection. ADJACENT to PAT-002.

Together with PAT-002 and PAT-018, the USB-security patent family is: PowerVerify (eliminate), PowerVerifyPlus (eliminate \+ attest), DataGap (detect), TrustMeter (measure). This is a defensible four-patent moat on USB security.

# **SECTION 9: ATTORNEY BRIEF FOR PAT-002**

When you engage a patent attorney for PAT-002 (target: June 30, 2026), send them the following as a starting package. This mirrors Vol 2 §8.2 but with PAT-002-specific content.

## **9.1 Core package**

* The PAT-002 provisional specification as filed (App\# 63/961,118, January 15, 2026\)  
* The completed non-provisional draft (March 28, 2026\)  
* The completed prior-art search documentation (March 28, 2026\)  
* This Companion document (PowerVerify Companion)  
* The PAT-001 Master Guide Vols 1 and 2 for shared context  
* DOC-001 patent tracker (for portfolio context and priorities)  
* The PAT-018 CIP provisional specification (App\# 64/007,940)  
* KiCad schematic and PCB files for ZKNOT AirGap Rev 1 (commercial embodiment)  
* The uploaded Market\_Need\_for\_Verifiable\_\_Tamper-Proof\_USB\_Power-Only\_Adapters.pdf (commercial-need documentation for §103 defense)

## **9.2 Specific questions to ask your attorney**

* Which of the three PAT-018 CIP filing strategies (Options A, B, C in §6.2) do you recommend for this portfolio?  
* Do you see a §101 Alice risk I'm missing? My read is the hardware claims are safe.  
* How do we handle the commercial embodiment's use of the GCT USB4135 6-pin receptacle in the claims? Is Claim 3 drafted well or does it need adjustment?  
* Who are we likely to encounter as the examiner? Art Unit assignment matters for prosecution tone.  
* Do you recommend a prior-art Information Disclosure Statement (IDS) at filing, or waiting to see what the examiner cites?  
* What's your estimated timeline from retainer to filing? We target July 31, 2026\.

## **9.3 Red flags to watch for in attorney drafting**

* Claims using 'consisting of' instead of 'comprising' without specific reason. Closed claims limit scope — see Vol 1 §4.4.  
* Claims using 'means for' language unless intentionally invoking §112(f). 'Means for' claims are limited to what's in the specification, not what the language might cover.  
* Loss of 'physically absent' language in favor of 'disconnected' or 'blocked.' These are weaker and easier to design around.  
* Dependent claims that narrow too early. Claim 1 should be as broad as possible; narrowing happens in dependent claims, not in the independent.  
* Any §103 argument during prosecution that unnecessarily concedes scope. Read every response carefully. Prosecution history estoppel is permanent — see Vol 1 §4.9.

# **SECTION 10: EXECUTION CHECKLIST**

For the period April 21, 2026 to July 31, 2026:

| Week of | Action |
| :---- | :---- |
| **Apr 21, 2026** | Review this Companion \+ the PAT-001 Master Guide. Identify any gaps in your understanding. Use AI assistant for follow-up questions on specific sections. |
| **Apr 28, 2026** | Ship PowerVerify AirGap Rev 1 boards. The commercial embodiment is evidence of reduction to practice — useful for prosecution. |
| **May 5, 2026** | Identify 3-5 patent attorneys experienced in USB hardware and power electronics. Request quotes and availability. |
| **May 19, 2026** | Short-list 2 attorneys. Provide them with the attorney brief package (§9.1). Request sample claim redrafts. |
| **Jun 2, 2026** | Evaluate attorney redrafts. Choose attorney. Sign engagement letter. |
| **Jun 30, 2026** | Attorney engagement commences. Target: PAT-002 non-provisional ready to file by mid-July. |
| **Jul 15, 2026** | Review final non-provisional from attorney. Verify (a) priority claim language correct, (b) claim 1 preserves 'physically absent' language, (c) IDS complete, (d) micro-entity cert attached. |
| **Jul 31, 2026** | File PAT-002 non-provisional via Patent Center. Pay $664 in micro-entity fees. Confirm filing receipt. Update DOC-001 tracker. |
| **Aug 2026 onwards** | Begin PAT-018 CIP preparation. Non-prov deadline March 17, 2027\. Earliest filing: after PAT-002 non-provisional is on file and before PAT-018 provisional's 12-month window closes. |

# **CLOSING NOTES**

The PAT-001 Master Guide taught patent law. This Companion taught PowerVerify. Together they should be everything you and your attorney need to execute PAT-002 non-provisional conversion on schedule.  
One thing worth remembering: the most important decision in the entire process is which attorney you choose. A competent attorney will draft strong claims, defend them intelligently during prosecution, and preserve broad scope to the final allowance. A weaker attorney will accept narrowing amendments too easily, file a weak IDS, and leave claims exposed to invalidity challenges. The attorney engagement is the single highest-leverage decision. Invest time in the selection.  
The PAT-002 non-provisional is not the end. Prosecution will run 18-30 months. Maintenance fees accrue for 20 years. But the filing on or before July 31, 2026 is the hinge. Everything downstream depends on it.

**— END OF POWERVERIFY COMPANION —**

ZKNOT, INC. · CONFIDENTIAL · Patent Pending App\# 63/961,118  
*Physics enforces. Math proves. You verify.*  
shop.zknot.io · verifyknot.io · ops@zknot.io