import pandas as pd
from io import BytesIO
from datetime import datetime


def generate_excel_report(
    original_df: pd.DataFrame,
    cleaned_df: pd.DataFrame,
    summary: dict,
    changes: list,
    issues: list
) -> bytes:
    """
    Generate comprehensive Excel report with multiple sheets.
    """
    output = BytesIO()
    
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        # Sheet 1: Cleaned Data
        cleaned_df.to_excel(writer, sheet_name='Cleaned Data', index=False)
        
        # Sheet 2: Original Data
        original_df.to_excel(writer, sheet_name='Original Data', index=False)
        
        # Sheet 3: Summary
        summary_df = pd.DataFrame([summary])
        summary_df.to_excel(writer, sheet_name='Summary', index=False)
        
        # Sheet 4: All Changes
        if changes:
            changes_df = pd.DataFrame(changes)
            changes_df.to_excel(writer, sheet_name='Changes Made', index=False)
        
        # Sheet 5: Issues Found
        if issues:
            issues_df = pd.DataFrame(issues)
            issues_df.to_excel(writer, sheet_name='Issues', index=False)
        
        # Sheet 6: Metadata
        metadata = {
            'Report Generated': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'Tool': 'DataSanity AI',
            'Version': '2.0.0',
            'Quality Score': summary.get('quality_score', 0)
        }
        metadata_df = pd.DataFrame([metadata])
        metadata_df.to_excel(writer, sheet_name='Metadata', index=False)
    
    output.seek(0)
    return output.getvalue()