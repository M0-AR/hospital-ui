import pandas as pd
import ast
import numpy as np

# Read the data
df = pd.read_excel('combine_all_data.xlsx')

# ------------------- Convert string cells to list in selected columns ----------
# Select columns that start with "pato" or "cpr"
cpr_pato_columns = [col for col in df.columns if col.startswith(('cpr', 'pato'))]

# Create a new dataframe with only the selected columns
cpr_pato_df = df[cpr_pato_columns]


def validate_and_clean_item(item):
    """
    Validates and cleans individual list items.
    """
    cleaned_item = item.strip().strip("'\"")
    try:
        ast.literal_eval(f"'{cleaned_item}'")
    except SyntaxError:
        print(f"validate_and_clean_item(): Error on: {cleaned_item}.")
        cleaned_item = cleaned_item.replace("'", r"\'")
    return cleaned_item

def check_individual_items(string_list_repr):
    """
    Processes a string representing a list, attempting to validate and clean each item.
    """
    items = string_list_repr.strip('[]').split(',')
    return [validate_and_clean_item(item) for item in items]

def handle_malformed_string(s):
    """
    Fixes common malformed patterns in the string.
    """
    # Remove trailing , ']'
    if s.endswith(', \']'):
        s = s[:-3] + ']'
    # Remove trailing comma before ']'
    if s.endswith(',]'):
        s = s[:-2] + ']'
    return s

def safe_literal_eval(s):
    """
    Attempts to convert a string representation of lists to an actual list.
    """
    if pd.isna(s):
        return []

    s = str(s).strip("'\"")  # Remove surrounding single or double quotes

    s = handle_malformed_string(s)

    try:
        return ast.literal_eval(s)
    except SyntaxError:
        return check_individual_items(s)

def parse(x, col):
    try:
        x = x.replace('nan', 'None')  # Replace 'nan' with 'None'
        # return ast.literal_eval(x)
        return safe_literal_eval(x)
    except Exception as e:
        print(f"Failed to parse column: {col}")
        return np.nan

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

# Usage
cpr_pato_df_list = convert_string_to_list(cpr_pato_df)

# End: Convert string cells to list in selected columns
# ----------------------------------------------------

# ------------- If one of these codes in the data exist then keep it --------------

# Get only the relevant columns
pato_cols = [col for col in df.columns if col.startswith('pato')]

# Define a function to filter all lists in a row based on 'pato_diagnoses' list
def filter_row_based_on_pato_diagnoses(row):
    # Define the codes you want to keep
    codes_to_keep_01 = ['T74940', 'T74000', 'T74950', 'T74010', 'T74030', 'T7432A', 'T7432B', 'T75000', 'T75050', 'T75060',
                        'T75010', 'T75110']

    # Get the 'pato_diagnoses' list
    diagnoses = row['pato_diagnoses']
    # Check if 'diagnoses' is a list
    if isinstance(diagnoses, list):
        # Iterate over each item and its index in the 'pato_diagnoses' list
        for i in reversed(range(len(diagnoses))):
            # If the item doesn't contain any code in 'codes_to_keep_01' or 'codes_to_keep_02', remove it and the
            # corresponding item in all lists
            if not any(code in diagnoses[i] for code in codes_to_keep_01): #\ 
                    # and not any(code in diagnoses[i] for code in codes_to_keep_02):
                for col in pato_cols:
                    del row[col][i]
    return row


# Copy the 'cpr_pato_df_list' to 'cpr_pato_df_list_contain_TCodes'
cpr_pato_df_list_contain_TCodes = cpr_pato_df_list.copy()

# Apply the function to each row
cpr_pato_df_list_contain_TCodes = cpr_pato_df_list_contain_TCodes.apply(filter_row_based_on_pato_diagnoses, axis=1)  # ----------------------------------------------------
# cpr_pato_df_list_contain_TCodes.to_excel('cpr_pato_TCodes_oldestDate_new_method.xlsx', index=False)
# cpr_pato_df_list_contain_TCodes.to_excel('cpr_pato_TCodes_oldestDate_old_method.xlsx', index=False)
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

