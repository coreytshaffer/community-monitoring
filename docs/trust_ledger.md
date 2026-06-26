# Trust Ledger

## Purpose
The **Citizen Trust Ledger** is a local, append-only JSONL file that records deterministic review-readiness outcomes for simulated citizen observations. It provides the pipeline with an auditable internal memory.

## Scope and Limitations
This ledger answers the question: *What did the local system evaluate, when, with what status and rationale?*

It explicitly **does not** answer whether an observation is environmentally true. 

* This is **not** a blockchain or distributed ledger.
* This is **not** a public database.
* This is **not** a publication approval mechanism.
* This prototype does not determine environmental truth, issue regulatory findings, or replace field/lab verification. It evaluates whether an observation contains enough provenance and metadata to support human review.

## Format
The ledger uses JSON Lines (`.jsonl`). Each line is a single JSON object representing the evaluation of one observation payload.

Key fields included:
* `ledger_entry_id`: Unique ID for the evaluation event.
* `recorded_at`: ISO8601 timestamp of evaluation.
* `observation_id`, `observation_type`, `waterbody`, `site_name`: Copied from the payload.
* `provenance_status`, `review_status`, `reasons`: Outcomes from the deterministic evaluator.
* `payload_hash`: SHA-256 hash of the canonicalized input JSON for local integrity checks (not a cryptographic proof of real-world truth).

## Usage
You can write one or more observation payloads to the ledger:

```bash
python scripts/write_citizen_trust_ledger.py examples/citizen_observation_valid_algae_report.json --output staging/citizen-trust-ledger.jsonl
```

The script will automatically append the records to the specified JSONL file, creating the file and parent directories if they do not exist.
