import pandas as pd


##################################################################################################################
def drop_column_by_index(input_path: str, column_index: int, output_path: str = "modified_dataset.csv") -> None:
    """
    Reads a CSV file, drops the specified column by its index, and saves the modified dataframe back to a CSV file.

    Parameters:
    - input_path (str): Path to the input CSV file.
    - column_index (int): Index of the column to be dropped (0-based index).
    - output_path (str, optional): Path to save the modified CSV file. Defaults to "modified_dataset.csv".

    Returns:
    None: The function saves the modified dataframe to a CSV file and does not return any value.
    """

    # Read the dataset
    df = pd.read_csv(input_path)

    # Drop the specified column by its index
    df.drop(df.columns[column_index], axis=1, inplace=True)

    # Save the modified dataset back to a .csv file
    df.to_csv(output_path, index=False)


# Drop cpr's column
# drop_column_by_index("Test_DATA_2023-09-18_0823.csv", 1, "modified_data_without_cpr.csv")
##################################################################################################################


##################################################################################################################
"""
We have columns with string representations of lists, and elements in the same position across these lists are correlated. 
For example, the first element in the miba_sample_type list is correlated with the first element in the miba_collection_date list for each record.
"""
import pandas as pd
import ast


def expand_section(df, section_cols):
    """
    Expand columns for a particular section that contain string representations of lists into multiple rows.

    Parameters:
    - df (DataFrame): Input DataFrame.
    - section_cols (list): Columns in the section containing string representations of lists.

    Returns:
    DataFrame: A DataFrame with expanded rows for the section.
    """

    def safe_literal_eval(s):
        if pd.isna(s):
            return []

        # Check if the string starts and ends with double quotes
        if s.startswith('"') and s.endswith('"'):
            s = s[1:-1]

        try:
            result = ast.literal_eval(s)
        except Exception as e:
            print(f"Error: {e}")

        return result

    # Convert string representation of lists to actual lists
    for col in section_cols:
        df[col] = df[col].apply(safe_literal_eval)

    # Use the 'explode' function to expand lists into rows for each column in the section
    for col in section_cols:
        df = df.explode(col)

    return df


def get_sections_by_keyword(df, keywords):
    """
    Group columns by their common prefixes (keywords).

    Parameters:
    - df (DataFrame): Input DataFrame.
    - keywords (list): List of keywords.

    Returns:
    List[List[str]]: List of lists of columns grouped by keywords.
    """
    sections = []
    for keyword in keywords:
        section = [col for col in df.columns if keyword in col]
        sections.append(section)
    return sections


import pandas as pd

# Reading the CSV file
file_path = "20_record_data.csv"
# df = pd.read_csv(file_path)
df = pd.read_csv(file_path, nrows=5)

# Define the list of columns to be removed
columns_to_remove = ['test_complete']

# Use the drop method to remove the specified columns
df = df.drop(columns=columns_to_remove)

# Get columns that start with 'blood'
blood_columns = [col for col in df.columns if col.lower().startswith('blood')]

# Include 'record_id' in the list of columns to be copied to df_blood
blood_columns_with_id = ['record_id'] + blood_columns

# Create new DataFrame with columns that start with 'blood' and 'record_id'
df_blood = df[blood_columns_with_id].copy()

# Drop only the 'blood' columns from the original DataFrame, keep 'record_id'
df.drop(columns=blood_columns, inplace=True)

# Now, df is the original DataFrame without the 'blood' columns, and df_blood is a new DataFrame containing only the 'blood' columns.


import ast
import pandas as pd

def validate_and_clean_item(item):
    """
    Validates and cleans individual list items.
    """
    cleaned_item = item.strip().strip("'\"")
    try:
        ast.literal_eval(f"'{cleaned_item}'")
    except SyntaxError:
        print(f"Error on: {cleaned_item}.")
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


# Convert the string representation of lists to actual lists using the safe function
for col in df.columns:
    df[col] = df[col].apply(safe_literal_eval)

# Initialize an empty dataframe to store the unstacked data
unstacked_data = []

for idx, row in df.iterrows():
    # Get the maximum length from the row elements that are lists
    max_len = max(len(item) if isinstance(item, list) else 0 for item in row)

    # For each length, create a new row dictionary
    for i in range(max_len):
        row_data = {'original_id': idx + 1}
        for col in df.columns:
            row_data[col] = row[col][i] if isinstance(row[col], list) and i < len(row[col]) else None

        unstacked_data.append(row_data)

