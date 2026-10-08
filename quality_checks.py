import pandas as pd

raw = pd.read_csv("data/raw_hr_employee_data.csv")
clean = pd.read_csv("data/cleaned_hr_employee_data.csv")

print("RAW SHAPE:", raw.shape)
print("CLEAN SHAPE:", clean.shape)

print("\nMissing values before:")
print(raw.isna().sum()[raw.isna().sum() > 0])

print("\nDuplicate rows before:", raw.duplicated().sum())
print("Duplicate rows after:", clean.duplicated().sum())

print("\nData types after cleaning:")
print(clean.dtypes)

print("\nStandardized categories:")
for col in ["Gender", "Department", "BusinessTravel", "Attrition", "OverTime"]:
    print(col, sorted(clean[col].dropna().unique().tolist()))
