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
    ({"persons=2"}, "car=unacc", "A car with only two seats is never acceptable (100% Unacc in the data)."),
    ({"safety=low"}, "car=unacc", "Low safety is a veto (100% Unacc in the data)."),

    # Reference: OR is written as two rules with the same conclusion, as on Session 3 slide 13.
    ({"buying=low"}, "cheap_to_buy", "Low buying cost makes the car cheap to buy."),
    ({"buying=med"}, "cheap_to_buy", "Medium buying cost is still considered affordable(ie.cheap to buy)."),

    ({"maint=low"}, "cheap_to_run", "Low maintenance costs make the car cheap to maintain."),
    ({"maint=med"}, "cheap_to_run", "Medium maintenance costs are considered affordable to maintain."),

    #LOW
    ({"buying=low", "cheap_to_run"}, "price=low", "Low buying cost combined with affordable maintenance gives a low overall price."),
    ({"buying=med", "maint=low"}, "price=low", "Medium buying cost combined with low maintenance gives a low overall price."),
    

    #MED
    ({"buying=med", "maint=med"}, "price=med", "Medium buying cost combined with medium maintenance gives a medium overall price."),
    ({"buying=low", "maint=high"}, "price=med", "Low buying cost combined with high maintenance gives a medium overall price."),

    #HIGH
    ({"buying=high", "maint=med"}, "price=high", "High buying cost combined with medium maintenance gives a high overall price."),
    ({"buying=high", "maint=high"}, "price=high", "High buying cost combined with high maintenance gives a high overall price."),
    ({"buying=med", "maint=vhigh"}, "price=high", "Medium buying cost combined with very high maintenance gives a high overall price."),
    ({"buying=low", "maint=vhigh"}, "price=high", "Low buying cost combined with very high maintenance gives a high overall price."),

    #VHIGH
    ({"buying=vhigh", "maint=vhigh"}, "price=vhigh", "Very high buying and maintenance costs make the car unaffordable."),
    ({"buying=vhigh", "maint=high"}, "price=vhigh", "Very high buying costs and high maintenance costs make the car unaffordable."),
    ({"buying=high", "maint=vhigh"}, "price=vhigh", "High buying costs and very high maintenance costs make the car unaffordable."),

    # UNACC
    ({"price=vhigh"}, "car=unacc", "A very high overall price makes the car unacceptable."),

    # FAMILY CAR
    ({"persons=4"}, "family_car", "A car with four seats can fit a family."),
    ({"persons=more"}, "family_car", "A car with more than four seats can fit a family."),

    #ROOMY
    ({"lug_boot=med", "doors=4"}, "roomy", "Medium luggage space and four doors is considered roomy."),
    ({"lug_boot=med", "doors=5more"}, "roomy", "Medium luggage space and five doors is considered roomy."),
    ({"lug_boot=big"}, "roomy", "Large luggage space is considered roomy."),

    # Reference: several car= answers can be true at once; engine.verdict picks one (conflict resolution, Session 3 slides 14-15).
    #ACCEPTABLE
    ({"family_car", "safety=med"}, "car=acc", "A family car with medium safety is acceptable."),
    ({"family_car", "safety=high"}, "car=acc", "A family car with high safety is acceptable."),

    #GOOD
    ({"price=low", "family_car", "safety=med", "lug_boot=med"}, "car=good", "An affordable family car with medium safety and medium luggage space is considered good."),
    ({"price=low", "family_car", "safety=med", "lug_boot=big"}, "car=good", "An affordable family car with medium safety and large luggage space is considered good."),
    ({"price=low", "family_car", "safety=high"}, "car=good", "An affordable family car with high safety is considered good."),

    #VGOOD
    ({"price=low", "family_car", "safety=high", "roomy"}, "car=vgood", "An affordable family car with high safety and a roomy interior is considered very good."),
    ({"price=med", "family_car", "safety=high", "roomy"}, "car=vgood", "A family car with medium overall price, high safety and a roomy interior is considered very good."),
]
    