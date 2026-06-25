import sys
import json
from datetime import datetime, timezone

# Define parameter bounds
PARAMETER_RULES = {
    "pH": {"unit": "pH", "min": 0.0, "max": 14.0},
    "turbidity": {"unit": "NTU", "min": 0.0, "max": None},
    "dissolved_oxygen": {"unit": "mg/L", "min": 0.0, "max": None},
    "water_temperature": {"unit": "C", "min": -5.0, "max": 40.0},
    "temperature": {"unit": "C", "min": -20.0, "max": 60.0},
}

def parse_iso(ts):
    if ts.endswith('Z'):
        return datetime.fromisoformat(ts[:-1] + '+00:00')
    return datetime.fromisoformat(ts)

def qaqc_check(observation):
    param = observation.get("parameter")
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
        pass # Structural schema validation catches bad formats, we ignore here

    return "PASS", "Semantic QA/QC checks passed"

def main():
    if len(sys.argv) < 2:
        print("Usage: python qaqc_observation.py <file1.json> [file2.json ...]")
        sys.exit(1)

    all_passed = True
    for file_path in sys.argv[1:]:
        try:
            with open(file_path, "r") as f:
                instance = json.load(f)
            
            status, reason = qaqc_check(instance)
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
