import os
import pandas as pd
import re
import openpyxl
from collections import defaultdict


def transform_vitale_data(original_data):
    # Dictionary to store the tidy data
    # Keys are tuples of (cpr, date), values are dictionaries of the measurements
    tidy_data_dict = defaultdict(dict)

    # Regular expression pattern to extract date
    date_pattern = re.compile(r'\d{2}-\d{2}-\d{4}')

    # Regular expression pattern to extract date and time
    date_time_pattern = re.compile(r'\d{2}-\d{2}-\d{4} \d{2}:\d{2}')

    # Mapping from measurement type to column name
    measurement_to_column = {
        'Blodtryk': 'vitale_blodtryk',
        'Puls': 'vitale_puls',
        'Resp.frekv.': 'vitale_respfrekv',
        'Temperatur': 'vitale_temperatur',
        'Temp.kilde': 'vitale_tempkilde',
        'Saturation': 'vitale_saturation',
        'Hovedomfang (cm)': 'vitale_hovedomfang',
        'Vægt': 'vitale_vaegt',
        'Højde': 'vitale_hoejde',
        'Body Mass Index': 'vitale_bodymassindex'
    }

    # Loop through each row in the original data
    for index, row in original_data.iterrows():
        # Extract the cpr
        cpr = row['cpr']

        # Extract the measurement type
        measurement_type = str(row['værdier']).replace(':', '').strip()

        # Check if the measurement type is in the mapping
        if measurement_type in measurement_to_column:
            # Loop through each column except 'værdier'
            for column in original_data.columns[2:]:
                raw_value = str(row[column]).replace('\xa0', ' ').replace('_x000D_', '').strip()

                # Extract date from column name
                match = date_time_pattern.search(column)
                column_date = match.group() if match else None

                # If date is extracted from column name, use it, otherwise, extract from raw value
                measurement_date = column_date
                if not measurement_date:
                    match = date_pattern.search(raw_value)
                    measurement_date = match.group() if match else None

                    # Remove date from raw_value if measurement_date exists
                    if measurement_date:
                        raw_value_no_date = date_pattern.sub('', raw_value)
                    else:
                        raw_value_no_date = raw_value

                    # Split the string into an array
                    raw_value_array = raw_value_no_date.split()

                    if 'pr.' in raw_value_array:
                        raw_value_array.remove('pr.')

                    # Check if raw_value_array[1] is not a date and concatenate
                    if len(raw_value_array) > 1 and not date_pattern.match(raw_value_array[1]):
                        raw_value_no_date = raw_value_array[0] + ' ' + raw_value_array[1]
                    else:
                        raw_value_no_date = raw_value_array[0] if raw_value_array else ''
                else:
                    raw_value_no_date = raw_value

                # Extract the measurement value
                if raw_value_no_date not in ('nan', ''):
                    # Add data to the tidy data dict
                    key = (cpr, measurement_date)
                    tidy_data_dict[key][measurement_to_column[measurement_type]] = raw_value_no_date

    # Convert the nested dictionaries to a list of dictionaries
    tidy_data_list = [{'cpr': cpr, 'vitale_measurement_date': date, **measurements}
                      for (cpr, date), measurements in tidy_data_dict.items()]

    # Convert the list of dictionaries to a DataFrame
    tidy_data = pd.DataFrame(tidy_data_list)

    # Return the tidy data
    return tidy_data


def read_blood_test_excel_data():
    # Base directory
    base_directory = 'HospitalData'

    # List subdirectories within the base directory
    patient_dirs = [dir_name for dir_name in os.listdir(base_directory) if
                    os.path.isdir(os.path.join(base_directory, dir_name))]

    # Define the default file name here
    file_name = 'blood_test.xlsx'

    # Regular expression pattern to match dates
    pattern = re.compile(r'^\d{2}-\d{2}-\d{2}\s')

    # List to store the data
    data_list = []

    # Iterate over each subdirectory and read the blood_test.xlsx file
    for patient_dir in patient_dirs:
        file_path = os.path.join(base_directory, patient_dir, file_name)

        if os.path.isfile(file_path):
            workbook = openpyxl.load_workbook(file_path)
            sheet = workbook.active
            current_date = None

            for cell in sheet['A']:
                content = cell.value.strip().replace('_x000D_', '')
                if content:
                    if pattern.match(content):
                        current_date = content
                    else:
                        # Append row data to the list as a dictionary
                        data_list.append({
                            'cpr': patient_dir,
                            'blood_date': current_date,
                            'content': content
                        })

    # Convert the list of dictionaries to a DataFrame
    data_frame = pd.DataFrame(data_list)

    return data_frame


