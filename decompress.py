import zipfile
import gzip
import bz2
import lzma
from pathlib import Path

def ensure_directory_exists(directory: Path) -> None:
    """Create the directory if it does not exist."""
    directory.mkdir(parents=True, exist_ok=True)

def get_valid_filepath(prompt: str, expected_extension: str) -> Path:
    """Prompt the user for a valid file path until the file exists."""
    while True:
        filepath = input(prompt).strip()
        path = Path(filepath)
        # Check if the file exists
        if not path.is_file():
            print(f"Error: The file '{filepath}' does not exist. Please try again.")
            continue
        # Check the file extension
        if path.suffix != expected_extension:
            print(f"Error: The file must have a '{expected_extension}' extension.")
            continue
        return path


def handle_existing_file(file_path: Path) -> bool:
    """Handle cases when the output file already exists.
    Returns True if the file should be overwritten, False otherwise.
    """
    while True:
        user_input = input(f"Warning: '{file_path}' already exists. "
                           "Do you want to (O)verwrite, (S)kip, or (R)ename? ").strip().lower()
        if user_input == 'o':
            return True  # Overwrite the file
        elif user_input == 's':
            return False  # Skip file
        elif user_input == 'r':
            new_name = input("Enter a path with a new name for the file: ").strip()
            new_path = Path(new_name)

            # Add the extension if it is not there
            if not new_path.suffix:
                new_path = new_path.with_suffix(file_path.suffix)

            # Check whether a new file exists
            if not new_path.exists():
                file_path.rename(new_path)  # Change the file name
                print(f"File will be saved as '{new_path}'.")
                return True  # Continue unpacking with a new path
            else:
                print(f"Error: '{new_path}' already exists. Please try again.")
        else:
            print("Invalid option. Please enter 'O', 'S', or 'R'.")


def decompress_zip(zip_filename: Path, extract_to: Path) -> None:
    """Decompress a ZIP file."""
    try:
        ensure_directory_exists(extract_to)  # Ensure output directory exists
        with zipfile.ZipFile(zip_filename, 'r') as zipf:
            for member in zipf.namelist():
                output_path = extract_to / member

                # Handle existing files
                if output_path.exists() and not handle_existing_file(output_path):
                    print(f"Skipping: {member}")
                    continue  # Skip this file

                zipf.extract(member, extract_to)
                print(f"Decompressed ZIP archive: {zip_filename} to {extract_to}")
    except zipfile.BadZipFile:
        print(f"Error: '{zip_filename}' is not a valid ZIP archive.")
    except Exception as e:
        print(f"An error occurred: {e}")


def decompress_gzip(gzip_filename: Path, output_dir: Path) -> None:
    """Decompress a GZIP file."""
    ensure_directory_exists(output_dir)  # Ensure output directory exists

    # Generate the path to the unpacked file in the selected folder
    output_filename = Path(gzip_filename).with_suffix('.txt').name
    output_path = Path(output_dir) / output_filename

    # Check for file existence
    if output_path.exists():
        print(f"Output file already exists: {output_path}")
        if not handle_existing_file(output_path):
            print("Skipping extraction.")
            return

    try:
        with gzip.open(gzip_filename, 'rb') as f_in:  # Open the GZIP file in binary read mode
            with open(output_path, 'wb') as f_out:  # Open the output file in binary write mode
                f_out.write(f_in.read())  # Read from the GZIP file and write to the output file

        print(f"Decompressed GZIP archive: {gzip_filename} to {output_path}")
    except OSError:
        print(f"Error: '{gzip_filename}' is not a valid GZIP archive.")
    except Exception as e:
        print(f"An error occurred: {e}")

def decompress_xz(xz_filename: Path, output_dir: Path) -> None:
    """Decompress an XZ file."""
    ensure_directory_exists(output_dir)  # Ensure output directory exists

    # Generate the path to the unpacked file by removing .xz extension
    output_filename = xz_filename.with_suffix('.txt').name
    output_path = output_dir / output_filename

    # Check for file existence
    if output_path.exists():
        print(f"Output file already exists: {output_path}")
        if not handle_existing_file(output_path):
            print("Skipping extraction.")
            return

    try:
        with lzma.open(xz_filename, 'rb') as f_in:  # Open the XZ file in binary read mode
            with open(output_path, 'wb') as f_out:  # Open the output file in binary write mode
                f_out.write(f_in.read())  # Read from the XZ file and write to the output file

        print(f"Decompressed XZ archive: {xz_filename} to {output_path}")
    except OSError:
        print(f"Error: '{xz_filename}' is not a valid XZ archive.")
    except Exception as e:
        print(f"An error occurred: {e}")

def decompress_bz2(bz2_filename: Path, output_dir: Path) -> None:
    """Decompress a BZIP2 file."""
    ensure_directory_exists(output_dir)  # Ensure output directory exists

    # Generate the path to the unpacked file by removing .bz2 extension
    output_filename = bz2_filename.with_suffix('.txt').name
    output_path = output_dir / output_filename

    # Check for file existence
    if output_path.exists():
        print(f"Output file already exists: {output_path}")
        if not handle_existing_file(output_path):
            print("Skipping extraction.")
            return

    try:
        with bz2.open(bz2_filename, 'rb') as f_in:  # Open the BZIP2 file in binary read mode
            with open(output_path, 'wb') as f_out:  # Open the output file in binary write mode
                f_out.write(f_in.read())  # Read from the BZIP2 file and write to the output file

        print(f"Decompressed BZIP2 archive: {bz2_filename} to {output_path}")
    except OSError:
        print(f"Error: '{bz2_filename}' is not a valid BZIP2 archive.")
    except Exception as e:
        print(f"An error occurred: {e}")



def main():
    """Main function to handle user input for decompression."""
    while True:
        archive_type = input("Archive type (zip/gz/bz2/xz): ").strip().lower()
        if archive_type in ('zip', 'gz', 'bz2', 'xz'):
            break
        print("Unsupported archive type. Please choose either 'zip' or 'gz', 'bz2' or 'xz'.")

    # Pass the expected extension directly to the get_valid_filepath function
    source_file = get_valid_filepath("Source archive file: ", f".{archive_type}")
    output_dir = input("Output directory: ").strip()
    output_path = Path(output_dir)  # Convert the line to Path

    print(f"Decompressing {archive_type} file: {source_file} to {output_path}")
    # Determine which decompression method to call based on the archive type
    if archive_type == 'zip':
        decompress_zip(source_file, output_path)
    elif archive_type == 'gz':
        decompress_gzip(source_file, output_path)
    elif archive_type == 'bz2':
        decompress_bz2(source_file, output_path)
    elif archive_type == 'xz':
        decompress_bz2(source_file, output_path)


if __name__ == "__main__":
    main()

