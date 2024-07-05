from sf_login import sf_login
from create_report import create_report
import pandas as pd
from tkinter import Tk
from tkinter.filedialog import askopenfilename
import requests
import json

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
    sf = sf_login()

    csv_file_path = select_csv_file()
    data = read_csv_file(csv_file_path)
    # Would need to get Agent information from website or something, or add it in the CSV somewhere
        
    if data is not None:
        sf = sf_login()
        account_ids = data['Account ID'].values.tolist()  # Assuming 'AccountId' column exists in the CSV
        # Find an existing report
        report_name = "Accounts from CSV Report"
        query = f"SELECT Id FROM Report WHERE Name = '{report_name}'"
        result = sf.query(query)

        if result['totalSize'] == 0:
            print(f"Report '{report_name}' not found. Please create a report manually first.")
        else:
            report_id = result['records'][0]['Id']
            
            # Get the current report metadata
            current_metadata = sf.restful(f'analytics/reports/{report_id}/describe', method='GET')
            
            # Update the report filters
            current_metadata['reportMetadata']['reportFilters'] = [{
                "column": "ACCOUNT_ID",
                "operator": "in",
                "value": account_ids
            }]
            
            # Prepare the update payload
            update_payload = {
                "reportMetadata": current_metadata['reportMetadata']
            }

            try:
                # Update the report
                response = sf.restful(f'analytics/reports/{report_id}/describe', method='POST', json=update_payload)
                
                if response.status_code == 200:
                    print(f"Report updated successfully. Report ID: {report_id}")
                    
                    # Run the report
                    report_results = sf.restful(f'analytics/reports/{report_id}', method='GET')
                    
                    if report_results.status_code == 200:
                        print("Report run successfully. Results:")
                        print(json.dumps(report_results.json(), indent=2))
                    else:
                        print(f"Failed to run report. Status code: {report_results.status_code}")
                        print(report_results.text)
                else:
                    print(f"Failed to update report. Status code: {response.status_code}")
                    print(response.text)
            except Exception as e:
                print(f"An error occurred: {str(e)}")
                print("Response content:")
                print(e.content if hasattr(e, 'content') else "No additional content")