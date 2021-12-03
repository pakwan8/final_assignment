####################################################################################################
# Fraser Pada, Thierry Laforge                                                                     #
# A terminal-based application to process and display data based on given user input and internet  #
# sourced csv files.                                                                               # 
#                                                                                                  #
####################################################################################################
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.image as im


class Dataset:
    def __init__(self, dataset, dataset_name, year):
        self.header = dataset[0]
        self.dataset_chopped = dataset[1::]
        self.year = year
        self.name = dataset_name
        self.vals = [[], [], [], []]
        for count, row in enumerate(self.dataset_chopped):
            if row[0][4::] == self.year:
                for i in range(4):
                    self.vals[i].append(float(row[i + 1]))
        self.columns = [np.array(i) for i in self.vals]
                
    def print_data(self, mode):
        print()
        if mode == "mean":
            for count, col in enumerate(self.columns):
                print(f"{np.mean(col):.2f} {self.header[count + 1]}")
            self.graph_data(mode)
        if mode == "max":
            for count, col in enumerate(self.columns):
                print(f"{np.max(col):.2f} {self.header[count + 1]}")
            self.graph_data(mode)
        if mode == "min":
            for count, col in enumerate(self.columns):
                print(f"{np.min(col):.2f} {self.header[count + 1]}")
            self.graph_data(mode)
        print()
        
        
    def graph_data(self, mode):
        fig = plt.figure(0)
        chart_items = ['All Sectors', 'Residential', 'Commercial', 'Industrial']
        if mode == "mean":
            chart_vals = [float(np.mean(col)) for count, col in enumerate(self.columns)]
        if mode == "max":
            chart_vals = [float(np.max(col)) for count, col in enumerate(self.columns)]
        if mode == "min":
            chart_vals = [float(np.min(col)) for count, col in enumerate(self.columns)]
        bars = plt.bar([1, 2, 3, 4], chart_vals)
        bars[0].set_color([0.75, 0, 0])
        bars[1].set_color([0, 0.75, 0])
        bars[2].set_color([0, 0, 0.75])
        bars[3].set_color([0.90, 0.90, 0])
        fig.canvas.manager.set_window_title(f"{self.name.title()} in {self.year} in The United States")
        plt.ylabel(f"{self.name.title()} ({self.header[1][11::]})")
        plt.title(f"{self.name.title()} in {self.year} in The United States")
        plt.xticks([1, 2, 3, 4], chart_items)
        plt.show()    


def main():
    #TODO: Possibly incorporate some sort of comparison. Could be something like comparing two years side by side in an ASCII table.
    
    retail_price = np.genfromtxt(r"./datasets/ave_retail_price.csv", delimiter=",", dtype="str", encoding="utf-8-sig")
    customer_accounts = np.genfromtxt(r"./datasets/num_cust_acc.csv", delimiter=",", dtype="str", encoding="utf-8-sig")
    retail_sales = np.genfromtxt(r"./datasets/retail_sales.csv", delimiter=",", dtype="str", encoding="utf-8-sig")
    revenue_from_sales = np.genfromtxt(r"./datasets/rev_retail_sales.csv", delimiter=",", dtype="str", encoding="utf-8-sig")
    stack_data = np.vstack([retail_price, customer_accounts, retail_sales, revenue_from_sales])
    option1_menu = {
        "1": lambda temp_class: temp_class.print_data("mean"),
        "2": lambda temp_class: temp_class.print_data("max"),
        "3": lambda temp_class: temp_class.print_data("min"),
    }
    option2_menu = {
        "retail price": retail_price,
        "customer accounts": customer_accounts,
        "retail sales": retail_sales,
        "revenue from sales": revenue_from_sales,
        "peepeepoopoo": ""
    } 
    print("\nThis program will find the monthly mean, min, or max over a year from an electrical dataset of your choice.\n" +
          "The available datasets are:\n  'Retail Price' (2001-2021)\n  'Customer Accounts' (2008-2021)\n  'Retail Sales' (2001-2021)\n"  +
          "  'Revenue from Sales' (2001-2021)\n")
    while True:
        option1 = input("1 - Mean\n2 - Max\n3 - Min\nh - Help\nq - Quit\n➜  ").strip().lower()
        print()
        if option1 in option1_menu:
            data_choice = input("Enter dataset: ").strip().lower()
            if data_choice in option2_menu.keys():
                data_year = input("Enter year: ").strip()
                limit = 2001
                if data_choice == "customer accounts":
                    limit = 2008
                if data_choice == "peepeepoopoo":
                    print("Hoorah you found the easter egg! What a fuckin idiot!")
                    bruh = plt.figure(figsize=(1, 1), dpi=100)
                    plt.imshow(im.imread(f"./ignore/spongeman.jpg"))
                    plt.xlabel("length")
                    plt.ylabel("girth")
                    plt.title("Lindsay's cock")
                    bruh.canvas.manager.set_window_title("Herro")
                    bruh.canvas.manager.full_screen_toggle()
                    bruh.canvas.toolbar.pack_forget()
                    bruh.set_facecolor([0, 0, 0])
                    plt.show()
                    limit = 6969
                if limit <= int(data_year) <= 2021:
                    option1_menu[option1](Dataset(option2_menu[data_choice], data_choice, data_year))
                else:
                    print("\nEnter a valid year for your dataset\n")
            else:
                print("\nPlease enter a valid dataset\n")
        elif option1 == "h":
            print("\nThis program will find the monthly mean, min, or max over a year from an electrical dataset of your choice.\n" +
                  "The available datasets are:\n  'Retail Price' (2001-2021)\n  'Customer Accounts' (2008-2021)\n  'Retail Sales' (2001-2021)\n" + 
                  "  'Revenue from Sales' (2001-2021)\nYou will need to choose either, Mean(1), Max(2), or Min(3)\n" + 
                  "after selecting an option you will be prompted to input a dataset and a year.\n" + 
                  "Choose these from the list above and follow the prompts.\n")
        elif option1 == "q":
            print("Thank you for using our program")
            exit()
        elif not(option1 in option1_menu.keys()):
            print("Please enter the number coresponding to the desired menu option.")
      
            
if __name__ == "__main__":
    main()
