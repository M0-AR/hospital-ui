import pandas as pd
import traceback
import os
import re

subtype_mapping = {
    "M82603": "papillært adenokarcinom",
    "M82900": "onkocytom (oksyfilt adenom)",
    "M829A1": "onkocytær tumor NOS",
    "M83103": "clear cell adenokarcinom",
    "M83113": "fumarat hydratase-deficient renalcellekarcinom",
    "M83123": "uklassificerbart renalcellekarcinom",
    "M83161": "multilokulær cystisk clear cell neoplasi, lavt malignitetspotentiale",
    "M83163": "tubulocystisk renalcellekarcinom",
    "M83173": "kromofobt renalcellekarcinom",
    "M83193": "samlerørskarcinom",
    "M831A3": "mucinøst tubulært og spindle cell karcinom",
    "M831D3": "succinat dehydrogenase-deficient renalcellekarcinom",
    "M831E3": "erhvervet cystisk nyresygdom-associeret renalcellekarcinom",
    "M831F3": "eosinofilt solidt og cystisk renalcellekarcinom",
    "M831G3": "TFE3-rearrangeret renalcellekarcinom",
    "M831H3": "TFEB-ændret renalcellekarcinom",
    "M831J3": "ELOC-muteret renalcellekarcinom",
    "M831K3": "ALK-rearrangeret renalcellekarcinom",
    "M83231": "clear cell papillær renalcelletumor",
    "M83250": "metanefrisk adenom",
    "M84803": "mucinøst adenokarcinom",
    "M84903": "Signetringscellekarcinom",
    "M73050": "onkocytær metaplasi"
}

leibovich_score_mapping = {
    "ÆF000B": "Leibovich score 0",
    "ÆF001B": "Leibovich score 1",
    "ÆF002B": "Leibovich score 2",
    "ÆF003B": "Leibovich score 3",
    "ÆF004B": "Leibovich score 4",
    "ÆF005B": "Leibovich score 5",
    "ÆF006B": "Leibovich score 6",
    "ÆF007B": "Leibovich score 7",
    "ÆF008B": "Leibovich score 8",
    "ÆF009B": "Leibovich score 9",
    "ÆF010B": "Leibovich score 10",
    "ÆF011B": "Leibovich score 11"
}

resection_range_mapping = {
    "M09400": "resektionsrande frie",
    "M09401": "resektionsrande ikke frie",
    "M09402": "resektionsrande kan ikke vurderes",
    # TODO: it was without 'e' at the end -> 'resektionsrand kan ikke vurderes' what is the correct with or without 'e'?
    "M09405": "resektionsflade fri",
    "M09406": "resektionsflade ikke fri",
    "M09407": "resektionsflade kan ikke vurderes",
    "M0940A": "resektionsafstand tilstrækkelig",
    "M0940B": "resektionsafstand ikke tilstrækkelig",
    "M0940P": "adenom i resektionsrand"
}

fuhrman_grade_mapping = {
    "ÆYYX10": "grad 1",
    "ÆYYX20": "grad 2",
    "ÆYYX30": "grad 3",
    "ÆYYX40": "grad 4",
    "ÆYYX50": "grad 5"
}

who_grade_mapping = {
    "ÆYYYH1": "WHO grad 1",
    "ÆYYYH2": "WHO grad 2",
    "ÆYYYH3": "WHO grad 3",
    "ÆYYYH4": "WHO grad 4",
    "ÆYYYH5": "WHO grad 5"
}

isup_mapping = {
    "ÆF0601": "ISUP grad 1",
    "ÆF0602": "ISUP grad 2",
    "ÆF0603": "ISUP grad 3",
    "ÆF0604": "ISUP grad 4",
    "ÆF0605": "ISUP grad 5"
}

sarkomatoid_mapping = {
    "ÆYYY0V": "sarkomatoid"
}