# -------------- Collect the following diagnose codes in multiple columns with sampling the rest of the text

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
        "M69760 malignitetssuspekte celler",
        "ÆF1810 pTis",
        "ÆF181a pTa",
        "ÆF1820 pT0",
        "ÆF1830 pT1",
        "ÆF1831 pT1a",
        "ÆF1832 pT1b",
        "ÆF1840 pT2",
        "ÆF1841 pT2a",
        "ÆF1842 pT2b",
        "ÆF1850 pT3",
        "ÆF1861 pT4a",
        "ÆF1862 pT4b",
        "ÆF1870 pTx",
        "ÆF1900 pN0",
        "ÆF1910 pN1",
        "ÆF1920 pN2",
        "ÆF1930 pN3",
        "ÆF1950 pNx"
    ]

    # Copy the original DataFrame and add new columns initialized with an empty string
    new_data = data.copy()
    for column in diagnose_codes:
        new_data[column] = ''

    # Initialize new columns with 'No'
    for code in diagnose_codes:
        new_data[code] = 'No'

    # Iterate through each row of the DataFrame
    for idx, row in new_data.iterrows():
        diagnoses = row['pato_diagnoses']

        # Skip the row if the 'pato_diagnoses' value is NaN
        if pd.isnull(diagnoses):
            continue

        # Check for the presence of each code in 'diagnoser' and update the corresponding column with 'Yes' if found
        for code in diagnose_codes:
            for diagnose in diagnoses:
                if code in diagnose:
                    new_data.at[idx, code] = 'Yes'

    return new_data


# Call the function with the sample data
cpr_pato_TCodes_oldestDate_diagnoseCodes_df = collect_diagnose_codes_in_columns(cpr_pato_TCodes_oldestDate)



# cpr_pato_TCodes_oldestDate_diagnoseCodes_df = convert_string_to_list(cpr_pato_TCodes_oldestDate_diagnoseCodes_df) 
# cpr_pato_TCodes_oldestDate_diagnoseCodes_df.to_excel('test_01.xlsx', index=False)
# TODO one cell has two diagnoseCodes where to 'sample the rest of the text'
# TODO docs: if the cell contain '\n[1] \n[3] \n[5]' that mean we found diagnose's code but there is no rest of the text to sample
# Select columns that start with "miba" or "cpr"
cpr_miba_columns = [col for col in df.columns if col.startswith(('cpr', 'miba'))]

# Create a new dataframe with only the selected columns
cpr_miba_df = df[cpr_miba_columns]

# Usage
cpr_miba_df_list = convert_string_to_list(cpr_miba_df)

# Remove unwanted columns
cpr_miba_df_list = cpr_miba_df_list[['cpr', 'miba_sample_type', 'miba_collection_date', 'miba_quantity']]

# Get only the relevant miba columns
miba_cols = [col for col in df.columns if col.startswith(('miba'))]
# ----------------------------------------

# Column A (“Prøvens art”) – only data concerning:
# ⦁	Blod … (Blod, Blod (bloddyrkningskolbe, etc)
# ⦁	Urin … (Urin, Urin – midtstråle, etc)


def filter_df_based_on_codes(df, codes_to_keep, cols_to_filter, filter_by_col_list):
    """
    Function to filter DataFrame rows based on specific codes.

    This function filters the DataFrame 'df' such that for each row, if a list
    item in the column 'list_col' does not contain any of the 'codes_to_keep',
    it removes that list item and corresponding list items from the other columns
    specified in 'cols_to_filter'.

    Parameters:
    df (pd.DataFrame): The DataFrame to filter.
    codes_to_keep (list): The list of codes to check for in each list item of 'list_col'.
    cols_to_filter (list): The list of column names whose corresponding list items should be removed.
    filter_by_col_list (str): The column name that contains the lists to be checked against 'codes_to_keep'.

    Returns:
    df_copy (pd.DataFrame): A copy of the original DataFrame after filtering.
    """
    # Make a copy of the DataFrame to prevent modifications on the original
    df_copy = df.copy()

    # Iterate over DataFrame rows
    for index, row in df_copy.iterrows():
        # Get the list from the specified column
        list_data = row[filter_by_col_list]

        # If the data is a list, proceed with filtering
        if isinstance(list_data, list):
            # Iterate over each item and its index in the list
            for i in reversed(range(len(list_data))):
                # If the list item doesn't contain any code in 'codes_to_keep'
                # remove it and corresponding items from all columns in 'cols_to_filter'
                if not any(code in list_data[i] for code in codes_to_keep):
                    for col in cols_to_filter:
                        # Check if the column exists in the DataFrame
                        if col in df_copy.columns:
                            del df_copy.at[index, col][i]

    # Return the filtered DataFrame
    return df_copy


