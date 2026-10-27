import pandas as pd
from pathlib import Path

files = {
    "Raw IDE": "Data/Raw/ide_activity.csv",
    "Raw Slack": "data/raw/slack_data.csv",
    "Cleaned IDE": "data/processed/ide_clean.csv",
    "Cleaned Slack": "data/processed/slack_clean.csv",
}

for name, file_path in files.items():
    path = Path(file_path)

    print("\n" + "=" * 60)
    print(f"DATASET: {name}")
    print(f"FILE: {file_path}")
    print("=" * 60)

    if not path.exists():
        print("File not found. Check the file path.")
        continue

    df = pd.read_csv(path)

    print("\nShape:", df.shape)
    print("\nColumns:", df.columns.tolist())
    print("\nData types:\n", df.dtypes)
    print("\nMissing values:\n", df.isnull().sum())
    print("\nDuplicate rows:", df.duplicated().sum())
    print("\nFirst 5 rows:\n", df.head())

    timestamp_columns = [
        col for col in df.columns
        if any(word in col.lower()
               for word in ["timestamp", "datetime", "created_at", "time", "date"])
    ]

    print("\nPossible timestamp columns:", timestamp_columns)

    if timestamp_columns:
        for col in timestamp_columns:
            print(f"\nTimestamp sample for {col}:")
            print(df[col].head())
