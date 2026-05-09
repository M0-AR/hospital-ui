from renal_cancer_porject.utils.helper import read_excel_data_into_dataframe

try:
    # Read miba data
    miba_excels = read_excel_data_into_dataframe('miba.xlsx', '../data')
except FileNotFoundError as e:
    print(e)
except Exception as e:
    print(f"An unexpected error occurred: {e}")

print(miba_excels)