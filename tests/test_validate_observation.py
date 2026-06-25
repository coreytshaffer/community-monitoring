import unittest
import subprocess
import os

class TestValidateObservation(unittest.TestCase):
    def setUp(self):
        self.script = os.path.join("scripts", "validate_observation.py")
        self.examples_dir = "examples"

    def run_script(self, filename):
        filepath = os.path.join(self.examples_dir, filename)
        return subprocess.run(["python", self.script, filepath], capture_output=True, text=True)

    def test_valid_schema(self):
        result = self.run_script("sample_observation_valid.json")
        self.assertEqual(result.returncode, 0)
        self.assertIn("PASS", result.stdout)

    def test_quarantined_schema(self):
        result = self.run_script("sample_observation_quarantined.json")
        self.assertEqual(result.returncode, 0)
        self.assertIn("PASS", result.stdout)

    def test_unknown_station_schema(self):
        result = self.run_script("sample_observation_unknown_station.json")
        self.assertEqual(result.returncode, 0)
        self.assertIn("PASS", result.stdout)

    def test_parameter_mismatch_schema(self):
        result = self.run_script("sample_observation_station_parameter_mismatch.json")
        self.assertEqual(result.returncode, 0)
        self.assertIn("PASS", result.stdout)

    def test_invalid_schema(self):
        result = self.run_script("sample_observation_invalid_schema.json")
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("FAIL", result.stdout)
        self.assertIn("not-a-number", result.stdout)

if __name__ == '__main__':
    unittest.main()
