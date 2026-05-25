"""
clean_data.py
Cleans the raw sales CSV produced by generate_data.py and saves:
  - cleaned_sales_data.csv   (clean dataset)
  - cleaning_log.txt         (audit trail of every fix applied)
"""

import pandas as pd
import numpy as np
import re
import os
from datetime import datetime

LOG_LINES = []

def log(msg):
    print(msg)
    LOG_LINES.append(msg)


# ── 1. Load ────────────────────────────────────────────────────────────────────
df = pd.read_csv("raw_sales_data.csv")
log(f"[{datetime.now()}] Loaded raw_sales_data.csv  →  {df.shape[0]} rows, {df.shape[1]} cols")
log(f"\n=== INITIAL QUALITY REPORT ===")
log(f"Total rows       : {len(df)}")
log(f"Duplicate rows   : {df.duplicated().sum()}")
log(f"Missing values   :\n{df.isnull().sum().to_string()}\n")


# ── 2. Remove duplicates ───────────────────────────────────────────────────────
before = len(df)
df.drop_duplicates(inplace=True)
df.reset_index(drop=True, inplace=True)
log(f"[DUPLICATES] Removed {before - len(df)} duplicate rows  →  {len(df)} rows remain")


# ── 3. Standardise text columns ───────────────────────────────────────────────
for col in ["region", "category", "status"]:
    df[col] = df[col].str.strip().str.title()
log(f"[STANDARDISE] region / category / status → Title Case")


# ── 4. Validate & fix emails ─────────────────────────────────────────────────
EMAIL_RE = re.compile(r"^[\w\.\+\-]+@[\w\-]+\.[a-z]{2,}$", re.I)

def fix_email(v):
    if pd.isna(v):
        return np.nan
    return v if EMAIL_RE.match(str(v)) else np.nan

bad_email = df["email"].apply(lambda v: pd.notna(v) and not EMAIL_RE.match(str(v))).sum()
df["email"] = df["email"].apply(fix_email)
log(f"[EMAIL] Invalidated {bad_email} malformed addresses → set to NaN")


# ── 5. Fix numeric columns ────────────────────────────────────────────────────
df["revenue"] = pd.to_numeric(df["revenue"], errors="coerce")
df["quantity"] = pd.to_numeric(df["quantity"], errors="coerce")
df["unit_price"] = pd.to_numeric(df["unit_price"], errors="coerce")
log(f"[NUMERIC] Coerced revenue / quantity / unit_price (bad strings → NaN)")


# ── 6. Fill missing numerics with median ──────────────────────────────────────
for col in ["quantity", "unit_price"]:
    med = df[col].median()
    missing = df[col].isna().sum()
    df[col] = df[col].fillna(med)
    log(f"[FILL] '{col}'  {missing} NaN → median {med:.2f}")

df["quantity"] = df["quantity"].round().astype("Int64")


# ── 7. Recalculate revenue where missing / wrong ──────────────────────────────
mask = df["revenue"].isna()
df.loc[mask, "revenue"] = (df.loc[mask, "quantity"] * df.loc[mask, "unit_price"]).round(2)
log(f"[RECALC] Re-computed revenue for {mask.sum()} rows")


# ── 8. Fill categorical NaNs ──────────────────────────────────────────────────
for col, fill in [("category", "Unknown"), ("status", "Unknown"), ("sales_rep", "Unassigned")]:
    n = df[col].isna().sum()
    df[col] = df[col].fillna(fill)
    log(f"[FILL] '{col}'  {n} NaN → '{fill}'")


# ── 9. Parse dates ────────────────────────────────────────────────────────────
df["order_date"] = pd.to_datetime(df["order_date"], errors="coerce")
log(f"[DATE] Parsed order_date  ({df['order_date'].isna().sum()} unparseable)")


# ── 10. Add derived columns ───────────────────────────────────────────────────
df["order_month"] = df["order_date"].dt.to_period("M").astype(str)
df["order_quarter"] = df["order_date"].dt.to_period("Q").astype(str)
log(f"[DERIVED] Added order_month, order_quarter")


# ── 11. Final report ──────────────────────────────────────────────────────────
log(f"\n=== FINAL QUALITY REPORT ===")
log(f"Total rows          : {len(df)}")
log(f"Remaining NaN total : {df.isnull().sum().sum()}")
log(f"Duplicate rows      : {df.duplicated().sum()}")
log(f"Columns             : {list(df.columns)}")


# ── 12. Save outputs ──────────────────────────────────────────────────────────
df.to_csv("cleaned_sales_data.csv", index=False)
log(f"\n✅  Saved cleaned_sales_data.csv")

with open("cleaning_log.txt", "w") as f:
    f.write("\n".join(LOG_LINES))
log(f"✅  Saved cleaning_log.txt")
