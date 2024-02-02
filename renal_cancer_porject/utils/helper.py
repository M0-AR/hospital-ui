import os
import pandas as pd
from typing import Dict, Callable, Optional


def read_excel_data_from_folders(file: str, data_folder_path: str) -> Dict[str, pd.DataFrame]:
    """
    Reads an Excel file from each subdirectory of the specified data folder,
    and stores them in a dictionary with keys formatted as '<patient_id>_<filename>'.

    Parameters:
    file (str): The name of the Excel file to read from each subfolder.
    data_folder_path (str): The path to the data folder containing patient subdirectories. Defaults to 'HospitalData'.

    Returns:
    Dict[str, pd.DataFrame]: A dictionary with patient IDs as keys and corresponding DataFrames as values.
    """

    # Validate input parameters
    if not os.path.isdir(data_folder_path):
        raise FileNotFoundError(f"The specified data folder path does not exist: {data_folder_path}")

    # Initialize a dictionary to store the data
    data = {}

    # Loop through each directory in the specified data folder path
    for patient_id in os.listdir(data_folder_path):
        patient_directory = os.path.join(data_folder_path, patient_id)

        if os.path.isdir(patient_directory):
            # Construct file path for the Excel file
            filepath = os.path.join(patient_directory, file)

            # Check if the file exists and is a file
            if os.path.isfile(filepath):
                try:
                    # Read the Excel file into a DataFrame
                    df = pd.read_excel(filepath, header=0)
                    # Add the DataFrame to the dictionary with a unique key
                    data[f"{patient_id}_{file}"] = df
                except Exception as e:
                    print(f"Failed to read the file {filepath}: {e}")

    return data


def read_excel_data_into_dataframe(file: str, data_folder_path: str) -> pd.DataFrame:
    """
    Read Excel files from patient folders within the specified data folder into a single DataFrame.

    Parameters:
    file (str): The name of the Excel file to read from each subfolder.
    data_folder_path (str): The path to the data folder containing patient subdirectories. Defaults to 'HospitalData'.

    Returns:
    pd.DataFrame: A DataFrame containing data from all Excel files, with an additional 'cpr' column for patient IDs.

    Raises:
    FileNotFoundError: If the data folder path does not exist.
    """
    # Check if the data_folder_path exists
    if not os.path.exists(data_folder_path):
        raise FileNotFoundError(f"Data folder does not exist: {data_folder_path}")

    # List to store individual DataFrames
    data_frames = []

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

                # Add cpr column
                df.insert(0, 'cpr', cpr)

                # Append the DataFrame to the data_frames list
                data_frames.append(df)
            except Exception as e:
                print(f"Failed to read the file {filepath}: {e}")

    # Concatenate all the data_frames into a single DataFrame
    if data_frames:
        data = pd.concat(data_frames, ignore_index=True)
        return data
    else:
        # Return an empty DataFrame if no data was added
        return pd.DataFrame()


def read_process_and_combine_excel_data(
        file: str,
        data_folder_path: str,
        operation_callback: Optional[Callable[[pd.DataFrame, str], pd.DataFrame]] = None
) -> pd.DataFrame:
    """
    Read Excel files from patient folders within the specified data folder into a single DataFrame.
    Optionally apply a callback operation on each DataFrame.

    Parameters:
    file (str): The name of the Excel file to read from each subfolder.
    data_folder_path (str): The path to the data folder containing patient subdirectories. Defaults to 'HospitalData'.
    operation_callback (Callable[[pd.DataFrame, str], pd.DataFrame], optional): A function to apply to each DataFrame.

    Returns:
    pd.DataFrame: A DataFrame containing data from all Excel files, with an additional 'cpr' column for patient IDs.

    Raises:
    FileNotFoundError: If the data folder path does not exist.
    """
    # Check if the data_folder_path exists
    if not os.path.exists(data_folder_path):
        raise FileNotFoundError(f"Data folder does not exist: {data_folder_path}")

    # List to store individual DataFrames
    data_frames = []

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

                # Add cpr column
                df.insert(0, 'cpr', cpr)

                # If a callback operation is provided, apply it
                if operation_callback:
                    df = operation_callback(df, cpr)

                # Append the DataFrame to the data_frames list
                data_frames.append(df)
            except Exception as e:
                print(f"Failed to read the file {filepath}: {e}")

    # Concatenate all the data_frames into a single DataFrame
    if data_frames:
        data = pd.concat(data_frames, ignore_index=True)
        return data
    else:
        # Return an empty DataFrame if no data was added
        return pd.DataFrame()
