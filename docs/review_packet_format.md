# Review Packet Format

## Purpose
The **Citizen Observation Review Packet** presents a structured, human-readable summary of a submitted environmental observation. It is designed to assist human reviewers in evaluating the review-readiness, provenance, and privacy implications of the data. 

This packet is an internal review aid, **not** a publication format or a public record.

## Limitations
This prototype does not determine environmental truth, issue regulatory findings, or replace field/lab verification. It evaluates whether an observation contains enough provenance and metadata to support human review.

## Required Sections
Each review packet is deterministically generated to include the following sections:

1. **Observation Summary:** Core fields like ID, type, and timestamps.
2. **Review Status:** Provenance status (e.g., `complete_metadata`, `private_location_review`), computed review status, and the system's reasoning for this status.
3. **Location and Privacy:** Coordinates, location precision, and privacy constraints.
4. **Evidence:** Provided evidence details (type, URI, and hash).
5. **Description:** The verbatim text submitted by the citizen.
6. **System Assessment:** Reiteration that this is a structural evaluation, not a truth verification.
7. **Recommended Human Review Questions:** Guided questions to help a reviewer evaluate the next step for the observation.
8. **Limitations:** The core limitation disclaimer regarding environmental truth.

## Usage

You can generate a review packet from an observation JSON file using the following command:

```bash
python scripts/render_citizen_review_packet.py examples/citizen_observation_valid_algae_report.json
```

By default, the packet is written to standard output (`stdout`).

### Writing to a file
To export the packet to a specific markdown file, use the `--output` flag:

```bash
python scripts/render_citizen_review_packet.py examples/citizen_observation_valid_algae_report.json --output staging/review-packets/example.md
```
