# Lab log - CPU5006 S1, Car Evaluation

## 31 Oct 2026 - setup and first look

What I did:
- Made the project structure: `data/` with `car.data` and `car.names`, `.gitignore`, `requirements.txt`, `explore.py`, this log. First commit.
- Read `car.names`. The link in it (http://www-ai.ijs.si/BlazZupan/car.html) is dead, so the example tables behind the hierarchy are not available; the structure is explained in the file itself.
- Wrote `explore.py`: load the file with pandas, print the shape and the first five rows.
- The first run failed with `ModuleNotFoundError: No module named 'pandas'`. Cause: the VS Code Run button used the bare Python (`C:\Users\spryn\.local\bin\python3.14.exe`), which has no pandas. Fix (with help from Claude Code): created a virtual environment `.venv` with python3.14, installed pandas from `requirements.txt`, selected `.venv` as the interpreter in VS Code. The second run printed `(1728, 7)` and the first rows.

What the dataset's own description says (`car.names`; summary written with Claude Code):
- The data comes from an expert decision model (DEX, 1990) with a hierarchy: CAR (acceptability) <- PRICE (buying, maint) + TECH (COMFORT (doors, persons, lug_boot) + safety). Only the six bottom attributes are in the data; PRICE, TECH and COMFORT are hidden.
- 1,728 instances that "completely cover the attribute space": every combination of values appears exactly once.
- Six attributes: buying and maint: v-high, high, med, low; doors: 2, 3, 4, 5-more; persons: 2, 4, more; lug_boot: small, med, big; safety: low, med, high.
- No missing values.
- Class distribution: unacc 1210 (70.0%), acc 384 (22.2%), good 69 (4.0%), v-good 65 (3.8%).

What I found from my own run of `explore.py`:
- Shape (1728, 7). The first five rows are all `vhigh, vhigh, 2, 2` and unacc; only the last two columns change (small/low, small/med, small/high, med/low, med/med): the file is sorted by attribute combination, not shuffled, so a train/test split must be random.
- Class shares: unacc 0.700, acc 0.222, good 0.040, vgood 0.038 (value_counts, normalize=True). Matches car.names.
- Baseline (always predict the biggest class, unacc): 0.700. Every model must beat this.
- Missing values: 0 in every column. Duplicated rows: 0.
- Crosstab patterns, one line per attribute (veto = a value that is 100% unacc; evidence for good/vgood; attributes that barely matter):
  - buying: vhigh and high never give good or vgood (0.00); vhigh is 83% unacc. low gives the most good (0.11) and vgood (0.09). Price is strong evidence both ways.
  - maint: same shape as buying: vhigh never good/vgood and 83% unacc; low gives the most good (0.11). buying and maint together form the hidden PRICE concept.
  - doors: the rows barely differ (unacc 0.75 / 0.69 / 0.68 / 0.68); only 2 doors is slightly worse. On its own, doors matters little.
  - persons: 2 is 1.00 unacc -> VETO (a two-seater is never acceptable). 4 and more look the same as each other.
  - lug_boot: small never gives vgood (0.00) and is 78% unacc; big gives the most vgood (0.07). Weak alone, probably matters in combination (COMFORT).
  - safety: low is 1.00 unacc -> VETO. high gives the most vgood (0.11) and the least unacc (0.48). med never gives vgood (0.00): vgood needs high safety.

AI help used today: Claude Code explained what `explore.py` should contain, helped fix the Python environment, tidied this log, and we read the crosstabs together (the six pattern lines were written with it). All code typed by me.


## 31 Oct 2026 (evening) - split, knowledge base v1, engine started

What I did:
- `data.py`: loading plus a stratified 70/30 hold-out split with seed 42 (the snippet came from Claude Code; typed and commented by me). Train 1,209 rows, test 519; every class keeps its share in both halves (unacc 0.70, acc 0.22, good 0.04, vgood 0.04). Rule for the rest of the project: rules are designed on TRAIN only, TEST is measured once per version (no peeking).
- `explore.py`: made the crosstabs readable: whole-number percentages, classes ordered worst -> best, values low -> high (the two ordering lists are from Claude Code).
- Claude Code pointed me to the buying x maint combinations that are 100% unacc: (vhigh, vhigh), (vhigh, high), (high, vhigh). Together they are the hidden PRICE = very high.
- `knowledge.py` v1: 19 rules, each written as (set of conditions, conclusion, reason). Design: two veto rules (persons=2, safety=low) and a third veto through the concept price=vhigh; helper concepts cheap_to_buy / cheap_to_run -> price=low, and family_car; then car=acc (family car, safety med or high), car=good (cheap family car, safety med or high), car=vgood (cheap family car, high safety, boot med or big). OR is written as two rules with the same conclusion. Several car= answers can be true for one car; the engine decides: unacc always wins (veto), then vgood > good > acc; nothing concluded = unacc (the majority class). The plan for which rules to write was made in the chat with Claude Code; I typed the rules and wrote the reasons (the first two, the vetoes, started from Claude Code's example of the format).
- `engine.py`: started. Claude Code gave me a skeleton (imports, function names, docstrings and STEP comments); I write the code inside next (Sunday evening or Monday): row_to_facts, forward_chain (repeat until no new fact appears, each rule fires once, the list of fired rules is the explanation) and verdict.

AI help used (evening): this evening entry was drafted by Claude Code from our chat for me to check and edit. Claude Code reviewed knowledge.py by running my rules through its own test engine (all facts spelled right, every helper fact used), tidied the file header, and wrote the plumbing files `evaluate.py`, `explain.py`, `class_example.py` (the five rules from the Session 3 notebook, scored on my split) and `tests/test_engine.py` (each marked "from Claude Code" at the top). Later tonight it also made skeletons with STEP comments for `backward.py` and `oner.py` (I write the bodies), drafted a `README.md` with TODO markers for me to edit, and corrected one sentence of the morning entry above (the first-five-rows line). I will run the scripts once the engine is finished and put the real numbers in the table below.

## 2 Nov 2026 (Monday) and the night to 3 Nov - engine, v2, v3, final files

(This entry was drafted by Claude Code from our chat for me to check and edit in the morning.)

What I did:
- `engine.py`: wrote the three function bodies. My first version had no `while` loop: it went through the rules once, which happened to give the right answers for my v1 rule order, so the accuracy looked fine (0.892). Claude Code added a unit test that reverses the rule order; it failed, I saw why (a car= rule that needs a helper fact can come before the rule that produces that fact), and I added the loop that repeats until a full pass adds nothing. Two hand tests at the bottom: the great car (vgood) and the same car with two seats (unacc: the veto does not stop the other rules, the verdict makes it win); with the v1 rules they fired 7 and 4 rules, with v3 the roomy rule also fires, so engine.py now prints 8 and 5. v1 measured with `evaluate.py`: 19 rules, train 0.892, test 0.882, 130 training errors.
- Error analysis of v1 (train only): 62 unacc called acc; 48 acc called good (safety med, small boot, buying and maint mostly med); 8 vgood called acc (buying low, maint high).
- `knowledge.py` v2 (30 rules): instead of one price=low concept I wrote a price grid: LOW (low+low, low+med, med+low), MED (med+med, low+high), HIGH (high+med, high+high, med+vhigh, low+vhigh), VHIGH (the three 100%-unacc combinations). A `roomy` concept (big boot; med boot with 4 or 5more doors). `good` at medium safety now needs a boot of at least med; `vgood` needs `roomy` and is allowed at price=med. Slips on the way, all caught by `evaluate.py` or the tests: med+med was still counted as low; `lug_boot=med` alone was roomy; I typed `doors=5` and `doors=4e` (the spelling test caught both). Result: train 0.937, test 0.915.
- `knowledge.py` v3 (33 rules): the 65 remaining unacc-called-acc cars were mostly high-priced with a small boot at medium safety. Filled two holes in the grid (vhigh+low and vhigh+med -> price=high) and added one veto: price=high AND lug_boot=small AND safety=med -> car=unacc. Train 0.963, test 0.948. 45 training errors left, 34 of them unacc cars called acc, and 23 of those have two doors; a "cramped" concept would be the next version. Stopped here for time.
- Committed one file at a time through GitHub Desktop, after going through each file: data, explore, knowledge (v1, v2, v3 as separate commits), engine, evaluate, tests, explain, class_example.
- Decisions: slide references (`# Reference:` comments) only in the files whose code I wrote; the plumbing files written by Claude Code carry none. Dropped OneR (`oner.py` was still an empty skeleton): the exploration crosstabs already show that no single attribute beats the baseline, so the point is made without the file.

AI help used: Claude Code explained each file to me before I committed it and asked me check questions; measured my candidate rules on the training half while I typed them; inserted, then thinned, then removed from its own files the slide-reference comments, at my request; ran an independent review of the repository for honesty and consistency and fixed what it found in the README draft; filled the README numbers from my runs; regenerated and ran the walkthrough notebook. At about 04:00 on 3 Nov I was too tired to go on and asked it to finish the remaining pieces: it wrote `backward.py` in full (declared in the file header and in the README), committed that file and the finished notebook for me (the four small commits made after 03:50, which I go through in the morning), drafted this entry for me to check, and wrote me a morning pack with a video walkthrough and a report plan. The report I write myself in the morning.

## Knowledge base log

| version | rules | train accuracy | test accuracy | what changed |
|---|---|---|---|---|
| v1 | 19 | 0.892 | 0.882 | vetoes, price and family concepts, acc/good/vgood rules |
| v2 | 30 | 0.937 | 0.915 | price grid (low/med/high/vhigh) instead of one price=low concept; roomy concept; good at medium safety needs a boot of at least med; vgood also at price=med |
| v3 | 33 | 0.963 | 0.948 | grid completed for a very high buying price (vhigh+low, vhigh+med); price=high + small boot + medium safety -> unacc |
