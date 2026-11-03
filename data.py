# from Claude Code: loading and a stratified hold-out split
# comments writtten by me
import pandas as pd

COLUMNS = ["buying", "maint", "doors", "persons", "lug_boot", "safety", "class"] #seven column names, in the order given in car.names

def load(path="data/car.data"): 
    """Read car.data (no header line) into a table."""
    return pd.read_csv(path, header=None, names=COLUMNS) # returns pd from read_csv, with the column names specified in COLUMNS


def split(df, test_share=0.3, seed=42): # splts the dataframe into train and test sets, with a specified test share and random seed
    """Hold out test_share of EACH class, so rare classes appear in both halves."""
    test = df.groupby("class").sample(frac=test_share, random_state=seed) # takes a sample of the dataframe, grouped by the "class" column, with a fraction of test_share and a random seed for reproducibility
    train = df.drop(test.index) # drops the rows in test from the original dataframe to create the train set
    return train, test

