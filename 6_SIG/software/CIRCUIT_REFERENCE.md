# ZKAuth Module - Circuit Diagram Reference

## Complete Schematic (ASCII Diagram)

```
                    +3.3V
                      │
                      ├──────────┬─────────────┬────────────────┐
                      │          │             │                │
                    ┌─┴─┐      ┌─┴─┐         ┌─┴─┐            ┌─┴─┐
                    │R4 │      │R5 │         │R1 │            │   │
                    │4k7│      │4k7│         │10k│            │   │
                    └─┬─┘      └─┬─┘         └─┬─┘            │   │
                      │          │             │              │C1 │
         ┌────────────┼──────────┼─────────────┼──────┐       │100│
         │            │          │             │      │       │nF │
         │  J1        │          │             │      │       └─┬─┘
         │ ┌────┐   ┌─┴──┐     ┌─┴──┐       ┌─┴─┐  ┌─┴─┐      │
         │ │ 1  │───│SDA │─────│SDA │       │   │  │VCC│──────┤
         │ │GND │   └─┬──┘     └─┬──┘       │   │  └─┬─┘      │
         │ │    │     │          │          │SW1│    │        │
         │ │ 2  │   ┌─┴──┐     ┌─┴──┐       │   │  ┌─┴─┐      │
         │ │VCC│───│SCL │─────│SCL │       │BTN│  │GND│──┐   │
         │ │    │   └────┘     └────┘       └─┬─┘  └───┘  │   │
         │ │ 3  │                             │           │   │
         │ │SDA│────────┬────────────────────┤           │   │
         │ │    │        │                    │           │   │
         │ │ 4  │        │                  ┌─┴─┐         │   │
         │ │SCL│────────┼──────────────────│C2 │         │   │
         │ └────┘        │                  │100│         │   │
         │               │                  │nF │         │   │
         │            ┌──┴──┐               └─┬─┘         │   │
         │            │     │                 │           │   │
         │            │ATECC│                GND          │   │
         │            │608B │                             │   │
         │            │  U1 │                             │   │
         │            │     │                             │   │
         │            │ NC  │1                            │   │
         │            │ NC  │2                            │   │
         │            │ NC  │3                            │   │
         │            │ GND │4────────────────────────────┼───┤
         │            │ SDA │5────────────────────────────┤   │
         │            │ SCL │6────────────────────────────┤   │
         │            │ VCC │7────────────────────────────┤   │
         │            │ NC  │8                            │   │
         │            └─────┘                             │   │
         │                                                │   │
         │                                                │   │
         │         Seeed XIAO RP2040 (U2)                │   │
         │         ┌─────────────────────┐               │   │
         │         │                     │               │   │
         │      ┌──┤1  3V3      D10  7 ──┤               │   │
         │      │  │                     │               │   │
         ├──────┼──┤2  GND       D9  8 ──┤               │   │
         │      │  │                     │               │   │
         │      │  │3  D0        D8  9 ──┼───────────────┘   │
         │      │  │             SCL     │                   │
         │      │  │                     │                   │
         │      │  │4  D1        D7 10 ──┼───────────────────┘
         │      │  │             SDA     │
         │      │  │                     │
         │      │  │5  D2        D6 11 ──┤
         │      │  │                     │
         │      │  │6  D3        5V 12 ──┤
         │      │  │                     │
         │      │  └─────────────────────┘
         │      │    │    │      │
         │      │    │    │      │
         │    ┌─┴─┐  │  ┌─┴─┐  ┌─┴─┐
         │    │   │  │  │   │  │   │
         │    GND  │  │  GND  │  GND
         │         │  │       │
         │       ┌─┴─┐│     ┌─┴─┐
         │       │R2 ││     │R3 │
         │       │330││     │330│
         │       └─┬─┘│     └─┬─┘
         │         │  │       │
         │       ┌─┴─┐│     ┌─┴─┐
         │       │ + ││     │ + │
         │       │D1 ││     │D2 │
         │       │LED││     │LED│
         │       │Grn││     │Red│
         │       │ - ││     │ - │
         │       └─┬─┘│     └─┬─┘
         │         │  │       │
         └─────────┴──┴───────┴───── GND


Legend:
  J1    - JST-SH 4-pin I2C connector
  U1    - ATECC608B secure element (SOIC-8)
  U2    - Seeed XIAO RP2040 microcontroller module
  SW1   - Tactile push button (authentication trigger)
  D1    - Green LED (ready indicator)
  D2    - Red LED (busy indicator)
  C1    - 100nF decoupling capacitor (ATECC608B)
  C2    - 100nF debounce capacitor (button)
  R1    - 10kΩ pull-up resistor (button)
  R2    - 330Ω current limiting resistor (green LED)
  R3    - 330Ω current limiting resistor (red LED)
  R4    - 4.7kΩ I2C pull-up resistor (SDA)
  R5    - 4.7kΩ I2C pull-up resistor (SCL)
```

