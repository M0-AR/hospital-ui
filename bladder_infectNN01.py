import os
import pandas as pd

def filter_records_by_codes(data_frame):
    """
    Filter out rows that don't contain any of the specified codes in the 'diagnosis_category' column.

    :param data_frame: Input DataFrame.
    :return: DataFrame with filtered records.
    """
    # List of codes to look for
    codes = [
        "ÆYY111", "ÆYY113", "P30611",
        "P30615",
        "P30619",
        "P30625",
        "P306x0",
        "P306x4",
        "ÆYYY0R",
        "ÆYYY0S",
        "ÆYYY0U",
        "ÆYYY0X",
        "M80133",
        "M80203",
        "M80403",
        "M80702",
        "M80703",
        "M80823",
        "M81200",
        "M81202",
        "M81203",
        "M81300",
        "M81233",
        "M81313",
        "M81301",
        "M81302",
        "M81403",
        "M81402",
        "M81303",
        "M80703",
        "M81403",
        "M69760",
    ]

    # Filter rows that contain any of the codes as substring
    code_filters = [data_frame['diagnosis_category'].str.contains(code, na=False) for code in codes]
    combined_filter = pd.concat(code_filters, axis=1).any(axis=1)

    # Return the DataFrame with the filtered rows
    return data_frame[combined_filter]


def read_excel_data_from_folders(file=None):
    data = {}
    patient_dirs = [dir_name for dir_name in os.listdir('HospitalData') if
                    os.path.isdir(os.path.join('HospitalData', dir_name))]

    for patient_id in patient_dirs:
        patient_directory = os.path.join('HospitalData', patient_id)

        # Read specific file
        filepath = os.path.join(patient_directory, file)
        if os.path.isfile(filepath):
            df = pd.read_excel(filepath, header=0)
            data[f"{patient_id}_{file}"] = df

    return data


import os
import pandas as pd


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


# Read data
pato_excels = read_excel_data_from_folders('pato_bank.xlsx')


# def sample_dates_and_diagnoser(data):
#     codes_to_look_for = [
#         "T74940",  # Urinblære, prostata og vesicula seminalis
#         "T74000",  # Urinblære
#         "T74950",  # Urinblære, vagina, uterus og adnexa
#         "T74010",  # Urinblæreslimhinde
#         "T74030",  # Urinblære, detrusor
#         "T7432A",  # Ureterostium, højre
#         "T7432B",  # Ureterostium, venstre
#         "T75000",  # Urethra
#         "T75050",  # Urethra, mand
#         "T75060",  # Urethra, kvinde
#         "T75010",  # Urethraslimhinde Urethrabiopsi
#         "T75110",  # Urethra pars prostatica
#     ]
#
#     samples = {}
#
#     for key, df in data.items():
#         for code in codes_to_look_for:
#             # Filter rows that contain the code as substring
#             filtered_rows = df[df['Diagnoser'].str.contains(code, na=False)]
#
#             # If any rows contain the code, get the first one and add it to samples
#             if not filtered_rows.empty:
#                 first_occurrence = filtered_rows.iloc[0]
#                 samples[f"{key}_{code}"] = {
#                     "Date": first_occurrence["Modtaget"],
#                     "Diagnoser": first_occurrence["Diagnoser"]
#                 }
#
#     return samples

def sample_dates_and_diagnoser(data):
    codes_to_look_for = [
        "T74940",  # Urinblære, prostata og vesicula seminalis
        "T74000",  # Urinblære
        "T74950",  # Urinblære, vagina, uterus og adnexa
        "T74010",  # Urinblæreslimhinde
        "T74030",  # Urinblære, detrusor
        "T7432A",  # Ureterostium, højre
        "T7432B",  # Ureterostium, venstre
        "T75000",  # Urethra
        "T75050",  # Urethra, mand
        "T75060",  # Urethra, kvinde
        "T75010",  # Urethraslimhinde Urethrabiopsi
        "T75110",  # Urethra pars prostatica
    ]

    samples = []

    for key, df in data.items():
        for code in codes_to_look_for:
            # Filter rows that contain the code as substring
            filtered_rows = df[df['Diagnoser'].str.contains(code, na=False)]

            # If any rows contain the code, get the first one and add it to samples
            if not filtered_rows.empty:
                first_occurrence = filtered_rows.iloc[0]
                samples.append({
                    "cpr": f"{key.split('_')[0]}",
                    "first_pato_date": first_occurrence["Modtaget"],
                    "diagnoser": first_occurrence["Diagnoser"]
                })

    # Convert the list of dictionaries to a DataFrame
    return pd.DataFrame(samples)


