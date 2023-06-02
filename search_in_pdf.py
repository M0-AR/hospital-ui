import os
import PyPDF2
import tkinter as tk
from tkinter import ttk

data = ''


def load_patient_data():
    # Load the patient data for the selected patient ID
    patient_id = id_var.get()
    patient_directory = os.path.join('HospitalData', patient_id)
    pdf_path = os.path.join(patient_directory, 'notater.pdf')

    # Show an error message if the PDF file doesn't exist
    if not os.path.isfile(pdf_path):
        results_text.delete('1.0', 'end')
        results_text.insert('end', 'Patient data not found for ID {}'.format(patient_id))
        return

    # Clear the search results and show the PDF file contents
    global page_texts
    page_texts = []
    with open(pdf_path, 'rb') as f:
        pdf_reader = PyPDF2.PdfReader(f)
        num_pages = len(pdf_reader.pages)
        for page_num in range(num_pages):
            page = pdf_reader.pages[page_num]
            page_text = "\n------------------------------------------------------------\n" \
                        + page.extract_text()
            page_texts.append(page_text)
    all_text = '\n'.join(page_texts)
    results_text.delete('1.0', 'end')
    results_text.insert('end', all_text)


def get_matching_pages(keyword, page_texts):
    matching_pages = []
    for page_num in range(len(page_texts)):
        page = page_texts[page_num].lower()
        if keyword.lower() in page:
            matching_pages.append(page_num + 1)
    return matching_pages


def get_line_col(text, index):
    """Get the line and column number of the given index in the text."""
    line_num = text.count('\n', 0, index) + 1
    col_num = index - text.rfind('\n', 0, index)
    return line_num, col_num


def search_keyword():
    # Get the selected patient ID and keyword
    patient_id = id_var.get()
    keyword = search_var.get()

    # Remove old highlights
    results_text.tag_remove('highlight', '1.0', 'end')

    global page_texts
    # Get the pages that match the keyword
    matching_pages = get_matching_pages(keyword, page_texts)

    # Display only the matching pages
    results_text.delete('1.0', 'end')
    if len(matching_pages) > 0:
        for page_num in matching_pages:
            page_text = page_texts[page_num - 1]
            start_index = page_text.lower().find(keyword.lower())
            while start_index != -1:
                end_index = start_index + len(keyword)
                results_text.insert('end', page_text[:start_index])
                results_text.insert('end', page_text[start_index:end_index], 'highlight')
                page_text = page_text[end_index:]
                start_index = page_text.lower().find(keyword.lower())
            results_text.insert('end', page_text)
    else:
        results_text.insert('end', 'No results found for keyword "{}" in patient "{}"'.format(keyword, patient_id))


# Initialize the Tkinter root window
root = tk.Tk()
root.title("Patient Data Search")

# Initialize variables for the selected patient ID and search keyword
id_var = tk.StringVar()
search_var = tk.StringVar()

# Initialize the search results text box
results_text = tk.Text(root, wrap=tk.WORD, width=80, height=30)

# Load the list of patient IDs from the HospitalData directory
ids = [dir_name for dir_name in os.listdir('HospitalData') if os.path.isdir(os.path.join('HospitalData', dir_name))]
id_var.set(ids[0])

# Add the patient ID picker to the UI
id_label = tk.Label(root, text="Select Patient ID:")
id_label.pack()

id_picker = ttk.Combobox(root, textvariable=id_var, values=ids)
id_picker.pack()

load_button = tk.Button(root, text="Load Patient Data", command=load_patient_data)
load_button.pack()

# Add the search functionality to the UI
search_label = tk.Label(root, text="Enter a keyword to search:")
search_label.pack()

search_entry = tk.Entry(root, textvariable=search_var)
search_entry.pack()

display_button = tk.Button(root, text="Search", command=search_keyword)
display_button.pack()

# Add the text box to display the search results
results_text.tag_configure('highlight', foreground='red')  # Create a custom tag with the desired foreground color
results_text.pack()

root.mainloop()
