import requests
import json
from requests.auth import HTTPBasicAuth
from datetime import datetime
import base64


class MpesaC2bCredential:
    consumer_key = '2P4cv9cG201Kp0xhCrnFpyELGqJxbAXe'
    consumer_secret = 'p2YWhvq3o9iO6yky'
    api_URL = 'https://sandbox.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials'


class MpesaAccessToken:
    r = requests.get(MpesaC2bCredential.api_URL,
                     auth=HTTPBasicAuth(MpesaC2bCredential.consumer_key, MpesaC2bCredential.consumer_secret))
    mpesa_access_token = json.loads(r.text)
    validated_mpesa_access_token = mpesa_access_token['access_token']
    # print("This is the access_token", validated_mpesa_access_token)

class LipanaMpesaPpassword:
    Time_stamp = datetime.now().strftime('%Y%m%d%H%M%S')
    Business_short_code = "600496"
    passkey = 'bfb279f9aa9bdbcf158e97dd71a467cd2e0c893059b10f78e6b72ada1ed2c919'
    data_to_encode = passkey + Business_short_code + Time_stamp

    encoded_string =base64.b64encode(data_to_encode.encode())
    # print("This is encoded string:",encoded_string)

    decoded_password = encoded_string.decode("utf-8")
    # print("This is the decoded password:", decoded_password)