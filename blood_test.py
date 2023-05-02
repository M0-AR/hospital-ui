import datetime
import tkinter as tk
from tkinter import ttk
import pandas as pd

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


def display_data_by_selected_date():
    date = date_var.get()
    result.delete('1.0', tk.END)
    result.insert(tk.END, '\n'.join(date_data[date]))


def display_data_before():
    result.delete('1.0', tk.END)

    desired_date_str = date_entry.get().strip()
    if not desired_date_str:
        return

    desired_date = datetime.datetime.strptime(desired_date_str, '%d-%m-%y')

    data_before = []

    for date_str in date_data.keys():
        date = datetime.datetime.strptime(date_str, '%d-%m-%y %H:%M')
        if date <= desired_date:
            data_before.append(date_str)
            data_before.extend(date_data[date_str])
            data_before.append('\n\n')  # add an empty line between each set of data

    result_text = '\n'.join(data_before)
    result.insert(tk.END, result_text)


def display_data_after():
    result.delete('1.0', tk.END)

    desired_date_str = date_entry.get().strip()
    if not desired_date_str:
        return

    desired_date = datetime.datetime.strptime(desired_date_str, '%d-%m-%y')

    data_after = []

    for date_str in date_data.keys():
        date = datetime.datetime.strptime(date_str, '%d-%m-%y %H:%M')
        if date >= desired_date:
            data_after.append(date_str)
            data_after.extend(date_data[date_str])
            data_after.append('\n\n')  # add an empty line between each set of data

    result_text = '\n'.join(data_after)
    result.insert(tk.END, result_text)


def display_data():
    if radio_var.get() == "before":
        display_data_before()
    else:
        display_data_after()


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

display_button = tk.Button(root, text="Display Data", command=display_data_by_selected_date)
display_button.pack()

date_prompt_label = tk.Label(root, text="Enter a desired date (MM-DD-YY):")
date_prompt_label.pack()

date_entry = tk.Entry(root)
date_entry.pack()

radio_var = tk.StringVar()
radio_var.set("before")

radio_before = tk.Radiobutton(root, text="Before", variable=radio_var, value="before")
radio_before.pack()

radio_after = tk.Radiobutton(root, text="After", variable=radio_var, value="after")
radio_after.pack()

submit_button = tk.Button(root, text="Submit", command=display_data)
submit_button.pack()

result = tk.Text(root, wrap=tk.WORD, width=80, height=30)
result.pack()

root.mainloop()
