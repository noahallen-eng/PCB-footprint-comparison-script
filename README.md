# PCB Footprint Search
Searches a directory of .txt files in Gerber ZIP files for a user-specified part number and reports every match of each relevant project.

## Setup
Edit the following line if your Gerber archive is stored elsewhere:

```python
zip_directory = r"T:\GERBER"
```

## Usage
Run:

```bash
python PCB_footprint_search.py
```

Enter the part number when prompted.

The script searches every ZIP file in the directory and generates `search_results.txt` containing:

- Matching ZIP files
- Matching text files
- Line numbers
- Matching data

- GUI interface
- Support for additional BOM formats
- Faster indexed searching
- Search by package type
- Interactive search and filtering
