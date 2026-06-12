import subprocess

scripts = [
    "scripts/data_ingestion.py",
    "scripts/live_nav_fetch.py",
    "scripts/clean_data.py",
    "scripts/load_to_sqlite.py"
]

for script in scripts:
    print(f"Running {script}")
    subprocess.run(["python", script])

print("Pipeline completed successfully.")