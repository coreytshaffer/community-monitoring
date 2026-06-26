import sys
import json
import os
import argparse

# Add the current directory to sys.path to import the evaluator
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from evaluate_citizen_provenance import evaluate_provenance

def render_packet(instance, provenance_result):
    """Renders the Markdown review packet based on observation and provenance."""
    
    # Extract fields with defaults
    obs_id = instance.get("observation_id", "Unknown")
    obs_type = instance.get("observation_type", "Unknown")
    waterbody = instance.get("waterbody", "Not provided")
    site_name = instance.get("site_name", "Not provided")
    observed_at = instance.get("observed_at", "Unknown")
    submitted_at = instance.get("submitted_at", "Unknown")
    simulated = instance.get("simulated", False)
    
    prov_status = provenance_result.get("provenance_status", "Unknown")
    rev_status = provenance_result.get("review_status", "Unknown")
    reasons = "\n- ".join([""] + provenance_result.get("reasons", ["No reasons provided."]))
    
    lat = instance.get("latitude", "Not provided")
    lon = instance.get("longitude", "Not provided")
    loc_precision = instance.get("location_precision", "Unknown")
    loc_privacy = instance.get("location_privacy", "Unknown")
    
    ev_type = instance.get("evidence_type", "none")
    ev_uri = instance.get("evidence_uri", "Not provided")
    ev_hash = instance.get("evidence_hash", "Not provided")
    
    description = instance.get("description", "No description provided.")

    md = f"""# Citizen Observation Review Packet

## Observation Summary
- Observation ID: {obs_id}
- Observation Type: {obs_type}
- Waterbody: {waterbody}
- Site Name: {site_name}
- Observed At: {observed_at}
- Submitted At: {submitted_at}
- Simulated: {simulated}

## Review Status
- Provenance Status: {prov_status}
- Review Status: {rev_status}
- Reasons:{reasons}

## Location and Privacy
- Latitude: {lat}
- Longitude: {lon}
- Location Precision: {loc_precision}
- Location Privacy: {loc_privacy}
- Privacy Notes: Ensure private or sensitive locations are protected before internal use.

## Evidence
- Evidence Type: {ev_type}
- Evidence URI: {ev_uri}
- Evidence Hash: {ev_hash}
- Evidence Notes: Evidence has not been verified or fact-checked by the system.

## Description
{description}

## System Assessment
This packet evaluates review-readiness and provenance metadata. It does not verify environmental truth.

## Recommended Human Review Questions
- Is the location suitable for internal use or should it be generalized/withheld?
- Is the evidence sufficient to support follow-up?
- Should the observation be rejected, held for more information, or approved for internal use?
- Is any public-facing use inappropriate because of privacy, ambiguity, or missing metadata?

## Limitations
This prototype does not determine environmental truth, issue regulatory findings, or replace field/lab verification. It evaluates whether an observation contains enough provenance and metadata to support human review.
"""
    return md

def main():
    parser = argparse.ArgumentParser(description="Render a citizen observation review packet.")
    parser.add_argument("payload", help="Path to the citizen observation JSON file")
    parser.add_argument("--output", help="Optional path to output the markdown file", default=None)
    args = parser.parse_args()

    try:
        with open(args.payload, "r") as f:
            instance = json.load(f)
    except Exception as e:
        print(f"Error loading JSON: {e}")
        sys.exit(1)

    try:
        result = evaluate_provenance(instance)
    except Exception as e:
        print(f"Error evaluating provenance: {e}")
        sys.exit(1)

    packet_md = render_packet(instance, result)

    if args.output:
        os.makedirs(os.path.dirname(os.path.abspath(args.output)), exist_ok=True)
        with open(args.output, "w") as f:
            f.write(packet_md)
        print(f"Packet successfully written to {args.output}")
    else:
        print(packet_md)

if __name__ == "__main__":
    main()
