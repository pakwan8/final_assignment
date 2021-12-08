###################################################################################
#                                                                                 #
#   Fraser Pada, Thierry Laforge                                                  #
#   A terminal-based application to process and display data based on given user  #
#   input and internet sourced datasets.                                          #
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
        self.sectors = {"all": [1, "all sectors"], "residential": [2, "residential"], "commercial": [3, "commercial"], "industrial": [4, "industrial"]}
        self.months = ["january", "february", "march", "april", "may", "june", "july", "august", "september", "october", "november", "december"]

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

        return dict(zip(self.months, temp[::-1])) if month == "" else dict(zip(self.months, temp[::-1]))[month.lower()]


def calculate(dataset, year, sector, rounded=False):
    """
    A function to calculate and display the mean, min, and max according to whichever dataset, year, and sector.

    Parameters:
        dataset (array): Array of data which will be indexed.
        year (int): Year that data will be taken from (Row of desired data).
        sector (str): Sector that data will be taken from (Column of desired data).
        rounded (bool): Determines whether final answer will be rounded or not.

    Returns:
        year_values (array): list of values for the year.
    """
    temp_data = Dataset(dataset)
    data_dict = temp_data.index(sector, year)
    year_values = np.array(list(data_dict.values()), dtype=np.float64)
    if not rounded:
        print(f"\nMean for {year}:\t{np.round(np.mean(year_values), 2)} {temp_data.units}")
        print(f"Min for {year}:\t{np.round(np.min(year_values), 2)} {temp_data.units}")
        print(f"Max for {year}:\t{np.round(np.max(year_values), 2)} {temp_data.units}\n")
    else:
        print(f"\nMean for {year}:\t{int(np.mean(year_values))} {temp_data.units}")
        print(f"Min for {year}:\t{int(np.min(year_values))} {temp_data.units}")
        print(f"Max for {year}:\t{int(np.max(year_values))} {temp_data.units}\n")

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
        [sector1, vals1] (list): List of sector's name with its corresponding values.
        [sector2, vals2] (list): List of sector's name with its corresponding values.
    """
    temp_data = Dataset(dataset)
    vals1 = np.array(list(temp_data.index(sector1, year).values()), dtype=np.float64)
    vals2 = np.array(list(temp_data.index(sector2, year).values()), dtype=np.float64)
    print("-" * 63)
    print(f"|{temp_data.sectors[sector1][1] + ' (' + temp_data.units + ')':^30}vs{temp_data.sectors[sector2][1] + ' (' + temp_data.units + ')':^29}|")
    print("-" * 63)
    for count in range(12):
        print(f"|{vals1[count]:^30.0f}|{vals2[count]:^30.0f}|") if temp_data.units == "customers" else print(f"|{vals1[count]:^30.2f}|{vals2[count]:^30.2f}|")
    print("-" * 63 + "\n")

    return [sector1, vals1], [sector2, vals2]


def print_help(newline=False):
    """
    Prints the help menu which contains useful information such as possible datasets, year ranges, etc.

    Parameters:
        newline (bool): Prints the menu with a new line at the top if True and without if False.

    Returns:
        None
    """
    h_str = "This program will find the monthly mean, min, or max over a year from an electrical dataset of your choice."
    print("\n" + h_str) if newline is True else print(h_str)
    print(f"The available datasets are:\n" + "  'Retail Price' (2001-2021)\n" + "  'Customer Accounts' (2008-2021)\n" + "  'Retail Sales' (2001-2021)\n" + "  'Revenue from Sales' (2001-2021)\n")


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
    months = ["january", "february", "march", "april", "may", "june", "july", "august", "september", "october", "november", "december"]
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
    month_test = True if month_txt in months or month_txt is None or month_txt == "" else False
    tests = [dataset_test, sector_test, year_test, month_test]
    indexed_inputs = {0: dataset, 1: sector, 2: year, 3: month}
    for index, test in enumerate(tests):
        if not test:
            passes = False
            failed_cases.append([index, indexed_inputs[index]])

    return passes, failed_cases


def plot_data(dataset, name, year, values, factor, comparing=False, sectors=None, values2=None):
    """
    A function to facilitate graphing / plotting data using matplotlib

    Parameters:
        dataset (array): Array of the desired data to be processed.
        name (str): Name of the dataset.
        year (int): Year that data will be taken from (Row of desired data).
        values (array): First set of values to be plotted.
        factor (int): Used for scaling purposes in order to emphasize the differences between each value.
        comparing (bool): If True, will plot 2 sets of bars next to each other showing the difference between both value sets.
        sectors (list): List of sector names to be displayed in legend.
        values2 (array): Second set of values to be plotted if provided.

    Returns:
        None
    """
    temp_dataset = Dataset(dataset)
    plt.rcParams["toolbar"] = "None"  # Can change this in order to show the toolbar or not
    fig = plt.figure(figsize=[10, 8], facecolor=[0, 0, 0], tight_layout=True)
    if name.replace(" ", "") == "customeraccounts" or name.replace(" ", "") == "revenuefromsales":
        plt.title(f"United States Electrical {name.capitalize()} in {year}", color=[1, 1, 1], fontsize=16)
    else:
        plt.title(f"United States Electricity {name.capitalize()} in {year}", color=[1, 1, 1], fontsize=18)
    plt.xlabel("Months", fontsize=14)
    plt.ylabel(temp_dataset.units, fontsize=14)
    fig.canvas.manager.set_window_title(name.title())
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
        plt.bar([x for x in range(1, 13)], np.array(values, dtype=np.float64), color=[0, 1, 0], edgecolor=[1, 1, 1], width=0.8, label=sectors[0])
    else:
        plt.bar([x + 0.2 for x in range(1, 13)], np.array(values, dtype=np.float64), color=[0, 0, 1], edgecolor=[1, 1, 1], width=0.4, label=sectors[1])
        plt.bar([x - 0.2 for x in range(1, 13)], np.array(values2, dtype=np.float64), color=[1, 0, 0], edgecolor=[1, 1, 1], width=0.4, label=sectors[0])
    plt.legend()
    plt.show()


def plot_ms(dataset, name, year, values, factor):
    """
    Function to plot the mean, min, and max.

    Parameters:
        dataset (array): Array of the desired data to be processed.
        name (str): Name of the dataset.
        year (int): Year that data will be taken from.
        values (array): Array of values to be plotted.
        factor (float): Float for how the graph should be scaled.

    Returns:
        None
    """
    temp_dataset = Dataset(dataset)
    plt.rcParams["toolbar"] = "None"  # Can change this in order to show the toolbar or not
    fig = plt.figure(facecolor=[0, 0, 0], tight_layout=True)
    plt.title(f"Calculated Values for {name.capitalize()} in {year}", color=[1, 1, 1])
    plt.xlabel("Calculated Values", fontsize=14)
    plt.ylabel(temp_dataset.units.title(), fontsize=14)
    fig.canvas.manager.set_window_title(name.title())
    plt.ylim(np.min(values) - 1 * factor, np.max(values) + 1 * factor)
    plt.xticks([1, 2, 3], ["Mean", "Min", "Max"])
    ax = plt.gca()
    ax.spines['bottom'].set_color([1, 1, 1])
    ax.spines['top'].set_color([0.35, 0.35, 0.35])
    ax.spines['right'].set_color([0.35, 0.35, 0.35])
    ax.spines['left'].set_color([1, 1, 1])
    ax.xaxis.label.set_color([1, 1, 1])
    ax.yaxis.label.set_color([1, 1, 1])
    ax.set_facecolor([0, 0, 0])
    ax.tick_params(axis='x', colors=[1, 1, 1])
    ax.tick_params(axis='y', colors=[1, 1, 1])
    plt.bar([1], np.float64(np.mean(values)), color=[1, 0, 0], edgecolor=[1, 1, 1], width=0.7, label="Mean")
    plt.bar([2], np.float64(np.min(values)), color=[0, 1, 0], edgecolor=[1, 1, 1], width=0.7, label="Min")
    plt.bar([3], np.float64(np.max(values)), color=[0, 0, 1], edgecolor=[1, 1, 1], width=0.7, label="Max")
    plt.legend()
    plt.show()


def main():
    retail_price = np.genfromtxt(r"./datasets/ave_retail_price.csv", delimiter=",", dtype="str", encoding="utf-8-sig")
    customer_accounts = np.genfromtxt(r"./datasets/num_cust_acc.csv", delimiter=",", dtype="str", encoding="utf-8-sig")
    retail_sales = np.genfromtxt(r"./datasets/retail_sales.csv", delimiter=",", dtype="str", encoding="utf-8-sig")
    revenue_from_sales = np.genfromtxt(r"./datasets/rev_retail_sales.csv", delimiter=",", dtype="str", encoding="utf-8-sig")
    datasets = {"retailprice": retail_price, "customeraccounts": customer_accounts, "retailsales": retail_sales, "revenuefromsales": revenue_from_sales}
    options = {"1": calculate, "2": compare, "3": None, "h": print_help, "q": lambda: print("Thank you for using our program.")}
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
                    if option == "1":
                        if data_input.replace(" ", "") == "customeraccounts":
                            vals = calculate(dataset_final, year_final, sector_final, rounded=True)
                            plot_ms(dataset_final, data_input, year_final, vals, np.min(vals) / 100)
                        elif data_input.replace(" ", "") == "revenuefromsales" or data_input.replace(" ", "") == "retailsales":
                            vals = calculate(dataset_final, year_final, sector_final, rounded=True)
                            plot_ms(dataset_final, data_input, year_final, vals, np.min(vals))
                        else:
                            vals = calculate(dataset_final, year_final, sector_final, rounded=False)
                            plot_ms(dataset_final, data_input, year_final, vals, 1)
                    if option == "2":
                        sector2_choice = input("Sector 2: ").replace(" ", "").lower()
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
                            plot_data(dataset_final, data_input, year_final, values2[1], 100, values2=values1[1], sectors=[values1[0], values2[0]], comparing=True)
                        else:
                            plot_data(dataset_final, data_input, year_final, values1[1], 10, values2=values2[1], sectors=[values1[0], values2[0]], comparing=True)
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
                                plot_data(dataset_final, data_input, year_final, [np.float64(val) for val in vals_dict.values()], 100, sectors=[sector_final])
                            else:
                                plot_data(dataset_final, data_input, year_final, [np.float64(val) for val in vals_dict.values()], 10, sectors=[sector_final])
                        else:
                            if data_input.replace(" ", "") == "customeraccounts":
                                print(f"{month_final.title()} - {np.round(np.float64(vals_dict), 2):.0f}")
                            else:
                                print(f"{month_final.title()} - {np.round(np.float64(vals_dict), 2):.2f}")
                        print()
            else:
                if option == "h":
                    print_help(True)
                else:
                    print("\nThanks for using our program.\n")
                    break


if __name__ == "__main__":
    main()