# Sample the date(s) and text
samples = sample_dates_and_diagnoser(pato_excels)

# Remove duplication
samples = samples.drop_duplicates()

samples

# Custom function to split text by '['
def split_by_bracket(text):
    # Split records within 'Diagnoser' by '[' and strip whitespace
    return [record.strip() for record in text.split('[') if record.strip()]

# Assuming that samples is a DataFrame with a 'Diagnoser' column
# Apply the custom function to split the text within the 'Diagnoser' column
samples['diagnoser'] = samples['diagnoser'].apply(split_by_bracket)

# Now, use the explode() method to transform each element of the list into separate rows
samples = samples.explode('diagnoser')
samples

"""
def keep_earliest_records(data_frame):
    # Keep only the earliest record for each unique cpr.
    # 
    # :param data_frame: Input DataFrame.
    # :return: DataFrame with earliest records.

    # Create a copy of the data frame
    df_copy = data_frame.copy()

    # Convert date to datetime for sorting
    df_copy['date'] = pd.to_datetime(df_copy['date'], format='%d.%m.%Y')

    # Sort by date
    df_copy = df_copy.sort_values(by='date')

    # Drop duplicates by cpr, keeping only the first (earliest) record
    df_copy = df_copy.drop_duplicates(subset='cpr', keep='first')

    # Convert date back to string in the desired format
    df_copy['date'] = df_copy['date'].dt.strftime('%d.%m.%Y')

    return df_copy
"""


def keep_earliest_records(data_frame):
    """
    Keep only the earliest record for each unique cpr and code.

    :param data_frame: Input DataFrame.
    :return: DataFrame with earliest records.
    """
    # Create a copy of the data frame
    df_copy = data_frame.copy()

    # Convert date to datetime for sorting
    df_copy['first_pato_date'] = pd.to_datetime(df_copy['first_pato_date'], format='%d.%m.%Y')

    # List of codes to look for
    codes_to_look_for = [
        "T74940", "T74000", "T74950", "T74010", "T74030",
        "T7432A", "T7432B", "T75000", "T75050", "T75060",
        "T75010", "T75110"
    ]

    # Filter rows that contain any of the codes as substring
    code_filters = [df_copy['diagnoser'].str.contains(code, na=False) for code in codes_to_look_for]
    combined_filter = pd.concat(code_filters, axis=1).any(axis=1)
    df_copy = df_copy[combined_filter]

    # Group by cpr, then get index of min date
    idx = df_copy.groupby(['cpr'])['first_pato_date'].idxmin()

    # Select the rows with the earliest dates
    df_copy = df_copy.loc[idx]

    # Convert date back to string in the desired format
    df_copy['first_pato_date'] = df_copy['first_pato_date'].dt.strftime('%d.%m.%Y')

    return df_copy

# Use the function
earliest_records_df = keep_earliest_records(samples)

# Output the result
print(earliest_records_df)


