import argparse
from pathlib import Path

from reconcile import reconcile
from report import write_report


BASE_DIR = Path(__file__).resolve().parent


def parse_arguments():
    parser = argparse.ArgumentParser(
        description="Compare two CSV files and generate a reconciliation report."
    )

    parser.add_argument(
        "--source-a",
        type=Path,
        default=BASE_DIR / "samples" / "source_a.csv",
        help="Path to the first CSV file.",
    )

    parser.add_argument(
        "--source-b",
        type=Path,
        default=BASE_DIR / "samples" / "source_b.csv",
        help="Path to the second CSV file.",
    )

    parser.add_argument(
        "--key",
        default="customer_id",
        help="Column used to identify matching records.",
    )

    parser.add_argument(
        "--output",
        type=Path,
        default=BASE_DIR / "reports" / "reconciliation_report.txt",
        help="Path where the report will be saved.",
    )

    return parser.parse_args()


def main():
    args = parse_arguments()

    try:
        result = reconcile(
            args.source_a,
            args.source_b,
            key=args.key,
        )

        args.output.parent.mkdir(parents=True, exist_ok=True)
        write_report(result, args.output)

        print("Reconciliation completed successfully.")
        print(f"Matching records: {result['matching_count']}")
        print(f"Missing from source B: {len(result['missing_from_b'])}")
        print(f"Missing from source A: {len(result['missing_from_a'])}")
        print(f"Conflicting records: {len(result['conflicting_ids'])}")
        print(f"Report saved to: {args.output}")

    except (OSError, ValueError) as error:
        print(f"Reconciliation failed: {error}")


if __name__ == "__main__":
    main()
