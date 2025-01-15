import tkinter as tk
from tkinter import filedialog
from pdf_processing import extract_text_from_pdf  # Function to extract text from a PDF
from mcq_generation import generate_mcqs_and_answers  # Function to generate MCQs and answers
from pdf_and_csv_output import save_mcqs_to_pdf, save_answers_to_csv  # Functions to save data to PDF and CSV
from omr_processing import process_main  # Function to process OMR sheets
import datetime
import pkg_resources


def generate_unique_filename():
    #Generate a unique filename using the current date and time.
    current_time = datetime.datetime.now().strftime("%Y_%m_%d-%H_%M_%S")  # Format the date and time
    return f"{current_time}"

def pdf_and_mcq_interface():
    #Open a window for uploading a PDF and specifying the number of MCQs.
    pdf_window = tk.Toplevel(root)  # Create a new top-level window
    pdf_window.title("Upload PDF and Specify MCQs")  # Set the title of the window
    pdf_window.geometry("400x400")  # Set the size of the window
    pdf_window.configure(bg="white")  # Set the background color of the window
    mcq_entry = tk.StringVar()  # Variable to store the number of MCQs entered by the user
    pdf_file_path = tk.StringVar()  # Variable to store the path of the uploaded PDF file

    def validate_mcq():
        #Check if the number of MCQs entered is valid.
        try:
            num_mcqs = int(mcq_entry.get())  # Get the entered number as an integer
            if 1 <= num_mcqs <= 30:  # Ensure the number is between 1 and 30
                upload_pdf_button.config(state="normal")  # Enable the upload button
                status_label.config(text="Valid MCQ number. Proceed to upload PDF.", fg="green")
            else:
                # If invalid, disable the upload and process buttons, and reset the file path
                upload_pdf_button.config(state="disabled")
                process_pdf_button.config(state="disabled")
                pdf_file_path.set("")
                status_label.config(text="MCQ number must be between 1 and 30.", fg="red")
        except ValueError:
            # Handle non-numeric input
            upload_pdf_button.config(state="disabled")
            process_pdf_button.config(state="disabled")
            pdf_file_path.set("")
            status_label.config(text="Invalid MCQ number. Enter a number between 1 and 30.", fg="red")

    def upload_pdf():
        #Open a file dialog to upload a PDF.
        file_path = filedialog.askopenfilename(filetypes=[("PDF Files", "*.pdf")])
        if file_path:
            pdf_file_path.set(file_path)
            status_label.config(text="PDF uploaded successfully.", fg="green")
            process_pdf_button.config(state="normal")
        else:
            # If no file is selected, reset the file path and disable the process button
            pdf_file_path.set("")
            process_pdf_button.config(state="disabled")
            status_label.config(text="PDF upload cancelled. Please upload again.", fg="red")

    def process_pdf():
        #Process the uploaded PDF and generate MCQs and answers.
        try:
            num_mcqs = int(mcq_entry.get())
            if not pdf_file_path.get():
                status_label.config(text="No PDF file uploaded!", fg="red")
                return

            text = extract_text_from_pdf(pdf_file_path.get())
            if not text:
                status_label.config(text="No text extracted from the PDF!", fg="red")
                return

            # Generate MCQs, answers, and a formatted question-answer list
            mcqs, answers, formatted_question_no_answer = generate_mcqs_and_answers(text, num_mcqs)
            if not mcqs or not answers:
                status_label.config(text="Failed to generate MCQs or answers!", fg="red")
                return

            # Generate unique filenames for the output files
            base_filename = generate_unique_filename()
            mcq_filename = f"PDF_questions_{base_filename}.pdf"
            answer_pdf_filename = f"PDF_answers_{base_filename}.pdf"
            answer_csv_filename = f"CSV_answers_{base_filename}.csv"

            # Save the MCQs, answers, and formatted question-answer list to files
            save_mcqs_to_pdf(mcqs, mcq_filename)
            save_mcqs_to_pdf(answers, answer_pdf_filename)
            save_answers_to_csv(formatted_question_no_answer, answer_csv_filename)

            # Update the status label to indicate success
            status_label.config(text="MCQs and Answer Sheet generated successfully!", fg="green")
        except Exception as e:
            # Handle any errors and update the status label
            status_label.config(text=f"An error occurred: {e}", fg="red")

    # UI elements for the PDF and MCQ interface
    mcq_label = tk.Label(pdf_window, text="Enter number of MCQs (1-30):", bg="white", font=("Helvetica", 12), fg="black")
    mcq_label.pack(pady=10)  # Add padding around the label

    mcq_entry_field = tk.Entry(pdf_window, textvariable=mcq_entry, font=("Helvetica", 12), justify="center", relief=tk.GROOVE, bd=1, width=10)
    mcq_entry_field.pack(pady=10)  # Add padding around the entry field
    mcq_entry_field.bind("<KeyRelease>", lambda e: validate_mcq())  # Validate input as the user types

    upload_pdf_button = tk.Button(pdf_window, text="Upload PDF", command=upload_pdf, bg="black", fg="white", font=("Helvetica", 12), padx=10, pady=5, state="disabled")
    upload_pdf_button.pack(pady=20)  # Add padding around the button

    process_pdf_button = tk.Button(pdf_window, text="Process PDF", command=process_pdf, bg="black", fg="white", font=("Helvetica", 12, "bold"), padx=10, pady=5, state="disabled")
    process_pdf_button.pack(pady=30)  # Add padding around the button

    status_label = tk.Label(pdf_window, text="", bg="white", font=("Helvetica", 10), fg="black")
    status_label.pack(pady=20)  # Add padding around the label


