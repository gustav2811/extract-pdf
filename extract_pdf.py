import os
import logging
import shutil
import pdfplumber
import pandas as pd
import traceback
import sys
from pdfminer.pdfdocument import PDFPasswordIncorrect

# Configure logging to display the time, level and message.
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)


def get_password_if_needed(pdf_path):
    """
    Check if a PDF is password-protected and get the password if needed.
    Returns None if no password is required.
    """
    # First try without any password
    try:
        with pdfplumber.open(pdf_path, password="") as pdf:
            return None
    except PDFPasswordIncorrect:
        # If we get here, the PDF is password-protected
        logging.info(f"{os.path.basename(pdf_path)} is password-protected.")
        while True:
            password = input(f"Enter password for {os.path.basename(pdf_path)}: ")
            try:
                # Test if the password works
                with pdfplumber.open(pdf_path, password=password):
                    return password
            except PDFPasswordIncorrect:
                print("Incorrect password. Please try again.")
    except Exception as e:
        # Handle other exceptions
        logging.error(f"Error in get_password_if_needed: {str(e)}")
        logging.error(f"Traceback: {traceback.format_exc()}")
        raise


def extract_tables_from_pdf(pdf_path):
    """
    Extracts all tables from the PDF and returns a list of pandas DataFrames.
    """
    try:
        if not os.path.exists(pdf_path):
            logging.error(f"File not found: {pdf_path}")
            return None

        logging.info(f"Extracting tables from {os.path.basename(pdf_path)}.")

        # Get password if needed
        password = get_password_if_needed(pdf_path)

        # Open the PDF with password (if any)
        with pdfplumber.open(pdf_path, password=password) as pdf:
            all_tables = []

            # Extract tables from each page
            for page in pdf.pages:
                tables = page.extract_tables()
                if tables:
                    # Convert each table to a pandas DataFrame
                    for table in tables:
                        # Remove empty rows and columns
                        table = [[cell or "" for cell in row] for row in table]
                        # Get header from first row
                        header = table[0]
                        # Convert to DataFrame
                        df = pd.DataFrame(table[1:], columns=header)
                        all_tables.append(df)

            if not all_tables:
                logging.warning(f"No tables found in {os.path.basename(pdf_path)}.")
                return None

            logging.info(
                f"Found {len(all_tables)} tables in {os.path.basename(pdf_path)}."
            )
            return all_tables

    except Exception as e:
        logging.error(f"Error processing {os.path.basename(pdf_path)}: {str(e)}")
        logging.error(f"Traceback: {traceback.format_exc()}")
        return None


def save_tables_to_csv(tables, base_name, output_folder):
    """
    Saves each extracted table to a separate CSV file.
    """
    try:
        for i, table in enumerate(tables, 1):
            output_csv_path = os.path.join(output_folder, f"{base_name}_table_{i}.csv")
            table.to_csv(output_csv_path, index=False)
            logging.info(f"Table {i} saved to {os.path.basename(output_csv_path)}.")
    except Exception as e:
        logging.error(f"Error writing CSV files for {base_name}: {e}")


def move_to_archive(file_path, archive_folder):
    """
    Moves the processed PDF to the archive folder.
    """
    try:
        shutil.move(
            file_path, os.path.join(archive_folder, os.path.basename(file_path))
        )
        logging.info(f"Moved {os.path.basename(file_path)} to archive.")
    except Exception as e:
        logging.error(f"Error moving {os.path.basename(file_path)} to archive: {e}")


def main():
    # Show startup message
    print("Welcome!\n")
    print("IMPORTANT: Please read the instructions in 'Instructions.pdf' before using this tool.\n")
    print("Press Enter to continue...")
    input()  # Wait for user to press Enter

    logging.info("Starting PDF table extraction process.")

    # Determine base directory
    if getattr(sys, "frozen", False):
        # Running as PyInstaller executable
        base_dir = os.path.dirname(sys.executable)
    else:
        # Running as normal Python script
        base_dir = os.path.dirname(os.path.abspath(__file__))


    # Define paths relative to the script's location
    input_folder = os.path.join(base_dir, "input")
    output_folder = os.path.join(base_dir, "output")
    archive_folder = os.path.join(base_dir, "archive")

    # Ensure folders exist
    os.makedirs(input_folder, exist_ok=True)
    os.makedirs(output_folder, exist_ok=True)
    os.makedirs(archive_folder, exist_ok=True)

    # Process each PDF file in the input folder
    pdf_files = [f for f in os.listdir(input_folder) if f.lower().endswith(".pdf")]
    if not pdf_files:
        logging.info("No PDF files found in the input folder.")
        return

    for filename in pdf_files:
        pdf_path = os.path.join(input_folder, filename)
        logging.info(f"Processing {filename}...")

        # Extract tables from the PDF
        tables = extract_tables_from_pdf(pdf_path)
        if tables is None:
            logging.error(f"Skipping {filename} due to errors.")
            continue

        # Save the extracted tables to CSV files
        base_name = os.path.splitext(filename)[0]
        save_tables_to_csv(tables, base_name, output_folder)

        # Move the processed PDF to the archive folder
        move_to_archive(pdf_path, archive_folder)

    logging.info("PDF table extraction process completed.")


if __name__ == "__main__":
    main()

input("\nProcessing complete. Press Enter to close the program...")