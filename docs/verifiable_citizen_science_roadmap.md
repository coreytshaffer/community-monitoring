# Verifiable Citizen Science Roadmap

## Project Direction

Verifiable Citizen Science (VCS) extends the existing **Community Environmental Monitoring Platform** from field-sensor trust gates into a broader pipeline for citizen-submitted environmental observations.

The core claim of this platform remains unchanged: **observations are claims that require structure, provenance, privacy screening, and human review before any public-facing use.** The system evaluates whether citizen observations are structured, provenance-aware, privacy-bounded, and ready for human review. It does not determine environmental truth.

## Core Framing

Every citizen observation entering the pipeline is treated as a claim, not a fact. The system's job is to evaluate:

1. **Structure** — Does the observation conform to the expected schema?
2. **Provenance** — Does the observation carry sufficient metadata about who submitted it, when, where, and under what conditions?
3. **Privacy** — Does the observation avoid exposing private locations, identifiable individuals, or sensitive site coordinates?
4. **Review readiness** — Is the observation complete enough to present to a qualified human reviewer?

Only after passing these gates and receiving explicit human approval can an observation be considered for any downstream use. The pipeline never bypasses expert judgment.

## v0.1 Focus

Version 0.1 operates exclusively on **simulated observations**. No real community submissions are accepted, processed, or stored. All fixtures, examples, and test data are synthetic and explicitly labeled as such.

## Phased Roadmap

### VCS-001 — Docs-Only Roadmap *(current phase)*

* Define the Verifiable Citizen Science direction.
* Document the Proof-of-Observation v0.1 concept.
* Update README and release checklist with VCS framing.
* No runtime code, schemas, or fixtures.

### VCS-002 — Citizen Observation Schema + Simulated Fixtures

* Define a JSON Schema for citizen-submitted observations.
* Create simulated fixture files covering valid, invalid, and edge-case observations.
* All fixtures explicitly marked as simulated/demo.

### VCS-003 — Provenance-Status Evaluator

* Implement a local evaluator that assigns provenance status to observations.
* Statuses include `complete_metadata`, `incomplete_metadata`, `private_location_review`, `ambiguous_evidence_review`, and `invalid_structure`.
* Provenance status is explicitly not truth status.

### VCS-004 — Human Review Packet Export

* Export observations that pass schema validation and provenance evaluation into a structured review packet.
* Review packets are formatted for human reviewers, not automated downstream systems.
* `accepted-internal` routing is not public approval.

### VCS-005 — Local Trust Ledger Stub

* Stub a local-only trust ledger for tracking observation provenance decisions.
* No blockchain, DAO, or distributed ledger infrastructure.
* The ledger is an internal audit trail, not a public verification system.

## Explicit Non-Goals

The following are explicitly out of scope for Verifiable Citizen Science v0.1:

* **No real community submissions.** All observations are simulated.
* **No live public reporting.** No dashboards, alerts, or public-facing outputs.
* **No public-health guidance.** The system does not issue health advisories or safety recommendations.
* **No regulatory violation claims.** The system does not assert regulatory compliance or non-compliance.
* **No agency notification workflows.** The system does not send notifications to regulatory agencies.
* **No truth scores.** Provenance status evaluates metadata completeness, not factual accuracy.
* **No blockchain/DAO framing in v0.1.** Trust ledger work (VCS-005) uses local-only, non-distributed storage.
* **No facial recognition, ALPR, biometrics, or surveillance use cases.** This pipeline processes environmental observations only. It does not process images of people, license plates, or any biometric data. Surveillance applications are categorically excluded.
