from sf_login import sf_login
from create_report import create_report
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


def insert_data_to_salesforce(sf, data, salesforce_object):
    for index, row in data.iterrows():
        record = {
            'Name': row['Name'],
            'CloseDate': row['CloseDate'],
            'Amount': row['Amount']
        }
        sf.__getattr__(salesforce_object).create(record)


if __name__ == "__main__":
    prompt = ""
    while prompt != "x":
        prompt = input("Press enter to select a CSV file to create a Salesforce report from. Type x to quit.")
        csv_file_path = select_csv_file()
        data = read_csv_file(csv_file_path)
        # Would need to get Agent information from website or something, or add it in the CSV somewhere
        
        if data is not None:
            sf = sf_login()
            account_ids = data['Account ID'].values.tolist()  # Assuming 'AccountId' column exists in the CSV
            
            report_id = create_report(sf, account_ids)
            print("Created Report ID:", report_id)