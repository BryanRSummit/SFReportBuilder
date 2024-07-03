from sf_login import sf_login
import pandas as pd
from tkinter import Tk
from tkinter.filedialog import askopenfilename


def select_csv_file():
    # Hide the root window
    Tk().withdraw()
    # Open file dialog
    file_path = askopenfilename(
        filetypes=[("CSV files", "*.csv")], 
        title="Select a CSV file"
    )
    return file_path


def read_csv_file(file_path):
    if file_path:
        data = pd.read_csv(file_path)
        return data
    else:
        print("No file selected")
        return None


if __name__ == "__main__":
    sf = sf_login()
    csv_file_path = select_csv_file()
    data = read_csv_file(csv_file_path)
    if data is not None:
        print("CSV Data:")
        print(data.head()) 