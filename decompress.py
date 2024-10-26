import zipfile
import gzip
from pathlib import Path

def decompress_zip(zip_filename: str, extract_to: str) -> None:
    """Decompress a ZIP file."""
    # Check for the existence of the source file
    if not Path(zip_filename).is_file():
        print(f"Error: The file '{zip_filename}' does not exist.")
        return

    try:
        with zipfile.ZipFile(zip_filename, 'r') as zipf:
            zipf.extractall(extract_to)  # Extract all files to the specified directory
        print(f"Decompressed ZIP archive: {zip_filename} to {extract_to}")
    except Exception as e:
        print(f"An error occurred: {e}")


def decompress_gzip(gzip_filename: str, output_dir: str) -> None:
    """Decompress a GZIP file."""
    # Check for the existence of the source file
    if not Path(gzip_filename).is_file():
        print(f"Error: The file '{gzip_filename}' does not exist.")
        return

    # Create the source directory if it does not already exist
    Path(output_dir).mkdir(parents=True, exist_ok=True)

    # We generate the path to the unpacked file in the selected folder
    output_filename = Path(gzip_filename).stem  # Назва без '.gz'
    output_path = Path(output_dir) / output_filename

    try:
        with gzip.open(gzip_filename, 'rb') as f_in:  # Open the GZIP file in binary read mode
            with open(output_path, 'wb') as f_out:  # Open the output file in binary write mode
                f_out.write(f_in.read())  # Read from the GZIP file and write to the output file
        print(f"Decompressed GZIP archive: {gzip_filename} to {output_filename}")
    except Exception as e:
        print(f"An error occurred: {e}")


def main():
    """Main function to handle user input for decompression."""
    while True:
        archive_type = input("Archive type (zip/gzip): ").strip().lower()
        if archive_type in ('zip', 'gzip'):
            break
        print("Unsupported archive type. Please choose either 'zip' or 'gzip'.")

    source_file = input("Source archive file: ").strip()  # Get the path to the source archive

    # Determine which decompression method to call based on the archive type
    if archive_type == 'zip':
        output_dir = input("Output directory: ").strip()  # Get the output directory for ZIP
        decompress_zip(source_file, output_dir)  # Call the ZIP decompression function
    elif archive_type == 'gzip':
        output_dir = input("Output directory: ").strip()  # Get the output file name for GZIP
        decompress_gzip(source_file, output_dir)  # Call the GZIP decompression function


if __name__ == "__main__":
    main()

