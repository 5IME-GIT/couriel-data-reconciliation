from pathlib import Path

from reconcile import reconcile
from report import write_report


BASE_DIR = Path(__file__).resolve().parent

SOURCE_A = BASE_DIR / "samples" / "source_a.csv"
SOURCE_B = BASE_DIR / "samples" / "source_b.csv"
REPORT_PATH = BASE_DIR / "reports" / "reconciliation_report.txt"


def main():
    try:
        result = reconcile(
            SOURCE_A,
            SOURCE_B,
            key="customer_id",
        )

        write_report(result, REPORT_PATH)

        print("Reconciliation completed successfully.")
        print(f"Matching records: {result['matching_count']}")
        print(f"Missing from source B: {len(result['missing_from_b'])}")
        print(f"Missing from source A: {len(result['missing_from_a'])}")
        print(f"Conflicting records: {len(result['conflicting_ids'])}")
        print(f"Report saved to: {REPORT_PATH}")

    except (OSError, ValueError) as error:
        print(f"Reconciliation failed: {error}")


if __name__ == "__main__":
    main()
