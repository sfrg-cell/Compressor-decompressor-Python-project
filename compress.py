import zipfile
import gzip
import bz2
import lzma
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

    # Check for the existence of the source file
    while not Path(filename).exists():
        print(f"The source file '{filename}' does not exist. Enter the valid source file.")
        filename = input("Source file: ").strip()

    archive_name = generate_unique_archive_name(filename, 'zip', out_dir)
    print(f"Creating ZIP archive: {Path(out_dir) / archive_name}")  # Debug

    try:
        with zipfile.ZipFile(Path(out_dir) / archive_name, 'w') as zipf:
            zipf.write(filename, arcname=Path(filename).name)
    except Exception as e:
        print(f"An unexpected error occurred while creating ZIP archive: {e}")

def compress_to_gzip(filename: str, out_dir: str) -> None:
    """File compression in GZIP format."""
    # Check for the existence of the source file
    while not Path(filename).exists():
        print(f"The source file '{filename}' does not exist. Enter the valid source file.")
        filename = input("Source file: ").strip()

    archive_name = generate_unique_archive_name(filename, 'gz', out_dir)
    print(f"Creating GZIP archive: {Path(out_dir) / archive_name}")
    try:
        with gzip.open(Path(out_dir) / archive_name, 'wb') as f_out:
            with open(filename, 'rb') as f_in:
                f_out.write(f_in.read())
    except Exception as e:
        print(f"An unexpected error occurred while creating GZIP archive: {e}")


def compress_to_bzip2(filename: str, out_dir: str) -> None:
    """File compression in BZIP2 format."""
    # Check for the existence of the source file
    while not Path(filename).exists():
        print(f"The source file '{filename}' does not exist. Enter a valid source file.")
        filename = input("Source file: ").strip()

    archive_name = generate_unique_archive_name(filename, 'bz2', out_dir)
    print(f"Creating BZIP2 archive: {Path(out_dir) / archive_name}")
    try:
        with bz2.open(Path(out_dir) / archive_name, 'wb') as f_out:
            with open(filename, 'rb') as f_in:
                f_out.write(f_in.read())
    except Exception as e:
        print(f"An unexpected error occurred while creating BZIP2 archive: {e}")

def compress_to_xz(filename: str, out_dir: str) -> None:
    """File compression in XZ format."""
    # Check for the existence of the source file
    while not Path(filename).exists():
        print(f"The source file '{filename}' does not exist. Enter a valid source file.")
        filename = input("Source file: ").strip()

    archive_name = generate_unique_archive_name(filename, 'xz', out_dir)
    print(f"Creating XZ archive: {Path(out_dir) / archive_name}")
    try:
        with lzma.open(Path(out_dir) / archive_name, 'wb') as f_out:
            with open(filename, 'rb') as f_in:
                f_out.write(f_in.read())
    except Exception as e:
        print(f"An unexpected error occurred while creating XZ archive: {e}")

def main():
    try:
        source_file = input("Source file     : ").strip()
        output_dir = input("Output directory: ").strip()
        archive_type = input("Archive type    : ").strip().lower()

        # Ensure the output directory exists
        ensure_directory_exists(output_dir)

        # Call the appropriate compression function based on user input
        if archive_type == 'zip':
            compress_to_zip(source_file, output_dir)
        elif archive_type == 'gzip':
            compress_to_gzip(source_file, output_dir)
        elif archive_type == 'bzip2':
            compress_to_bzip2(source_file, output_dir)
        elif archive_type == 'xz':
            compress_to_xz(source_file, output_dir)
        else:
            print("Unsupported archive type. Please choose either 'zip', 'gzip', 'bzip2' or 'xz'.")
    except ValueError:
        print("Error: Invalid value entered.")
    except Exception as e:
        print(f"An unexpected error occurred in main: {e}")


if __name__ == "__main__":
    main()



