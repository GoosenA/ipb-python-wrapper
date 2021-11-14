import datetime
from openapi_client import OpenAPIClient
import os


script_dir = os.path.dirname(__file__)
file_path = os.path.join(script_dir, 'credentials')


client = OpenAPIClient(credentials_path=file_path)

print("ACCOUNT")
accounts = client.get_accounts()
for account in accounts["accounts"]:
    print(account)

print("MAKING TRANSFER")
sid = "from_account_id"
transfer_details = [{
                "BeneficiaryAccountId": "to_account_id",
                "Amount": "1.01",
                "MyReference": "Test from PBA to PS",
                "TheirReference": "Test_python1"
        }]
response = client.make_inter_account_transfer(sid, transfer_details)