def read_excel_data_into_dataframe(file=None):
    """
    Read Excel files from patient folders into a DataFrame.

    :param file: Name of the Excel file to read.
    :return: DataFrame containing data from Excel files with additional columns for cpr.
    """
    # List to store individual DataFrames
    data_frames = []

    # Patient directories
    patient_dirs = [dir_name for dir_name in os.listdir('HospitalData') if
                    os.path.isdir(os.path.join('HospitalData', dir_name))]

    # Iterate through patient directories
    for cpr in patient_dirs:
        patient_directory = os.path.join('HospitalData', cpr)

        # Read specific file
        filepath = os.path.join(patient_directory, file)
        if os.path.isfile(filepath):
            # Read Excel file into DataFrame
            df = pd.read_excel(filepath, header=0)

            # Add cpr column
            df.insert(0, 'cpr', cpr)

            # Append the DataFrame to the data_frames list
            data_frames.append(df)

    # Concatenate all the data_frames into a single DataFrame
    data = pd.concat(data_frames, ignore_index=True)

    return data


# Read Data
# Read miba data
miba_excels = read_excel_data_into_dataframe('miba.xlsx')

# Read medications data
medicin_excels = read_excel_data_into_dataframe('medicin.xlsx')

# Read diagnoses data
diagnoses_excels = read_excel_data_into_dataframe('diagnose_list.xlsx')

# Read pato_bank data
pato_bank_excels = read_excel_data_into_dataframe('pato_bank.xlsx')

vitale_excels = read_excel_data_into_dataframe('vitale.xlsx')

blood_test_excels = read_blood_test_excel_data()

# Transform Data
vitale_excels = transform_vitale_data(vitale_excels)

# Rename Column
miba_excels = miba_excels.rename(
    columns={'Prøvens art': 'miba_sample_type', 'Taget d.': 'miba_collection_date', 'Kvantitet': 'miba_quantity',
             'Analyser': 'miba_analysis', 'Resistens': 'miba_resistance', 'Mikroskopi': 'miba_microscopy'})
medicin_excels = medicin_excels.rename(
    columns={'Medication': 'medicines_name', 'Start-Date': 'medicine_start_date', 'End-Date': 'medicine_end_date'})
diagnoses_excels = diagnoses_excels.rename(columns={'note': 'diagnose_note', 'date': 'diagnose_date'})
pato_bank_excels = pato_bank_excels.rename(
    columns={'Modtaget': 'pato_received_date', 'Serviceyder': 'pato_service_provider',
             'Rekv.nr.': 'pato_request_number', 'Kategori': 'pato_category', 'Diagnoser': 'pato_diagnoses',
             'Mat.nr.	Beskrivelse af materiale/prøve': 'pato_material_description_of_smple',
             'Konklusion': 'pato_conclusion', 'Mikroskopi': 'pato_microscopy',
             'Andre undersøgelser': 'pato_other_investigations', 'Makroskopi': 'pato_macroscopy',
             'Kliniske oplysninger': 'pato_clinical_information'})
blood_test_excels = blood_test_excels.rename(columns={'content': 'blood_content'})

# Aggregate Data into List
# Group by 'cpr' and aggregate all other columns into lists
aggregations = {col: list for col in miba_excels.columns if col != 'cpr'}
miba_agg = miba_excels.groupby('cpr').agg(aggregations).reset_index()

aggregations = {col: list for col in medicin_excels.columns if col != 'cpr'}
medicin_agg = medicin_excels.groupby('cpr').agg(aggregations).reset_index()

aggregations = {col: list for col in diagnoses_excels.columns if col != 'cpr'}
diagnoses_egg = diagnoses_excels.groupby('cpr').agg(aggregations).reset_index()

aggregations = {col: list for col in pato_bank_excels.columns if col != 'cpr'}
pato_bank_egg = pato_bank_excels.groupby('cpr').agg(aggregations).reset_index()

aggregations = {col: list for col in vitale_excels.columns if col != 'cpr'}
vitale_egg = vitale_excels.groupby('cpr').agg(aggregations).reset_index()

MAX_LEN = 32767
MAX_LEN = 25000

