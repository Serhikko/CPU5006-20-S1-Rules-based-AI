import pandas as pd # loads the library and lets me write pd. as a short name.

COLUMNS = ["buying", "maint", "doors", "persons", "lug_boot", "safety", "class"] # the seven column names, in the order given in car.names
df = pd.read_csv("data/car.data", header=None, names=COLUMNS) # stores the table in a variable called df so the following lines can use it

print(df.shape) # shape of the dataframe
print(df.head()) #  first 5 rows of the dataframe
print(df.isna().sum()) #  number of missing values in each column
print(df.duplicated().sum()) #  number of duplicated rows in the dataframe
print(df["class"].value_counts(normalize=True)) # normalized value counts of the "class" column

for col in COLUMNS[:-1]: # for loop to iterate over all columns except the last one
    print(col) # name of the column
    print(pd.crosstab(df[col], df["class"], normalize="index").round(2))  # prints the crosstab of the column and the "class" column, normalized by index