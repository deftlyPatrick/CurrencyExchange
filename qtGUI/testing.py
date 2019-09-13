__author__ = "Patrick Wong"
__copyright__ = "Copyright by Patrick Wong"
import os
import urllib.request
import httplib2
import json
import sys
import platform


class CurrencyConverter:

    def __init__(self):
        self.system = str(platform.system()).lower()
        req = urllib.request.Request("https://free.currconv.com/api/v7/currencies?apiKey=0348799f934010f56f8b")
        from_currency = "https://free.currconv.com/api/v7/convert?q="
        to_currency = "&compact=ultra&apiKey=0348799f934010f56f8b"
        self.data = urllib.request.urlopen(req).read()
        self.data = json.loads(self.data.decode('utf-8'))
        self.currency_name = {}
        self.currency_symbol = {}
        self.currency_abv = []
        self.money_holding = 0
        self.total_exchange = []

        self.from_country = ""
        self.to_country = ""

        self.sort_currency()
        self.input_website()
        self.final_website = self.print_website(self.from_country, self.to_country)
        self.check_website()
        self.print_currency_rate_today()
        self.print_exchanging()

    def sort_currency(self):
        for k, dk in self.data.items():
            # print(k)
            for i, di in dk.items():
                # print(di)
                self.currency_abv.append(i)
                temp_name = di['currencyName'].split()
                temp_word = temp_name[-1]
                # print(temp_word)
                if (temp_name[-1][len(temp_name[-1]) - 1:]) == ")":
                    temp_name[-1] = temp_name[-1].replace(")", "")
                    temp_name[-1] += "s)"
                    temp_str = temp_name[-1]
                    # print(temp_str)
                else:
                    temp_name[-1] += "s"
                    temp_str = temp_name[-1]
                    # print("temp_str: ", temp_str)
                    # print("temp_name[-1]: ", temp_name[-1])

                di['currencyName'] = di['currencyName'].replace(temp_word, temp_str)
                self.currency_name[i] = di['currencyName']

                # print("self.currency_name[i]: ", self.currency_name[i])
                if 'currencySymbol' in di:
                    self.currency_symbol[i] = di['currencySymbol']
                    # print("self.currency_symbol[i]: ", self.currency_symbol[i])
                else:
                    temp_words = di['currencyName'].split()
                    if (temp_words[-1][len(temp_words[-1]) - 1:]) == ")":
                        temp_words[-1] = temp_words[-1].replace(")", "")
                        temp_words[-1] += "s"
                    else:
                        temp_words[-1] += "s"
                    self.currency_symbol[i] = temp_words[-1]
                    # print("self.currency_symbol[i]: ",  self.currency_symbol[i])
        # pprint.pprint(self.currency_name)

    def print_website(self, from_country, to_country):
        from_currency = "https://free.currconv.com/api/v7/convert?q="
        to_currency = "&compact=ultra&apiKey=0348799f934010f56f8b"

        updated_website = ""

        updated_website += from_country + "_" + to_country + ","
        updated_website += to_country + "_" + from_country

        return from_currency + updated_website + to_currency

    def input_website(self):
        # Example : "https://free.currconv.com/api/v7/convert?q=USD_PHP,PHP_USD&compact=ultra&apiKey=0348799f934010f56f8b"

        temp = input("Do you know what currency you are exchanging to? Y/N \n")
        temp = temp.lower()

        if temp == "":
            print("Error: Invalid Command, Please try again. \n")
            while (temp == ""):
                temp = input("Do you know what currency you are exchanging to? Y/N \n")
        elif not (temp == "yes" or temp == "y"):
            while not (temp == "yes" or temp == "y"):
                print("Here is a list of all available currencies: \n")
                for abb, currency in self.currency_name.items():
                    print("{} ({})".format(abb, currency))
                temp = input("Do you know what currency you want to exchange to now? \n")

        self.to_country = input("What currency do you want to exchange to? \n")
        self.from_country = input("What currency do you currently own? \n")

        self.to_country = self.to_country.upper()
        self.from_country = self.from_country.upper()

        if not (self.to_country in self.currency_abv and self.from_country in self.currency_abv):
            while not (self.to_country in self.currency_abv and self.from_country in self.currency_abv):
                print("This is not a valid currency. Please try again. \n")
                self.to_country = input("What currency do you want to exchange to? \n")
                self.from_country = input("What currency do you currently own? \n")

                self.to_country = self.to_country.upper()
                self.from_country = self.from_country.upper()

        # print("valid currency")

        return self.to_country, self.from_country

    def check_website(self):

        check_website = httplib2.Http()
        resp = check_website.request(self.final_website)
        resp = int(resp[0]['status'])

        return resp

    def print_currency_rate_today(self):

        resp = self.check_website()

        if resp == 200:
            # print("Response Code: ", resp)
            req = urllib.request.Request(self.final_website)
            data = urllib.request.urlopen(req).read()
            data = json.loads(data.decode('utf-8'))
            from_to = list(data.values())
            if (self.system == "linux" or self.system == "darwin"):
                os.system("clear")
            else:
                os.system("cls")
            print( "Today's exchange rate for %s to %s is %.2f\n" % (self.from_country, self.to_country, from_to[0]))
        else:
            print("self.final_website: \n\n", self.final_website)
            print("Response Code: \n", resp)
            print("Error website loading. \n")

    def print_exchanging(self):
        for key in self.currency_name.keys():
            if key == self.from_country:
                currency_name = self.currency_name[self.from_country]

        for key in self.currency_symbol.keys():
            if key == self.from_country:
                symbol_from = self.currency_symbol[self.from_country]
                symbol_to = self.currency_symbol[self.to_country]

        # print("temp: ", temp)
        currency_name = currency_name.split()
        new_word = ""
        if ((currency_name[-1][len(currency_name[-1]) - 1:]) == ")"):
            new_word = currency_name[-1].replace(")", "")
            # print("new_word: ", new_word)
            while True:
                try:
                    self.money_holding = float(input("How many %s are you trying to exchange? \n" % (new_word.lower())))
                except ValueError:
                    print("This is invalid amount of money. Please the amount of money that you currently hold right now.")
                else:
                    break


        else:
            while True:
                try:
                    self.money_holding = float(input("How many %s are you trying to exchange? \n" % (currency_name[-1].lower())))
                except ValueError:
                    print("This is invalid amount of money. Please the amount of money that you currently hold right now. \n")
                else:
                    break


        money_exchanged_from_country = self.calculate_exchange_rate_from_country(self.money_holding)
        money_exchanged_to_country = self.calculate_exchange_rate_to_country(self.money_holding)

        print("The money you exchange is %s to %s and you have received %s%.2f \n" % (self.from_country,
                                                                                      self.to_country,
                                                                                      symbol_from,
                                                                                      money_exchanged_from_country))

        temp = input("Do you want to know the exchange for %s to %s? Y/N \n" % (self.to_country, self.from_country))
        temp = temp.lower()
        if (temp == "y" or temp == "yes"):
            print("The money exchanged for %s to %s and you have received %s%.2f \n" % (self.to_country,
                                                                                       self.from_country,
                                                                                       symbol_to,
                                                                                       money_exchanged_to_country))
        else:
            sys.exit()

    def calculate_exchange_rate_from_country(self, money_holding):

        resp = self.check_website()

        money_from_to = 0

        if resp == 200:
            req = urllib.request.Request(self.final_website)
            data = urllib.request.urlopen(req).read()
            data = json.loads(data.decode('utf-8'))
            currency_today = list(data.values())
            money_from_to = (currency_today[0] * float(money_holding))
        else:
            print("Error Response: ", resp)

        return money_from_to

    def calculate_exchange_rate_to_country(self, money_holding):

        resp = self.check_website()

        if resp == 200:
            req = urllib.request.Request(self.final_website)
            data = urllib.request.urlopen(req).read()
            data = json.loads(data.decode('utf-8'))
            currency_today = list(data.values())
            money_to_from = (currency_today[1] * float(money_holding))
        else:
            print("Error Response: ", resp)

        return money_to_from


a = CurrencyConverter()
