# Sensor Data Contract

This document defines the minimal JSON data contract for field observations. It establishes the required structure and allowed values for all incoming sensor telemetry.

## Schema Definition

### Fields
- `observation_id` (string): A unique identifier for the specific reading (e.g., UUID).
- `sensor_id` (string): The unique identifier of the sensor producing the data.
- `station_id` (string): The identifier for the physical location/station where the sensor is deployed.
- `observed_at` (string): ISO 8601 timestamp of when the physical reading was taken.
- `received_at` (string): ISO 8601 timestamp of when the platform received the payload.
- `parameter` (string): The environmental variable being measured (e.g., "temperature", "pH", "dissolved_oxygen").
- `value` (float): The numeric measurement.
- `unit` (string): The unit of measurement (e.g., "C", "mg/L").
- `latitude` (float): The latitude coordinate of the observation.
- `longitude` (float): The longitude coordinate of the observation.
- `source` (string): The origin system or protocol (e.g., "lorawan_gateway_01").
- `quality_flag` (string): The current data quality classification.
- `review_status` (string): The current state of human or automated review.
- `notes` (string): Optional field for additional context or human reviewer comments.

### Allowed Values

#### `quality_flag`
- `raw`: Initial state upon ingestion before any checks.
- `valid`: Passed automated QA/QC gates.
- `suspect`: Failed automated checks; requires review.
- `invalid`: Confirmed to be erroneous.
- `quarantined`: Isolated due to suspected sensor failure or extreme anomalies.

#### `review_status`
- `unreviewed`: Default state for new data.
- `auto_checked`: Processed by automated QA/QC rules.
- `human_review_required`: Flagged for manual inspection.
- `approved_for_internal_use`: Verified, but not cleared for public release.
- `approved_for_publication`: Fully validated and ready for Clear Lake Watch.
- `rejected`: Manually reviewed and discarded.

## Example JSON Records

### Valid Observation
```json
{
  "observation_id": "550e8400-e29b-41d4-a716-446655440000",
  "sensor_id": "temp_probe_a1",
  "station_id": "station_north_shore",
  "observed_at": "2026-06-25T08:30:00Z",
  "received_at": "2026-06-25T08:30:05Z",
  "parameter": "temperature",
  "value": 18.5,
  "unit": "C",
  "latitude": 39.0435,
  "longitude": -122.8821,
  "source": "mqtt_bridge",
  "quality_flag": "valid",
  "review_status": "auto_checked",
  "notes": ""
}
```

### Quarantined Observation
```json
{
  "observation_id": "6ba7b810-9dad-11d1-80b4-00c04fd430c8",
  "sensor_id": "ph_sensor_b2",
  "station_id": "station_east_bay",
  "observed_at": "2026-06-25T08:45:00Z",
  "received_at": "2026-06-25T08:45:10Z",
  "parameter": "pH",
  "value": 15.2,
  "unit": "pH",
  "latitude": 39.0210,
  "longitude": -122.8500,
  "source": "mqtt_bridge",
  "quality_flag": "quarantined",
  "review_status": "human_review_required",
  "notes": "Value exceeds physically possible upper bound of 14.0"
}
```

## Structural vs. Semantic Validation

* **JSON Schema validates structure only**: The schema defined in this repository ensures that incoming data has the correct fields, types, and allowed enumerated values (like `quality_flag`).
* **QA/QC rules determine publishability**: A payload may be structurally valid but semantically flawed (e.g., an impossible parameter value). In this case, the `quality_flag` might be `quarantined`, meaning it passes schema validation but fails semantic QA/QC.
* **Separation of Concerns**: A quarantined observation is still structurally sound and can flow through the platform's routing logic, but it remains unsuitable for public display until human review occurs.
