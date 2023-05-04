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


def load_patient_data():
    patient_id = id_var.get()
    patient_directory = os.path.join('HospitalData', patient_id)
    global data
    data = read_excel_data(patient_directory)


root = tk.Tk()
root.title("Test")

id_var = tk.StringVar()

ids = [dir_name for dir_name in os.listdir('HospitalData') if os.path.isdir(os.path.join('HospitalData', dir_name))]
id_var.set(ids[0])

id_label = tk.Label(root, text="Select Patient ID:")
id_label.pack()

id_picker = ttk.Combobox(root, textvariable=id_var, values=ids)
id_picker.pack()

load_button = tk.Button(root, text="Load Patient Data", command=load_patient_data)
load_button.pack()

search_label = tk.Label(root, text="Enter a keyword to search:")
search_label.pack()

search_entry = tk.Entry(root)
search_entry.pack()

display_button = tk.Button(root, text="Search", command=search_keyword)
display_button.pack()

results_text = tk.Text(root, height=20, width=80)
results_text.pack()
results_text.tag_configure('highlight', foreground='red')  # Create a custom tag with the desired foreground color

root.mainloop()
