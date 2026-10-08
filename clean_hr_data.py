import pandas as pd
from pathlib import Path

BASE = Path(__file__).resolve().parents[1]
RAW = BASE / "data" / "raw_hr_employee_data.csv"
CLEAN = BASE / "data" / "cleaned_hr_employee_data.csv"
REPORT = BASE / "reports" / "data_quality_report.csv"

df = pd.read_csv(RAW)

rows_before = len(df)
duplicates_before = int(df.duplicated().sum())
missing_before = int(df.isna().sum().sum())

# 1) Standardize whitespace in text columns
text_cols = df.select_dtypes(include="object").columns
for col in text_cols:
    df[col] = df[col].apply(lambda x: x.strip() if isinstance(x, str) else x)

# 2) Standardize categorical values
maps = {
    "Gender": {"M": "Male", "F": "Female", "male": "Male", "female": "Female"},
    "Department": {"R&D": "Research & Development", "Research and Development": "Research & Development"},
    "BusinessTravel": {"Travel Rarely": "Travel_Rarely", "travel_frequently": "Travel_Frequently"},
    "Attrition": {"YES": "Yes", "NO": "No", "yes": "Yes", "no": "No"},
    "OverTime": {"YES": "Yes", "NO": "No", "yes": "Yes", "no": "No"},
}
for col, mapping in maps.items():
    df[col] = df[col].replace(mapping)

# 3) Convert numeric columns safely.
# Invalid text such as "thirty-five" becomes NaN and is handled below.
numeric_cols = [
    "Age","DailyRate","DistanceFromHome","Education","EmployeeCount","EmployeeNumber",
    "EnvironmentSatisfaction","HourlyRate","JobInvolvement","JobLevel","JobSatisfaction",
    "MonthlyIncome","MonthlyRate","NumCompaniesWorked","PercentSalaryHike",
    "PerformanceRating","RelationshipSatisfaction","StandardHours","StockOptionLevel",
    "TotalWorkingYears","TrainingTimesLastYear","WorkLifeBalance","YearsAtCompany",
    "YearsInCurrentRole","YearsSinceLastPromotion","YearsWithCurrManager"
]
for col in numeric_cols:
    if col == "PercentSalaryHike":
        df[col] = df[col].astype(str).str.replace("%", "", regex=False)
    if col == "MonthlyIncome" or col == "MonthlyRate" or col == "DailyRate":
        df[col] = df[col].astype(str).str.replace(",", "", regex=False)
    df[col] = pd.to_numeric(df[col], errors="coerce")

# 4) Remove exact duplicate records
df = df.drop_duplicates().copy()

# 5) Handle missing / invalid values.
# Numeric fields: median imputation.
for col in numeric_cols:
    if df[col].isna().any():
        df[col] = df[col].fillna(df[col].median())

# Categorical fields: mode imputation.
categorical_cols = [c for c in df.columns if c not in numeric_cols]
for col in categorical_cols:
    if df[col].isna().any():
        mode = df[col].mode(dropna=True)
        if not mode.empty:
            df[col] = df[col].fillna(mode.iloc[0])

# 6) Basic range validation.
df.loc[~df["Age"].between(18, 60), "Age"] = df["Age"].median()
df.loc[~df["JobLevel"].between(1, 5), "JobLevel"] = df["JobLevel"].median()
df.loc[~df["PerformanceRating"].between(1, 4), "PerformanceRating"] = df["PerformanceRating"].median()

# Restore integer-like columns.
integer_cols = [c for c in numeric_cols if c not in ["MonthlyIncome","MonthlyRate","DailyRate"]]
for col in integer_cols:
    df[col] = df[col].round().astype(int)

df.to_csv(CLEAN, index=False)

# Quality report
report = pd.DataFrame([
    ["Missing values", missing_before, int(df.isna().sum().sum()), "Handled with median/mode imputation"],
    ["Duplicate rows", duplicates_before, int(df.duplicated().sum()), "Removed exact duplicate records"],
    ["Rows", rows_before, len(df), "Three exact duplicate rows removed"],
    ["Columns", df.shape[1], df.shape[1], "No columns removed"],
    ["Object/numeric conversion", "Dirty numeric strings present", "Validated numeric columns", "Converted with pandas.to_numeric"],
])
report.columns = ["Issue", "Before", "After", "Action"]
report.to_csv(REPORT, index=False)

print("Cleaning completed.")
print(f"Rows before: {rows_before}")
print(f"Rows after : {len(df)}")
print(f"Duplicates removed: {duplicates_before}")
print(f"Missing values before: {missing_before}")
print(f"Missing values after : {int(df.isna().sum().sum())}")
