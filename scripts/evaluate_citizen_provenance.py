import sys
import json
import os
from jsonschema import validate, ValidationError, FormatChecker

def load_schema(schema_path="schemas/citizen_observation.schema.json"):
    if not os.path.exists(schema_path):
        script_dir = os.path.dirname(os.path.abspath(__file__))
        schema_path = os.path.join(script_dir, "..", "schemas", "citizen_observation.schema.json")
    with open(schema_path, "r") as f:
        return json.load(f)

def evaluate_provenance(instance):
    """
    Evaluates a citizen observation dictionary and determines its provenance status.
    Returns a result dict with provenance_status, review_status, and reasons.
    """
    observation_id = instance.get("observation_id", "unknown")
    
    # Check metadata completeness (location)
    location_precision = instance.get("location_precision")
    lat = instance.get("latitude")
    lon = instance.get("longitude")
    if location_precision in ["withheld", "unknown"] or lat is None or lon is None:
        return {
            "observation_id": observation_id,
            "provenance_status": "incomplete_metadata",
            "review_status": "human_review_required",
            "reasons": ["Location metadata is incomplete or withheld."]
        }

    # Check location privacy
    location_privacy = instance.get("location_privacy")
    if location_privacy in ["private_property", "sensitive_habitat", "withheld"]:
        return {
            "observation_id": observation_id,
            "provenance_status": "private_location_review",
            "review_status": "human_review_required",
            "reasons": [f"Location privacy is marked as '{location_privacy}'."]
        }
        
    # Check evidence ambiguity
    evidence_type = instance.get("evidence_type")
    evidence_uri = instance.get("evidence_uri")
    evidence_hash = instance.get("evidence_hash")
    
    if evidence_type == "none" or (evidence_type == "photo" and (not evidence_uri or not evidence_hash)):
        return {
            "observation_id": observation_id,
            "provenance_status": "ambiguous_evidence_review",
            "review_status": "human_review_required",
            "reasons": ["Evidence is marked as 'none' or missing required URI/hash."]
        }

    # Otherwise complete
    return {
        "observation_id": observation_id,
        "provenance_status": "complete_metadata",
        "review_status": "auto_checked",
        "reasons": ["Metadata and structure are complete."]
    }

def main():
    if len(sys.argv) < 2:
        print("Usage: python evaluate_citizen_provenance.py <observation.json>")
        sys.exit(1)
        
    file_path = sys.argv[1]
    
    try:
        schema = load_schema()
    except Exception as e:
        print(f"Error loading schema: {e}")
        sys.exit(1)
        
    try:
        with open(file_path, "r") as f:
            instance = json.load(f)
    except Exception as e:
        print(json.dumps({
            "observation_id": "unknown",
            "provenance_status": "invalid_structure",
            "review_status": "rejected",
            "reasons": [f"Failed to load JSON: {e}"]
        }, indent=2))
        sys.exit(0)
        
    # 1. Schema Validation
    try:
        validate(instance=instance, schema=schema, format_checker=FormatChecker())
    except ValidationError as e:
        print(json.dumps({
            "observation_id": instance.get("observation_id", "unknown"),
            "provenance_status": "invalid_structure",
            "review_status": "rejected",
            "reasons": [f"Schema validation failed: {e.message}"]
        }, indent=2))
        sys.exit(0)
        
    # 2. Evaluate Provenance
    result = evaluate_provenance(instance)
    print(json.dumps(result, indent=2))
    
if __name__ == "__main__":
    main()
