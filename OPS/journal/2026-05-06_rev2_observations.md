
## Discovered features

### Thermal tamper indicator (DK-2251 red/white)
Brother DK-2251 thermal label tape, when placed inside heat shrink encapsulation,
provides a passive thermal tamper indicator. Normal handling and careful heat-gun
shrink work preserves the label. Sustained exposure to high heat (hot car,
microwave attack, heat gun for board-swap attempt) activates the red layer,
visibly destroying printed text underneath.

Claims this enables:
- Passive (no power needed)
- One-shot (cannot be reset)
- Visible through translucent/clear heat shrink
- Differentiates "tamper attempt visible to user" without complex electronics

For Rev 1 batch 1, this becomes the on-unit tamper-evidence layer alongside:
- Cryptographic provenance via QR scan
- Email registration mismatch detection
- (Future) PUF holographic visual fingerprint

Cost: ~$0.01 per label. Fits naturally inside existing heat shrink workflow.

