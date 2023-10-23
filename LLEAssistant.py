import pandas as pd
import tkinter as tk
from tkinter import filedialog
import openpyxl


class LLEAssistant:
    def __init__(self, data_sheet_path, cryo_master_sheet_path, network_location):
        self.data_sheet_path = r"C:\Users\abehl\Downloads\Data Sheet A.xlsx"
        self.cryo_master_sheet_path = r"C:\Users\abehl\Downloads\CryoMaster.xlsx"
        self.network_location = r"C:\Users\abehl\Downloads"
        self.data_wb = openpyxl.load_workbook(self.data_sheet_path)
        self.cryo_master_wb = openpyxl.load_workbook(
            self.cryo_master_sheet_path)


    def _get_digit_input() -> int:
        while True:
            try:
                user_input = int(
                    input("Please enter a slide position between 1 and 50"))
            except ValueError:
                print("Invalid input, please try again")
            else:
                if user_input not in range(1, 51):
                print("Invalid input, please try again")
            else:
                return user_input


def _get_sheet_path():
    root = tk.Tk()
    root.withdraw()
    file_path = filedialog.askopenfilename(
        filetypes=[("Excel files", "*.xlsx"), ("CSV files", "*.csv")])
    return file_path


def get_sheet(user_input: int, file_path: str) -> pd.DataFrame:
    sheet_name = "Final Data"
    if file_path.endswith(".csv"):
        df = pd.read_csv(file_path)
    else:
        df = pd.read_excel(file_path, sheet_name=sheet_name)
    # Save the results to variables before returning
    csv_result = pd.read_csv(file_path)
    excel_result = pd.read_excel(file_path, sheet_name=sheet_name)
    return df, csv_result, excel_result


def get_capsule_id_from_slide_position() -> str:
    # Takes the user-inputted slide position and returns the corresponding capsule ID
    slide_position = _get_digit_input()

    data = pd.read_excel(io=_get_sheet_path, header=9,
                         usecols="C:D", skiprows=14)

    # 0-based index, so 2 and 3 correspond to "C" and "D"
    c_column, d_column = data.columns[2], data.columns[3]
    for idx, entry in enumerate(data[c_column]):
        try:
            last_digits = int(str(entry).split('-')[-1])
        except ValueError:
            continue

        if last_digits == slide_position:
            return data[d_column].iloc[idx]
        return "No match found"
