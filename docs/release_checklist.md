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
A license has **not yet been chosen** for this repository. Until a `LICENSE` file is committed, default copyright is retained, meaning the repository is not officially "open source."

Common options to consider prior to publication:
* **MIT**: Permissive, simple, highly common for civic tech tools.
* **Apache-2.0**: Permissive, includes an explicit patent grant clause.
* **GPL-3.0**: Strong copyleft; requires derivative projects to also remain open source.

## Initial Release Candidate
**Proposed Tag:** `v0.1.0-docs-and-local-trust-gates`

### Included in this release:
* JSON Schemas (sensor observations and station metadata)
* Example JSON payload fixtures (passing and failing)
* Simulated station registry
* Structural validation scripts
* Semantic QA/QC boundary enforcement scripts
* Intake routing scripts
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
