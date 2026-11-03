# from Claude Code: command-line explanation tool (plumbing). Everything it prints about a car
# comes from Serhii's rules (knowledge.py) and reasoning (engine.py).
# Run from the project folder, giving the six values in the data order:
#   .\.venv\Scripts\python.exe explain.py low low 4 4 big high
#   (buying maint doors persons lug_boot safety)
import sys
from data import COLUMNS, load
from knowledge import RULES
from engine import forward_chain, verdict

ATTRIBUTES = COLUMNS[:-1]


def check_values(values):
    """Stop with a clear message if the number of values or a spelling is wrong."""
    df = load()
    if len(values) != len(ATTRIBUTES):
        print("Please give exactly", len(ATTRIBUTES), "values, in this order:", " ".join(ATTRIBUTES))
        sys.exit(1)
    for col, value in zip(ATTRIBUTES, values):
        allowed = sorted(df[col].unique())
        if value not in allowed:
            print("Unknown value " + repr(value) + " for " + col + ". Allowed:", ", ".join(allowed))
            sys.exit(1)


def explain(values):
    facts = {col + "=" + value for col, value in zip(ATTRIBUTES, values)}
    final_facts, fired = forward_chain(facts, RULES)
    print()
    print("The car: " + ", ".join(col + "=" + value for col, value in zip(ATTRIBUTES, values)))
    print()
    print("Rules that fired, in order (forward chaining):")
    if not fired:
        print("  none - no rule matched this car")
    for number, (conditions, conclusion, reason) in enumerate(fired, 1):
        print("  " + str(number) + ". IF " + " AND ".join(sorted(conditions)) + " THEN " + conclusion)
        print("     because: " + reason)
    answers = sorted(fact for fact in final_facts if fact.startswith("car="))
    print()
    print("Final answers concluded: " + (", ".join(answers) if answers else "none (default applies)"))
    print("Verdict: " + verdict(final_facts) + "   (unacc always wins, then vgood, good, acc; nothing concluded = unacc)")


if __name__ == "__main__":
    check_values(sys.argv[1:])
    explain(sys.argv[1:])
