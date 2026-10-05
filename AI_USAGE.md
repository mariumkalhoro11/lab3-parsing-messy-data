# AI Usage

## Tool Used
ChatGPT

## Prompt Used

I am cleaning a synthetic clinical dataset for a university data-wrangling assignment.

Convert the records into a structured CSV table.

Requirements:
1. Preserve exactly one output row for every input record.
2. Do not invent missing information.
3. Convert all dates to YYYY-MM-DD.
4. Standardize sex values as Male, Female, or Unknown.
5. Standardize enrollment site values as Site A, Site B, or Site C.
6. Standardize glucose units.
7. Convert glucose values to mg/dL where possible.
8. Preserve notes.
9. Do not guess when a value is ambiguous.
10. Return a structured CSV table comparable to the regex output.