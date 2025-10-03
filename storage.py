# storage.py
import json, os, time, hashlib

SIM_FILE = "simulated_candidates.json"

def hash_pii(value: str) -> str:
    return hashlib.sha256(value.encode("utf-8")).hexdigest()

def save_candidate(candidate: dict):
    # candidate: dict with fields; do not store raw email/phone
    record = candidate.copy()
    if "email" in record:
        record["email_hashed"] = hash_pii(record.pop("email"))
    if "phone" in record:
        record["phone_hashed"] = hash_pii(record.pop("phone"))
    record["saved_at"] = int(time.time())
    data = []
    if os.path.exists(SIM_FILE):
        try:
            with open(SIM_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
        except Exception:
            data = []
    data.append(record)
    with open(SIM_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)
    return True