miba_sample_type_keywords_to_keep = ['Blod', 'Urin']



cpr_miba_filterByKeywords = filter_df_based_on_codes(cpr_miba_df_list, miba_sample_type_keywords_to_keep, miba_cols, 'miba_sample_type')

# ---------------------------------

# If “Kvantitet” is empty = Negative

def replace_none_in_list(df, keyword):
    """
    Function to replace 'None' values in lists within all DataFrame columns.

    This function goes through each row of the DataFrame 'df' and each column,
    checks the list in the column and replaces 'None' values with the provided 'keyword'.

    Parameters:
    df (pd.DataFrame): The DataFrame to manipulate.
    keyword (str): The string to replace 'None' values with.

    Returns:
    df_copy (pd.DataFrame): A copy of the original DataFrame after replacement.
    """
    # Make a copy of the DataFrame to prevent modifications on the original
    df_copy = df.copy()

    # Iterate over DataFrame rows
    for index, row in df_copy.iterrows():
        # Iterate over each column
        for column_name in df_copy.columns:
            # Get the list from the current column
            list_data = row[column_name]

            # If the data is a list, proceed with replacement
            if isinstance(list_data, list):
                # Replace 'None' with 'keyword' in the list
                df_copy.at[index, column_name] = [item if item is not None else keyword for item in list_data]

    # Return the DataFrame with replaced values
    return df_copy

cpr_miba_filterByKeywords_NoneToNegative = replace_none_in_list(cpr_miba_filterByKeywords, 'Negative')
# ----------------------------------------
# Filter the miba DataFrame based on the miba_collection_date column so that only records that occurred before the pato_received_date in the pato DataFrame are kept.
def parse_string(x):
    try:
        x = x.replace('nan', 'None')  # Replace 'nan' with 'None'
        return ast.literal_eval(x)
    except Exception as e:
        print(f"Failed to parse: {x}")
        return None

def convert_dates(date_list):
    # Check if date_list is not iterable (float, None etc.)
    if isinstance(date_list, str):
        date_list = parse_string(date_list)

    if not isinstance(date_list, list):
        return []

    # Converts a list of strings to datetime, ignoring non-dates and None values
    return [pd.to_datetime(date) for date in date_list if pd.to_datetime(date, errors='coerce') is not pd.NaT]

# Apply the function to each row of 'miba_collection_date' and 'pato_received_date'
cpr_miba_filterByKeywords_NoneToNegative['miba_collection_date'] = cpr_miba_filterByKeywords_NoneToNegative['miba_collection_date'].apply(convert_dates)

cpr_pato_TCodes_oldestDate_diagnoseCodes_df['pato_received_date'] = cpr_pato_TCodes_oldestDate_diagnoseCodes_df['pato_received_date'].apply(convert_dates)

def filter_by_date(df1, df2, id_col, date_col_df1, date_col_df2, cols_to_filter):
    """
    Filters df1 to only include elements where the date in date_col_df1 is earlier than the date in date_col_df2 in df2 for a matching id_col.

    Parameters:
    df1 (pd.DataFrame): The first DataFrame. Expected to contain id_col and date_col_df1 columns.
    df2 (pd.DataFrame): The second DataFrame. Expected to contain id_col and date_col_df2 columns.
    cols_to_filter (list): The list of columns in df1 to filter based on the dates.

    Returns:
    df1_filtered (pd.DataFrame): A filtered version of df1.
    """
    # Make a copy of df1 to prevent modifications on the original
    df1_filtered = df1.copy()

    # Iterate over the rows of df1
    for index, row in df1.iterrows():
        id_val = row[id_col]

        # Find the corresponding row in df2
        df2_row = df2[df2[id_col] == id_val]

        # If there is no corresponding row in df2, drop the row from df1
        if df2_row.empty:
            df1_filtered = df1_filtered.drop(index)
            continue

        # Get the dates from df1 and df2
        dates_df1 = row[date_col_df1]
        # Get the first (and only) date from date_col_df2 or None if the list is empty
        date_df2 = df2_row.iloc[0][date_col_df2][0] if df2_row.iloc[0][date_col_df2] else None

        # Iterate over each date in dates_df1 and its index in reverse order
        for i in reversed(range(len(dates_df1))):
            # If date_df2 is None or if the date in dates_df1 is not earlier than date_df2, remove the
            # corresponding elements from all columns in cols_to_filter
            if date_df2 is None or dates_df1[i] >= date_df2:
                for col in cols_to_filter:
                    # Check if the column exists in the DataFrame
                    if col in df1_filtered.columns:
                        del df1_filtered.at[index, col][i]

    return df1_filtered


