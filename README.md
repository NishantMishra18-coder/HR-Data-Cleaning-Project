# HR Employee Data Cleaning Project

## 1. Project Overview

This project demonstrates an end-to-end data cleaning workflow using **Python and Pandas**.

The selected public reference dataset is **IBM HR Analytics Employee Attrition & Performance**, a widely used HR analytics dataset containing employee demographics, job information, compensation, satisfaction and attrition fields.

**Public source:** Kaggle - IBM HR Analytics Employee Attrition & Performance  
https://www.kaggle.com/pavansubhasht/ibm-hr-analytics-attrition-dataset

The public dataset contains 1,470 rows and 35 columns. The original public file is already relatively clean. To make this assignment reproducible and demonstrate the requested data-quality problems, this repository contains a **controlled messy practice copy** using the same public dataset schema. Missing values, duplicates, incorrect numeric representations and inconsistent category labels were intentionally introduced.

> Important: The messy file in this repository is a controlled practice version, not an unmodified copy of the public source.

## 2. Objective

Identify and correct:

- Missing values
- Duplicate records
- Incorrect data types
- Inconsistent categorical values
- Basic invalid/range values

## 3. Tools Used

- Python 3
- Pandas
- NumPy
- GitHub

## 4. Repository Structure

```text
HR_Data_Cleaning_Project/
│
├── data/
│   ├── raw_hr_employee_data.csv
│   └── cleaned_hr_employee_data.csv
│
├── scripts/
│   └── clean_hr_data.py
│
├── reports/
│   ├── data_quality_report.csv
│   ├── issue_log.csv
│   └── data_dictionary.csv
│
├── README.md
└── requirements.txt
```

## 5. Problems Identified

### Missing Values
Several cells were intentionally left blank in fields such as Age, Department, Gender, MonthlyIncome and JobRole.

**Solution:**
- Numeric missing values → median
- Categorical missing values → mode

### Duplicate Records
Three exact duplicate employee records were intentionally inserted.

**Solution:**
`drop_duplicates()` was used to remove exact duplicate rows.

### Incorrect Data Types
Examples included:
- `Age = "thirty-five"`
- `MonthlyIncome = "5,500"`
- `DailyRate = "1,250"`
- `PercentSalaryHike = "15%"`
- `JobLevel = "2"`

**Solution:**
Numeric fields were cleaned and converted using `pd.to_numeric()`.

### Inconsistent Values
Examples included:
- `M`, `male`, ` male ` → `Male`
- `female` → `Female`
- `R&D` / `Research and Development` → `Research & Development`
- `Travel Rarely` → `Travel_Rarely`
- `YES` / `no` → standardized `Yes` / `No`

**Solution:**
Whitespace was removed and category mapping was applied.

### Range Validation
Age, JobLevel and PerformanceRating were checked against reasonable ranges.

## 6. Cleaning Workflow

```text
Load raw CSV
     ↓
Inspect missing values
     ↓
Check duplicates
     ↓
Trim text values
     ↓
Standardize categories
     ↓
Convert numeric columns
     ↓
Remove duplicates
     ↓
Impute missing values
     ↓
Validate ranges
     ↓
Export cleaned CSV
```

## 7. How to Run

Install dependencies:

```bash
pip install -r requirements.txt
```

Run:

```bash
python scripts/clean_hr_data.py
```

The cleaned dataset will be created at:

```text
data/cleaned_hr_employee_data.csv
```

The quality report will be created at:

```text
reports/data_quality_report.csv
```

## 8. Result

The final dataset is standardized and suitable for further analysis in:

- Excel
- Power BI
- SQL
- Python

The cleaned data can be used for HR dashboards, employee attrition analysis and exploratory data analysis.

## 9. Portfolio Skills Demonstrated

This project demonstrates practical skills in:

- Data cleaning
- Data validation
- Missing-value handling
- Duplicate removal
- Data-type conversion
- Categorical standardization
- Pandas
- CSV processing
- Documentation
- GitHub project organization

## 10. Source

IBM HR Analytics Employee Attrition & Performance is publicly available through Kaggle and other public repositories.

Original dataset reference:
https://www.kaggle.com/pavansubhasht/ibm-hr-analytics-attrition-dataset