# Convert the list of dictionaries to a DataFrame
unstacked_df = pd.DataFrame(unstacked_data)
unstacked_df.drop(columns=['record_id'], inplace=True)

# Replace NaN values with 'None'
unstacked_df.fillna('None', inplace=True)

# Replace empty strings with 'None'
unstacked_df.replace('', 'None', inplace=True)
import re

# Iterate over each column in the DataFrame, except 'original_id'
for column in unstacked_df.columns:
    if column == 'original_id':
        continue  # Skip the 'original_id' column

    # Replace '\n' with ' ' in each column
    # unstacked_df[column] = unstacked_df[column].apply(lambda x: x.replace('\n', '') if isinstance(x, str) else x)

    # Replace '\t' with '|' in each column
    unstacked_df[column] = unstacked_df[column].apply(lambda x: re.sub('\t+', '|', x) if isinstance(x, str) else x)

    # Normalize Data: Convert to lowercase and strip leading and trailing whitespaces
    unstacked_df[column] = unstacked_df[column].apply(lambda x: x.lower().strip() if isinstance(x, str) else x)

# Replace '|s' with 's' in the 'miba_resistance' column
unstacked_df['miba_resistance'] = unstacked_df['miba_resistance'].apply(
    lambda x: x.replace('|s', 's') if isinstance(x, str) else x
)

# Replace '|s' with 's' in the 'miba_resistance' column
unstacked_df['miba_resistance'] = unstacked_df['miba_resistance'].apply(
    lambda x: x.replace('|r', 'r') if isinstance(x, str) else x
)

# Fill NA/NaN values
unstacked_df.fillna('none', inplace=True)

# Normalize string data (excluding 'original_id' column)
str_columns = unstacked_df.select_dtypes(include=['object']).columns
str_columns = str_columns.difference(['original_id'])
unstacked_df[str_columns] = unstacked_df[str_columns].applymap(lambda x: x.lower().strip() if isinstance(x, str) else x)

# Ensure that the date columns are in a datetime format.
unstacked_df['miba_collection_date'] = pd.to_datetime(unstacked_df['miba_collection_date'], dayfirst=True, errors='coerce')
unstacked_df['medicine_start_date'] = pd.to_datetime(unstacked_df['medicine_start_date'], dayfirst=True, errors='coerce')
unstacked_df['medicine_end_date'] = pd.to_datetime(unstacked_df['medicine_end_date'], dayfirst=True, errors='coerce')
unstacked_df['diagnose_date'] = pd.to_datetime(unstacked_df['diagnose_date'], dayfirst=True, errors='coerce')
unstacked_df['pato_received_date'] = pd.to_datetime(unstacked_df['pato_received_date'], dayfirst=True, errors='coerce')
unstacked_df['vitale_measurement_date'] = pd.to_datetime(unstacked_df['vitale_measurement_date'], dayfirst=True, errors='coerce')


# Replace any digit followed by a dot either at the beginning of the string or after a newline character with an empty string
unstacked_df['miba_quantity'] = unstacked_df['miba_quantity'].replace(r'(^|\n)\d+\.', r'\1', regex=True)

"""
2. Exploratory Data Analysis (EDA):
2.1 Summary Statistics:
"""
pd.set_option('display.max_rows', 20)
pd.set_option('display.max_columns', 50)
pd.set_option('display.max_colwidth', None)

print(unstacked_df.describe(include='all'))  # include='all' will include statistics for all columns irrespective of their data type

"""
2.3 Categorical Data Analysis:

Explore the unique values and their counts for categorical columns.
"""
unstacked_df['miba_sample_type'].value_counts()

"""
4. Data Visualization:
Create meaningful visualizations like line plots, bar plots, pie charts, etc., based on the insights you gather.
"""
import matplotlib
# matplotlib.use('TkAgg')

import matplotlib.pyplot as plt

unstacked_df['miba_sample_type'].value_counts().plot(kind='bar')
plt.show()




# Define keywords for sections
keywords = ['miba', 'medicine', 'diagnose', 'pato', 'vital', 'blood']

# TODO:
# - Need a way to take a sample of data then compare it with the real
# - Try to remove bloods column and continue further
# - Find data analysis example over blood data

"""
# keywords = ['miba']

# Generate sections based on keywords
sections = get_sections_by_keyword(df, keywords)

# Transform the DataFrame by section
for section in sections:
    df = expand_section(df, section)
"""

# If you want to save the expanded data to a new CSV
# df.to_csv("expanded_data.csv", index=False)
##################################################################################################################