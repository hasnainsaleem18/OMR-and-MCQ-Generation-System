import cv2
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime
import os

# Setup image and thresholding
def setup_image_and_threshold_basic(image_path, green_box_coordinates):
    #Load the image, crop the green box, and apply basic thresholding.
    image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    show_image("Grayscale Image", image)
    x1, y1, x2, y2 = green_box_coordinates
    green_box_image = image[y1:y2, x1:x2]
    show_image("Cropped Green Box", green_box_image)
    _, thresholded_green_box = cv2.threshold(green_box_image, 110, 255, cv2.THRESH_BINARY_INV)
    show_image("Thresholded Image", thresholded_green_box)
    return green_box_image, thresholded_green_box

def setup_image_and_threshold_advanced(image_path, green_box_coordinates):
    #Load the image, crop the green box, and apply advanced thresholding.
    image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    show_image("Grayscale Image", image)
    x1, y1, x2, y2 = green_box_coordinates
    green_box_image = image[y1:y2, x1:x2]
    show_image("Cropped Green Box", green_box_image)
    _, thresholded_green_box = cv2.threshold(green_box_image, 127, 255, cv2.THRESH_BINARY_INV)
    show_image("Thresholded Image", thresholded_green_box)
    return green_box_image, thresholded_green_box

# Detect filled circles
def detect_filled_circles_basic(thresholded_image, min_area=35, max_area=100, min_radius=0.5, max_radius=10):
    #Detect filled circles using basic parameters.
    contours, _ = cv2.findContours(thresholded_image, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    show_image("Contours Detected", cv2.cvtColor(cv2.cvtColor(thresholded_image, cv2.COLOR_GRAY2BGR), cv2.COLOR_BGR2RGB), cmap=None)
    filled_circles = []
    for contour in contours:
        area = cv2.contourArea(contour)
        if min_area < area < max_area:
            ((x, y), radius) = cv2.minEnclosingCircle(contour)
            if min_radius < radius < max_radius:
                filled_circles.append((int(x), int(y), int(radius)))
    return filled_circles

def detect_filled_circles_advanced(thresholded_image, min_area=20, max_area=800, min_radius=3, max_radius=20):
    #Detect filled circles using advanced parameters.
    contours, _ = cv2.findContours(thresholded_image, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    contour_debug_image = cv2.cvtColor(thresholded_image, cv2.COLOR_GRAY2BGR)
    cv2.drawContours(contour_debug_image, contours, -1, (0, 255, 0), 1)
    show_image("Contours Detected", cv2.cvtColor(contour_debug_image, cv2.COLOR_BGR2RGB), cmap=None)
    filled_circles = []
    for contour in contours:
        area = cv2.contourArea(contour)
        if min_area < area < max_area:
            ((x, y), radius) = cv2.minEnclosingCircle(contour)
            if min_radius < radius < max_radius:
                filled_circles.append((int(x), int(y), int(radius)))
    return filled_circles

def highlight_circles_and_grid(image, circles, column_x_coordinates, row_y_coordinates, row_labels, color=(0, 255, 0),line_thickness=1, circle_color=(0, 0, 255), circle_thickness=2):
    #Highlight circles and overlay grid on the image.
    image_with_grid = cv2.cvtColor(image, cv2.COLOR_GRAY2BGR)
    for x in column_x_coordinates:
        cv2.line(image_with_grid, (x, 0), (x, image_with_grid.shape[0]), color, line_thickness)
    for y in row_y_coordinates:
        cv2.line(image_with_grid, (0, y), (image_with_grid.shape[1], y), color, line_thickness)
    for (x, y, r) in circles:
        cv2.circle(image_with_grid, (x, y), r, circle_color, circle_thickness)
    for row_y, label in zip(row_y_coordinates, row_labels):
        cv2.putText(image_with_grid, str(label), (10, row_y), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 1, cv2.LINE_AA)
    show_image("Grid with Circles Highlighted", cv2.cvtColor(image_with_grid, cv2.COLOR_BGR2RGB), cmap=None)
    return image_with_grid

# Highlight circles for MCQs
def highlight_mcq_circles(image, black_circles, all_circles, column_ranges, total_rows=10, color=(0, 255, 0),thickness=2):
    # Convert the grayscale image to BGR for visualization
    image_with_highlight = cv2.cvtColor(image, cv2.COLOR_GRAY2BGR)

    # Sort circles by their y-coordinates
    all_circles_sorted = sorted(all_circles, key=lambda x: x[1])
    row_height = (all_circles_sorted[-1][1] - all_circles_sorted[0][1]) / total_rows

    # Define row boundaries
    row_boundaries = [
        (int(all_circles_sorted[0][1] + i * row_height), int(all_circles_sorted[0][1] + (i + 1) * row_height))
        for i in range(total_rows)
    ]

    # Highlight circles
    for y_start, y_end in row_boundaries:
        for circle in black_circles:
            if y_start <= circle[1] <= y_end:
                cv2.circle(image_with_highlight, (circle[0], circle[1]), circle[2], color, thickness)

    show_image("MCQ Circles Highlighted", cv2.cvtColor(image_with_highlight, cv2.COLOR_BGR2RGB))
    return image_with_highlight

def analyze_all_columns_with_visualization(image, black_filled_circles, column_x_coordinates, row_y_coordinates, row_labels):
    roll_number = []
    for col_index in range(len(column_x_coordinates) - 1):
        column_start = column_x_coordinates[col_index]
        column_end = column_x_coordinates[col_index + 1]
        if col_index == 2:
            roll_number.append("P")
            continue
        detected_row = None
        column_circles = [circle for circle in black_filled_circles if column_start <= circle[0] < column_end]
        for _, y, _ in column_circles:
            for row_index, row_y in enumerate(row_y_coordinates):
                if abs(y - row_y) <= (row_y_coordinates[1] - row_y_coordinates[0]) // 2:
                    detected_row = row_index
                    break
        roll_number.append(str(detected_row) if detected_row is not None else '0')
    visualization_image = highlight_circles_and_grid(
        image, black_filled_circles, column_x_coordinates, row_y_coordinates, row_labels,
        color=(0, 255, 0), line_thickness=1, circle_color=(0, 0, 255), circle_thickness=2
    )
    return roll_number, visualization_image

# Utility functions for image display
def show_image(title, image, cmap='gray'):
    #Utility function to display an image with a specific title.
    plt.figure(figsize=(10, 10))
    plt.title(title)
    if cmap == 'gray':
        plt.imshow(image, cmap='gray')
    else:
        plt.imshow(image)
    plt.axis('off')
    plt.show()

# Setup image and thresholding
def setup_image_and_threshold(image_path, green_box_coordinates):
    #Load the image, crop the green box, and apply thresholding.
    image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    show_image("Original OMR Sheet", image)
    x1, y1, x2, y2 = green_box_coordinates
    green_box_image = image[y1:y2, x1:x2]
    show_image("Cropped Green Box", green_box_image)
    _, thresholded_green_box = cv2.threshold(green_box_image, 127, 255, cv2.THRESH_BINARY_INV)
    show_image("Thresholded Green Box (Binary Image)", thresholded_green_box)
    return green_box_image, thresholded_green_box

# Detect filled circles
def detect_filled_circles(thresholded_image, min_area=20, max_area=800, min_radius=3, max_radius=20):
    #Detect circles from contours in the thresholded image.
    contours, _ = cv2.findContours(thresholded_image, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    contour_debug_image = cv2.cvtColor(thresholded_image, cv2.COLOR_GRAY2BGR)
    cv2.drawContours(contour_debug_image, contours, -1, (0, 255, 0), 1)
    show_image("Contours Detected", cv2.cvtColor(contour_debug_image, cv2.COLOR_BGR2RGB), cmap=None)
    filled_circles = []
    for contour in contours:
        area = cv2.contourArea(contour)
        if min_area < area < max_area:
            ((x, y), radius) = cv2.minEnclosingCircle(contour)
            if min_radius < radius < max_radius:
                filled_circles.append((int(x), int(y), int(radius)))
    return filled_circles

# Count black-filled circles
def count_black_filled_circles(thresholded_image, filled_circles, black_pixel_ratio_threshold=0.7):
    black_filled_count = 0
    corrected_filled_circles = []
    for (x, y, r) in filled_circles:
        mask = cv2.circle(np.zeros_like(thresholded_image, dtype=np.uint8), (x, y), r, 255, -1)
        circle_pixels = cv2.bitwise_and(thresholded_image, mask)
        total_pixels = np.sum(mask > 0)
        black_pixels = np.sum(circle_pixels > 0)
        if black_pixels / total_pixels > black_pixel_ratio_threshold:
            black_filled_count += 1
            corrected_filled_circles.append((x, y, r))
    return black_filled_count, corrected_filled_circles

# Highlight filled and unfilled circles
def highlight_filled_and_unfilled_circles(image, all_circles, filled_circles, filled_color=(0, 255, 0),unfilled_color=(0, 0, 255), thickness=2):
    #Highlight filled and unfilled circles on the image.
    image_with_circles = cv2.cvtColor(image, cv2.COLOR_GRAY2BGR)
    for circle in all_circles:
        if circle in filled_circles:
            cv2.circle(image_with_circles, (circle[0], circle[1]), circle[2], filled_color, thickness)
        else:
            cv2.circle(image_with_circles, (circle[0], circle[1]), circle[2], unfilled_color, thickness)
    show_image("Circles Highlighted", cv2.cvtColor(image_with_circles, cv2.COLOR_BGR2RGB), cmap=None)
    return image_with_circles

# Analyze rows
def analyze_all_rows(image, black_circles, all_circles, total_rows=10, column_ranges=None, start_question=1):
    #nalyze all rows and determine the selected option for each question.
    if column_ranges is None:
        raise ValueError("Column ranges must be provided for analysis.")
    all_circles_sorted = sorted(all_circles, key=lambda x: x[1])
    row_height = (all_circles_sorted[-1][1] - all_circles_sorted[0][1]) / total_rows
    row_boundaries = [
        (int(all_circles_sorted[0][1] + i * row_height), int(all_circles_sorted[0][1] + (i + 1) * row_height))
        for i in range(total_rows)
    ]
    results = {}
    question_number = start_question
    for y_start, y_end in row_boundaries:
        row_circles = [circle for circle in all_circles if y_start <= circle[1] <= y_end]
        black_circles_in_row = [circle for circle in row_circles if circle in black_circles]
        row_answer = "No answer detected"
        for circle in black_circles_in_row:
            for option, (start, end) in column_ranges.items():
                if start <= circle[0] <= end:
                    row_answer = option
                    break
        results[question_number] = row_answer
        question_number += 1

    return results

# Check answers and store results
def check_answers_and_store_results(omr_results, correct_answers_csv):
    #Check detected answers against the correct ones and save the detailed results.
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_csv = f"results_{timestamp}.csv"  # Generate unique filename using timestamp
    correct_answers_df = pd.read_csv(correct_answers_csv)
    correct_answers = dict(zip(correct_answers_df['question_no'], correct_answers_df['answer']))
    total_marks = len(correct_answers)
    obtained_marks = 0
    results = []
    for question_no, correct_answer in correct_answers.items():
        detected_answer = omr_results.get(question_no, "No answer detected")
        is_correct = detected_answer == correct_answer
        obtained_marks += 1 if is_correct else 0
        results.append({
            "question_no": question_no,
            "correct_answer": correct_answer,
            "detected_answer": detected_answer,
            "is_correct": "Yes" if is_correct else "No"
        })
    results.append({
        "question_no": "Total",
        "correct_answer": total_marks,
        "detected_answer": obtained_marks,
        "is_correct": ""
    })
    results_df = pd.DataFrame(results)
    results_df.to_csv(output_csv, index=False)
    print(f"Results saved to {output_csv}")

# Function to store summary results
def store_summary_results(roll_number, total_marks, obtained_marks):
    #Store the summary results including roll number, total marks, and obtained marks in a unique CSV file.
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_summary_csv = f"summary_results_{timestamp}.csv"  # Generate unique filename using timestamp
    summary_data = {
        "Roll Number": [roll_number],
        "Total Marks": [total_marks],
        "Obtained Marks": [obtained_marks]
    }
    summary_df = pd.DataFrame(summary_data)
    summary_df.to_csv(output_summary_csv, index=False)
    print(f"Summary results saved to {output_summary_csv}")

def process_single_file(image_path, answers_csv_path):
    #Process a single image and corresponding answer CSV file.
    # Code logic remains the same for single file processing
    print(f"Processing single file: {image_path}")

    # Parameters for Code 1
    green_box_coordinates = (670, 250, 1000, 490)
    column_x_coordinates_code1 = [40, 80, 120, 160, 200, 240, 280, 320]
    row_y_coordinates_code1 = [50, 70, 90, 110, 130, 150, 170, 190, 207, 230]
    row_labels_code1 = list(range(len(row_y_coordinates_code1)))

    # Code 1 Execution
    print("Executing Code 1...")
    green_box_image, thresholded_green_box = setup_image_and_threshold_basic(image_path, green_box_coordinates)
    detected_circles = detect_filled_circles_basic(thresholded_green_box)
    _, black_filled_circles = count_black_filled_circles(thresholded_green_box, detected_circles)
    roll_number, visualization_image = analyze_all_columns_with_visualization(green_box_image, black_filled_circles, column_x_coordinates_code1, row_y_coordinates_code1, row_labels_code1)
    plt.imshow(cv2.cvtColor(visualization_image, cv2.COLOR_BGR2RGB))
    plt.title("Gridlines with Highlighted Circles and Row Labels (Code 1)")
    plt.show()
    roll_number_str = ''.join(roll_number)
    print(f"Detected Roll Number (Code 1): {roll_number_str}")

    # Parameters for Code 2
    green_boxes_code2 = [
        {
            "coordinates": (0, 580, 860, 900),
            "column_ranges": {
                "A": (0, 750),
                "B": (751, 790),
                "C": (791, 820),
                "D": (821, 850)
            },
            "start_question": 1
        },
        {
            "coordinates": (860, 580, 1035, 1100),
            "column_ranges": {
                "A": (0, 60),
                "B": (61, 90),
                "C": (91, 130),
                "D": (131, 160)
            },
            "start_question": 11
        },
        {
            "coordinates": (1035, 580, 1600, 1100),
            "column_ranges": {
                "A": (0, 60),
                "B": (61, 100),
                "C": (101, 140),
                "D": (141, 180)
            },
            "start_question": 21
        }
    ]

    print("Executing Code 2...")
    all_results = {}
    for green_box in green_boxes_code2:
        coordinates = green_box["coordinates"]
        column_ranges = green_box["column_ranges"]
        start_question = green_box["start_question"]
        green_box_image, thresholded_green_box = setup_image_and_threshold(image_path, coordinates)
        detected_circles = detect_filled_circles(thresholded_green_box)
        _, black_filled_circles = count_black_filled_circles(thresholded_green_box, detected_circles)
        box_results = analyze_all_rows(
            green_box_image,
            black_circles=black_filled_circles,
            all_circles=detected_circles,
            total_rows=10,
            column_ranges=column_ranges,
            start_question=start_question
        )
        all_results.update(box_results)

        # Highlight MCQ Circles
        highlight_mcq_circles(green_box_image, black_filled_circles, detected_circles, column_ranges, total_rows=10)

    # Compute results and store them
    correct_answers_df = pd.read_csv(answers_csv_path)
    correct_answers = dict(zip(correct_answers_df['question_no'], correct_answers_df['answer']))
    total_marks = len(correct_answers)
    obtained_marks = sum(1 for q, a in correct_answers.items() if all_results.get(q) == a)

    # Save detailed results to the primary CSV
    check_answers_and_store_results(all_results, answers_csv_path)

    # Save the summary results
    store_summary_results(roll_number_str, total_marks, obtained_marks)

def process_single_file_for_folder(image_path, answers_csv_path):
    #Process a single file and return summary results for folder processing.
    # Reuse the logic from `process_single_file`
    green_box_coordinates = (670, 250, 1000, 490)
    column_x_coordinates_code1 = [40, 80, 120, 160, 200, 240, 280, 320]
    row_y_coordinates_code1 = [50, 70, 90, 110, 130, 150, 170, 190, 207, 230]
    row_labels_code1 = list(range(len(row_y_coordinates_code1)))

    # Code 1 Execution
    print("Executing Code 1...")
    green_box_image, thresholded_green_box = setup_image_and_threshold_basic(image_path, green_box_coordinates)
    detected_circles = detect_filled_circles_basic(thresholded_green_box)
    _, black_filled_circles = count_black_filled_circles(thresholded_green_box, detected_circles)
    roll_number, visualization_image = analyze_all_columns_with_visualization(green_box_image, black_filled_circles, column_x_coordinates_code1, row_y_coordinates_code1, row_labels_code1)
    plt.imshow(cv2.cvtColor(visualization_image, cv2.COLOR_BGR2RGB))
    plt.title("Gridlines with Highlighted Circles and Row Labels (Code 1)")
    plt.show()
    roll_number_str = ''.join(roll_number)
    print(f"Detected Roll Number (Code 1): {roll_number_str}")

    # Code 2 logic for question analysis
    # Define the configuration for processing different green box sections on the OMR sheet
    green_boxes_code2 = [
        {
            "coordinates": (0, 580, 860, 900),
            "column_ranges": {
                "A": (0, 750),
                "B": (751, 790),
                "C": (791, 820),
                "D": (821, 850),
            },
            "start_question": 1,
        },
        {
            "coordinates": (860, 580, 1035, 1100),
            "column_ranges": {
                "A": (0, 60),
                "B": (61, 90),
                "C": (91, 130),
                "D": (131, 160),
            },
            "start_question": 11,
        },
        {
            "coordinates": (1035, 580, 1600, 1100),
            "column_ranges": {
                "A": (0, 60),
                "B": (61, 100),
                "C": (101, 140),
                "D": (141, 180),
            },
            "start_question": 21,
        },
    ]

    all_results = {}
    for green_box in green_boxes_code2:
        coordinates = green_box["coordinates"]
        column_ranges = green_box["column_ranges"]
        start_question = green_box["start_question"]
        green_box_image, thresholded_green_box = setup_image_and_threshold(image_path, coordinates)
        detected_circles = detect_filled_circles(thresholded_green_box)
        _, black_filled_circles = count_black_filled_circles(thresholded_green_box, detected_circles)
        box_results = analyze_all_rows(
            green_box_image,
            black_circles=black_filled_circles,
            all_circles=detected_circles,
            total_rows=10,
            column_ranges=column_ranges,
            start_question=start_question
        )
        all_results.update(box_results)

        # Highlight MCQ Circles
        highlight_mcq_circles(green_box_image, black_filled_circles, detected_circles, column_ranges, total_rows=10)

    # Compute marks
    correct_answers_df = pd.read_csv(answers_csv_path)
    correct_answers = dict(zip(correct_answers_df['question_no'], correct_answers_df['answer']))
    total_marks = len(correct_answers)
    obtained_marks = sum(1 for q, a in correct_answers.items() if all_results.get(q) == a)
    return roll_number_str, total_marks, obtained_marks

def process_folder(folder_path):
    #Process multiple images and corresponding answer CSVs from a single folder and save results to a single CSV.
    print(f"Processing folder: {folder_path}")
    all_results = []

    # Ensure folder exists
    if not os.path.isdir(folder_path):
        raise ValueError("The specified folder does not exist.")

    # Get all files in the folder
    files = os.listdir(folder_path)

    # Filter and pair files by their names (matching .png and .csv)
    paired_files = {}
    for file in files:
        name, ext = os.path.splitext(file)
        if ext == ".png":
            paired_files[name] = {"image": os.path.join(folder_path, file)}
        elif ext == ".csv":
            paired_files.setdefault(name, {})["csv"] = os.path.join(folder_path, file)

    # Process each pair
    for name, paths in paired_files.items():
        if "image" in paths and "csv" in paths:
            image_path = paths["image"]
            csv_path = paths["csv"]
            print(f"Processing: {image_path} with {csv_path}")
            roll_number, total_marks, obtained_marks = process_single_file_for_folder(image_path, csv_path)
            all_results.append({
                "Roll Number": roll_number,
                "Total Marks": total_marks,
                "Obtained Marks": obtained_marks,
            })
        else:
            print(f"Missing pair for: {name}")

    # Save all results to a single CSV file
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_csv = f"summary_results_{timestamp}.csv"
    pd.DataFrame(all_results).to_csv(output_csv, index=False)
    print(f"Summary results saved to {output_csv}")

def process_main(image_path_or_folder, answers_csv_path_or_folder, process_mode="single"):
    #Main function to process OMR sheets and answers.
    if process_mode == "single":
        # Single file processing logic
        process_single_file(image_path_or_folder, answers_csv_path_or_folder)
    elif process_mode == "multiple":
        # Folder processing logic
        process_folder(image_path_or_folder)
    else:
        raise ValueError("Invalid process_mode. Use 'single' or 'multiple'.")
