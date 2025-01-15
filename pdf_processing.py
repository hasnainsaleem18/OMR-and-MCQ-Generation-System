from PyPDF2 import PdfReader
import os

def extract_text_from_pdf(file_path):
    #Extract text from a PDF file.

    # Check if the file exists
    if not os.path.isfile(file_path):
        raise FileNotFoundError(f"The file '{file_path}' was not found.")

    try:
        # Initialize the PDF reader
        pdf_reader = PdfReader(file_path)
        extracted_text = ""

        # Iterate through all pages to extract text
        for page in pdf_reader.pages:
            page_text = page.extract_text()
            if page_text:
                extracted_text += page_text  # Append text from the current page
            else:
                # Warn if no text is found on a page
                page_number = pdf_reader.pages.index(page) + 1
                print(f"Warning: No text found on page {page_number}")

        return extracted_text

    except PermissionError:
        # Handle permission errors
        print(f"Permission denied: Unable to read the file '{file_path}'. Please check the file permissions.")
    except Exception as exception:
        # Handle any other exceptions
        print(f"An unexpected error occurred while reading the PDF: {exception}")
