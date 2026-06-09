"""
TrustSeal Batch A001 Label Generator
ZKNOT, INC. — PAT-003 App# 63/961,112
Generates print-ready label artwork for 100 seals
Label spec: 25mm x 50mm, 300 DPI, white background, black print
"""

import qrcode
from PIL import Image, ImageDraw, ImageFont
import os
import json
from datetime import date

# ── Label physical spec ──────────────────────────────────────────────────────
LABEL_W_MM   = 50     # landscape width
LABEL_H_MM   = 25     # landscape height
DPI          = 300
MM_TO_PX     = DPI / 25.4

W = int(LABEL_W_MM * MM_TO_PX)   # 591 px
H = int(LABEL_H_MM * MM_TO_PX)   # 295 px

# ── Batch config ─────────────────────────────────────────────────────────────
BATCH        = "A001"
BATCH_SIZE   = 100
BASE_URL     = "https://verifyknot.io/seal/"
PRODUCT      = "TrustSeal"
COMPANY      = "ZKNOT, INC."
PAT_LINE     = "PAT. PEND. — App# 63/961,112"
DATE_STR     = date.today().strftime("%Y-%m-%d")

# ── Luhn-style check character ───────────────────────────────────────────────
CHARSET = "ABCDEFGHJKLMNPQRSTUVWXYZ23456789"  # no 0/O, no 1/I

def check_char(serial_body: str) -> str:
    """Single check character derived from serial body."""
    val = sum(ord(c) * (i + 1) for i, c in enumerate(serial_body))
    return CHARSET[val % len(CHARSET)]

def make_serial(batch: str, seq: int) -> str:
    body = f"TS-{batch}-{seq:05d}"
    chk  = check_char(body)
    return f"{body}-{chk}"

# ── QR code generator ────────────────────────────────────────────────────────
def make_qr(url: str, size_px: int) -> Image.Image:
    qr = qrcode.QRCode(
        version=3,
        error_correction=qrcode.constants.ERROR_CORRECT_H,
        box_size=4,
        border=1,
    )
    qr.add_data(url)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white").convert("RGB")
    return img.resize((size_px, size_px), Image.LANCZOS)

# ── Font loader (use default PIL font if system fonts unavailable) ────────────
def get_font(size):
    try:
        return ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", size)
    except:
        try:
            return ImageFont.truetype("/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf", size)
        except:
            return ImageFont.load_default()

def get_font_regular(size):
    try:
        return ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", size)
    except:
        try:
            return ImageFont.truetype("/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf", size)
        except:
            return ImageFont.load_default()

