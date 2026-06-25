import unittest
import subprocess
import os
import tempfile
import json

class TestValidateStationRegistry(unittest.TestCase):
    def setUp(self):
        self.script = os.path.join("scripts", "validate_station_registry.py")

    def run_script(self, filepath):
        return subprocess.run(["python", self.script, filepath], capture_output=True, text=True)

    def test_valid_registry(self):
        result = self.run_script(os.path.join("registries", "known_stations.json"))
        self.assertEqual(result.returncode, 0)
        self.assertIn("PASS", result.stdout)

    def test_duplicate_station_ids(self):
        bad_registry = [
            {
                "station_id": "duplicate-001",
                "station_name": "Test 1",
                "status": "demo",
                "latitude": 39.0,
                "longitude": -122.0,
                "location_description": "Test",
                "waterbody": "Clear Lake",
                "county": "Lake County",
                "state": "CA",
                "operator": "Test",
                "deployment_type": "simulated",
                "allowed_parameters": ["pH"],
                "notes": "test"
            },
            {
                "station_id": "duplicate-001",
                "station_name": "Test 2",
                "status": "demo",
                "latitude": 39.0,
                "longitude": -122.0,
                "location_description": "Test",
                "waterbody": "Clear Lake",
                "county": "Lake County",
                "state": "CA",
                "operator": "Test",
                "deployment_type": "simulated",
                "allowed_parameters": ["pH"],
                "notes": "test"
            }
        ]
        
        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.json') as f:
            json.dump(bad_registry, f)
            temp_path = f.name
            
        try:
            result = self.run_script(temp_path)
            self.assertNotEqual(result.returncode, 0)
            self.assertIn("FAIL", result.stdout)
            self.assertIn("Duplicate station_id", result.stdout)
        finally:
            os.remove(temp_path)

    def test_missing_required_fields(self):
        bad_registry = [
            {
                "station_id": "missing-fields-001",
                "status": "demo",
                "latitude": 39.0,
                "longitude": -122.0
            }
        ]
        
        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.json') as f:
            json.dump(bad_registry, f)
            temp_path = f.name
            
        try:
            result = self.run_script(temp_path)
            self.assertNotEqual(result.returncode, 0)
            self.assertIn("FAIL", result.stdout)
        finally:
            os.remove(temp_path)

if __name__ == '__main__':
    unittest.main()
