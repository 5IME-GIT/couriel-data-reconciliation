# CSV Data Reconciliation Tool

A lightweight, cross-platform Python command-line tool for comparing two CSV datasets, identifying missing records and conflicting values, validating input data, and generating a reconciliation report.

## Problem Statement

When two systems maintain related records, their datasets can become inconsistent. Records may be missing from one system, contain different field values, or violate expected data-quality rules.

This tool compares two datasets without modifying the original files and produces a report that helps users investigate discrepancies.

## Features

- Compare two CSV files using a configurable record key.
- Identify records missing from either dataset.
- Detect conflicting field values for matching identifiers.
- Validate CSV headers and compatible schemas.
- Reject blank or duplicate column names.
- Detect empty and duplicate record identifiers.
- Reject rows containing too few or too many fields.
- Include file paths and row numbers in relevant validation errors.
- Support header-only CSV files while rejecting files without headers.
- Generate a readable text reconciliation report.
- Include automated regression tests using Python's standard library.

## Requirements

- Python 3.10 or later.
- No third-party Python packages required.

The project uses Python's standard library and is designed to run on Linux, Windows, and macOS.

## Project Structure

```text
couriel-data-reconciliation/
 main.py
 reconcile.py
 report.py
 README.md
 samples/
   ├── source_a.csv
   └── source_b.csv
 reports/
   └── reconciliation_report.txt
 tests/
    ├── test_reconcile.py
    └── test_report.py
```

## Quick Start

Clone the repository:

```bash
git clone https://github.com/5IME-GIT/couriel-data-reconciliation.git
cd couriel-data-reconciliation
```

Run the sample reconciliation:

```bash
python main.py
```

On Linux systems where Python 3 is invoked as `python3`, use:

```bash
python3 main.py
```

By default, the tool compares the sample datasets using `customer_id` as the record key and writes the report to:

`reports/reconciliation_report.txt`

## Command-Line Options

The command-line interface supports the following options:

| Option | Default | Purpose |
|---|---|---|
| `--source-a` | `samples/source_a.csv` | First input CSV |
| `--source-b` | `samples/source_b.csv` | Second input CSV |
| `--key` | `customer_id` | Column used to identify records |
| `--output` | `reports/reconciliation_report.txt` | Destination for the report |

Example using custom input files:

```bash
python main.py \
  --source-a data/system_a.csv \
  --source-b data/system_b.csv \
  --key customer_id \
  --output reports/custom_report.txt
```

Use `python3` instead of `python` if that is how Python is invoked on your system.

## Example Results

The included sample datasets demonstrate these reconciliation outcomes:

| Result | Count |
|---|---:|
| Matching records | 1 |
| Records missing from source B | 1 |
| Records missing from source A | 1 |
| Records with conflicting values | 1 |

Customer ID `102` has a conflicting email address between the two datasets. Customer ID `103` appears only in source A, while customer ID `104` appears only in source B.

## Data Validation and Error Handling

The tool validates input data before completing reconciliation. Checks include:

- Missing CSV headers and required key columns.
- Blank or duplicate column names.
- Incompatible schemas between input files.
- Missing or extra fields in individual rows.
- Empty record identifiers.
- Duplicate record identifiers.

Relevant row-level errors include the input file path and row number to help users locate invalid data.

For example:

```text
CSV row has incorrect field count in source_a.csv at row 2
```

The reported row number includes the header as row 1. For CSV records spanning multiple physical lines, the reported line number follows the CSV reader's physical-line count.

## Run the Tests

From the project root, run:

```bash
python -m unittest discover -s tests -v
```

Or, where appropriate:

```bash
python3 -m unittest discover -s tests -v
```

The automated tests cover reconciliation results, missing and conflicting records, invalid schemas, duplicate identifiers, malformed rows, row-number-aware errors, and report generation.

## Design Principles

- Preserve source files: reconciliation does not silently overwrite the input datasets.
- Fail clearly: invalid input is rejected with actionable error messages.
- Prefer portability: standard-library functionality avoids unnecessary dependencies.
- Verify behavior: automated tests protect existing functionality as validation improves.

## Current Limitations

- Records are identified using one key column.
- Input data is processed locally from CSV files.
- The current report format is plain text.
- Large-scale performance has not yet been benchmarked.

Potential future improvements include structured JSON reports, configurable comparison rules, performance benchmarking, and support for more complex reconciliation workflows.

## Technical Skills Demonstrated

- Python programming and modular design.
- CSV parsing and file handling.
- Data reconciliation and set operations.
- Input validation and exception handling.
- Command-line interface development.
- Automated unit testing and regression prevention.
- Technical documentation and Git-based version control.

## Author

**COURIEL DUREL**

GitHub: [5IME-GIT](https://github.com/5IME-GIT)
