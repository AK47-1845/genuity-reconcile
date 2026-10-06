import csv
import json
from pathlib import Path


root = Path(__file__).resolve().parent
batch = json.loads((root / "batch_result.json").read_text(encoding="utf-8"))
documents = {item["id"]: item for item in batch["documents"]}


def write_csv(name, fieldnames, rows):
    with (root / name).open("w", newline="", encoding="utf-8-sig") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


chemistry_rows = []
doc = documents["DOC-01"]
for element, value in doc["analysis_percent"].items():
    chemistry_rows.append({"document_id": "DOC-01", "sample": "reported analysis", "element": element, "value": value, "unit": "percent", "status": "RECOVERED", "source": doc["source"]})

doc = documents["DOC-04"]
for element, value in doc["ladle_analysis"].items():
    chemistry_rows.append({"document_id": "DOC-04", "sample": "ladle", "element": element, "value": value, "unit": "ppm" if element == "H_ppm" else "percent", "status": "OBSERVED", "source": doc["source"]})
for index, result in enumerate(doc["product_analysis"], start=1):
    for element, value in result.items():
        chemistry_rows.append({"document_id": "DOC-04", "sample": f"product_{index}", "element": element, "value": value, "unit": "percent", "status": "OBSERVED", "source": doc["source"]})

doc = documents["DOC-08"]
for result in doc["results"]:
    for element, value in result.items():
        if element == "sample":
            continue
        chemistry_rows.append({"document_id": "DOC-08", "sample": result["sample"], "element": element, "value": "" if value is None else value, "unit": "percent", "status": "UNRESOLVED" if value is None else "OBSERVED", "source": doc["source"]})
write_csv("chemistry_records.csv", ["document_id", "sample", "element", "value", "unit", "status", "source"], chemistry_rows)


doc = documents["DOC-05"]
hardness_rows = []
for row_index, row in enumerate(doc["hardness_readings"], start=1):
    for column_index, value in enumerate(row, start=1):
        hardness_rows.append({"document_id": "DOC-05", "row": row_index, "column": column_index, "value": "" if value is None else value, "unit": "HRC", "status": "UNRESOLVED" if value is None else "RECOVERED", "source": doc["source"]})
write_csv("hardness_records.csv", ["document_id", "row", "column", "value", "unit", "status", "source"], hardness_rows)


doc = documents["DOC-09"]
mechanical_rows = []
for result in doc["mechanical_properties"]:
    mechanical_rows.append({"document_id": "DOC-09", **result, "source": doc["source"]})
write_csv("mechanical_properties.csv", ["document_id", "sample", "tensile_psi", "yield_0_2_psi", "yield_0_6_psi", "elongation_percent", "reduction_percent", "source"], mechanical_rows)


use_case_rows = []
for document_id in ("DOC-02", "DOC-03"):
    doc = documents[document_id]
    for index, item in enumerate(doc["items"], start=1):
        use_case_rows.append({"document_id": document_id, "item_number": index, "use_case": item, "source": doc["source"]})
write_csv("use_case_catalog.csv", ["document_id", "item_number", "use_case", "source"], use_case_rows)


exception_rows = [
    {"document_id": "DOC-05", "field": "hardness row 9 column 2", "status": "UNRESOLVED", "reason": "Obscured value; no supporting document supplied"},
    {"document_id": "DOC-08", "field": "W3535 01 boron", "status": "MISSING_WITH_CANDIDATE", "reason": "Blank result; same-heat ladle row reports 0.0002"},
    {"document_id": "DOC-08", "field": "W3535 27B boron", "status": "MISSING_WITH_CANDIDATE", "reason": "Blank result; same-heat ladle row reports 0.0002"},
    {"document_id": "DOC-06", "field": "part number", "status": "UNRESOLVED", "reason": "Multiple handwritten character candidates"},
    {"document_id": "DOC-06", "field": "dimension rows", "status": "REVIEW_REQUIRED", "reason": "Handwritten measurements need field confirmation"},
    {"document_id": "DOC-07", "field": "dense table rows", "status": "REVIEW_REQUIRED", "reason": "Schema recovered; row transcription not accepted without stronger evidence"},
]
write_csv("exceptions.csv", ["document_id", "field", "status", "reason"], exception_rows)

print({
    "chemistry_records": len(chemistry_rows),
    "hardness_records": len(hardness_rows),
    "mechanical_records": len(mechanical_rows),
    "use_cases": len(use_case_rows),
    "exceptions": len(exception_rows),
})
