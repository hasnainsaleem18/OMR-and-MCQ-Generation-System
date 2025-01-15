from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
import pandas as pd

def save_mcqs_to_pdf(mcq_list, file_name):
    #Save a list of MCQs to a PDF file.

    try:
        # Check if the file name ends with .pdf
        if not file_name.endswith('.pdf'):
            raise ValueError("File name must end with .pdf")

        # Initialize the PDF canvas with A4 page size
        pdf = canvas.Canvas(file_name, pagesize=A4)
        pdf.setTitle("MCQs")  # Set the title of the PDF
        pdf.setFont("Helvetica", 12)  # Set the font style and size

        # Get the width and height of the A4 page
        page_width, page_height = A4

        # Define margins
        left_margin = 50
        right_margin = page_width - 50
        top_margin = page_height - 50
        bottom_margin = 50

        # Set initial x and y positions
        x_position = left_margin
        y_position = top_margin
        line_height = 15  # Line height for text spacing

        # Iterate through the MCQs
        for mcq in mcq_list:
            # Split the MCQ into lines (question, options, answer)
            lines = mcq.split("\n")

            for line in lines:
                # Handle text that exceeds the right margin
                if len(line) * 6 + x_position > right_margin:
                    # Split long text into two lines
                    split_index = int((right_margin - x_position) / 6)
                    first_part = line[:split_index]
                    second_part = line[split_index:]
                    pdf.drawString(x_position, y_position, first_part)
                    y_position -= line_height
                    pdf.drawString(x_position, y_position, second_part)
                else:
                    # Draw text if it fits within the margins
                    pdf.drawString(x_position, y_position, line)

                # Move to the next line
                y_position -= line_height

                # Add a new page if the text exceeds the bottom margin
                if y_position < bottom_margin:
                    pdf.showPage()
                    pdf.setFont("Helvetica", 12)  # Reset font for new page
                    y_position = top_margin

            # Add extra space between MCQs
            y_position -= line_height

            # Add a new page if the extra space exceeds the bottom margin
            if y_position < bottom_margin:
                pdf.showPage()
                pdf.setFont("Helvetica", 12)  # Reset font for new page
                y_position = top_margin

        pdf.save()

    except PermissionError:
        print(f"Permission denied: Unable to save the file '{file_name}'. Please check the file path and try again.")
    except FileNotFoundError:
        print(f"File not found: Please check the file path '{file_name}'.")
    except ValueError as value_error:
        print(f"Value error: {value_error}")
    except Exception as exception:
        print(f"An unexpected error occurred: {exception}")


def save_answers_to_csv(answer_data, file_name):
    #Save question numbers and answers to a CSV file.

    try:
        # Check if the input data is valid
        if not answer_data:
            raise ValueError("Answer data is empty. Cannot save to CSV.")

        # Create a DataFrame from the answer data
        data_frame = pd.DataFrame(answer_data, columns=["question_no", "answer"])

        # Save the DataFrame to a CSV file without the index
        data_frame.to_csv(file_name, index=False, encoding="utf-8")

    except Exception as exception:
        raise RuntimeError(f"Failed to save CSV file: {exception}")
