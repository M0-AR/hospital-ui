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


# Copy the 'cpr_pato_df_list' to 'cpr_pato_df_list_contain_codes'
cpr_pato_df_list_contain_TCodes = cpr_pato_df_list.copy()

# Apply the function to each row
cpr_pato_df_list_contain_TCodes = cpr_pato_df_list_contain_TCodes.apply(filter_row, axis=1)
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


# Create a copy of 'cpr_pato_df_list_contain_codes' dataframe to preserve the original data
cpr_pato_TCodes_oldestDate = cpr_pato_df_list_contain_TCodes.copy()

# Apply the 'keep_oldest_record_in_pato' function to each row
cpr_pato_TCodes_oldestDate = cpr_pato_TCodes_oldestDate.apply(keep_oldest_record_in_pato, axis=1)
# ------------------------------------

# -------------- Collect the following diagnose codes in multiple colomns -----------

def collect_diagnose_codes_in_columns(data):
    """
    Process the patients' data and collect specified diagnose codes into multiple columns.

    :param data: DataFrame containing patients' data with 'cpr' and 'patos' columns.
    :return: DataFrame with collected diagnose codes in multiple columns.
    """
    # List of columns
    diagnose_codes = [
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

    # Copy the original DataFrame and add new columns initialized with an empty string
    new_data = data.copy()
    for column in diagnose_codes:
        new_data[column] = ''

    # Iterating through each row of the DataFrame
    for idx, row in new_data.iterrows():
        diagnoser = row['pato_diagnoses']

        # Skip the row if the 'pato_diagnoses' value is NaN
        if pd.isnull(diagnoser):
            continue

        # Extract the column names and data from the diagnoses list
        for diagnose in diagnoser:
            column_name = diagnose.split('\n')[1].strip()
            column_data = '\n'.join(diagnose.split('\n')[2:]).strip()
            code = column_name.split()[0]  # Extract the code part

            # Adjust the condition to check for the code in the columns
            for column in diagnose_codes:
                if column.startswith(code):
                    new_data.at[idx, column] = column_data
                    break

    return new_data

# Call the function with the sample data
cpr_pato_TCodes_oldestDate_diagnoseCodes = collect_diagnose_codes_in_columns(cpr_pato_TCodes_oldestDate)
