import unittest
import subprocess
import os

class TestQAQCObservation(unittest.TestCase):
    def setUp(self):
        self.script = os.path.join("scripts", "qaqc_observation.py")
        self.examples_dir = "examples"

    def run_script(self, filename):
        filepath = os.path.join(self.examples_dir, filename)
        return subprocess.run(["python", self.script, filepath], capture_output=True, text=True)

    def test_valid_qaqc(self):
        result = self.run_script("sample_observation_valid.json")
        self.assertEqual(result.returncode, 0)
        self.assertIn("PASS", result.stdout)

    def test_quarantined_turbidity(self):
        result = self.run_script("sample_observation_quarantined.json")
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("FAIL", result.stdout)

    def test_bad_ph(self):
        result = self.run_script("sample_observation_bad_ph.json")
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("FAIL", result.stdout)

    def test_unknown_parameter(self):
        result = self.run_script("sample_observation_unknown_parameter.json")
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("REVIEW", result.stdout)

    def test_unknown_station(self):
        result = self.run_script("sample_observation_unknown_station.json")
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("REVIEW", result.stdout)

    def test_station_parameter_mismatch(self):
        result = self.run_script("sample_observation_station_parameter_mismatch.json")
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("REVIEW", result.stdout)

if __name__ == '__main__':
    unittest.main()
