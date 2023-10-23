import pandas as pd
import os


class ExcelManipulator:

    def __init__(self, data_sheet_path, cryo_master_sheet_path, network_location):
        self.data_sheet_path = data_sheet_path
        self.cryo_master_sheet_path = cryo_master_sheet_path
        self.network_location = network_location

    def get_capsule_id(self, slide_position):
        data = pd.read_excel(io=self.data_sheet_path)
        match_row = data[data.iloc[:, 1] == slide_position]
        if not match_row.empty:
            return match_row.iloc[0, 2]

    def get_capsule_id_from_slide_position(self, slide_position) -> str:
        data = pd.read_excel(io=self.cryo_master_sheet_path,
                             header=9, usecols="C:D", skiprows=14)
        c_column = data.columns[0]
        d_column = data.columns[1]
        for idx, entry in data.iterrows():
            try:
                last_digits = int(str(entry[c_column]).split('-')[-1])
            except ValueError:
                continue
            if last_digits == slide_position:
                return entry[d_column]

    def get_dimensional_measurements(self, slide_position):
        data = pd.read_excel(io=self.data_sheet_path)
        match_row = data[data.iloc[:, 1] == slide_position]
        if not match_row.empty:
            return match_row.iloc[0, 7], match_row.iloc[0, 8]

    def add_data_to_cryo_master(self, slide_position):
        capsule_id = self.get_capsule_id(slide_position)
        od, wall_thickness = self.get_dimensional_measurements(slide_position)
        new_row = pd.DataFrame([[capsule_id, od, wall_thickness]])
        cryo_master_data = pd.read_excel(io=self.cryo_master_sheet_path)
        appended_data = cryo_master_data.append(new_row, ignore_index=True)
        appended_data.to_excel(self.cryo_master_sheet_path, index=False)

    def create_folder_and_notes(self, capsule_id, pin_number):
        folder_name = f"{capsule_id} {pin_number} 1E"
        full_path = f"{self.network_location}/{folder_name}"
        os.makedirs(full_path, exist_ok=True)
        notes_content = f"{capsule_id} {pin_number} 1E\n" \
                        "0 deg  defects between 5um and 10um\n" \
                        "90 deg  defects between 5um and 10um\n" \
                        "180 deg  defects between 5um and 10um\n" \
                        "270 deg  defects between 5um and 10um"
        with open(f"{full_path}/notes.txt", "w") as f:
            f.write(notes_content)
