"""
HR Data Cleaning Project
------------------------
Reads raw_hr_data.csv, applies validation and cleaning rules,
and writes cleaned_hr_data.csv.
"""

import pandas as pd
import numpy as np

INPUT_FILE = "raw_hr_data.csv"
OUTPUT_FILE = "cleaned_hr_data.csv"

# Load data
df = pd.read_csv(INPUT_FILE)

# Standardize column names
df.columns = [c.strip().lower().replace(" ", "_") for c in df.columns]

# Remove duplicate employee IDs, retaining the first complete occurrence
df = df.drop_duplicates(subset=["employee_id"], keep="first")

# Trim and normalize text
text_cols = [
    "employee_name", "gender", "department", "job_title",
    "location", "employment_type", "email"
]
for col in text_cols:
    df[col] = df[col].astype("string").str.strip()

df["gender"] = df["gender"].str.title()
df["department"] = df["department"].str.title()
df["location"] = df["location"].str.title()
df["employment_type"] = df["employment_type"].str.title()

# Convert common empty strings to missing values
df = df.replace({"": pd.NA, "None": pd.NA, "nan": pd.NA, "NaN": pd.NA})

# Date validation
df["joining_date"] = pd.to_datetime(df["joining_date"], errors="coerce")

# Age validation: working-age employee range used for this simulated dataset
df["age"] = pd.to_numeric(df["age"], errors="coerce")
df.loc[~df["age"].between(18, 65, inclusive="both"), "age"] = np.nan

# Salary validation
df["salary"] = pd.to_numeric(df["salary"], errors="coerce")
df.loc[df["salary"] <= 0, "salary"] = np.nan

# Basic email validation
email_pattern = r"^[^@\s]+@[^@\s]+\.[^@\s]+$"
df.loc[~df["email"].fillna("").str.match(email_pattern), "email"] = pd.NA

# Impute missing age with overall median
df["age"] = df["age"].fillna(df["age"].median())

# Impute missing salary with department median, then overall median
df["salary"] = df["salary"].fillna(
    df.groupby("department")["salary"].transform("median")
)
df["salary"] = df["salary"].fillna(df["salary"].median())

# Business-rule correction for the known missing department
# In production, this should be confirmed against an authoritative HR source.
df.loc[df["employee_id"] == 1034, "department"] = "HR"

# Sort and export
df = df.sort_values("employee_id").reset_index(drop=True)
df["joining_date"] = df["joining_date"].dt.strftime("%Y-%m-%d")

df.to_csv(OUTPUT_FILE, index=False)

# Validation checks
assert df["employee_id"].is_unique
assert df["age"].between(18, 65).all()
assert (df["salary"] > 0).all()
assert pd.to_datetime(df["joining_date"], errors="coerce").notna().all()

print(f"Cleaned dataset written to: {OUTPUT_FILE}")
print(f"Rows: {len(df)}")
print(f"Columns: {len(df.columns)}")
print("Validation checks passed.")
