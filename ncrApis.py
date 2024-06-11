import requests
import pandas as pd
import json
from time import gmtime, strftime
from datetime import datetime
from datetime import timezone
import pytz
from hmacHelper import hmacHelper
from ui import TabApp, LaunchScreen
import tkinter as tk

def exampleGet(secretKey, sharedKey, nepOrganization):
    now = datetime.now(tz = timezone.utc)
    now = datetime(now.year, now.month, now.day, hour = now.hour,
                minute=now.minute, second=now.second)

    requestURL = baseUrl() + findAllOrders()
    httpMethod = 'GET'
    contentType = 'application/json'

    hmacAccessKey = hmacHelper(sharedKey, secretKey, now, httpMethod,
                        requestURL, contentType, None, None, None, nepOrganization, None)
    
    utcDate = now.strftime('%a, %d %b %Y %H:%M:%S GMT')
    headers = {
        "Date": utcDate,
        "Content-Type": contentType,
        "Authorization": "AccessKey " + hmacAccessKey,
        "nep-organization": nepOrganization,
        'nep-enterprise-unit': '9af39a319af44df58b2b332c7b759c5f'
    }
    request = requests.get(requestURL, headers = headers)

    print(request.status_code)
    parseAllOrders(request.text)

    # print(res)
    return      

def hmacHeaders(secretKey, sharedKey, nepOrganization, enterpriseUnit, requestUrl, reqMethod):
    now = datetime.now(tz = timezone.utc)
    now = datetime(now.year, now.month, now.day, hour = now.hour, minute = now.minute, second = now.second)

    contentType = 'application/json'

    hmacAccessKey = hmacHelper(sharedKey, secretKey, now, reqMethod,
                        requestUrl, contentType, None, None, None, nepOrganization, None)
    
    utcDate = now.strftime('%a, %d %b %Y %H:%M:%S GMT')
    hmacHeaders = {
        "Date": utcDate,
        "Content-Type": contentType,
        "Authorization": f'AccessKey {hmacAccessKey}',
        "nep-organization": nepOrganization,
        'nep-enterprise-unit': enterpriseUnit
    }
    return hmacHeaders

def baseUrl():
    return 'https://api.ncr.com'

def findAllOrders():
    findUnacks = '/order/orders/find-unacknowledged'
    return findUnacks

def getSpecificOrder(orderId):
    return f'{baseUrl()}/order/orders/{orderId}'

def basicUsername():
    return 'f73ac580-bca1-4070-8cc7-602cc0d531ac'

def basicPassword():
    return 'Password123!'

def basicAuth():
    return (basicUsername(), basicPassword())

def headers():
    heads = {
        'Content-Type': 'application/json',
        'nep-organization': 'test-drive-000aeaece5fe49d7891a8',
        'nep-enterprise-unit': '9af39a319af44df58b2b332c7b759c5f'#,
        # 'Date': 'Tue, 21 May 2024 00:50:06 GMT'  # might need date? not sure
        }
    return heads

def parseAllOrders(allOrdersObj):
    data = json.loads(allOrdersObj)
    for order in data['orders']:
        id = order['id']
        total_value = order['totals'][0]['value']
        # orderLinesFromOrder(order)
        # print(f'Order ID: {id}, Order Total Price: {total_value}')
    # print(data)
    return data

def orderLinesFromOrder(orderObj):
    id = orderObj['id']
    print(f'Order ID: {id}')

    for orderLine in orderObj["orderLines"]:
        # lineId = orderLine.get("lineId")
        lineId = setVal('lineId', orderLine)
        extendedAmount = orderLine.get("extendedAmount")
        unitPrice = orderLine.get("unitPrice")
        productType = orderLine.get("productId", {}).get("type")
        productValue = orderLine.get("productId", {}).get("value")
        print(f'Line ID: {lineId}, Product Type: {productType}, Product: {productValue}, Unit Price: {unitPrice}')
    return

