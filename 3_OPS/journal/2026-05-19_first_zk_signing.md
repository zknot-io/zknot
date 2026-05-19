# First ZK signing — 2026-05-19

Device: ZK-EW6E-EERX (PC-based, software keys, firmware 0.1-pc-keys)
First ZK number: KAM6-M30B-4JHP
Signed: "PowerVerify SN12345"

This is the start of cryptographically signed provenance for ZKNOT products.
Path C (PC signer) chosen for week-1 shipping; ATECC migration deferred until
MCP2221 arrives for proper provisioning.

Two ATECC608B chips bricked during initial Pico-based provisioning attempts
(CRC mismatch during gen_key, suspected breadboard power transient). Three
breakouts + DigiKey SOIC-8 chips remain.

Registry: ~/.zkkey/registry/
Signer key: ~/.zkkey/signer.pem (backed up to 99_SENSITIVE)
Pubkey: 9b130211b7439cce0b98a06b3c214d31b04702f03c6d4a64ea34c5720c965cc5ce5243aef65378540b53b76712ded011780381dd81c5b333aaba2e961b0d2743
