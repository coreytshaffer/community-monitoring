import unittest
import os
import subprocess
import tempfile
import json

class TestWriteCitizenTrustLedger(unittest.TestCase):
    def setUp(self):
        self.script = os.path.join("scripts", "write_citizen_trust_ledger.py")
        self.examples_dir = "examples"

    def run_writer(self, filenames, output_path):
        filepaths = [os.path.join(self.examples_dir, f) for f in filenames]
        cmd = ["python", self.script] + filepaths + ["--output", output_path]
            
        result = subprocess.run(cmd, capture_output=True, text=True)
        self.assertEqual(result.returncode, 0)
        return result.stdout

    def test_single_valid_algae_report(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            out_file = os.path.join(tmpdir, "ledger.jsonl")
            self.run_writer(["citizen_observation_valid_algae_report.json"], out_file)
            
            self.assertTrue(os.path.exists(out_file))
            with open(out_file, "r") as f:
                lines = f.readlines()
            
            self.assertEqual(len(lines), 1)
            record = json.loads(lines[0])
            self.assertEqual(record["observation_id"], "vcs-obs-001")
            self.assertEqual(record["provenance_status"], "complete_metadata")
            self.assertIn("payload_hash", record)

    def test_multiple_fixtures(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            out_file = os.path.join(tmpdir, "ledger.jsonl")
            self.run_writer([
                "citizen_observation_valid_algae_report.json",
                "citizen_observation_missing_location.json"
            ], out_file)
            
            with open(out_file, "r") as f:
                lines = f.readlines()
            
            self.assertEqual(len(lines), 2)
            
            statuses = [json.loads(line)["provenance_status"] for line in lines]
            self.assertIn("complete_metadata", statuses)
            self.assertIn("incomplete_metadata", statuses)

    def test_missing_location(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            out_file = os.path.join(tmpdir, "ledger.jsonl")
            self.run_writer(["citizen_observation_missing_location.json"], out_file)
            with open(out_file, "r") as f:
                record = json.loads(f.readline())
            self.assertEqual(record["provenance_status"], "incomplete_metadata")

    def test_sensitive_location(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            out_file = os.path.join(tmpdir, "ledger.jsonl")
            self.run_writer(["citizen_observation_sensitive_location.json"], out_file)
            with open(out_file, "r") as f:
                record = json.loads(f.readline())
            self.assertEqual(record["provenance_status"], "private_location_review")

    def test_ambiguous_evidence(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            out_file = os.path.join(tmpdir, "ledger.jsonl")
            self.run_writer(["citizen_observation_ambiguous_evidence.json"], out_file)
            with open(out_file, "r") as f:
                record = json.loads(f.readline())
            self.assertEqual(record["provenance_status"], "ambiguous_evidence_review")

if __name__ == '__main__':
    unittest.main()
