import requests
import json
import stripe

def stripeKeys():
    testSecretKey = 'Bearer sk_test_51PT3FoP359XzvQdX0HLe2KGuFpvWjIUk4GDqA0rKortkfHt7ikVOVDj4trsy90UZ4iitq3RvwRprmdNVDETmiwGA00CaAtXYN0'
    return testSecretKey

def stripeDirectKey():
    return 'sk_test_51PT3FoP359XzvQdX0HLe2KGuFpvWjIUk4GDqA0rKortkfHt7ikVOVDj4trsy90UZ4iitq3RvwRprmdNVDETmiwGA00CaAtXYN0'

def getPaymentIntents():
    url = f'https://api.stripe.com/v1/payment_intents'
    heads = {'Authorization': stripeKeys()}
    req = requests.get(url, headers = heads)
    print(req.json())

def createPaymentIntent(amt): # https://docs.stripe.com/terminal/quickstart
    url = f'https://api.stripe.com/v1/payment_intents'
    heads = {'Authorization': stripeKeys(), 'Content-Type': 'application/x-www-form-urlencoded'}
    payBody = {
        "amount": str(int(amt * 100)), # Amount is in ${XX.XX} format. Stripe wants the amount to be in cents. Multiply by 100 to remove decimals and then cast to an integer
        "currency": "USD", 
        "payment_method_types": ["card_present"],
        "capture_method": 'automatic'
    }
    form_data = []
    for key, values in payBody.items():
        if isinstance(values, list):
            for i, value in enumerate(values):
                form_data.append((f'{key}[{i}]', value))
        else:
            form_data.append((key, values))
    req = requests.post(url, headers = heads, data = form_data)
    # print(req.json())
    if req.status_code == 200:
        print(f'Payment intent {req.json()["id"]} created successfully')
        return req.json()['id']
    else:
        print('Payment intent not created')
        print(req.json())
    return

def processPaymentIntent(id):
    stripe.api_key = stripeDirectKey()
    print(f'\nProcessing payment intent')
    return stripe.terminal.Reader.process_payment_intent(
        "tmr_Fm6YDQycNkDMvZ",
        payment_intent = id,
    )

def retrieveReader():
    stripe.api_key = stripeDirectKey()
    print(f'Retrieving reader')
    return stripe.terminal.Reader.retrieve("tmr_Fm6YDQycNkDMvZ")

def presentPayment():
    stripe.api_key = stripeDirectKey()
    print(f'Presenting payment')
    return stripe.terminal.Reader.TestHelpers.present_payment_method("tmr_Fm6YDQycNkDMvZ")

def capturePaymentIntent(id): # not being used
   stripe.api_key = stripeDirectKey()
   print(f'Capturing payment intent for id {id}')
   return stripe.PaymentIntent.capture(id)

def retrievePaymentIntent(id):
    stripe.api_key = stripeDirectKey()
    print(f'Retrieving payment intent for id {id}')
    return stripe.PaymentIntent.retrieve(id)