# TrustSeal Printer Setup — Quick Start
**ZKNOT, INC. | 2026-04-16**

---

## What You Need

| Item | Source | Cost |
|------|--------|------|
| Zebra ZT230 or ZT410 (used) | eBay search "Zebra ZT230 thermal transfer" | $300–500 |
| Tamper-evident VOID label roll, 2"×1", thermal transfer | ULINE S-19197 or similar | ~$45/1000 |
| Thermal transfer ribbon (wax-resin, black) | eBay, Zebra.com, or Amazon | ~$15/roll |
| USB cable A-B (comes with printer usually) | Any | — |

**Total setup cost: ~$400–550.** Per-label cost at volume: ~$0.06–0.10.

---

## Printer Setup (5 minutes)

### 1. Load label stock
- Open the media cover
- Load the tamper-evident label roll (labels face up, liner down)
- Thread through the media guides
- Close the cover — printer will calibrate automatically

### 2. Load ribbon
- Open the ribbon compartment
- Install ribbon roll on the supply spindle, take-up core on the take-up spindle
- Thread ribbon under the printhead
- Ribbon goes ink-side down against the label face

### 3. Connect USB
```
Printer USB-B → your computer USB-A
Linux:   appears as /dev/usb/lp0
Windows: install Zebra ZPL driver from zebra.com/setup
Mac:     appears as /dev/usb/lp0 or /dev/tty.usbserial*
```

### 4. Set permissions (Linux only)
```bash
sudo usermod -aG lp $USER
newgrp lp
# or for immediate access without logout:
sudo chmod 666 /dev/usb/lp0
```

### 5. Test print
```bash
cd /path/to/TrustSeal/printer
python3 trustseal_print.py --serial TS-A001-00001-T --usb /dev/usb/lp0
```

---

## Network Printing (if printer has Ethernet)

Most ZT-series printers have an Ethernet port. Find the printer IP from its display or print a config label (hold Feed button 5 seconds).

```bash
# Test connection
nc -zv 192.168.1.100 9100

# Print
python3 trustseal_print.py --serial TS-A001-00001-T --printer-ip 192.168.1.100
```

Zebra default port is 9100. No driver needed for network printing — raw TCP.

---

## Common Print Commands

```bash
# Print one seal (USB)
python3 trustseal_print.py \
    --serial TS-A001-00001-T \
    --usb /dev/usb/lp0

# Print one seal (network)
python3 trustseal_print.py \
    --serial TS-A001-00047-R \
    --printer-ip 192.168.1.100

# Print seals 1 through 10
python3 trustseal_print.py \
    --batch A001 --from 1 --to 10 \
    --usb /dev/usb/lp0

# Print device provisioning seal (goes over SWD header after flash)
python3 trustseal_print.py \
    --provision \
    --device-id ZKC-A1B2C3D4 \
    --device-type "ZKKey Connect" \
    --batch A001 \
    --usb /dev/usb/lp0

# Preview without printer (saves PNG to /tmp/)
python3 trustseal_print.py \
    --serial TS-A001-00001-T \
    --preview

# Validate a serial number (check character only)
python3 trustseal_print.py --validate TS-A001-00047-R

# Save ZPL to file for manual inspection
python3 trustseal_print.py \
    --serial TS-A001-00001-T \
    --zpl-out /tmp/seal.zpl

# Send saved ZPL manually
cat /tmp/seal.zpl > /dev/usb/lp0
# or
nc 192.168.1.100 9100 < /tmp/seal.zpl
```

---

## ZPL Calibration (if labels print offset)

If the label content is positioned wrong, the printer needs to know the label length. Run this ZPL to auto-calibrate:

```bash
# Write to file then send
cat > /tmp/calibrate.zpl << 'EOF'
^XA
^MNY
^JUS
^XZ
EOF
cat /tmp/calibrate.zpl > /dev/usb/lp0
```

Or adjust `^LL` (label length in dots) in `build_label_zpl()`. At 12 dpmm, 25mm = 300 dots. If your stock is slightly different, measure and adjust.

---

## Label Stock Spec for Reorder

When you need more stock, tell the supplier:

```
Tamper-evident security label
Face:     White gloss polyester
Adhesive: Permanent acrylic with VOID destructive pattern
Finish:   Matte or gloss laminate
Size:     2" × 1" (50.8mm × 25.4mm)
Core:     3" core
Print:    Thermal transfer compatible
Quantity: 1000 per roll
```

ULINE item numbers to search: S-19197, S-14573, or ask for "tamper-evident thermal transfer security label 2x1."

Zebra part number equivalent: PolyPro 3000T or Z-Select 4000T in tamper-evident variant.

---

## Provisioning Flow — Full Sequence

When a new ZKKey device is flashed and provisioned:

```
1. Flash firmware via SWD (BOOT0 shunted)
2. Remove BOOT0 shunt → boot into run mode
3. Device boots → ATECC608A generates keypair → registers at api.zknot.io/v1/provision
4. api.zknot.io returns: device_id = ZKC-XXXXXXXX
5. Print provisioning seal:
   python3 trustseal_print.py --provision --device-id ZKC-XXXXXXXX --device-type "ZKKey Connect" --batch A001
6. Apply seal over SWD header on PCB
7. Register seal application: POST api.zknot.io/v1/seal/register
8. Both records (device provisioning + seal application) are now in ZK-LocalChain
```

Anyone who subsequently opens the device (breaking the SWD seal) is recorded as a tamper event when the seal serial is next scanned. The broken seal is physical evidence. The ledger record is cryptographic evidence. Both are independently verifiable at verifyknot.io.

---

## File Structure

```
TrustSeal/printer/
  trustseal_print.py          ← main print driver (run this)
  PRINTER_SETUP.md            ← this file
  previews/
    TS-A001-00001-T_preview.png   ← sample label renders
    TS-A001-00047-R_preview.png
    TS-A001-00100-R_preview.png
```

---

*ZKNOT, INC. — When physics is policy, trust is optional.*
*PAT-003 App# 63/961,112*
