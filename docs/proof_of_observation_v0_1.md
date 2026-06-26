# Proof-of-Observation v0.1

## Purpose

Proof-of-Observation v0.1 defines a **chain-of-custody and review-readiness pattern** for citizen-submitted environmental observations. It establishes the gates an observation must pass before a human reviewer can evaluate it — and explicitly separates provenance status from truth status.

The goal is not to determine whether an observation is factually correct. The goal is to determine whether the observation carries enough structure, metadata, and provenance to support informed human review.

## Data Flow

```
observation
  → schema validation
    → metadata / provenance review
      → privacy gate
        → routing
          → human review packet
            → optional internal acceptance
```

Each stage evaluates a specific dimension of the observation:

| Stage | Evaluates | Outcome |
|---|---|---|
| Schema validation | Structural conformity to the observation schema | Pass / fail |
| Metadata / provenance review | Completeness of who, when, where, and how | Provenance status assigned |
| Privacy gate | Presence of private locations, identifiable individuals, sensitive coordinates | Route to privacy review or pass |
| Routing | Provenance status + privacy result → routing decision | `accepted-internal`, `review-queue`, `quarantine`, or `dead-letter` |
| Human review packet | Assemble observation + provenance status + routing rationale into a reviewable bundle | Packet exported |
| Optional internal acceptance | A qualified human reviewer marks the observation as internally accepted | `accepted-internal` (not public approval) |

## Core Distinction

> **Provenance status is not truth status.**

An observation with `complete_metadata` status means it contains all the metadata fields the schema requires, its provenance chain is traceable, and it passed the privacy gate. It does **not** mean the observation is factually accurate, environmentally significant, or suitable for public reporting.

Truth determination — if it ever occurs — requires field verification, laboratory analysis, expert judgment, and institutional review. This pipeline does none of those things.

## Recommended Future Statuses

The following provenance statuses are recommended for implementation in VCS-003:

| Status | Meaning |
|---|---|
| `complete_metadata` | All required metadata fields are present; provenance chain is traceable. |
| `incomplete_metadata` | One or more required metadata fields are missing or malformed. |
| `private_location_review` | The observation references a location flagged for privacy review (e.g., private property, sensitive ecological site). |
| `ambiguous_evidence_review` | The observation's supporting evidence is present but ambiguous — e.g., unclear photos, conflicting timestamps, or inconsistent geolocation. |
| `invalid_structure` | The observation does not conform to the schema at all. |

## Limitations

This prototype does not determine environmental truth, issue regulatory findings, or replace field/lab verification. It evaluates whether an observation contains enough provenance and metadata to support human review.

Additional limitations:

* All observations in v0.1 are simulated. No real community data is processed.
* The privacy gate in v0.1 is a conceptual placeholder. Production privacy screening would require geospatial boundary checks, PII detection, and legal review.
* `accepted-internal` is an internal routing status, not a public endorsement or approval.
* No automated downstream actions (alerts, publications, agency notifications) are triggered by any status.

## VCS-002 Schema Contract

The initial structural contract and simulated fixtures for citizen observations can be found here:

* [citizen_observation.schema.json](../schemas/citizen_observation.schema.json)
* [citizen_observation_valid_algae_report.json](../examples/citizen_observation_valid_algae_report.json)
* [citizen_observation_missing_location.json](../examples/citizen_observation_missing_location.json)
* [citizen_observation_sensitive_location.json](../examples/citizen_observation_sensitive_location.json)
* [citizen_observation_ambiguous_evidence.json](../examples/citizen_observation_ambiguous_evidence.json)

## VCS-003 Provenance Status Evaluator

The deterministic provenance status evaluator for citizen observations can be found in `scripts/evaluate_citizen_provenance.py`.

* This evaluator assigns review-readiness/provenance status.
* It does not verify environmental truth.
* It uses deterministic local rules based on metadata completeness, location privacy, and evidence clarity.
* It is intended to support later routing and human-review packet generation.

## VCS-004 Human Review Packet Export

A deterministic review packet is exported for observations entering the review queue.

* The packet is a human-review aid.
* It summarizes metadata, evidence, privacy concerns, provenance status, and limitations.
* It does not approve publication or verify the observation.
* For full formatting details and examples, see the [Review Packet Format](review_packet_format.md).