def custom_aggregate(series):
    columns_data = []
    current_str = ""
    cumulative_length = 0  # This will keep a running count of the items' lengths in the series

    for item in series:
        item_str = str(item)
        cumulative_length += len(item_str)

        # If adding the cumulative length of items and the current_str exceeds MAX_LEN
        if cumulative_length + 300 > MAX_LEN:  # Can use either cumulative_length or len(current_str)
            columns_data.append(current_str)
            current_str = ""
            cumulative_length = 0  # Reset the cumulative length for the new chunk
        else:
            # Separate 'item' by @ because we already have data some '3,2' as decimal number
            current_str += '\'' + item_str + '\'' + ', ' if current_str else  item_str + '\'' + ', '

    # Add the last chunk if any data is left
    if current_str:
        columns_data.append(current_str)

    return columns_data


aggregations = {col: custom_aggregate for col in blood_test_excels.columns if col != 'cpr'}
blood_test_egg = blood_test_excels.groupby('cpr').agg(aggregations).reset_index()


def explode_list_columns(df):
    """Expand columns with list entries into separate columns."""
    for col in df.columns:
        # If any cell in the column is a list, we proceed
        if any(isinstance(cell, list) for cell in df[col]):
            # Create separate columns for each item in the list
            exploded = df[col].apply(pd.Series)
            exploded.columns = [f"{col}_{i}" for i in range(1, len(exploded.columns) + 1)]

            # Drop original column and append exploded columns to dataframe
            df = df.drop(col, axis=1).join(exploded)
    return df


# Process your dataframe
blood_test_egg_exploded = explode_list_columns(blood_test_egg)

# Combine Data
# Merge the two DataFrames based on the 'cpr' column
miba_medicin_combined_data = pd.merge(miba_agg, medicin_agg, on='cpr', how='outer')

miba_medicin_diagnoses_combined_data = pd.merge(miba_medicin_combined_data, diagnoses_egg, on='cpr', how='outer')

miba_medicin_diagnoses_pato_combined_data = pd.merge(miba_medicin_diagnoses_combined_data, pato_bank_egg, on='cpr',
                                                     how='outer')

miba_medicin_diagnoses_pato_vitale_combined_data = pd.merge(miba_medicin_diagnoses_pato_combined_data, vitale_egg,
                                                            on='cpr', how='outer')

miba_medicin_diagnoses_pato_vitale_blood_combined_data = pd.merge(miba_medicin_diagnoses_pato_vitale_combined_data,
                                                                  blood_test_egg_exploded, on='cpr', how='outer')

miba_medicin_diagnoses_pato_vitale_blood_combined_data.insert(0, 'record_id', [i for i in range(1, 1 + len(
    miba_medicin_diagnoses_pato_vitale_blood_combined_data))])


def process_cell(cell_value):
    # If cell_value is empty, return an empty string ""
    if str(cell_value) == 'nan':
        return "nan"

    # Check if cell_value is already a list
    if isinstance(cell_value, list):
        # Convert list items to string, replace 'nan' with empty string
        values = [str(item) if str(item) != 'nan' else '' for item in cell_value]
        return '\"' + str(values) + '\"'

    # If cell_value is a string and starts with "[" and ends with "]"
    if isinstance(cell_value, str) and cell_value.startswith("[") and cell_value.endswith("]"):
        # Strip off the brackets and split the string into a list based on comma separation
        values = cell_value[1:-1].split(", ")

        # Replace 'nan' with empty string
        values = ['' if val.strip() == 'nan' else val for val in values]

        # Convert list back to string representation
        return values

    # If cell_value is a string and NOT starts with "[" and ends with "]"
    if isinstance(cell_value, str):
        return '\"[\'' + str(cell_value) + '\']\"'

    # If it's neither a string in list format nor a list, return the cell_value as is
    return cell_value


# Apply the function to each cell in the dataframe
miba_medicin_diagnoses_pato_vitale_blood_combined_data = miba_medicin_diagnoses_pato_vitale_blood_combined_data.applymap(
    process_cell)

# Save with headers
miba_medicin_diagnoses_pato_vitale_blood_combined_data.to_csv('combine_all_data.csv', index=False, header=False)
miba_medicin_diagnoses_pato_vitale_blood_combined_data.to_excel('combine_all_data.xlsx', index=False, header=False)
# miba_medicin_diagnoses_pato_vitale_blood_combined_data.to_excel('combine_all_data.xlsx', index=False, header=True)