# Use the function to filter cpr_miba_filterByKeywords_NoneToNegative
filtered_miba_by_date_before_pato = filter_by_date(cpr_miba_filterByKeywords_NoneToNegative, cpr_pato_TCodes_oldestDate_diagnoseCodes_df,
                                                   'cpr', 'miba_collection_date', 'pato_received_date', miba_cols)

# Merge the filtered DataFrame with cpr_pato_TCodes_oldestDate_diagnoseCodes_df
cpr_pato_miba = pd.merge(filtered_miba_by_date_before_pato, cpr_pato_TCodes_oldestDate_diagnoseCodes_df, on='cpr')

# ---------------------------------------
# ---------------------------------------
# ---------------------------------------
def convert_dates(date_list):
    # Check if date_list is not iterable (float, None etc.)
    if not isinstance(date_list, list):
        return []

    # Converts a list of strings to datetime, ignoring non-dates and None values
    return [pd.to_datetime(date) for date in date_list if pd.to_datetime(date, errors='coerce') is not pd.NaT]

# Select columns that start with "blood" or "cpr"
cpr_blood_columns = [col for col in df.columns if col.startswith(('cpr', 'blood'))]

# Create a new dataframe with only the selected columns
cpr_blood_df = df[cpr_blood_columns]


# # Convert the string representation of lists to actual lists using the safe function
# for col in blood_cols:
#     cpr_blood_df[col] = cpr_blood_df[col].apply(safe_literal_eval)

# Usage
cpr_blood_df_list = convert_string_to_list(cpr_blood_df)
# cpr_blood_df_list = cpr_blood_df
# ---------------------------------------

# Only data concerning
keywords = ['Hæmoglobin', 'Leukocytter', 'Neutrophilocytter', 'CRP', 'kreatinin', 'natrium', 'kalium', 'trombocytter', 'LDH']

def filter_lists(df, cols, keywords):
    """
    This function takes a DataFrame, column names, and a list of keywords. It filters out entries in the specified
    columns of the DataFrame that do not contain any of the keywords.

    Parameters:
    df (pd.DataFrame): DataFrame containing the columns.
    cols (List[str]): List of column names to filter.
    keywords (List[str]): List of keywords to filter the contents.

    Returns:
    pd.DataFrame: The DataFrame with filtered content.
    """

    # Iterate over each row in DataFrame
    for idx, row in df.iterrows():

        # Initialize a dictionary to store new lists for each column
        new_lists = {col: [] for col in cols}

        # Check if all items in cols are lists, if not, continue to next iteration
        if not all(isinstance(row[col], list) for col in cols):
            continue

        # Find the minimum length of lists in the current row, to avoid out-of-range errors
        min_len = min(len(row[col]) for col in cols)

        # Iterate over elements in the lists in the current row
        for i in range(min_len):

            # Check if any keyword is in the content of all columns for current index
            if any(keyword in row[col][i] for keyword in keywords for col in cols):

                # If yes, append the element at current index to the new list for each column
                for col in cols:
                    new_lists[col].append(row[col][i])

        # Replace the old lists with new filtered lists in the DataFrame
        for col in cols:
            df.at[idx, col] = new_lists[col]

    return df


# Merge blood columns 
blood_date_cols = [col for col in cpr_blood_df_list.columns if col.startswith('blood_date')]
blood_content_cols = [col for col in cpr_blood_df_list.columns if col.startswith('blood_content')]

cpr_blood_df_list['blood_date'] = None
cpr_blood_df_list['blood_content'] = None

