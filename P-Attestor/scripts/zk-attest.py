#!/usr/bin/env python3
"""
zk-attest.py — ZKNOT document issuance (Tier-0 / AP-1, SELF-ASSERTED)

The pipeline that turns the *mechanism* (a signature) into the *product* (an issued,
citable attestation):

  file ->  document_hash = SHA-256(file)        # the file NEVER leaves your machine
       ->  challenge = SHA-256(document_hash)    # the 32-byte digest the device signs
       ->  press the Attestor button to sign
       ->  host-verify the signature   (FAIL-CLOSED: refuses to continue if invalid)
       ->  assemble a v1 record         (stores the HASH, not the document)
       ->  [--submit]  POST /v1/attest  ->  ZK number
       ->  write a verification certificate (.md) you can hand to a skeptic

Crypto model is identical to verifyknot /start, so verifier.js verifies it unchanged.
We store signed_payload = SHA-256(file) (a 32-byte commitment), and the device signs
SHA-256(that) — the double hash is what lets the record carry only the hash while the
browser verifier (which always hashes the payload) still checks out. Privacy: the
document content never goes on the chain; only its hash does.

Run inside the project venv (cryptography + pyserial):
  ~/ZKNOT/P-Attestor/.venv/bin/python zk-attest.py <file> [--submit]
"""
import argparse, glob, hashlib, json, re, sys, time, uuid
from datetime import datetime, timezone

# ---- bundled pubkeys (swap seam -> api.zknot.io lookup later) ----
BUNDLED_PUBKEYS = {
    "01234DF53F8AF547EE":
        "683a08ef83be128fb1640ecb9c21f0f474e1dc2e29b7d9332c68fa0a05644b83"
        "10004516c96225a85e329cdf5f882e1f4bdadb22076ff2b8ac176810fc4909eb",
}
def pubkey_for_serial(serial):
    return BUNDLED_PUBKEYS.get(serial.upper())   # 128 hex X||Y, or None

# ---- honest Tier-0 / AP-1 binding fields ----
BINDING = {
    "record_version": "1.0",
    "identity_tier": "SELF-ASSERTED",
    "presence_binding_type": "firmware-mediated",
    "content_binding_type": "none",
}

def sha256(b): return hashlib.sha256(b).digest()

def find_port():
    ports = sorted(glob.glob("/dev/ttyACM*"))
    return ports[0] if ports else None

def sign_with_device(port, challenge_hex, timeout=120):
    import serial  # pyserial
    ser = serial.Serial(port, 115200, timeout=1)
    time.sleep(1.2)                       # let any reset-on-open settle
    ser.reset_input_buffer()
    # robust SIG parse: tolerate CircuitPython's OSC terminal-title escape prefix
    sig_re = re.compile(r"SIG\s+([0-9A-Fa-f]+)\s+([0-9a-fA-F]{64})\s+([0-9a-fA-F]{128})")
    print("  -> challenge sent. PRESS THE BUTTON on the Attestor to sign ...")
    deadline = time.time() + timeout
    last_send = 0.0
    buf = ""
    while time.time() < deadline:
        if time.time() - last_send > 1.5:        # resend until a matching SIG arrives
            ser.write((challenge_hex + "\n").encode())
            last_send = time.time()
        data = ser.read(256).decode("utf-8", "replace")
        if data:
            buf += data
            m = sig_re.search(buf)
            if m:
                serial_id, ch_echo, sig_hex = m.group(1), m.group(2), m.group(3)
                if ch_echo.lower() == challenge_hex.lower():
                    ser.close()
                    return serial_id.upper(), sig_hex
            buf = buf[-1024:]                     # keep a tail, avoid unbounded growth
    ser.close()
    raise TimeoutError("no matching signature received (did you press the button in time?)")

def host_verify(pubkey_xy_hex, challenge_hex, sig_hex):
    from cryptography.hazmat.primitives.asymmetric import ec, utils
    from cryptography.hazmat.primitives import hashes
    pub = ec.EllipticCurvePublicKey.from_encoded_point(
        ec.SECP256R1(), bytes.fromhex("04" + pubkey_xy_hex))
    sig = bytes.fromhex(sig_hex)
    r = int.from_bytes(sig[:32], "big")
    s = int.from_bytes(sig[32:], "big")
    der = utils.encode_dss_signature(r, s)
    digest = bytes.fromhex(challenge_hex)         # device signed this 32-byte digest
    pub.verify(der, digest, ec.ECDSA(utils.Prehashed(hashes.SHA256())))  # raises if invalid
    return True

def post_attest(api_base, ingest_body):
    # Matches app/schemas/artifact.py::ArtifactIngest. Server verifies the signature over
    # challenge_hash (prehashed), derives the short_code, and chains the entry.
    import urllib.request, urllib.error
    body = json.dumps(ingest_body, default=str).encode()
    req = urllib.request.Request(f"{api_base}/v1/attest", data=body,
                                 headers={"Content-Type": "application/json",
                                          "User-Agent": "Mozilla/5.0 (ZKNOT zk-attest)",
                                          "Accept": "application/json"}, method="POST")
    try:
        with urllib.request.urlopen(req, timeout=20) as r:
            return json.loads(r.read().decode())
    except urllib.error.HTTPError as e:
        detail = e.read().decode("utf-8", "replace")
        raise RuntimeError(f"HTTP {e.code}: {detail}") from None

