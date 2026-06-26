# Initial Release Checklist

## Before Publishing
- [ ] Confirm repository contains no secrets, API keys, or credentials.
- [ ] Confirm all station IDs and examples are explicitly marked as `simulated` or `demo`.
- [ ] Confirm no real physical sensor data is included in the payload fixtures.
- [ ] Confirm no private household, location, or sensitive security information is included.
- [ ] Confirm `staging/`, `__pycache__/`, and other generated artifacts are included in `.gitignore`.
- [ ] Confirm automated tests pass (`python -m unittest discover tests`).
- [ ] Confirm `README.md` accurately scopes the project as a local staging trust gate rather than a real-time IoT dashboard.
- [ ] Confirm `accepted-internal` routing destination is **not** described as equivalent to public approval or automatic publication.

## License Decision
The **MIT License** has been selected for this repository.

**Why MIT?**
* **Permissive and simple**: Highly common and well-understood in the civic tech and open-source community.
* **Portfolio-friendly**: Encourages low-friction reuse, adaptation, and sharing.
* **Appropriate for scope**: As a local staging pipeline without commercial/patented hardware control mechanisms, MIT provides the right balance of openness and attribution.

*Note: If explicit patent grant language becomes a requirement for future institutional/commercial reuse, an upgrade to **Apache-2.0** could be considered. For now, MIT is sufficient.*

## Initial Release Candidate
**Proposed Tag:** `v0.1.0-docs-and-local-trust-gates`

### Included in this release:
* JSON Schemas (sensor observations and station metadata)
* Example JSON payload fixtures (passing and failing)
* Simulated station registry
* Structural validation scripts
* Semantic QA/QC boundary enforcement scripts
* Intake routing scripts
* Citizen provenance evaluator script
* Citizen human review packet renderer
* Citizen local trust ledger stub
* Minimal `unittest` validation suite
* Documentation (Readiness Packet, Contract, QA/QC Rules, Routing, Quickstart, Metadata, Portfolio Abstract)

### NOT included in this release:
* Live field sensors or hardware deployments
* Active MQTT broker connections
* Public-facing dashboards
* Production database storage
* Cloud deployments or CI/CD integrations
* Automatic public publication workflows
* Official agency water-quality data
* Real Clear Lake field measurements

## Verifiable Citizen Science / Proof-of-Observation Checks

- [ ] Confirm citizen-observation examples are simulated.
- [ ] Confirm no real submitter names, household details, private locations, faces, license plates, or sensitive site coordinates are included.
- [ ] Confirm provenance status is not described as truth status.
- [ ] Confirm `accepted-internal` routing is not described as public approval.
- [ ] Confirm no automated public-health, regulatory, or agency-notification claims are made.
