import os
import pandas as pd
import tkinter as tk
from tkinter import ttk
import tkinter.messagebox as messagebox

data = ''


def read_excel_data(directory):
    data = {}

    excel_files = [f for f in os.listdir(directory) if f.endswith('.xlsx') and f != 'blood_test.xlsx']

    for file in excel_files:
        filepath = os.path.join(directory, file)
        df = pd.read_excel(filepath, header=0)
        data[file] = df

    return data


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


def search_keyword():
    global data
    if not data:
        messagebox.showwarning("Data not loaded", "Please click on 'Load Patient Data' before searching.")
        return
    keyword = search_entry.get()
    if not keyword:  # Check if the keyword is empty
        results_text.delete('1.0', tk.END)
        messagebox.showwarning("No Keyword Entered", "Please enter a keyword in the search box.")
        return
    results_text.delete('1.0', tk.END)
    for filename, df in data.items():
        rows_with_keyword = df[df.apply(lambda row: row.astype(str).str.contains(keyword, regex=False).any(), axis=1)]
        if not rows_with_keyword.empty:
            results_text.insert(tk.END, f"-----------------------------------------\n"
                                        f"Results found in {filename}:\n"
                                        f"-----------------------------------------\n")
            formatted_rows = format_dataframe(rows_with_keyword, keyword)
            start = 0
            while True:
                start = formatted_rows.find("[[[", start)
                if start == -1:
                    break
                results_text.insert(tk.END, formatted_rows[:start])
                results_text.insert(tk.END, formatted_rows[start + 3:start + 3 + len(keyword)], 'highlight')
                formatted_rows = formatted_rows[start + 3 + len(keyword):]
                start = 0
            results_text.insert(tk.END, formatted_rows + "\n\n")


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


def search_keyword_all():
    data_all = read_all_excel_data()
    keyword = search_entry.get()
    if not keyword:  # Check if the keyword is empty
        results_text.delete('1.0', tk.END)
        messagebox.showwarning("No Keyword Entered", "Please enter a keyword in the search box.")
        return
    results_text.delete('1.0', tk.END)

    cpr_list = []  # To store cpr numbers where results were found

    for filename, df in data_all.items():
        rows_with_keyword = df[df.apply(lambda row: row.astype(str).str.contains(keyword, regex=False).any(), axis=1)]
        if not rows_with_keyword.empty:
            cpr_number = filename.split('_')[0]  # Extracting cpr number from filename
            cpr_list.append(cpr_number)  # Storing cpr number

            results_text.insert(tk.END, f"-----------------------------------------\n"
                                        f"Results found in {filename}:\n"
                                        f"-----------------------------------------\n")
            formatted_rows = format_dataframe(rows_with_keyword, keyword)
            start = 0
            while True:
                start = formatted_rows.find("[[[", start)
                if start == -1:
                    break
                results_text.insert(tk.END, formatted_rows[:start])
                results_text.insert(tk.END, formatted_rows[start + 3:start + 3 + len(keyword)], 'highlight')
                formatted_rows = formatted_rows[start + 3 + len(keyword):]
                start = 0
            results_text.insert(tk.END, formatted_rows + "\n\n")

    if cpr_list:  # If the list is not empty
        id_picker['values'] = cpr_list  # Update id_var with the new string
        id_var.set(cpr_list[0])
    else:
        messagebox.showwarning("OppppS!", "No matches found.")


def load_patient_data():
    patient_id = id_var.get()
    patient_directory = os.path.join('HospitalData', patient_id)
    global data
    data = read_excel_data(patient_directory)


def setup_id_picker():
    global ids
    ids = [dir_name for dir_name in os.listdir('HospitalData') if os.path.isdir(os.path.join('HospitalData', dir_name))]
    id_var.set(ids[0])


def reset_id_var():
    id_picker['values'] = ids # Update id_var with the new string
    id_var.set(ids[0])


root = tk.Tk()
root.title("Test")

root.columnconfigure(0, weight=1)
root.rowconfigure(0, weight=1)

main_frame = tk.Frame(root)
main_frame.grid(sticky='nsew', padx=10, pady=10)  # Added padding
main_frame.columnconfigure(0, weight=1)
main_frame.rowconfigure(1, weight=1)

id_label = tk.Label(main_frame, text="Select Patient ID:")
id_label.grid(row=0, column=0, sticky='w', padx=5, pady=5)

id_var = tk.StringVar()
ids = None
setup_id_picker()

id_picker = ttk.Combobox(main_frame, textvariable=id_var, values=ids)
id_picker.grid(row=1, column=0, sticky='ew', padx=5, pady=5)

button_frame_row2 = tk.Frame(main_frame)
button_frame_row2.grid(row=2, column=0, sticky='ew', padx=5, pady=5)

load_button = tk.Button(button_frame_row2, text="Load Patient Data", command=load_patient_data)
load_button.grid(row=0, column=0, padx=5, pady=5)

reset_button = tk.Button(button_frame_row2, text="Reset Cpr Numbers", command=reset_id_var)
reset_button.grid(row=0, column=1, padx=5, pady=5)

search_label = tk.Label(main_frame, text="Enter a keyword to search:")
search_label.grid(row=3, column=0, sticky='w', padx=5, pady=5)

search_entry = tk.Entry(main_frame)
search_entry.grid(row=4, column=0, sticky='ew', padx=5, pady=5)

button_frame = tk.Frame(main_frame)
button_frame.grid(row=5, column=0, sticky='ew', padx=5, pady=5)

display_button = tk.Button(button_frame, text="Search", command=search_keyword)
display_button.grid(row=0, column=0, padx=5, pady=5)

display_all_button = tk.Button(button_frame, text="Search in All Patients", command=search_keyword_all)
display_all_button.grid(row=0, column=1, padx=5, pady=5)

results_frame = tk.Frame(main_frame)  # A frame to hold the Text widget and the Scrollbar widget
results_frame.grid(row=6, column=0, sticky='nsew', padx=5, pady=5)
results_frame.columnconfigure(0, weight=1)
results_frame.rowconfigure(0, weight=1)

scrollbar = tk.Scrollbar(results_frame)
scrollbar.grid(row=0, column=1, sticky='ns')

results_text = tk.Text(results_frame, yscrollcommand=scrollbar.set)
results_text.grid(row=0, column=0, sticky='nsew')

scrollbar.config(command=results_text.yview)  # Link scrollbar to results_text

results_text.tag_configure('highlight', foreground='red')

root.mainloop()