# 01
def collect_diagnose_codes_in_columns(patients_data):
    """
    Process the patients' data and collect specified diagnose codes into multiple columns.

    :param patients_data: DataFrame containing patients' data with 'cpr', 'date', and 'diagnoser' columns.
    :return: DataFrame with collected diagnose codes in multiple columns.
    """
    # List of columns
    columns = [
        "cpr",
        "first_pato_date",
        "ÆYY111 lav malignitetsgrad",
        "ÆYY113 høj malignitetsgrad",
        "P30611 ekscisionsbiopsi",
        "P30615 endoskopisk biopsi",
        "P30619 randombiopsi",
        "P30625 spånresektat",
        "P306x0 ektomipræparat",
        "P306x4 tumorektomi",
        "ÆYYY0R nested inkl. large nested type",
        "ÆYYY0S mikrocystisk type",
        "ÆYYY0U plasmacytoid/signetringscelle/diffus type",
        "ÆYYY0X lipidrig type",
        "M80133 storcellet neuroendokrint karcinom",
        "M80203 udifferentieret karcinom",
        "M80403 småcellet karcinom",
        "M80702 planocellulært karcinom in situ",
        "M80703 planocellulært karcinom",
        "M80823 lymfoepitelialt karcinom",
        # "M09450 ingen tegn på malignitet", # TODO: this code was not exist -> do we need it or just stick with the list in document
        "M81200 urotelialt papillom",
        "M81202 urotelialt karcinom in situ",
        "M81203 urotelialt",
        "M81300 inverteret urotelialt papillom",
        "M81233 sarkomatoidt urotelialt karcinom",
        "M81313 mikropapillært urotelialt karcinom",
        "M81301 papillær urotelial tumor med minimalt malignitetspotentiale",
        "M81302 ikkeinvasiv papillær urotelial tumor",
        "M81403 adenokarcinom",
        "M81402 adenokarcinom in situ",
        "M81303 urotelial tumor",
        "M80703 planocellulært karcinom",
        "M81403 adenokarcinom",
        "M69760 malignitetssuspekte celler"
    ]

    # Create an empty DataFrame with specified columns
    data_frame = pd.DataFrame(columns=columns)

    # Iterating through each row of the DataFrame
    for index, row in patients_data.iterrows():
        cpr = row['cpr']
        first_pato_date = row['first_pato_date']
        diagnoser = row['diagnoser']

        lines = diagnoser.split('\n')
        record_dict = {'cpr': cpr, 'first_pato_date': first_pato_date}

        # Skip if there are not enough lines
        if len(lines) < 3:
            continue

        # Column name is in the second line
        column_name = lines[1].strip()

        # The rest of the lines are the data for the column
        column_data = '\n'.join(lines[2:]).strip()

        if column_name in columns:
            record_dict[column_name] = column_data

            # Append the structured record to the DataFrame
            data_frame.loc[len(data_frame)] = record_dict

    return data_frame


# Call the function with the sample data
diagnose_codes_in_columns_data = collect_diagnose_codes_in_columns(samples)
diagnose_codes_in_columns_data # TODO: Here you can compare second method with this table because you can see the blue color which represents not empty column


# Remove duplicates
# processed_data_no_duplicates = processed_data.drop_duplicates()



# Read miba data
miba_excels = read_excel_data_from_folders('miba.xlsx')

from datetime import datetime


def filter_dataframes(miba_excels, earliest_records_df):
    # Start with an empty DataFrame
    filtered_data = pd.DataFrame(columns=['cpr', 'Prøvens art', 'Taget d.', 'Kvantitet'])

    for _, row in earliest_records_df.iterrows():
        cpr_number = row['cpr']
        min_date = row['first_pato_date']  # Get the minimum date from the row
        min_date_obj = datetime.strptime(min_date, '%d.%m.%Y')  # Convert min_date to datetime object

        for filename, df in miba_excels.items():
            if filename.startswith(cpr_number):
                # Convert the 'Taget d.' column to datetime objects with errors='coerce'
                df['Taget d.'] = pd.to_datetime(df['Taget d.'], format='%d.%m.%Y')

                # Filter rows based on date and 'Prøvens art' starting with 'Blod' or 'Urin'
                filtered_rows = df[(df['Taget d.'] < min_date_obj) &
                                   (df['Prøvens art'].str.startswith('Blod') |
                                    df['Prøvens art'].str.startswith('Urin'))][['Prøvens art', 'Taget d.', 'Kvantitet']]
                filtered_rows['cpr'] = cpr_number  # Adding the cpr column to the filtered rows

                # Fill empty 'Kvantitet' cells with 'Negative'
                filtered_rows['Kvantitet'].fillna('Negative', inplace=True)

                if not filtered_rows.empty:
                    # Concatenate the filtered rows to the final DataFrame
                    filtered_data = pd.concat([filtered_data, filtered_rows], ignore_index=True)

    # Convert date back to string in the desired format
    filtered_data['Taget d.'] = filtered_data['Taget d.'].dt.strftime('%d.%m.%Y')

    # Rename the column
    filtered_data = filtered_data.rename(columns={'Taget d.': 'mida_date'})

    return filtered_data


# Usage example:
miba_filtered_data = filter_dataframes(miba_excels, diagnose_codes_in_columns_data)
print(miba_filtered_data)

# Merge the two DataFrames based on the 'cpr' column
pato_miba_combined_data = pd.merge(diagnose_codes_in_columns_data, miba_filtered_data, on='cpr', how='left')

# Display the combined DataFrame
print(pato_miba_combined_data)

# Get the list of column names
columns = list(pato_miba_combined_data.columns)

# Move the last columns to index 2
new_order = columns[:2] + columns[-3:] + columns[2:-3]

