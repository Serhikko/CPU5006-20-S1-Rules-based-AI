# from Claude Code: unit tests (plumbing). They check that Serhii's engine and knowledge base behave as designed.
# Run from the project folder:  .\.venv\Scripts\python.exe -m unittest discover -s tests -t .
import unittest
import pandas as pd
from data import COLUMNS, load, split
from knowledge import RULES
from engine import row_to_facts, forward_chain, verdict

GREAT_CAR = {"buying=low", "maint=low", "doors=4", "persons=4", "lug_boot=big", "safety=high"}


class TestFacts(unittest.TestCase):
    def test_row_becomes_six_facts(self):
        row = pd.Series({"buying": "low", "maint": "med", "doors": "2", "persons": "4",
                         "lug_boot": "small", "safety": "high", "class": "acc"})
        self.assertEqual(row_to_facts(row),
                         {"buying=low", "maint=med", "doors=2", "persons=4", "lug_boot=small", "safety=high"})


class TestForwardChaining(unittest.TestCase):
    def test_chains_through_helper_facts(self):
        facts, fired = forward_chain(GREAT_CAR, RULES)
        self.assertIn("car=vgood", facts)
        conclusions = [conclusion for conditions, conclusion, reason in fired]
        self.assertIn("price=low", conclusions)
        self.assertLess(conclusions.index("price=low"), conclusions.index("car=vgood"))

    def test_each_rule_fires_at_most_once(self):
        facts, fired = forward_chain(GREAT_CAR, RULES)
        conclusions = [conclusion for conditions, conclusion, reason in fired]
        self.assertEqual(len(conclusions), len(set(conclusions)))

    def test_a_conclusion_is_never_added_twice(self):
        # a two-seater with low safety matches both veto rules; car=unacc must appear once in fired
        facts, fired = forward_chain({"buying=low", "maint=low", "doors=4", "persons=2",
                                      "lug_boot=big", "safety=low"}, RULES)
        conclusions = [conclusion for conditions, conclusion, reason in fired]
        self.assertEqual(conclusions.count("car=unacc"), 1)

    def test_does_not_change_the_input_set(self):
        original = set(GREAT_CAR)
        forward_chain(original, RULES)
        self.assertEqual(original, GREAT_CAR)

    def test_nothing_fires_for_unknown_facts(self):
        facts, fired = forward_chain({"colour=red"}, RULES)
        self.assertEqual(fired, [])
        self.assertEqual(facts, {"colour=red"})

    def test_rule_order_does_not_matter(self):
        # forward chaining repeats until a full pass adds nothing, so the rules may come in any order:
        # with the list reversed, the car= rules are tried before their helper facts exist and must be retried
        facts_normal, fired_normal = forward_chain(GREAT_CAR, RULES)
        facts_reversed, fired_reversed = forward_chain(GREAT_CAR, list(reversed(RULES)))
        self.assertEqual(facts_reversed, facts_normal)
        self.assertEqual(len(fired_reversed), len(fired_normal))


class TestVerdict(unittest.TestCase):
    def test_great_car_is_vgood(self):
        facts, fired = forward_chain(GREAT_CAR, RULES)
        self.assertEqual(verdict(facts), "vgood")

    def test_two_seater_is_vetoed(self):
        facts, fired = forward_chain((GREAT_CAR - {"persons=4"}) | {"persons=2"}, RULES)
        self.assertEqual(verdict(facts), "unacc")

    def test_good_beats_acc_when_vgood_is_absent(self):
        # a cheap family car with safety=med concludes both car=acc and car=good; the better answer wins
        self.assertEqual(verdict({"car=acc", "car=good"}), "good")
        self.assertEqual(verdict({"car=acc", "car=vgood"}), "vgood")

    def test_veto_beats_a_positive_answer(self):
        # a safe family car that is far too expensive: car=acc fires, but price=vhigh vetoes it
        facts, fired = forward_chain({"buying=vhigh", "maint=vhigh", "doors=4", "persons=4",
                                      "lug_boot=big", "safety=high"}, RULES)
        self.assertIn("car=acc", facts)
        self.assertEqual(verdict(facts), "unacc")

    def test_default_is_the_majority_class(self):
        self.assertEqual(verdict(set()), "unacc")


class TestKnowledgeBase(unittest.TestCase):
    def test_every_condition_is_a_known_fact_or_a_conclusion(self):
        df = load()
        data_facts = {col + "=" + value for col in COLUMNS[:-1] for value in df[col].unique()}
        conclusions = {conclusion for conditions, conclusion, reason in RULES}
        for conditions, conclusion, reason in RULES:
            for fact in conditions:
                self.assertIn(fact, data_facts | conclusions, "misspelled condition: " + fact)

    def test_rules_have_the_right_shape(self):
        for rule in RULES:
            conditions, conclusion, reason = rule
            self.assertIsInstance(conditions, set)
            self.assertIsInstance(conclusion, str)
            self.assertTrue(reason.strip(), "empty reason in rule " + str(rule))


class TestSplit(unittest.TestCase):
    def test_train_and_test_do_not_overlap_and_keep_class_shares(self):
        df = load()
        train, test = split(df)
        self.assertEqual(len(train) + len(test), len(df))
        self.assertTrue(set(train.index).isdisjoint(test.index))
        for c in df["class"].unique():
            share_train = (train["class"] == c).mean()
            share_test = (test["class"] == c).mean()
            self.assertAlmostEqual(share_train, share_test, delta=0.01)


if __name__ == "__main__":
    unittest.main()
