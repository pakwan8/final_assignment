####################################################################################################
# Fraser Pada, Thierry Laforge                                                                     #
# A terminal-based application to process and display data based on given user input and internet  #
# sourced csv files.                                                                               #
#                                                                                                  #
####################################################################################################

import numpy as np
from matplotlib import pyplot as plt


class Dataset:
    def __init__(self, dataset):
        self.units = dataset[0][1][12:]
        self.dataset = dataset[1:]
        self.index_cols = [row[0] for row in self.dataset]
        self.sectors = {"all": [1, "all sectors"],
                        "residential": [2, "residential"],
                        "commercial": [3, "commercial"],
                        "industrial": [4, "industrial"]}
        self.months = ["january", "february", "march",
                       "april", "may", "june",
                       "july", "august", "september",
                       "october", "november", "december"]

    def index(self, sector, year, month=None):
        temp = []
        for index in self.dataset:
            if index[0][4:] == str(year):
                temp.append(index[self.sectors[sector][0]])

        if month == "":
            return dict(zip(self.months, temp[::-1]))

        else:
            return dict(zip(self.months, temp[::-1]))[month.lower()]


def calculate(dataset, year, sector, trunc=False):
    temp_data = Dataset(dataset)
    data_dict = temp_data.index(sector, year)
    year_values = np.array([val for val in data_dict.values()], dtype=np.float64)
    if not trunc:
        print()
        print(f"Mean for {year}:\t{np.round(np.mean(year_values), 2):.2f} {temp_data.units}")
        print(f"Min for {year}:\t{np.round(np.min(year_values), 2):.2f} {temp_data.units}")
        print(f"Max for {year}:\t{np.round(np.max(year_values), 2):.2f} {temp_data.units}")
        print()
    else:
        print()
        print(f"Mean for {year}:\t{int(np.trunc(np.mean(year_values)))} {temp_data.units}")
        print(f"Min for {year}:\t{int(np.trunc(np.min(year_values)))} {temp_data.units}")
        print(f"Max for {year}:\t{int(np.trunc(np.max(year_values)))} {temp_data.units}")
        print()


def compare(dataset, year, sector1, sector2):
    temp_data = Dataset(dataset)
    vals1 = np.array(temp_data.index(year, sector1), dtype=np.float64)
    vals2 = np.array(temp_data.index(year, sector2), dtype=np.float64)
    print("-" * 43)
    print(f"|{temp_data.sectors[sector1][1]:^20}vs{temp_data.sectors[sector2][1]:^19}|")
    print("-" * 43)
    for count in range(12):
        print(f"|{vals1[count]:^20.2f}|{vals2[count]:^20.2f}|")
    print("-" * 43)


def print_help(newline=False):
    if not newline:
        print("This program will find the monthly mean, min, or max over a year from an electrical dataset of your choice.")

    else:
        print("\nThis program will find the monthly mean, min, or max over a year from an electrical dataset of your choice.")

    print(f"The available datasets are:\n  'Retail Price' (2001-2021)\n  'Customer Accounts' (2008-2021)\n  'Retail Sales' (2001-2021)\n  'Revenue from Sales' (2001-2021)\n")


def verify(dataset=None, sector=None, year=None, month=""):
    passes = True
    failed_cases = []
    dataset_test = True if dataset in ["retailprice", "customeraccounts", "retailsales", "revenuefromsales"] or dataset is None else False
    if year is None:
        year_test = True
    elif year.isdigit():
        if 2001 <= int(year) <= 2020:
            year_test = True
        else:
            year_test = False
    else:
        year_test = False

    sector_test = True if sector in ["all", "residential", "commercial", "industrial"] or sector is None else False
    month_test = True if month in ["january", "february", "march", "april", "may", "june", "july", "august", "september", "october", "november", "december"] or month == "" else False
    tests = [dataset_test, sector_test, year_test, month_test]
    indexed_inputs = {0: dataset, 1: sector, 2: year, 3: month}
    for index, test in enumerate(tests):
        if not test:
            passes = False
            failed_cases.append([index, indexed_inputs[index]])

    return passes, failed_cases


retail_price = np.genfromtxt(r"./datasets/ave_retail_price.csv", delimiter=",", dtype="str", encoding="utf-8-sig")
customer_accounts = np.genfromtxt(r"./datasets/num_cust_acc.csv", delimiter=",", dtype="str", encoding="utf-8-sig")
retail_sales = np.genfromtxt(r"./datasets/retail_sales.csv", delimiter=",", dtype="str", encoding="utf-8-sig")
revenue_from_sales = np.genfromtxt(r"./datasets/rev_retail_sales.csv", delimiter=",", dtype="str", encoding="utf-8-sig")
datasets = {"retailprice": retail_price, "customeraccounts": customer_accounts, "retailsales": retail_sales, "revenuefromsales": revenue_from_sales}
options = {"1": calculate, "2": compare, "3": None, "h": print_help, "q": lambda: print("Thank you for using our program.")}

print_help()
while True:
    option = input("1 - Mean/Min/Max\n2 - Compare\n3 - Get data\nh - Help\nq - Quit\n➜  ").replace(" ", "").lower()
    if option not in options:
        print("Please enter the number or letter corresponding to the process you would like.")

    else:
        if option.isdigit():
            data_input = input("Dataset ➜ ").replace(" ", "").lower()
            year_input = input("Year    ➜ ").replace(" ", "")
            sector_input = input("Sector  ➜ ").replace(" ", "").lower()
            inputs = {0: "Dataset", 1: "Sector", 2: "Year", 3: "Month"}
            passed, fails = verify(data_input, sector_input, year_input)
            if not passed:
                print("Invalid data was inputted, please try again.")
                for fail in fails:
                    print(f"  >>> {inputs[fail[0]]}: '{fail[1]}'")
                print()
                continue

            else:
                dataset_final = datasets[data_input]
                year_final = int(year_input)
                sector_final = sector_input
                if option == "1":
                    if data_input == "customeraccounts":
                        calculate(dataset_final, year_final, sector_final, trunc=True)

                    else:
                        calculate(dataset_final, year_final, sector_final)
                    print("Some other matplotlib shit")

                if option == "2":
                    sector2_choice = input("Second sector ➜ ").replace(" ", "").lower()
                    passed, fails = verify(sector=sector2_choice)
                    if not passed:
                        print("Invalid data was inputted, please try again.")
                        for fail in fails:
                            print(f"  >>> {inputs[fail[0]]}: '{fail[1]}'")
                        print()
                        continue
                    sector2_final = sector2_choice
                    compare(dataset_final, year_final, sector_final, sector2_final)
                    print("Some matplotlib shit")

                if option == "3":
                    month_input = input("Month   ➜ ").replace(" ", "").lower()
                    passed, fails = verify(month=month_input)
                    if not passed:
                        print("Invalid data was inputted, please try again.")
                        for fail in fails:
                            print(f"  >>> {inputs[fail[0]]}: '{fail[1]}'")
                        print()
                        continue
                    month_final = month_input
                    dataset_obj = Dataset(dataset_final)
                    vals = dataset_obj.index(sector_final, year_final, month_final)
                    print()
                    if type(vals) is dict:
                        for index_month in vals:
                            print(f"{index_month.title():<10} - {np.round(np.float64(vals[index_month]), 2):<10.2f}")

                    else:
                        print(f"{month_final.title()} - {np.round(np.float64(vals), 2):.2f}")
                    print()

        else:
            if option == "q":
                options[option]()
                break

            else:
                options[option](True)