# Reorder the columns
pato_miba_combined_data = pato_miba_combined_data[new_order]

# Display the DataFrame with rearranged columns
print(pato_miba_combined_data)  # TODO: Demo here

import openpyxl
import re


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


# Example usage:
blood_test_data = read_blood_test_excel_data()
print(blood_test_data)


def filter_blood_test_data(blood_test_data, keep_values):
    """
    Filter blood_test_data DataFrame to keep only rows with specific content.

    :param blood_test_data: DataFrame with blood test data.
    :param keep_values: List of strings to keep in the 'content' column.
    :return: Filtered DataFrame.
    """
    # Convert the values in the 'content' column to lowercase and strip spaces
    lower_content = blood_test_data['content'].str.lower().str.strip()

    # Convert keep_values to lowercase for comparison
    lower_keep_values = [value.lower() for value in keep_values]

    # Filter the DataFrame
    filtered_blood_test_data = blood_test_data[lower_content.isin(lower_keep_values)]

    return filtered_blood_test_data


def filter_blood_test_data(blood_test_data):
    # Define the terms you want to keep (case insensitive)
    keep_values = [
        'hæmoglobin',
        'leukocytter',
        'neutrophilocytter',
        'crp',
        'kreatinin',
        'natrium',
        'kalium',
        'trombocytter',
        'ldh'
    ]

    # Define a function that checks if any of the terms in keep_values are in the content
    def contains_keep_value(content):
        content_lower = str(content).lower()
        return any(keep_value in content_lower for keep_value in keep_values)

    # Filter the DataFrame
    mask = blood_test_data['content'].apply(contains_keep_value)
    filtered_blood_test_data = blood_test_data[mask]

    return filtered_blood_test_data


# Usage:
filtered_blood_test_data = filter_blood_test_data(blood_test_data)

# Searching for a specific term in the 'content' column
# print(blood_test_data[blood_test_data['content'].str.contains('Hæmoglobin', case=False, na=False)])

# ---
# Split the 'content' column into 'content_name' and 'content_value'
filtered_blood_test_data[['content_name', 'content_value']] = filtered_blood_test_data['content'].str.split(';', n=1, expand=True)

# Function to extract numerical values using regex
def extract_numerical_value(value):
    # This regex captures numerical values and includes cases like <2,9
    match = re.search(r'([<>]?\s?[\d,\.]+)', value)
    return match.group(1) if match else None

# Apply the function to extract numerical values
filtered_blood_test_data['numerical_value'] = filtered_blood_test_data['content_value'].apply(extract_numerical_value)
# ---


# Copy the DataFrame
new_filtered_blood_test_data = filtered_blood_test_data.copy()

# TODO: NOTE: in content Leukocytter would have Negtive value in content_value so it would be in numerical_value None=Negative

# Drop the 'content' column
new_filtered_blood_test_data.drop(columns=['content', 'content_value'], inplace=True)

# Display the new DataFrame
print(new_filtered_blood_test_data)
####

# TODO
# pato_miba_blood_combined_data = pd.merge(pato_miba_combined_data, new_filtered_blood_test_data, on='cpr', how='outer')

def move_columns(dataframe, insert_index, number_of_columns):
    """
    Move the last columns of a DataFrame to a specified index position.

    :param dataframe: The DataFrame whose columns need to be reordered.
    :param insert_index: The index at which the last columns need to be inserted.
    :param number_of_columns: Number of last columns to be moved.
    :return: DataFrame with reordered columns.
    """
    # Extract column names
    cols = list(dataframe.columns)

    # Select the order of columns
    new_order = cols[:insert_index] + cols[-number_of_columns:] + cols[insert_index:-number_of_columns]

    # Reorder the columns
    reordered_dataframe = dataframe[new_order]

    return reordered_dataframe

# Example usage:
# pato_miba_blood_combined_data = move_columns(pato_miba_blood_combined_data, 5, 3) # TODO: uncomment blood combine line
pato_miba_blood_combined_data = move_columns(pato_miba_combined_data, 5, 3)
print(pato_miba_blood_combined_data) # TODO: DEMO

# ----
# Display unique values in the 'content' column
# unique_content_values = blood_test_data['content'].unique()
# print(unique_content_values)
# ----


# Read Medications data
medicin_excels = read_excel_data_into_dataframe('medicin.xlsx')


