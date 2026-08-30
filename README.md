# HR Data Cleaning Project

## Files

- `raw_hr_data.csv` — original simulated HR data with deliberate quality issues.
- `cleaned_hr_data.csv` — validated and cleaned output.
- `hr_data_cleaning.py` — reproducible Python cleaning script.
- `HR_Data_Cleaning_Report.docx` — methodology, cleaning decisions, validation and conclusion.

## Requirements

Python 3.9+ and:

```bash
pip install pandas numpy
```

## Run

Place all files in the same directory and run:

```bash
python hr_data_cleaning.py
```

The script reads `raw_hr_data.csv` and creates/overwrites `cleaned_hr_data.csv`.

## Main Cleaning Rules

1. Standardize column names and text values.
2. Remove duplicate employee IDs.
3. Validate and parse joining dates.
4. Validate age (18–65 for this simulated dataset).
5. Treat zero/negative salary as invalid.
6. Validate basic email structure.
7. Impute missing age with the median.
8. Impute missing salary with department median, then overall median.
9. Resolve the missing department for the Recruiter record as HR.
10. Run final validation assertions before export.

> Note: The dataset is simulated for demonstration/assignment purposes. In a production HR system, corrections should be checked against authoritative HR records.
