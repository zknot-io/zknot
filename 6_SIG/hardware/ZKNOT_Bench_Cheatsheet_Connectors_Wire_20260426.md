# ZKNOT Bench Cheat Sheet — Connectors, Wire & Common Traps
**Rev 1 · 2026-04-26 · Keep at the bench**

---

## 1. The Mental Model (read this first)

There are **four different naming systems** layered on top of each other, and people use them interchangeably. Untangling them ends most confusion:

| System | What it describes | Example |
|---|---|---|
| **Pitch** | Distance between adjacent pins, in mm | "2.54mm pitch" |
| **Series / family** | The connector design (housing + terminal style) | "JST PH", "Dupont", "Wago 221" |
| **AWG range** | Wire thickness the terminal is designed to grip | "26-32 AWG" |
| **Mating style** | How the housing connects (friction, lock, lever, etc.) | "friction-fit", "polarized lock", "lever clamp" |

**Two connectors can share a pitch and still be totally incompatible.** JST XH and Dupont are both 2.54mm pitch. They do not mate. Different housings, different terminal shapes, different crimp barrel sizes. Pitch tells you spacing, not compatibility.

---

## 2. AWG ↔ mm ↔ Connector — the core table

Wire thickness in American Wire Gauge (AWG) is **inversely** numbered: bigger number = thinner wire. The numbering is logarithmic, not linear.

| AWG | Diameter (mm) | Cross-section (mm²) | Typical use | Best connector match |
|---|---|---|---|---|
| 12 | 2.05 | 3.31 | House wiring, big DC power | Wago 221, butt splice |
| 14 | 1.63 | 2.08 | House wiring, solar | Wago 221, butt splice |
| 16 | 1.29 | 1.31 | LiPo packs, 3D printer heaters | XT60, ring terminal |
| 18 | 1.02 | 0.823 | Robotics motors, servos | XT30, JST VH |
| 20 | 0.81 | 0.518 | Lower-power DC, 3D printer steppers | JST VH, JST XH (high end) |
| **22** | 0.64 | 0.326 | Hobby projects, **borderline for Dupont** | JST XH, JST PH (tight) |
| **24** | 0.51 | 0.205 | Standard hobby signal | JST XH, JST PH, Dupont |
| **26** | 0.40 | 0.129 | Most CircuitPython projects | **JST PH, Dupont** ✓ |
| **28** | 0.32 | 0.0810 | **Pico/microcontroller signal lines** | **JST PH, JST SH, Dupont** ✓ |
| **30** | 0.25 | 0.0509 | Wirewrap, fine PCB rework | JST SH |
| 32 | 0.20 | 0.0320 | Tiny SMD work | JST SH (limit) |

**Rule of thumb for ZKNOT builds:** 28 AWG silicone-jacketed stranded for inside-the-case signal wiring. It's flexible, takes JST PH and Dupont crimps cleanly, and routes around tight 3D-printed pockets.

---

## 3. Hobbyist Connector Families — the ones you'll actually meet

### JST family (most common in hobby electronics)

JST is the *manufacturer*; the letters after (PH, XH, SH, ZH, VH) are the **series**. They do not interchange.

| Series | Pitch | AWG | Crimp barrel | What it's for | Typical use |
|---|---|---|---|---|---|
| **SH** | 1.0 mm | 28-32 | Tiny | Smallest practical | STEMMA QT/Qwiic, drone cameras |
| **ZH** | 1.5 mm | 26-32 | Small | Compact sensors | Some breakouts |
| **PH** ⭐ | 2.0 mm | 26-32 | Medium-small | **Inside-the-case signal** | Hobby projects, 3D printer endstops |
| **XH** | 2.5 mm | 22-28 | Medium-large | Mid-power, LiPo balance | LiPo balance leads, pump motors |
| **VH** | 3.96 mm | 16-22 | Large | DC power | Power distribution |
| **EH** | 2.5 mm | 22-28 | Like XH but locking | Identical wires to XH, polarized | Sometimes seen on industrial |
| **GH** | 1.25 mm | 28-32 | Like SH but locking | Tiny + secure | LCD modules |

**Key trap:** XH and PH are *not* substitutes. PH is smaller. A PH plug will rattle in an XH socket and won't make contact. An XH plug won't fit in a PH socket at all.

⭐ **For inside ZKKey Connect Pico:** JST PH 2.0mm. Always.

### Dupont (the breadboard jumper world)

"Dupont" is technically a trademark for a connector style, but everyone uses the name generically for **2.54mm pitch single-row pin/socket housings** — the classic breadboard jumper wires.

| Variant | Description | Notes |
|---|---|---|
| Male pin | Solid pin sticking out | Goes into female socket or breadboard hole |
| Female socket | Hollow, accepts male pin | Goes onto pin headers or male pins |
| Crimp + housing | Crimp metal terminal, then slide into plastic housing | What's in your IWISS/Taiss kits |
| Pre-made jumpers | Already assembled, just plug in | M-M, M-F, F-F variants |

