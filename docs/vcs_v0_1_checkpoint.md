# Verifiable Citizen Science v0.1 Checkpoint

## Overview
This checkpoint marks the completion of the backend conceptual loop for the Verifiable Citizen Science (VCS) pipeline. 

The pipeline establishes a disciplined local-first trust architecture for community environmental observations. It treats community submissions as claims, not facts. They must be structurally valid, provenance-evaluated, privacy-screened, rendered for human review, and logged locally before they can ever be considered for public use.

## The Completed v0.1 Backend Loop
Through slices VCS-001 to VCS-005, the following backend skeleton has been established:

1. **Citizen Observation Fixture:** A standardized JSON representation of a community observation.
2. **Schema Validation:** Strict JSON Schema structural validation ensuring required fields and data types are present.
3. **Deterministic Provenance Evaluation:** A deterministic Python evaluator (`evaluate_citizen_provenance.py`) that scores review-readiness based on metadata completeness, location precision/privacy, and evidence clarity.
4. **Human Review Packet:** A Markdown renderer (`render_citizen_review_packet.py`) that exports a clean, human-readable summary of the payload and its provenance status to assist human reviewers.
5. **Local JSONL Trust Ledger:** An append-only local ledger stub (`write_citizen_trust_ledger.py`) that records deterministic evaluation outcomes and payload hashes to provide the pipeline with an auditable internal memory.

## Explicit Non-Goals (What is NOT Live)
To maintain project credibility and avoid unwarranted risk, the following are explicitly **out of scope** and **not implemented** in v0.1:

* **Live Community Intake:** No public-facing forms or live submission endpoints exist.
* **Public Database or Blockchain:** The ledger is a local JSONL file, not a blockchain or distributed ledger.
* **Clear Lake Watch Export:** There is no integration to push data to the public dashboard.
* **Truth Scoring / Verification:** The pipeline evaluates metadata structure and review-readiness; it does **not** determine environmental truth.
* **Image Classification:** There is no automated analysis or classification of provided photo evidence.
* **Publication Approval:** No observation is automatically approved for public release.
* **Public-Health / Regulatory Claims:** The pipeline issues no advisories, warnings, or regulatory findings.

## Prerequisites for Real Citizen Submissions (Future Work)
Before any real community observations can be ingested, the following architectural gaps must be addressed:

* **Secure Authentication & Identity:** A robust system for identifying and authorizing community submitters.
* **Live Ingestion Endpoints:** Secure, rate-limited APIs to receive JSON payloads from a mobile app or web form.
* **Media Storage & Integrity:** A secure bucket architecture for storing photo evidence and verifying hashes upon receipt.
* **Review Interface:** A UI/tooling layer for human experts to consume the review packets and make final publication decisions.
* **Routing Engine & Export:** A mechanism to securely promote approved observations from the local trust ledger to the public Clear Lake Watch dashboard.

## Reviewer "Start Here"
If you are reviewing this repository for its data governance and architecture, start by examining how the pipeline handles edge cases:

1. Read the [Proof of Observation v0.1](proof_of_observation_v0_1.md) documentation.
2. Examine the simulated boundary conditions in the `examples/` directory (e.g., missing location, sensitive location, ambiguous evidence).
3. Run the automated test suite to see the deterministic evaluation in action:
   ```bash
   python -m unittest discover tests
   ```
4. Render a human review packet for yourself:
   ```bash
   python scripts/render_citizen_review_packet.py examples/citizen_observation_valid_algae_report.json
   ```
5. Review the [Trust Ledger format](trust_ledger.md) to understand how the system maintains its internal memory.
