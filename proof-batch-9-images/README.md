# Genuity local proof: nine-image engineering batch

This package is the concrete output of processing the nine supplied WhatsApp images locally.

## Result

- 9/9 inputs inventoried and classified.
- 41 service-company use cases recovered into a catalog.
- Three different chemistry formats converted to one long-form chemistry table.
- 95 of 96 visible hardness cells structured; the obscured cell is explicitly unresolved.
- Two mechanical-property samples, two heat-treatment steps and one Charpy test set structured.
- A handwritten inspection form was classified and its quantity accounting was reconciled.
- 11 deterministic checks passed.
- Candidate document links were recorded but not merged without a common identifier.
- Three missing-data candidates were produced with explicit usage restrictions.

## Database-ready outputs

- `chemistry_records.csv`
- `hardness_records.csv`
- `mechanical_properties.csv`
- `use_case_catalog.csv`
- `exceptions.csv`

The evidence-linked canonical result is in `batch_result.json`; rule outcomes are in `validation_results.json`.

## Important demonstration

The raw local OCR read `INCONEL alloy 72S`; the structured record recovered `INCONEL alloy 725` from the image context. It also reconstructed the analysis table and verified two internal relationships:

- Ni + Co = 58.14, matching the reported 58.1 after rounding.
- Nb + Ta = 3.4232, matching the reported 3.42 after rounding.

For heat/lot W3535, all three displayed chemistry rows pass every minimum or maximum that is explicitly shown in the supplied image.

No value was invented for the obscured hardness cell, ambiguous handwritten part number, or dense table rows that could not be supported strongly enough.

## Actual missing-data synthesis demonstrated

- The boron result is blank for `W3535 01` and `W3535 27B`. The ladle row for the same heat reports `0.0002`, so Genuity proposes `0.0002` as an evidence-backed reconciliation candidate. It is not written as observed until a domain rule confirms that ladle boron may be treated as a heat-level property.
- Hardness row 9 column 2 is obscured. The median of the three visible same-row readings is `39.0 HRC`; Genuity records that only as an analytics imputation, never as a certified measurement.
