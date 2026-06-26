import sys
import json
import os
import argparse
import hashlib
from datetime import datetime, timezone
import uuid

# Add the current directory to sys.path to import the evaluator
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from evaluate_citizen_provenance import evaluate_provenance

def compute_payload_hash(payload_dict):
    """Computes a deterministic SHA-256 hash of the JSON payload."""
    canonical_json = json.dumps(payload_dict, sort_keys=True, separators=(',', ':'))
    return hashlib.sha256(canonical_json.encode('utf-8')).hexdigest()

def create_ledger_entry(file_path):
    """Loads a payload, evaluates it, and returns a ledger entry dictionary."""
    with open(file_path, "r") as f:
        payload = json.load(f)
        
    prov_result = evaluate_provenance(payload)
    
    return {
        "ledger_entry_id": f"ledg-{uuid.uuid4().hex[:12]}",
        "recorded_at": datetime.now(timezone.utc).isoformat(),
        "observation_id": payload.get("observation_id", "unknown"),
        "observation_type": payload.get("observation_type", "unknown"),
        "waterbody": payload.get("waterbody"),
        "site_name": payload.get("site_name"),
        "provenance_status": prov_result.get("provenance_status", "unknown"),
        "review_status": prov_result.get("review_status", "unknown"),
        "quality_flag": payload.get("quality_flag", "unknown"),
        "simulated": payload.get("simulated", False),
        "source": payload.get("source", "unknown"),
        "reasons": prov_result.get("reasons", []),
        "input_file": os.path.basename(file_path),
        "schema_name": "citizen_observation",
        "schema_version": "unversioned",
        "payload_hash": compute_payload_hash(payload)
    }

def main():
    parser = argparse.ArgumentParser(description="Write review-readiness outcomes to a local trust ledger.")
    parser.add_argument("payloads", nargs="+", help="Paths to citizen observation JSON files")
    parser.add_argument("--output", help="Path to output ledger JSONL file", default="staging/citizen-trust-ledger.jsonl")
    args = parser.parse_args()

    # Ensure parent directory exists
    output_dir = os.path.dirname(os.path.abspath(args.output))
    if output_dir:
        os.makedirs(output_dir, exist_ok=True)

    entries_written = 0
    with open(args.output, "a") as out_f:
        for payload_path in args.payloads:
            try:
                entry = create_ledger_entry(payload_path)
                out_f.write(json.dumps(entry) + "\n")
                entries_written += 1
            except Exception as e:
                print(f"Failed to process {payload_path}: {e}")

    print(f"Wrote {entries_written} ledger entries to {args.output}")

if __name__ == "__main__":
    main()
