###################################################################################
#                                                                                 #
#   Fraser Pada, Thierry Laforge                                                  #
#   A terminal-based application to process and display data based on given user  #
#   input and internet sourced datasets.                                          #
#                                                                                 #
#                                                                                 #
#   !!! DO NOT FORGET TO PUT A LEGEND FOR THE PLOTS !!!                           #
#                                                                                 #
#                                                                                 #
###################################################################################

import numpy as np
from matplotlib import pyplot as plt


class Dataset:
    """
    A class to modify a dataset in order to more effectively use it.

    Attributes:
        dataset (array): Array of the desired data to be processed.
    """

    def __init__(self, dataset):
        """
        Constructor for the dataset class. Will prep the dataset by modifying the array passed in.

        Parameters:
            dataset (array): Array of the desired data to be processed.
        """
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

    def index(self, sector, year, month=""):
        """
        Used to facilitate indexing the numpy array by returning dictionaries populated with specific data.

        Parameters:
            sector (str): Sector from which the data will be taken.
            year (int): Year from which the data will be taken.
            month (str): Specific month from the year that was provided for which the data will be taken.

        Returns:
            (dict): Depending on whether the month variable was passed,
                    will return dictionary of month and data from sector
                    or all months from year specified and chosen sector.
        """
        temp = []
        for index in self.dataset:
            if index[0][4:] == str(year):
                temp.append(index[self.sectors[sector][0]])

        if month == "":
            return dict(zip(self.months, temp[::-1]))

        else:
            return dict(zip(self.months, temp[::-1]))[month.lower()]


def calculate(dataset, year, sector, rounded=False):
    """
    A function to calculate and display the mean, min, and max according to whichever dataset, year, and sector.

    Parameters:
        dataset (array): Array of data which will be indexed.
        year (int): Year that data will be taken from (Row of desired data).
        sector (str): Sector that data will be taken from (Column of desired data).
        rounded (bool): Determines whether final answer will be rounded or not.

    Returns:
        year_values (array)
    """
    temp_data = Dataset(dataset)
    data_dict = temp_data.index(sector, year)
    year_values = np.array([val for val in data_dict.values()], dtype=np.float64)
    if not rounded:
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

    return year_values


def compare(dataset, year, sector1, sector2):
    """
    Compares two sectors from a given year from the chosen dataset and displays the data in a table.

    Parameters:
        dataset (array): Array of data which will be indexed.
        year (int): Year that data will be taken from (Row of desired data).
        sector1 (str): First sector that data will be taken from (First column of desired data).
        sector2 (str): Second sector that data will be taken from (Second column of desired data).

    Returns:
        vals1 (array): First set of calculated values
        vals2 (array): Second set of calculated values
    """
    temp_data = Dataset(dataset)
    vals1 = np.array([val for val in temp_data.index(sector1, year).values()], dtype=np.float64)
    vals2 = np.array([val for val in temp_data.index(sector2, year).values()], dtype=np.float64)
    print("-" * 63)
    print(f"|{temp_data.sectors[sector1][1] + ' (' + temp_data.units + ')':^30}vs{temp_data.sectors[sector2][1] + ' (' + temp_data.units + ')':^29}|")
    print("-" * 63)
    for count in range(12):
        if temp_data.units == "customers":
            print(f"|{vals1[count]:^30.0f}|{vals2[count]:^30.0f}|")
        else:
            print(f"|{vals1[count]:^30.2f}|{vals2[count]:^30.2f}|")
    print("-" * 63 + "\n")
    return vals1, vals2


def print_help(newline=False):
    """
    Prints the help menu which contains useful information such as possible datasets, year ranges, etc.

    Parameters:
        newline (bool): Prints the menu with a new line at the top if True and without if False.

    Returns:
        None
    """
    if not newline:
        print("This program will find the monthly mean, min, or max over a year from an electrical dataset of your choice.")

    else:
        print("\nThis program will find the monthly mean, min, or max over a year from an electrical dataset of your choice.")

    print(f"The available datasets are:\n" +
          "  'Retail Price' (2001-2021)\n" +
          "  'Customer Accounts' (2008-2021)\n" +
          "  'Retail Sales' (2001-2021)\n" +
          "  'Revenue from Sales' (2001-2021)\n")


