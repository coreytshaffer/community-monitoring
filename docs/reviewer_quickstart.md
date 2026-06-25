# Reviewer Quickstart

This guide walks you through the local validation and routing flow of the Community Monitoring pipeline using our bundled examples.

## 1. Install dependencies

```powershell
pip install -r requirements.txt
```

## 2. Run Automated Test Suite (Optional)

You can run the full test suite to prove the trust gates enforce their rules correctly.

```powershell
python -m unittest discover tests
```
*Note: The test suite intentionally processes malformed and broken examples to assert they are correctly rejected. The suite itself will pass (`OK`) if the routing behaves as expected.*

## 3. Validate station registry

Ensure the station registry meets the required metadata schema and contains no duplicate IDs.

```powershell
python scripts\validate_station_registry.py registries\known_stations.json
```

## 3. Validate observation structure

Check various payload structures against the core observation contract.

```powershell
python scripts\validate_observation.py examples\sample_observation_valid.json examples\sample_observation_quarantined.json examples\sample_observation_unknown_station.json
```

## 4. Run semantic QA/QC

Evaluate the environmental plausibility of the payload and enforce station provenance checks.

```powershell
python scripts\qaqc_observation.py examples\sample_observation_valid.json
python scripts\qaqc_observation.py examples\sample_observation_quarantined.json
python scripts\qaqc_observation.py examples\sample_observation_unknown_station.json
```

## 5. Run intake routing

Test the full routing logic which encompasses parsing, schema validation, and QA/QC in a dry-run mode.

```powershell
python scripts\route_observation.py examples\sample_observation_valid.json
python scripts\route_observation.py examples\sample_observation_quarantined.json
python scripts\route_observation.py examples\sample_observation_bad_ph.json
python scripts\route_observation.py examples\sample_observation_unknown_parameter.json
python scripts\route_observation.py examples\sample_observation_invalid_schema.json
python scripts\route_observation.py examples\sample_observation_unknown_station.json
python scripts\route_observation.py examples\sample_observation_station_parameter_mismatch.json
```

## 6. Optional write-mode demonstration

Execute the routing pipeline and securely write the sorted files to the staging directories, automatically resolving filename conflicts.

```powershell
python scripts\route_observation.py --write --output-dir staging examples\sample_observation_valid.json examples\sample_observation_quarantined.json examples\sample_observation_bad_ph.json examples\sample_observation_unknown_parameter.json examples\sample_observation_invalid_schema.json examples\sample_observation_unknown_station.json examples\sample_observation_station_parameter_mismatch.json

dir staging
```

### Expected Destinations
* **`accepted-internal`**: Passes all structural, semantic, and provenance gates. Note that this means they are accepted for internal staging, not public display!
* **`review-queue`**: Valid structure but triggers provenance uncertainty (unknown parameter, unregistered station ID, or mismatched parameter-station capabilities).
* **`quarantine`**: Structurally valid but represents physically impossible values (e.g. pH > 14).
* **`dead-letter`**: Fails basic JSON parsing or strict schema validations.
