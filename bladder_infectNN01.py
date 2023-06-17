import os
import pandas as pd


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

# Read data
pato_excels = read_excel_data_from_folders('pato_bank.xlsx')


def sample_dates_and_diagnoser(data):
    codes_to_look_for = [
        "T74940", # Urinblære, prostata og vesicula seminalis
        "T74000", # Urinblære
        "T74950", # Urinblære, vagina, uterus og adnexa
        "T74010", # Urinblæreslimhinde
        "T74030", # Urinblære, detrusor
        "T7432A", # Ureterostium, højre
        "T7432B", # Ureterostium, venstre
        "T75000", # Urethra
        "T75050", # Urethra, mand
        "T75060", # Urethra, kvinde
        "T75010", # Urethraslimhinde Urethrabiopsi
        "T75110", # Urethra pars prostatica
    ]

    samples = {}

    for key, df in data.items():
        for code in codes_to_look_for:
            # Filter rows that contain the code as substring
            filtered_rows = df[df['Diagnoser'].str.contains(code, na=False)]

            # If any rows contain the code, get the first one and add it to samples
            if not filtered_rows.empty:
                first_occurrence = filtered_rows.iloc[0]
                samples[f"{key}_{code}"] = {
                    "Date": first_occurrence["Modtaget"],
                    "Diagnoser": first_occurrence["Diagnoser"]
                }

    return samples

# Sample the date(s) and text
samples = sample_dates_and_diagnoser(pato_excels)


# 01
def process_patients_data(patients_data):
    # List of columns
    columns = [
        "cpr",
        "date",
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

    for cpr, patient_info in patients_data.items():
        date = patient_info['Date']
        diagnoser = patient_info['Diagnoser']

        # Split records within 'Diagnoser' by '[XX]' pattern
        records = [record.strip() for record in diagnoser.split('[') if record.strip()]

        for record in records:
            lines = record.split('\n')
            cpr_number = cpr.split('_')[0]  # Extracting CPR number from filename
            record_dict = {'cpr': cpr_number, 'date': date}

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
processed_data = process_patients_data(samples)

# Remove duplicates
# processed_data_no_duplicates = processed_data.drop_duplicates()


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
earliest_records_df = keep_earliest_records(processed_data)

# Output the result
print(earliest_records_df)

# ------------------------------------------------
# 02
import pandas as pd


def process_patient_data(patient_data):
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

    for cpr, patient_info in patient_data.items():
        date = patient_info['Date']
        diagnoser = patient_info['Diagnoser']

        # Split records within 'Diagnoser' by '[XX]' pattern
        record_entries = [record.strip() for record in diagnoser.split('[') if record.strip()]

        for record in record_entries:
            lines = record.split('\n')

            # Skip if there are not enough lines
            if len(lines) < 3:
                continue

            # Diagnosis category is in the second line
            diagnosis_category = lines[1].strip()

            # The rest of the lines are the sub-diagnoses
            sub_diagnoses = '\n'.join(lines[2:]).strip()

            # Extracting CPR number from filename
            cpr_number = cpr.split('_')[0]

            # Create record dictionary and add to list
            record_dict = {
                'cpr': cpr_number,
                'date': date,
                'diagnosis_category': diagnosis_category,
                'sub_diagnoses': sub_diagnoses
            }
            records.append(record_dict)

    # Convert the records list to a DataFrame
    data_frame = pd.DataFrame(records)

    return data_frame

processed_data = process_patient_data(samples)

# Remove duplicates
processed_data_no_duplicates = processed_data.drop_duplicates()

print(processed_data_no_duplicates)

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
earliest_records_df = keep_earliest_records(processed_data_no_duplicates)

# Output the result
print(earliest_records_df)

# -----------------------------------------------------
# Convert to DataFrame
df_long = pd.DataFrame(processed_data)

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