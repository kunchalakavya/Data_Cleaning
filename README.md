# Data Cleaning & Reporting Automation

Automated Python pipeline that generates a messy sales dataset, cleans it, and produces a professional multi-sheet Excel report with charts — all in one command.

---

## Project Structure

```
data-cleaning-automation/
│
├── generate_data.py      # Creates raw messy CSV (duplicates, nulls, bad values)
├── clean_data.py         # Cleans and standardises the data
├── generate_report.py    # Builds Excel report + PNG charts
├── run_pipeline.py       # ▶ Run this — executes all 3 steps in order
├── requirements.txt      # Python dependencies
└── README.md
```

---

## What the Pipeline Does

### Step 1 — `generate_data.py`
Generates a realistic but deliberately messy 315-row sales CSV with:
- Missing values across 6 columns
- Duplicate rows (15 injected)
- Inconsistent casing (`north`, `NORTH`, `North`)
- Invalid emails (`notanemail`)
- Non-numeric revenue values (`N/A` strings)

### Step 2 — `clean_data.py`
Cleans every issue and writes an audit log:

| Issue | Fix Applied |
|---|---|
| Duplicate rows | `drop_duplicates()` |
| Inconsistent casing | `.str.title()` normalisation |
| Invalid emails | Regex validation → NaN |
| Non-numeric revenue | `pd.to_numeric(errors='coerce')` |
| Missing numerics | Filled with column **median** |
| Missing categories | Filled with `"Unknown"` / `"Unassigned"` |
| Revenue mismatches | Recalculated as `quantity × unit_price` |
| Date parsing | `pd.to_datetime()` with derived month/quarter columns |

### Step 3 — `generate_report.py`
Produces `sales_report.xlsx` with **5 sheets**:

| Sheet | Contents |
|---|---|
| Executive Summary | KPI cards + Revenue by Region table |
| Monthly Trends | Month-wise orders & revenue + bar chart |
| Category Analysis | Revenue per category + pie chart |
| Status Breakdown | Completed / Pending / Cancelled + bar chart |
| Cleaned Data (Sample) | First 200 rows of the clean dataset |

Charts are also saved as PNG files in the `charts/` folder.

---

## How to Run

### 1. Install dependencies
```bash
pip install -r requirements.txt
```

### 2. Run the full pipeline
```bash
python run_pipeline.py
```

### Output files created
```
raw_sales_data.csv        ← messy input
cleaned_sales_data.csv    ← clean output
cleaning_log.txt          ← full audit trail
sales_report.xlsx         ← Excel report (5 sheets)
charts/
  ├── monthly_revenue.png
  ├── category_pie.png
  └── status_breakdown.png
```

---

## Key Concepts Demonstrated

- **Data Preprocessing** — handling nulls, duplicates, type errors, inconsistent formats
- **Automation** — single command runs the entire ETL + reporting pipeline
- **Reporting Efficiency** — structured Excel output with KPIs, tables, and embedded charts
- **Audit Trail** — `cleaning_log.txt` records every transformation with counts

---

## Technologies Used

| Tool | Purpose |
|---|---|
| `pandas` | Data loading, cleaning, aggregation |
| `openpyxl` | Excel workbook creation and formatting |
| `matplotlib` | Chart generation |
| `faker` | Realistic synthetic data generation |
| `numpy` | Numerical operations |

---

## Sample Output

**KPIs on Executive Summary sheet:**
- Total Revenue, Total Orders, Avg Order Value, Completion Rate

**Cleaning log excerpt:**
```
[DUPLICATES] Removed 15 duplicate rows → 300 rows remain
[STANDARDISE] region / category / status → Title Case
[EMAIL] Invalidated 10 malformed addresses → set to NaN
[FILL] 'quantity'  12 NaN → median 10.0
[RECALC] Re-computed revenue for 8 rows
```
