import pandas as pd
from io import StringIO, BytesIO
from fastapi import UploadFile


async def read_csv(file: UploadFile) -> pd.DataFrame:
    """
    Read uploaded CSV into a pandas DataFrame.
    """
    contents = await file.read()

    try:
        text = contents.decode("utf-8")
    except UnicodeDecodeError:
        text = contents.decode("latin-1")

    # Read with dtype=object to avoid strict string types
    df = pd.read_csv(StringIO(text), dtype=object)

    # Strip whitespace from column names
    df.columns = df.columns.str.strip()

    return df


def dataframe_to_csv_bytes(df: pd.DataFrame) -> bytes:
    """Convert DataFrame back to CSV bytes for download."""
    buffer = BytesIO()
    df.to_csv(buffer, index=False)
    buffer.seek(0)
    return buffer.getvalue()