def verify(dataset=None, sector=None, year=None, month=None):
    """
    Verifies that given data is valid. Pretty much just basic error handling.

    Parameters:
        dataset (array): Array of data which will be indexed.
        sector (str): First sector that data will be taken from (Column of desired data).
        year (int): Year that data will be taken from (Row of desired data).
        month (str): Month that data will be taken from if provided.

    Returns:
        passes (bool): Used to determine which (if any) tests have failed.
        failed_cases (list): List containing which tests failed (if any).
    """
    passes = True
    failed_cases = []
    dataset_txt = dataset.replace(" ", "") if dataset is not None else None
    sector_txt = sector.replace(" ", "") if sector is not None else None
    year_txt = year.replace(" ", "") if year is not None else None
    month_txt = month.replace(" ", "") if month is not None else ""
    dataset_test = True if dataset_txt in ["retailprice", "customeraccounts", "retailsales", "revenuefromsales"] or dataset is None else False
    if year_txt is not None:
        if year_txt.isdigit():
            if dataset_txt != "customeraccounts":
                year_test = True if 2001 <= int(year_txt) <= 2021 else False

            else:
                year_test = True if 2008 <= int(year_txt) <= 2021 else False

        else:
            year_test = False
    else:
        year_test = True

    sector_test = True if sector_txt in ["all", "residential", "commercial", "industrial"] or sector is None else False
    month_test = True if month_txt in ["january", "february", "march", "april", "may", "june",
                                       "july", "august", "september", "october", "november", "december"] or month_txt is None or month_txt == "" else False
    tests = [dataset_test, sector_test, year_test, month_test]
    indexed_inputs = {0: dataset, 1: sector, 2: year, 3: month}
    for index, test in enumerate(tests):
        if not test:
            passes = False
            failed_cases.append([index, indexed_inputs[index]])

    return passes, failed_cases


def plot_data(dataset, name, values, colors, factor, comparing=False, values2=None):
    """
    A function to facilitate graphing / plotting data using matplotlib

    Parameters:
        dataset (array): Array of the desired data to be processed.
        name (str): Name of the dataset.
        values (array): First set of values to be plotted.
        colors (array): Array of arrays containing RGB values for the colors of the bars.
        factor (int): Used for scaling purposes in order to emphasize the differences between each value.
        comparing (bool): If True, will plot 2 sets of bars next to each other showing the difference between both value sets.
        values2 (array): Second set of values to be plotted if provided.

    Returns:
        None
    """
    temp_dataset = Dataset(dataset)
    plt.rcParams["toolbar"] = "None"
    plt.figure(facecolor=[0, 0, 0], tight_layout=True)
    plt.title(name.title(), color=[1, 1, 1], fontsize=16)
    plt.xlabel("Months", fontsize=14)
    plt.ylabel(temp_dataset.units, fontsize=14)
    comb_vals = np.array(list(values) + list(values2)) if values2 is not None else np.array(list(values))
    comb_vals_n = [x for x in comb_vals if x is not None]
    plt.ylim(int(np.min(comb_vals_n)) - (int(np.min(comb_vals_n)) / factor), int(np.max(comb_vals_n)) + (int(np.max(comb_vals_n)) / factor))
    plt.xticks([x for x in range(1, 13)], [m.title() for m in temp_dataset.months])
    ax = plt.gca()
    ax.spines['bottom'].set_color([1, 1, 1])
    ax.spines['top'].set_color([0.35, 0.35, 0.35])
    ax.spines['right'].set_color([0.35, 0.35, 0.35])
    ax.spines['left'].set_color([1, 1, 1])
    ax.xaxis.label.set_color([1, 1, 1])
    ax.yaxis.label.set_color([1, 1, 1])
    ax.set_facecolor([0, 0, 0])
    ax.tick_params(axis='x', colors=[1, 1, 1], labelrotation=35)
    ax.tick_params(axis='y', colors=[1, 1, 1])

    if not comparing:
        plt.bar([x for x in range(1, 13)], values, color=[[float(y) / 255 for y in x] for x in colors], edgecolor=[1, 1, 1], width=0.8)

    else:
        plt.bar([x + 0.2 for x in range(1, 13)], np.array(values, dtype=np.float64), color=[[float(y) / 255 for y in x] for x in colors], edgecolor=[1, 1, 1], width=0.4)
        plt.bar([x - 0.2 for x in range(1, 13)], np.array(values2, dtype=np.float64), color=[[float(y) / 255 for y in x] for x in colors], edgecolor=[1, 1, 1], width=0.4)

    plt.show()


