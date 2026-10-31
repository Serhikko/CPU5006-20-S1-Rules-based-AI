import pandas as pd # loads the library and lets me write pd. as a short name.
from data import COLUMNS, load, split # now importing the functions and variables from data.py
df = load()

print("\n------------------Shape of the dataframe------------------")
print(df.shape) # shape of the dataframe

print("\n------------------Dataframe info------------------")
df.info() # info about the dataframe, including the number of non-null values in each

print("\n------------------First 5 rows------------------")
print(df.head()) #  first 5 rows of the dataframe

print("\n------------------Missing values------------------")
print(df.isna().sum()) #  number of missing values in each column

print("\n------------------Duplicated rows------------------")
print(df.duplicated().sum()) #  number of duplicated rows in the dataframe

print("\n------------------Value counts of 'class' column------------------") 
print(df["class"].value_counts(normalize=True)) # normalized value counts of the "class" column


print("\n------------------Crosstab of each column with 'class' column------------------")
# from Claude Code: the two orderings below make the tables readable (classes worst -> best, values low -> high)
ORDER = ["unacc", "acc", "good", "vgood"]  # worst to best, instead of alphabetical
VALUE_ORDER = {
    "buying": ["low", "med", "high", "vhigh"],
    "maint": ["low", "med", "high", "vhigh"],
    "doors": ["2", "3", "4", "5more"],
    "persons": ["2", "4", "more"],
    "lug_boot": ["small", "med", "big"],
    "safety": ["low", "med", "high"],
}

for col in COLUMNS[:-1]: # for loop to iterate over all columns except the last one
    print("\n--- " + col + " (% of cars with that value) ---")
    table = pd.crosstab(df[col], df["class"], normalize="index") * 100  # share of each class per value, as a percentage
    print(table[ORDER].reindex(VALUE_ORDER[col]).round(0).astype(int))  # columns worst -> best, rows low -> high, whole numbers


print("\n------------------Splitting the dataframe into train and test sets------------------")
train, test = split(df) # splits the dataframe into train and test sets
print(len(train), len(test)) # prints the lengths of the train and test sets
print(train["class"].value_counts(normalize=True).round(3)) # prints the normalized value counts of the "class" column in the train set
print(test["class"].value_counts(normalize=True).round(3)) # .round 3 means round to 3 decimal places