for index, row in cpr_blood_df_list.iterrows():
    merged_date_list = []
    merged_content_list = []

    for col in blood_date_cols:
        row_data = row[col]
        if isinstance(row_data, list):
            merged_date_list.extend(row_data)
    for col in blood_content_cols:
        row_data = row[col]
        if isinstance(row_data, list):
            merged_content_list.extend(row_data)

    cpr_blood_df_list.at[index, 'blood_date'] = merged_date_list
    cpr_blood_df_list.at[index, 'blood_content'] = merged_content_list
 
# Remove undesire columns
blood_date_cols = [col for col in cpr_blood_df_list.columns if col.startswith('blood_date_')]
blood_content_cols = [col for col in cpr_blood_df_list.columns if col.startswith('blood_content_')]
cpr_blood_df_list = cpr_blood_df_list.drop(columns=blood_date_cols + blood_content_cols)

# Fliter 
blood_cols = [col for col in cpr_blood_df_list.columns if col.startswith(('blood'))]
cpr_blood_codes_filter = filter_lists(cpr_blood_df_list, blood_cols, keywords)

cpr_blood_codes_filter['blood_date'] = cpr_blood_codes_filter['blood_date'].apply(convert_dates)
cpr_blood_filter_by_codes_and_dates = filter_by_date(cpr_blood_codes_filter, cpr_pato_miba, 'cpr', 'blood_date',  'pato_received_date', blood_cols)

# Merge two dataframe
cpr_pato_miba_blood = pd.merge(cpr_blood_filter_by_codes_and_dates, cpr_pato_miba, on='cpr')

# ----------------------------------------
# ----------------------------------------
# ----------------------------------------

# Select columns that start with "medicine" or "cpr"
cpr_medicine_columns = [col for col in df.columns if col.startswith(('cpr', 'medicine'))]

# Create a new dataframe with only the selected columns
cpr_medicine_df = df[cpr_medicine_columns]

medicine_cols = [col for col in df.columns if col.startswith(('medicine'))]
# Usage
cpr_medicine_df_list = convert_string_to_list(cpr_medicine_df)
# ---------------------------------------

medicine_keywords = [
    "Mod infektion", "Mod urinvejsinfektion",
    "Mod blærebetændelse", "Pivmecillinam",
    "Amoxicillin", "Trimopan", "Sulfamethizol",
    "Ciprofloxacin", "Gentamicin", "Piperacillin",
    "Cefuroxim", "Meropenem"
]

cpr_medicine_filter_by_kewords = filter_lists(cpr_medicine_df_list, medicine_cols, medicine_keywords)

# Merge two dataframe
cpr_pato_miba_blood_medicine = pd.merge(cpr_medicine_filter_by_kewords, cpr_pato_miba_blood, on='cpr')

# ----------------------------------------
# ----------------------------------------
# ----------------------------------------

# Select columns that start with "diagnose" or "cpr"
cpr_diagnose_columns = [col for col in df.columns if col.startswith(('cpr', 'diagnose'))]

# Create a new dataframe with only the selected columns
cpr_diagnose_df = df[cpr_diagnose_columns]

diagnose_cols = [col for col in df.columns if col.startswith(('diagnose'))]

# Usage
cpr_diagnose_df_list = convert_string_to_list(cpr_diagnose_df)

# Merge two dataframe
cpr_pato_miba_blood_medicine_diagnose = pd.merge(cpr_diagnose_df_list, cpr_pato_miba_blood_medicine, on='cpr')

# ----------------------------------------
# ----------------------------------------
# ----------------------------------------

# Select columns that start with "vitale" or "cpr"
cpr_vitale_columns = [col for col in df.columns if col.startswith(('cpr', 'vitale'))]

# Create a new dataframe with only the selected columns
cpr_vitale_df = df[cpr_vitale_columns]

vitale_cols = [col for col in df.columns if col.startswith(('vitale'))]

# Usage
cpr_vitale_df_list = convert_string_to_list(cpr_vitale_df)

# TODO: The closest test prior to the index date -> 'closest'?
# Merge two dataframe
cpr_pato_miba_blood_medicine_diagnose_vitale = pd.merge(cpr_vitale_df_list, cpr_pato_miba_blood_medicine_diagnose, on='cpr')

cpr_pato_miba_blood_medicine_diagnose_vitale.to_excel('bladder_infect_data.xlsx', index=False)