t_stage_mapping = {
    "ÆF1800": "pT",
    "ÆF1810": "pTis",
    "ÆF181A": "pTa",
    "ÆF1820": "pT0",
    "ÆF1830": "pT1",
    "ÆF1831": "pT1a",
    "ÆF1832": "pT1b",
    "ÆF1833": "pT1c",
    "ÆF1834": "pT1a1",
    "ÆF1835": "pT1a2",
    "ÆF1836": "pT1b1",
    "ÆF1837": "pT1b2",
    "ÆF1838": "pT1d",
    "ÆF1839": "pT1mi",
    "ÆF183A": "pT1c1",
    "ÆF183B": "pT1c2",
    "ÆF183C": "pT1c3",
    "ÆF1840": "pT2",
    "ÆF1841": "pT2a",
    "ÆF1842": "pT2b",
    "ÆF1843": "pT2c",
    "ÆF1844": "pT2d",
    "ÆF1845": "pT2a1",
    "ÆF1846": "pT2a2",
    "ÆF1850": "pT3",
    "ÆF1851": "pT3a",
    "ÆF1852": "pT3b",
    "ÆF1853": "pT3c",
    "ÆF1854": "pT3d",
    "ÆF1860": "pT4",
    "ÆF1861": "pT4a",
    "ÆF1862": "pT4b",
    "ÆF1863": "pT4c",
    "ÆF1864": "pT4d",
    "ÆF1870": "pTx"
}

n_stage_mapping = {
    "ÆF1900": "pN0",
    "ÆF1902": "pN0(i+)",
    "ÆF1903": "pN0(mol-)",
    "ÆF1904": "pN0(mol+)",
    "ÆF1905": "pN0(sn)",
    "ÆF1906": "pN0(i+)(sn)",
    "ÆF1907": "pN0(mol-)(sn)",
    "ÆF1908": "pN0(mol+)(sn)",
    "ÆF1910": "pN1",
    "ÆF1911": "pN1a",
    "ÆF1912": "pN1b",
    "ÆF1913": "pN1c",
    "ÆF1914": "pN1(mi)",
    "ÆF1915": "pN1(sn)",
    "ÆF1916": "pN1(mi)(sn)",
    "ÆF1917": "pN1a(sn)",
    "ÆF1918": "pN1b(sn)",
    "ÆF1919": "pN1c(sn)",
    "ÆF1920": "pN2",
    "ÆF1921": "pN2a",
    "ÆF1922": "pN2b",
    "ÆF1923": "pN2(sn)",
    "ÆF1924": "pN2a(sn)",
    "ÆF1925": "pN2b(sn)",
    "ÆF1930": "pN3",
    "ÆF1931": "pN3a",
    "ÆF1932": "pN3b",
    "ÆF1933": "pN3c",
    "ÆF1940": "pN4",
    "ÆF1950": "pNx"
}

m_stage_mapping = {
    "ÆF2000": "pM0",
    "ÆF2001": "pM0(i+)",
    "ÆF2004": "pM0(mol+)",
    "ÆF2010": "pM1",
    "ÆF2011": "pM1a",
    "ÆF2012": "pM1b",
    "ÆF2013": "pM1c",
    "ÆF2014": "pM1d",
    "ÆF2050": "pMx"
}

nekroser_mapping = {
    "M54000": "nekrose"
}

mappings = {
    "Subtype": subtype_mapping,
    "LeibovichScore": leibovich_score_mapping,
    "ResectionRange": resection_range_mapping,
    "FuhrmanGrade": fuhrman_grade_mapping,
    "WHOScore": who_grade_mapping,
    "ISUPGrade": isup_mapping,
    "Sarkomatoid": sarkomatoid_mapping,
    "TStage": t_stage_mapping,
    "NStage": n_stage_mapping,
    "MStage": m_stage_mapping,
    "Nekroser": nekroser_mapping
}


def parse_diagnosis_detail(diagnosis_details, mapping_dict):
    """
    Parses the diagnosis details based on a provided mapping dictionary.

    Parameters:
    diagnosis_details (str): The string containing diagnosis codes.
    mapping_dict (dict): A dictionary mapping codes to their descriptions.

    Returns:
    tuple: A tuple containing the code and its corresponding description.
           Returns (None, None) if no match is found.
    """
    for code, description in mapping_dict.items():
        if code in diagnosis_details:
            return code, description
    return None, None  # Return a tuple with both elements as None if no match is found


