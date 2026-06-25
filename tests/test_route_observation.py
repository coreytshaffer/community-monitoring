import unittest
import subprocess
import os
import shutil
import tempfile

class TestRouteObservation(unittest.TestCase):
    def setUp(self):
        self.script = os.path.join("scripts", "route_observation.py")
        self.examples_dir = "examples"

    def run_script(self, filename):
        filepath = os.path.join(self.examples_dir, filename)
        return subprocess.run(["python", self.script, filepath], capture_output=True, text=True)

    def test_route_valid(self):
        result = self.run_script("sample_observation_valid.json")
        self.assertEqual(result.returncode, 0)
        self.assertIn("ACCEPTED-INTERNAL", result.stdout)
        self.assertIn("accepted-internal", result.stdout)

    def test_route_quarantine(self):
        result = self.run_script("sample_observation_quarantined.json")
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("QUARANTINE", result.stdout)
        self.assertIn("quarantine", result.stdout)

    def test_route_bad_ph(self):
        result = self.run_script("sample_observation_bad_ph.json")
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("QUARANTINE", result.stdout)
        self.assertIn("quarantine", result.stdout)

    def test_route_unknown_parameter(self):
        result = self.run_script("sample_observation_unknown_parameter.json")
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("REVIEW", result.stdout)
        self.assertIn("review-queue", result.stdout)

    def test_route_unknown_station(self):
        result = self.run_script("sample_observation_unknown_station.json")
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("REVIEW", result.stdout)
        self.assertIn("review-queue", result.stdout)

    def test_route_parameter_mismatch(self):
        result = self.run_script("sample_observation_station_parameter_mismatch.json")
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("REVIEW", result.stdout)
        self.assertIn("review-queue", result.stdout)

    def test_route_invalid_schema(self):
        result = self.run_script("sample_observation_invalid_schema.json")
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("DEAD-LETTER", result.stdout)
        self.assertIn("dead-letter", result.stdout)

    def test_write_mode(self):
        with tempfile.TemporaryDirectory() as tempdir:
            filepath = os.path.join(self.examples_dir, "sample_observation_valid.json")
            result = subprocess.run([
                "python", self.script, "--write", "--output-dir", tempdir, filepath
            ], capture_output=True, text=True)
            self.assertEqual(result.returncode, 0)
            
            # Check if file exists in accepted-internal
            dest_file = os.path.join(tempdir, "accepted-internal", "sample_observation_valid.json")
            self.assertTrue(os.path.exists(dest_file))
            
            # Confirm original still exists
            self.assertTrue(os.path.exists(filepath))

if __name__ == '__main__':
    unittest.main()
