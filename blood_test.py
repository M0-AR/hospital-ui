import tkinter as tk
from tkinter import ttk

import openpyxl
import os
import re


def read_excel_data(directory, file_name='blood_test.xlsx'):
    data = {}
    file_path = os.path.join(directory, file_name)
    workbook = openpyxl.load_workbook(file_path)
    sheet = workbook.active
    current_date = None

    pattern = re.compile(r'^\d{2}-\d{2}-\d{2}\s')

    for cell in sheet['A']:
        content = cell.value.strip().replace('_x000D_', '')
        if content:
            if pattern.match(content):
                current_date = content
                data[current_date] = []
            else:
                data[current_date].append(content)

    return data


def load_patient_data():
    patient_id = id_var.get()
    patient_directory = os.path.join('HospitalData', patient_id)
    global date_data
    date_data = read_excel_data(patient_directory)

    dates = list(date_data.keys())
    date_var.set(dates[0])
    date_picker['values'] = dates


def display_data():
    date = date_var.get()
    result.delete('1.0', tk.END)
    result.insert(tk.END, '\n'.join(date_data[date]))


root = tk.Tk()
root.title("Blood Test")

id_var = tk.StringVar()
date_var = tk.StringVar()

ids = [dir_name for dir_name in os.listdir('HospitalData') if os.path.isdir(os.path.join('HospitalData', dir_name))]
id_var.set(ids[0])

id_label = tk.Label(root, text="Select Patient ID:")
id_label.pack()

id_picker = ttk.Combobox(root, textvariable=id_var, values=ids)
id_picker.pack()

load_button = tk.Button(root, text="Load Patient Data", command=load_patient_data)
load_button.pack()

date_label = tk.Label(root, text="Select Date:")
date_label.pack()

date_picker = ttk.Combobox(root, textvariable=date_var)
date_picker.pack()

display_button = tk.Button(root, text="Display Data", command=display_data)
display_button.pack()

result = tk.Text(root, wrap=tk.WORD, width=80, height=30)
result.pack()

root.mainloop()