def taxesForOrder(orderObj):
    for tax in orderObj["taxes"]:
        lineId = setVal('lineId', tax)
        amt = setVal('amount', tax)
        
    return

def setVal(apiField, object):
    retVal = object.get(apiField)
    return retVal

def patchOrderAsPaid(orderId, amountToPay, heads):
    current_time = datetime.now(pytz.UTC)
    formatted_time = current_time.strftime("%Y-%m-%dT%H:%M:%S.%f")[:-3] + "Z"
    # https://codepal.ai/code-generator/query/23WgC7ad/python-function-print-cvv-expiration-date
    payload = {
        "payments": [
            {
                "accountNumber": "123321", # Need to figure out how to pull this
                "amount": amountToPay,
                "description": "Paid via Carpe",
                "expiration": {  # Need to find out how to identify the card's expiration date
                    "month": 11,
                    "year": 2031
                },
                "gratuity": 0,
                "maskedPAN": "321123", # Masked Personal Account number. Don't know how to generate what this should be 
                "payBalance": True,
                "status": "Authorized",
                "type": "CreditDebit",
                "subType": "Credit",  # Need to find out how to identify whether a card is credit or debit
                "paymentTime": formatted_time
            }
        ]
    }

    apiUrl = f'{baseUrl()}/order/orders/{orderId}'
    # print(payload)
    # request = requests.patch(apiUrl, json = payload, headers = heads, auth = basicAuth())
    # print(request.status_code)
    return

# def creds():
#     secretKey = '2a8e9a34a61c45e1850963054b704f82'
#     sharedKey = 'b1d4a804aa0241babd77e3ab08fece2a'
#     org = 'test-drive-000aeaece5fe49d7891a8'
#     enterpriseUnit = '9af39a319af44df58b2b332c7b759c5f'
#     second enterpriseUnit = '7a52036837db408cba1e088b86833865'
#     return [secretKey, sharedKey, org, enterpriseUnit]

def parse_orders(json_data):
    orders = []
    for order in json_data['orders']:
        order_info = {
            'id': order['id'],
            'dateCreated': order['dateCreated'],
            'status': order['status'],
            'owner': order['owner'],
            'channel': order['channel'],
            'customer': order['customer']['name'],
            'total': order['totals'][0]['value'],
            'currency': order['currency']
        }
        orders.append(order_info)
    return orders

def process_field_values(field_values):
    secretKey, sharedKey, org, enterpriseUnit = field_values
    getAllOrders = baseUrl() + findAllOrders()
    heads = hmacHeaders(secretKey, sharedKey, org, enterpriseUnit, getAllOrders, 'GET')
    
    root = tk.Tk()
    app = TabApp(root)  # Initialize TabApp with root window
    
    def fetch_orders():
        orders = autoGetOrders(getAllOrders, heads, app)
        app.update_orders(orders)  # Update the TabApp with new orders
        root.after(3000, fetch_orders)  # Schedule the next fetch in 3 seconds
    
    fetch_orders()  # Initial call to start the loop
    root.mainloop()

def autoGetOrders(getAllOrders, heads, tab_app):
    request = requests.get(getAllOrders, headers = heads)
    print(f'Sent request at {strftime("%Y-%m-%d %H:%M:%S", gmtime())} GMT')
    response_data = json.loads(request.text)
    # incorrect_orders = tab_app.get_incorrect_orders()
    # correct_orders = tab_app.get_correct_orders()
    # unConfOrders = tab_app.getOrders()
    
    orders = response_data['orders']
    processed_orders = tab_app.getProcessedOrders()
    for order in orders:
        order_id = order['id']
        # if order_id not in incorrect_orders and order_id not in correct_orders:
        if order_id not in processed_orders:
            print(f"Got new Order ID: {order_id}")
            tab_app.addProcessedOrder(order_id)
    return orders

def main():
    root = tk.Tk()
    launch_screen = LaunchScreen(root, submit_callback=process_field_values)
    root.mainloop()

if __name__ == "__main__":
    main()
