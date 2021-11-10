from ipb_client import OpenAPIClient
import os


script_dir = os.path.dirname(__file__)
file_path = os.path.join(script_dir, 'credentials')


client = OpenAPIClient(credentials_path=file_path)

accounts = client.get_accounts()

print("ACCOUNT")
for account in accounts["accounts"]:
    print(account)
    balance = client.get_balance( account["accountId"])
    print("balance: ", balance)

