import pandas as pd
import ast
import numpy as np

# Read the data
df = pd.read_csv('combine_all_data.csv')

# ------------------- Convert string cells to list in selected columns ----------
# Select columns that start with "pato" or "cpr"
cpr_pato_columns = [col for col in df.columns if col.startswith(('cpr', 'pato'))]

# Create a new dataframe with only the selected columns
cpr_pato_df = df[cpr_pato_columns]


def convert_string_to_list(df):
    """
    Convert cells in all columns (except 'cpr') from string to list.

    Args:
    df (pd.DataFrame): DataFrame to modify.

    Returns:
    pd.DataFrame: DataFrame with modified columns.
    """
    df_copy = df.copy()  # Create a copy of the DataFrame
    for col in df.columns:
        if col != 'cpr':
            df_copy[col] = df[col].apply(lambda x: parse(x, col) if pd.notnull(x) else x)
    return df_copy


def parse(x, col):
    try:
        x = x.replace('nan', 'None')  # Replace 'nan' with 'None'
        return ast.literal_eval(x)
    except Exception as e:
        print(f"Failed to parse: {x} in column: {col}")
        return np.nan


# Usage
cpr_pato_df_list = convert_string_to_list(cpr_pato_df)

# End: Convert string cells to list in selected columns
# ----------------------------------------------------

# ------------- If one of these codes in the data exist then keep it --------------

# Define the codes you want to keep
codes_to_keep = ['T74940', 'T74000', 'T74950', 'T74010', 'T74030', 'T7432A', 'T7432B', 'T75000', 'T75050', 'T75060',
                 'T75010', 'T75110']

# Get only the relevant columns
pato_cols = ['pato_received_date', 'pato_service_provider', 'pato_request_number', 'pato_category', 'pato_diagnoses',
             'pato_material_description_of_smple', 'pato_conclusion', 'pato_microscopy', 'pato_other_investigations',
             'pato_macroscopy', 'pato_clinical_information']


# Define a function to filter all lists in a row based on 'pato_diagnoses' list
def filter_row(row):
    # Get the 'pato_diagnoses' list
    diagnoses = row['pato_diagnoses']
    # Check if 'diagnoses' is a list
    if isinstance(diagnoses, list):
        # Iterate over each item and its index in the 'pato_diagnoses' list
        for i in reversed(range(len(diagnoses))):
            # If the item doesn't contain any code in 'codes_to_keep', remove it and the corresponding item in all lists
            if not any(code in diagnoses[i] for code in codes_to_keep):
                for col in pato_cols:
                    del row[col][i]
    return row


# Apply the function to each row
cpr_pato_df_list_contain_codes = cpr_pato_df_list.apply(filter_row, axis=1)
# ----------------------------------------------------

# ------ Retrieve the earliest date from the data ------

from datetime import datetime


def keep_oldest_record_in_pato(row):
    dates = row['pato_received_date']

    # Check if 'dates' is a list and not empty
    if isinstance(dates, list) and len(dates) > 0:
        # Find the oldest date in the 'pato_received_date' list
        oldest_date = min(dates, key=lambda x: datetime.strptime(x, '%d.%m.%Y'))

        # Find the indices of all occurrences of the oldest date
        oldest_index = [i for i, date in enumerate(dates) if date == oldest_date]

        # Keep only the elements at the corresponding indices in each column
        for col in pato_cols:
            row[col] = [row[col][i] for i in oldest_index]

        # Update the 'pato_received_date' column with the oldest date repeated for the same number of occurrences
        row['pato_received_date'] = [oldest_date] * len(oldest_index)

    return row


# Apply the 'keep_oldest_record_in_pato' function to each row
cpr_pato_df_list_contain_codes_with_oldest_date = cpr_pato_df_list.apply(keep_oldest_record_in_pato, axis=1)