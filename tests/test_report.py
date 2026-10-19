import tempfile
import unittest
from pathlib import Path

from reconcile import reconcile
from report import write_report


BASE_DIR = Path(__file__).resolve().parents[1]
SOURCE_A = BASE_DIR / "samples" / "source_a.csv"
SOURCE_B = BASE_DIR / "samples" / "source_b.csv"


class TestReport(unittest.TestCase):

    def test_report_contains_reconciliation_results(self):
        result = reconcile(SOURCE_A, SOURCE_B, key="customer_id")

        with tempfile.TemporaryDirectory() as temp_dir:
            output_path = Path(temp_dir) / "report.txt"
            write_report(result, output_path)

            report_text = output_path.read_text(encoding="utf-8")

            self.assertIn("DATA RECONCILIATION REPORT", report_text)
            self.assertIn("Matching records: 1", report_text)
            self.assertIn("Records missing from source B: 1", report_text)
            self.assertIn("Records missing from source A: 1", report_text)
            self.assertIn("Records with conflicting values: 1", report_text)
            self.assertIn("sam@example.com", report_text)
            self.assertIn("sam.new@example.com", report_text)
            self.assertTrue(output_path.exists())


if __name__ == "__main__":
    unittest.main()
