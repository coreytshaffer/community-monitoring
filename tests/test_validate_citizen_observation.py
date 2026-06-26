import unittest
import json
import os
from jsonschema import validate, ValidationError, FormatChecker

class TestValidateCitizenObservation(unittest.TestCase):
    def setUp(self):
        self.schema_path = os.path.join("schemas", "citizen_observation.schema.json")
        self.examples_dir = "examples"
        
        with open(self.schema_path, "r") as f:
            self.schema = json.load(f)
            
        self.format_checker = FormatChecker()

    def validate_fixture(self, filename):
        filepath = os.path.join(self.examples_dir, filename)
        with open(filepath, "r") as f:
            instance = json.load(f)
        
        try:
            validate(instance=instance, schema=self.schema, format_checker=self.format_checker)
            return True, instance
        except ValidationError as e:
            return False, e

    def test_valid_algae_report(self):
        is_valid, instance = self.validate_fixture("citizen_observation_valid_algae_report.json")
        self.assertTrue(is_valid, msg=f"Validation failed: {instance if not is_valid else ''}")
        self.assertEqual(instance.get("provenance_status"), "complete_metadata")
        self.assertEqual(instance.get("simulated"), True)

    def test_missing_location(self):
        is_valid, instance = self.validate_fixture("citizen_observation_missing_location.json")
        self.assertTrue(is_valid, msg=f"Validation failed: {instance if not is_valid else ''}")
        self.assertEqual(instance.get("provenance_status"), "incomplete_metadata")
        self.assertIsNone(instance.get("latitude"))
        self.assertIsNone(instance.get("longitude"))

    def test_sensitive_location(self):
        is_valid, instance = self.validate_fixture("citizen_observation_sensitive_location.json")
        self.assertTrue(is_valid, msg=f"Validation failed: {instance if not is_valid else ''}")
        self.assertEqual(instance.get("provenance_status"), "private_location_review")
        self.assertIn(instance.get("location_privacy"), ["private_property", "sensitive_habitat"])

    def test_ambiguous_evidence(self):
        is_valid, instance = self.validate_fixture("citizen_observation_ambiguous_evidence.json")
        self.assertTrue(is_valid, msg=f"Validation failed: {instance if not is_valid else ''}")
        self.assertEqual(instance.get("provenance_status"), "ambiguous_evidence_review")

if __name__ == '__main__':
    unittest.main()
