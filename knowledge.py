# from Claude Code: this header, the rule format and the first two rules (as an example of the format).
# The list of rules to write was planned in the Claude Code tutoring chat;
# the rules below were typed, and their reasons written, by me (Serhii).
#
# A fact is a string like "safety=low" (column=value, spelled exactly as in the data).
# A rule is (conditions, conclusion, reason):
#   conditions = a set of facts that must ALL be true,
#   conclusion = the new fact we may add,
#   reason     = one sentence, printed later as the explanation.
# A conclusion starting with "car=" is a final answer.
# Any other conclusion is a helper fact (a concept) that other rules can use.

# Reference: rules as (set of conditions, conclusion) follow Session 3 slide 8; the reason sentences in the third part are mine.
# Helper facts that later rules build on are the mammal -> carnivore -> tiger chain of slides 8-9.
RULES = [
    # Reference: the same two vetoes as the class example on Session 3 slide 13.
    ({"persons=2"}, "car=unacc", "A car with only two seats is never acceptable (100% Unacc in the data)."),# 1
    ({"safety=low"}, "car=unacc", "Low safety is a veto (100% Unacc in the data)."),# 1.1

    # Reference: OR is written as two rules with the same conclusion, as on Session 3 slide 13.
    ({"buying=low"}, "cheap_to_buy", "Low buying cost makes the car cheap to buy."),# 2
    ({"buying=med"}, "cheap_to_buy", "Medium buying cost is still considered affordable(ie.cheap to buy)."),# 2.1

    ({"maint=low"}, "cheap_to_run", "Low maintenance costs make the car cheap to maintain."),# 3
    ({"maint=med"}, "cheap_to_run", "Medium maintenance costs are considered affordable to maintain."),# 3.1

    ({"cheap_to_buy", "cheap_to_run"}, "price=low", "Affordable buying and maintenance costs show a low overall price."),# 4

    ({"buying=vhigh", "maint=vhigh"}, "price=vhigh", "Very high buying and maintenance costs make the car unaffordable."),# 5
    ({"buying=vhigh", "maint=high"}, "price=vhigh", "Very high buying costs and high maintenance costs make the car unaffordable."),# 5.1
    ({"buying=high", "maint=vhigh"}, "price=vhigh", "High buying costs and very high maintenance costs make the car unaffordable."),# 5.2

    ({"price=vhigh"}, "car=unacc", "A very high overall price makes the car unacceptable."),# 6

    ({"persons=4"}, "family_car", "A car with four seats can fit a family."),# 7
    ({"persons=more"}, "family_car", "A car with more than four seats can fit a family."),# 7.1

    # Reference: several car= answers can be true at once; engine.verdict picks one (conflict resolution, Session 3 slides 14-15).
    ({"family_car", "safety=med"}, "car=acc", "A family car with medium safety is acceptable."),# 8
    ({"family_car", "safety=high"}, "car=acc", "A family car with high safety is acceptable."),# 8.1

    ({"price=low", "family_car", "safety=med"}, "car=good", "An affordable family car with medium safety is considered good."),# 9
    ({"price=low", "family_car", "safety=high"}, "car=good", "An affordable family car with high safety is considered good."),# 9.1

    ({"price=low", "family_car", "safety=high", "lug_boot=med"}, "car=vgood", "An affordable family car with high safety and medium luggage space is considered very good."),# 10
    ({"price=low", "family_car", "safety=high", "lug_boot=big"}, "car=vgood", "An affordable family car with high safety and large luggage space is considered very good."),# 10.1
]