def build_cert(fname, doc_hash, serial_id, ts, zk_code, chain, api):
    base = fname.split("/")[-1]
    if zk_code:
        code_line = f"**ZK number: {zk_code}**  →  https://verifyknot.io/v/{zk_code}"
        step3 = (f"Look up `{zk_code}` at https://verifyknot.io/v/{zk_code} — the server "
                 f"re-verified this signature before chaining it, and you can re-verify it yourself.")
        pos = chain.get("chain_position")
        chain_line = (f"- Chain position: {pos}  (entry_hash `{(chain.get('entry_hash') or '')[:16]}…`)\n"
                      if pos is not None else "")
    else:
        code_line = "ZK number: _(pending submission — run with --submit)_"
        step3 = "Submit the saved record to verifyknot to obtain a public ZK number."
        chain_line = ""
    return f"""# ZKNOT Attestation Certificate

{code_line}

- Document: `{base}`
- Document SHA-256: `{doc_hash}`
- Signed by device: `{serial_id}`  (SELF-ASSERTED · firmware-mediated presence)
- Attested (UTC): {ts}
{chain_line}
## What this proves
A signature was produced by device `{serial_id}`'s non-extractable key over the SHA-256
hash of this exact document, at the time above. It proves the document existed in this
exact form at that time and was approved by this device, and that it has not been altered
since. It does NOT assert that the document's contents are correct, nor the real-world
identity of the signer (this is the SELF-ASSERTED tier).

## How a skeptic verifies it — without trusting ZKNOT
1. Hash your copy of the document:  `sha256sum {base}`
2. Confirm the result equals the Document SHA-256 above. (Binds your copy to this record.)
3. {step3}

_The timestamp above is host-supplied (the device has no clock). Ordering is anchored by the chain position; independently-trusted time (RFC-3161 / transparency log) is on the roadmap._\n\n_Tier-0 / AP-1. The verifier states exactly what was proven, and no more._

Page 1 of 1
"""

def main():
    ap = argparse.ArgumentParser(description="ZKNOT document issuance (Tier-0 / SELF-ASSERTED)")
    ap.add_argument("file", help="document to attest")
    ap.add_argument("--port", default=None, help="serial port (default: autodetect /dev/ttyACM*)")
    ap.add_argument("--submit", action="store_true", help="POST to /v1/attest for a ZK number")
    ap.add_argument("--api", default="https://api.zknot.io")
    ap.add_argument("--out", default=None, help="cert path (default: <file>.zkcert.md)")
    args = ap.parse_args()

    data = open(args.file, "rb").read()
    doc_hash = sha256(data)
    challenge = sha256(doc_hash)
    doc_hash_hex, challenge_hex = doc_hash.hex(), challenge.hex()
    print(f"file: {args.file}  ({len(data)} bytes)")
    print(f"document hash (SHA-256): {doc_hash_hex}")

    port = args.port or find_port()
    if not port:
        sys.exit("no serial device found (is the Attestor plugged in?)")
    print(f"device port: {port}")

    serial_id, sig_hex = sign_with_device(port, challenge_hex)
    print(f"  <- SIG from {serial_id}")

    pub = pubkey_for_serial(serial_id)
    if not pub:
        sys.exit(f"device {serial_id} is not in the enrolled key set; cannot verify")
    host_verify(pub, challenge_hex, sig_hex)
    print("  [PASS] signature verified on this machine")

    base = args.file.split("/")[-1]
    ts = datetime.now(timezone.utc).isoformat(timespec="seconds")

    # ---- ArtifactIngest body (the server's documented contract) ----
    # The device signs challenge_hash directly; the server verifies the signature over it.
    ingest = {
        "artifact_id": str(uuid.uuid4()),
        "artifact_type": "ZKEY_SIGN",              # press-to-sign event (enum member)
        "device_id": serial_id,
        "challenge_hash": challenge_hex,           # = SHA-256(document_hash); what the device signed
        "signature": sig_hex,                      # raw r||s hex (server + verifier expect this)
        "public_key": "04" + pub,                  # uncompressed SEC1 point, hex
        "signed_at": ts,                           # host-supplied time (no device RTC); see cert note
        "metadata": {
            "product": "Rev2-Attestor",
            "document_name": base,
            "document_sha256": doc_hash_hex,        # binds the file to this record
            "signed_payload_hex": doc_hash_hex,     # = document_hash; lets the browser verifier check it
            "identity_tier": "SELF-ASSERTED",
            "presence_binding_type": "firmware-mediated",
            "content_binding_type": "none",
        },
    }

    # ---- v1 verify-record (offline / browser-verifier shape) ----
    record = dict(BINDING)
    record.update({
        "device_id": serial_id,
        "signed_payload_hex": doc_hash_hex,        # document HASH, not the document
        "challenge_hash": challenge_hex,
        "signature": sig_hex,
        "public_key": "04" + pub,
        "artifact": {"name": base, "sha256": doc_hash_hex},
    })

    zk_code = None
    chain = {}
    if args.submit:
        try:
            resp = post_attest(args.api, ingest)
            zk_code = resp.get("short_code")
            chain = {k: resp.get(k) for k in ("chain_position", "chain_prev_hash", "entry_hash")}
            print(f"  ZK number issued: {zk_code}  (chain position {chain.get('chain_position')})")
        except Exception as e:
            print(f"  !! submission failed -> {e}")
            print("     record saved locally; fix and re-run with --submit")

    req_path = args.file + ".zkrequest.json"
    open(req_path, "w").write(json.dumps(ingest, indent=2, default=str))
    rec_path = args.file + ".zkrecord.json"
    open(rec_path, "w").write(json.dumps(record, indent=2))
    out = args.out or (args.file + ".zkcert.md")
    open(out, "w").write(build_cert(args.file, doc_hash_hex, serial_id, ts, zk_code, chain, args.api))
    print(f"\ncert:    {out}\nrequest: {req_path}\nrecord:  {rec_path}")
    if not zk_code:
        print("\n(no ZK number yet — re-run with --submit when ready)")

if __name__ == "__main__":
    main()
