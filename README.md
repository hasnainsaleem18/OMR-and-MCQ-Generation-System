# OMR and MCQ Generation System

## Table of Contents
- [OMR and MCQ Generation System](#omr-and-mcq-generation-system)
  - [Table of Contents](#table-of-contents)
  - [Overview](#overview)
  - [Features](#features)
    - [MCQ Generation](#mcq-generation)
    - [OMR Sheet Processing](#omr-sheet-processing)
  - [Workflow](#workflow)
    - [MCQ Generation Workflow](#mcq-generation-workflow)
    - [OMR Sheet Processing Workflow](#omr-sheet-processing-workflow)
  - [Technologies Used](#technologies-used)
  - [Screenshots/Diagrams](#screenshotsdiagrams)
    - [MAIN OMR SHEET](#main-omr-sheet)
    - [Step 1: Main Dashboard](#step-1-main-dashboard)
    - [Step 2: Upload PDF and Specify MCQs](#step-2-upload-pdf-and-specify-mcqs)
    - [Step 3: Process OMR Sheets](#step-3-process-omr-sheets)
    - [Step 4: Upload OMR and Answer Key](#step-4-upload-omr-and-answer-key)
    - [Step 5: Convert OMR Sheet to Grayscale](#step-5-convert-omr-sheet-to-grayscale)
    - [Step 6: Scan OMR Sheet in Parts](#step-6-scan-omr-sheet-in-parts)
    - [Step 7: Threshold Image for Roll Number](#step-7-threshold-image-for-roll-number)
    - [Step 8: Highlight Filled Circles](#step-8-highlight-filled-circles)
    - [Step 9: Process MCQs 1–10](#step-9-process-mcqs-110)
    - [Steps 10–13: Process Remaining MCQs](#steps-1013-process-remaining-mcqs)
  - [Contributions](#contributions)

## Overview
This project is a dual-functionality system designed to streamline two essential tasks:

1. **MCQ Generation**: Extracts multiple-choice questions (MCQs), with the number specified by user input, from a PDF file using the GROQ API. The system generates a PDF and CSV file containing the questions along with their solutions.
2. **OMR Sheet Processing**: Scans Optical Mark Recognition (OMR) sheets (single or batch) and evaluates them against a CSV file containing the correct answers. The results are outputted as a checked CSV file.

Both functionalities leverage tools like OpenCV for image processing and are integrated into a user-friendly workflow.

## Features

### MCQ Generation
- Uploads a PDF file for processing.
- Generates MCQs with solutions in both PDF and CSV formats.

### OMR Sheet Processing
- Processes individual OMR sheets or entire folders.
- Matches responses with the provided answer key.
- Outputs results as a CSV file of checked answers.

## Workflow

### MCQ Generation Workflow
1. User uploads a PDF file.
2. The system extracts questions and their solutions using the GROQ API, with the number of MCQs specified by the user.
3. Outputs a separate PDF file containing MCQs and their answers, along with a CSV file of answers that includes properly labeled columns and rows.

### OMR Sheet Processing Workflow
1. User uploads an OMR sheet or a folder of sheets along with the answer key in CSV format.
2. The system:
   - Preprocesses the OMR sheet using OpenCV.
   - Detects filled circles to determine answers.
   - Compares detected answers with the provided key.
3. Outputs a CSV file containing the results.

## Technologies Used
- **Python**: Core programming language.
- **OpenCV**: Image processing for OMR sheets.
- **GROQ API**: For extracting MCQs from PDFs.
- **NumPy**: For numerical operations.
- **Pandas**: For handling CSV data.
- **Matplotlib**: For plotting and visualization.
- **Tkinter**: For GUI file selection dialogs.
- **PyPDF2**: For reading and handling PDF files.
- **ReportLab**: For generating PDF files.

## Screenshots/Diagrams

### MAIN OMR SHEET
(omr_sheet.pdf)

### Step 1: Main Dashboard
The main dashboard provides two options:
- Upload a PDF to specify the number of MCQs via the GROQ API.
- Process OMR sheets.

!(images/1.png)

### Step 2: Upload PDF and Specify MCQs
If the user selects the first option:
1. They upload a PDF file.
2. Specify the number of MCQs to be generated.
3. Click "Process PDF" to generate:
   - A PDF file containing MCQs and answers.
   - A CSV file with answers for OMR checking.

(images/2.png)

### Step 3: Process OMR Sheets
If the user selects the second option, they see:
1. An option to process a bundle of OMR sheets.
2. An option to scan a single OMR sheet (steps remain the same for both).

(images/3.png)

### Step 4: Upload OMR and Answer Key
1. Upload a scanned OMR sheet.
(images/4.png)
2. Upload a CSV file containing answers.
3. Click "Process" to start execution.
(images/5.png)

### Step 5: Convert OMR Sheet to Grayscale
The system converts the entire OMR sheet to a grayscale image for processing.

(images/6.png)

### Step 6: Scan OMR Sheet in Parts
The sheet is divided into sections for scanning:
- Roll number section.
- MCQs 1–10.
- MCQs 11–20.
- MCQs 21–30.
This method ensures 100% success in recognition.

### Step 7: Threshold Image for Roll Number
The roll number section is converted to a threshold image for clarity.

(images/7.png)
(images/8.png)

### Step 8: Highlight Filled Circles
The grid is created, highlighting filled circles for answers.

(images/9.png)
(images/10.png)

### Step 9: Process MCQs 1–10
1. Convert the section to a binary image.
   (images/11.png)
   (images/12.png)
2. Detect contours.
   (images/13.png)
3. Highlight filled circles.
   (images/14.png)



### Steps 10–13: Process Remaining MCQs
Steps are repeated for:
- MCQs 11–20.
- MCQs 21–30.
Each section undergoes the same binary conversion, contour detection, and highlighting process.

(images/15.png)
(images/16.png)
(images/17.png)
(images/18.png)
(images/19.png)
(images/20.png)
(images/21.png)
(images/22.png)
(images/23.png)

## Contributions
Contributions are welcome! Please submit a pull request or create an issue for suggestions and improvements.


