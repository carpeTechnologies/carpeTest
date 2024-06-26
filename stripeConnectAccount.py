import stripe
import stripeApis

stripe.api_key = stripeApis.stripeDirectKey()

def getAccountInfo():
    country = input(f'What country is your business headquartered in?: ').upper()
    email = input(f'What is the best contact email for your business?: ')
    return country, email
    
def createConnectAccount():
    userCountry, userEmail = getAccountInfo()
    # print(userCountry, )
    return stripe.Account.create(country = userCountry, type = "standard", business_type = 'company', email = userEmail)

def createAccountLink(conAccountId):
    return stripe.AccountLink.create(account = conAccountId, refresh_url = "https://example.com/reauth",
        return_url = "https://example.com/return",
        type = "account_onboarding",)
 
def createAndConnectAccount():
    connectedAccountId = createConnectAccount()['id']
    accountLink = createAccountLink(connectedAccountId)['url']
    return accountLink

createAndConnectAccount()