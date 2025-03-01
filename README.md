# PDF Table Extractor

This tool automatically extracts tables from PDF files and saves them as CSV files. It's designed to be easy to use for both technical and non-technical users.

## Features

- Extracts all tables from PDF files
- Supports password-protected PDFs
- Automatically converts tables to CSV format
- Organizes processed files by moving them to an archive folder
- Works on both Windows and macOS

## Prerequisites

1. Install Python (3.7 or newer):

   - **Windows**: Download and install from [python.org](https://www.python.org/downloads/)
   - **macOS**: Download and install from [python.org](https://www.python.org/downloads/)

   During installation:

   - ✅ Make sure to check "Add Python to PATH" (Windows)
   - ✅ Click "Install for all users"

2. Install pip (Python package manager):
   - It usually comes with Python installation
   - To verify, open Terminal (macOS) or Command Prompt (Windows) and type:
     ```
     pip --version
     ```

## Installation

1. Download or clone this repository to your computer

2. Open Terminal (macOS) or Command Prompt (Windows)

3. Navigate to the project folder:

   ```
   cd path/to/extract-pdf
   ```

4. Install required packages:
   ```
   pip install -r requirements.txt
   ```

## Usage

1. Create the following folders in the project directory (if they don't exist):

   - `input` - Place your PDF files here
   - `output` - Extracted CSV files will appear here
   - `archive` - Processed PDF files will be moved here

2. Place your PDF files in the `input` folder

3. Run the script:

   - **Windows**:
     ```
     python extract_pdf.py
     ```
   - **macOS**:
     ```
     python3 extract_pdf.py
     ```

4. If your PDF is password-protected:

   - Enter the password when prompted
   - Press Enter if no password is required

5. Check the `output` folder for your extracted CSV files
   - Each table will be saved as a separate CSV file
   - Files are named as: `original_pdf_name_table_1.csv`, `original_pdf_name_table_2.csv`, etc.

## Folder Structure

```
extract-pdf/
│
├── input/          # Place PDF files here
├── output/         # Extracted CSV files appear here
├── archive/        # Processed PDFs are moved here
├── extract_pdf.py  # Main script
└── README.md       # This file
```

## Troubleshooting

1. **"Python not found" error**:

   - Make sure Python is installed
   - Verify Python is in your system's PATH
   - Try using `python3` instead of `python` on macOS

2. **"Module not found" error**:

   - Run `pip install -r requirements.txt` again
   - Try using `pip3` instead of `pip` on macOS

3. **No tables extracted**:
   - Verify your PDF actually contains tables
   - Check if the PDF is corrupted
   - Ensure you entered the correct password (if required)

## Notes

- The script will process all PDF files in the input folder
- Processed PDFs are automatically moved to the archive folder
- The script creates log messages to help track the extraction process
- Each table from the PDF is saved as a separate CSV file

## Support

If you encounter any issues:

1. Check the console output for error messages
2. Verify all prerequisites are correctly installed
3. Ensure you have proper permissions to read/write in the project folders