def extract_details_from_other(other_text):
    """
    Extracts additional details from the 'Other' text and returns a dictionary of the parsed fields.

    Parameters:
    other_text (str): The text to parse.

    Returns:
    dict: Dictionary containing parsed data.
    """
    mappings = {
        "TumorSize": {
            "ÆTD": {"pattern": r"ÆTD(\d{3})\s*tumordiameter (\d+ mm)", "group": 1}
        },
        "Side": {
            "T71010": {"pattern": "T71010 Højre nyre", "group": 0},
            "T71020": {"pattern": "T71020 Venstre nyre", "group": 0}
        },
        "Karination": {
            "M09420": {"pattern": "M09420 karinvasion ikke påvist", "group": 0},
            "M09421": {"pattern": "M09421 karinvasion påvist", "group": 0}
        },
        "PapellerTumorType": {
            "ÆYYY41": {"pattern": "ÆYYY41 type 1", "group": 0},
            "ÆYYY42": {"pattern": "ÆYYY42 type 2", "group": 0}
        },
        "OperationType": {
            "P306X4": {"pattern": "P306X4 tumorektomi", "group": 0},
            "P306X0": {"pattern": "P306X0 ektomipraeparat", "group": 0}
        },
        "Biopsi": {
            "P30990": {"pattern": "P30990 nålebiopsi", "group": 0}
        },
        "Lymphadenectomy": {
            "ÆLY007": {"pattern": "ÆLY007 lymfeknuder", "group": 0},
            "T0857": {"pattern": "T0857", "group": 0},
            "T0858": {"pattern": "T0858", "group": 0}
        },
        "LymphnodesMetastasis": {
            "ÆLX001": {"pattern": "ÆLX001 lymfeknudemetastaser", "group": 0}
        },
        "Rhabdoid": {
            "ÆYYY0Z": {"pattern": "ÆYYY0Z rhabdoid", "group": 0}
        }
    }

    details = {}
    for key, sub_mappings in mappings.items():
        for code, info in sub_mappings.items():
            match = re.search(info["pattern"], other_text)
            if match:
                details[key] = match.group(info["group"])
                # Optional: remove found data from other_text to avoid duplication
                other_text = re.sub(info["pattern"], '', other_text)
            else:
                details[key] = ''
    details['RemainingTextInOther'] = other_text.strip()  # To store any text that was not matched
    return details



def extract_patient_diagnosis_records(patient_df, patient_id, mappings):
    """
    Extracts and compiles key information from the earliest occurrence of specified diagnosis codes in a patient's data.

    This function processes each specified diagnosis code within the patient's medical records. It identifies the earliest
    occurrence of each code and extracts various mapped details from the diagnosis text. The function also collects any
    uncategorized information from the diagnosis text into an 'Other' column.

    Parameters:
    patient_df (pd.DataFrame): The DataFrame containing the patient's medical records.
    patient_id (str): The unique identifier for the patient.
    mappings (dict): A dictionary of mappings where each key is a column name and each value is a dictionary mapping diagnosis codes to descriptive text.

    Returns:
    pd.DataFrame: A DataFrame containing the extracted information, with each row representing the earliest record for a specific diagnosis code.

    Note:
    This function assumes the existence of 'Diagnoser' (diagnosis details) and 'Modtaget' (received date) columns in the input DataFrame.
    """

    # Define the list of diagnosis codes to search for.
    diagnosis_codes = [
        "T71000", "T71003", "T71007", "T71008",
        "T7100R", "T7100S", "T7100T", "T7100U",
        "T71010", "T71020"
        # Additional diagnosis codes can be added here.
    ]

    records = []

    for code in diagnosis_codes:
        # Filter the DataFrame for rows containing the current diagnosis code.
        matching_rows = patient_df[patient_df['Diagnoser'].str.contains(code, na=False)]

        if not matching_rows.empty:
            # Select the earliest record based on 'Modtaget' column.
            earliest_record = matching_rows.sort_values(by='Modtaget').iloc[0]
            diagnoser_text = earliest_record["Diagnoser"]

            # Initialize the record with patient ID and the earliest diagnosis date.
            record = {
                "PatientID": patient_id,
                "EarliestDiagnosisDate": earliest_record["Modtaget"]
            }

            # Extract and assign mapped values; remove mapped text from diagnoser_text.
            for column_name, mapping_dict in mappings.items():
                code, extracted_value = parse_diagnosis_detail(diagnoser_text, mapping_dict)
                record[column_name] = extracted_value
                if code:
                    diagnoser_text = diagnoser_text.replace(code, "")
                    diagnoser_text = diagnoser_text.replace(extracted_value, "")

            # Assign remaining text to 'Other'.
            # record['Other'] = diagnoser_text.strip()

            # Extract additional details from the 'Other' column
            additional_details = extract_details_from_other(diagnoser_text.strip())
            record.update(additional_details)

            records.append(record)

    return pd.DataFrame(records)


