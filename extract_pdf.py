import os
import csv
import shutil
import getpass
from PyPDF2 import PdfReader

def run_terminal_command():
    # Run a terminal command. Change the command as needed.
    os.system("echo Starting PDF extraction process...")

def extract_text_from_pdf(pdf_path, password):
    """Extracts text from each page of the PDF. Returns a list of rows for the CSV."""
    rows = []
    try:
        with open(pdf_path, "rb") as file:
            reader = PdfReader(file)
            if reader.is_encrypted:
                try:
                    reader.decrypt(password)
                except Exception as e:
                    print(f"Failed to decrypt {os.path.basename(pdf_path)}: {e}")
                    return None

            # Extract text page by page
            for page_num, page in enumerate(reader.pages):
                text = page.extract_text() or ""
                rows.append([f"Page {page_num + 1}", text])
    except Exception as e:
        print(f"Error processing {os.path.basename(pdf_path)}: {e}")
        return None

    return rows

def save_to_csv(data, output_csv_path):
    """Saves extracted data to a CSV file."""
    try:
        with open(output_csv_path, "w", newline="", encoding="utf-8") as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(["Page", "Content"])
            writer.writerows(data)
        print(f"Extracted text saved to {os.path.basename(output_csv_path)}")
    except Exception as e:
        print(f"Error writing CSV file {os.path.basename(output_csv_path)}: {e}")

def move_to_archive(file_path, archive_folder):
    """Moves the processed PDF to the archive folder."""
    try:
        shutil.move(file_path, os.path.join(archive_folder, os.path.basename(file_path)))
        print(f"Moved {os.path.basename(file_path)} to archive.")
    except Exception as e:
        print(f"Error moving {os.path.basename(file_path)} to archive: {e}")

def main():
    run_terminal_command()

    # Prompt the user for the PDF password.
    password = getpass.getpass("Enter PDF password: ")

    # Define paths relative to the script's location.
    base_dir = os.path.dirname(os.path.abspath(__file__))
    input_folder = os.path.join(base_dir, "input")
    output_folder = os.path.join(base_dir, "output")
    archive_folder = os.path.join(base_dir, "archive")

    # Ensure output and archive directories exist.
    os.makedirs(output_folder, exist_ok=True)
    os.makedirs(archive_folder, exist_ok=True)

    # Process each PDF file in the input folder.
    for filename in os.listdir(input_folder):
        if filename.lower().endswith(".pdf"):
            pdf_path = os.path.join(input_folder, filename)
            print(f"Processing {filename}...")

            # Extract text from the PDF.
            extracted_data = extract_text_from_pdf(pdf_path, password)
            if extracted_data is None:
                print(f"Skipping {filename} due to errors.")
                continue

            # Prepare the CSV file path.
            base_name = os.path.splitext(filename)[0]
            output_csv_path = os.path.join(output_folder, f"{base_name}_extracted.csv")

            # Save the extracted data to CSV.
            save_to_csv(extracted_data, output_csv_path)

            # Move the processed PDF to the archive folder.
            move_to_archive(pdf_path, archive_folder)

if __name__ == "__main__":
    main()
