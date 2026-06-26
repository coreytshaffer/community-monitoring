import unittest
import json
import os
import subprocess
import tempfile

class TestEvaluateCitizenProvenance(unittest.TestCase):
    def setUp(self):
        self.script = os.path.join("scripts", "evaluate_citizen_provenance.py")
        self.examples_dir = "examples"

    def run_evaluator(self, filepath):
        result = subprocess.run(["python", self.script, filepath], capture_output=True, text=True)
        self.assertEqual(result.returncode, 0)
        return json.loads(result.stdout)

    def test_complete_metadata(self):
        filepath = os.path.join(self.examples_dir, "citizen_observation_valid_algae_report.json")
        result = self.run_evaluator(filepath)
        self.assertEqual(result["provenance_status"], "complete_metadata")

    def test_incomplete_metadata(self):
        filepath = os.path.join(self.examples_dir, "citizen_observation_missing_location.json")
        result = self.run_evaluator(filepath)
        self.assertEqual(result["provenance_status"], "incomplete_metadata")

    def test_private_location_review(self):
        filepath = os.path.join(self.examples_dir, "citizen_observation_sensitive_location.json")
        result = self.run_evaluator(filepath)
        self.assertEqual(result["provenance_status"], "private_location_review")

    def test_ambiguous_evidence_review(self):
        filepath = os.path.join(self.examples_dir, "citizen_observation_ambiguous_evidence.json")
        result = self.run_evaluator(filepath)
        self.assertEqual(result["provenance_status"], "ambiguous_evidence_review")

    def test_invalid_structure(self):
        # Create a temporary invalid JSON file (missing required fields)
        invalid_payload = {
            "observation_id": "invalid-123",
            "simulated": True
            # missing observation_type
        }
        
        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.json') as tmp:
            json.dump(invalid_payload, tmp)
            tmp_path = tmp.name
            
        try:
            result = self.run_evaluator(tmp_path)
            self.assertEqual(result["provenance_status"], "invalid_structure")
            self.assertIn("Schema validation failed", result["reasons"][0])
        finally:
            os.unlink(tmp_path)

if __name__ == '__main__':
    unittest.main()
