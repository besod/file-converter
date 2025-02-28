import os
import logging
import comtypes.client
from dotenv import load_dotenv

#  Load environment variables from .env file
load_dotenv()

# Get the folder path from the environment variable
WORD_FOLDER = os.getenv("WORD_FOLDER")

if not WORD_FOLDER:
    raise ValueError("❌ ERROR: WORD_FOLDER is not set in the .env file!")

# Setup logging 
logging.basicConfig(
    filename="wordtoPDF.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)


def get_word_files():
    """Returns a list of .docx and .doc files in the configured WORD_FOLDER."""
    try:
        return [f for f in os.listdir(WORD_FOLDER) if f.lower().endswith((".docx", ".doc"))]
    except Exception as e:
        logging.error(f"Error accessing directory: {e}")
        return []


def is_valid_filename(filename):
    """Validates the filename to prevent path traversal attacks."""
    return filename in get_word_files()


def convert_word_to_pdf(filename):
    """Converts a specific DOCX or DOC file to PDF."""
    input_path = os.path.join(WORD_FOLDER, filename)
    output_path = os.path.splitext(input_path)[0] + ".pdf"

    if not is_valid_filename(filename):
        logging.warning(f"Security alert: Attempted invalid file access - {filename}")
        print("❌ Invalid file selection.")
        return None

    try:
        word = comtypes.client.CreateObject("Word.Application")
        word.Visible = False  # Run in the background

        doc = word.Documents.Open(input_path)
        doc.SaveAs(output_path, FileFormat=17)  # 17 = PDF format
        doc.Close()
        word.Quit()

        logging.info(f"✅ Successfully converted: {filename} -> {output_path}")
        print(f"✅ Conversion successful: {output_path}")
        return output_path

    except comtypes.COMError as e:
        logging.error(f"Word COM error: {e}")
    except Exception as e:
        logging.error(f"❌ Unexpected error: {e}")
    finally:
        try:
            word.Quit()
        except:
            pass


def main():
    """Main function to list files and allow user selection."""
    word_files = get_word_files()

    if not word_files:
        print("⚠️ No Word files (.docx/.doc) found in the folder.")
        return

    print("\n📄 Available Word files:")
    for i, file in enumerate(word_files, 1):
        print(f"{i}. {file}")

    try:
        choice = int(input("\nEnter the number of the file to convert: ").strip())
        if 1 <= choice <= len(word_files):
            selected_file = word_files[choice - 1]
            convert_word_to_pdf(selected_file)
        else:
            print("❌ Invalid selection. Please enter a valid number.")
    except ValueError:
        print("❌ Invalid input. Please enter a number.")


if __name__ == "__main__":
    main()
