import os
from PyPDF2 import PdfMerger
from logger import setup_logger  # Custom logger
from dotenv import load_dotenv

# Setup logger for this script
pdf_logger = setup_logger("PDFcombiner")

# Load environment variables
load_dotenv()
FILE_FOLDER = os.getenv("FILE_FOLDER")

if not FILE_FOLDER:
    raise ValueError("❌ ERROR: FILE_FOLDER is not set in the .env file!")

def get_pdf_files():
    """Returns a list of .pdf files in the configured FILE_FOLDER."""
    try:
        return [f for f in os.listdir(FILE_FOLDER) if f.lower().endswith(".pdf")]
    except Exception as e:
        pdf_logger.error(f"Error accessing directory: {e}")
        return []

def combine_pdfs(pdf_list, output_path):
    """Combines multiple PDF files into a single PDF."""
    if not output_path.lower().endswith(".pdf"):
        output_path += ".pdf"
    
    merger = PdfMerger()
    try:
        for pdf in pdf_list:
            full_path = os.path.join(FILE_FOLDER, pdf)
            merger.append(full_path)
        output_full_path = os.path.join(FILE_FOLDER, output_path)
        merger.write(output_full_path)
        merger.close()
        pdf_logger.info(f"Successfully combined PDFs into {output_full_path}")
        print(f"✅ Successfully combined PDFs into {output_full_path}")
    except Exception as e:
        pdf_logger.error(f"Error combining PDFs: {e}")
        print(f"❌ Error combining PDFs: {e}")

def main():
    """Main function to list files and allow user selection."""
    pdf_files = get_pdf_files()

    if not pdf_files:
        print("⚠️ No PDF files found in the configured folder.")
        return

    print("\n📄 Available PDF files:")
    for i, file in enumerate(pdf_files, 1):
        print(f"{i}. {file}")

    try:
        choices = input("\nEnter the numbers of the files to combine in the desired order (e.g., 1 3 2): ").strip().split()
        selected_files = [pdf_files[int(choice) - 1] for choice in choices]
        output_name = input("Enter the name for the combined PDF (e.g., combined.pdf): ").strip()
        combine_pdfs(selected_files, output_name)
    except (ValueError, IndexError):
        print("❌ Invalid selection. Please enter valid numbers.")

if __name__ == "__main__":
    main()
