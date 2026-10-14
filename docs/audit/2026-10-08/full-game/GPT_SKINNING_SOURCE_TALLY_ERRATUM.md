# Skinning arithmetic erratum — GT-S11 and GT-S18

**Confirmed correction:** replace **191 component occurrences / 108 consumed rows** in both GT-S11 and GT-S18 with **192 component occurrences / 109 consumed rows**. The correct breakdown is **83 nonconsumed tool rows + 109 consumed rows: 54 material, 35 solvent and 20 stabilizer; zero consumed-tool rows and zero catalysts**. Independent summation of the supplied 43 per-recipe counts gives 192/109/83, with every row satisfying total = consumed + nonconsumed.

This corrects the two tally statements and their corresponding validation expectations only. Preserve the original GT-S verdict as historical; change no ingredient occurrence, recipe register entry, body/effect mapping, price, source field or operational decision to fit the old tally. The mounted original Skinning verdict matches the supplied SHA-256 `a1fc285c49c91a3c9d977c988f7ff0266a481c633df0ae333429b1b26973c7e0` and is not overwritten by this erratum.

