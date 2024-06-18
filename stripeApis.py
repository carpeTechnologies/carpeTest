import requests
import json

def stripeKeys():
    testSecretKey = 'Bearer sk_test_51PT3FoP359XzvQdX0HLe2KGuFpvWjIUk4GDqA0rKortkfHt7ikVOVDj4trsy90UZ4iitq3RvwRprmdNVDETmiwGA00CaAtXYN0'
    return testSecretKey

def getPaymentIntents():
    url = f'https://api.stripe.com/v1/payment_intents'
    heads = {'Authorization': stripeKeys()}
    req = requests.get(url, headers = heads)
    print(req.json())

def createPaymentIntent(amt): # https://docs.stripe.com/terminal/quickstart
    url = f'https://api.stripe.com/v1/payment_intents'
    heads = {'Authorization': stripeKeys()}
    payBody = {
        "amount": str(int(amt * 100)), # Amount is in ${XX.XX} format. Stripe wants the amount to be in cents. Multiply by 100 to remove decimals and then cast to an integer
        "currency": "USD"
    }
    req = requests.post(url, headers = heads, data = payBody)
    # print(req.json())
    if req.status_code == 200:
        print('Payment intent created successfully')
    else:
        print('Payment intent not created')
        print(req.json())
