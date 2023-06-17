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

# Create empty DataFrame with specified columns
data_frame = pd.DataFrame(columns=columns)

