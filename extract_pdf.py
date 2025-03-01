import os
import logging
import shutil
import pdfplumber
import pandas as pd

# Configure logging to display the time, level and message.
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)


def extract_tables_from_pdf(pdf_path, password=None):
    """
    Extracts all tables from the PDF and returns a list of pandas DataFrames.
    """
    try:
        logging.info(f"Extracting tables from {os.path.basename(pdf_path)}.")

        # Open the PDF with password if provided
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
        logging.error(f"Error processing {os.path.basename(pdf_path)}: {e}")
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
    logging.info("Starting PDF table extraction process.")

    # Get password with visible input
    password = input("Enter PDF password (press Enter if none): ") or None

    # Define paths relative to the script's location
    base_dir = os.path.dirname(os.path.abspath(__file__))
    input_folder = os.path.join(base_dir, "input")
    output_folder = os.path.join(base_dir, "output")
    archive_folder = os.path.join(base_dir, "archive")

    # Ensure output and archive directories exist
    os.makedirs(output_folder, exist_ok=True)
    os.makedirs(archive_folder, exist_ok=True)

    # Process each PDF file in the input folder
    pdf_files = [f for f in os.listdir(input_folder) if f.lower().endswith(".pdf")]
    if not pdf_files:
        logging.info("No PDF files found in the input folder.")
    else:
        for filename in pdf_files:
            pdf_path = os.path.join(input_folder, filename)
            logging.info(f"Processing {filename}...")

            # Extract tables from the PDF
            tables = extract_tables_from_pdf(pdf_path, password)
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
