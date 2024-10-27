import tarfile
from pathlib import Path
from compress import compress_to_zip, compress_to_gzip, compress_to_bzip2, compress_to_xz
from decompress import decompress_zip, decompress_gzip, decompress_bz2, decompress_xz

def generate_backup_name(source_dir: Path, count: int, archive_type: str) -> str:
    """Generates a unique backup name based on the source directory and current date."""
    archive_name = f"{source_dir.name}_{count}.{archive_type}"
    return archive_name

def create_tar_backup(source_dir: Path, output_dir: Path, files_to_backup: dict) -> Path:
    """Create a TAR backup of the specified files."""
    archive_name = generate_backup_name(source_dir, 1, 'tar')
    archive_path = output_dir / archive_name

    # Ensure a unique archive name
    count = 1
    while archive_path.exists():
        count += 1
        archive_name = generate_backup_name(source_dir, count, 'tar')
        archive_path = output_dir / archive_name

    # Create TAR archive
    with tarfile.open(archive_path, 'w') as tar:
        for file in files_to_backup:
            for files in source_dir.rglob(f'*.{file}'):
                tar.add(files, arcname=files.relative_to(source_dir))

    print(f"Backup created: {archive_path}")
    return archive_path

def create_backup(source_dir: Path, output_dir: Path, extensions: list, archive_type: str) -> None:
    """Create a backup of all files in the specified directory."""
    if not source_dir.is_dir():
        print(f"Error: Source directory '{source_dir}' does not exist.")
        return

    output_dir.mkdir(parents=True, exist_ok=True)

    files_to_backup = {}
    for ext in extensions:
        files = list(source_dir.rglob(f'*.{ext}'))
        if files:
            files_to_backup[ext] = files

    if not files_to_backup:
        print("No files found to back up.")
        return

    archive_path = create_tar_backup(source_dir, output_dir, files_to_backup)

    if archive_type == 'zip':
        compress_to_zip(str(archive_path), str(output_dir))
    elif archive_type == 'gz':
        compress_to_gzip(str(archive_path), str(output_dir))
    elif archive_type == 'bz2':
        compress_to_bzip2(str(archive_path), str(output_dir))
    elif archive_type == 'xz':
        compress_to_xz(str(archive_path), str(output_dir))
    else:
        print("Unsupported archive type.")
        return

    archive_path.unlink()

def restore_backup(archive_path: Path, output_dir: Path, archive_type: str) -> None:
    """Restore files from a backup archive."""
    if not archive_path.is_file():
        print(f"Error: Archive '{archive_path}' does not exist.")
        return

    output_dir.mkdir(parents=True, exist_ok=True)
    print(f"Restoring from archive: {archive_path}")

    if archive_type == 'zip':
        decompress_zip(archive_path, output_dir)
    elif archive_type == 'gz':
        decompress_gzip(archive_path, output_dir)
    elif archive_type == 'bz2':
        decompress_bz2(archive_path, output_dir)
    elif archive_type == 'xz':
        decompress_xz(archive_path, output_dir)
    else:
        print("Unsupported archive type.")
        return

    tar_files = list(output_dir.glob("*.tar"))
    if not tar_files:
        print("No TAR files found for extraction.")
        return

    tar_filename = tar_files[0]
    with tarfile.open(tar_filename, 'r') as tar:
        tar.extractall(output_dir)
    tar_filename.unlink()

def main():
    operation = input("Operation [c]ompress/[d]ecompress: ").strip().lower()
    if operation not in ('c', 'd'):
        print("Invalid operation. Please enter 'c' for compress or 'd' for decompress.")
        return

    if operation == 'c':
        source_directory = Path(input("Source directory: ").strip())
        if not source_directory.is_dir():
            print(f"Error: Source directory '{source_directory}' does not exist.")
            return

        extensions = input("Files to process (separate by space): ").strip().split()
        if not extensions:
            print("Error: No file extensions provided.")
            return

        output_directory = Path(input("Output directory: ").strip())
        archive_type = input("Archive type (zip/gz/bz2/xz): ").strip().lower()
        if archive_type not in ('zip', 'gz', 'bz2', 'xz'):
            print("Invalid archive type. Please choose from 'zip', 'gz', 'bz2', or 'xz'.")
            return

        create_backup(source_directory, output_directory, extensions, archive_type)

    elif operation == 'd':
        archive = Path(input("Archive: ").strip())
        if not archive.is_file():
            print(f"Error: Archive '{archive}' does not exist.")
            return

        output_directory = Path(input("Output directory: ").strip())
        archive_type = archive.suffix[1:]  # Get the archive type from the file extension
        if archive_type not in ('zip', 'gz', 'bz2', 'xz'):
            print(f"Invalid archive type detected: '{archive.suffix}'.")
            return

        restore_backup(archive, output_directory, archive_type)

if __name__ == "__main__":
    main()
