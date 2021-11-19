# TODO: Obtain datasets to work with. Put into datasets folder.
# TODO: Import pop_data sets in order to read them.
# TODO: Create search engine that uses keywords. (Can be done using lists?)
# TODO: Figure out if using pandas can replace the 3 numpy arrays as per the requirements.
# TODO: Figure out how the user input can manipulate the pop_data in the csv (Pandas can write to cells easily I think.)
# TODO: Once finding the pop_data, display to user in nice way. (Data table using matplotlib or using CLI table.)
# TODO: Once all this shite is done make other shit like the pdf and prep the demo
# TODO: Return to monke
# TODO: Don't eat shit
# Run 'python -m pip install -r requirements.txt' after activating virtual environment.
# (Top line really just install pandas for TAs. Still not 100% sure if we can use it but Marasco said we could so idk)
import pandas as pd

# Imports the csv file and sets the first column as row indices
# (Might have to change this next line if the pop_data is formatted a different way)

pop_data = pd.read_csv(r"datasets\Population_Data.csv", index_col=0)
co_data = pd.read_csv(r"datasets\Country_Data.csv", index_col=0)
print(pop_data)
print(co_data)

# Able to now access items by DataFrame.loc[row, column]
peepee = pop_data.loc["Vietnam", "2018 Pop"]
poopoo = co_data.loc["Vietnam", "UN Region"]
print(peepee)
print(poopoo)
