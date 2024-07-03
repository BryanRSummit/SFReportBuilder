import json
import time

def create_report(sf, account_ids, sf_object="Account", agent="Bryan Edman"):
    # # Used to see Object fields
    # account_metadata = sf.Account.describe()
    # # Extract field names
    # field_names = [field['name'] for field in account_metadata['fields']]

#Account ID,Owner,Account Name,Type,Average Policy Size,Operating Acreage,Years Positive,Converted,Phone,Email,Lat,Lng,Grid State,Probability
    # Define the report metadata
    account_id_string = "','".join(account_ids)
    
    # Define the report metadata
    report_metadata = {
        "reportMetadata": {
            "name": "Custom Account Report",
            "developerName": f"Custom_Account_Report_{int(time.time())}",
            "reportType": {"type": "Account"},
            "description": "Custom report for specific Account IDs",
            "reportFormat": "TABULAR",
            "detailColumns": [
                "ACCOUNT.NAME",
                "ACCOUNT.TYPE",
                "ACCOUNT.INDUSTRY",
                "ACCOUNT.ANNUAL_REVENUE",
                "ACCOUNT.NUMBER_OF_EMPLOYEES"
            ],
            "reportFilters": [
                {
                    "column": "ACCOUNT.ID",
                    "operator": "in",
                    "value": account_id_string
                }
            ]
        }
    }
    
    # Create the report
    headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/json'
    }
    
    response = sf.restful('analytics/reports', method='POST', headers=headers, data=json.dumps(report_metadata))
    
    return response