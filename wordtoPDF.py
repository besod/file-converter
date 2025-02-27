import os
import comtypes.client

# Define the folder containing the Word files
WORD_FOLDER = r"D:\example folder\word_files"

def convert_docx_to_pdf(filename):
    """
    Converts a specific DOCX file to PDF.

    Parameters:
        filename (str): The name of the DOCX file (without the full path).
    
    Returns:
        str: The path of the generated PDF file if successful, otherwise None.
    """
    input_path = os.path.join(WORD_FOLDER, filename)

    if not os.path.exists(input_path):
        print(f"Error: The file '{filename}' does not exist in '{WORD_FOLDER}'.")
        return None

    if not filename.lower().endswith(".docx"):
        print("Error: The specified file is not a DOCX file.")
        return None

    # Define output PDF path (same folder, same name but with .pdf extension)
    output_path = os.path.splitext(input_path)[0] + ".pdf"

    try:
        # Open Word application
        word = comtypes.client.CreateObject("Word.Application")
        word.Visible = False  # Run in the background

        # Open the document and save it as PDF
        doc = word.Documents.Open(input_path)
        doc.SaveAs(output_path, FileFormat=17)  # 17 corresponds to PDF format
        doc.Close()
        word.Quit()

        print(f"✅ Conversion successful: {output_path}")
        return output_path
    except Exception as e:
        print(f"❌ Error during conversion: {e}")
        return None

if __name__ == "__main__":
    # List all DOCX files in the folder
    docx_files = [f for f in os.listdir(WORD_FOLDER) if f.lower().endswith(".docx")]

    if not docx_files:
        print("No DOCX files found in the folder.")
    else:
        print("\nAvailable DOCX files:")
        for i, file in enumerate(docx_files, 1):
            print(f"{i}. {file}")

        # Ask user to select a file
        choice = input("\nEnter the number of the file you want to convert: ").strip()
        
        if choice.isdigit():
            choice = int(choice)
            if 1 <= choice <= len(docx_files):
                selected_file = docx_files[choice - 1]
                convert_docx_to_pdf(selected_file)
            else:
                print("Invalid selection. Please enter a valid number.")
        else:
            print("Invalid input. Please enter a number.")
