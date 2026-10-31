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
- Shape (1728, 7). The first five rows are all `vhigh, vhigh, 2, 2, small` with safety low/med/high and class unacc: the file is sorted by attribute combination, not shuffled, so a train/test split must be random.
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

