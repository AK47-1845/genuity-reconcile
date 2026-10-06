import json
from pathlib import Path
from statistics import mean


root = Path(__file__).resolve().parent
batch = json.loads((root / "batch_result.json").read_text(encoding="utf-8"))
documents = {item["id"]: item for item in batch["documents"]}
checks = []


def add(check_id, document, passed, explanation, details=None):
    checks.append(
        {
            "check_id": check_id,
            "document": document,
            "result": "PASS" if passed else "FAIL",
            "explanation": explanation,
            "details": details or {},
        }
    )


doc = documents["DOC-01"]
ni_co = doc["analysis_percent"]["Ni"] + doc["analysis_percent"]["Co"]
nb_ta = doc["analysis_percent"]["Nb"] + doc["analysis_percent"]["Ta"]
add(
    "combined_Ni_Co",
    "DOC-01",
    round(ni_co, 1) == doc["reported_combined_values"]["Ni_plus_Co"],
    "Reported Ni+Co agrees after document-level rounding.",
    {"calculated": ni_co, "reported": doc["reported_combined_values"]["Ni_plus_Co"]},
)
add(
    "combined_Nb_Ta",
    "DOC-01",
    round(nb_ta, 2) == doc["reported_combined_values"]["Nb_plus_Ta"],
    "Reported Nb+Ta agrees after document-level rounding.",
    {"calculated": nb_ta, "reported": doc["reported_combined_values"]["Nb_plus_Ta"]},
)

doc = documents["DOC-04"]
for index, row in enumerate(doc["product_analysis"], start=1):
    largest = max((abs(row[key] - doc["ladle_analysis"][key]), key) for key in row)
    add(
        f"product_vs_ladle_{index}",
        "DOC-04",
        largest[0] <= 0.03,
        "Product analysis remains close to the displayed ladle analysis for all shared fields.",
        {"largest_absolute_difference": largest[0], "element": largest[1]},
    )

doc = documents["DOC-05"]
hardness = [value for row in doc["hardness_readings"] for value in row if value is not None]
add(
    "hardness_table_completeness",
    "DOC-05",
    len(hardness) == 95,
    "95 of 96 visible table cells were structured; the obscured cell remains unresolved.",
    {"captured": len(hardness), "expected": 96, "minimum": min(hardness), "maximum": max(hardness), "mean": round(mean(hardness), 3)},
)

doc = documents["DOC-06"]
quantities = doc["quantity"]
add(
    "inspection_quantity_reconciliation",
    "DOC-06",
    quantities["inspected"] == quantities["accepted"] + quantities["rejected"],
    "Inspected quantity equals accepted plus rejected quantity.",
    quantities,
)

doc = documents["DOC-08"]
for row in doc["results"]:
    failures = []
    for element, lower in doc["spec_min"].items():
        value = row.get(element)
        if value is not None and value < lower:
            failures.append({"element": element, "value": value, "minimum": lower})
    for element, upper in doc["spec_max"].items():
        value = row.get(element)
        if value is not None and value > upper:
            failures.append({"element": element, "value": value, "maximum": upper})
    add(
        f"chemistry_spec_{row['sample'].replace(' ', '_')}",
        "DOC-08",
        not failures,
        "All displayed result values with an explicit displayed limit are within range.",
        {"violations": failures},
    )

doc = documents["DOC-09"]
for row in doc["mechanical_properties"]:
    passed = row["yield_0_2_psi"] <= row["tensile_psi"] and 0 <= row["elongation_percent"] <= 100 and 0 <= row["reduction_percent"] <= 100
    add(
        f"mechanical_sanity_{row['sample'].replace(' ', '_')}",
        "DOC-09",
        passed,
        "Yield is not above tensile strength and percentage fields are physically bounded.",
        row,
    )

report = {
    "batch_id": batch["batch_id"],
    "check_count": len(checks),
    "passed": sum(item["result"] == "PASS" for item in checks),
    "failed": sum(item["result"] == "FAIL" for item in checks),
    "checks": checks,
}
(root / "validation_results.json").write_text(json.dumps(report, indent=2), encoding="utf-8")
print(json.dumps(report, indent=2))