def open_omr_interface():
    #Open a window for processing OMR sheets.
    omr_window = tk.Toplevel(root)
    omr_window.title("Process OMR")
    omr_window.geometry("400x400")
    omr_window.configure(bg="white")

    def process_folder():
        # Process a folder containing both images and answer CSV files.
        folder_path = filedialog.askdirectory(title="Select Folder Containing Images and CSVs")
        if folder_path:
            try:
                process_main(folder_path, None, process_mode="multiple")
                status_label.config(text="Folder processing completed successfully.", fg="green")
            except ValueError as ve:
                status_label.config(text=f"Error: {ve}", fg="red")
            except Exception as e:
                status_label.config(text=f"Unexpected error: {e}", fg="red")
        else:
            status_label.config(text="No folder selected! Please try again.", fg="red")

    def process_file_interface():
        # Open the interface for processing individual OMR sheets and CSV files.
        file_window = tk.Toplevel(omr_window)
        file_window.title("Upload Files")
        file_window.geometry("400x400")
        file_window.configure(bg="white")

        omr_file_path = tk.StringVar()
        csv_file_path = tk.StringVar()

        def upload_omr_sheet():
            # Upload the OMR sheet image file.
            file_path = filedialog.askopenfilename(filetypes=[("Image Files", "*.png")], title="Select OMR Sheet Image")
            if file_path:
                omr_file_path.set(file_path)
                omr_status_label.config(text="OMR file uploaded successfully.", fg="green")
                csv_button.config(state="normal")
            else:
                omr_file_path.set("")
                csv_button.config(state="disabled")
                process_button.config(state="disabled")
                omr_status_label.config(text="OMR upload cancelled. Please upload again.", fg="red")

        def upload_csv_file():
            # Upload the answer CSV file.
            if not omr_file_path.get():
                omr_status_label.config(text="Upload OMR sheet first!", fg="red")
                return
            file_path = filedialog.askopenfilename(filetypes=[("CSV Files", "*.csv")], title="Select Answer CSV File")
            if file_path:
                csv_file_path.set(file_path)
                omr_status_label.config(text="CSV file uploaded successfully.", fg="green")
                process_button.config(state="normal")
            else:
                csv_file_path.set("")
                process_button.config(state="disabled")
                omr_status_label.config(text="CSV upload cancelled. Please upload again.", fg="red")

        def process_file():
            # Process the uploaded OMR sheet and CSV file.
            if not omr_file_path.get() or not csv_file_path.get():
                omr_status_label.config(text="Ensure both OMR and CSV files are uploaded!", fg="red")
                return
            try:
                process_main(omr_file_path.get(), csv_file_path.get(), process_mode="single")
                omr_status_label.config(text="OMR processing completed successfully!", fg="green")
            except Exception as e:
                omr_status_label.config(text=f"Error during processing: {e}", fg="red")

        tk.Button(file_window, text="Upload OMR Sheet", command=upload_omr_sheet, bg="black", fg="white", font=("Helvetica", 12), padx=10, pady=5).pack(pady=10)

        csv_button = tk.Button(file_window, text="Upload CSV", command=upload_csv_file, bg="black", fg="white", font=("Helvetica", 12), padx=10, pady=5, state="disabled")
        csv_button.pack(pady=10)

        process_button = tk.Button(file_window, text="Process", command=process_file, bg="black", fg="white", font=("Helvetica", 12, "bold"), padx=10, pady=5, state="disabled")
        process_button.pack(pady=10)

        omr_status_label = tk.Label(file_window, text="", bg="white", font=("Helvetica", 10), fg="black")
        omr_status_label.pack(pady=20)

    # Add buttons for folder and file processing in the OMR interface
    tk.Button(omr_window, text="Process Folder", command=process_folder, bg="black", fg="white", font=("Helvetica", 12),padx=10, pady=5).pack(pady=20)
    tk.Button(omr_window, text="Process File", command=process_file_interface, bg="black", fg="white", font=("Helvetica", 12), padx=10, pady=5).pack(pady=10)

    # Label to display general status updates
    status_label = tk.Label(omr_window, text="", bg="white", font=("Helvetica", 10), fg="black")
    status_label.pack(pady=20)


# Main Application Window
root = tk.Tk()
root.title("OMR by Nerds🤓")  # Title of the main application window
root.geometry("500x500")  # Set the size of the main window
root.configure(bg="white")  # Set the background color

# Header for the application
tk.Label(root, text="OMR and PDF Processor", bg="white", font=("Helvetica", 16, "bold"), fg="black").pack(pady=20)

# Button to open the PDF upload and MCQ specification interface
tk.Button(
    root,
    text="Upload PDF & Specify MCQs",
    command=pdf_and_mcq_interface,
    bg="black",
    fg="white",
    font=("Helvetica", 14),
    padx=20,
    pady=10
).pack(pady=10)

# Button to open the OMR processing interface
tk.Button(
    root,
    text="Process OMR",
    command=open_omr_interface,
    bg="black",
    fg="white",
    font=("Helvetica", 14),
    padx=20,
    pady=10
).pack(pady=10)

# Run the Tkinter event loop to keep the application running
root.mainloop()