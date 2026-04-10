import pandas as pd
from datetime import datetime
from typing import List, Dict


def validate_required_fields(
    df: pd.DataFrame,
    logs: List[Dict]
) -> None:
    """Flag rows where critical fields are empty."""
    name_columns = [
        col for col in df.columns
        if 'name' in col.lower()
        or 'medicine' in col.lower()
        or 'product' in col.lower()
    ]

    for col in name_columns:
        for idx in df.index:
            val = df.at[idx, col]
            if pd.isna(val) or (
                isinstance(val, str) and val.strip() == ''
            ):
                logs.append({
                    "row": int(idx + 2),
                    "column": str(col),
                    "old": str(val) if val else "empty",
                    "new": "None",
                    "action": "validation_error",
                    "severity": "critical",
                    "reason": f"Required field '{col}' is empty"
                })


def validate_prices(
    df: pd.DataFrame,
    logs: List[Dict]
) -> None:
    """Check for negative or zero prices."""
    price_columns = [
        col for col in df.columns
        if 'price' in col.lower()
        or 'cost' in col.lower()
        or 'mrp' in col.lower()
    ]

    for col in price_columns:
        for idx in df.index:
            val = df.at[idx, col]
            if pd.notna(val):
                try:
                    numeric_val = float(val)
                    if numeric_val < 0:
                        logs.append({
                            "row": int(idx + 2),
                            "column": str(col),
                            "old": str(val),
                            "new": "None",
                            "action": "validation_error",
                            "severity": "critical",
                            "reason": f"Negative price: {val}"
                        })
                    elif numeric_val == 0:
                        logs.append({
                            "row": int(idx + 2),
                            "column": str(col),
                            "old": str(val),
                            "new": "None",
                            "action": "validation_warning",
                            "severity": "medium",
                            "reason": "Price is zero"
                        })
                except (ValueError, TypeError):
                    pass


def validate_quantities(
    df: pd.DataFrame,
    logs: List[Dict]
) -> None:
    """Check for missing or invalid quantities."""
    qty_columns = [
        col for col in df.columns
        if 'quantity' in col.lower()
        or 'qty' in col.lower()
        or 'stock' in col.lower()
    ]

    for col in qty_columns:
        for idx in df.index:
            val = df.at[idx, col]
            if pd.isna(val) or val == '':
                logs.append({
                    "row": int(idx + 2),
                    "column": str(col),
                    "old": "empty",
                    "new": "None",
                    "action": "validation_warning",
                    "severity": "medium",
                    "reason": "Quantity is missing"
                })


def validate_expiry_dates(
    df: pd.DataFrame,
    logs: List[Dict]
) -> None:
    """Flag expired medicines and those expiring soon."""
    date_columns = [
        col for col in df.columns
        if 'expiry' in col.lower()
        or 'exp' in col.lower()
    ]

    today = pd.Timestamp.now()

    for col in date_columns:
        for idx in df.index:
            val = df.at[idx, col]
            if pd.isna(val) or val == '':
                continue
            try:
                date_val = pd.to_datetime(val)
                
                # Check if already expired
                if date_val < today:
                    days_ago = (today - date_val).days
                    logs.append({
                        "row": int(idx + 2),
                        "column": str(col),
                        "old": str(val),
                        "new": "None",
                        "action": "validation_error",
                        "severity": "critical",
                        "reason": f"Medicine EXPIRED {days_ago} days ago on {val}"
                    })
                # Check if expiring within 30 days
                elif date_val < today + pd.Timedelta(days=30):
                    days_left = (date_val - today).days
                    logs.append({
                        "row": int(idx + 2),
                        "column": str(col),
                        "old": str(val),
                        "new": "None",
                        "action": "validation_warning",
                        "severity": "high",
                        "reason": f"Expiring soon in {days_left} days on {val}"
                    })
                # Check if expiring within 90 days (3 months)
                elif date_val < today + pd.Timedelta(days=90):
                    days_left = (date_val - today).days
                    logs.append({
                        "row": int(idx + 2),
                        "column": str(col),
                        "old": str(val),
                        "new": "None",
                        "action": "validation_info",
                        "severity": "low",
                        "reason": f"Expiring in {days_left} days on {val}"
                    })
                    
            except (ValueError, TypeError):
                logs.append({
                    "row": int(idx + 2),
                    "column": str(col),
                    "old": str(val),
                    "new": "None",
                    "action": "validation_error",
                    "severity": "medium",
                    "reason": f"Invalid date format: {val}"
                })


def run_validation(
    df: pd.DataFrame,
    logs: List[Dict]
) -> None:
    """Execute all validation checks."""
    validate_required_fields(df, logs)
    validate_prices(df, logs)
    validate_quantities(df, logs)
    validate_expiry_dates(df, logs)