def main():
    retail_price = np.genfromtxt(r"./datasets/ave_retail_price.csv", delimiter=",", dtype="str", encoding="utf-8-sig")
    customer_accounts = np.genfromtxt(r"./datasets/num_cust_acc.csv", delimiter=",", dtype="str", encoding="utf-8-sig")
    retail_sales = np.genfromtxt(r"./datasets/retail_sales.csv", delimiter=",", dtype="str", encoding="utf-8-sig")
    revenue_from_sales = np.genfromtxt(r"./datasets/rev_retail_sales.csv", delimiter=",", dtype="str", encoding="utf-8-sig")
    datasets = {"retailprice": retail_price, "customeraccounts": customer_accounts,
                "retailsales": retail_sales, "revenuefromsales": revenue_from_sales}
    options = {"1": calculate, "2": compare, "3": None, "h": print_help, "q": lambda: print("Thank you for using our program.")}
    bar_colors_rgb = [[200, 0, 0], [200, 80, 10], [200, 200, 0], [80, 200, 0],
                      [0, 200, 0], [0, 200, 80], [0, 200, 200], [0, 80, 200],
                      [0, 0, 200], [80, 0, 200], [200, 0, 200], [200, 0, 80]]

    print_help()
    while True:
        option = input("1 - Mean/Min/Max\n2 - Compare\n3 - Get data\nh - Help\nq - Quit\n> ").replace(" ", "").lower()
        if option not in options:
            print("\nPlease enter the number or letter corresponding to the process you would like.\n")

        else:
            if option.isdigit():
                data_input = input("Dataset: ").lower()
                year_input = input("Year: ")
                sector_input = input("Sector 1: ").lower()
                inputs = {0: "Dataset", 1: "Sector", 2: "Year", 3: "Month"}
                passed, fails = verify(data_input, sector_input, year_input)
                if not passed:
                    print("Invalid data was inputted, please try again.")
                    for fail in fails:
                        print(f"  ➜ {inputs[fail[0]]}: '{fail[1]}'")
                    print()
                    continue

                else:
                    dataset_final = datasets[data_input.replace(" ", "")]
                    year_final = int(year_input.replace(" ", ""))
                    sector_final = sector_input
                    dataset_obj = Dataset(dataset_final)
                    if option == "1":
                        if data_input.replace(" ", "") == "customeraccounts":
                            vals = calculate(dataset_final, year_final, sector_final, rounded=True)
                            plot_data(dataset_final, data_input, vals, bar_colors_rgb, 100)

                        else:
                            vals = calculate(dataset_final, year_final, sector_final, rounded=False)
                            plot_data(dataset_final, data_input, vals, bar_colors_rgb, 10)

                    if option == "2":
                        sector2_choice = input("Second 2: ").replace(" ", "").lower()
                        passed, fails = verify(sector=sector2_choice)
                        if not passed:
                            print("Invalid data was inputted, please try again.")
                            for fail in fails:
                                print(f"  ➜ {inputs[fail[0]]}: '{fail[1]}'")
                            print()
                            continue
                        sector2_final = sector2_choice
                        values1, values2 = compare(dataset_final, year_final, sector_final, sector2_final)
                        if data_input.replace(" ", "") == "customeraccounts":
                            plot_data(dataset_final, data_input, values1, bar_colors_rgb, 100, values2=values2, comparing=True)

                        else:
                            plot_data(dataset_final, data_input, values1, bar_colors_rgb, 10, values2=values2, comparing=True)

                    if option == "3":
                        print("(Leave blank to see every month)")
                        month_input = input("Month: ").lower()
                        passed, fails = verify(month=month_input)
                        if not passed:
                            print("Invalid data was inputted, please try again.")
                            for fail in fails:
                                print(f"  ➜ {inputs[fail[0]]}: '{fail[1]}'")
                            print()
                            continue
                        month_final = month_input
                        dataset_obj = Dataset(dataset_final)
                        vals_dict = dataset_obj.index(sector_final, year_final, month_final)
                        print()
                        if type(vals_dict) is dict:
                            for index_month in vals_dict:
                                print(f"{index_month.title():^10} - {np.round(np.float64(vals_dict[index_month]), 2):^10.2f}")

                            if data_input.replace(" ", "") == "customeraccounts":
                                plot_data(dataset_final, data_input, bar_colors_rgb, vals_dict.values(), 100)

                            else:
                                plot_data(dataset_final, data_input, bar_colors_rgb, vals_dict.values(), 10)

                        else:
                            if data_input.replace(" ", "") == "customeraccounts":
                                print(f"{month_final.title()} - {np.round(np.float64(vals_dict), 2):.0f}")

                            else:
                                print(f"{month_final.title()} - {np.round(np.float64(vals_dict), 2):.2f}")
                        print()

            else:
                if option == "q":
                    options[option]()
                    break

                else:
                    options[option](True)


if __name__ == "__main__":
    main()
