from typing import Dict, List
import pandas as pd


def detect_column_types(df: pd.DataFrame) -> Dict[str, List[str]]:
    """
    Automatically detect what each column represents.
    """
    
    medicine_keywords = ['medicine', 'drug', 'name', 'product', 'item', 'med']
    price_keywords = ['price', 'cost', 'rate', 'amount', 'mrp', 'value']
    quantity_keywords = ['quantity', 'qty', 'stock', 'units', 'count', 'available']
    date_keywords = ['expiry', 'exp', 'date', 'valid', 'mfg', 'manufacture']
    batch_keywords = ['batch', 'lot', 'serial', 'code']
    
    column_map = {
        'medicine_name': [],
        'price': [],
        'quantity': [],
        'expiry_date': [],
        'batch': [],
        'unknown': []
    }
    
    for col in df.columns:
        col_lower = col.lower()
        
        if any(kw in col_lower for kw in medicine_keywords):
            column_map['medicine_name'].append(col)
        elif any(kw in col_lower for kw in price_keywords):
            column_map['price'].append(col)
        elif any(kw in col_lower for kw in quantity_keywords):
            column_map['quantity'].append(col)
        elif any(kw in col_lower for kw in date_keywords):
            column_map['expiry_date'].append(col)
        elif any(kw in col_lower for kw in batch_keywords):
            column_map['batch'].append(col)
        else:
            column_map['unknown'].append(col)
    
    return column_map