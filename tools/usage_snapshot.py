#!/usr/bin/env python3
"""Pure Bible usage snapshot for /api/purebible/usage/.

Reads every UsageDay record from the app's CloudKit public database (Production) with a
server-to-server key, drops the owner's own devices and App Review devices (a version
newer than the one the App Store sells), compresses and encrypts the rows with AES-256-GCM
under a key derived from USAGE_PASSPHRASE (PBKDF2-SHA256), and saves the result in one
UsageSnapshot record that the page can read without signing in. Without the passphrase
the record is noise. Secrets come from the environment; nothing is printed but counts.
"""
import base64, datetime as dt, gzip, hashlib, json, os, subprocess, urllib.request
from cryptography.hazmat.primitives.ciphers.aead import AESGCM

CONTAINER = "iCloud.group.PureBibleContainer"
OWNER = "_d948aa0b9936d4caa5a09dfdf5703b58"
FIELDS = ["device", "day", "firstDay", "country", "version", "build", "main", "reference", "split",
          "language", "theme", "typeface", "platform", "model", "os", "opens", "seconds"]
KEY_PATH = os.environ["CK_KEY_PATH"]
KEY_ID = os.environ["CK_KEY_ID"]
PASSPHRASE = os.environ["USAGE_PASSPHRASE"].encode()


def request(operation, body):
    sub = f"/database/1/{CONTAINER}/production/public/{operation}"
    payload = json.dumps(body).encode()
    date = dt.datetime.now(dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    message = f"{date}:{base64.b64encode(hashlib.sha256(payload).digest()).decode()}:{sub}"
    signature = subprocess.run(["openssl", "dgst", "-sha256", "-sign", KEY_PATH], input=message.encode(),
                               capture_output=True, check=True).stdout
    req = urllib.request.Request("https://api.apple-cloudkit.com" + sub, data=payload, method="POST", headers={
        "Content-Type": "application/json", "X-Apple-CloudKit-Request-KeyID": KEY_ID,
        "X-Apple-CloudKit-Request-ISO8601Date": date,
        "X-Apple-CloudKit-Request-SignatureV1": base64.b64encode(signature).decode()})
    with urllib.request.urlopen(req, timeout=60) as response:
        return json.load(response)


def newer(a, b):
    pa, pb = [int(x) for x in a.split(".")], [int(x) for x in b.split(".")]
    n = max(len(pa), len(pb)); pa += [0] * (n - len(pa)); pb += [0] * (n - len(pb))
    return pa > pb


def main():
    store = json.load(urllib.request.urlopen("https://itunes.apple.com/lookup?id=6467870565&country=us", timeout=30))
    live = store["results"][0]["version"]
    rows, marker = [], None
    while True:
        body = {"query": {"recordType": "UsageDay"}, "resultsLimit": 200}
        if marker:
            body["continuationMarker"] = marker
        reply = request("records/query", body)
        for record in reply.get("records", []):
            if record.get("serverErrorCode"):
                continue
            row = {k: record.get("fields", {}).get(k, {}).get("value") for k in FIELDS}
            row["person"] = record.get("created", {}).get("userRecordName", "")
            rows.append(row)
        marker = reply.get("continuationMarker")
        if not marker:
            break
    kept = [r for r in rows if r.get("device") and r.get("day") and r["person"] != OWNER
            and not (r.get("version") and newer(r["version"], live))]
    stamp = dt.datetime.now(dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    plain = gzip.compress(json.dumps({"updated": stamp, "live": live, "rows": kept,
                                      "dropped": len(rows) - len(kept)}, separators=(",", ":")).encode())
    salt, nonce = os.urandom(16), os.urandom(12)
    key = hashlib.pbkdf2_hmac("sha256", PASSPHRASE, salt, 310000, 32)
    sealed = base64.b64encode(salt + nonce + AESGCM(key).encrypt(nonce, plain, None)).decode()
    reply = request("records/modify", {"operations": [{"operationType": "forceReplace", "record": {
        "recordName": "usageSnapshot", "recordType": "UsageSnapshot",
        "fields": {"payload": {"value": sealed}, "updated": {"value": stamp}}}}]})
    error = reply["records"][0].get("serverErrorCode")
    print(f"rows {len(rows)} kept {len(kept)} live {live} bytes {len(sealed)} {'ERROR ' + error if error else 'saved'}")
    if error:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