**Pitch:** 2.54mm — same as standard 0.1" prototyping holes. Dupont mates with **2.54mm pin headers** (the kind soldered onto the Pico if you use them).

**Critical Dupont fact you already learned the hard way:** the SN-28B crimper's smallest die is too wide for Dupont's small **conductor wings**. Use the **PA-09** for Dupont conductor wings. The SN-28B's "Dupont" rating is misleading marketing.

### Wago 221 / 222 / 211 — splice connectors (different universe)

These are **lever-action splice connectors**, not pin-and-socket. You strip the wire, push the lever up, insert the wire, push the lever down. Used to splice two or more wires together where you'd otherwise use a wire nut.

| Series | Description | Wire range |
|---|---|---|
| **Wago 221** | Compact lever splice. Modern, transparent housing. | 24-12 AWG, solid/stranded/fine |
| **Wago 222** | Predecessor of 221. Bigger, opaque, similar function. | 24-12 AWG |
| **Wago 211** | Pluggable male/female lever connectors (different family) | Varies |
| **Wago 627** | Splicing connectors with push-in (no lever) | Solid wire only |

**These are for AC/DC building wiring, automotive, and lighting.** Not for hobby microcontroller work — they're physically too big and rated for too much current. You'll see them in junction boxes, behind light switches, in trailers, etc.

You don't need any of these for ZKKey Connect. They're useful to know about for house projects.

### Other connectors you'll meet

| Name | Pitch / type | What it is |
|---|---|---|
| **2.54mm pin header** | 2.54mm | The "default" pin strip on most dev boards. Mates with Dupont. |
| **STEMMA QT / Qwiic** | JST SH 1.0mm 4-pin | Adafruit/Sparkfun's I2C convention. Same physical connector, identical pinout. |
| **GH** | 1.25mm | Common on LCD displays, often confused with SH |
| **XT30 / XT60 / XT90** | Bullet-style power | Drone/RC battery connectors. Numbers = current rating in amps. |
| **DuPont vs JST XH** | Both 2.54mm | **NOT compatible.** Different housing geometry. |
| **PH vs PicoBlade vs SH** | All small | Molex PicoBlade is 1.25mm and looks like JST GH but isn't. Yes, it's annoying. |

---

## 4. Crimper-to-Connector Match-up

Your tools as of today, sorted by what they're actually good for:

| Tool | Genuinely good at | Also rated for, but mediocre at |
|---|---|---|
| **PA-09 (Engineer)** | JST PH, JST SH, Dupont conductor wings, fine-pitch anything | JST XH (works but small dies make it slower) |
| **PA-07 (Engineer)** | Wire stripping 24-12 AWG (thicker wires) | — |
| **PA-14 (Engineer)** | Wire stripping 32-20 AWG (thinner wires) | — |
| **SN-28B (iCrimp)** | JST XH 22-26, larger Dupont (but borderline) | Dupont small (wings won't close — known issue) |

**Working rule:**
- 28 AWG signal wire → **PA-14 strip → PA-09 crimp** → JST PH or Dupont
- 22 AWG power-ish wire → **PA-07 strip → SN-28B crimp** → JST XH
- Avoid 22 AWG into Dupont; the conductor is too thick for the terminal.

---

## 5. GPIO / Pico / Breadboard Cheat Items

### Pico 2 pin spacing
- 2.54mm (0.1") pitch on both pin rows
- Mates with: Dupont jumpers, 2.54mm pin headers, standard breadboards
- 40 pins total, 20 per side
- Pin 1 = top-left when USB faces away from you (silkscreen marks it)

### Breadboard basics (the trap that gets everyone)
- **Power rails** (the long stripes on the sides): each colored line is one continuous rail. The blue stripe and red stripe are independent — wire 3.3V to red, GND to blue, by convention.
- **Tie points** (the central area): each row of 5 holes is electrically connected. The two halves (left and right of the central trough) are NOT connected to each other.
- **Some cheap breadboards have split power rails:** the red and blue rails on some boards are split in the middle. Look for a tiny break in the colored stripe. If your power doesn't reach the right end, this is why. Bridge it with a jumper.

### Wire color conventions (helpful, not enforced)
- **Red** → +V (3.3V or 5V)
- **Black** → GND
- **Yellow / orange** → I2C SCL or "data clock"
- **Blue / green** → I2C SDA or "data line"
- **White** → general signal
- **Purple / brown** → "whatever I had on hand"

This is convention, not law. Your wires don't know what color they are. But following it makes debugging at 2 AM easier.

### Resistor color codes (quick reference)
For 4-band resistors, the bands are: digit, digit, multiplier, tolerance.

| Color | Digit | Multiplier |
|---|---|---|
| Black | 0 | ×1 |
| Brown | 1 | ×10 |
| Red | 2 | ×100 |
| Orange | 3 | ×1k |
| Yellow | 4 | ×10k |
| Green | 5 | ×100k |
| Blue | 6 | ×1M |
| Violet | 7 | ×10M |
| Gray | 8 | — |
| White | 9 | — |
| Gold | — | ×0.1 (also: 5% tol) |
| Silver | — | ×0.01 (also: 10% tol) |

**Common values you'll reach for:**
- **220Ω** — red-red-brown — LED current limit (safe minimum at 3.3V)
- **330Ω** — orange-orange-brown — LED current limit (universal "just works")
- **1kΩ** — brown-black-red — pull-up/pull-down, base resistor
- **4.7kΩ** — yellow-violet-red — I2C pull-up (often)
- **10kΩ** — brown-black-orange — pull-up/pull-down (default choice)

---

## 6. Common Traps (the things that actually cost you hours)

1. **VCC/GND swapped** — Will instantly fry sensitive parts (OLED, ATECC). Always double-check before powering. Habit: trace the 3.3V wire from the board pin to the device pin with your finger before plugging in USB.

2. **SDA/SCL swapped** — Won't fry anything but I2C scan will return empty `[]`. If your scan is empty, swap these two wires before assuming anything else is wrong.

3. **Pull-up resistor missing on I2C** — Modern breakouts (Adafruit ATECC, most SSD1306) have pull-ups on board. Bare chips do not. If you're rolling your own, you need 4.7kΩ from SDA→3.3V and SCL→3.3V.

4. **Multiple pull-ups on the same bus** — Two breakouts each with 10kΩ pull-ups in parallel = 5kΩ effective. Usually fine. Three or more starts to slow edges. Rare problem on short wiring.

5. **5V tolerance** — RP2040/RP2350 GPIO is **3.3V only**. Driving a 5V signal into it can destroy the pin. Use a level shifter or a voltage divider for any 5V sensor.

6. **Floating button input** — A button with no pull-up reads random noise when not pressed. Always enable internal pull-up (`Pull.UP` in CircuitPython, `INPUT_PULLUP` in Arduino). Then "pressed" reads LOW.

7. **LED polarity** — Long leg (or round side) = anode (+). Short leg (or flat side) = cathode (−). Backwards = no light, no damage (LEDs are diodes, they just don't conduct in reverse).

8. **Resistor calculation panic** — For LEDs at 3.3V, anything 220-470Ω is safe. Don't overthink it. 330Ω is the universal answer.

9. **Stranded vs solid** — Solid core is rigid (great for breadboards). Stranded is flexible (great for inside cases). Strip stranded carefully — nicked strands break later. Tin (apply solder) the strand bundle before crimping if your terminal allows it for permanence; or just crimp clean stranded for repairability.

10. **The "23 AWG" trap** — Some Chinese sellers list wire as "23 AWG" or other oddball sizes that aren't standard. Standard AWG is even-numbered for the common range (16, 18, 20, 22, 24, 26, 28, 30). If someone's selling odd-numbered AWG, measure it before trusting the label.

11. **The Pico's USB pins** — Pico has VBUS (5V from USB), VSYS (battery/USB after diode), and 3V3(OUT) (regulated 3.3V output). For powering 3.3V sensors, **always use 3V3(OUT)** (pin 36). Never VBUS or VSYS for 3.3V parts.

12. **Heat shrink before crimping, not after** — Slide the heat shrink onto the wire **before** you crimp the terminal. Cannot fit shrink over a crimped terminal. (Ask me how I know.)

---

## 7. Strip Lengths — a quick reference

| Connector | Strip length | Notes |
|---|---|---|
| Dupont 2.54mm | 2-3 mm | Conductor wings + insulation wings |
| JST PH 2.0mm | 1.5-2 mm | Tiny, careful |
| JST XH 2.5mm | 2-3 mm | More forgiving |
| JST SH 1.0mm | 1-1.5 mm | Very tiny, use PA-09 |
| Wago 221 | 11 mm | Stripped per Wago spec |
| Standard breadboard | 5-7 mm | For pushing into tie points |
| Soldering to PCB pad | 3-5 mm | Tin the conductor |

**Rule:** strip just enough that the bare conductor reaches but doesn't pass the conductor wing. Excess bare wire past the wing is a short waiting to happen.

---

## 8. Final Sanity Check — Before You Power On

Run through this every time you build a circuit:

1. ☐ VCC/GND not swapped — trace the wires
2. ☐ Logic level matches (3.3V parts on 3.3V, 5V parts on 5V)
3. ☐ I2C pull-ups present (built into breakouts in most cases)
4. ☐ LED polarity correct (anode through resistor to GPIO)
5. ☐ Buttons go to GND, internal pull-up enabled in code
6. ☐ No bare wire whisking out of crimps or terminals
7. ☐ USB cable is data-capable (some "charging only" cables won't enumerate)
8. ☐ Multimeter on the 3.3V rail before plugging anything in

---

*ZKNOT, INC. — When physics is policy, trust is optional.*