def merge_keep_non_null(value1, value2):
    """
    Merges two values by keeping the non-null value.

    If both values are non-null, the first value is kept.

    Parameters:
    value1: The first value.
    value2: The second value.

    Returns:
    The non-null value, or the first value if both are non-null.
    """
    return value1 if value1 is not None else value2


def merge_based_on_date_preference(consolidated_value, next_value, use_newest_date=True):
    """
    Merges two values based on date preference.

    If one value is None, the other is kept. If both are non-null, the value
    associated with the newest or oldest date is kept based on the preference.

    Parameters:
    consolidated_value: The current value in the consolidated record.
    next_value: The value in the next record to be merged.
    use_newest_date (bool): If True, keeps the value associated with the newest date.
                            If False, keeps the value associated with the oldest date.

    Returns:
    The value to be kept after merging.
    """
    if consolidated_value is None:
        return next_value
    elif next_value is None:
        return consolidated_value
    return next_value if use_newest_date else consolidated_value


def consolidate_diagnosis_dates(patient_records, mappings, merge_rule_function):
    """
    Consolidates patient diagnosis records based on the closeness of their dates.

    Parameters:
    patient_records (pd.DataFrame): A DataFrame containing patient diagnosis records with dates.
    mappings (dict): A dictionary of mappings where each key is a column name.
    merge_rule_function (function): A function that defines how to merge values of additional columns.

    Returns:
    pd.DataFrame: A DataFrame with consolidated diagnosis records.
    """
    # Convert 'EarliestDiagnosisDate' to datetime objects and sort records
    patient_records['EarliestDiagnosisDate'] = pd.to_datetime(patient_records['EarliestDiagnosisDate'], dayfirst=True)
    patient_records.sort_values(by='EarliestDiagnosisDate', ascending=True, inplace=True)

    consolidated_records = []
    i = 0
    while i < len(patient_records):
        current_record = patient_records.iloc[i].to_dict()
        j = i + 1
        while j < len(patient_records):
            next_record = patient_records.iloc[j].to_dict()
            days_diff = (next_record["EarliestDiagnosisDate"] - current_record["EarliestDiagnosisDate"]).days
            if days_diff < 60:
                # Merge each column using the appropriate rule
                for col in mappings.keys():
                    current_record[col] = merge_rule_function(current_record[col], next_record[col])

                # Special handling for 'Other' column if it exists
                if 'Other' in current_record and 'Other' in next_record:
                    current_record['Other'] = (current_record['Other'] or '') + '; ' + (next_record['Other'] or '')

                j += 1
            else:
                break
        consolidated_records.append(current_record)
        i = j  # Move to the next unprocessed record

    return pd.DataFrame(consolidated_records)


