import polars as pl
from pathlib import Path

# Input and output directories
output_dir = Path("data/processed")
output_dir.mkdir(parents=True, exist_ok=True)

# Locate existing CSV files
files = {
    "github": [
        Path("data/raw/github_commits.csv"),
    ],
    "slack": [
        Path("data/raw/slack_data.csv"),
    ],
    "ide": [
        Path("Data/Raw/ide_activity.csv"),
        Path("data/raw/ide_activity.csv"),
    ],
}


def find_file(paths):
    for path in paths:
        if path.exists():
            return path
    return None


# 1. Clean GitHub data
github_path = find_file(files["github"])

if github_path:
    github = pl.read_csv(github_path)

    # Keep only relevant commit fields
    github = github.select([
        "sha",
        "commit.author.name",
        "commit.author.date",
        "commit.message",
    ])

    # Standardize column names
    github = github.rename({
        "sha": "commit_id",
        "commit.author.name": "author_name",
        "commit.author.date": "commit_timestamp",
        "commit.message": "commit_message",
    })

    # Convert timestamp to datetime
    github = github.with_columns(
        pl.col("commit_timestamp")
        .str.to_datetime(strict=False, time_zone="UTC")
    )

    # Remove duplicate records and save
    github = github.unique(subset=["commit_id"], maintain_order=True)

    github.write_csv(output_dir / "github_clean.csv")
    print("GitHub cleaned:", github.shape)

else:
    print("GitHub CSV not found.")


# 2. Clean Slack mock data
slack_path = find_file(files["slack"])

if slack_path:
    slack = pl.read_csv(slack_path)

    slack = slack.rename({
        "userId": "user_id",
        "id": "record_id",
    })

    # Remove duplicate records
    slack = slack.unique(subset=["record_id"], maintain_order=True)

    # Identify the source
    slack = slack.with_columns(
        pl.lit("slack_mock").alias("source")
    )

    slack.write_csv(output_dir / "slack_clean.csv")
    print("Slack mock data cleaned:", slack.shape)

else:
    print("Slack CSV not found.")


# 3. Clean IDE mock data
ide_path = find_file(files["ide"])

if ide_path:
    ide = pl.read_csv(ide_path)

    ide = ide.rename({
        "userId": "user_id",
        "id": "record_id",
    })

    # Remove duplicate records
    ide = ide.unique(subset=["record_id"], maintain_order=True)

    # Identify the source
    ide = ide.with_columns(
        pl.lit("ide_mock").alias("source")
    )

    ide.write_csv(output_dir / "ide_clean.csv")
    print("IDE mock data cleaned:", ide.shape)

else:
    print("IDE CSV not found.")


print("\nPreprocessing completed.")
print("Output folder:", output_dir.resolve())