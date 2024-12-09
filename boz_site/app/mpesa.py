
consumer_key = 'wDPtxcrJAVQRrlvWOegjCHA0E922A64B1idjko2Dkzk4iAk4'
consumer_secret = 'cZ4vhy9SvfMiZ8OapYZnS5hAynxeAF7xTAGPlmkDi1OWaLNBE9pLtIcO6Y16KqFE'

import requests
import hashlib
import datetime
from requests.auth import HTTPBasicAuth
import base64


import random
import string

def generate_unique_id():
    """Generates a unique ID in the format "order_xxxx" where "xxxx" are random characters.

    Returns:
        str: The generated unique ID.
    """

    random_chars = ''.join(random.choices(string.ascii_uppercase + string.digits, k=12))
    unique_id = f"order_{random_chars[:12]}"
    return unique_id




def convert_prefix(mobile_number):
    # Strip any leading or trailing whitespace from the input
    mobile_number = mobile_number.strip()
    
    # Check if the number starts with '07' or '01' and convert accordingly
    if mobile_number.startswith('07'):
        return '254' + mobile_number[1:]
    elif mobile_number.startswith('01'):
        return '254' + mobile_number[2:]
    else:
        # If the number does not start with '07' or '01', return it unchanged
        return mobile_number

def mpesa_pr(phon, amount):
    phone=convert_prefix(phon)
    # Function to encode the "Password" field using the M-Pesa passkey
    def encode_password(shortcode, passkey, timestamp):
        data = f"{shortcode}{passkey}{timestamp}"
        return base64.b64encode(data.encode()).decode()

    try:
        # API credentials
        CONSUMER_KEY = consumer_key#"4Ik4gdO6OrWRmbwxukUl8L45BZXAXx7y"
        CONSUMER_SECRET = consumer_secret#"FIClzK0zb18dJntf"

        BASE_URL = "https://sandbox.safaricom.co.ke"
        API_ENDPOINT = "/mpesa/stkpush/v1/processrequest"

        # Request an access token
        auth_headers = {
            "Authorization": "Basic "
            + base64.b64encode(f"{CONSUMER_KEY}:{CONSUMER_SECRET}".encode()).decode()
        }
        access_token_url = "https://sandbox.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials"
        access_token_response = requests.get(access_token_url, headers=auth_headers)
        access_token = access_token_response.json().get("access_token")

        if not access_token:
            print("Failed to get the access token.")
            return

        # Headers setup
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {access_token}",
        }
        paybill='174379'
        # Payload setup
        payload = {
            "BusinessShortCode": paybill,
            "Password": "",
            "Timestamp": "",
            "TransactionType": "CustomerPayBillOnline",
            "Amount": amount,
            "PartyA": phone,
            "PartyB": paybill,
            "PhoneNumber": phone,
            "CallBackURL": "https://drum-clear-hawk.ngrok-free.app/transac-status/",
            "AccountReference": "BozBet networks",
            "TransactionDesc": "Contract fee",
        }

        # Format the timestamp as "YYYYMMDDHHMMSS"
        timestamp = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
        payload["Timestamp"] = timestamp

        # Calculate the password based on the provided Passkey
        passkey = "bfb279f9aa9bdbcf158e97dd71a467cd2e0c893059b10f78e6b72ada1ed2c919"
        password = encode_password(
            str(payload["BusinessShortCode"]), passkey, timestamp
        )
        payload["Password"] = password

        # Make the POST request
        response = requests.post(BASE_URL + API_ENDPOINT, headers=headers, json=payload)
        #print(response)
        # Check the response status and handle accordingly
        if response.status_code == 200:
            print("STK Push request successful.")
            #print(response.text.encode("utf8"))
        else:
            print(f"STK Push request failed. Status code: {response.status_code}")
            print(response.text.encode("utf8"))

    except requests.exceptions.RequestException as e:
        print(f"An error occurred during the request: {e}")
    except Exception as ex:
        print(f"An unexpected error occurred: {ex}")
        
#mpesa_pr('0702162058','100')
        
