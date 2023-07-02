import os
import pandas as pd


def format_dataframe(dataframe, keyword):
    formatted_text = ""
    for index, row in dataframe.iterrows():
        for column in dataframe.columns:
            cell_value = str(row[column])
            formatted_text += f"{column}: "
            start = 0
            while True:
                start = cell_value.lower().find(keyword.lower(), start)
                if start == -1:
                    break
                end = start + len(keyword)
                formatted_text += cell_value[:start]
                formatted_text += f"[[[{cell_value[start:end]}]]]"
                cell_value = cell_value[end:]
                start = end - len(keyword)
            formatted_text += cell_value + "\t"
        formatted_text += "\n----------------------\n"  # Add a separator between rows
    return formatted_text


def read_all_excel_data():
    data = {}
    patient_dirs = [dir_name for dir_name in os.listdir('HospitalData') if
                    os.path.isdir(os.path.join('HospitalData', dir_name))]

    for patient_id in patient_dirs:
        patient_directory = os.path.join('HospitalData', patient_id)
        excel_files = [f for f in os.listdir(patient_directory) if f.endswith('.xlsx') and f != 'blood_test.xlsx']

        for file in excel_files:
            filepath = os.path.join(patient_directory, file)
            df = pd.read_excel(filepath, header=0)
            data[f"{patient_id}_{file}"] = df

    return data


def search_keyword_all(data_all, keyword):
    cpr_list = []  # To store CPR numbers where results were found
    results = []

    for filename, df in data_all.items():
        rows_with_keyword = df[df.apply(lambda row: row.astype(str).str.contains(keyword, regex=False).any(), axis=1)]
        if not rows_with_keyword.empty:
            cpr_number = filename.split('_')[0]  # Extracting CPR number from filename
            cpr_list.append(cpr_number)  # Storing CPR number

            result = f"-----------------------------------------\n"
            result += f"Results found in {filename}:\n"
            result += f"-----------------------------------------\n"
            formatted_rows = format_dataframe(rows_with_keyword, keyword)
            start = 0
            while True:
                start = formatted_rows.find("[[[", start)
                if start == -1:
                    break
                result += formatted_rows[:start]
                result += formatted_rows[start + 3:start + 3 + len(keyword)]
                formatted_rows = formatted_rows[start + 3 + len(keyword):]
                start = 0
            result += formatted_rows + "\n\n"
            results.append(result)

    return cpr_list, results


keyword = 'YY113'
cpr_list, results = search_keyword_all(read_all_excel_data(), keyword)


def read_excel_data(cpr_list, file):
    data = {}

    for cpr_number in cpr_list:
        patient_directory = os.path.join('HospitalData', cpr_number)
        filepath = os.path.join(patient_directory, file)
        if not os.path.isfile(filepath):
            continue  # Skip if the file does not exist
        df = pd.read_excel(filepath, header=0)
        data[f"{cpr_number}_{file}"] = df

    return data


pato_excels = read_excel_data(cpr_list, 'pato_bank.xlsx')  # Key, Value


def search_keyword_in_data(data, keyword):
    results = {}  # Key: CPR number, Value: data

    for filename, df in data.items():
        rows_with_keyword = df[df.apply(lambda row: row.astype(str).str.contains(keyword, regex=False).any(), axis=1)]
        if not rows_with_keyword.empty:
            cpr_number = filename.split('_')[0]  # Extracting CPR number from filename
            if cpr_number not in results:
                results[cpr_number] = {}
            for index, row in rows_with_keyword.iterrows():
                date = row['Modtaget']
                keyword_cell = row[row.astype(str).str.contains(keyword, na=False)].index[0]
                results[cpr_number][date] = row[keyword_cell]

    return results


"""
for cpr_number, data in extract_dates_and_diagnoses.items():
    for date, value in data.items():
        # Perform operations with the CPR number, date, and value
"""
extract_dates_and_diagnoses = search_keyword_in_data(pato_excels, keyword)


def extract_cpr_dates(data):
    extracted_cpr_dates = {}

    for cpr_number, dates in data.items():
        if cpr_number not in extracted_cpr_dates:
            extracted_cpr_dates[cpr_number] = []
        extracted_cpr_dates[cpr_number].extend(dates)

    return extracted_cpr_dates


extracted_cpr_dates = extract_cpr_dates(extract_dates_and_diagnoses)

miba_excels = read_excel_data(cpr_list, 'miba.xlsx')  # Key, Value

from datetime import datetime
from collections import defaultdict


def filter_dataframes(miba_excels, cpr_dates_dict):
    filtered_data = defaultdict(list)  # Use defaultdict to automatically initialize an empty list for each CPR number

    for cpr_number, dates in cpr_dates_dict.items():
        min_date = min(dates)  # Calculate the minimum date for the current CPR number
        min_date_obj = datetime.strptime(min_date, '%d.%m.%Y')  # Convert min_date to datetime object

        if cpr_number not in filtered_data:
            filtered_data[cpr_number] = []

        for filename, df in miba_excels.items():
            if filename.startswith(cpr_number):
                # Convert the 'Prøvens art' column to datetime objects with errors='coerce'
                df['Taget d.'] = pd.to_datetime(df['Taget d.'], format='%d.%m.%Y')
                filtered_rows = df[df['Taget d.'] < min_date_obj][['Prøvens art', 'Taget d.']]
                if not filtered_rows.empty:
                    filtered_data[cpr_number].append(filtered_rows)

    return filtered_data


filtered_data = filter_dataframes(miba_excels, extracted_cpr_dates)

for cpr_number, dataframes in filtered_data.items():
    print("CPR Number:", cpr_number)
    for dataframe in dataframes:
        print(dataframe)
        print()
