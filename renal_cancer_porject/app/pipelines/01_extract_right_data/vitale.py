import os
import pandas as pd
import re


def extract_numeric_value(string):
    """
    Extracts the first numeric value (integer or decimal) from a given string.

    Parameters:
    string (str): The string containing the numeric value.

    Returns:
    float: The extracted numeric value, or None if no numeric value is found.
    """
    match = re.search(r'\d+(\.\d+)?', string)
    if match:
        return float(match.group())
    return None


def convert_cm_to_m(cm_value):
    """
    Converts a value from centimeters to meters.

    Parameters:
    cm_value (float): The value in centimeters.

    Returns:
    float: The value converted to meters.
    """
    return cm_value / 100 if cm_value is not None else None


def calculate_bmi(weight_kg, height_cm):
    """
    Calculate the Body Mass Index (BMI) using weight in kilograms and height in centimeters.

    Parameters:
    weight_kg (float): Weight in kilograms.
    height_cm (float): Height in centimeters.

    Returns:
    float: Calculated BMI.
    """
    # Convert height from cm to m
    height_m = convert_cm_to_m(height_cm)
    return weight_kg / (height_m ** 2)


def extract_and_calculate_bmi_from_patient_data(file: str, data_folder_path: str) -> pd.DataFrame:
    """
    Read Excel files from patient folders within the specified data folder into a single DataFrame.
    Calculate BMI for each patient and store 'cpr' and 'BMI' values.

    Parameters:
    file (str): The name of the Excel file to read from each subfolder.
    data_folder_path (str): The path to the data folder containing patient subdirectories.

    Returns:
    pd.DataFrame: A DataFrame containing 'cpr' and 'BMI' for each patient.

    Raises:
    FileNotFoundError: If the data folder path does not exist.
    """
    # Check if the data_folder_path exists
    if not os.path.exists(data_folder_path):
        raise FileNotFoundError(f"Data folder does not exist: {data_folder_path}")

    bmi_data = []

    # Patient directories
    patient_dirs = [dir_name for dir_name in os.listdir(data_folder_path) if
                    os.path.isdir(os.path.join(data_folder_path, dir_name))]

    # Iterate through patient directories
    for cpr in patient_dirs:
        patient_directory = os.path.join(data_folder_path, cpr)

        # Read specific file
        filepath = os.path.join(patient_directory, file)
        if os.path.isfile(filepath):
            try:
                # Read Excel file into DataFrame
                df = pd.read_excel(filepath, header=0)

                # Extract weight and height values for BMI calculation
                weight_string = df[df['værdier'].str.contains('Vægt', na=False)]['Seneste værdi'].iloc[0]
                height_string = df[df['værdier'].str.contains('Højde', na=False)]['Seneste værdi'].iloc[0]

                # Extract numeric values
                weight_kg = extract_numeric_value(weight_string)
                height_cm = extract_numeric_value(height_string)

                # Calculate BMI and store it with the cpr
                bmi = calculate_bmi(weight_kg, height_cm)
                bmi_data.append({'cpr': cpr, 'BMI': bmi})
            except Exception as e:
                print(f"Failed to process data for {cpr}: {e}")
                # Choose the appropriate placeholder for BMI
                bmi_placeholder = None  # or "N/A", or -1, depending on your requirement
                bmi_data.append({'cpr': cpr, 'BMI': bmi_placeholder})

    # Create a DataFrame from the bmi_data
    bmi_df = pd.DataFrame(bmi_data)

    return bmi_df


# Read vitale data
vitale_data = extract_and_calculate_bmi_from_patient_data('vitale.xlsx',
                                                          'C:\\src\\hospital-ui\\renal_cancer_porject\\data')
print(vitale_data)