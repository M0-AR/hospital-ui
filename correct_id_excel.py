import numpy as np
import pandas as pd

# Define the function to check and replace 'nan' values
def check_nan(cell_value):
    if str(cell_value) == 'nan':
        return "nan"
    return cell_value

# Read the CSV file
df = pd.read_csv("Test_ImportTemplate_2023-09-08.csv", encoding='ISO-8859-1')

# Get the column name from the user
column_name = 'record_id'

# Check if the column exists
if column_name not in df.columns:
    print(f"Column '{column_name}' does not exist in the CSV!")
else:
    # Get the starting number from the user
    start_number = 1901

    # Update the 'record_id' column with incrementing numbers
    df['record_id'] = [i for i in range(start_number, start_number + len(df))]

    # Apply the function to each cell in the DataFrame
    df = df.applymap(check_nan)

    # Save the updated dataframe back to the CSV
    df.to_csv("Test_ImportTemplate_2023-09-08.csv", index=False, encoding='ISO-8859-1')
    print("Values in column 'record_id' changed successfully!")