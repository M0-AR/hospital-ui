# Medical Data Analysis Toolkit

## High-Level Overview

This repository contains a suite of Python-based tools designed to process, analyze, and explore complex medical data from patient records. It provides two core analysis pipelines—one for renal cancer and another for bladder infections—along with data exploration GUIs and utility scripts to streamline clinical research and data-driven decision-making.

The project is built to handle data from various sources, including pathology reports, blood tests, microbiology results, and medication logs, transforming raw, semi-structured data into clean, aggregated datasets ready for analysis.

## Key Features

- **Automated Data Pipelines:** Streamlines the process of cleaning, merging, and structuring complex medical data.
- **Specialized Analysis:** Includes dedicated pipelines for renal cancer and bladder infection research.
- **Data Exploration Tools:** Offers simple graphical user interfaces (GUIs) for searching and visualizing patient data.
- **Modular and Extensible:** Built with modular scripts that can be adapted for other clinical research needs.
- **Comprehensive Data Mapping:** Translates medical codes into human-readable descriptions for easier interpretation.

## Core Projects

### 1. Renal Cancer Analysis Pipeline

This pipeline is designed to identify and analyze renal cancer cases, distinguishing between initial diagnoses and recurrences.

- **Functionality:** It processes patient pathology reports (`pato_bank.xlsx`) to identify diagnosis codes related to renal cell carcinoma (RCC). It then aligns this data with blood test results (`blood_test.xlsx`) from periods both before and after the diagnosis date.
- **Inputs:**
    - `pato_bank.xlsx`: Contains pathology report details, including diagnosis codes and dates.
    - `blood_test.xlsx`: Contains time-stamped blood test results.
- **Outputs:**
    - `rcc_.xlsx`: A consolidated dataset of initial RCC diagnoses with corresponding blood test data.
    - `recurrences_.xlsx`: A dataset of cancer recurrences with their associated blood test data.
- **Key Scripts:** `renal_cancer_porject/app/pipelines/01_extract_right_data/`

### 2. Bladder Infection Analysis Pipeline

This pipeline processes patient data to identify individuals with specific bladder-related conditions and infections.

- **Functionality:** It reads and merges data from multiple sources, including pathology reports, microbiology results (`miba.xlsx`), medication lists (`medicin.xlsx`), and vital signs (`vitale.xlsx`). It filters and combines this information to create a detailed patient profile.
- **Inputs:**
    - `pato_bank.xlsx`: Pathology reports.
    - `miba.xlsx`: Microbiology results (e.g., urine and blood cultures).
    - `medicin.xlsx`: Medication administration records.
    - `diagnose_list.xlsx`: List of diagnoses.
    - `vitale.xlsx`: Vital signs measurements.
    - `blood_test.xlsx`: Blood test results.
- **Output:**
    - `bladder_infect_data.xlsx`: A comprehensive dataset of patients with bladder-related conditions, including their full medical context.
- **Key Scripts:** `bladder_infectNN.py`, `bladder_infectNN01.py`, `bladder_infectNN02.py`, `combine_data.py`.

## For Business Stakeholders

This toolkit offers significant value by:
- **Accelerating Research:** Automating data processing tasks that would otherwise require extensive manual effort.
- **Improving Data Quality:** Ensuring that data is clean, consistent, and ready for analysis, reducing errors in research outcomes.
- **Supporting Data-Driven Decisions:** Providing clinicians and researchers with structured datasets that can be used to identify trends, evaluate treatment efficacy, and inform clinical guidelines.

## For Medical Researchers

This repository provides powerful tools to support your research:
- **Ready-to-Analyze Datasets:** The output files (`rcc_.xlsx`, `bladder_infect_data.xlsx`) are structured for immediate use in statistical analysis software.
- **Transparent Data Mapping:** The scripts in `renal_cancer_porject/app/pipelines/01_extract_right_data/pato_bank.py` contain explicit mappings from medical codes (e.g., SNOMED, ICD) to human-readable text, ensuring clarity and consistency in data interpretation.
- **Customizable Pipelines:** The modular nature of the scripts allows you to adapt the data extraction and analysis logic to fit the specific needs of your study.

