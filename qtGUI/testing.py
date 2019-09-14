__author__ = "Patrick Wong"
__copyright__ = "Copyright by Patrick Wong"
import os
import urllib.request
import httplib2
import json
import sys
import platform
import pprint


class CurrencyConverter:

    def __init__(self):
        self.system = str(platform.system()).lower()
        self.data_processing("https://free.currconv.com/api/v7/currencies?apiKey=0348799f934010f56f8b")
        self.currency_name = {}
        self.currency_symbol = {}
        self.currency_abv = []
        self.money_holding = 0
        self.total_exchange = []

        self.currency_today = 0

        self.from_country = ""
        self.to_country = ""

        self.sort_currency()
        self.input_website()
        self.final_website = self.print_website(self.from_country, self.to_country)
        self.print_currency_rate_today()
        self.print_exchanging()

    def check_website(self, website):
        check_website = httplib2.Http()
        resp = check_website.request(website)
        resp = int(resp[0]['status'])

        return resp

    def data_processing(self, website):

        resp = self.check_website(website)

        if resp == 200:
            req = urllib.request.Request(website)
            self.data = urllib.request.urlopen(req).read()
            self.data = json.loads(self.data.decode('utf-8'))
            self.currency_today = list(self.data.values())
        else:
            print("Error Response: ", resp)

    def sort_currency(self):
        for k, dk in self.data.items():
            for i, di in dk.items():
                self.currency_abv.append(i)
                temp_name = di['currencyName'].split()
                temp_word = temp_name[-1]
                if (temp_name[-1] == "Rights"):
                    temp_name[-1] = temp_name[-1].replace("Rights", "")
                    temp_name[-1] += "Rights"
                elif (temp_name[-1][len(temp_name[-1]) - 1:]) == ")":
                    temp_name[-1] = temp_name[-1].replace(")", "")
                    temp_name[-1] += "s)"
                    temp_str = temp_name[-1]
                    di['currencyName'] = di['currencyName'].replace(temp_word, temp_str)
                else:
                    temp_name[-1] += "s"
                    temp_str = temp_name[-1]
                    di['currencyName'] = di['currencyName'].replace(temp_word, temp_str)

                self.currency_name[i] = di['currencyName']

                if 'currencySymbol' in di:
                    self.currency_symbol[i] = di['currencySymbol']
                else:
                    temp_words = di['currencyName'].split()
                    if (temp_words[-1][len(temp_words[-1]) - 2:]) == "s)":
                        temp_words[-1] = temp_words[-1].replace("s)", "")
                        temp_words[-1] += "s"
                    self.currency_symbol[i] = temp_words[-1]

    def print_website(self, from_country, to_country):
        from_currency = "https://free.currconv.com/api/v7/convert?q="
        to_currency = "&compact=ultra&apiKey=0348799f934010f56f8b"

        updated_website = ""

        updated_website += from_country + "_" + to_country + ","
        updated_website += to_country + "_" + from_country

        return from_currency + updated_website + to_currency

    def input_website(self):
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

        self.to_country = input("What currency do you want to exchange to? Type in the country abbreviation.  \n")
        self.from_country = input("What currency do you currently own? \n")

        self.to_country = self.to_country.upper()
        self.from_country = self.from_country.upper()

        if not (self.to_country in self.currency_abv and self.from_country in self.currency_abv):
            while not (self.to_country in self.currency_abv and self.from_country in self.currency_abv):
                print("This is not a valid currency. Please try again. \n")
                self.to_country = input("What currency do you want to exchange to? Type in the country abbreviation. \n")
                self.from_country = input("What currency do you currently own? \n")

                self.to_country = self.to_country.upper()
                self.from_country = self.from_country.upper()

        # print("valid currency")

        return self.to_country, self.from_country

    def print_currency_rate_today(self):

        self.data = self.data_processing(self.final_website)

        if (self.system == "linux" or self.system == "darwin"):
            os.system("clear")
        else:
            os.system("cls")
        print("Today's exchange rate for %s to %s is %.2f\n" % (self.from_country, self.to_country, self.currency_today[0]))

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
                    print(
                        "This is invalid amount of money. Please the amount of money that you currently hold right now.")
                else:
                    break


        else:
            while True:
                try:
                    self.money_holding = float(
                        input("How many %s are you trying to exchange? \n" % (currency_name[-1].lower())))
                except ValueError:
                    print(
                        "This is invalid amount of money. Please the amount of money that you currently hold right now. \n")
                else:
                    break

        money_exchanged_from_country = self.calculate_exchange_rate_from_country(self.money_holding)
        money_exchanged_to_country = self.calculate_exchange_rate_to_country(self.money_holding)
        print("len(symbol_from): ", len(symbol_from))
        if (len(symbol_from) < 2):
            print("The money you exchange is %s to %s and you have received %s%.2f \n" % (self.from_country,
                                                                                          self.to_country,
                                                                                          symbol_from,
                                                                                          money_exchanged_from_country))
        else:
            print("The money you exchange is %s to %s and you have received %.2f %s \n" % (self.from_country,
                                                                                          self.to_country,
                                                                                          money_exchanged_from_country,
                                                                                          symbol_from,))


        temp = input("Do you want to know the exchange for %s to %s? Y/N \n" % (self.to_country, self.from_country))
        temp = temp.lower()
        if (temp == "y" or temp == "yes"):
            print("len(symbol_to): ", len(symbol_to))
            if (len(symbol_to) < 2):
                print("The money exchanged for %s to %s and you have received %s%.2f \n" % (self.to_country,
                                                                                            self.from_country,
                                                                                            symbol_to,
                                                                                            money_exchanged_to_country))
            else:
                print("The money exchanged for %s to %s and you have received %.2f %s \n" % (self.to_country,
                                                                                            self.from_country,
                                                                                            money_exchanged_to_country,
                                                                                            symbol_to))

        else:
            sys.exit()

    def calculate_exchange_rate_from_country(self, money_holding):

        money_from_to = (self.currency_today[0] * float(money_holding))
        return money_from_to

    def calculate_exchange_rate_to_country(self, money_holding):

        money_to_from = (self.currency_today[1] * float(money_holding))
        return money_to_from


a = CurrencyConverter()
