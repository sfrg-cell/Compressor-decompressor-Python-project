import tarfile

def create_backup(source_dir, output_file):
    # Open a tarfile for writing with xz compression
    with tarfile.open(output_file, "w:xz") as tar:
        # Add the entire source directory to the archive
        tar.add(source_dir)
    # Print confirmation message once backup is created
    print(f"Backup created: {output_file}")

if __name__ == "__main__":
    # Ask the user for the directory to back up
    source_directory = input("Source directory: ")
    # Ask the user for the name and location of the output file
    output_file = input("Output file (e.g., backup.tar.xz): ")

    # Call the function to create the backup
    create_backup(source_directory, output_file)
