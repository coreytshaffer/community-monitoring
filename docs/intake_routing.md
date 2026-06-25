# Intake Routing

This document defines how environmental observation payloads are routed within the platform's intake pipeline after initial receipt.

## Routing Categories

1. **`dead-letter`**
   * **Criteria**: The payload cannot be parsed as valid JSON or fails JSON Schema structural validation.
   * **Meaning**: The message is structurally flawed and cannot be processed by the system. It is routed here for engineering review or dropped.

2. **`quarantine`**
   * **Criteria**: The payload is structurally valid, but semantic QA/QC explicitly fails (e.g., negative turbidity, impossible pH).
   * **Meaning**: The payload represents an environmentally impossible state. It is separated to ensure flawed data does not leak into public dashboards.

3. **`review-queue`**
   * **Criteria**: The payload is structurally valid, but semantic QA/QC flags it for review (e.g., unknown parameter, stale reading, uncertain unit).
   * **Meaning**: The reading is anomalous or unrecognized but not definitively impossible. A human operator must determine if the reading is valid, suspect, or requires a new schema update.

4. **`accepted-internal`**
   * **Criteria**: The payload is structurally valid and passes all semantic QA/QC gates.
   * **Meaning**: The data is eligible for internal staging and further programmatic analysis.

## Critical Principle: `accepted-internal` Does Not Mean Public Approval

Passing structural validation and automated QA/QC means the data is correctly shaped and physically plausible. **It does not automatically authorize the reading for public display on Clear Lake Watch.** 

True public trust requires cross-referencing provenance, hardware history, multi-sensor consensus, and final human sign-off before a dataset is deemed a reliable environmental record.

## Operating Model & Suggested Workflow

* **Dry-Run First**: Operators should validate new sensor integrations using dry-run tools to see where payloads would route before committing them to live staging.
* **Review Loop**: Operators should regularly review the `quarantine` and `review-queue` buckets. 
  * If the sensor is miscalibrated, issue a hardware fix.
  * If a parameter is newly introduced and flagged as unknown, update the platform's known registry.
* **Station-Aware Routing (Planned)**: While the station metadata registry exists, it is not yet strictly enforced in the router. Future updates will automatically push readings from unknown `station_id`s into the `review-queue`.
