import zipfile
import gzip
import bz2
import lzma
from pathlib import Path
from typing import Callable

def ensure_directory_exists(directory: Path) -> None:
    """Create the directory if it does not exist."""
    directory.mkdir(parents=True, exist_ok=True)

def get_valid_filepath(prompt: str, expected_extension: str) -> Path:
    """Prompt the user for a valid file path until the file exists."""
    while True:
        filepath = input(prompt).strip()
        path = Path(filepath)
        if not path.is_file():
            print(f"Error: The file '{filepath}' does not exist. Please try again.")
        elif path.suffix != expected_extension:
            print(f"Error: The file must have a '{expected_extension}' extension.")
        else:
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
            if not new_path.suffix:
                new_path = new_path.with_suffix(file_path.suffix)

            if not new_path.exists():
                file_path.rename(new_path)  # Change the file name
                print(f"File will be saved as '{new_path}'.")
                return True  # Continue unpacking with a new path
            else:
                print(f"Error: '{new_path}' already exists. Please try again.")
        else:
            print("Invalid option. Please enter 'O', 'S', or 'R'.")

def decompress_file(filename: Path, output_dir: Path, decompress_func: Callable[[Path, Path], None]) -> None:
    """Decompress a file using the provided decompression function."""
    ensure_directory_exists(output_dir)  # Ensure output directory exists
    output_filename = filename.with_suffix('.txt').name
    output_path = output_dir / output_filename

    if output_path.exists() and not handle_existing_file(output_path):
        print("Skipping extraction.")
        return

    try:
        decompress_func(filename, output_path)
        print(f"Decompressed {filename} to {output_path}")
    except Exception as e:
        print(f"An error occurred: {e}")

def decompress_zip(zip_filename: Path, output_path: Path) -> None:
    """Decompress a GZIP file."""
    with zipfile.ZipFile(zip_filename, 'r') as zipf:
        members = zipf.namelist()

        # Checking for a common root directory
        common_prefix = Path(members[0]).parts[0] if all(Path(m).parts[0] == Path(members[0]).parts[0] for m in members) else ""

        for member in members:
            # Remove the common prefix, if there is one
            relative_path = Path(member).relative_to(common_prefix) if common_prefix else Path(member)
            output_file_path = output_path / relative_path

            if member.endswith('/'):
                ensure_directory_exists(output_file_path)  # Create a folder
            else:
                ensure_directory_exists(output_file_path.parent)  # Create a parent folder

                if output_file_path.exists() and not handle_existing_file(output_file_path):
                    print(f"Skipping: {member}")
                    continue

                with zipf.open(member) as source, open(output_file_path, 'wb') as target:
                    target.write(source.read())

                print(f"Extracted '{member}' to '{output_file_path}'")

def decompress_gzip(gzip_filename: Path, output_path: Path) -> None:
    """Decompress a GZIP file."""
    with gzip.open(gzip_filename, 'rb') as f_in:
        write_file(f_in, output_path)

def decompress_bz2(bz2_filename: Path, output_path: Path) -> None:
    """Decompress a BZIP2 file."""
    with bz2.open(bz2_filename, 'rb') as f_in:
        write_file(f_in, output_path)

def decompress_xz(xz_filename: Path, output_path: Path) -> None:
    """Decompress an XZ file."""
    with lzma.open(xz_filename, 'rb') as f_in:
        write_file(f_in, output_path)

def write_file(source, output_path: Path) -> None:
    """Write the decompressed content to the output file."""
    with open(output_path, 'wb') as f_out:
        f_out.write(source.read())

def main():
    """Main function to handle user input for decompression."""
    archive_type = input("Archive type (zip/gz/bz2/xz): ").strip().lower()
    archive_format_map = {
        'zip': decompress_zip,
        'gz': decompress_gzip,
        'bz2': decompress_bz2,
        'xz': decompress_xz
    }

    if archive_type not in archive_format_map:
        print("Unsupported archive type. Please choose either 'zip', 'gz', 'bz2' or 'xz'.")
        return

    source_file = get_valid_filepath(f"Source archive file: ", f".{archive_type}")
    output_dir = Path(input("Output directory: ").strip())
    print(f"Decompressing {archive_type} file: {source_file} to {output_dir}")

    decompress_file(source_file, output_dir, archive_format_map[archive_type])

if __name__ == "__main__":
    main()
