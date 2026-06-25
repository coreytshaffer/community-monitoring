import sys
import json
import os
from datetime import datetime, timezone

# Define parameter bounds
PARAMETER_RULES = {
    "pH": {"unit": "pH", "min": 0.0, "max": 14.0},
    "turbidity": {"unit": "NTU", "min": 0.0, "max": None},
    "dissolved_oxygen": {"unit": "mg/L", "min": 0.0, "max": None},
    "water_temperature": {"unit": "C", "min": -5.0, "max": 40.0},
    "temperature": {"unit": "C", "min": -20.0, "max": 60.0},
    "air_temperature": {"unit": "C", "min": -40.0, "max": 60.0},
}

def parse_iso(ts):
    if ts.endswith('Z'):
        return datetime.fromisoformat(ts[:-1] + '+00:00')
    return datetime.fromisoformat(ts)

def load_station_registry(registry_path="registries/known_stations.json"):
    if not os.path.exists(registry_path):
        script_dir = os.path.dirname(os.path.abspath(__file__))
        registry_path = os.path.join(script_dir, "..", "registries", "known_stations.json")
    with open(registry_path, "r") as f:
        registry = json.load(f)
    return {s["station_id"]: s for s in registry}

def qaqc_check(observation, stations_registry=None):
    if stations_registry is None:
        try:
            stations_registry = load_station_registry()
        except Exception as e:
            return "FAIL", f"Unable to load station registry: {e}"

    station_id = observation.get("station_id")
    if station_id not in stations_registry:
        return "REVIEW", f"unknown station_id '{station_id}' requires human review"

    station = stations_registry[station_id]

    if station.get("status") in ["inactive", "retired"]:
        return "REVIEW", f"station '{station_id}' is {station.get('status')} and not eligible for normal intake"

    param = observation.get("parameter")
    if param not in station.get("allowed_parameters", []):
        return "REVIEW", f"parameter '{param}' not allowed for station '{station_id}'"

    value = observation.get("value")
    unit = observation.get("unit")

    if param not in PARAMETER_RULES:
        return "REVIEW", f"Unknown parameter '{param}' requires human review"

    rules = PARAMETER_RULES[param]

    if rules["unit"] and unit != rules["unit"]:
        return "FAIL", f"Invalid unit '{unit}' for {param}. Expected '{rules['unit']}'"

    if rules["min"] is not None and value < rules["min"]:
        return "FAIL", f"{param} cannot be less than {rules['min']} (got {value})"

    if rules["max"] is not None and value > rules["max"]:
        return "FAIL", f"{param} cannot be greater than {rules['max']} (got {value})"

    # Simple freshness check: received vs observed
    try:
        observed_at = parse_iso(observation.get("observed_at"))
        received_at = parse_iso(observation.get("received_at"))
        if (received_at - observed_at).total_seconds() > 86400:
            return "REVIEW", "Observation is stale (> 24 hours between observation and receipt)"
    except Exception:
        pass

    return "PASS", "Semantic QA/QC checks passed"

def main():
    import argparse
    parser = argparse.ArgumentParser(description="Run semantic QA/QC checks on observations.")
    parser.add_argument("--station-registry", type=str, default="registries/known_stations.json", help="Path to known stations registry JSON")
    parser.add_argument("files", nargs="+", help="JSON files to QA/QC")
    args = parser.parse_args()

    try:
        stations_registry = load_station_registry(args.station_registry)
    except Exception as e:
        print(f"Error loading station registry: {e}")
        sys.exit(1)

    all_passed = True
    for file_path in args.files:
        try:
            with open(file_path, "r") as f:
                instance = json.load(f)

            status, reason = qaqc_check(instance, stations_registry)
            print(f"{status} {file_path}: {reason}")

            if status != "PASS":
                all_passed = False

        except Exception as e:
            print(f"FAIL {file_path}: Unable to process file ({e})")
            all_passed = False

    if not all_passed:
        sys.exit(1)
    sys.exit(0)

if __name__ == "__main__":
    main()
