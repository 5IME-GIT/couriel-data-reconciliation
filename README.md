# CSV Data Reconciliation Tool

A Python tool for comparing two CSV datasets, identifying missing records,
detecting conflicting field values, validating input schemas, and generating
a readable reconciliation report.

## Problem Statement

When two systems store related customer data, their records may become
inconsistent. This tool helps identify records that are missing, mismatched,
or conflicting between two datasets without silently overwriting the source data.

## Features

- Compare two CSV files using a unique record identifier.
- Identify records missing from either dataset.
- Detect conflicting field values for matching identifiers.
- Reject duplicate identifiers and empty identifier values.
- Validate required columns and compatible CSV schemas.
- Handle header-only CSV files and reject files without headers.
- Generate a readable text report.
- Run automated tests using Python's unittest framework.

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

## Requirements

- Python 3.10 or later
- No third-party Python packages required

## Usage

Run the reconciliation workflow:

```bash
python3 main.py
```

The program compares the sample datasets and writes the report to:

`reports/reconciliation_report.txt`

## Example Results

Using the included sample data:

- Matching records: 1
- Records missing from source B: 1
- Records missing from source A: 1
- Records with conflicting values: 1

The sample conflict concerns customer ID `102`, whose email address differs
between the two datasets.

## Run the Tests

From the project root, execute:

```bash
python3 -m unittest discover -s tests -v
```

The test suite checks reconciliation results, duplicate identifiers, missing
key columns, incompatible schemas, empty CSV files, and report generation.

## Technical Skills Demonstrated

- Python programming
- CSV processing
- Data validation and quality checks
- Set operations and record reconciliation
- Exception handling
- Automated unit testing
- File handling and report generation
- Command-line workflow development

## Limitations

This version processes CSV files locally and uses a single key column to
identify records. It is a prototype intended for small-to-medium datasets;
large-scale processing, configurable input paths, and additional output formats
could be added in future versions.

## Author

COURIEL DUREL
