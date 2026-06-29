import copy
import os
import subprocess
import sys
import unittest

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SCRIPTS_DIR = os.path.join(REPO_ROOT, "scripts")

if SCRIPTS_DIR not in sys.path:
    sys.path.insert(0, SCRIPTS_DIR)

from qaqc_observation import load_station_registry, qaqc_check


class TestQAQCObservation(unittest.TestCase):
    def setUp(self):
        self.script = os.path.join(SCRIPTS_DIR, "qaqc_observation.py")
        self.examples_dir = os.path.join(REPO_ROOT, "examples")
        self.registry = load_station_registry(os.path.join(REPO_ROOT, "registries", "known_stations.json"))
        self.valid_observation = {
            "observation_id": "simulated-valid-001",
            "sensor_id": "do_sensor_01",
            "station_id": "demo-clearlake-shore-001",
            "observed_at": "2026-06-25T07:00:00Z",
            "received_at": "2026-06-25T07:05:00Z",
            "parameter": "dissolved_oxygen",
            "value": 8.2,
            "unit": "mg/L",
            "latitude": 39.0435,
            "longitude": -122.8821,
            "source": "lorawan_gateway_main",
            "quality_flag": "valid",
            "review_status": "auto_checked",
            "notes": "Simulated example data for a healthy dissolved oxygen reading in Clear Lake. Not real field data.",
        }

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

    def test_dissolved_oxygen_below_zero_fails(self):
        observation = copy.deepcopy(self.valid_observation)
        observation["value"] = -0.1

        status, reason = qaqc_check(observation, self.registry)

        self.assertEqual(status, "FAIL")
        self.assertIn("cannot be less than 0.0", reason)

    def test_dissolved_oxygen_above_twenty_reviews(self):
        observation = copy.deepcopy(self.valid_observation)
        observation["value"] = 20.1

        status, reason = qaqc_check(observation, self.registry)

        self.assertEqual(status, "REVIEW")
        self.assertIn("above 20.0 mg/L", reason)

    def test_invalid_coordinates_fail(self):
        observation = copy.deepcopy(self.valid_observation)
        observation["latitude"] = 95.0

        status, reason = qaqc_check(observation, self.registry)

        self.assertEqual(status, "FAIL")
        self.assertIn("Earth bounds", reason)

    def test_missing_observed_at_reviews(self):
        observation = copy.deepcopy(self.valid_observation)
        observation["observed_at"] = None

        status, reason = qaqc_check(observation, self.registry)

        self.assertEqual(status, "REVIEW")
        self.assertIn("Timestamp review required", reason)

    def test_unparseable_received_at_reviews(self):
        observation = copy.deepcopy(self.valid_observation)
        observation["received_at"] = "not-a-timestamp"

        status, reason = qaqc_check(observation, self.registry)

        self.assertEqual(status, "REVIEW")
        self.assertIn("Timestamp review required", reason)

    def test_received_before_observed_fails(self):
        observation = copy.deepcopy(self.valid_observation)
        observation["received_at"] = "2026-06-25T06:59:00Z"

        status, reason = qaqc_check(observation, self.registry)

        self.assertEqual(status, "FAIL")
        self.assertIn("received_at cannot be earlier", reason)


if __name__ == '__main__':
    unittest.main()
