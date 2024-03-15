# File Search and Archive Script

This Python script facilitates the search and archival of specific files within directories. It provides functionality to search for files listed in `listFile.txt` within directories specified in `listPath.txt` and copies them to a destination directory.

## Usage

1. **Setup Lists**: Ensure `listFile.txt` contains the filenames to search for, and `listPath.txt` contains the directories to search within.
2. **Run Script**: Execute the script, providing a directory path where the matching files will be archived:

```bash
python search_and_archive.py /path/to/destination/directory

