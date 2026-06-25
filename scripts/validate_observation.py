import sys
import json
import os
from jsonschema import validate, ValidationError, FormatChecker

def load_schema(schema_path="schemas/sensor_observation.schema.json"):
    # Allow the script to be run from different directories
    if not os.path.exists(schema_path):
        # Try relative to the script
        script_dir = os.path.dirname(os.path.abspath(__file__))
        schema_path = os.path.join(script_dir, "..", "schemas", "sensor_observation.schema.json")
    
    with open(schema_path, "r") as f:
        return json.load(f)

def main():
    if len(sys.argv) < 2:
        print("Usage: python validate_observation.py <file1.json> [file2.json ...]")
        sys.exit(1)

    try:
        schema = load_schema()
    except Exception as e:
        print(f"Error loading schema: {e}")
        sys.exit(1)

    format_checker = FormatChecker()
    
    all_passed = True
    for file_path in sys.argv[1:]:
        try:
            with open(file_path, "r") as f:
                instance = json.load(f)
            validate(instance=instance, schema=schema, format_checker=format_checker)
            print(f"PASS: {file_path}")
        except FileNotFoundError:
            print(f"FAIL: {file_path} (File not found)")
            all_passed = False
        except json.JSONDecodeError as e:
            print(f"FAIL: {file_path} (Invalid JSON: {e})")
            all_passed = False
        except ValidationError as e:
            print(f"FAIL: {file_path} (Schema validation failed: {e.message})")
            all_passed = False
            
    if not all_passed:
        sys.exit(1)
    sys.exit(0)

if __name__ == "__main__":
    main()
