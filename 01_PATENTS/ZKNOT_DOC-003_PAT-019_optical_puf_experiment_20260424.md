# ZKNOT Experiment Protocol — Optical PUF in Potted Enclosure

**Doc ID:** ZKNOT_DOC-003_PAT-019_optical_puf_experiment_20260424
**Related Patent:** PAT-019 (pending — not yet filed)
**Related Products:** PowerVerify (PAT-002), PowerVerifyPlus (PAT-018), TrustSeal (PAT-003)
**Author:** William Shane Wilkinson
**Date Opened:** April 24, 2026
**Status:** Planned — not started
**Estimated Duration:** 2 weekends (bench work) + 1 week (analysis)
**Estimated Cost:** $56 USD (materials only)

Page 1 of 4

---

## 1. Objective

Determine whether a clear two-part epoxy loaded with holographic glitter flakes, poured over a PCB, produces an optical pattern that is:

- **Unique per unit** — two boards potted from the same mix produce maximally different images.
- **Stable per unit** — the same board photographed repeatedly produces near-identical images under controlled conditions.
- **Unclonable** — a third party given the reference image and unlimited attempts cannot reproduce a matching pattern.

If all three hold, the optical pattern qualifies as a Physical Unclonable Function (PUF) suitable for binding to ZK-LocalChain via the PAT-019 integration claim.

If any one fails, PAT-019 has no technical basis and should not be pursued.

---

## 2. Pass/Fail Criteria

| Test | Pass | Fail |
|---|---|---|
| Uniqueness (different boards, same mix) | Perceptual hash Hamming distance ≥ 20 bits out of 64 | Distance < 10 bits (patterns too similar) |
| Stability (same board, 10 captures) | Hamming distance ≤ 4 bits between all pairs | Any pair > 8 bits (capture too noisy) |
| Separation margin | Uniqueness min > Stability max by ≥ 3× | Overlap — attacker could spoof |
| Reproducibility attempt | 3 attempts to replicate target pattern all fail uniqueness threshold | Any attempt produces distance < 10 bits to target |

**Gate:** All four must pass before PAT-019 provisional filing is reconsidered.

---

## 3. Bill of Materials

| Item | Source | Qty | Est. Cost |
|---|---|---|---|
| Clear 2-part epoxy (JB Weld ClearWeld or equivalent), 4 oz | Amazon / hardware store | 1 | $15 |
| Holographic glitter, fine grade (~50 μm flakes) | Amazon craft supplies | 1 | $6 |
| Thermochromic pigment or stickers (>50°C threshold) | Amazon / SpecialChem | 1 | $12 |
| Silicone mold release spray | Amazon / hardware store | 1 | $8 |
| Macro phone lens clip | Amazon | 1 | $15 |
| Scrap PCBs (non-functional) for potting substrate | Bench stock | 3+ | $0 |
| Disposable mixing cups + stir sticks | Bench stock | — | $0 |
| **Total** | | | **$56** |

Page 2 of 4

---

## 4. Procedure

### 4.1 Preparation

1. Label three scrap PCBs: BOARD-A, BOARD-B, BOARD-C.
2. Build a **fixed-position capture rig**: phone clamped at known distance and angle, single LED light source at fixed position, matte black background. Document rig dimensions.
3. Mix epoxy + glitter in a single batch sufficient for all three boards. Target loading: ~2% glitter by volume (adjust after first pour if pattern is too dense or too sparse).

### 4.2 Pour

1. Apply mold release to any surfaces that must not bond.
2. Pour identical volumes over BOARD-A, BOARD-B, BOARD-C from the same batch.
3. Agitate gently to distribute flakes without introducing bubbles.
4. Cure per epoxy manufacturer spec (typically 24h at room temp).

### 4.3 Capture — Uniqueness Test

1. Photograph BOARD-A, BOARD-B, BOARD-C in the capture rig. One image each.
2. Compute perceptual hash (pHash 64-bit) of each image.
3. Compute pairwise Hamming distances: A-B, A-C, B-C.
4. **Record:** uniqueness distances.

### 4.4 Capture — Stability Test

1. Photograph BOARD-A ten times. Between captures, remove board from rig, handle normally, return to rig.
2. Compute pHash of each of the 10 images.
3. Compute all 45 pairwise Hamming distances.
4. **Record:** stability distance distribution (min, max, mean).

### 4.5 Replication Attempt

1. Given the reference image of BOARD-A only (no access to the physical board), mix a fresh batch of epoxy with glitter from the same bag and pour a new board (BOARD-D1).
2. Photograph BOARD-D1. Compute pHash. Compute Hamming distance to BOARD-A reference.
3. Repeat with BOARD-D2, BOARD-D3, each time attempting to match the target pattern visually.
4. **Record:** all three attempt distances.

### 4.6 Thermochromic Witness Test

1. Apply thermochromic dot to a scrap enclosure piece.
2. Heat with a heat gun to ~60°C for 10 seconds.
3. Cool to room temperature.
4. **Record:** whether color change is permanent (required) or reverses (disqualifies the pigment).

---

## 5. Data Capture Template

All data logged in `/ZKNOT-IP/Patents/PAT-019/experiment_data_YYYYMMDD.csv` with columns:

```
board_id, capture_timestamp, image_filename, phash_hex, notes
```

Analysis script (Python, pillow + imagehash libraries) lives at `/ZKNOT-IP/Patents/PAT-019/analyze.py`. Outputs uniqueness matrix, stability distribution, and pass/fail verdict per §2.

Page 3 of 4

---

## 6. Decision Tree After Experiment

| Outcome | Action |
|---|---|
| All four criteria pass | Proceed to PAT-019 provisional filing ($65), update PowerVerifyPlus integration notes, defensive-publish on GitHub |
| Uniqueness passes, stability fails | Re-engineer capture rig (better lighting, fixed focal plane). Re-test. Do not file until stability passes. |
| Uniqueness fails | Optical PUF approach dead for this material. Consider alternative PUF substrates (metal flakes, fiber composites) or abandon PAT-019. |
| Replication succeeds (any attempt < 10 bits) | Attacker can spoof. Abandon PAT-019 in current form. |
| Thermochromic reverses on cooling | Source different pigment; unrelated to PAT-019 decision. |

---

## 7. Open Questions / TODO Before Starting

- [ ] Confirm glitter particle size (~50 μm target) — vendor specs vary
- [ ] Decide whether potting happens over live PCB or scrap — scrap is fine for PUF test, live PCB adds thermal risk during cure
- [ ] Build / source the capture rig before mixing epoxy (rig failure mid-experiment invalidates stability data)
- [ ] Document lighting conditions precisely — PUF verification fails if field conditions diverge from reference conditions
- [ ] Consider whether a second hash algorithm (e.g., feature-point matching via SIFT/ORB) produces better stability margins than pHash alone

---

## 8. Links to Related Portfolio

- **PAT-002** PowerVerify — potting already specified as tamper barrier; this experiment adds PUF function to existing material
- **PAT-003** TrustSeal — separate tamper-evident layer, complementary not redundant
- **PAT-004** ZK-LocalChain — destination ledger for PUF hash records
- **PAT-011** DualSE — dual-signature structure for manufacturing record
- **PAT-018** PowerVerifyPlus — natural integration point if PAT-019 succeeds

---

## 9. Notes

Keep this document updated in-place as experiment progresses. Do not create new dated versions — use git history or a dated change log section at the bottom if needed.

Page 4 of 4
