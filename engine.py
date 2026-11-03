# from Claude Code: the skeleton of this file (imports, function names, docstrings and the step comments).
# The code inside each function was written by me (Serhii), following the step comments,adn normal comments.

# Reference: knowledge base and inference engine kept apart, Session 2 slide 21 (Components of Rule-Based Systems).
from data import COLUMNS
from knowledge import RULES


def row_to_facts(row):
    """Turn one row of the table into a set of facts like "safety=high"."""
    facts = set()

    # STEP 1: Convert each column into a fact
    for col in COLUMNS[:-1]:
        facts.add(col + "=" + str(row[col])) # Add the fact to the set

    return facts


# Reference: the forward_chain loop of Session 3 slide 10, with the fired list of slide 11 kept for the explanation.
def forward_chain(facts, rules):
    """Apply the rules again and again until no new fact appears."""
    facts = set(facts)
    fired = []
    changed = True

    # STEP 2: Apply rules until no new facts are generated
    while changed:
        changed = False

        for conditions, conclusion, reason in rules:
            if conditions <= facts and conclusion not in facts:
                facts.add(conclusion)
                fired.append((conditions, conclusion, reason)) # Add the rule to the fired list
                changed = True

    return facts, fired


# Reference: conflict resolution by priority (Session 3 slides 14-15); the default is the majority class (slide 26).
def verdict(facts):
    """Pick one class from the car facts. A veto (unacc) always wins."""

    # STEP 3: Check the veto first
    if "car=unacc" in facts:
        return "unacc"

    for name in ["vgood", "good", "acc"]:
        if "car=" + name in facts:
            return name

    return "unacc"


if __name__ == "__main__":

    # STEP 4: Test 1
    facts1 = {
        "buying=low",
        "maint=low",
        "doors=4",
        "persons=4",
        "lug_boot=big",
        "safety=high"
    }

    final_facts1, fired1 = forward_chain(facts1, RULES)

    print("TEST 1")
    print("Verdict:", verdict(final_facts1))
    print("Rules fired:")

    for rule in fired1:
        print(rule[2])

    print("\nNumber of rules fired:", len(fired1))

    # Test 2: Same car but with only 2 persons
    facts2 = {
        "buying=low",
        "maint=low",
        "doors=4",
        "persons=2",
        "lug_boot=big",
        "safety=high"
    }

    final_facts2, fired2 = forward_chain(facts2, RULES)

    print("\nTEST 2")
    print("Verdict:", verdict(final_facts2))
    print("Rules fired:")

    for rule in fired2:
        print(rule[2])

    print("\nNumber of rules fired:", len(fired2))

