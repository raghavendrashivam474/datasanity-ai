from fastapi import APIRouter, UploadFile, File, HTTPException
from fastapi.responses import JSONResponse, StreamingResponse
from io import BytesIO
import pandas as pd
import json
import math
from datetime import datetime

from app.utils.file_handler import read_csv, dataframe_to_csv_bytes
from app.services.cleaner import run_cleaning_pipeline
from app.services.suggester import run_typo_fixes
from app.services.validator import run_validation
from app.services.column_detector import detect_column_types
from app.services.report_generator import generate_excel_report

router = APIRouter()


def convert_to_json_safe(obj):
    """Convert any value to JSON-safe format."""
    if obj is None:
        return None
    if isinstance(obj, float):
        if math.isnan(obj) or math.isinf(obj):
            return None
        if obj == int(obj):
            return int(obj)
        return round(obj, 2)
    if isinstance(obj, (int, bool)):
        return obj
    if isinstance(obj, str):
        return obj
    return str(obj)


def clean_dict_for_json(data):
    """Recursively clean a dictionary for JSON serialization."""
    if isinstance(data, dict):
        return {k: clean_dict_for_json(v) for k, v in data.items()}
    elif isinstance(data, list):
        return [clean_dict_for_json(item) for item in data]
    else:
        return convert_to_json_safe(data)


@router.post("/clean-data")
async def clean_data(file: UploadFile = File(...)):
    """
    Main endpoint: Upload CSV → Get cleaned data + report.
    """
    if not file.filename.endswith('.csv'):
        raise HTTPException(
            status_code=400,
            detail="Only CSV files are supported"
        )

    try:
        # Step 1: Read the file
        df = await read_csv(file)
        original_rows = len(df)
        original_df = df.copy()

        # Step 2: Detect column types
        column_types = detect_column_types(df)

        # Step 3: Run cleaning pipeline
        df, cleaning_logs = run_cleaning_pipeline(df)

        # Step 4: Run typo detection
        df = run_typo_fixes(df, cleaning_logs)

        # Step 5: Run validation
        validation_logs = []
        run_validation(df, validation_logs)

        # Step 6: Calculate quality score
        all_logs = cleaning_logs + validation_logs
        total_cells = len(df) * len(df.columns)
        
        critical_issues = sum(
            1 for log in validation_logs 
            if log.get("severity") == "critical"
        )
        
        quality_score = max(0, min(100, 100 - (
            (critical_issues / max(total_cells, 1) * 200) + 
            (len(validation_logs) / max(total_cells, 1) * 50)
        )))

        # Step 7: Build summary
        summary = {
            "original_rows": original_rows,
            "cleaned_rows": len(df),
            "duplicates_removed": sum(
                1 for log in all_logs
                if log.get("action") == "remove_duplicate"
            ),
            "typos_fixed": sum(
                1 for log in all_logs
                if log.get("action") == "typo_fix"
            ),
            "validation_errors": sum(
                1 for log in all_logs
                if log.get("action") == "validation_error"
            ),
            "validation_warnings": sum(
                1 for log in all_logs
                if log.get("action") == "validation_warning"
            ),
            "validation_info": sum(
                1 for log in all_logs
                if log.get("action") == "validation_info"
            ),
            "total_changes": len(cleaning_logs),
            "total_issues": len(validation_logs),
            "quality_score": round(quality_score, 1),
            "total_cells": total_cells,
            "columns_detected": column_types
        }

        # Convert DataFrame to list of dicts
        df_clean = df.fillna("")
        cleaned_data = df_clean.to_dict(orient="records")

        # Build response
        response_data = {
            "status": "success",
            "summary": summary,
            "changes": cleaning_logs,
            "validation_issues": validation_logs,
            "cleaned_data": cleaned_data
        }

        # Clean everything for JSON
        safe_response = clean_dict_for_json(response_data)

        return JSONResponse(content=safe_response)

    except Exception as e:
        import traceback
        print(traceback.format_exc())
        raise HTTPException(
            status_code=500,
            detail=f"Error processing file: {str(e)}"
        )


@router.post("/clean-data/download")
async def clean_and_download(file: UploadFile = File(...)):
    """Upload CSV → Download cleaned CSV file."""
    if not file.filename.endswith('.csv'):
        raise HTTPException(
            status_code=400,
            detail="Only CSV files are supported"
        )

    try:
        df = await read_csv(file)
        df, logs = run_cleaning_pipeline(df)
        df = run_typo_fixes(df, logs)

        csv_bytes = dataframe_to_csv_bytes(df)

        return StreamingResponse(
            BytesIO(csv_bytes),
            media_type="text/csv",
            headers={
                "Content-Disposition":
                    f"attachment; filename=cleaned_{file.filename}"
            }
        )

    except Exception as e:
        import traceback
        print(traceback.format_exc())
        raise HTTPException(
            status_code=500,
            detail=f"Error processing file: {str(e)}"
        )


@router.post("/clean-data/report")
async def download_excel_report(file: UploadFile = File(...)):
    """Generate comprehensive Excel report with multiple sheets."""
    if not file.filename.endswith('.csv'):
        raise HTTPException(
            status_code=400,
            detail="Only CSV files are supported"
        )

    try:
        # Read original
        original_df = await read_csv(file)
        
        # Process
        df = original_df.copy()
        df, cleaning_logs = run_cleaning_pipeline(df)
        df = run_typo_fixes(df, cleaning_logs)
        
        validation_logs = []
        run_validation(df, validation_logs)
        
        # Calculate summary
        all_logs = cleaning_logs + validation_logs
        total_cells = len(df) * len(df.columns)
        
        critical_issues = sum(
            1 for log in validation_logs 
            if log.get("severity") == "critical"
        )
        
        quality_score = max(0, min(100, 100 - (
            (critical_issues / max(total_cells, 1) * 200) + 
            (len(validation_logs) / max(total_cells, 1) * 50)
        )))
        
        summary = {
            "original_rows": len(original_df),
            "cleaned_rows": len(df),
            "duplicates_removed": sum(
                1 for log in all_logs
                if log.get("action") == "remove_duplicate"
            ),
            "typos_fixed": sum(
                1 for log in all_logs
                if log.get("action") == "typo_fix"
            ),
            "validation_errors": sum(
                1 for log in all_logs
                if log.get("action") == "validation_error"
            ),
            "validation_warnings": sum(
                1 for log in all_logs
                if log.get("action") == "validation_warning"
            ),
            "total_changes": len(cleaning_logs),
            "total_issues": len(validation_logs),
            "quality_score": round(quality_score, 1),
            "total_cells": total_cells
        }
        
        # Generate Excel
        excel_bytes = generate_excel_report(
            original_df, df, summary, cleaning_logs, validation_logs
        )
        
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        
        return StreamingResponse(
            BytesIO(excel_bytes),
            media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            headers={
                "Content-Disposition": f"attachment; filename=DataSanity_Report_{timestamp}.xlsx"
            }
        )

    except Exception as e:
        import traceback
        print(traceback.format_exc())
        raise HTTPException(
            status_code=500,
            detail=f"Error generating report: {str(e)}"
        )