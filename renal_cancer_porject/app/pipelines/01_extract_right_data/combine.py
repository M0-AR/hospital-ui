import pandas as pd
from static_data import mappings
from pato_bank import merge_based_on_date_preference, consolidate_patient_data

# Path to the main Excel file and configurations
base_directory = 'C:\\src\\hospital-ui\\renal_cancer_porject\\data'
patient_diagnoses_file = 'rcc.xlsx'
file_name = 'blood_test.xlsx'


initial_diagnoses, recurrences = consolidate_patient_data('pato_bank.xlsx',
                                                          base_directory, mappings, merge_based_on_date_preference)

# Save the initial_diagnoses DataFrame to an Excel file
initial_diagnoses.to_excel(patient_diagnoses_file, index=False)

# Save the recurrences DataFrame to another Excel file
# recurrences.to_excel('recurrences.xlsx', index=False)

from blood_test_all_before import extract_latest_patient_biochemistry_data_before_operation

# Call the function
blood_test_data_before = extract_latest_patient_biochemistry_data_before_operation(
    file_name=file_name,
    base_directory=base_directory,
    patient_date_file=patient_diagnoses_file
)
from blood_test_all_after import extract_patient_biochemistry_data_after_operation

# Call the function
# Extract biochemistry data after operation
blood_test_data_after = extract_patient_biochemistry_data_after_operation(
    file_name=file_name,
    base_directory=base_directory,
    patient_date_file=patient_diagnoses_file,
    days_after=31
)

# Merge initial diagnoses with blood test data before operation
combined_data_rcc = pd.merge(initial_diagnoses, blood_test_data_before, on='PatientID', how='left')

# Now merge the combined data with blood test data after operation
final_combined_data_rcc = pd.merge(combined_data_rcc, blood_test_data_after, on='PatientID', how='left')

# Save the combined DataFrame to an Excel file
final_combined_data_rcc.to_excel('rcc_.xlsx', index=False)

# Merge initial diagnoses with blood test data before operation
combined_data_recurrences = pd.merge(recurrences, blood_test_data_before, on='PatientID', how='left')

# Now merge the combined data with blood test data after operation
final_combined_data_recurrences = pd.merge(combined_data_recurrences, blood_test_data_after, on='PatientID', how='left')

# Save the combined DataFrame to an Excel file
final_combined_data_recurrences.to_excel('recurrences_.xlsx', index=False)

# # Saving all data to one Excel file with different sheets
# with pd.ExcelWriter('rcc_.xlsx') as writer:
#     initial_diagnoses.to_excel(writer, sheet_name='Initial Diagnoses', index=False)
#     blood_test_data_before.to_excel(writer, sheet_name='Biochemistry Before', index=False)
#     blood_test_data_after.to_excel(writer, sheet_name='Biochemistry After', index=False)
#
# # Saving all data to one Excel file with different sheets
# with pd.ExcelWriter('recurrences_.xlsx') as writer:
#     recurrences.to_excel(writer, sheet_name='Recurrences', index=False)
#     blood_test_data_before.to_excel(writer, sheet_name='Biochemistry Before', index=False)
#     blood_test_data_after.to_excel(writer, sheet_name='Biochemistry After', index=False)