## Technical Deep Dive

### System Architecture

The system is designed around a set of Python scripts that read data from a structured file system, process it in memory using the `pandas` library, and write the output to Excel files. The core logic is encapsulated in individual scripts, which can be run independently or as part of a larger pipeline.

### Data Requirements

For the scripts to function correctly, your data must be organized in the following directory structure:

```
HospitalData/
├── patient_cpr_1/
│   ├── blood_test.xlsx
│   ├── diagnose_list.xlsx
│   ├── medicin.xlsx
│   ├── miba.xlsx
│   └── pato_bank.xlsx
│   └── vitale.xlsx
├── patient_cpr_2/
│   ├── blood_test.xlsx
│   ├── ...
└── ...
```

- The root data folder must be named `HospitalData`.
- Each patient's data should be in a separate subfolder, with the folder name being the patient's CPR number or unique identifier.

### Setup and Installation

1.  **Clone the repository:**
    ```bash
    git clone <repository_url>
    cd <repository_directory>
    ```

2.  **Install dependencies:** It is recommended to use a virtual environment.
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
    pip install pandas openpyxl
    ```

### Scripts and Modules

- **`main.py`:** A Tkinter-based GUI for loading data from a selected patient and searching for keywords across their records.
- **`blood_test.py`:** A GUI tool to explore `blood_test.xlsx` data for a specific patient, with options to filter by date.
- **`bladder_infectNN.py` / `bladder_infectNN01.py` / `bladder_infectNN02.py`:** A series of scripts for the bladder infection analysis pipeline. They contain functions for reading, filtering, and merging patient data from various sources.
- **`combine_data.py` / `combine_data_reverse.py`:** Scripts for aggregating data from multiple Excel files across all patients into a single combined dataset.
- **`renal_cancer_porject/`:**
    - **`app/pipelines/01_extract_right_data/`:** Contains the core logic for the renal cancer pipeline.
        - **`pato_bank.py`:** Extracts and categorizes renal cancer diagnoses from pathology reports.
        - **`blood_test_all_before.py` / `blood_test_all_after.py`:** Extracts blood test data relative to a diagnosis date.
        - **`combine.py`:** Orchestrates the renal cancer pipeline, running the other scripts and merging their outputs.
    - **`utils/`:** Utility functions (currently minimal).

## How to Use

### Running the Data Exploration GUIs

1.  **Keyword Search GUI:**
    ```bash
    python main.py
    ```
    - Select a patient ID from the dropdown.
    - Click "Load Patient Data."
    - Enter a keyword and click "Search" to search within the selected patient's data or "Search in All Patients" to search across all records.

2.  **Blood Test Explorer GUI:**
    ```bash
    python blood_test.py
    ```
    - Select a patient ID and click "Load Patient Data."
    - Choose a date from the dropdown to view results for that specific date.

### Executing the Analysis Pipelines

1.  **Renal Cancer Pipeline:**
    - Navigate to the `renal_cancer_porject/app/pipelines/01_extract_right_data/` directory.
    - Modify the file paths in `combine.py` to point to your data directory.
    - Run the script:
      ```bash
      python combine.py
      ```
    - The output files `rcc_.xlsx` and `recurrences_.xlsx` will be generated in the script's directory.

2.  **Bladder Infection Pipeline:**
    - Ensure your `HospitalData` directory is in the root of the repository.
    - Run the main script for this pipeline (e.g., `bladder_infectNN02.py`).
      ```bash
      python bladder_infectNN02.py
      ```
    - The output file `bladder_infect_data.xlsx` will be created.

## Contributing

Contributions are welcome! If you would like to contribute, please follow these steps:

1.  Fork the repository.
2.  Create a new branch for your feature or bug fix.
3.  Make your changes and ensure they are well-tested.
4.  Submit a pull request with a clear description of your changes.

---
*This README was generated by an AI assistant.*