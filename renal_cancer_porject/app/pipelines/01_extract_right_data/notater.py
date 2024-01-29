import os
import PyPDF2
import pandas as pd


def search_terms_in_pdf(pdf_path, search_terms):
    """
    Searches for specified terms within a PDF file and records the first found term for each category.

    Parameters:
        pdf_path (str): The file path to the PDF document.
        search_terms (dict): A dictionary of terms to search for, organized by category.

    Returns:
        dict: A dictionary with category as key and the first found term as value.
    """
    found_terms = {category: None for category in search_terms}
    with open(pdf_path, 'rb') as f:
        pdf_reader = PyPDF2.PdfReader(f)
        for page in pdf_reader.pages:
            page_text = page.extract_text().lower()
            for category, terms in search_terms.items():
                if found_terms[category] is None:  # Skip if we've already found a term for this category
                    for term in terms:
                        if term.lower() in page_text:
                            found_terms[category] = term
                            # break  # Stop after the first term is found in category
    return found_terms


import PyPDF2

def search_terms_in_pdf(pdf_path, search_terms):
    """
    Searches for specified terms within a PDF file and checks the same or next few lines
    after finding a category, to find the first term for each category.

    Parameters:
        pdf_path (str): The file path to the PDF document.
        search_terms (dict): A dictionary of terms to search for, organized by category.

    Returns:
        dict: A dictionary with category as key and the first found term as value.
    """
    found_terms = {category: None for category in search_terms}
    with open(pdf_path, 'rb') as f:
        pdf_reader = PyPDF2.PdfReader(f)
        for page in pdf_reader.pages:
            page_text = page.extract_text()
            if page_text:  # Ensure there's text on the page
                lines = page_text.split('\n')
                for i, line in enumerate(lines):
                    for category in search_terms:
                        if found_terms[category] is None and category.lower() in line.lower():
                            # Check the same line and the next few lines for terms
                            search_window = lines[i:i+3]  # Current line and the next two lines
                            for term in search_terms[category]:
                                if any(term.lower() in line.lower() for line in search_window):
                                    found_terms[category] = term
                                    break
    return found_terms



def process_patient_directories(base_directory, search_terms):
    """
    Processes all patient directories to search for terms within their PDF files and records findings.

    Parameters:
        base_directory (str): The base directory containing patient subdirectories.
        search_terms (dict): A dictionary of terms to search for, organized by category.

    Returns:
        pd.DataFrame: A DataFrame with patient CPR numbers and corresponding found terms.
    """
    patient_findings = []

    for patient_dir in os.listdir(base_directory):
        patient_path = os.path.join(base_directory, patient_dir)
        if os.path.isdir(patient_path):
            pdf_files = [f for f in os.listdir(patient_path) if f.endswith('.pdf')]
            for pdf_file in pdf_files:
                pdf_path = os.path.join(patient_path, pdf_file)
                found_terms = search_terms_in_pdf(pdf_path, search_terms)
                patient_findings.append({
                    'cpr': patient_dir,
                    **found_terms
                })

    # Convert the list of dictionaries to a DataFrame
    return pd.DataFrame(patient_findings)


# Example usage:
base_directory = 'C:\\src\\hospital-ui\\renal_cancer_porject\\data'

# Example usage:
search_terms = {
    'Symptomer': ['Hæmaturi', 'Smerte', 'Vægttab', 'Andet'],
    'Rygning': ['Aktuelt', 'Tidligere', 'Aldrig'],
    'Forhøjt blodtryk': ['Ja', 'Nej'],
    'ASA-score': ['1', '2', '>3'],
    'Performance status': ['0', '1', '2', '3', '4', '5'],
    'Charlson score': ['0', '1', '2', '3', '4', '5'],
    'Beslutning truffet i MDT': ['Ja', 'Nej'],
    'Subtype af RCC': ['Type1', 'Type2'],  # Replace with actual subtypes
    'Type af kirurgi': ['Ingen', 'Laparoskopi', 'Robot', 'Åben'],
    'Tilbagefald': ['Ja', 'Nej']
}

patient_results_df = process_patient_directories(base_directory, search_terms)
print(patient_results_df)
