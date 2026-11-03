# from Claude Code: comparison script (plumbing). The five rules and the 'first match wins' prediction below
# are copied from the Session 3 class notebook (the "From a dataset row to a prediction" cell; slides 13 and 15),
# with the conclusions shortened from "class=unacc" to "unacc". Scoring them on Serhii's train/test split
# is the only addition.
from data import COLUMNS, load, split

# the class example: five rules, "first match wins", default unacc
CLASS_RULES = [
    ({"safety=low"}, "unacc"),
    ({"persons=2"}, "unacc"),
    ({"safety=high", "buying=low"}, "good"),
    ({"safety=high", "buying=med"}, "good"),
    ({"persons=4"}, "acc"),
]


def predict_first_match(row):
    """The class notebook's strategy: the first rule in the list that matches decides."""
    facts = {col + "=" + str(row[col]) for col in COLUMNS[:-1]}
    for conditions, conclusion in CLASS_RULES:
        if conditions <= facts:
            return conclusion
    return "unacc"


if __name__ == "__main__":
    train, test = split(load())
    for name, part in [("train", train), ("test", test)]:
        predicted = part.apply(predict_first_match, axis=1)
        print("class example (five rules, first match wins), " + name + " accuracy:",
              round((predicted == part["class"]).mean(), 3))
