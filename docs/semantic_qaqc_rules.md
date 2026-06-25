# Semantic QA/QC Rules

This document defines the semantic rules for evaluating whether a structurally valid observation contains environmentally plausible values. These rules do not automatically approve data for publication. Rather, they provide operator-facing findings that support quarantine, review, or rejection decisions.

## Evaluated Parameters

### `pH`
* **Valid physical range**: 0 to 14
* **Rule**: Values outside this range will fail semantic QA/QC.

### `turbidity`
* **Unit**: `NTU`
* **Rule**: Values cannot be negative. Negative values will fail semantic QA/QC.

### `dissolved_oxygen`
* **Unit**: `mg/L`
* **Rule**: Values cannot be negative. Very high values (e.g., > 20 mg/L) are physically rare and should be flagged as suspect for review, but are not automatically rejected unless explicitly negative. Negative values fail semantic QA/QC.

### `water_temperature`
* **Unit**: `C`
* **Rule**: Values must be within plausible freshwater bounds (e.g., -5°C to 40°C). Values outside this conservative range will fail semantic QA/QC.

## Additional Behaviors

* **Missing fields**: Handled by JSON schema validation (structural) before reaching QA/QC.
* **Negative Values**: Most parameters cannot be negative (except temperature if in C).
* **Unknown Parameters**: If the parameter is not listed in the rulebook, the script flags it as `REVIEW` instead of `FAIL`. This prevents valid but newly introduced sensors from being permanently quarantined while still demanding human attention.
* **Unknown Units**: If a parameter is known but the unit does not match expectations (e.g., `pH` unit is not `pH`), it will fail semantic QA/QC.
* **Stale Observations**: If the `observed_at` timestamp is significantly older than the `received_at` timestamp (e.g., > 24 hours lag), the record is considered stale and should be flagged for review.
* **Invalid Coordinates**: Coordinates outside the Lake County region bounds (or standard Earth bounds [-90, 90] / [-180, 180]) will fail QA/QC if verified.

## Station Provenance Rules

* **Unknown Station**: If the `station_id` is missing from `registries/known_stations.json`, the observation is flagged for `REVIEW`.
* **Parameter Mismatch**: If the parameter is not explicitly listed in the station's `allowed_parameters`, the observation is flagged for `REVIEW`.
* **Station Status**: If the station's status is `inactive` or `retired`, the observation is flagged for `REVIEW`. Demo, planned, and active stations pass this gate for internal staging purposes.

## Why QA/QC Findings are Recommendations

Passing semantic QA/QC means an observation is not trivially false. However, passing these checks **does not** automatically mean the reading is approved for publication. Human review, context evaluation, and cross-verification of historical trends and sensor provenance remain essential.
