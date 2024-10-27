import zipfile
import gzip
import bz2
import lzma
from datetime import datetime
from pathlib import Path
from typing import Callable, Dict

def generate_unique_archive_name(filename: str, extension: str, out_dir: str) -> Path:
    """Generates a unique archive name with the date and counter."""
    date = datetime.now().strftime('%Y%m%d')
    name = Path(filename).stem
    count = 1

    while True:
        archive_name = f"{name}_{date}_{count}.{extension}"
        archive_path = Path(out_dir) / archive_name
        if not archive_path.exists():
            return archive_path  # Unique name found
        count += 1

def ensure_directory_exists(directory: str) -> None:
    """Checks if the directory exists and creates it if necessary."""
    Path(directory).mkdir(parents=True, exist_ok=True)

def check_file_exists(filename: str) -> Path:
    """Checks if the file exists and prompts the user again if the file is missing."""
    path = Path(filename)
    while not path.exists():
        print(f"The source file '{filename}' does not exist. Enter a valid source file.")
        filename = input("Source file: ").strip()
        path = Path(filename)
    return path

def compress_file(
    filename: Path,
    out_dir: str,
    extension: str,
    compress_func: Callable[[Path, Path], None]
) -> None:
    """Universal function for compressing files in various formats."""
    ensure_directory_exists(out_dir)
    archive_path = generate_unique_archive_name(filename, extension, out_dir)

    print(f"Creating {extension.upper()} archive: {archive_path}")
    try:
        compress_func(filename, archive_path)
    except Exception as e:
        print(f"An unexpected error occurred while creating {extension.upper()} archive: {e}")

def compress_to_zip(filename: Path, archive_path: Path) -> None:
    """Compresses the file in ZIP format."""
    with zipfile.ZipFile(archive_path, 'w') as zipf:
        zipf.write(filename, arcname=filename.name)

def compress_to_gzip(filename: Path, archive_path: Path) -> None:
    """Compresses the file in GZIP format."""
    with open(filename, 'rb') as f_in, gzip.open(archive_path, 'wb') as f_out:
        f_out.write(f_in.read())

def compress_to_bzip2(filename: Path, archive_path: Path) -> None:
    """Compresses the file in BZIP2 format."""
    with open(filename, 'rb') as f_in, bz2.open(archive_path, 'wb') as f_out:
        f_out.write(f_in.read())

def compress_to_xz(filename: Path, archive_path: Path) -> None:
    """Compresses the file in XZ format."""
    with open(filename, 'rb') as f_in, lzma.open(archive_path, 'wb') as f_out:
        f_out.write(f_in.read())

def main():
    """Main function for handling user input and initiating compression."""
    try:
        source_file = check_file_exists(input("Source file     : ").strip())
        output_dir = input("Output directory: ").strip()
        archive_type = input("Archive type    : ").strip().lower()

        # Mapping archive types to their corresponding functions
        archive_map: Dict[str, Callable[[Path, Path], None]] = {
            'zip': compress_to_zip,
            'gzip': compress_to_gzip,
            'bzip2': compress_to_bzip2,
            'xz': compress_to_xz
        }

        if archive_type in archive_map:
            compress_file(source_file, output_dir, archive_type, archive_map[archive_type])
        else:
            print("Unsupported archive type. Please choose either 'zip', 'gzip', 'bzip2', or 'xz'.")

    except Exception as e:
        print(f"An unexpected error occurred: {e}")

if __name__ == "__main__":
    main()