def split_initial_and_recurrences(merged_records):
    """
    Splits merged patient diagnosis records into two distinct DataFrames: one for initial diagnoses and another for recurrences.

    This function identifies the earliest diagnosis record for each patient and separates these as initial diagnoses. All other records are considered as recurrences.

    Parameters:
    merged_records (pd.DataFrame): A DataFrame containing merged patient diagnosis records, with an 'EarliestDiagnosisDate' column.

    Returns:
    tuple of pd.DataFrame: A tuple containing two DataFrames. The first DataFrame ('initial_diagnoses') contains only the earliest diagnosis date for each patient. The second DataFrame ('recurrences') contains all subsequent records.

    Note:
    The function expects 'PatientID' and 'EarliestDiagnosisDate' columns in the input DataFrame. It assumes that 'EarliestDiagnosisDate' is in a format compatible with pandas' to_datetime method.
    """
    # Ensure that 'EarliestDiagnosisDate' is in datetime format for accurate comparisons
    merged_records['EarliestDiagnosisDate'] = pd.to_datetime(
        merged_records['EarliestDiagnosisDate'], dayfirst=True)

    # Group by 'PatientID' and find the earliest diagnosis date for each patient
    earliest_dates = merged_records.groupby('PatientID')['EarliestDiagnosisDate'].min().reset_index()

    # Merge with the original records to isolate the initial diagnoses
    initial_diagnoses = merged_records.merge(earliest_dates, on=['PatientID', 'EarliestDiagnosisDate'])

    # Exclude initial diagnoses from the merged records to identify recurrences
    recurrences = merged_records[~(merged_records['PatientID'].isin(initial_diagnoses['PatientID']) &
                                   merged_records['EarliestDiagnosisDate'].isin(initial_diagnoses['EarliestDiagnosisDate']))]

    return initial_diagnoses, recurrences


def consolidate_patient_data(file_name, data_directory, mappings, merge_rule_function):
    """
    Reads and consolidates patient data from Excel files located in subdirectories of a specified data folder.
    It then splits the consolidated data into two distinct DataFrames: one for initial diagnoses and another for recurrences.

    Parameters:
    file_name (str): Name of the Excel file to be read from each patient subfolder.
    data_directory (str): Path to the folder containing patient subdirectories.
    mappings (dict): Dictionary of mappings for parsing diagnosis details.
    merge_rule_function (function): Function defining the rule for merging diagnosis records.

    Returns:
    tuple: A tuple containing two DataFrames. The first DataFrame ('initial_diagnoses') contains the consolidated
           initial diagnosis data, and the second DataFrame ('recurrences') contains the recurrence data.

    Raises:
    FileNotFoundError: If the specified data folder path does not exist.
    """

    if not os.path.exists(data_directory):
        raise FileNotFoundError(f"Data directory not found: {data_directory}")

    consolidated_initial_diagnoses = []  # List to store initial diagnoses data from all patients
    consolidated_recurrences = []  # List to store recurrences data from all patients

    # Retrieve patient folders
    patient_folders = [folder for folder in os.listdir(data_directory) if
                       os.path.isdir(os.path.join(data_directory, folder))]

    # Process data for each patient
    for patient_id in patient_folders:
        patient_file_path = os.path.join(data_directory, patient_id, file_name)

        if os.path.isfile(patient_file_path):
            try:
                # Read patient data from Excel file
                patient_df = pd.read_excel(patient_file_path, header=0)

                # Extract and consolidate patient diagnosis records
                patient_records = extract_patient_diagnosis_records(patient_df, patient_id, mappings)
                consolidated_records = consolidate_diagnosis_dates(patient_records, mappings, merge_rule_function)

                # Split into initial diagnoses and recurrences
                initial_diagnoses, recurrences = split_initial_and_recurrences(consolidated_records)

                # Append to the respective lists
                consolidated_initial_diagnoses.append(initial_diagnoses)
                consolidated_recurrences.append(recurrences)
            except Exception as e:
                # Capture and print any errors during processing
                traceback_details = traceback.format_exc()
                print(f"Error processing file {patient_file_path}: {e}\nTraceback details: {traceback_details}")

    # Combine all initial diagnoses and recurrences into final DataFrames
    final_initial_diagnoses = pd.concat(consolidated_initial_diagnoses, ignore_index=True) if consolidated_initial_diagnoses else pd.DataFrame()
    final_recurrences = pd.concat(consolidated_recurrences, ignore_index=True) if consolidated_recurrences else pd.DataFrame()

    return final_initial_diagnoses, final_recurrences



initial_diagnoses, recurrences = consolidate_patient_data('pato_bank.xlsx',
                                                          'C:\\src\\hospital-ui\\renal_cancer_porject\\data', mappings, merge_based_on_date_preference)

# Save the initial_diagnoses DataFrame to an Excel file
# initial_diagnoses.to_excel('rcc.xlsx', index=False)
# initial_diagnoses.to_excel('rcc_new.xlsx', index=False)

# Save the recurrences DataFrame to another Excel file
# recurrences.to_excel('recurrences.xlsx', index=False)