## Pin-by-Pin Connections

### J1 (JST-SH Connector)
```
Pin 1 (GND) ──→ GND rail
Pin 2 (VCC) ──→ +3.3V rail
Pin 3 (SDA) ──→ I2C SDA net
Pin 4 (SCL) ──→ I2C SCL net
```

### U1 (ATECC608B)
```
Pin 1 (NC)  ──→ Not connected
Pin 2 (NC)  ──→ Not connected
Pin 3 (NC)  ──→ Not connected
Pin 4 (GND) ──→ GND
Pin 5 (SDA) ──→ I2C SDA net
Pin 6 (SCL) ──→ I2C SCL net
Pin 7 (VCC) ──→ +3.3V (with C1 to GND)
Pin 8 (NC)  ──→ Not connected
```

### U2 (XIAO RP2040)
```
Left side (top to bottom):
Pin 1  (3V3) ──→ +3.3V output
Pin 2  (GND) ──→ GND
Pin 3  (D0)  ──→ Button signal (with R1 pull-up)
Pin 4  (D1)  ──→ Green LED (via R2)
Pin 5  (D2)  ──→ Red LED (via R3)
Pin 6  (D3)  ──→ Not connected

Right side (top to bottom):
Pin 7  (D10) ──→ Not connected
Pin 8  (D9)  ──→ Not connected
Pin 9  (D8)  ──→ I2C SCL net
Pin 10 (D7)  ──→ I2C SDA net
Pin 11 (D6)  ──→ Not connected
Pin 12 (5V)  ──→ Not connected (or USB power input)
```

### SW1 (Button)
```
Pin 1 ──→ XIAO D0 (via R1 to +3.3V, via C2 to GND)
Pin 2 ──→ GND
```

### D1, D2 (LEDs)
```
D1 Anode  ──→ R2 ──→ XIAO D1
D1 Cathode ──→ GND

D2 Anode  ──→ R3 ──→ XIAO D2
D2 Cathode ──→ GND
```

## Net List

| Net Name | Connected Pins |
|----------|----------------|
| GND | J1-1, U1-4, U2-2, SW1-2, D1-cathode, D2-cathode, C1-pin2, C2-pin2 |
| +3V3 | J1-2, U1-7, U2-1, R1-pin1, R4-pin1, R5-pin1, C1-pin1 |
| SDA | J1-3, U1-5, U2-10, R4-pin2 |
| SCL | J1-4, U1-6, U2-9, R5-pin2 |
| BTN | SW1-1, U2-3, R1-pin2, C2-pin1 |
| LED_GREEN | U2-4, R2-pin1 |
| LED_RED | U2-5, R3-pin1 |

## Component Values Summary

| Reference | Value | Package | LCSC Part # |
|-----------|-------|---------|-------------|
| C1, C2 | 100nF | 0603 | C14663 |
| R1 | 10kΩ | 0603 | C25804 |
| R2, R3 | 330Ω | 0603 | C23138 |
| R4, R5 | 4.7kΩ | 0603 | C23162 |
| D1 | Green LED | 0603 | C72043 |
| D2 | Red LED | 0603 | C72041 |
| SW1 | Tactile Switch | SMD | C231329 |
| J1 | JST-SH 4-pin | SMD | C160404 |
| U1 | ATECC608B | SOIC-8 | C2932020 |
| U2 | XIAO RP2040 | Module | 102010428 |

## PCB Layout Guidelines

### Component Placement Priority
1. **J1** - Left edge, facing outward
2. **U1** - Close to J1 (minimize I2C trace length)
3. **C1** - Within 5mm of U1 pin 7
4. **R4, R5** - Near J1/U1
5. **U2** - Center of board
6. **SW1** - Right edge, accessible
7. **D1, D2** - Right side, visible from top
8. **R2, R3** - Near LEDs

### Trace Routing Priority
1. Power (+3.3V, GND) - widest traces or planes
2. I2C (SDA, SCL) - keep equal length, avoid crossover
3. Button signal - short to XIAO
4. LED signals - can be longer, less critical

### Design Rules
- Minimum trace width: 0.127mm (5 mil)
- Recommended trace width: 0.25mm (10 mil)
- Power traces: 0.4mm (16 mil)
- Minimum clearance: 0.127mm (5 mil)
- Via size: 0.8mm diameter, 0.4mm drill

---

Use this reference when building the design in KiCad!
