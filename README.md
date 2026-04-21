# Archive and Backup Tool

A Python utility for creating and restoring backups using various compression formats. This project was developed during the first year of university to practice modular programming and file system operations.

## Description

The tool allows users to aggregate specific files into TAR archives and then compress them using multiple algorithms. It also supports standalone compression and decompression of individual files.

## Project Structure

* **backup.py**: The main entry point. Orchestrates the creation of TAR-based backups and handles the restoration process.
* **compress.py**: Contains logic for compressing files into ZIP, GZIP, BZIP2, and XZ formats.
* **decompress.py**: Contains logic for extracting data from ZIP, GZIP, BZIP2, and XZ archives.

## Features

- Multi-format support: ZIP, GZIP (.gz), BZIP2 (.bz2), and XZ (.xz).
- Recursive file searching by extension for automated backups.
- Unique filename generation with timestamps to prevent accidental overwrites.
- Interactive CLI for selecting operations and archive types.

## Installation

Clone the repository:
```bash
git clone https://github.com/sfrg-cell/Compressor-decompressor-Python-project.git
```

## Usage

### Creating/Restoring Backups
Run the backup script to start the interactive wizard:
```bash
python backup.py
```
You will be prompted to choose between compression or decompression, specify directories, and select the archive format.

### Standalone Compression
To compress a single file directly:
```bash
python compress.py
```

### Standalone Decompression
To decompress an archive directly:
```bash
python decompress.py
```

## Technologies

- Python 3.x
- Standard libraries: `tarfile`, `zipfile`, `gzip`, `bz2`, `lzma`, `pathlib`
