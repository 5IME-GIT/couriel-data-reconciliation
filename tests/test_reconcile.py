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

    def test_header_only_csvs_with_different_columns_raise_error(self):
            with tempfile.TemporaryDirectory() as temp_dir:
                source_a = Path(temp_dir) / "source_a.csv"
                source_b = Path(temp_dir) / "source_b.csv"

                source_a.write_text(
                    "customer_id,email\n",
                    encoding="utf-8",
                )
                source_b.write_text(
                    "customer_id,phone\n",
                    encoding="utf-8",
                )

                with self.assertRaisesRegex(ValueError, "columns"):
                    reconcile(source_a, source_b, key="customer_id")


    def test_duplicate_column_names_raise_error(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            path = Path(temp_dir) / "duplicate_columns.csv"
            path.write_text(
                "customer_id,email,email\n"
                "101,alex@example.com,other@example.com\n",
                encoding="utf-8",
            )

            with self.assertRaisesRegex(ValueError, "duplicate column names"):
                reconcile(path, SOURCE_B, key="customer_id")

    def test_blank_column_name_raises_error(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            path = Path(temp_dir) / "blank_column.csv"
            path.write_text(
                "customer_id,,email\n"
                "101,123,alex@example.com\n",
                encoding="utf-8",
            )

            with self.assertRaisesRegex(ValueError, "blank column name"):
                reconcile(path, SOURCE_B, key="customer_id")


    def test_missing_fields_in_csv_row_raise_error(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            path = Path(temp_dir) / "missing_fields.csv"
            path.write_text(
                "customer_id,email\n"
                "101\n",
                encoding="utf-8",
            )

            with self.assertRaisesRegex(ValueError, "field count"):
                reconcile(path, SOURCE_B, key="customer_id")

    def test_extra_fields_in_csv_row_raise_error(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            path = Path(temp_dir) / "extra_fields.csv"
            path.write_text(
                "customer_id,email\n"
                "101,alex@example.com,unexpected\n",
                encoding="utf-8",
            )

            with self.assertRaisesRegex(ValueError, "field count"):
                reconcile(path, SOURCE_B, key="customer_id")


    def test_missing_fields_error_includes_file_and_row_number(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            path = Path(temp_dir) / "missing_fields.csv"
            path.write_text(
                "customer_id,email\n"
                "101\n",
                encoding="utf-8",
            )

            with self.assertRaisesRegex(
                ValueError, r"missing_fields\.csv.*row 2"
            ):
                reconcile(path, SOURCE_B, key="customer_id")

    def test_empty_key_error_includes_row_number(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            path = Path(temp_dir) / "empty_key.csv"
            path.write_text(
                "customer_id,email\n"
                ",alex@example.com\n",
                encoding="utf-8",
            )

            with self.assertRaisesRegex(
                ValueError, r"empty_key\.csv.*row 2"
            ):
                reconcile(path, SOURCE_B, key="customer_id")

    def test_duplicate_id_error_includes_row_number(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            path = Path(temp_dir) / "duplicates.csv"
            path.write_text(
                "customer_id,email\n"
                "102,first@example.com\n"
                "102,second@example.com\n",
                encoding="utf-8",
            )

            with self.assertRaisesRegex(
                ValueError, r"duplicates\.csv.*row 3"
            ):
                reconcile(path, SOURCE_B, key="customer_id")


if __name__ == "__main__":
    unittest.main()