def filter_medicin_by_keywords(dataframe):
    """
    Filters rows in the DataFrame that contain any of the specified keywords
    in the 'Medication' column.

    :param dataframe: The input DataFrame.
    :return: A DataFrame with only the rows containing the specified keywords.
    """
    # Make a copy of the input DataFrame to avoid modifying the original
    df_copy = dataframe.copy()

    # List of keywords to filter
    keywords = [
        "Mod infektion",
        "Mod urinvejsinfektion",
        "Mod blærebetændelse",
        "Pivmecillinam",
        "Amoxicillin",
        "Trimopan",
        "Sulfamethizol",
        "Ciprofloxacin",
        "Gentamicin",
        "Piperacillin",
        "Cefuroxim",
        "meropenem"
    ]

    # Create a pattern string by joining keywords with '|' as delimiter
    pattern = '|'.join(keywords)

    # Filter rows where 'Medication' contains any of the keywords
    filtered_df = df_copy[df_copy['Medication'].str.contains(pattern, case=False, na=False)]

    return filtered_df

medicin_excels = filter_medicin_by_keywords(medicin_excels)
medicin_excels = medicin_excels.rename(columns={'Medication': 'medicines', 'Start-Date': 'medicine_start_date', 'End-Date': 'medicine_end_date'})

pato_miba_blood_medicine_combined_data = pd.merge(pato_miba_blood_combined_data, medicin_excels, on='cpr', how='left')


# Read Diagnoses data
diagnose_list_data = read_excel_data_into_dataframe('diagnose_list.xlsx')
diagnose_list_data = diagnose_list_data.rename(columns={'note': 'diagnose_note', 'date': 'diagnose_date'})

pato_miba_blood_medicine_diagnoses_combined_data = pd.merge(pato_miba_blood_medicine_combined_data, diagnose_list_data, on='cpr', how='left')
# pato_miba_blood_medicine_diagnoses_combined_data = move_columns(pato_miba_blood_medicine_diagnoses_combined_data, 5, 5)

# Specify the filename
filename = 'combined_data.xlsx'

# Save the DataFrame to an Excel file
pato_miba_blood_medicine_diagnoses_combined_data.to_excel(filename, index=False)

# Read diagnoses data
vitale_data = read_excel_data_into_dataframe('vitale.xlsx')

vitale_data



# ------------------------------------------------
# 02
import pandas as pd


def process_patient_data(patients_data):
    """
    cpr       | date       | diagnosis_category           | sub_diagnoses
    --------------------------------------------------------------------------------
    patient_a | 24.02.2023 | M81302 ikkeinvasiv ... tumor | ÆYY111 lav malignitetsgrad\nÆF181A pTa\nP30625 spånresektat
    patient_a | 24.02.2023 | T75110 Urethra ...           | M09450 ingen tegn på malignitet\nP30619 randombiopsi
    patient_b | 19.05.2017 | ...                         | ...
    ...
    :param patient_data:
    :return:
    """
    # List to store individual records
    records = []

    # Iterating through each row of the DataFrame
    for index, row in patients_data.iterrows():
        cpr = row['cpr']
        first_pato_date = row['first_pato_date']
        diagnoser = row['diagnoser']

        lines = diagnoser.split('\n')

        # Skip if there are not enough lines
        if len(lines) < 3:
            continue

        # Diagnosis category is in the second line
        diagnosis_category = lines[1].strip()

        # The rest of the lines are the sub-diagnoses
        sub_diagnoses = '\n'.join(lines[2:]).strip()

        # Create record dictionary and add to list
        record_dict = {
            'cpr': cpr,
            'first_pato_date': first_pato_date,
            'diagnoser': diagnoser,
            'diagnosis_category': diagnosis_category,
            'sub_diagnoses': sub_diagnoses
        }
        records.append(record_dict)

    # Convert the records list to a DataFrame
    data_frame = pd.DataFrame(records)

    return data_frame


diagnose_codes_in_columns_data = process_patient_data(samples)

# Remove duplicates
processed_data_no_duplicates = diagnose_codes_in_columns_data.drop_duplicates()


