import pandas as pd
import re
from typing import List, Dict


def normalize_column_names(df: pd.DataFrame) -> pd.DataFrame:
    """
    Convert column names to clean snake_case.
    """
    cleaned_columns = {}
    for col in df.columns:
        new_col = col.strip().lower()
        new_col = re.sub(r'[^a-z0-9]+', '_', new_col)
        new_col = new_col.strip('_')
        cleaned_columns[col] = new_col

    df = df.rename(columns=cleaned_columns)
    return df


def strip_whitespace(df: pd.DataFrame, logs: List[Dict]) -> pd.DataFrame:
    """Remove leading/trailing whitespace from all string cells."""
    for col in df.columns:
        for idx in df.index:
            val = df.at[idx, col]
            if isinstance(val, str) and val != val.strip():
                old_val = val
                df.at[idx, col] = val.strip()
                logs.append({
                    "row": int(idx + 2),
                    "column": str(col),
                    "old": str(old_val),
                    "new": str(val.strip()),
                    "action": "strip_whitespace",
                    "reason": "Removed extra spaces"
                })
    return df


def normalize_prices(df: pd.DataFrame, logs: List[Dict]) -> pd.DataFrame:
    """
    Clean price column:
    - Remove currency symbols
    - Convert to float
    - Flag non-numeric values
    """
    price_columns = [
        col for col in df.columns
        if 'price' in col.lower() or 'cost' in col.lower() or 'amount' in col.lower() or 'mrp' in col.lower()
    ]

    for col in price_columns:
        # Create new list to store cleaned values
        cleaned_values = []
        
        for idx in df.index:
            val = df.at[idx, col]
            if pd.isna(val) or val == '':
                cleaned_values.append(None)
                continue

            original = str(val)
            # Remove currency symbols and spaces
            cleaned = re.sub(r'[₹$€£,\s]', '', str(val))

            try:
                numeric_val = float(cleaned)
                if str(val) != str(numeric_val):
                    logs.append({
                        "row": int(idx + 2),
                        "column": str(col),
                        "old": str(original),
                        "new": str(numeric_val),
                        "action": "normalize_price",
                        "reason": "Converted to numeric"
                    })
                cleaned_values.append(numeric_val)
            except ValueError:
                logs.append({
                    "row": int(idx + 2),
                    "column": str(col),
                    "old": str(original),
                    "new": "None",
                    "action": "invalid_price",
                    "reason": f"Cannot convert '{original}' to number"
                })
                cleaned_values.append(None)
        
        # Replace entire column at once
        df[col] = cleaned_values

    return df


def remove_duplicates(df: pd.DataFrame, logs: List[Dict]) -> pd.DataFrame:
    """Remove duplicate rows and log them."""
    duplicate_mask = df.duplicated(keep='first')
    duplicate_count = duplicate_mask.sum()

    if duplicate_count > 0:
        duplicate_indices = df[duplicate_mask].index.tolist()
        for idx in duplicate_indices:
            logs.append({
                "row": int(idx + 2),
                "column": "all",
                "old": "duplicate row",
                "new": "removed",
                "action": "remove_duplicate",
                "reason": "Exact duplicate of earlier row"
            })
        df = df[~duplicate_mask].reset_index(drop=True)

    return df


def lowercase_text(df: pd.DataFrame, logs: List[Dict]) -> pd.DataFrame:
    """Lowercase all text in name/medicine columns."""
    name_columns = [
        col for col in df.columns
        if 'name' in col.lower() or 'medicine' in col.lower() or 'drug' in col.lower() or 'product' in col.lower()
    ]

    for col in name_columns:
        for idx in df.index:
            val = df.at[idx, col]
            if isinstance(val, str) and val != val.lower():
                old_val = val
                df.at[idx, col] = val.lower()
                logs.append({
                    "row": int(idx + 2),
                    "column": str(col),
                    "old": str(old_val),
                    "new": str(val.lower()),
                    "action": "lowercase",
                    "reason": "Standardized to lowercase"
                })

    return df


def run_cleaning_pipeline(df: pd.DataFrame) -> tuple:
    """
    Execute all cleaning steps in order.
    """
    logs: List[Dict] = []

    # Step 1: Normalize column names
    df = normalize_column_names(df)

    # Step 2: Strip whitespace
    df = strip_whitespace(df, logs)

    # Step 3: Lowercase medicine names
    df = lowercase_text(df, logs)

    # Step 4: Normalize prices
    df = normalize_prices(df, logs)

    # Step 5: Remove duplicates
    df = remove_duplicates(df, logs)

    return df, logs