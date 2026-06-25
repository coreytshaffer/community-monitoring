import sys
import json
import os
from jsonschema import validate, ValidationError

def main():
    if len(sys.argv) != 2:
        print("Usage: python validate_station_registry.py <registry_file.json>")
        sys.exit(1)

    registry_path = sys.argv[1]
    schema_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "schemas", "station.schema.json")
    
    try:
        with open(schema_path, "r") as f:
            schema = json.load(f)
    except Exception as e:
        print(f"ERROR: Cannot load schema: {e}")
        sys.exit(1)
        
    try:
        with open(registry_path, "r") as f:
            registry = json.load(f)
    except Exception as e:
        print(f"ERROR: Cannot load registry JSON: {e}")
        sys.exit(1)
        
    if not isinstance(registry, list):
        print("ERROR: Registry must be a JSON array of station objects.")
        sys.exit(1)
        
    all_passed = True
    seen_ids = set()
    
    for i, station in enumerate(registry):
        station_id = station.get("station_id", f"index-{i}")
        
        try:
            validate(instance=station, schema=schema)
            print(f"PASS: Station '{station_id}' matches schema.")
        except ValidationError as e:
            print(f"FAIL: Station '{station_id}' schema validation failed: {e.message}")
            all_passed = False
            
        if station_id in seen_ids:
            print(f"FAIL: Duplicate station_id found: '{station_id}'")
            all_passed = False
        else:
            seen_ids.add(station_id)
            
    if not all_passed:
        print("\nRegistry validation failed.")
        sys.exit(1)
        
    print("\nRegistry validation successful.")
    sys.exit(0)

if __name__ == "__main__":
    main()
