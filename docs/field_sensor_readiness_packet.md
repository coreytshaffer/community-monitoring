# Field Sensor Readiness Packet

## Purpose of the Platform
The Community Environmental Monitoring Platform is the future field data acquisition layer. It is designed to capture, validate, and structure environmental observations from remote hardware. Its primary mandate is data integrity, ensuring that any sensor reading is subjected to rigorous quality checks before being considered for broader consumption.

## Relationship to Clear Lake Watch
Clear Lake Watch serves as the public trust and dashboard layer. The Community Environmental Monitoring Platform acts as a companion to Clear Lake Watch, providing the foundational telemetry that, once fully validated, can feed into public environmental reporting. The platform does not claim environmental truth just because a sensor emitted a reading; rather, it prepares data to meet the high standards required by Clear Lake Watch.

## Field Sensor Data Lifecycle
1. **Acquisition:** Raw data is captured by field sensors and transmitted via MQTT.
2. **Ingestion & Validation:** Incoming payloads are validated against the sensor data contract.
3. **Quarantine/Review:** Suspect or anomalous readings are flagged and placed in quarantine for human review.
4. **Promotion:** Data that passes all QA/QC gates (or is approved by human review) is marked as publishable.
5. **Consumption:** Publishable data is made available for downstream systems like Clear Lake Watch.

## Publishable vs Non-Publishable Data
- **Publishable:** Data that has successfully passed all QA/QC gates or has been manually reviewed and approved.
- **Non-Publishable:** Raw, unvalidated, suspect, or quarantined data that has not yet met the criteria for public consumption.

## Resource Freshness vs Observation Freshness
- **Observation Freshness:** The exact timestamp when the sensor recorded the physical phenomenon (`observed_at`).
- **Resource Freshness:** The timestamp when the platform received and processed the data (`received_at`).
*Note:* A sensor may batch and delay transmission, meaning observation freshness can lag behind resource freshness. Both must be tracked to accurately assess data relevance.

## QA/QC Gates
All incoming observations must pass automated Quality Assurance and Quality Control (QA/QC) gates:
- **Schema Validation:** Payload must match the expected JSON structure.
- **Range Checks:** Values must fall within physically possible bounds for the given parameter (e.g., pH between 0 and 14).
- **Rate of Change Check:** The difference between consecutive readings should not exceed expected environmental variance.

## Quarantine Rules
Readings that fail QA/QC gates are immediately flagged as `suspect` and placed in quarantine. Quarantined data is isolated from the main publishable dataset and cannot be accessed by public-facing layers until reviewed.

## Dead-Letter Handling
Messages that are fundamentally malformed, lack required identifiers, or fail basic schema validation are routed to a dead-letter queue. These messages are logged for engineering diagnostics but do not enter the environmental data pipeline.

## Human Review Requirements
Quarantined data requires manual intervention. A qualified reviewer must examine the context, compare historical trends, and either:
- Approve the data for internal use.
- Approve the data for publication.
- Reject the data as invalid.

## Minimal Viable Deployment Path
1. Define and enforce the data contract.
2. Establish a lightweight message broker with strict topic routing.
3. Implement basic QA/QC rules and quarantine routing.
4. Provide a simple interface for engineers/scientists to review quarantined data.
5. Expose only fully validated data to downstream consumers.

## Known Limitations
- Initial deployment lacks automated sensor calibration drift detection.
- Human review is a potential bottleneck if anomaly rates are high.
- The platform does not currently support bidirectional sensor control or OTA updates.

## Local Intake Gates
The platform currently implements the following sequence for local intake processing:
1. **JSON Parsing:** Validates basic payload legibility.
2. **Structural Validation (JSON Schema):** Ensures the payload strictly matches the data contract (required fields, types, enumerations).
3. **Semantic QA/QC:** Evaluates whether structurally valid observations represent environmentally plausible values.
4. **Intake Routing:** Sorts payloads into logical queues (`dead-letter`, `quarantine`, `review-queue`, `accepted-internal`) based on the outcomes of the prior steps.
5. **Station Metadata/Provenance Review:** Station metadata provides an independent provenance layer. During QA/QC, known stations are validated against their allowed parameters and operational status. Unknown or unauthorized readings are flagged for review.
6. **Human Review Before Publication:** Finally, even payloads that successfully land in `accepted-internal` must undergo human contextual review and final provenance checks before they are considered suitable for public consumption on Clear Lake Watch.