def keep_earliest_records(data_frame):
    """
    Keep only the earliest record for each unique cpr and code.

    :param data_frame: Input DataFrame.
    :return: DataFrame with earliest records.
    """
    # Create a copy of the data frame
    df_copy = data_frame.copy()

    # Convert date to datetime for sorting
    df_copy['first_pato_date'] = pd.to_datetime(df_copy['first_pato_date'], format='%d.%m.%Y')

    # List of codes to look for
    codes_to_look_for = [
        "T74940", "T74000", "T74950", "T74010", "T74030",
        "T7432A", "T7432B", "T75000", "T75050", "T75060",
        "T75010", "T75110"
    ]

    # Filter rows that contain any of the codes as substring
    code_filters = [df_copy['diagnoser'].str.contains(code, na=False) for code in codes_to_look_for]
    combined_filter = pd.concat(code_filters, axis=1).any(axis=1)
    df_copy = df_copy[combined_filter]

    # Convert date back to string in the desired format
    df_copy['first_pato_date'] = df_copy['first_pato_date'].dt.strftime('%d.%m.%Y')

    return df_copy

# Use the function
earliest_records_df = keep_earliest_records(processed_data_no_duplicates)
earliest_records_df.drop(columns=['diagnoser'], inplace=True)
earliest_records_df = earliest_records_df.drop_duplicates()
earliest_records_df = filter_records_by_codes(earliest_records_df)
# Output the result
print(earliest_records_df)

# Usage example:
miba_filtered_data = filter_dataframes(miba_excels, earliest_records_df)
print(miba_filtered_data)

# Merge the two DataFrames based on the 'cpr' column
combined_data = pd.merge(earliest_records_df, miba_filtered_data, on='cpr', how='left')

# Display the combined DataFrame
print(combined_data) # TODO: OK


pato_miba_blood_combined_data = pd.merge(combined_data, new_filtered_blood_test_data, on='cpr', how='outer')
pato_miba_blood_combined_data
def move_columns(dataframe, insert_index, number_of_columns):
    """
    Move the last columns of a DataFrame to a specified index position.

    :param dataframe: The DataFrame whose columns need to be reordered.
    :param insert_index: The index at which the last columns need to be inserted.
    :param number_of_columns: Number of last columns to be moved.
    :return: DataFrame with reordered columns.
    """
    # Extract column names
    cols = list(dataframe.columns)

    # Select the order of columns
    new_order = cols[:insert_index] + cols[-number_of_columns:] + cols[insert_index:-number_of_columns]

    # Reorder the columns
    reordered_dataframe = dataframe[new_order]

    return reordered_dataframe

# Example usage:
pato_miba_blood_combined_data = move_columns(pato_miba_blood_combined_data, 5, 3)
print(pato_miba_blood_combined_data) # TODO: DEMO





# -----------------------------------------------------
# Convert to DataFrame
df_long = pd.DataFrame(diagnose_codes_in_columns_data)


# Function to aggregate diagnoses into a list of dictionaries
def aggregate_diagnoses(group):
    return [{
        "diagnosis_category": row["diagnosis_category"],
        "sub_diagnoses": row["sub_diagnoses"]
    } for _, row in group.iterrows()]


# Group by cpr and date, and aggregate diagnoses
aggregated = df_long.groupby(["cpr", "date"]).apply(aggregate_diagnoses)

# Convert back to DataFrame
df_single_row = pd.DataFrame(aggregated, columns=["diagnoses"]).reset_index()

# This DataFrame has one row per patient with a list of dictionaries storing the diagnoses information.
print(df_single_row)


def keep_earliest_records(data_frame):
    """
    Keep only the earliest record for each unique cpr.

    :param data_frame: Input DataFrame.
    :return: DataFrame with earliest records.
    """
    # Create a copy of the data frame
    df_copy = data_frame.copy()

    # Convert date to datetime for sorting
    df_copy['date'] = pd.to_datetime(df_copy['date'], format='%d.%m.%Y')

    # Sort by date
    df_copy = df_copy.sort_values(by='date')

    # Drop duplicates by cpr, keeping only the first (earliest) record
    df_copy = df_copy.drop_duplicates(subset='cpr', keep='first')

    # Convert date back to string in the desired format
    df_copy['date'] = df_copy['date'].dt.strftime('%d.%m.%Y')

    return df_copy


# Use the function
earliest_records_df = keep_earliest_records(df_single_row)

# Output the result
print(earliest_records_df)

# ------------------------------------------
# Convert to DataFrame
df = pd.DataFrame(df_single_row)

# Group by 'cpr' and combine the values in 'date' and 'diagnoses' columns
combined = df.groupby('cpr').agg({
    'date': list,
    'diagnoses': lambda x: [item for sublist in x for item in sublist]
}).reset_index()

print(combined)
