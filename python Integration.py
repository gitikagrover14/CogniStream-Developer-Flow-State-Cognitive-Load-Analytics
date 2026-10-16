import subprocess

scripts = [
    "python github_ingestion.py",
    "python slack_ingestion.py",
    "python ide_ingestion.py"
]

for script in scripts:
    print(f"Running {script}...")
    result = subprocess.run(["python", script], capture_output=True, text=True)
    print(result.stdout)
    print(result.stderr)
print("✅ All ingestion scripts executed successfully.")