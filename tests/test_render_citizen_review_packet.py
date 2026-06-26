import unittest
import os
import subprocess
import tempfile

class TestRenderCitizenReviewPacket(unittest.TestCase):
    def setUp(self):
        self.script = os.path.join("scripts", "render_citizen_review_packet.py")
        self.examples_dir = "examples"

    def run_renderer(self, filename, output_arg=None):
        filepath = os.path.join(self.examples_dir, filename)
        cmd = ["python", self.script, filepath]
        if output_arg:
            cmd.extend(["--output", output_arg])
            
        result = subprocess.run(cmd, capture_output=True, text=True)
        self.assertEqual(result.returncode, 0)
        return result.stdout

    def test_valid_algae_report_render(self):
        stdout = self.run_renderer("citizen_observation_valid_algae_report.json")
        self.assertIn("vcs-obs-001", stdout)
        self.assertIn("complete_metadata", stdout)
        self.assertIn("This prototype does not determine environmental truth", stdout)
        self.assertIn("It does not verify environmental truth", stdout)

    def test_missing_location_render(self):
        stdout = self.run_renderer("citizen_observation_missing_location.json")
        self.assertIn("incomplete_metadata", stdout)
        self.assertIn("Recommended Human Review Questions", stdout)

    def test_sensitive_location_render(self):
        stdout = self.run_renderer("citizen_observation_sensitive_location.json")
        self.assertIn("private_location_review", stdout)
        self.assertIn("Ensure private or sensitive locations are protected", stdout)

    def test_ambiguous_evidence_render(self):
        stdout = self.run_renderer("citizen_observation_ambiguous_evidence.json")
        self.assertIn("ambiguous_evidence_review", stdout)
        self.assertIn("Evidence has not been verified or fact-checked", stdout)

    def test_file_output_mode(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            out_file = os.path.join(tmpdir, "test_packet.md")
            stdout = self.run_renderer("citizen_observation_valid_algae_report.json", output_arg=out_file)
            
            self.assertTrue(os.path.exists(out_file))
            with open(out_file, "r") as f:
                content = f.read()
                
            self.assertIn("complete_metadata", content)
            self.assertIn("Packet successfully written", stdout)

if __name__ == '__main__':
    unittest.main()
