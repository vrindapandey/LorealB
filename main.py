import subprocess
import sys

scripts = [
    "Scraper.py",
    "dataCleaner.py",
    "productScraper.py",
    "analyzer.py"
]

for script in scripts:
    print(f"\nRunning {script}...\n")

    result = subprocess.run([sys.executable, script])

    if result.returncode != 0:
        print(f"{script} failed. Stopping pipeline.")
        sys.exit(1)

    print(f"{script} complete.\n")

print("Process completed successfully.")
