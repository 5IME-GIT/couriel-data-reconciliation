import csv


def load_records(path, key):
    """Load CSV records and return their headers and indexed records."""
    records = {}

    with open(path, "r", newline="", encoding="utf-8-sig") as file:
        reader = csv.DictReader(file)

        if reader.fieldnames is None:
            raise ValueError(f"CSV file has no header: {path}")

        headers = reader.fieldnames

        if any(not column.strip() for column in headers):
            raise ValueError(f"CSV contains a blank column name: {path}")

        if len(headers) != len(set(headers)):
            raise ValueError(f"CSV contains duplicate column names: {path}")

        columns = set(headers)

        if key not in columns:
            raise ValueError(f"Required column not found: {key}")

        for row in reader:
            record_id = (row.get(key) or "").strip()

            if not record_id:
                raise ValueError(f"Empty value found in key column: {key}")

            if record_id in records:
                raise ValueError(f"Duplicate ID found: {record_id}")

            records[record_id] = {
                column: (value or "").strip()
                for column, value in row.items()
                if column is not None
            }

    return columns, records


def reconcile(source_a, source_b, key):
    """Compare two CSV datasets and report discrepancies."""
    columns_a, records_a = load_records(source_a, key)
    columns_b, records_b = load_records(source_b, key)

    if columns_a != columns_b:
        raise ValueError(
            f"CSV columns do not match. "
            f"Only in source A: {sorted(columns_a - columns_b)}; "
            f"only in source B: {sorted(columns_b - columns_a)}"
        )

    ids_a = set(records_a)
    ids_b = set(records_b)

    missing_from_b = sorted(ids_a - ids_b)
    missing_from_a = sorted(ids_b - ids_a)

    common_ids = ids_a & ids_b
    matching_ids = []
    conflicting_ids = []
    conflicts = []

    for record_id in sorted(common_ids):
        fields_a = records_a[record_id]
        fields_b = records_b[record_id]
        differing_fields = []

        for column in fields_a:
            if column == key:
                continue

            if fields_a[column] != fields_b[column]:
                differing_fields.append(column)

        if differing_fields:
            conflicting_ids.append(record_id)
            conflicts.append({
                "id": record_id,
                "fields": differing_fields,
                "source_a": {
                    field: fields_a[field] for field in differing_fields
                },
                "source_b": {
                    field: fields_b[field] for field in differing_fields
                },
            })
        else:
            matching_ids.append(record_id)

    return {
        "matching_count": len(matching_ids),
        "matching_ids": matching_ids,
        "missing_from_b": missing_from_b,
        "missing_from_a": missing_from_a,
        "conflicting_ids": conflicting_ids,
        "conflicts": conflicts,
    }
