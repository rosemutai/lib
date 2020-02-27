from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
import requests
from requests.auth import HTTPBasicAuth
import json
from . mpesa_credentials import MpesaAccessToken, LipanaMpesaPpassword
from django.views.decorators.csrf import csrf_exempt
from .models import Stk

from datetime import datetime, timedelta, date
from base64 import b64decode, b64encode



@csrf_exempt
def MpesaAccessToken(request):
    """
    Function to generate token from the consumer secret and key
    """
    consumer_key = '2P4cv9cG201Kp0xhCrnFpyELGqJxbAXe'
    consumer_secret = 'p2YWhvq3o9iO6yky'
    api_URL = 'https://sandbox.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials'

    r = requests.get(api_URL, auth=HTTPBasicAuth(
        consumer_key, consumer_secret))
    auth = json.loads(r.text)
    token = auth['access_token']
    return token

@csrf_exempt
def lipa_na_mpesa_online(request):
    """
    Initiate stk push to client. Pass phone number of the client and amount to be billed as parameters.
    Will be called by any the other fucntion that requires to perform a billing and return the data response from safaricom
    """
    phone = '254703119877'
    amount = 1

    api_transaction_URL = 'https://sandbox.safaricom.co.ke/mpesa/stkpush/v1/processrequest'
    BusinessShortCode = 174379;
    LipaNaMpesaPasskey = 'bfb279f9aa9bdbcf158e97dd71a467cd2e0c893059b10f78e6b72ada1ed2c919';
    access_token = MpesaAccessToken(request)
    data = None

    get_now = datetime.now()
    payment_time = get_now.strftime("%Y%m%d%H%M%S")
    to_encode = '{}{}{}'.format(
        BusinessShortCode, LipaNaMpesaPasskey, payment_time)
    payment_password = (b64encode(to_encode.encode('ascii'))).decode("utf-8")

    if access_token:
        headers = {"Authorization": "Bearer %s" % access_token}
        request = {
            "BusinessShortCode": BusinessShortCode,
            "Password": payment_password,
              "Timestamp": payment_time,
              "TransactionType": "CustomerPayBillOnline",
              "Amount": amount,
              "PartyA": phone,
              "PartyB": BusinessShortCode,
              "PhoneNumber": phone,
              "CallBackURL": 'https://7ccb3733.ngrok.io/mpesa/stk/confirmation/',
              "AccountReference": "ebook",
              "TransactionDesc": 'payment'
        }
        response = requests.post(
            api_transaction_URL, json=request, headers=headers)
        data = response.text
    else:
        print('access token failed')

    return data


@csrf_exempt
def confirmation(request):
    mpesa_body =request.body.decode('utf-8')
    mpesa_payment = json.loads(mpesa_body)
    payment = Stk(
        first_name=mpesa_payment['FirstName'],
        last_name=mpesa_payment['LastName'],
        middle_name=mpesa_payment['MiddleName'],
        description=mpesa_payment['TransID'],
        phone_number=mpesa_payment['MSISDN'],
        amount=mpesa_payment['TransAmount'],
        reference=mpesa_payment['BillRefNumber'],
        organization_balance=mpesa_payment['OrgAccountBalance'],
        type=mpesa_payment['TransactionType'],
    )
    payment.save()

    context = {
        "ResultCode": 0,
        "ResultDesc": "Accepted"
    }
    return JsonResponse(dict(context))

@csrf_exempt
def stkconfirmation(request):
    mpesa_body =request.body.decode('utf-8')
    mpesa_payment = json.loads(mpesa_body)


    # get_data = mpesa_payment['Body']['stkCallback']
    # get_success_data = get_data['CallbackMetadata']
    #
    # if get_data:
    #     MerchantRequestID = get_data[
    #         'MerchantRequestID']
    #     CheckoutRequestID = get_data[
    #         'CheckoutRequestID']
    #     ResultCode = get_data['ResultCode']
    #     ResultDesc = get_data['ResultDesc']
    #
    #     if get_success_data:
    #         get_items = get_success_data['Item']
    #         for i in get_items:
    #             if i['Name'] == 'Amount':
    #                 Amount = i.get('Value')
    #             elif i['Name'] == 'MpesaReceiptNumber':
    #                 MpesaReceiptNumber = i.get('Value')
    #             elif i['Name'] == 'PhoneNumber':
    #                 PhoneNumber = i.get('Value')
    #             elif i['Name'] == 'Balance':
    #                 Balance = i.get('Value')
    #             elif i['Name'] == 'TransactionDate':
    #                 TransactionDate = i.get('Value')
    #             else:
    #                 continue
    #
    #     else:
    #         Amount = None
    #         MpesaReceiptNumber = None
    #         PhoneNumber = None
    #         Balance = None
    #         TransactionDate = None
    #
    #     stk_response = Stk.objects.create(MerchantRequestID=MerchantRequestID, CheckoutRequestID=CheckoutRequestID, \
    #                                       ResultCode=ResultCode, ResultDesc=ResultDesc, Amount=Amount,
    #                                       MpesaReceiptNumber=MpesaReceiptNumber, \
    #                                       PhoneNumber=PhoneNumber, Balance=Balance, TransactionDate=TransactionDate)

    print(mpesa_payment)


    context = {
        "ResultCode": 0,
        "ResultDesc": "Accepted"
    }
    return JsonResponse(dict(context))

