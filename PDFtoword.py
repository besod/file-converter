import os
from pdf2docx import Converter
from logger import setup_logger  # Reusing the existing logger setup
from dotenv import load_dotenv

# Setup logger for this script
logger = setup_logger("PDFtoWord")

# Load environment variables
load_dotenv()
FILE_FOLDER = os.getenv("FILE_FOLDER")

if not FILE_FOLDER:
    logger.error("❌ ERROR: FILE_FOLDER is not set in the .env file!")
    raise ValueError("❌ ERROR: FILE_FOLDER is not set in the .env file!")

def get_pdf_files():
    """Returns a list of .pdf files in the configured FILE_FOLDER."""
    try:
        return [f for f in os.listdir(FILE_FOLDER) if f.lower().endswith(".pdf")]
    except Exception as e:
        logger.error(f"Error accessing directory: {e}")
        return []

def convert_pdf_to_word(pdf_filename):
    """Converts a specific PDF file to DOCX."""
    input_path = os.path.join(FILE_FOLDER, pdf_filename)
    output_path = os.path.splitext(input_path)[0] + ".docx"

    try:
        cv = Converter(input_path)
        cv.convert(output_path, start=0, end=None)
        cv.close()
        logger.info(f"✅ Successfully converted: {pdf_filename} -> {output_path}")
        print(f"✅ Successfully converted: {pdf_filename} -> {output_path}")
    except Exception as e:
        logger.error(f"❌ Error converting {pdf_filename}: {e}")
        print(f"❌ Error converting {pdf_filename}: {e}")

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
        choice = int(input("\nEnter the number of the file to convert: ").strip())
        if 1 <= choice <= len(pdf_files):
            selected_file = pdf_files[choice - 1]
            convert_pdf_to_word(selected_file)
        else:
            print("❌ Invalid selection. Please enter a valid number.")
    except ValueError:
        print("❌ Invalid input. Please enter a number.")

if __name__ == "__main__":
    main()
