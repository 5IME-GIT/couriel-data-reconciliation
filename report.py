from pathlib import Path


def write_report(result, output_path):
    """Write reconciliation results to a readable text report."""
    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    lines = [
        "DATA RECONCILIATION REPORT",
        "=" * 30,
        "",
        f"Matching records: {result['matching_count']}",
        f"Records missing from source B: {len(result['missing_from_b'])}",
        f"Records missing from source A: {len(result['missing_from_a'])}",
        f"Records with conflicting values: {len(result['conflicting_ids'])}",
        "",
        "RECORDS MISSING FROM SOURCE B",
        "-" * 30,
    ]

    lines.extend(result["missing_from_b"] or ["None"])

    lines.extend([
        "",
        "RECORDS MISSING FROM SOURCE A",
        "-" * 30,
    ])

    lines.extend(result["missing_from_a"] or ["None"])

    lines.extend([
        "",
        "CONFLICTING RECORDS",
        "-" * 30,
    ])

    if result["conflicts"]:
        for conflict in result["conflicts"]:
            lines.append(f"Record ID: {conflict['id']}")

            for field in conflict["fields"]:
                lines.append(f"  Field: {field}")
                lines.append(
                    f"  Source A: {conflict['source_a'][field]}"
                )
                lines.append(
                    f"  Source B: {conflict['source_b'][field]}"
                )

            lines.append("")
    else:
        lines.append("None")

    output_path.write_text(
        "\n".join(lines) + "\n",
        encoding="utf-8",
    )

    return output_path
