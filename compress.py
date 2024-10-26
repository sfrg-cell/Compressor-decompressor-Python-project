import zipfile
import gzip
from datetime import datetime
from pathlib import Path

def generate_unique_archive_name(filename: str, extension: str, out_dir: str) -> str:
    """Generates a unique archive name with the date and counter."""
    date = datetime.now().strftime('%Y%m%d')
    name = Path(filename).stem
    count = 1  # Initial counter

    # Loop to ensure the archive name is unique
    while True:
        archive_name = f"{name}_{date}_{count}.{extension}"
        archive_path = Path(out_dir) / archive_name
        if not archive_path.exists():  # If the file doesn't exist, return the name
            return archive_name
        count += 1  # If the file exists, increment the counter

def ensure_directory_exists(directory: str) -> None:
    """Checks if the directory exists and creates it if necessary."""
    Path(directory).mkdir(parents=True, exist_ok=True)

def compress_to_zip(filename: str, out_dir: str) -> None:
    """File compression in ZIP format."""
    ensure_directory_exists(out_dir)  # Ensure the directory is created
    archive_name = generate_unique_archive_name(filename, 'zip', out_dir)
    print(f"Creating ZIP archive: {Path(out_dir) / archive_name}")  # Debug
    with zipfile.ZipFile(Path(out_dir) / archive_name, 'w') as zipf:
        zipf.write(filename, arcname=Path(filename).name)

compress_to_zip('example2.txt', './archives')
