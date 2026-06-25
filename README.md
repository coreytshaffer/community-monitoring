# Community Environmental Monitoring Platform

This project treats field sensor readings as claims that require structure, provenance, freshness, QA/QC, routing, and human review before any public-facing use.

## Portfolio Abstract

This repository represents a disciplined approach to environmental data governance. For a concise summary of the project's technical highlights, resume bullets, and core philosophy, please see the **[Portfolio Abstract](docs/portfolio_abstract.md)**.

## Repository Status

* This repository is currently a local pipeline populated exclusively with simulated/demo testing fixtures.
* It does not contain real physical sensor deployments or public environmental observations.
* The repository may be published as a portfolio artifact or open-source foundation after final review. See the **[Release Checklist](docs/release_checklist.md)** before considering publication.

## Relationship to Clear Lake Watch

This repository serves as a companion field data acquisition layer for **Clear Lake Watch**. While Clear Lake Watch is the public trust and dashboard layer, this platform focuses exclusively on capturing, validating, and qualifying community-submitted environmental data.

## What This Project Does

The platform establishes a disciplined local-first trust pipeline. It performs the following checks:
1. **JSON Parsing:** Validates basic payload legibility.
2. **Structural Validation:** Ensures payloads strictly match the data contract via JSON Schema.
3. **Semantic QA/QC:** Checks whether values fall into environmentally plausible bounds.
4. **Station Provenance Checks:** Cross-references readings with a known station registry.
5. **Intake Routing:** Sorts observations into logical queues (`accepted-internal`, `review-queue`, `quarantine`, `dead-letter`).

## What This Project Does NOT Do

* **It does not build ingestion, MQTT servers, databases, or cloud dashboards.**
* **It does not automatically publish data.** Payloads landing in `accepted-internal` still require manual review and context before going live.
* **It does not use real deployed sensor configurations yet.** All existing stations and examples are simulated or demos.

## Repository Structure

* `docs/`: Architectural and standard operating procedure documentation.
* `examples/`: Simulated payload fixtures covering various scenarios.
* `schemas/`: JSON schemas for observations and station metadata.
* `registries/`: The known station registry.
* `scripts/`: Local validation, QA/QC, and routing Python scripts.

## Setup Instructions

1. Ensure Python 3 is installed.
2. Install the lightweight dependencies:
   ```powershell
   pip install -r requirements.txt
   ```

## Testing the Pipeline

A minimal automated test suite is included to prove the scripts behave as documented without needing manual invocation.

```powershell
python -m unittest discover tests
```

*Note: It is normal and expected that tests assert on validation failures (e.g., negative pH, unknown stations, invalid JSON). The test suite passes when the pipelines correctly trap these errors.*

## Example Routing Results & Validation

For a comprehensive command-driven walkthrough of the pipeline and how it handles pass, fail, unknown stations, and parameter mismatches, see the **[Reviewer Quickstart](docs/reviewer_quickstart.md)**.

## Documentation Index

Explore the core documentation files defining this architecture:
* [Field Sensor Readiness Packet](docs/field_sensor_readiness_packet.md)
* [Architecture Sketch](docs/architecture_sketch.md)
* [Sensor Data Contract](docs/sensor_data_contract.md)
* [Station Metadata Contract](docs/station_metadata_contract.md)
* [Semantic QA/QC Rules](docs/semantic_qaqc_rules.md)
* [Intake Routing](docs/intake_routing.md)
* [MQTT Topic Conventions](docs/mqtt_topic_conventions.md)

## Safety & Publication Doctrine

We do not publish readings just because they exist. They must pass rigorous gates. 
* **Structurally invalid payloads** route to `dead-letter`.
* **Physically impossible values** route to `quarantine`.
* **Unknown stations or unallowed parameters** route to `review-queue`.

All current station IDs and payload examples in this repo are specifically marked as `demo` or `simulated` and should not be treated as live sensor data.

## Current Limitations

* The routing is primarily a local staging process; full CI and cloud intake integrations are deferred.
* Automated testing relies on local script invocations instead of `pytest` or similar frameworks.

## Suggested Next Work

* Add minimal tests for validator, QA/QC, registry, and router behavior.

## License

This project is licensed under the MIT License. See [LICENSE](LICENSE).
