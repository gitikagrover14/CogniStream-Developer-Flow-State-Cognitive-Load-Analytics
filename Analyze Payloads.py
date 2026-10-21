import pandas as pd
from pathlib import Path

# CSV file paths
files = {
    "GitHub": "data/raw/github_commits.csv",
    "Slack": "data/raw/slack_data.csv",
    "IDE": "Data/Raw/ide_activity.csv"
}

for source, file_path in files.items():
    print(f"\n{'=' * 50}")
    print(f"SOURCE: {source}")
    print(f"{'=' * 50}")

    path = Path(file_path)

    if not path.exists():
        print(f"File not found: {file_path}")
        continue

    df = pd.read_csv(path)

    print("\nShape (rows, columns):")
    print(df.shape)

    print("\nColumn names:")
    print(df.columns.tolist())

    print("\nData types:")
    print(df.dtypes)

    print("\nMissing values:")
    print(df.isnull().sum())

    print("\nDuplicate rows:")
    print(df.duplicated().sum())

    print("\nSample records:")
    print(df.head(3).to_string(index=False))