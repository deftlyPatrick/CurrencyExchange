__author__ = "Patrick Wong"
__copyright__ = "Copyright by Patrick Wong"

import urllib.request
import httplib2
import json
from pprint import pprint
import pandas as pd


class CurrencyConverter:

    def __init__(self):
        req = urllib.request.Request("https://free.currconv.com/api/v7/currencies?apiKey=0348799f934010f56f8b")
        from_currency = "https://free.currconv.com/api/v7/convert?q="
        to_currency = "&compact=ultra&apiKey=0348799f934010f56f8b"
        self.data = urllib.request.urlopen(req).read()
        self.data = json.loads(self.data.decode('utf-8'))
        self.currency_name = {}
        self.currency_symbol = {}
        self.currency_abv = []

        self.from_country = ""
        self.to_country = ""

        self.sort_currency()
        self.input_website()
        self.final_website = self.print_website(self.from_country, self.to_country)
        print("self.final_website: ", self.final_website)
        self.check_website()
        self.print_currency_rate_today()

    def sort_currency(self):
        for k, dk in self.data.items():
            # print(k)
            for i, di in dk.items():
                # print(di)
                self.currency_abv.append(i)
                self.currency_name[i] = di['currencyName']
                if 'currencySymbol' in di:
                    self.currency_symbol[i] = di['currencySymbol']
                else:
                    temp_words = di['currencyName'].split()
                    self.currency_symbol[i] = temp_words[-1]

    def print_website(self, from_country, to_country):
        from_currency = "https://free.currconv.com/api/v7/convert?q="
        to_currency = "&compact=ultra&apiKey=0348799f934010f56f8b"

        updated_website = ""

        updated_website += from_country + "_" + to_country + ","
        updated_website += to_country + "_" + from_country


        return from_currency + updated_website + to_currency

    def input_website(self):
        # Example : "https://free.currconv.com/api/v7/convert?q=USD_PHP,PHP_USD&compact=ultra&apiKey=0348799f934010f56f8b"

        print(self.currency_abv)

        self.to_country = input("What currency do you want to exchange to? ")
        self.from_country = input("What currency do you currently own? ")

        self.to_country = self.to_country.upper()
        self.from_country = self.from_country.upper()

        if not (self.to_country in self.currency_abv and self.from_country in self.currency_abv):
            while not (self.to_country in self.currency_abv and self.from_country in self.currency_abv):
                print("This is not a valid currency. Please try again. \n")
                self.to_country = input("What currency do you want to exchange to? ")
                self.from_country = input("What currency do you currently own? ")

                self.to_country = self.to_country.upper()
                self.from_country = self.from_country.upper()

        print("valid currency")

        return self.to_country, self.from_country


    def check_website(self):

        check_website = httplib2.Http()
        resp = check_website.request(self.final_website)
        resp = int(resp[0]['status'])

        return resp

    def print_currency_rate_today(self):

        resp = self.check_website()

        print(resp)

        if resp == 200:
            print("Response Code: ", resp)
            req = urllib.request.Request(self.final_website)
            self.data = urllib.request.urlopen(req).read()
            self.data = json.loads(self.data.decode('utf-8'))
            print(self.data)
            from_to = list(self.data.values())
            print("Today's exchange rate for %s to %s is %f" % (self.from_country, self.to_country, from_to[0]))
        else:
            print("self.final_website: ", self.final_website)
            print("Response Code:", resp)
            print("Error website loading")




a = CurrencyConverter()
print(a)
