import re
import requests

def validate_contract_address(address):
    # Check if the address has the correct length and starts with '0x'
    if len(address) == 42 and address.startswith("0x"):
        # Check if the remaining 40 characters are hexadecimal
        if re.fullmatch(r"0x[a-fA-F0-9]{40}", address):
            return True
    return False

def check_address_on_etherscan(address, api_key):
    url = f"https://api.etherscan.io/api"
    params = {
        "module": "account",
        "action": "txlist",
        "address": address,
        "startblock": 0,
        "endblock": 99999999,
        "page": 1,
        "offset": 1,
        "sort": "asc",
        "apikey": api_key
    }
    response = requests.get(url, params=params)
    
    # Check if the response is successful and parse JSON
    if response.status_code == 200:
        data = response.json()
        # Check if there are transactions or other data
        if data['status'] == "1":
            return True  # Address exists with transactions
        elif data['status'] == "0" and data['message'] == "No transactions found":
            return False  # Address exists but has no transactions
    return False  # Invalid or non-existent address

# Get your Etherscan API key
api_key = "Your_Etherscan_API_Key"

# Loop until the user provides a valid address
while True:
    address = input("Enter the smart contract address: ")
    
    # Validate the address format
    if validate_contract_address(address):
        # If the format is correct, check against the Ethereum API
        if check_address_on_etherscan(address, api_key):
            print("Address is valid and exists on the Ethereum network.")
            break
        else:
            print("Address does not exist or has no transactions on the Ethereum network. Please try again.")
    else:
        print("Error: Invalid smart contract address format. Please try again.")

