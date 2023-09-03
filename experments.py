"""
Utilities for Cell Value Processing

This module provides utility functions to handle and process cell values,
specifically targeting the conversion of strings that represent lists,
replacement of the string 'nan' with empty strings, and date format adjustments.

Functions:
    - process_cell: Transforms cell values by converting 'nan' to empty strings and processing potential date strings.
    - remove_two_chars_from_year: Adjusts the year in a date string by removing its first two characters.

Example:
    process_cell("[nan, nan, 2020.01.01]")
    ["", "", "20.01.01"]
"""

def process_cell(cell_value):
    # If cell_value doesn't start with "[" or end with "]", return it as is.
    if not (cell_value.startswith("[") and cell_value.endswith("]")):
        return cell_value

    # Strip off the brackets and split the string into a list based on comma separation
    values = cell_value[1:-1].split(", ")

    # Replace 'nan' with empty string
    values = ['' if val == 'nan' else val for val in values]

    # Convert list back to string representation
    return str(values)


# Sample execution
cell_value = "[nan, nan, nan, nan, nan, nan, nan, nan, nan, nan, nan, nan, nan, nan, nan, nan, nan, nan, nan, nan, nan, nan]"
processed_value = process_cell(cell_value)
print(processed_value)  # Expected: ['', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '']

#

def remove_two_chars_from_year(date_str):
    # Check if the date string contains exactly two periods
    if date_str.count('.') == 2:
        day, month, year = date_str.split('.')
        year = year[2:]  # Removes the first two characters of the year
        return f"{day}.{month}.{year}"
    # Return the original string if it's not a valid date
    return date_str

def process_cell(cell_value):
    # If cell_value is empty, return an empty string ""
    if str(cell_value) == 'nan':
        return ""

    # Check if cell_value is already a list
    if isinstance(cell_value, list):
        # Convert list items to string, replace 'nan' with empty string, and process dates
        values = [remove_two_chars_from_year(str(item)) if str(item) != 'nan' and '.' in str(item) else str(item) for
                  item in cell_value]
        return '\"' + str(values) + '\"'

    # If cell_value is a string and starts with "[" and ends with "]"
    if isinstance(cell_value, str) and cell_value.startswith("[") and cell_value.endswith("]"):
        # Strip off the brackets and split the string into a list based on comma separation
        values = cell_value[1:-1].split(", ")

        # Replace 'nan' with empty string and process dates
        values = ['' if val.strip() == 'nan' else remove_two_chars_from_year(val.strip()) for val in values]

        # Convert list back to string representation
        return values

    # If it's neither a string in list format nor a list, return the cell_value as is
    return cell_value