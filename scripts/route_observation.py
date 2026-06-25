import sys
import json
import os
import shutil
import argparse
from jsonschema import validate, ValidationError, FormatChecker

# Import local helpers safely
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from validate_observation import load_schema
from qaqc_observation import qaqc_check

def route_payload(file_path, schema, format_checker):
    try:
        with open(file_path, "r") as f:
            instance = json.load(f)
    except Exception as e:
        return "DEAD-LETTER", "dead-letter", f"JSON parse error: {e}"
        
    try:
        validate(instance=instance, schema=schema, format_checker=format_checker)
    except ValidationError as e:
        return "DEAD-LETTER", "dead-letter", f"schema validation failed: {e.message}"
        
    status, reason = qaqc_check(instance)
    
    if status == "FAIL":
        return "QUARANTINE", "quarantine", reason
    elif status == "REVIEW":
        return "REVIEW", "review-queue", reason
    elif status == "PASS":
        return "ACCEPTED-INTERNAL", "accepted-internal", reason
        
    return "DEAD-LETTER", "dead-letter", f"Unknown QA/QC status: {status}"

def main():
    parser = argparse.ArgumentParser(description="Route observation payloads based on validation and QA/QC gates.")
    parser.add_argument("--write", action="store_true", help="Enable write mode (copies files to output-dir)")
    parser.add_argument("--output-dir", type=str, default="staging", help="Output directory for routed files in write mode")
    parser.add_argument("files", nargs="+", help="JSON files to route")
    
    args = parser.parse_args()
    
    try:
        schema = load_schema()
    except Exception as e:
        print(f"Error loading schema: {e}")
        sys.exit(1)
        
    format_checker = FormatChecker()
    
    if args.write:
        for dest in ["accepted-internal", "review-queue", "quarantine", "dead-letter"]:
            os.makedirs(os.path.join(args.output_dir, dest), exist_ok=True)
            
    all_accepted = True
    for file_path in args.files:
        if not os.path.exists(file_path):
            print(f"ERROR: File not found: {file_path}")
            all_accepted = False
            continue
            
        label, dest_dir, reason = route_payload(file_path, schema, format_checker)
        
        # Output style requested: LABEL file -> dest: reason (omitted for ACCEPTED-INTERNAL)
        if label == "ACCEPTED-INTERNAL":
            print(f"{label} {file_path} -> {dest_dir}")
        else:
            all_accepted = False
            print(f"{label} {file_path} -> {dest_dir}: {reason}")
            
        if args.write:
            dest_path = os.path.join(args.output_dir, dest_dir, os.path.basename(file_path))
            if os.path.exists(dest_path):
                import uuid
                base, ext = os.path.splitext(os.path.basename(file_path))
                dest_path = os.path.join(args.output_dir, dest_dir, f"{base}_{uuid.uuid4().hex[:6]}{ext}")
            shutil.copy2(file_path, dest_path)
            
    if not all_accepted:
        sys.exit(1)
    sys.exit(0)

if __name__ == "__main__":
    main()
