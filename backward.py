# from Claude Code: this file was written in full by Claude Code on the night before the deadline (3 Nov 2026),
# when Serhii ran out of time to write the body of its skeleton himself. It adapts the backward_chain / prove
# pattern of Session 3 (slides 20-21 and the class notebook warm-up) to the three-part rules of knowledge.py.
# The rules it reasons from are Serhii's, and so is the forward-chaining engine it complements.
# Run from the project folder:  .\.venv\Scripts\python.exe backward.py
from knowledge import RULES


def prove(goal, facts, rules, depth=0):
    """Try to prove ONE goal from the facts by working backwards through the rules.

    Prints one line per step, indented by depth, so the output reads like a proof.
    Returns True if the goal is a known fact or can be derived, otherwise False."""
    indent = "    " * depth
    if goal in facts:
        print(indent + goal + ": known fact")
        return True
    for conditions, conclusion, reason in rules:
        if conclusion == goal:
            needed = sorted(conditions)  # a fixed order, so the printed proof reads the same every run
            print(indent + goal + ": try rule needing " + ", ".join(needed))
            if all(prove(condition, facts, rules, depth + 1) for condition in needed):
                print(indent + goal + ": proved, because " + reason)
                return True
    print(indent + goal + ": cannot be proved")
    return False


if __name__ == "__main__":
    great_car = {"buying=low", "maint=low", "doors=4", "persons=4", "lug_boot=big", "safety=high"}
    two_seater = {"buying=low", "maint=low", "doors=4", "persons=2", "lug_boot=big", "safety=high"}

    print("Demo 1: can car=vgood be proved for the great car (low low 4 4 big high)?")
    print()
    print("Answer:", prove("car=vgood", great_car, RULES))
    print()
    print("Demo 2: can car=good be proved for the same car with only two seats?")
    print()
    print("Answer:", prove("car=good", two_seater, RULES))