# ── Single label renderer ────────────────────────────────────────────────────
def render_label(serial: str, url: str) -> Image.Image:
    img  = Image.new("RGB", (W, H), "white")
    draw = ImageDraw.Draw(img)

    # Border — thin outer rule, slightly inset
    MARGIN = 4
    draw.rectangle([MARGIN, MARGIN, W - MARGIN, H - MARGIN],
                   outline="black", width=2)

    # ── QR code — left zone ──────────────────────────────────────────────────
    QR_SIZE   = int(H * 0.78)
    QR_LEFT   = int(MARGIN + 8)
    QR_TOP    = int((H - QR_SIZE) / 2)
    qr_img    = make_qr(url, QR_SIZE)
    img.paste(qr_img, (QR_LEFT, QR_TOP))

    # ── Right zone — text content ────────────────────────────────────────────
    TEXT_LEFT = QR_LEFT + QR_SIZE + 10
    TEXT_W    = W - TEXT_LEFT - MARGIN - 8

    # ZKNOT wordmark
    f_brand = get_font(int(H * 0.14))
    draw.text((TEXT_LEFT, int(H * 0.06)), "ZKNOT", font=f_brand, fill="black")

    # TrustSeal product name
    f_product = get_font(int(H * 0.11))
    draw.text((TEXT_LEFT, int(H * 0.24)), "TrustSeal", font=f_product, fill="black")

    # Separator rule
    sep_y = int(H * 0.38)
    draw.line([(TEXT_LEFT, sep_y), (W - MARGIN - 8, sep_y)],
              fill="black", width=1)

    # Serial number — bold, largest text in right zone
    f_serial = get_font(int(H * 0.095))
    # Split serial for two-line readability if needed
    # TS-A001-00001-K → TS-A001 / 00001-K
    parts = serial.split("-")
    line1 = f"{parts[0]}-{parts[1]}"   # TS-A001
    line2 = f"{parts[2]}-{parts[3]}"   # 00001-K
    draw.text((TEXT_LEFT, int(H * 0.42)), line1, font=f_serial, fill="black")
    draw.text((TEXT_LEFT, int(H * 0.56)), line2, font=f_serial, fill="black")

    # Verify callout
    f_verify = get_font_regular(int(H * 0.07))
    draw.text((TEXT_LEFT, int(H * 0.72)),
              "Scan to verify", font=f_verify, fill="#444444")
    f_url_small = get_font_regular(int(H * 0.065))
    draw.text((TEXT_LEFT, int(H * 0.82)),
              "verifyknot.io", font=f_url_small, fill="#444444")

    # Patent pending — bottom strip
    f_pat = get_font_regular(int(H * 0.055))
    pat_bbox = draw.textbbox((0, 0), PAT_LINE, font=f_pat)
    pat_w = pat_bbox[2] - pat_bbox[0]
    draw.text(((W - pat_w) // 2, int(H * 0.91)),
              PAT_LINE, font=f_pat, fill="#888888")

    # VOID watermark text in background (simulates void pattern area)
    # In actual print this would be the tamper-evident substrate
    f_void = get_font(int(H * 0.055))
    void_text = "VOID " * 12
    draw.text((MARGIN + 5, int(H * 0.001)), void_text,
              font=f_void, fill="#f0f0f0")

    return img

# ── Sheet compositor — 8-up on A4 for desktop proofing ──────────────────────
def render_sheet(labels: list) -> Image.Image:
    """Arrange 8 labels per A4 sheet (297x210mm at 300 DPI)."""
    A4_W = int(297 * MM_TO_PX)
    A4_H = int(210 * MM_TO_PX)
    sheet = Image.new("RGB", (A4_W, A4_H), "#cccccc")  # grey background

    COLS    = 4
    ROWS    = 2
    PAD_X   = int(5 * MM_TO_PX)
    PAD_Y   = int(5 * MM_TO_PX)
    GAP_X   = int(3 * MM_TO_PX)
    GAP_Y   = int(3 * MM_TO_PX)

    for i, lbl in enumerate(labels[:COLS * ROWS]):
        col = i % COLS
        row = i // COLS
        x   = PAD_X + col * (W + GAP_X)
        y   = PAD_Y + row * (H + GAP_Y)
        sheet.paste(lbl, (x, y))

    return sheet

# ── Main generation loop ─────────────────────────────────────────────────────
def main():
    out_dir    = "/home/claude/TrustSeal/labels"
    sheet_dir  = "/home/claude/TrustSeal/sheets"
    os.makedirs(out_dir,   exist_ok=True)
    os.makedirs(sheet_dir, exist_ok=True)

    registry   = []
    all_labels = []

    print(f"Generating batch {BATCH} — {BATCH_SIZE} seals...")

    for seq in range(1, BATCH_SIZE + 1):
        serial = make_serial(BATCH, seq)
        url    = BASE_URL + serial
        label  = render_label(serial, url)

        # Save individual label
        label.save(f"{out_dir}/{serial}.png", dpi=(DPI, DPI))

        # Registry entry
        registry.append({
            "serial":      serial,
            "batch":       BATCH,
            "seq":         seq,
            "verify_url":  url,
            "status":      "UNREGISTERED",
            "created":     DATE_STR,
            "applied_at":  None,
            "event_hash":  None,
            "device_id":   None,
            "operator":    None,
        })

        all_labels.append(label)

        if seq % 10 == 0:
            print(f"  {seq}/{BATCH_SIZE} — {serial}")

    # Save proof sheets (8-up)
    print("\nCompositing proof sheets...")
    for sheet_num in range(0, BATCH_SIZE, 8):
        batch_labels = all_labels[sheet_num:sheet_num + 8]
        sheet        = render_sheet(batch_labels)
        sheet_file   = f"{sheet_dir}/sheet_{(sheet_num // 8) + 1:02d}.png"
        sheet.save(sheet_file, dpi=(DPI, DPI))
        print(f"  Sheet {(sheet_num // 8) + 1}: seals {sheet_num + 1}–{min(sheet_num + 8, BATCH_SIZE)}")

    # Save registry JSON
    reg_path = "/home/claude/TrustSeal/ZKNOT_TS-A001_serial_registry_20260416.json"
    with open(reg_path, "w") as f:
        json.dump({
            "batch":        BATCH,
            "product":      PRODUCT,
            "company":      COMPANY,
            "patent":       "App# 63/961,112",
            "generated":    DATE_STR,
            "count":        BATCH_SIZE,
            "base_url":     BASE_URL,
            "seals":        registry,
        }, f, indent=2)

    print(f"\nDone.")
    print(f"  Individual labels: {out_dir}/")
    print(f"  Proof sheets:      {sheet_dir}/")
    print(f"  Registry JSON:     {reg_path}")
    print(f"\nFirst serial:  {registry[0]['serial']}")
    print(f"Last serial:   {registry[-1]['serial']}")

if __name__ == "__main__":
    main()
