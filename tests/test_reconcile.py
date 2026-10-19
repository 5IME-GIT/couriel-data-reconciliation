import unittest
import tempfile
from pathlib import Path

from reconcile import reconcile

BASE_DIR = Path(__file__).resolve().parents[1]
SOURCE_A = BASE_DIR / "samples" / "source_a.csv"
SOURCE_B = BASE_DIR / "samples" / "source_b.csv"


class TestReconcile(unittest.TestCase):

    def test_detects_missing_and_conflicting_records(self):
        result = reconcile(SOURCE_A, SOURCE_B, key="customer_id")

        self.assertEqual(result["matching_count"], 1)
        self.assertEqual(result["missing_from_b"], ["103"])
        self.assertEqual(result["missing_from_a"], ["104"])
        self.assertEqual(result["conflicting_ids"], ["102"])
        self.assertEqual(
            result["conflicts"],
            [{
                "id": "102",
                "fields": ["email"],
                "source_a": {"email": "sam@example.com"},
                "source_b": {"email": "sam.new@example.com"},
            }]
        )

    def test_duplicate_ids_raise_error(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            path = Path(temp_dir) / "duplicates.csv"
            path.write_text(
                "customer_id,email\n"
                "102,first@example.com\n"
                "102,second@example.com\n",
                encoding="utf-8",
            )

            with self.assertRaisesRegex(ValueError, "Duplicate ID"):
                reconcile(path, SOURCE_B, key="customer_id")

    def test_missing_key_column_raises_error(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            path = Path(temp_dir) / "wrong_schema.csv"
            path.write_text(
                "email\nalex@example.com\n",
                encoding="utf-8",
            )

            with self.assertRaisesRegex(ValueError, "Required column"):
                reconcile(path, SOURCE_B, key="customer_id")

    def test_different_columns_raise_error(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            path = Path(temp_dir) / "different_schema.csv"
            path.write_text(
                "customer_id,phone\n"
                "101,123456789\n",
                encoding="utf-8",
            )

            with self.assertRaisesRegex(ValueError, "columns"):
                reconcile(SOURCE_A, path, key="customer_id")

    def test_header_only_csv_is_valid(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            empty_path = Path(temp_dir) / "empty_records.csv"
            empty_path.write_text(
                "customer_id,email\n",
                encoding="utf-8",
            )

            result = reconcile(empty_path, empty_path, key="customer_id")

            self.assertEqual(result["matching_count"], 0)
            self.assertEqual(result["missing_from_b"], [])
            self.assertEqual(result["missing_from_a"], [])
            self.assertEqual(result["conflicting_ids"], [])

    def test_completely_empty_csv_raises_error(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            empty_path = Path(temp_dir) / "blank.csv"
            empty_path.write_text("", encoding="utf-8")

            with self.assertRaisesRegex(ValueError, "header"):
                reconcile(empty_path, SOURCE_B, key="customer_id")


if __name__ == "__main__":
    unittest.main()
