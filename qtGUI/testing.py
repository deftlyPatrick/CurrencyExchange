import urllib.request
import httplib2
import json
from pprint import pprint
import pandas as pd

class CurrencyConverter:

    def __init__(self):
        req = urllib.request.Request("https://free.currconv.com/api/v7/currencies?apiKey=0348799f934010f56f8b")
        data = urllib.request.urlopen(req).read()
        data = json.loads(data.decode('utf-8'))
        self.currency_name = {}
        self.currency_symbol = {}
        self.currency_abv = []
        self.allCurrency = []

    def sort_currency(self):
        for k, dk in data.items():
            # print(k)
            for i, di in dk.items():
                # print(di)
                currency_abv.append(i)
                currency_name[i] = di['currencyName']
                if 'currencySymbol' in di:
                    currency_symbol[i] = di['currencySymbol']
                else:
                    temp_words = di['currencyName'].split()
                    currency_symbol[i] = temp_words[-1]

    def 



# converter = CurrencyConverter("https://free.currconv.com/api/v7/currencies?apiKey=0348799f934010f56f8b")

req = urllib.request.Request("https://free.currconv.com/api/v7/currencies?apiKey=0348799f934010f56f8b")
data = urllib.request.urlopen(req).read()
data = json.loads(data.decode('utf-8'))
# from_currency = ""
# to_currency = "USD"
# allCurrency = data["currencyName"]
currency_name = {}
currency_symbol = {}
currency_abv = []
allCurrency = []
# print((data['results'].keys()))

# print(len(data['results']))




# print(currency_symbol)
# print(currency_name)


# for x in data['results']:
#     print(repr(x), ":", data['results'][x])


# Example : "https://free.currconv.com/api/v7/convert?q=USD_PHP,PHP_USD&compact=ultra&apiKey=0348799f934010f56f8b"
from_currency = "https://free.currconv.com/api/v7/convert?q="
to_currency = "&compact=ultra&apiKey=0348799f934010f56f8b"

final_website = ""

print(currency_abv)
user_input = False

from_to = []

temp_val = ""
temp_val2 = ""

val = input("What currency do you want to exchange to? ")
val2 = input("What currency do you currently own? ")
val = val.upper()
val2 = val2.upper()


# print(val in currency_abv)
# print(val2 in currency_abv)
# print(val in currency_abv and val2 in currency_abv)

if not (val in currency_abv and val2 in currency_abv):
    while not (val in currency_abv and val2 in currency_abv):
        print("This is not a valid currency. Please try again. \n")
        val = input("What currency do you want to exchange to? ")
        val = val.upper()
        val2 = input("What currency do you currently own? ")
        val2 = val2.upper()


print("valid currency")
final_website += from_currency + val + "_" + val2 + ","
final_website += val2 + "_" + val + to_currency
print("final_website: ", final_website)

check_website = httplib2.Http()
resp = check_website.request(final_website)
resp = int(resp[0]['status'])

if resp == 200:
     print("Response Code: ", resp)
     req = urllib.request.Request(final_website)
     data = urllib.request.urlopen(req).read()
     data = json.loads(data.decode('utf-8'))
     print(data)
     from_to = list(data.values())
     print("Today's exchange rate for %s to %s is %f" %(val, val2, from_to[1]))
else:
    print("Response Code: ", check_website[0]['status'])
    print("Error website loading")

# req = urllib.request.Request("https://free.currconv.com/api/v7/convert?q=USD_PHP,PHP_USD&compact=ultra&apiKey=0348799f934010f56f8b")
# data = urllib.request.urlopen(req).read()
# data = json.loads(data.decode('utf-8'))
# print(data.values(1))