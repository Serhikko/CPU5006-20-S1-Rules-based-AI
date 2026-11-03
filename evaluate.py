# from Claude Code: evaluation script (plumbing). It only measures. The rules (knowledge.py)
# and the reasoning (engine.py) are Serhii's work.
# Run from the project folder:
#   .\.venv\Scripts\python.exe evaluate.py          -> TRAIN score and the error analysis (use this while changing rules)
#   .\.venv\Scripts\python.exe evaluate.py test     -> the same plus the TEST score (run once per version, when the rules are final)
import sys
import pandas as pd
from data import COLUMNS, load, split
from knowledge import RULES
from engine import row_to_facts, forward_chain, verdict

ORDER = ["unacc", "acc", "good", "vgood"]  # worst to best


def predict(df):
    """Run the expert system on every row and return the predicted class of each row."""
    predictions = []
    for _, row in df.iterrows():
        facts, fired = forward_chain(row_to_facts(row), RULES)
        predictions.append(verdict(facts))
    return pd.Series(predictions, index=df.index, name="predicted")


def report(name, df):
    """Print accuracy, the confusion matrix and the recall of each class."""
    predicted = predict(df)
    actual = df["class"]
    print()
    print("------------------ " + name + " ------------------")
    print("rows:", len(df), "  rules:", len(RULES))
    print("accuracy:", round((predicted == actual).mean(), 3))
    print()
    print("confusion matrix (rows = real class, columns = predicted class)")
    matrix = pd.crosstab(actual, predicted).reindex(index=ORDER, columns=ORDER, fill_value=0)
    print(matrix)
    print()
    print("recall per class (share of each real class that was predicted correctly)")
    for c in ORDER:
        print("  " + c + ":", round(matrix.loc[c, c] / matrix.loc[c].sum(), 2))
    return predicted


def error_analysis(df, predicted):
    """Show what the wrong predictions have in common.

    Only ever run this on TRAIN, so the test set is never used to design rules (no peeking)."""
    wrong = df[predicted != df["class"]].copy()
    wrong["predicted"] = predicted[wrong.index]
    print()
    print("------------------ error analysis on TRAIN ------------------")
    print("wrong rows:", len(wrong), "of", len(df))
    print()
    print("how many of each kind (real class, predicted class):")
    kinds = wrong.groupby(["class", "predicted"]).size().sort_values(ascending=False)
    print(kinds.to_string())
    for (real, pred), group in wrong.groupby(["class", "predicted"]):
        print()
        print("real " + real + " but predicted " + pred + " (" + str(len(group)) + " cars). Their values:")
        for col in COLUMNS[:-1]:
            counts = group[col].value_counts()
            print("  " + col + ": " + ", ".join(value + " " + str(int(n)) for value, n in counts.items()))


if __name__ == "__main__":
    train, test = split(load())
    train_predicted = report("TRAIN (the rules are designed on this half)", train)
    error_analysis(train, train_predicted)
    if "test" in sys.argv:
        report("TEST (held out; look at it once per version, when the rules are final)", test)
    else:
        print()
        print("(TEST not shown. Run  evaluate.py test  once per version, when the rules are final, to see the held-out score.)")
