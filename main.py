import os
from tkinter import filedialog
from excelhelper.excelhelper import ExcelManipulator


def main():

    excel_manipulator = ExcelManipulator(
        r"C:\users\abehl\Downloads\Data Sheet A.xlsx",
        r"C:\users\abehl\Downloads\CryoMaster.xlsx",
        r"C:\users\abehl\Downloads"
    )
    # data_sheet_path = filedialog.askopenfilename(
    # initialdir=excel_manipulator.network_location, title="Select Data Sheet")

    # cryo_master_sheet_path = filedialog.askopenfilename(
    # initialdir=excel_manipulator.network_location, title="Select Cryo Master Sheet")
    slide_position, pin_number = excel_manipulator.get_initial_values()
    print(slide_position, pin_number)
    print("Getting capsule ID...")
    capsule_id = excel_manipulator.get_capsule_id(
        slide_position=slide_position)
    print(capsule_id)
    print(pin_number)
    print("Adding data to cryo master...")
    excel_manipulator.add_data_to_cryo_master(slide_position=slide_position)
    print("Creating folder and notes...")
    excel_manipulator.create_folder_and_notes(capsule_id, pin_number)

    return "Done!"


if __name__ == "__main__":
    main()
