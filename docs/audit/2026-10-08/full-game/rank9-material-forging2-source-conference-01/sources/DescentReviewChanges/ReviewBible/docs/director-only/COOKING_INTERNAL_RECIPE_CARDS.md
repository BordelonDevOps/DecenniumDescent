# Cooking Director internal recipe cards

**REVIEWED provisional authored operational PLAYTEST Cooking recipe set.** All 44 formulas: 30 public, two restricted, 12 Director-only. Keep this file internal.

Every card uses the shared Cooking procedure for consumption, feast replacement, nutrition, storage, quality and donor-trait eligibility. Source quantities are servings; prices are Standard batch references. Source names and legacy fields remain preserved and do not grant additional powers.

## recipe-81 — Refined Caustic Feast

**Source:** public; Cooking level 3; tier 2; Common; DC 11; 2 active hours; 3 serving(s). Standard batch reference 89 gp.

**Preserved effect:** After a 10-minute meal, gain 4 temporary hit points and resistance to acid damage for 1 hour. A creature can benefit from one feast at a time.

**Operational effect:** After completing and accepting this feast, offer 4 temporary HP. Gain resistance to acid damage for 1 elapsed hour(s), ending earlier with the parent feast.

**Duration:** Parent feast and its temporary HP end at the next completed beneficial Long Rest. Every rider also ends when this feast ends or is replaced. Its explicitly shorter deadline remains separate.

**Work:** Cookfire or Kitchen; Cook's utensils, Knife, Pot or pan. Mode field; field flag true; maximum assistants 0; formula required false.

**Exact ingredients:** 5 × Oil (component tier 2; 0.5 lb/unit; 8 gp/unit; solvent; consumed); 2 × Water (component tier 2; 0.5 lb/unit; 8 gp/unit; solvent; consumed); 1 × caustic goo (component tier 1; 0.99 lb/unit; 8 gp/unit; material; consumed).

**Food reservation:** 2.5 lb credited nutritive source inputs; up to 0 lb may return as the selected catalyst. For Standard quantity without catalyst retention, add 0 lb real ration-equivalent food. Before any completion check reserve 0.17 lb supplementary food for full Masterwork yield and worst legal nutritive catalyst retention. This is additional to every exact ingredient. Reservation does not consume food; after the outcome/catalyst choice and before finished servings are created, incorporate only the actual required amount. Generic failure without a finished product leaves all supplement unincorporated; a specific failed product spends only its required supplement. Actual food reference is 25 cp/lb, prorated from 5 sp per 2-lb daily ration; supplier quotes and transaction rounding still apply.

**Serving and storage:** each serving contains exactly 2/3 lb food and credits 1/3 Small/Medium daily food or 1/6 Large daily food after complete consumption. Before rolling, predeclare actual output dispositions for all 4 possible servings: real compatible storage capacity or distinct present recipients ready to begin immediate ten-minute consumption, one simultaneous slot per recipient. Immediate servings commit at batch completion; an invalid immediate slot needs actual reserved storage or cannot use the exception. Existing containers count only to their real capacity. A dedicated Meal Crock is 0.5 lb empty, 2 sp, 1 quart, AC 13/HP 2; one serving gives 7/6 lb gross. No water, fuel or full Supply is supplied by this food credit. Finished-food shelf life is 24 unprotected elapsed hours.

**Flawed:** {"mode": "half-batch-quantity", "quantity": 1}. Quality can change finite yield or dedicated mundane packaging durability; it does not improve meal potency. A dedicated Meal Crock first improved from maximum HP 2 to 3 gains exactly +1 current HP, preserving existing damage; an already-HP-3 crock gains neither again.

**Nutritional source map:** Oil counts as ordinary food; Water has no credited nutritive bulk in this card; caustic goo has no credited nutritive bulk in this card.

## recipe-82 — Refined Venom Feast

**Source:** public; Cooking level 4; tier 2; Common; DC 8; 4 active hours; 1 serving(s). Standard batch reference 102 gp.

**Preserved effect:** After a 10-minute meal, gain 4 temporary hit points and advantage on saves against poison for 4 hours. A creature can benefit from one feast at a time.

**Operational effect:** After completing and accepting this feast, offer 4 temporary HP. Gain advantage on saves against poison for 4 elapsed hours, ending earlier with the parent feast. No poison immunity, condition cure or damage resistance.

**Duration:** Parent feast and its temporary HP end at the next completed beneficial Long Rest. Every rider also ends when this feast ends or is replaced. Its explicitly shorter deadline remains separate.

**Work:** Cookfire or Kitchen; Cook's utensils, Knife, Pot or pan. Mode expedition; field flag true; maximum assistants 0; formula required false.

**Exact ingredients:** 1 × Water (component tier 2; 0.5 lb/unit; 8 gp/unit; solvent; consumed); 1 × Milk (component tier 2; 0.5 lb/unit; 8 gp/unit; substrate; consumed); 5 × Meat (component tier 2; 0.1 lb/unit; 8 gp/unit; substrate; consumed); 1 × Poisonous meat (component tier 1; 0.38 lb/unit; 14 gp/unit; catalyst; consumed).

**Food reservation:** 1.38 lb credited nutritive source inputs; up to 0.38 lb may return as the selected catalyst. For Standard quantity without catalyst retention, add 0 lb real ration-equivalent food. Before any completion check reserve 0 lb supplementary food for full Masterwork yield and worst legal nutritive catalyst retention. This is additional to every exact ingredient. Reservation does not consume food; after the outcome/catalyst choice and before finished servings are created, incorporate only the actual required amount. Generic failure without a finished product leaves all supplement unincorporated; a specific failed product spends only its required supplement. Actual food reference is 25 cp/lb, prorated from 5 sp per 2-lb daily ration; supplier quotes and transaction rounding still apply.

**Serving and storage:** each serving contains exactly 2/3 lb food and credits 1/3 Small/Medium daily food or 1/6 Large daily food after complete consumption. Before rolling, predeclare actual output dispositions for all 1 possible servings: real compatible storage capacity or distinct present recipients ready to begin immediate ten-minute consumption, one simultaneous slot per recipient. Immediate servings commit at batch completion; an invalid immediate slot needs actual reserved storage or cannot use the exception. Existing containers count only to their real capacity. A dedicated Meal Crock is 0.5 lb empty, 2 sp, 1 quart, AC 13/HP 2; one serving gives 7/6 lb gross. No water, fuel or full Supply is supplied by this food credit. Finished-food shelf life is 24 unprotected elapsed hours.

**Flawed:** {"mode": "treat-as-Failed", "quantity": 0, "materialRecoveryPercent": 25}. Quality can change finite yield or dedicated mundane packaging durability; it does not improve meal potency. A dedicated Meal Crock first improved from maximum HP 2 to 3 gains exactly +1 current HP, preserving existing damage; an already-HP-3 crock gains neither again.

**Nutritional source map:** Water has no credited nutritive bulk in this card; Milk counts as ordinary food; Meat counts as ordinary food; Poisonous meat counts as ordinary food.

## recipe-83 — Field Mighty Feast

**Source:** public; Cooking level 1; tier 1; Common; DC 8; 8 active hours; 3 serving(s). Standard batch reference 40 gp.

**Preserved effect:** After a 10-minute meal, gain 3 temporary hit points and +1 to Athletics checks. A creature can benefit from one feast at a time.

**Operational effect:** After completing and accepting this feast, offer 3 temporary HP. Gain +1 to actual Athletics checks until the parent feast ends.

**Duration:** Parent feast and its temporary HP end at the next completed beneficial Long Rest. Every rider also ends when this feast ends or is replaced. Its explicitly shorter deadline remains separate.

**Work:** Cookfire or Kitchen; Cook's utensils, Knife, Pot or pan. Mode expedition; field flag true; maximum assistants 0; formula required false.

**Exact ingredients:** 2 × Milk (component tier 1; 0.5 lb/unit; 2 gp/unit; substrate; consumed); 2 × Fruit (component tier 1; 0.1 lb/unit; 2 gp/unit; substrate; consumed); 1 × putrid marrow (component tier 2; 0.18 lb/unit; 19 gp/unit; material; consumed).

**Food reservation:** 1.2 lb credited nutritive source inputs; up to 0 lb may return as the selected catalyst. For Standard quantity without catalyst retention, add 0.8 lb real ration-equivalent food. Before any completion check reserve 1.47 lb supplementary food for full Masterwork yield and worst legal nutritive catalyst retention. This is additional to every exact ingredient. Reservation does not consume food; after the outcome/catalyst choice and before finished servings are created, incorporate only the actual required amount. Generic failure without a finished product leaves all supplement unincorporated; a specific failed product spends only its required supplement. Actual food reference is 25 cp/lb, prorated from 5 sp per 2-lb daily ration; supplier quotes and transaction rounding still apply.

**Serving and storage:** each serving contains exactly 2/3 lb food and credits 1/3 Small/Medium daily food or 1/6 Large daily food after complete consumption. Before rolling, predeclare actual output dispositions for all 4 possible servings: real compatible storage capacity or distinct present recipients ready to begin immediate ten-minute consumption, one simultaneous slot per recipient. Immediate servings commit at batch completion; an invalid immediate slot needs actual reserved storage or cannot use the exception. Existing containers count only to their real capacity. A dedicated Meal Crock is 0.5 lb empty, 2 sp, 1 quart, AC 13/HP 2; one serving gives 7/6 lb gross. No water, fuel or full Supply is supplied by this food credit. Finished-food shelf life is 24 unprotected elapsed hours.

**Flawed:** {"mode": "half-batch-quantity", "quantity": 1}. Quality can change finite yield or dedicated mundane packaging durability; it does not improve meal potency. A dedicated Meal Crock first improved from maximum HP 2 to 3 gains exactly +1 current HP, preserving existing damage; an already-HP-3 crock gains neither again.

**Nutritional source map:** Milk counts as ordinary food; Fruit counts as ordinary food; putrid marrow has no credited nutritive bulk in this card.

## recipe-84 — Superior Verdant Cake of Living Root

**Source:** public; Cooking level 5; tier 3; Common; DC 8; 2 active hours; 1 serving(s). Standard batch reference 392 gp.

**Preserved effect:** After a 10-minute meal, gain 5 temporary hit points and advantage on saves against poison and disease. A creature can benefit from one feast at a time.

**Operational effect:** After completing and accepting this feast, offer 5 temporary HP. Gain advantage on saves against poison and disease until the parent feast ends. No automatic condition cure or immunity.

**Duration:** Parent feast and its temporary HP end at the next completed beneficial Long Rest. Every rider also ends when this feast ends or is replaced. Its explicitly shorter deadline remains separate.

**Work:** Cookfire or Kitchen; Cook's utensils, Knife, Pot or pan. Mode field; field flag true; maximum assistants 0; formula required true.

**Exact ingredients:** 2 × Sugar (component tier 3; 0.1 lb/unit; 25 gp/unit; seasoning; consumed); 4 × Fruit (component tier 3; 0.1 lb/unit; 25 gp/unit; substrate; consumed); 5 × Salt (component tier 3; 0.1 lb/unit; 25 gp/unit; seasoning; consumed); 1 × living root (component tier 1; 0.29 lb/unit; 12 gp/unit; material; consumed).

**Food reservation:** 0.6 lb credited nutritive source inputs; up to 0 lb may return as the selected catalyst. For Standard quantity without catalyst retention, add 0.07 lb real ration-equivalent food. Before any completion check reserve 0.07 lb supplementary food for full Masterwork yield and worst legal nutritive catalyst retention. This is additional to every exact ingredient. Reservation does not consume food; after the outcome/catalyst choice and before finished servings are created, incorporate only the actual required amount. Generic failure without a finished product leaves all supplement unincorporated; a specific failed product spends only its required supplement. Actual food reference is 25 cp/lb, prorated from 5 sp per 2-lb daily ration; supplier quotes and transaction rounding still apply.

**Serving and storage:** each serving contains exactly 2/3 lb food and credits 1/3 Small/Medium daily food or 1/6 Large daily food after complete consumption. Before rolling, predeclare actual output dispositions for all 1 possible servings: real compatible storage capacity or distinct present recipients ready to begin immediate ten-minute consumption, one simultaneous slot per recipient. Immediate servings commit at batch completion; an invalid immediate slot needs actual reserved storage or cannot use the exception. Existing containers count only to their real capacity. A dedicated Meal Crock is 0.5 lb empty, 2 sp, 1 quart, AC 13/HP 2; one serving gives 7/6 lb gross. No water, fuel or full Supply is supplied by this food credit. Finished-food shelf life is 24 unprotected elapsed hours.

**Flawed:** {"mode": "treat-as-Failed", "quantity": 0, "materialRecoveryPercent": 25}. Quality can change finite yield or dedicated mundane packaging durability; it does not improve meal potency. A dedicated Meal Crock first improved from maximum HP 2 to 3 gains exactly +1 current HP, preserving existing damage; an already-HP-3 crock gains neither again.

**Nutritional source map:** Sugar counts as ordinary food; Fruit counts as ordinary food; Salt has no credited nutritive bulk in this card; living root has no credited nutritive bulk in this card.

## recipe-85 — Field Ember Snack

**Source:** public; Cooking level 2; tier 1; Common; DC 12; 4 active hours; 3 serving(s). Standard batch reference 31 gp.

**Preserved effect:** After a 10-minute meal, gain 3 temporary hit points and resistance to fire damage for 1 hour. A creature can benefit from one feast at a time.

**Operational effect:** After completing and accepting this feast, offer 3 temporary HP. Gain resistance to fire damage for 1 elapsed hour(s), ending earlier with the parent feast.

**Duration:** Parent feast and its temporary HP end at the next completed beneficial Long Rest. Every rider also ends when this feast ends or is replaced. Its explicitly shorter deadline remains separate.

**Work:** Cookfire or Kitchen; Cook's utensils, Knife, Pot or pan. Mode expedition; field flag true; maximum assistants 0; formula required false.

**Exact ingredients:** 4 × Water (component tier 1; 0.5 lb/unit; 2 gp/unit; solvent; consumed); 1 × Fire meat (component tier 1; 0.56 lb/unit; 12 gp/unit; material; consumed).

**Food reservation:** 0.56 lb credited nutritive source inputs; up to 0 lb may return as the selected catalyst. For Standard quantity without catalyst retention, add 1.44 lb real ration-equivalent food. Before any completion check reserve 2.11 lb supplementary food for full Masterwork yield and worst legal nutritive catalyst retention. This is additional to every exact ingredient. Reservation does not consume food; after the outcome/catalyst choice and before finished servings are created, incorporate only the actual required amount. Generic failure without a finished product leaves all supplement unincorporated; a specific failed product spends only its required supplement. Actual food reference is 25 cp/lb, prorated from 5 sp per 2-lb daily ration; supplier quotes and transaction rounding still apply.

**Serving and storage:** each serving contains exactly 2/3 lb food and credits 1/3 Small/Medium daily food or 1/6 Large daily food after complete consumption. Before rolling, predeclare actual output dispositions for all 4 possible servings: real compatible storage capacity or distinct present recipients ready to begin immediate ten-minute consumption, one simultaneous slot per recipient. Immediate servings commit at batch completion; an invalid immediate slot needs actual reserved storage or cannot use the exception. Existing containers count only to their real capacity. A dedicated Meal Crock is 0.5 lb empty, 2 sp, 1 quart, AC 13/HP 2; one serving gives 7/6 lb gross. No water, fuel or full Supply is supplied by this food credit. Finished-food shelf life is 24 unprotected elapsed hours.

**Flawed:** {"mode": "half-batch-quantity", "quantity": 1}. Quality can change finite yield or dedicated mundane packaging durability; it does not improve meal potency. A dedicated Meal Crock first improved from maximum HP 2 to 3 gains exactly +1 current HP, preserving existing damage; an already-HP-3 crock gains neither again.

**Nutritional source map:** Water has no credited nutritive bulk in this card; Fire meat counts as ordinary food.

## recipe-86 — Refined Ember Bread

**Source:** public; Cooking level 4; tier 2; Common; DC 8; 4 active hours; 1 serving(s). Standard batch reference 89 gp.

**Preserved effect:** After a 10-minute meal, gain 4 temporary hit points and resistance to fire damage for 1 hour. A creature can benefit from one feast at a time.

**Operational effect:** After completing and accepting this feast, offer 4 temporary HP. Gain resistance to fire damage for 1 elapsed hour(s), ending earlier with the parent feast.

**Duration:** Parent feast and its temporary HP end at the next completed beneficial Long Rest. Every rider also ends when this feast ends or is replaced. Its explicitly shorter deadline remains separate.

**Work:** Cookfire or Kitchen; Cook's utensils, Knife, Pot or pan. Mode expedition; field flag true; maximum assistants 0; formula required false.

**Exact ingredients:** 2 × Honey (component tier 2; 0.1 lb/unit; 8 gp/unit; seasoning; consumed); 4 × Fruit (component tier 2; 0.1 lb/unit; 8 gp/unit; substrate; consumed); 1 × Fire meat (component tier 1; 0.56 lb/unit; 12 gp/unit; material; consumed).

**Food reservation:** 1.16 lb credited nutritive source inputs; up to 0 lb may return as the selected catalyst. For Standard quantity without catalyst retention, add 0 lb real ration-equivalent food. Before any completion check reserve 0 lb supplementary food for full Masterwork yield and worst legal nutritive catalyst retention. This is additional to every exact ingredient. Reservation does not consume food; after the outcome/catalyst choice and before finished servings are created, incorporate only the actual required amount. Generic failure without a finished product leaves all supplement unincorporated; a specific failed product spends only its required supplement. Actual food reference is 25 cp/lb, prorated from 5 sp per 2-lb daily ration; supplier quotes and transaction rounding still apply.

**Serving and storage:** each serving contains exactly 2/3 lb food and credits 1/3 Small/Medium daily food or 1/6 Large daily food after complete consumption. Before rolling, predeclare actual output dispositions for all 1 possible servings: real compatible storage capacity or distinct present recipients ready to begin immediate ten-minute consumption, one simultaneous slot per recipient. Immediate servings commit at batch completion; an invalid immediate slot needs actual reserved storage or cannot use the exception. Existing containers count only to their real capacity. A dedicated Meal Crock is 0.5 lb empty, 2 sp, 1 quart, AC 13/HP 2; one serving gives 7/6 lb gross. No water, fuel or full Supply is supplied by this food credit. Finished-food shelf life is 24 unprotected elapsed hours.

**Flawed:** {"mode": "treat-as-Failed", "quantity": 0, "materialRecoveryPercent": 25}. Quality can change finite yield or dedicated mundane packaging durability; it does not improve meal potency. A dedicated Meal Crock first improved from maximum HP 2 to 3 gains exactly +1 current HP, preserving existing damage; an already-HP-3 crock gains neither again.

**Nutritional source map:** Honey counts as ordinary food; Fruit counts as ordinary food; Fire meat counts as ordinary food.

## recipe-87 — Field Storm Pie

**Source:** public; Cooking level 2; tier 1; Common; DC 8; 2 active hours; 3 serving(s). Standard batch reference 42 gp.

**Preserved effect:** After a 10-minute meal, gain 3 temporary hit points and resistance to lightning damage for 1 hour. A creature can benefit from one feast at a time.

**Operational effect:** After completing and accepting this feast, offer 3 temporary HP. Gain resistance to lightning damage for 1 elapsed hour(s), ending earlier with the parent feast.

**Duration:** Parent feast and its temporary HP end at the next completed beneficial Long Rest. Every rider also ends when this feast ends or is replaced. Its explicitly shorter deadline remains separate.

**Work:** Cookfire or Kitchen; Cook's utensils, Knife, Pot or pan. Mode field; field flag true; maximum assistants 0; formula required false.

**Exact ingredients:** 5 × Salt (component tier 1; 0.1 lb/unit; 2 gp/unit; seasoning; consumed); 5 × Water (component tier 1; 0.5 lb/unit; 2 gp/unit; solvent; consumed); 1 × sparkling petal (component tier 1; 0.36 lb/unit; 10 gp/unit; material; consumed).

**Food reservation:** 0 lb credited nutritive source inputs; up to 0 lb may return as the selected catalyst. For Standard quantity without catalyst retention, add 2 lb real ration-equivalent food. Before any completion check reserve 2.67 lb supplementary food for full Masterwork yield and worst legal nutritive catalyst retention. This is additional to every exact ingredient. Reservation does not consume food; after the outcome/catalyst choice and before finished servings are created, incorporate only the actual required amount. Generic failure without a finished product leaves all supplement unincorporated; a specific failed product spends only its required supplement. Actual food reference is 25 cp/lb, prorated from 5 sp per 2-lb daily ration; supplier quotes and transaction rounding still apply.

**Serving and storage:** each serving contains exactly 2/3 lb food and credits 1/3 Small/Medium daily food or 1/6 Large daily food after complete consumption. Before rolling, predeclare actual output dispositions for all 4 possible servings: real compatible storage capacity or distinct present recipients ready to begin immediate ten-minute consumption, one simultaneous slot per recipient. Immediate servings commit at batch completion; an invalid immediate slot needs actual reserved storage or cannot use the exception. Existing containers count only to their real capacity. A dedicated Meal Crock is 0.5 lb empty, 2 sp, 1 quart, AC 13/HP 2; one serving gives 7/6 lb gross. No water, fuel or full Supply is supplied by this food credit. Finished-food shelf life is 24 unprotected elapsed hours.

**Flawed:** {"mode": "half-batch-quantity", "quantity": 1}. Quality can change finite yield or dedicated mundane packaging durability; it does not improve meal potency. A dedicated Meal Crock first improved from maximum HP 2 to 3 gains exactly +1 current HP, preserving existing damage; an already-HP-3 crock gains neither again.

**Nutritional source map:** Salt has no credited nutritive bulk in this card; Water has no credited nutritive bulk in this card; sparkling petal has no credited nutritive bulk in this card.

## recipe-88 — Refined Resonant Feast

**Source:** public; Cooking level 3; tier 2; Common; DC 8; 1 active hours; 2 serving(s). Standard batch reference 105 gp.

**Preserved effect:** After a 10-minute meal, gain 4 temporary hit points and restore 1 Resonance Point(s). A creature can benefit from one feast at a time.

**Operational effect:** After completing and accepting this feast, offer 4 temporary HP. On accepting this completed feast, restore 1 expended RP, capped at the actual existing RP maximum. There is no new once-per-rest cap: another genuine paid serving requires its full consumption and accepted feast replacement. No pool creation, RC conversion, Dissonance/Refrain reset, partial-meal or replay recovery.

**Duration:** Parent feast and its temporary HP end at the next completed beneficial Long Rest. Every rider also ends when this feast ends or is replaced. Its explicitly shorter deadline remains separate.

**Work:** Cookfire or Kitchen; Cook's utensils, Knife, Pot or pan. Mode field; field flag true; maximum assistants 0; formula required false.

**Exact ingredients:** 4 × Salt (component tier 2; 0.1 lb/unit; 8 gp/unit; seasoning; consumed); 4 × Meat (component tier 2; 0.1 lb/unit; 8 gp/unit; substrate; consumed); 1 × eldritch ichor (component tier 1; 0.45 lb/unit; 13 gp/unit; catalyst; consumed).

**Food reservation:** 0.4 lb credited nutritive source inputs; up to 0 lb may return as the selected catalyst. For Standard quantity without catalyst retention, add 0.94 lb real ration-equivalent food. Before any completion check reserve 1.6 lb supplementary food for full Masterwork yield and worst legal nutritive catalyst retention. This is additional to every exact ingredient. Reservation does not consume food; after the outcome/catalyst choice and before finished servings are created, incorporate only the actual required amount. Generic failure without a finished product leaves all supplement unincorporated; a specific failed product spends only its required supplement. Actual food reference is 25 cp/lb, prorated from 5 sp per 2-lb daily ration; supplier quotes and transaction rounding still apply.

**Serving and storage:** each serving contains exactly 2/3 lb food and credits 1/3 Small/Medium daily food or 1/6 Large daily food after complete consumption. Before rolling, predeclare actual output dispositions for all 3 possible servings: real compatible storage capacity or distinct present recipients ready to begin immediate ten-minute consumption, one simultaneous slot per recipient. Immediate servings commit at batch completion; an invalid immediate slot needs actual reserved storage or cannot use the exception. Existing containers count only to their real capacity. A dedicated Meal Crock is 0.5 lb empty, 2 sp, 1 quart, AC 13/HP 2; one serving gives 7/6 lb gross. No water, fuel or full Supply is supplied by this food credit. Finished-food shelf life is 24 unprotected elapsed hours.

**Flawed:** {"mode": "half-batch-quantity", "quantity": 1}. Quality can change finite yield or dedicated mundane packaging durability; it does not improve meal potency. A dedicated Meal Crock first improved from maximum HP 2 to 3 gains exactly +1 current HP, preserving existing damage; an already-HP-3 crock gains neither again.

**Nutritional source map:** Salt has no credited nutritive bulk in this card; Meat counts as ordinary food; eldritch ichor has no credited nutritive bulk in this card.

## recipe-89 — Field Gale Meal

**Source:** public; Cooking level 1; tier 1; Common; DC 8; 4 active hours; 2 serving(s). Standard batch reference 30 gp.

**Preserved effect:** After a 10-minute meal, gain 3 temporary hit points and +10 feet movement speed for 1 hour. A creature can benefit from one feast at a time.

**Operational effect:** After completing and accepting this feast, offer 3 temporary HP. Increase walking speed by 10 feet for 1 elapsed hour or until the parent feast ends, whichever comes first. Other movement modes change only if their own rule derives them from walking speed.

**Duration:** Parent feast and its temporary HP end at the next completed beneficial Long Rest. Every rider also ends when this feast ends or is replaced. Its explicitly shorter deadline remains separate.

**Work:** Cookfire or Kitchen; Cook's utensils, Knife, Pot or pan. Mode expedition; field flag true; maximum assistants 0; formula required false.

**Exact ingredients:** 5 × Water (component tier 1; 0.5 lb/unit; 2 gp/unit; solvent; consumed); 1 × Quetzalcoatlus meat (component tier 1; 0.97 lb/unit; 11 gp/unit; material; consumed).

**Food reservation:** 0.97 lb credited nutritive source inputs; up to 0 lb may return as the selected catalyst. For Standard quantity without catalyst retention, add 0.37 lb real ration-equivalent food. Before any completion check reserve 1.03 lb supplementary food for full Masterwork yield and worst legal nutritive catalyst retention. This is additional to every exact ingredient. Reservation does not consume food; after the outcome/catalyst choice and before finished servings are created, incorporate only the actual required amount. Generic failure without a finished product leaves all supplement unincorporated; a specific failed product spends only its required supplement. Actual food reference is 25 cp/lb, prorated from 5 sp per 2-lb daily ration; supplier quotes and transaction rounding still apply.

**Serving and storage:** each serving contains exactly 2/3 lb food and credits 1/3 Small/Medium daily food or 1/6 Large daily food after complete consumption. Before rolling, predeclare actual output dispositions for all 3 possible servings: real compatible storage capacity or distinct present recipients ready to begin immediate ten-minute consumption, one simultaneous slot per recipient. Immediate servings commit at batch completion; an invalid immediate slot needs actual reserved storage or cannot use the exception. Existing containers count only to their real capacity. A dedicated Meal Crock is 0.5 lb empty, 2 sp, 1 quart, AC 13/HP 2; one serving gives 7/6 lb gross. No water, fuel or full Supply is supplied by this food credit. Finished-food shelf life is 24 unprotected elapsed hours.

**Flawed:** {"mode": "half-batch-quantity", "quantity": 1}. Quality can change finite yield or dedicated mundane packaging durability; it does not improve meal potency. A dedicated Meal Crock first improved from maximum HP 2 to 3 gains exactly +1 current HP, preserving existing damage; an already-HP-3 crock gains neither again.

**Nutritional source map:** Water has no credited nutritive bulk in this card; Quetzalcoatlus meat counts as ordinary food.

## recipe-90 — Field Vital Soup

**Source:** public; Cooking level 1; tier 1; Common; DC 11; 4 active hours; 3 serving(s). Standard batch reference 29 gp.

**Preserved effect:** After a 10-minute meal, gain 3 temporary hit points and +1 to Constitution saves. A creature can benefit from one feast at a time.

**Operational effect:** After completing and accepting this feast, offer 3 temporary HP. Gain +1 to actual Constitution saving throws until the parent feast ends, including concentration and Wound/Injury saves when they are CON saves. Other roll types are not converted.

**Duration:** Parent feast and its temporary HP end at the next completed beneficial Long Rest. Every rider also ends when this feast ends or is replaced. Its explicitly shorter deadline remains separate.

**Work:** Cookfire or Kitchen; Cook's utensils, Knife, Pot or pan. Mode expedition; field flag true; maximum assistants 0; formula required false.

**Exact ingredients:** 4 × Vegetables (component tier 1; 0.1 lb/unit; 2 gp/unit; substrate; consumed); 1 × living root (component tier 1; 0.29 lb/unit; 12 gp/unit; material; consumed).

**Food reservation:** 0.4 lb credited nutritive source inputs; up to 0 lb may return as the selected catalyst. For Standard quantity without catalyst retention, add 1.6 lb real ration-equivalent food. Before any completion check reserve 2.27 lb supplementary food for full Masterwork yield and worst legal nutritive catalyst retention. This is additional to every exact ingredient. Reservation does not consume food; after the outcome/catalyst choice and before finished servings are created, incorporate only the actual required amount. Generic failure without a finished product leaves all supplement unincorporated; a specific failed product spends only its required supplement. Actual food reference is 25 cp/lb, prorated from 5 sp per 2-lb daily ration; supplier quotes and transaction rounding still apply.

**Serving and storage:** each serving contains exactly 2/3 lb food and credits 1/3 Small/Medium daily food or 1/6 Large daily food after complete consumption. Before rolling, predeclare actual output dispositions for all 4 possible servings: real compatible storage capacity or distinct present recipients ready to begin immediate ten-minute consumption, one simultaneous slot per recipient. Immediate servings commit at batch completion; an invalid immediate slot needs actual reserved storage or cannot use the exception. Existing containers count only to their real capacity. A dedicated Meal Crock is 0.5 lb empty, 2 sp, 1 quart, AC 13/HP 2; one serving gives 7/6 lb gross. No water, fuel or full Supply is supplied by this food credit. Finished-food shelf life is 24 unprotected elapsed hours.

**Flawed:** {"mode": "half-batch-quantity", "quantity": 1}. Quality can change finite yield or dedicated mundane packaging durability; it does not improve meal potency. A dedicated Meal Crock first improved from maximum HP 2 to 3 gains exactly +1 current HP, preserving existing damage; an already-HP-3 crock gains neither again.

**Nutritional source map:** Vegetables counts as ordinary food; living root has no credited nutritive bulk in this card.

## recipe-91 — Superior Gale Meal of Vulture Meat

**Source:** public; Cooking level 5; tier 3; Common; DC 11; 1 active hours; 1 serving(s). Standard batch reference 123 gp.

**Preserved effect:** After a 10-minute meal, gain 5 temporary hit points and +10 feet movement speed for 1 hour. A creature can benefit from one feast at a time.

**Operational effect:** After completing and accepting this feast, offer 5 temporary HP. Increase walking speed by 10 feet for 1 elapsed hour or until the parent feast ends, whichever comes first. Other movement modes change only if their own rule derives them from walking speed.

**Duration:** Parent feast and its temporary HP end at the next completed beneficial Long Rest. Every rider also ends when this feast ends or is replaced. Its explicitly shorter deadline remains separate.

**Work:** Cookfire or Kitchen; Cook's utensils, Knife, Pot or pan. Mode field; field flag true; maximum assistants 0; formula required true.

**Exact ingredients:** 1 × Salt (component tier 3; 0.1 lb/unit; 25 gp/unit; seasoning; consumed); 2 × Herbs (component tier 3; 0.1 lb/unit; 25 gp/unit; substrate; consumed); 1 × Vulture meat (component tier 1; 0.42 lb/unit; 14 gp/unit; material; consumed).

**Food reservation:** 0.42 lb credited nutritive source inputs; up to 0 lb may return as the selected catalyst. For Standard quantity without catalyst retention, add 0.25 lb real ration-equivalent food. Before any completion check reserve 0.25 lb supplementary food for full Masterwork yield and worst legal nutritive catalyst retention. This is additional to every exact ingredient. Reservation does not consume food; after the outcome/catalyst choice and before finished servings are created, incorporate only the actual required amount. Generic failure without a finished product leaves all supplement unincorporated; a specific failed product spends only its required supplement. Actual food reference is 25 cp/lb, prorated from 5 sp per 2-lb daily ration; supplier quotes and transaction rounding still apply.

**Serving and storage:** each serving contains exactly 2/3 lb food and credits 1/3 Small/Medium daily food or 1/6 Large daily food after complete consumption. Before rolling, predeclare actual output dispositions for all 1 possible servings: real compatible storage capacity or distinct present recipients ready to begin immediate ten-minute consumption, one simultaneous slot per recipient. Immediate servings commit at batch completion; an invalid immediate slot needs actual reserved storage or cannot use the exception. Existing containers count only to their real capacity. A dedicated Meal Crock is 0.5 lb empty, 2 sp, 1 quart, AC 13/HP 2; one serving gives 7/6 lb gross. No water, fuel or full Supply is supplied by this food credit. Finished-food shelf life is 24 unprotected elapsed hours.

**Flawed:** {"mode": "treat-as-Failed", "quantity": 0, "materialRecoveryPercent": 25}. Quality can change finite yield or dedicated mundane packaging durability; it does not improve meal potency. A dedicated Meal Crock first improved from maximum HP 2 to 3 gains exactly +1 current HP, preserving existing damage; an already-HP-3 crock gains neither again.

**Nutritional source map:** Salt has no credited nutritive bulk in this card; Herbs has no credited nutritive bulk in this card; Vulture meat counts as ordinary food.

## recipe-92 — Refined Storm Roast

**Source:** public; Cooking level 3; tier 2; Common; DC 11; 1 active hours; 5 serving(s). Standard batch reference 69 gp.

**Preserved effect:** After a 10-minute meal, gain 4 temporary hit points and resistance to lightning damage for 1 hour. A creature can benefit from one feast at a time.

**Operational effect:** After completing and accepting this feast, offer 4 temporary HP. Gain resistance to lightning damage for 1 elapsed hour(s), ending earlier with the parent feast.

**Duration:** Parent feast and its temporary HP end at the next completed beneficial Long Rest. Every rider also ends when this feast ends or is replaced. Its explicitly shorter deadline remains separate.

**Work:** Cookfire or Kitchen; Cook's utensils, Knife, Pot or pan. Mode field; field flag true; maximum assistants 0; formula required false.

**Exact ingredients:** 2 × Butter (component tier 2; 0.1 lb/unit; 8 gp/unit; seasoning; consumed); 1 × Water (component tier 2; 0.5 lb/unit; 8 gp/unit; solvent; consumed); 2 × Vegetables (component tier 2; 0.1 lb/unit; 8 gp/unit; substrate; consumed); 1 × sparkling petal (component tier 1; 0.36 lb/unit; 10 gp/unit; material; consumed).

**Food reservation:** 0.4 lb credited nutritive source inputs; up to 0 lb may return as the selected catalyst. For Standard quantity without catalyst retention, add 2.94 lb real ration-equivalent food. Before any completion check reserve 4.27 lb supplementary food for full Masterwork yield and worst legal nutritive catalyst retention. This is additional to every exact ingredient. Reservation does not consume food; after the outcome/catalyst choice and before finished servings are created, incorporate only the actual required amount. Generic failure without a finished product leaves all supplement unincorporated; a specific failed product spends only its required supplement. Actual food reference is 25 cp/lb, prorated from 5 sp per 2-lb daily ration; supplier quotes and transaction rounding still apply.

**Serving and storage:** each serving contains exactly 2/3 lb food and credits 1/3 Small/Medium daily food or 1/6 Large daily food after complete consumption. Before rolling, predeclare actual output dispositions for all 7 possible servings: real compatible storage capacity or distinct present recipients ready to begin immediate ten-minute consumption, one simultaneous slot per recipient. Immediate servings commit at batch completion; an invalid immediate slot needs actual reserved storage or cannot use the exception. Existing containers count only to their real capacity. A dedicated Meal Crock is 0.5 lb empty, 2 sp, 1 quart, AC 13/HP 2; one serving gives 7/6 lb gross. No water, fuel or full Supply is supplied by this food credit. Finished-food shelf life is 24 unprotected elapsed hours.

**Flawed:** {"mode": "half-batch-quantity", "quantity": 2}. Quality can change finite yield or dedicated mundane packaging durability; it does not improve meal potency. A dedicated Meal Crock first improved from maximum HP 2 to 3 gains exactly +1 current HP, preserving existing damage; an already-HP-3 crock gains neither again.

**Nutritional source map:** Butter counts as ordinary food; Water has no credited nutritive bulk in this card; Vegetables counts as ordinary food; sparkling petal has no credited nutritive bulk in this card.

## recipe-93 — Field Ember Feast

**Source:** public; Cooking level 2; tier 1; Common; DC 10; 4 active hours; 3 serving(s). Standard batch reference 28 gp.

**Preserved effect:** After a 10-minute meal, gain 3 temporary hit points and resistance to fire damage for 1 hour. A creature can benefit from one feast at a time.

**Operational effect:** After completing and accepting this feast, offer 3 temporary HP. Gain resistance to fire damage for 1 elapsed hour(s), ending earlier with the parent feast.

**Duration:** Parent feast and its temporary HP end at the next completed beneficial Long Rest. Every rider also ends when this feast ends or is replaced. Its explicitly shorter deadline remains separate.

**Work:** Cookfire or Kitchen; Cook's utensils, Knife, Pot or pan. Mode expedition; field flag true; maximum assistants 0; formula required false.

**Exact ingredients:** 3 × Fruit (component tier 1; 0.1 lb/unit; 2 gp/unit; substrate; consumed); 1 × Fire meat (component tier 1; 0.56 lb/unit; 12 gp/unit; material; consumed).

**Food reservation:** 0.86 lb credited nutritive source inputs; up to 0 lb may return as the selected catalyst. For Standard quantity without catalyst retention, add 1.14 lb real ration-equivalent food. Before any completion check reserve 1.81 lb supplementary food for full Masterwork yield and worst legal nutritive catalyst retention. This is additional to every exact ingredient. Reservation does not consume food; after the outcome/catalyst choice and before finished servings are created, incorporate only the actual required amount. Generic failure without a finished product leaves all supplement unincorporated; a specific failed product spends only its required supplement. Actual food reference is 25 cp/lb, prorated from 5 sp per 2-lb daily ration; supplier quotes and transaction rounding still apply.

**Serving and storage:** each serving contains exactly 2/3 lb food and credits 1/3 Small/Medium daily food or 1/6 Large daily food after complete consumption. Before rolling, predeclare actual output dispositions for all 4 possible servings: real compatible storage capacity or distinct present recipients ready to begin immediate ten-minute consumption, one simultaneous slot per recipient. Immediate servings commit at batch completion; an invalid immediate slot needs actual reserved storage or cannot use the exception. Existing containers count only to their real capacity. A dedicated Meal Crock is 0.5 lb empty, 2 sp, 1 quart, AC 13/HP 2; one serving gives 7/6 lb gross. No water, fuel or full Supply is supplied by this food credit. Finished-food shelf life is 24 unprotected elapsed hours.

**Flawed:** {"mode": "half-batch-quantity", "quantity": 1}. Quality can change finite yield or dedicated mundane packaging durability; it does not improve meal potency. A dedicated Meal Crock first improved from maximum HP 2 to 3 gains exactly +1 current HP, preserving existing damage; an already-HP-3 crock gains neither again.

**Nutritional source map:** Fruit counts as ordinary food; Fire meat counts as ordinary food.

## recipe-94 — Refined Mighty Soup

**Source:** public; Cooking level 4; tier 2; Common; DC 11; 1 active hours; 3 serving(s). Standard batch reference 49 gp.

**Preserved effect:** After a 10-minute meal, gain 4 temporary hit points and +1 to Athletics checks. A creature can benefit from one feast at a time.

**Operational effect:** After completing and accepting this feast, offer 4 temporary HP. Gain +1 to actual Athletics checks until the parent feast ends.

**Duration:** Parent feast and its temporary HP end at the next completed beneficial Long Rest. Every rider also ends when this feast ends or is replaced. Its explicitly shorter deadline remains separate.

**Work:** Cookfire or Kitchen; Cook's utensils, Knife, Pot or pan. Mode field; field flag true; maximum assistants 0; formula required false.

**Exact ingredients:** 2 × Spices (component tier 2; 0.1 lb/unit; 8 gp/unit; seasoning; consumed); 1 × putrid marrow (component tier 2; 0.18 lb/unit; 19 gp/unit; material; consumed).

**Food reservation:** 0 lb credited nutritive source inputs; up to 0 lb may return as the selected catalyst. For Standard quantity without catalyst retention, add 2 lb real ration-equivalent food. Before any completion check reserve 2.67 lb supplementary food for full Masterwork yield and worst legal nutritive catalyst retention. This is additional to every exact ingredient. Reservation does not consume food; after the outcome/catalyst choice and before finished servings are created, incorporate only the actual required amount. Generic failure without a finished product leaves all supplement unincorporated; a specific failed product spends only its required supplement. Actual food reference is 25 cp/lb, prorated from 5 sp per 2-lb daily ration; supplier quotes and transaction rounding still apply.

**Serving and storage:** each serving contains exactly 2/3 lb food and credits 1/3 Small/Medium daily food or 1/6 Large daily food after complete consumption. Before rolling, predeclare actual output dispositions for all 4 possible servings: real compatible storage capacity or distinct present recipients ready to begin immediate ten-minute consumption, one simultaneous slot per recipient. Immediate servings commit at batch completion; an invalid immediate slot needs actual reserved storage or cannot use the exception. Existing containers count only to their real capacity. A dedicated Meal Crock is 0.5 lb empty, 2 sp, 1 quart, AC 13/HP 2; one serving gives 7/6 lb gross. No water, fuel or full Supply is supplied by this food credit. Finished-food shelf life is 24 unprotected elapsed hours.

**Flawed:** {"mode": "half-batch-quantity", "quantity": 1}. Quality can change finite yield or dedicated mundane packaging durability; it does not improve meal potency. A dedicated Meal Crock first improved from maximum HP 2 to 3 gains exactly +1 current HP, preserving existing damage; an already-HP-3 crock gains neither again.

**Nutritional source map:** Spices has no credited nutritive bulk in this card; putrid marrow has no credited nutritive bulk in this card.

## recipe-95 — Field Mindward Feast

**Source:** public; Cooking level 1; tier 1; Common; DC 9; 2 active hours; 1 serving(s). Standard batch reference 43 gp.

**Preserved effect:** After a 10-minute meal, gain 3 temporary hit points and advantage on the first save against charm or fear. A creature can benefit from one feast at a time.

**Operational effect:** After completing and accepting this feast, offer 3 temporary HP. Before the parent feast ends, gain advantage on the first actual save against charm or fear. That save spends this one rider even if another source already grants advantage. No save required means no use spent; no cure or immunity.

**Duration:** Parent feast and its temporary HP end at the next completed beneficial Long Rest. Every rider also ends when this feast ends or is replaced. Its explicitly shorter deadline remains separate.

**Work:** Cookfire or Kitchen; Cook's utensils, Knife, Pot or pan. Mode field; field flag true; maximum assistants 0; formula required false.

**Exact ingredients:** 4 × Vegetables (component tier 1; 0.1 lb/unit; 2 gp/unit; substrate; consumed); 5 × Flour (component tier 1; 0.1 lb/unit; 2 gp/unit; substrate; consumed); 1 × eldritch ichor (component tier 1; 0.45 lb/unit; 13 gp/unit; catalyst; consumed).

**Food reservation:** 0.9 lb credited nutritive source inputs; up to 0 lb may return as the selected catalyst. For Standard quantity without catalyst retention, add 0 lb real ration-equivalent food. Before any completion check reserve 0 lb supplementary food for full Masterwork yield and worst legal nutritive catalyst retention. This is additional to every exact ingredient. Reservation does not consume food; after the outcome/catalyst choice and before finished servings are created, incorporate only the actual required amount. Generic failure without a finished product leaves all supplement unincorporated; a specific failed product spends only its required supplement. Actual food reference is 25 cp/lb, prorated from 5 sp per 2-lb daily ration; supplier quotes and transaction rounding still apply.

**Serving and storage:** each serving contains exactly 2/3 lb food and credits 1/3 Small/Medium daily food or 1/6 Large daily food after complete consumption. Before rolling, predeclare actual output dispositions for all 1 possible servings: real compatible storage capacity or distinct present recipients ready to begin immediate ten-minute consumption, one simultaneous slot per recipient. Immediate servings commit at batch completion; an invalid immediate slot needs actual reserved storage or cannot use the exception. Existing containers count only to their real capacity. A dedicated Meal Crock is 0.5 lb empty, 2 sp, 1 quart, AC 13/HP 2; one serving gives 7/6 lb gross. No water, fuel or full Supply is supplied by this food credit. Finished-food shelf life is 24 unprotected elapsed hours.

**Flawed:** {"mode": "treat-as-Failed", "quantity": 0, "materialRecoveryPercent": 25}. Quality can change finite yield or dedicated mundane packaging durability; it does not improve meal potency. A dedicated Meal Crock first improved from maximum HP 2 to 3 gains exactly +1 current HP, preserving existing damage; an already-HP-3 crock gains neither again.

**Nutritional source map:** Vegetables counts as ordinary food; Flour counts as ordinary food; eldritch ichor has no credited nutritive bulk in this card.

## recipe-96 — Masterwork Verdant Meal of Glimmering Leaf

**Source:** public; Cooking level 7; tier 4; Uncommon; DC 16; 8 active hours; 1 serving(s). Standard batch reference 565 gp.

**Preserved effect:** After a 10-minute meal, gain 8 temporary hit points and advantage on saves against poison and disease. A creature can benefit from one feast at a time.

**Operational effect:** After completing and accepting this feast, offer 8 temporary HP. Gain advantage on saves against poison and disease until the parent feast ends. No automatic condition cure or immunity.

**Duration:** Parent feast and its temporary HP end at the next completed beneficial Long Rest. Every rider also ends when this feast ends or is replaced. Its explicitly shorter deadline remains separate.

**Work:** Cookfire or Kitchen; Cook's utensils, Knife, Pot or pan. Mode expedition; field flag true; maximum assistants 0; formula required true.

**Exact ingredients:** 1 × Milk (component tier 4; 0.5 lb/unit; 75 gp/unit; substrate; consumed); 3 × Vegetables (component tier 4; 0.1 lb/unit; 75 gp/unit; substrate; consumed); 1 × Herbs (component tier 4; 0.1 lb/unit; 75 gp/unit; substrate; consumed); 1 × glimmering leaf (component tier 2; 0.75 lb/unit; 23 gp/unit; material; consumed).

**Food reservation:** 0.8 lb credited nutritive source inputs; up to 0 lb may return as the selected catalyst. For Standard quantity without catalyst retention, add 0 lb real ration-equivalent food. Before any completion check reserve 0 lb supplementary food for full Masterwork yield and worst legal nutritive catalyst retention. This is additional to every exact ingredient. Reservation does not consume food; after the outcome/catalyst choice and before finished servings are created, incorporate only the actual required amount. Generic failure without a finished product leaves all supplement unincorporated; a specific failed product spends only its required supplement. Actual food reference is 25 cp/lb, prorated from 5 sp per 2-lb daily ration; supplier quotes and transaction rounding still apply.

**Serving and storage:** each serving contains exactly 2/3 lb food and credits 1/3 Small/Medium daily food or 1/6 Large daily food after complete consumption. Before rolling, predeclare actual output dispositions for all 1 possible servings: real compatible storage capacity or distinct present recipients ready to begin immediate ten-minute consumption, one simultaneous slot per recipient. Immediate servings commit at batch completion; an invalid immediate slot needs actual reserved storage or cannot use the exception. Existing containers count only to their real capacity. A dedicated Meal Crock is 0.5 lb empty, 2 sp, 1 quart, AC 13/HP 2; one serving gives 7/6 lb gross. No water, fuel or full Supply is supplied by this food credit. Finished-food shelf life is 24 unprotected elapsed hours.

**Flawed:** {"mode": "treat-as-Failed", "quantity": 0, "materialRecoveryPercent": 25}. Quality can change finite yield or dedicated mundane packaging durability; it does not improve meal potency. A dedicated Meal Crock first improved from maximum HP 2 to 3 gains exactly +1 current HP, preserving existing damage; an already-HP-3 crock gains neither again.

**Nutritional source map:** Milk counts as ordinary food; Vegetables counts as ordinary food; Herbs has no credited nutritive bulk in this card; glimmering leaf has no credited nutritive bulk in this card.

## recipe-97 — Masterwork Verdant Stew of Dream Bark

**Source:** public; Cooking level 8; tier 4; Uncommon; DC 16; 24 active hours; 1 serving(s). Standard batch reference 1150 gp.

**Preserved effect:** After a 10-minute meal, gain 8 temporary hit points and advantage on saves against poison and disease. A creature can benefit from one feast at a time.

**Operational effect:** After completing and accepting this feast, offer 8 temporary HP. Gain advantage on saves against poison and disease until the parent feast ends. No automatic condition cure or immunity.

**Duration:** Parent feast and its temporary HP end at the next completed beneficial Long Rest. Every rider also ends when this feast ends or is replaced. Its explicitly shorter deadline remains separate.

**Work:** Cookfire or Kitchen; Cook's utensils, Knife, Pot or pan. Mode workshop; field flag false; maximum assistants 0; formula required true.

**Exact ingredients:** 1 × Herbs (component tier 4; 0.1 lb/unit; 75 gp/unit; substrate; consumed); 1 × Meat (component tier 4; 0.1 lb/unit; 75 gp/unit; substrate; consumed); 4 × Sugar (component tier 4; 0.1 lb/unit; 75 gp/unit; seasoning; consumed); 4 × Milk (component tier 4; 0.5 lb/unit; 75 gp/unit; substrate; consumed); 1 × dream bark (component tier 2; 0.45 lb/unit; 31 gp/unit; material; consumed).

**Food reservation:** 2.5 lb credited nutritive source inputs; up to 0 lb may return as the selected catalyst. For Standard quantity without catalyst retention, add 0 lb real ration-equivalent food. Before any completion check reserve 0 lb supplementary food for full Masterwork yield and worst legal nutritive catalyst retention. This is additional to every exact ingredient. Reservation does not consume food; after the outcome/catalyst choice and before finished servings are created, incorporate only the actual required amount. Generic failure without a finished product leaves all supplement unincorporated; a specific failed product spends only its required supplement. Actual food reference is 25 cp/lb, prorated from 5 sp per 2-lb daily ration; supplier quotes and transaction rounding still apply.

**Serving and storage:** each serving contains exactly 2/3 lb food and credits 1/3 Small/Medium daily food or 1/6 Large daily food after complete consumption. Before rolling, predeclare actual output dispositions for all 1 possible servings: real compatible storage capacity or distinct present recipients ready to begin immediate ten-minute consumption, one simultaneous slot per recipient. Immediate servings commit at batch completion; an invalid immediate slot needs actual reserved storage or cannot use the exception. Existing containers count only to their real capacity. A dedicated Meal Crock is 0.5 lb empty, 2 sp, 1 quart, AC 13/HP 2; one serving gives 7/6 lb gross. No water, fuel or full Supply is supplied by this food credit. Finished-food shelf life is 24 unprotected elapsed hours.

**Flawed:** {"mode": "treat-as-Failed", "quantity": 0, "materialRecoveryPercent": 25}. Quality can change finite yield or dedicated mundane packaging durability; it does not improve meal potency. A dedicated Meal Crock first improved from maximum HP 2 to 3 gains exactly +1 current HP, preserving existing damage; an already-HP-3 crock gains neither again.

**Nutritional source map:** Herbs has no credited nutritive bulk in this card; Meat counts as ordinary food; Sugar counts as ordinary food; Milk counts as ordinary food; dream bark has no credited nutritive bulk in this card.

## recipe-98 — Exalted Stone Meal of Gore Organ

**Source:** public; Cooking level 9; tier 5; Uncommon; DC 15; 24 active hours; 1 serving(s). Standard batch reference 3475 gp.

**Preserved effect:** After a 10-minute meal, gain 9 temporary hit points and advantage against being knocked prone for 1 hour. A creature can benefit from one feast at a time.

**Operational effect:** After completing and accepting this feast, offer 9 temporary HP. For 1 elapsed hour or until the parent feast ends, whichever comes first, gain advantage on an actual check or save whose direct consequence includes becoming Prone. No immunity to automatic Prone effects or benefit when standing.

**Duration:** Parent feast and its temporary HP end at the next completed beneficial Long Rest. Every rider also ends when this feast ends or is replaced. Its explicitly shorter deadline remains separate.

**Work:** Cookfire or Kitchen; Cook's utensils, Knife, Pot or pan. Mode workshop; field flag false; maximum assistants 0; formula required true.

**Exact ingredients:** 5 × Butter (component tier 5; 0.1 lb/unit; 200 gp/unit; seasoning; consumed); 5 × Oil (component tier 5; 0.5 lb/unit; 200 gp/unit; solvent; consumed); 1 × Meat (component tier 5; 0.1 lb/unit; 200 gp/unit; substrate; consumed); 1 × Honey (component tier 5; 0.1 lb/unit; 200 gp/unit; seasoning; consumed); 1 × gore organ (component tier 3; 0.14 lb/unit; 94 gp/unit; catalyst; consumed).

**Food reservation:** 3.2 lb credited nutritive source inputs; up to 0 lb may return as the selected catalyst. For Standard quantity without catalyst retention, add 0 lb real ration-equivalent food. Before any completion check reserve 0 lb supplementary food for full Masterwork yield and worst legal nutritive catalyst retention. This is additional to every exact ingredient. Reservation does not consume food; after the outcome/catalyst choice and before finished servings are created, incorporate only the actual required amount. Generic failure without a finished product leaves all supplement unincorporated; a specific failed product spends only its required supplement. Actual food reference is 25 cp/lb, prorated from 5 sp per 2-lb daily ration; supplier quotes and transaction rounding still apply.

**Serving and storage:** each serving contains exactly 2/3 lb food and credits 1/3 Small/Medium daily food or 1/6 Large daily food after complete consumption. Before rolling, predeclare actual output dispositions for all 1 possible servings: real compatible storage capacity or distinct present recipients ready to begin immediate ten-minute consumption, one simultaneous slot per recipient. Immediate servings commit at batch completion; an invalid immediate slot needs actual reserved storage or cannot use the exception. Existing containers count only to their real capacity. A dedicated Meal Crock is 0.5 lb empty, 2 sp, 1 quart, AC 13/HP 2; one serving gives 7/6 lb gross. No water, fuel or full Supply is supplied by this food credit. Finished-food shelf life is 24 unprotected elapsed hours.

**Flawed:** {"mode": "treat-as-Failed", "quantity": 0, "materialRecoveryPercent": 25}. Quality can change finite yield or dedicated mundane packaging durability; it does not improve meal potency. A dedicated Meal Crock first improved from maximum HP 2 to 3 gains exactly +1 current HP, preserving existing damage; an already-HP-3 crock gains neither again.

**Nutritional source map:** Butter counts as ordinary food; Oil counts as ordinary food; Meat counts as ordinary food; Honey counts as ordinary food; gore organ has no credited nutritive bulk in this card.

## recipe-99 — Superior Verdant Pie of Dream Bark

**Source:** public; Cooking level 6; tier 3; Uncommon; DC 17; 16 active hours; 1 serving(s). Standard batch reference 326 gp.

**Preserved effect:** After a 10-minute meal, gain 7 temporary hit points and advantage on saves against poison and disease. A creature can benefit from one feast at a time.

**Operational effect:** After completing and accepting this feast, offer 7 temporary HP. Gain advantage on saves against poison and disease until the parent feast ends. No automatic condition cure or immunity.

**Duration:** Parent feast and its temporary HP end at the next completed beneficial Long Rest. Every rider also ends when this feast ends or is replaced. Its explicitly shorter deadline remains separate.

**Work:** Cookfire or Kitchen; Cook's utensils, Knife, Pot or pan. Mode workshop; field flag false; maximum assistants 0; formula required true.

**Exact ingredients:** 3 × Flour (component tier 3; 0.1 lb/unit; 25 gp/unit; substrate; consumed); 3 × Spices (component tier 3; 0.1 lb/unit; 25 gp/unit; seasoning; consumed); 1 × Meat (component tier 3; 0.1 lb/unit; 25 gp/unit; substrate; consumed); 1 × dream bark (component tier 2; 0.45 lb/unit; 31 gp/unit; material; consumed).

**Food reservation:** 0.4 lb credited nutritive source inputs; up to 0 lb may return as the selected catalyst. For Standard quantity without catalyst retention, add 0.27 lb real ration-equivalent food. Before any completion check reserve 0.27 lb supplementary food for full Masterwork yield and worst legal nutritive catalyst retention. This is additional to every exact ingredient. Reservation does not consume food; after the outcome/catalyst choice and before finished servings are created, incorporate only the actual required amount. Generic failure without a finished product leaves all supplement unincorporated; a specific failed product spends only its required supplement. Actual food reference is 25 cp/lb, prorated from 5 sp per 2-lb daily ration; supplier quotes and transaction rounding still apply.

**Serving and storage:** each serving contains exactly 2/3 lb food and credits 1/3 Small/Medium daily food or 1/6 Large daily food after complete consumption. Before rolling, predeclare actual output dispositions for all 1 possible servings: real compatible storage capacity or distinct present recipients ready to begin immediate ten-minute consumption, one simultaneous slot per recipient. Immediate servings commit at batch completion; an invalid immediate slot needs actual reserved storage or cannot use the exception. Existing containers count only to their real capacity. A dedicated Meal Crock is 0.5 lb empty, 2 sp, 1 quart, AC 13/HP 2; one serving gives 7/6 lb gross. No water, fuel or full Supply is supplied by this food credit. Finished-food shelf life is 24 unprotected elapsed hours.

**Flawed:** {"mode": "treat-as-Failed", "quantity": 0, "materialRecoveryPercent": 25}. Quality can change finite yield or dedicated mundane packaging durability; it does not improve meal potency. A dedicated Meal Crock first improved from maximum HP 2 to 3 gains exactly +1 current HP, preserving existing damage; an already-HP-3 crock gains neither again.

**Nutritional source map:** Flour counts as ordinary food; Spices has no credited nutritive bulk in this card; Meat counts as ordinary food; dream bark has no credited nutritive bulk in this card.

## recipe-100 — Masterwork Venom Meal of Poisonous Meat

**Source:** public; Cooking level 8; tier 4; Uncommon; DC 16; 24 active hours; 1 serving(s). Standard batch reference 1634 gp.

**Preserved effect:** After a 10-minute meal, gain 8 temporary hit points and advantage on saves against poison for 4 hours. A creature can benefit from one feast at a time.

**Operational effect:** After completing and accepting this feast, offer 8 temporary HP. Gain advantage on saves against poison for 4 elapsed hours, ending earlier with the parent feast. No poison immunity, condition cure or damage resistance.

**Duration:** Parent feast and its temporary HP end at the next completed beneficial Long Rest. Every rider also ends when this feast ends or is replaced. Its explicitly shorter deadline remains separate.

**Work:** Cookfire or Kitchen; Cook's utensils, Knife, Pot or pan. Mode workshop; field flag false; maximum assistants 0; formula required true.

**Exact ingredients:** 3 × Spices (component tier 4; 0.1 lb/unit; 75 gp/unit; seasoning; consumed); 3 × Milk (component tier 4; 0.5 lb/unit; 75 gp/unit; substrate; consumed); 4 × Salt (component tier 4; 0.1 lb/unit; 75 gp/unit; seasoning; consumed); 5 × Meat (component tier 4; 0.1 lb/unit; 75 gp/unit; substrate; consumed); 1 × Poisonous meat (component tier 1; 0.38 lb/unit; 14 gp/unit; catalyst; consumed).

**Food reservation:** 2.38 lb credited nutritive source inputs; up to 0.38 lb may return as the selected catalyst. For Standard quantity without catalyst retention, add 0 lb real ration-equivalent food. Before any completion check reserve 0 lb supplementary food for full Masterwork yield and worst legal nutritive catalyst retention. This is additional to every exact ingredient. Reservation does not consume food; after the outcome/catalyst choice and before finished servings are created, incorporate only the actual required amount. Generic failure without a finished product leaves all supplement unincorporated; a specific failed product spends only its required supplement. Actual food reference is 25 cp/lb, prorated from 5 sp per 2-lb daily ration; supplier quotes and transaction rounding still apply.

**Serving and storage:** each serving contains exactly 2/3 lb food and credits 1/3 Small/Medium daily food or 1/6 Large daily food after complete consumption. Before rolling, predeclare actual output dispositions for all 1 possible servings: real compatible storage capacity or distinct present recipients ready to begin immediate ten-minute consumption, one simultaneous slot per recipient. Immediate servings commit at batch completion; an invalid immediate slot needs actual reserved storage or cannot use the exception. Existing containers count only to their real capacity. A dedicated Meal Crock is 0.5 lb empty, 2 sp, 1 quart, AC 13/HP 2; one serving gives 7/6 lb gross. No water, fuel or full Supply is supplied by this food credit. Finished-food shelf life is 24 unprotected elapsed hours.

**Flawed:** {"mode": "treat-as-Failed", "quantity": 0, "materialRecoveryPercent": 25}. Quality can change finite yield or dedicated mundane packaging durability; it does not improve meal potency. A dedicated Meal Crock first improved from maximum HP 2 to 3 gains exactly +1 current HP, preserving existing damage; an already-HP-3 crock gains neither again.

**Nutritional source map:** Spices has no credited nutritive bulk in this card; Milk counts as ordinary food; Salt has no credited nutritive bulk in this card; Meat counts as ordinary food; Poisonous meat counts as ordinary food.

## recipe-101 — Masterwork Stone Pie of Gore Organ

**Source:** public; Cooking level 7; tier 4; Uncommon; DC 15; 8 active hours; 1 serving(s). Standard batch reference 1269 gp.

**Preserved effect:** After a 10-minute meal, gain 8 temporary hit points and advantage against being knocked prone for 1 hour. A creature can benefit from one feast at a time.

**Operational effect:** After completing and accepting this feast, offer 8 temporary HP. For 1 elapsed hour or until the parent feast ends, whichever comes first, gain advantage on an actual check or save whose direct consequence includes becoming Prone. No immunity to automatic Prone effects or benefit when standing.

**Duration:** Parent feast and its temporary HP end at the next completed beneficial Long Rest. Every rider also ends when this feast ends or is replaced. Its explicitly shorter deadline remains separate.

**Work:** Cookfire or Kitchen; Cook's utensils, Knife, Pot or pan. Mode expedition; field flag true; maximum assistants 0; formula required true.

**Exact ingredients:** 4 × Wine (component tier 4; 0.5 lb/unit; 75 gp/unit; seasoning; consumed); 2 × Fruit (component tier 4; 0.1 lb/unit; 75 gp/unit; substrate; consumed); 5 × Honey (component tier 4; 0.1 lb/unit; 75 gp/unit; seasoning; consumed); 1 × gore organ (component tier 3; 0.14 lb/unit; 94 gp/unit; catalyst; consumed).

**Food reservation:** 0.7 lb credited nutritive source inputs; up to 0 lb may return as the selected catalyst. For Standard quantity without catalyst retention, add 0 lb real ration-equivalent food. Before any completion check reserve 0 lb supplementary food for full Masterwork yield and worst legal nutritive catalyst retention. This is additional to every exact ingredient. Reservation does not consume food; after the outcome/catalyst choice and before finished servings are created, incorporate only the actual required amount. Generic failure without a finished product leaves all supplement unincorporated; a specific failed product spends only its required supplement. Actual food reference is 25 cp/lb, prorated from 5 sp per 2-lb daily ration; supplier quotes and transaction rounding still apply.

**Serving and storage:** each serving contains exactly 2/3 lb food and credits 1/3 Small/Medium daily food or 1/6 Large daily food after complete consumption. Before rolling, predeclare actual output dispositions for all 1 possible servings: real compatible storage capacity or distinct present recipients ready to begin immediate ten-minute consumption, one simultaneous slot per recipient. Immediate servings commit at batch completion; an invalid immediate slot needs actual reserved storage or cannot use the exception. Existing containers count only to their real capacity. A dedicated Meal Crock is 0.5 lb empty, 2 sp, 1 quart, AC 13/HP 2; one serving gives 7/6 lb gross. No water, fuel or full Supply is supplied by this food credit. Finished-food shelf life is 24 unprotected elapsed hours.

**Flawed:** {"mode": "treat-as-Failed", "quantity": 0, "materialRecoveryPercent": 25}. Quality can change finite yield or dedicated mundane packaging durability; it does not improve meal potency. A dedicated Meal Crock first improved from maximum HP 2 to 3 gains exactly +1 current HP, preserving existing damage; an already-HP-3 crock gains neither again.

**Nutritional source map:** Wine has no credited nutritive bulk in this card; Fruit counts as ordinary food; Honey counts as ordinary food; gore organ has no credited nutritive bulk in this card.

## recipe-102 — Exalted Venom Snack of Poisonous Meat

**Source:** public; Cooking level 10; tier 5; Uncommon; DC 13; 24 active hours; 1 serving(s). Standard batch reference 2839 gp.

**Preserved effect:** After a 10-minute meal, gain 9 temporary hit points and advantage on saves against poison for 4 hours. A creature can benefit from one feast at a time.

**Operational effect:** After completing and accepting this feast, offer 9 temporary HP. Gain advantage on saves against poison for 4 elapsed hours, ending earlier with the parent feast. No poison immunity, condition cure or damage resistance.

**Duration:** Parent feast and its temporary HP end at the next completed beneficial Long Rest. Every rider also ends when this feast ends or is replaced. Its explicitly shorter deadline remains separate.

**Work:** Cookfire or Kitchen; Cook's utensils, Knife, Pot or pan. Mode workshop; field flag false; maximum assistants 0; formula required true.

**Exact ingredients:** 4 × Butter (component tier 5; 0.1 lb/unit; 200 gp/unit; seasoning; consumed); 1 × Flour (component tier 5; 0.1 lb/unit; 200 gp/unit; substrate; consumed); 5 × Water (component tier 5; 0.5 lb/unit; 200 gp/unit; solvent; consumed); 1 × Poisonous meat (component tier 1; 0.38 lb/unit; 14 gp/unit; catalyst; consumed).

**Food reservation:** 0.88 lb credited nutritive source inputs; up to 0.38 lb may return as the selected catalyst. For Standard quantity without catalyst retention, add 0 lb real ration-equivalent food. Before any completion check reserve 0.17 lb supplementary food for full Masterwork yield and worst legal nutritive catalyst retention. This is additional to every exact ingredient. Reservation does not consume food; after the outcome/catalyst choice and before finished servings are created, incorporate only the actual required amount. Generic failure without a finished product leaves all supplement unincorporated; a specific failed product spends only its required supplement. Actual food reference is 25 cp/lb, prorated from 5 sp per 2-lb daily ration; supplier quotes and transaction rounding still apply.

**Serving and storage:** each serving contains exactly 2/3 lb food and credits 1/3 Small/Medium daily food or 1/6 Large daily food after complete consumption. Before rolling, predeclare actual output dispositions for all 1 possible servings: real compatible storage capacity or distinct present recipients ready to begin immediate ten-minute consumption, one simultaneous slot per recipient. Immediate servings commit at batch completion; an invalid immediate slot needs actual reserved storage or cannot use the exception. Existing containers count only to their real capacity. A dedicated Meal Crock is 0.5 lb empty, 2 sp, 1 quart, AC 13/HP 2; one serving gives 7/6 lb gross. No water, fuel or full Supply is supplied by this food credit. Finished-food shelf life is 24 unprotected elapsed hours.

**Flawed:** {"mode": "treat-as-Failed", "quantity": 0, "materialRecoveryPercent": 25}. Quality can change finite yield or dedicated mundane packaging durability; it does not improve meal potency. A dedicated Meal Crock first improved from maximum HP 2 to 3 gains exactly +1 current HP, preserving existing damage; an already-HP-3 crock gains neither again.

**Nutritional source map:** Butter counts as ordinary food; Flour counts as ordinary food; Water has no credited nutritive bulk in this card; Poisonous meat counts as ordinary food.

## recipe-103 — Masterwork Resonant Meal of Black Blood

**Source:** public; Cooking level 8; tier 4; Uncommon; DC 13; 16 active hours; 1 serving(s). Standard batch reference 1032 gp.

**Preserved effect:** After a 10-minute meal, gain 8 temporary hit points and restore 1 Resonance Point(s). A creature can benefit from one feast at a time.

**Operational effect:** After completing and accepting this feast, offer 8 temporary HP. On accepting this completed feast, restore 1 expended RP, capped at the actual existing RP maximum. There is no new once-per-rest cap: another genuine paid serving requires its full consumption and accepted feast replacement. No pool creation, RC conversion, Dissonance/Refrain reset, partial-meal or replay recovery.

**Duration:** Parent feast and its temporary HP end at the next completed beneficial Long Rest. Every rider also ends when this feast ends or is replaced. Its explicitly shorter deadline remains separate.

**Work:** Cookfire or Kitchen; Cook's utensils, Knife, Pot or pan. Mode workshop; field flag false; maximum assistants 0; formula required true.

**Exact ingredients:** 5 × Butter (component tier 4; 0.1 lb/unit; 75 gp/unit; seasoning; consumed); 4 × Fruit (component tier 4; 0.1 lb/unit; 75 gp/unit; substrate; consumed); 1 × black blood sample (component tier 2; 0.38 lb/unit; 42 gp/unit; catalyst; consumed).

**Food reservation:** 0.9 lb credited nutritive source inputs; up to 0 lb may return as the selected catalyst. For Standard quantity without catalyst retention, add 0 lb real ration-equivalent food. Before any completion check reserve 0 lb supplementary food for full Masterwork yield and worst legal nutritive catalyst retention. This is additional to every exact ingredient. Reservation does not consume food; after the outcome/catalyst choice and before finished servings are created, incorporate only the actual required amount. Generic failure without a finished product leaves all supplement unincorporated; a specific failed product spends only its required supplement. Actual food reference is 25 cp/lb, prorated from 5 sp per 2-lb daily ration; supplier quotes and transaction rounding still apply.

**Serving and storage:** each serving contains exactly 2/3 lb food and credits 1/3 Small/Medium daily food or 1/6 Large daily food after complete consumption. Before rolling, predeclare actual output dispositions for all 1 possible servings: real compatible storage capacity or distinct present recipients ready to begin immediate ten-minute consumption, one simultaneous slot per recipient. Immediate servings commit at batch completion; an invalid immediate slot needs actual reserved storage or cannot use the exception. Existing containers count only to their real capacity. A dedicated Meal Crock is 0.5 lb empty, 2 sp, 1 quart, AC 13/HP 2; one serving gives 7/6 lb gross. No water, fuel or full Supply is supplied by this food credit. Finished-food shelf life is 24 unprotected elapsed hours.

**Flawed:** {"mode": "treat-as-Failed", "quantity": 0, "materialRecoveryPercent": 25}. Quality can change finite yield or dedicated mundane packaging durability; it does not improve meal potency. A dedicated Meal Crock first improved from maximum HP 2 to 3 gains exactly +1 current HP, preserving existing damage; an already-HP-3 crock gains neither again.

**Nutritional source map:** Butter counts as ordinary food; Fruit counts as ordinary food; black blood sample has no credited nutritive bulk in this card.

## recipe-104 — Exalted Tide Soup of Sea Meat

**Source:** public; Cooking level 10; tier 5; Uncommon; DC 14; 16 active hours; 1 serving(s). Standard batch reference 2526 gp.

**Preserved effect:** After a 10-minute meal, gain 9 temporary hit points and a swimming speed equal to walking speed for 1 hour. A creature can benefit from one feast at a time.

**Operational effect:** After completing and accepting this feast, offer 9 temporary HP. For 1 elapsed hour or until the parent feast ends, whichever comes first, gain a swimming speed equal to current effective walking speed, recalculated as that speed changes. No new walking mode, water breathing, underwater sight or current immunity.

**Duration:** Parent feast and its temporary HP end at the next completed beneficial Long Rest. Every rider also ends when this feast ends or is replaced. Its explicitly shorter deadline remains separate.

**Work:** Cookfire or Kitchen; Cook's utensils, Knife, Pot or pan. Mode workshop; field flag false; maximum assistants 0; formula required true.

**Exact ingredients:** 5 × Butter (component tier 5; 0.1 lb/unit; 200 gp/unit; seasoning; consumed); 4 × Oil (component tier 5; 0.5 lb/unit; 200 gp/unit; solvent; consumed); 1 × Sea meat (component tier 1; 0.39 lb/unit; 12 gp/unit; material; consumed).

**Food reservation:** 2.89 lb credited nutritive source inputs; up to 0 lb may return as the selected catalyst. For Standard quantity without catalyst retention, add 0 lb real ration-equivalent food. Before any completion check reserve 0 lb supplementary food for full Masterwork yield and worst legal nutritive catalyst retention. This is additional to every exact ingredient. Reservation does not consume food; after the outcome/catalyst choice and before finished servings are created, incorporate only the actual required amount. Generic failure without a finished product leaves all supplement unincorporated; a specific failed product spends only its required supplement. Actual food reference is 25 cp/lb, prorated from 5 sp per 2-lb daily ration; supplier quotes and transaction rounding still apply.

**Serving and storage:** each serving contains exactly 2/3 lb food and credits 1/3 Small/Medium daily food or 1/6 Large daily food after complete consumption. Before rolling, predeclare actual output dispositions for all 1 possible servings: real compatible storage capacity or distinct present recipients ready to begin immediate ten-minute consumption, one simultaneous slot per recipient. Immediate servings commit at batch completion; an invalid immediate slot needs actual reserved storage or cannot use the exception. Existing containers count only to their real capacity. A dedicated Meal Crock is 0.5 lb empty, 2 sp, 1 quart, AC 13/HP 2; one serving gives 7/6 lb gross. No water, fuel or full Supply is supplied by this food credit. Finished-food shelf life is 24 unprotected elapsed hours.

**Flawed:** {"mode": "treat-as-Failed", "quantity": 0, "materialRecoveryPercent": 25}. Quality can change finite yield or dedicated mundane packaging durability; it does not improve meal potency. A dedicated Meal Crock first improved from maximum HP 2 to 3 gains exactly +1 current HP, preserving existing damage; an already-HP-3 crock gains neither again.

**Nutritional source map:** Butter counts as ordinary food; Oil counts as ordinary food; Sea meat counts as ordinary food.

## recipe-105 — Superior Tide Meal of Sea Meat

**Source:** public; Cooking level 6; tier 3; Uncommon; DC 17; 8 active hours; 1 serving(s). Standard batch reference 479 gp.

**Preserved effect:** After a 10-minute meal, gain 7 temporary hit points and a swimming speed equal to walking speed for 1 hour. A creature can benefit from one feast at a time.

**Operational effect:** After completing and accepting this feast, offer 7 temporary HP. For 1 elapsed hour or until the parent feast ends, whichever comes first, gain a swimming speed equal to current effective walking speed, recalculated as that speed changes. No new walking mode, water breathing, underwater sight or current immunity.

**Duration:** Parent feast and its temporary HP end at the next completed beneficial Long Rest. Every rider also ends when this feast ends or is replaced. Its explicitly shorter deadline remains separate.

**Work:** Cookfire or Kitchen; Cook's utensils, Knife, Pot or pan. Mode expedition; field flag true; maximum assistants 0; formula required true.

**Exact ingredients:** 4 × Flour (component tier 3; 0.1 lb/unit; 25 gp/unit; substrate; consumed); 5 × Salt (component tier 3; 0.1 lb/unit; 25 gp/unit; seasoning; consumed); 4 × Water (component tier 3; 0.5 lb/unit; 25 gp/unit; solvent; consumed); 1 × Sea meat (component tier 1; 0.39 lb/unit; 12 gp/unit; material; consumed).

**Food reservation:** 0.79 lb credited nutritive source inputs; up to 0 lb may return as the selected catalyst. For Standard quantity without catalyst retention, add 0 lb real ration-equivalent food. Before any completion check reserve 0 lb supplementary food for full Masterwork yield and worst legal nutritive catalyst retention. This is additional to every exact ingredient. Reservation does not consume food; after the outcome/catalyst choice and before finished servings are created, incorporate only the actual required amount. Generic failure without a finished product leaves all supplement unincorporated; a specific failed product spends only its required supplement. Actual food reference is 25 cp/lb, prorated from 5 sp per 2-lb daily ration; supplier quotes and transaction rounding still apply.

**Serving and storage:** each serving contains exactly 2/3 lb food and credits 1/3 Small/Medium daily food or 1/6 Large daily food after complete consumption. Before rolling, predeclare actual output dispositions for all 1 possible servings: real compatible storage capacity or distinct present recipients ready to begin immediate ten-minute consumption, one simultaneous slot per recipient. Immediate servings commit at batch completion; an invalid immediate slot needs actual reserved storage or cannot use the exception. Existing containers count only to their real capacity. A dedicated Meal Crock is 0.5 lb empty, 2 sp, 1 quart, AC 13/HP 2; one serving gives 7/6 lb gross. No water, fuel or full Supply is supplied by this food credit. Finished-food shelf life is 24 unprotected elapsed hours.

**Flawed:** {"mode": "treat-as-Failed", "quantity": 0, "materialRecoveryPercent": 25}. Quality can change finite yield or dedicated mundane packaging durability; it does not improve meal potency. A dedicated Meal Crock first improved from maximum HP 2 to 3 gains exactly +1 current HP, preserving existing damage; an already-HP-3 crock gains neither again.

**Nutritional source map:** Flour counts as ordinary food; Salt has no credited nutritive bulk in this card; Water has no credited nutritive bulk in this card; Sea meat counts as ordinary food.

## recipe-106 — Exalted Grave Soup of Infernal Marrow

**Source:** public; Cooking level 10; tier 5; Rare; DC 19; 40 active hours; 1 serving(s). Standard batch reference 6287 gp.

**Preserved effect:** After a 10-minute meal, gain 11 temporary hit points and resistance to necrotic damage for 1 hour. A creature can benefit from one feast at a time.

**Operational effect:** After completing and accepting this feast, offer 11 temporary HP. Gain resistance to necrotic damage for 1 elapsed hour(s), ending earlier with the parent feast.

**Duration:** Parent feast and its temporary HP end at the next completed beneficial Long Rest. Every rider also ends when this feast ends or is replaced. Its explicitly shorter deadline remains separate.

**Work:** Cookfire or Kitchen; Cook's utensils, Knife, Pot or pan. Mode workshop; field flag false; maximum assistants 0; formula required true.

**Exact ingredients:** 5 × Water (component tier 5; 0.5 lb/unit; 200 gp/unit; solvent; consumed); 5 × Herbs (component tier 5; 0.1 lb/unit; 200 gp/unit; substrate; consumed); 5 × Sugar (component tier 5; 0.1 lb/unit; 200 gp/unit; seasoning; consumed); 3 × Oil (component tier 5; 0.5 lb/unit; 200 gp/unit; solvent; consumed); 4 × Salt (component tier 5; 0.1 lb/unit; 200 gp/unit; seasoning; consumed); 1 × infernal marrow (component tier 3; 0.18 lb/unit; 109 gp/unit; material; consumed).

**Food reservation:** 2 lb credited nutritive source inputs; up to 0 lb may return as the selected catalyst. For Standard quantity without catalyst retention, add 0 lb real ration-equivalent food. Before any completion check reserve 0 lb supplementary food for full Masterwork yield and worst legal nutritive catalyst retention. This is additional to every exact ingredient. Reservation does not consume food; after the outcome/catalyst choice and before finished servings are created, incorporate only the actual required amount. Generic failure without a finished product leaves all supplement unincorporated; a specific failed product spends only its required supplement. Actual food reference is 25 cp/lb, prorated from 5 sp per 2-lb daily ration; supplier quotes and transaction rounding still apply.

**Serving and storage:** each serving contains exactly 2/3 lb food and credits 1/3 Small/Medium daily food or 1/6 Large daily food after complete consumption. Before rolling, predeclare actual output dispositions for all 1 possible servings: real compatible storage capacity or distinct present recipients ready to begin immediate ten-minute consumption, one simultaneous slot per recipient. Immediate servings commit at batch completion; an invalid immediate slot needs actual reserved storage or cannot use the exception. Existing containers count only to their real capacity. A dedicated Meal Crock is 0.5 lb empty, 2 sp, 1 quart, AC 13/HP 2; one serving gives 7/6 lb gross. No water, fuel or full Supply is supplied by this food credit. Finished-food shelf life is 24 unprotected elapsed hours.

**Flawed:** {"mode": "treat-as-Failed", "quantity": 0, "materialRecoveryPercent": 25}. Quality can change finite yield or dedicated mundane packaging durability; it does not improve meal potency. A dedicated Meal Crock first improved from maximum HP 2 to 3 gains exactly +1 current HP, preserving existing damage; an already-HP-3 crock gains neither again.

**Nutritional source map:** Water has no credited nutritive bulk in this card; Herbs has no credited nutritive bulk in this card; Sugar counts as ordinary food; Oil counts as ordinary food; Salt has no credited nutritive bulk in this card; infernal marrow has no credited nutritive bulk in this card.

## recipe-107 — Exalted Tide Bread of Sea Sinew

**Source:** public; Cooking level 10; tier 5; Rare; DC 18; 80 active hours; 1 serving(s). Standard batch reference 4620 gp.

**Preserved effect:** After a 10-minute meal, gain 11 temporary hit points and a swimming speed equal to walking speed for 1 hour. A creature can benefit from one feast at a time.

**Operational effect:** After completing and accepting this feast, offer 11 temporary HP. For 1 elapsed hour or until the parent feast ends, whichever comes first, gain a swimming speed equal to current effective walking speed, recalculated as that speed changes. No new walking mode, water breathing, underwater sight or current immunity.

**Duration:** Parent feast and its temporary HP end at the next completed beneficial Long Rest. Every rider also ends when this feast ends or is replaced. Its explicitly shorter deadline remains separate.

**Work:** Cookfire or Kitchen; Cook's utensils, Knife, Pot or pan. Mode haven; field flag false; maximum assistants 0; formula required true.

**Exact ingredients:** 1 × Spices (component tier 5; 0.1 lb/unit; 200 gp/unit; seasoning; consumed); 4 × Oil (component tier 5; 0.5 lb/unit; 200 gp/unit; solvent; consumed); 3 × Fruit (component tier 5; 0.1 lb/unit; 200 gp/unit; substrate; consumed); 2 × Butter (component tier 5; 0.1 lb/unit; 200 gp/unit; seasoning; consumed); 5 × Meat (component tier 5; 0.1 lb/unit; 200 gp/unit; substrate; consumed); 1 × Sea sinew (component tier 3; 0.29 lb/unit; 126 gp/unit; material; consumed).

**Food reservation:** 3 lb credited nutritive source inputs; up to 0 lb may return as the selected catalyst. For Standard quantity without catalyst retention, add 0 lb real ration-equivalent food. Before any completion check reserve 0 lb supplementary food for full Masterwork yield and worst legal nutritive catalyst retention. This is additional to every exact ingredient. Reservation does not consume food; after the outcome/catalyst choice and before finished servings are created, incorporate only the actual required amount. Generic failure without a finished product leaves all supplement unincorporated; a specific failed product spends only its required supplement. Actual food reference is 25 cp/lb, prorated from 5 sp per 2-lb daily ration; supplier quotes and transaction rounding still apply.

**Serving and storage:** each serving contains exactly 2/3 lb food and credits 1/3 Small/Medium daily food or 1/6 Large daily food after complete consumption. Before rolling, predeclare actual output dispositions for all 1 possible servings: real compatible storage capacity or distinct present recipients ready to begin immediate ten-minute consumption, one simultaneous slot per recipient. Immediate servings commit at batch completion; an invalid immediate slot needs actual reserved storage or cannot use the exception. Existing containers count only to their real capacity. A dedicated Meal Crock is 0.5 lb empty, 2 sp, 1 quart, AC 13/HP 2; one serving gives 7/6 lb gross. No water, fuel or full Supply is supplied by this food credit. Finished-food shelf life is 24 unprotected elapsed hours.

**Flawed:** {"mode": "treat-as-Failed", "quantity": 0, "materialRecoveryPercent": 25}. Quality can change finite yield or dedicated mundane packaging durability; it does not improve meal potency. A dedicated Meal Crock first improved from maximum HP 2 to 3 gains exactly +1 current HP, preserving existing damage; an already-HP-3 crock gains neither again.

**Nutritional source map:** Spices has no credited nutritive bulk in this card; Oil counts as ordinary food; Fruit counts as ordinary food; Butter counts as ordinary food; Meat counts as ordinary food; Sea sinew has no credited nutritive bulk in this card.

## recipe-108 — Mythic Stone Meal of Shamanic Bloodstone

**Source:** director-only; Cooking level 15; tier 8; Rare; DC 18; 80 active hours; 1 serving(s). Standard batch reference 54036 gp.

**Preserved effect:** After a 10-minute meal, gain 14 temporary hit points and advantage against being knocked prone for 1 hour. A creature can benefit from one feast at a time.

**Operational effect:** After completing and accepting this feast, offer 14 temporary HP. For 1 elapsed hour or until the parent feast ends, whichever comes first, gain advantage on an actual check or save whose direct consequence includes becoming Prone. No immunity to automatic Prone effects or benefit when standing.

**Duration:** Parent feast and its temporary HP end at the next completed beneficial Long Rest. Every rider also ends when this feast ends or is replaced. Its explicitly shorter deadline remains separate.

**Work:** Cookfire or Kitchen; Cook's utensils, Knife, Pot or pan. Mode haven; field flag false; maximum assistants 1; formula required true.

**Exact ingredients:** 5 × Eggs (component tier 8; 0.1 lb/unit; 3000 gp/unit; substrate; consumed); 5 × Sugar (component tier 8; 0.1 lb/unit; 3000 gp/unit; seasoning; consumed); 2 × Vegetables (component tier 8; 0.1 lb/unit; 3000 gp/unit; substrate; consumed); 1 × Wine (component tier 8; 0.5 lb/unit; 3000 gp/unit; seasoning; consumed); 1 × shamanic bloodstone (component tier 5; 0.14 lb/unit; 582 gp/unit; catalyst; consumed).

**Food reservation:** 1.2 lb credited nutritive source inputs; up to 0 lb may return as the selected catalyst. For Standard quantity without catalyst retention, add 0 lb real ration-equivalent food. Before any completion check reserve 0 lb supplementary food for full Masterwork yield and worst legal nutritive catalyst retention. This is additional to every exact ingredient. Reservation does not consume food; after the outcome/catalyst choice and before finished servings are created, incorporate only the actual required amount. Generic failure without a finished product leaves all supplement unincorporated; a specific failed product spends only its required supplement. Actual food reference is 25 cp/lb, prorated from 5 sp per 2-lb daily ration; supplier quotes and transaction rounding still apply.

**Serving and storage:** each serving contains exactly 2/3 lb food and credits 1/3 Small/Medium daily food or 1/6 Large daily food after complete consumption. Before rolling, predeclare actual output dispositions for all 1 possible servings: real compatible storage capacity or distinct present recipients ready to begin immediate ten-minute consumption, one simultaneous slot per recipient. Immediate servings commit at batch completion; an invalid immediate slot needs actual reserved storage or cannot use the exception. Existing containers count only to their real capacity. A dedicated Meal Crock is 0.5 lb empty, 2 sp, 1 quart, AC 13/HP 2; one serving gives 7/6 lb gross. No water, fuel or full Supply is supplied by this food credit. Finished-food shelf life is 24 unprotected elapsed hours.

**Flawed:** {"mode": "treat-as-Failed", "quantity": 0, "materialRecoveryPercent": 25}. Quality can change finite yield or dedicated mundane packaging durability; it does not improve meal potency. A dedicated Meal Crock first improved from maximum HP 2 to 3 gains exactly +1 current HP, preserving existing damage; an already-HP-3 crock gains neither again.

**Nutritional source map:** Eggs counts as ordinary food; Sugar counts as ordinary food; Vegetables counts as ordinary food; Wine has no credited nutritive bulk in this card; shamanic bloodstone has no credited nutritive bulk in this card.

## recipe-109 — Mythic Vital Bread of Infernal Marrow

**Source:** director-only; Cooking level 15; tier 8; Rare; DC 19; 40 active hours; 1 serving(s). Standard batch reference 28797 gp.

**Preserved effect:** After a 10-minute meal, gain 14 temporary hit points and +2 to Constitution saves. A creature can benefit from one feast at a time.

**Operational effect:** After completing and accepting this feast, offer 14 temporary HP. Gain +2 to actual Constitution saving throws until the parent feast ends, including concentration and Wound/Injury saves when they are CON saves. Other roll types are not converted.

**Duration:** Parent feast and its temporary HP end at the next completed beneficial Long Rest. Every rider also ends when this feast ends or is replaced. Its explicitly shorter deadline remains separate.

**Work:** Cookfire or Kitchen; Cook's utensils, Knife, Pot or pan. Mode workshop; field flag false; maximum assistants 1; formula required true.

**Exact ingredients:** 2 × Oil (component tier 8; 0.5 lb/unit; 3000 gp/unit; solvent; consumed); 2 × Herbs (component tier 8; 0.1 lb/unit; 3000 gp/unit; substrate; consumed); 1 × Sugar (component tier 8; 0.1 lb/unit; 3000 gp/unit; seasoning; consumed); 2 × Honey (component tier 8; 0.1 lb/unit; 3000 gp/unit; seasoning; consumed); 1 × infernal marrow (component tier 3; 0.18 lb/unit; 109 gp/unit; material; consumed).

**Food reservation:** 1.3 lb credited nutritive source inputs; up to 0 lb may return as the selected catalyst. For Standard quantity without catalyst retention, add 0 lb real ration-equivalent food. Before any completion check reserve 0 lb supplementary food for full Masterwork yield and worst legal nutritive catalyst retention. This is additional to every exact ingredient. Reservation does not consume food; after the outcome/catalyst choice and before finished servings are created, incorporate only the actual required amount. Generic failure without a finished product leaves all supplement unincorporated; a specific failed product spends only its required supplement. Actual food reference is 25 cp/lb, prorated from 5 sp per 2-lb daily ration; supplier quotes and transaction rounding still apply.

**Serving and storage:** each serving contains exactly 2/3 lb food and credits 1/3 Small/Medium daily food or 1/6 Large daily food after complete consumption. Before rolling, predeclare actual output dispositions for all 1 possible servings: real compatible storage capacity or distinct present recipients ready to begin immediate ten-minute consumption, one simultaneous slot per recipient. Immediate servings commit at batch completion; an invalid immediate slot needs actual reserved storage or cannot use the exception. Existing containers count only to their real capacity. A dedicated Meal Crock is 0.5 lb empty, 2 sp, 1 quart, AC 13/HP 2; one serving gives 7/6 lb gross. No water, fuel or full Supply is supplied by this food credit. Finished-food shelf life is 24 unprotected elapsed hours.

**Flawed:** {"mode": "treat-as-Failed", "quantity": 0, "materialRecoveryPercent": 25}. Quality can change finite yield or dedicated mundane packaging durability; it does not improve meal potency. A dedicated Meal Crock first improved from maximum HP 2 to 3 gains exactly +1 current HP, preserving existing damage; an already-HP-3 crock gains neither again.

**Nutritional source map:** Oil counts as ordinary food; Herbs has no credited nutritive bulk in this card; Sugar counts as ordinary food; Honey counts as ordinary food; infernal marrow has no credited nutritive bulk in this card.

## recipe-110 — Legendary Caustic Meal of Caustic Goo

**Source:** restricted; Cooking level 12; tier 6; Rare; DC 19; 40 active hours; 1 serving(s). Standard batch reference 7676 gp.

**Preserved effect:** After a 10-minute meal, gain 12 temporary hit points and resistance to acid damage for 1 hour. A creature can benefit from one feast at a time.

**Operational effect:** After completing and accepting this feast, offer 12 temporary HP. Gain resistance to acid damage for 1 elapsed hour(s), ending earlier with the parent feast.

**Duration:** Parent feast and its temporary HP end at the next completed beneficial Long Rest. Every rider also ends when this feast ends or is replaced. Its explicitly shorter deadline remains separate.

**Work:** Cookfire or Kitchen; Cook's utensils, Knife, Pot or pan. Mode workshop; field flag false; maximum assistants 1; formula required true.

**Exact ingredients:** 1 × Spices (component tier 6; 0.1 lb/unit; 500 gp/unit; seasoning; consumed); 4 × Sugar (component tier 6; 0.1 lb/unit; 500 gp/unit; seasoning; consumed); 3 × Butter (component tier 6; 0.1 lb/unit; 500 gp/unit; seasoning; consumed); 1 × Meat (component tier 6; 0.1 lb/unit; 500 gp/unit; substrate; consumed); 2 × Milk (component tier 6; 0.5 lb/unit; 500 gp/unit; substrate; consumed); 1 × caustic goo (component tier 1; 0.99 lb/unit; 8 gp/unit; material; consumed).

**Food reservation:** 1.8 lb credited nutritive source inputs; up to 0 lb may return as the selected catalyst. For Standard quantity without catalyst retention, add 0 lb real ration-equivalent food. Before any completion check reserve 0 lb supplementary food for full Masterwork yield and worst legal nutritive catalyst retention. This is additional to every exact ingredient. Reservation does not consume food; after the outcome/catalyst choice and before finished servings are created, incorporate only the actual required amount. Generic failure without a finished product leaves all supplement unincorporated; a specific failed product spends only its required supplement. Actual food reference is 25 cp/lb, prorated from 5 sp per 2-lb daily ration; supplier quotes and transaction rounding still apply.

**Serving and storage:** each serving contains exactly 2/3 lb food and credits 1/3 Small/Medium daily food or 1/6 Large daily food after complete consumption. Before rolling, predeclare actual output dispositions for all 1 possible servings: real compatible storage capacity or distinct present recipients ready to begin immediate ten-minute consumption, one simultaneous slot per recipient. Immediate servings commit at batch completion; an invalid immediate slot needs actual reserved storage or cannot use the exception. Existing containers count only to their real capacity. A dedicated Meal Crock is 0.5 lb empty, 2 sp, 1 quart, AC 13/HP 2; one serving gives 7/6 lb gross. No water, fuel or full Supply is supplied by this food credit. Finished-food shelf life is 24 unprotected elapsed hours.

**Flawed:** {"mode": "treat-as-Failed", "quantity": 0, "materialRecoveryPercent": 25}. Quality can change finite yield or dedicated mundane packaging durability; it does not improve meal potency. A dedicated Meal Crock first improved from maximum HP 2 to 3 gains exactly +1 current HP, preserving existing damage; an already-HP-3 crock gains neither again.

**Nutritional source map:** Spices has no credited nutritive bulk in this card; Sugar counts as ordinary food; Butter counts as ordinary food; Meat counts as ordinary food; Milk counts as ordinary food; caustic goo has no credited nutritive bulk in this card.

## recipe-111 — Legendary Tide Soup of Sea Sinew

**Source:** restricted; Cooking level 11; tier 6; Rare; DC 20; 80 active hours; 1 serving(s). Standard batch reference 8035 gp.

**Preserved effect:** After a 10-minute meal, gain 12 temporary hit points and a swimming speed equal to walking speed for 1 hour. A creature can benefit from one feast at a time.

**Operational effect:** After completing and accepting this feast, offer 12 temporary HP. For 1 elapsed hour or until the parent feast ends, whichever comes first, gain a swimming speed equal to current effective walking speed, recalculated as that speed changes. No new walking mode, water breathing, underwater sight or current immunity.

**Duration:** Parent feast and its temporary HP end at the next completed beneficial Long Rest. Every rider also ends when this feast ends or is replaced. Its explicitly shorter deadline remains separate.

**Work:** Cookfire or Kitchen; Cook's utensils, Knife, Pot or pan. Mode haven; field flag false; maximum assistants 0; formula required true.

**Exact ingredients:** 2 × Herbs (component tier 6; 0.1 lb/unit; 500 gp/unit; substrate; consumed); 5 × Water (component tier 6; 0.5 lb/unit; 500 gp/unit; solvent; consumed); 3 × Salt (component tier 6; 0.1 lb/unit; 500 gp/unit; seasoning; consumed); 1 × Flour (component tier 6; 0.1 lb/unit; 500 gp/unit; substrate; consumed); 1 × Sea sinew (component tier 3; 0.29 lb/unit; 126 gp/unit; material; consumed).

**Food reservation:** 0.1 lb credited nutritive source inputs; up to 0 lb may return as the selected catalyst. For Standard quantity without catalyst retention, add 0.57 lb real ration-equivalent food. Before any completion check reserve 0.57 lb supplementary food for full Masterwork yield and worst legal nutritive catalyst retention. This is additional to every exact ingredient. Reservation does not consume food; after the outcome/catalyst choice and before finished servings are created, incorporate only the actual required amount. Generic failure without a finished product leaves all supplement unincorporated; a specific failed product spends only its required supplement. Actual food reference is 25 cp/lb, prorated from 5 sp per 2-lb daily ration; supplier quotes and transaction rounding still apply.

**Serving and storage:** each serving contains exactly 2/3 lb food and credits 1/3 Small/Medium daily food or 1/6 Large daily food after complete consumption. Before rolling, predeclare actual output dispositions for all 1 possible servings: real compatible storage capacity or distinct present recipients ready to begin immediate ten-minute consumption, one simultaneous slot per recipient. Immediate servings commit at batch completion; an invalid immediate slot needs actual reserved storage or cannot use the exception. Existing containers count only to their real capacity. A dedicated Meal Crock is 0.5 lb empty, 2 sp, 1 quart, AC 13/HP 2; one serving gives 7/6 lb gross. No water, fuel or full Supply is supplied by this food credit. Finished-food shelf life is 24 unprotected elapsed hours.

**Flawed:** {"mode": "treat-as-Failed", "quantity": 0, "materialRecoveryPercent": 25}. Quality can change finite yield or dedicated mundane packaging durability; it does not improve meal potency. A dedicated Meal Crock first improved from maximum HP 2 to 3 gains exactly +1 current HP, preserving existing damage; an already-HP-3 crock gains neither again.

**Nutritional source map:** Herbs has no credited nutritive bulk in this card; Water has no credited nutritive bulk in this card; Salt has no credited nutritive bulk in this card; Flour counts as ordinary food; Sea sinew has no credited nutritive bulk in this card.

## recipe-112 — Relic Stone Cake of Shamanic Bloodstone

**Source:** director-only; Cooking level 14; tier 7; Rare; DC 18; 40 active hours; 1 serving(s). Standard batch reference 30226 gp.

**Preserved effect:** After a 10-minute meal, gain 13 temporary hit points and advantage against being knocked prone for 1 hour. A creature can benefit from one feast at a time.

**Operational effect:** After completing and accepting this feast, offer 13 temporary HP. For 1 elapsed hour or until the parent feast ends, whichever comes first, gain advantage on an actual check or save whose direct consequence includes becoming Prone. No immunity to automatic Prone effects or benefit when standing.

**Duration:** Parent feast and its temporary HP end at the next completed beneficial Long Rest. Every rider also ends when this feast ends or is replaced. Its explicitly shorter deadline remains separate.

**Work:** Cookfire or Kitchen; Cook's utensils, Knife, Pot or pan. Mode workshop; field flag false; maximum assistants 1; formula required true.

**Exact ingredients:** 2 × Honey (component tier 7; 0.1 lb/unit; 1200 gp/unit; seasoning; consumed); 4 × Flour (component tier 7; 0.1 lb/unit; 1200 gp/unit; substrate; consumed); 5 × Fruit (component tier 7; 0.1 lb/unit; 1200 gp/unit; substrate; consumed); 5 × Meat (component tier 7; 0.1 lb/unit; 1200 gp/unit; substrate; consumed); 2 × Eggs (component tier 7; 0.1 lb/unit; 1200 gp/unit; substrate; consumed); 1 × shamanic bloodstone (component tier 5; 0.14 lb/unit; 582 gp/unit; catalyst; consumed).

**Food reservation:** 1.8 lb credited nutritive source inputs; up to 0 lb may return as the selected catalyst. For Standard quantity without catalyst retention, add 0 lb real ration-equivalent food. Before any completion check reserve 0 lb supplementary food for full Masterwork yield and worst legal nutritive catalyst retention. This is additional to every exact ingredient. Reservation does not consume food; after the outcome/catalyst choice and before finished servings are created, incorporate only the actual required amount. Generic failure without a finished product leaves all supplement unincorporated; a specific failed product spends only its required supplement. Actual food reference is 25 cp/lb, prorated from 5 sp per 2-lb daily ration; supplier quotes and transaction rounding still apply.

**Serving and storage:** each serving contains exactly 2/3 lb food and credits 1/3 Small/Medium daily food or 1/6 Large daily food after complete consumption. Before rolling, predeclare actual output dispositions for all 1 possible servings: real compatible storage capacity or distinct present recipients ready to begin immediate ten-minute consumption, one simultaneous slot per recipient. Immediate servings commit at batch completion; an invalid immediate slot needs actual reserved storage or cannot use the exception. Existing containers count only to their real capacity. A dedicated Meal Crock is 0.5 lb empty, 2 sp, 1 quart, AC 13/HP 2; one serving gives 7/6 lb gross. No water, fuel or full Supply is supplied by this food credit. Finished-food shelf life is 24 unprotected elapsed hours.

**Flawed:** {"mode": "treat-as-Failed", "quantity": 0, "materialRecoveryPercent": 25}. Quality can change finite yield or dedicated mundane packaging durability; it does not improve meal potency. A dedicated Meal Crock first improved from maximum HP 2 to 3 gains exactly +1 current HP, preserving existing damage; an already-HP-3 crock gains neither again.

**Nutritional source map:** Honey counts as ordinary food; Flour counts as ordinary food; Fruit counts as ordinary food; Meat counts as ordinary food; Eggs counts as ordinary food; shamanic bloodstone has no credited nutritive bulk in this card.

## recipe-113 — Ascendant Stone Snack of Shamanic Bloodstone

**Source:** director-only; Cooking level 17; tier 9; Very Rare; DC 23; 120 active hours; 1 serving(s). Standard batch reference 174078 gp.

**Preserved effect:** After a 10-minute meal, gain 17 temporary hit points and advantage against being knocked prone for 1 hour. A creature can benefit from one feast at a time.

**Operational effect:** After completing and accepting this feast, offer 17 temporary HP. For 1 elapsed hour or until the parent feast ends, whichever comes first, gain advantage on an actual check or save whose direct consequence includes becoming Prone. No immunity to automatic Prone effects or benefit when standing.

**Duration:** Parent feast and its temporary HP end at the next completed beneficial Long Rest. Every rider also ends when this feast ends or is replaced. Its explicitly shorter deadline remains separate.

**Work:** Cookfire or Kitchen; Cook's utensils, Knife, Pot or pan. Mode haven; field flag false; maximum assistants 2; formula required true.

**Exact ingredients:** 4 × Fruit (component tier 9; 0.1 lb/unit; 7500 gp/unit; substrate; consumed); 5 × Herbs (component tier 9; 0.1 lb/unit; 7500 gp/unit; substrate; consumed); 3 × Butter (component tier 9; 0.1 lb/unit; 7500 gp/unit; seasoning; consumed); 5 × Vegetables (component tier 9; 0.1 lb/unit; 7500 gp/unit; substrate; consumed); 1 × shamanic bloodstone (component tier 5; 0.14 lb/unit; 582 gp/unit; catalyst; consumed); 1 × infernal marrow (component tier 3; 0.18 lb/unit; 109 gp/unit; material; consumed).

**Food reservation:** 1.2 lb credited nutritive source inputs; up to 0 lb may return as the selected catalyst. For Standard quantity without catalyst retention, add 0 lb real ration-equivalent food. Before any completion check reserve 0 lb supplementary food for full Masterwork yield and worst legal nutritive catalyst retention. This is additional to every exact ingredient. Reservation does not consume food; after the outcome/catalyst choice and before finished servings are created, incorporate only the actual required amount. Generic failure without a finished product leaves all supplement unincorporated; a specific failed product spends only its required supplement. Actual food reference is 25 cp/lb, prorated from 5 sp per 2-lb daily ration; supplier quotes and transaction rounding still apply.

**Serving and storage:** each serving contains exactly 2/3 lb food and credits 1/3 Small/Medium daily food or 1/6 Large daily food after complete consumption. Before rolling, predeclare actual output dispositions for all 1 possible servings: real compatible storage capacity or distinct present recipients ready to begin immediate ten-minute consumption, one simultaneous slot per recipient. Immediate servings commit at batch completion; an invalid immediate slot needs actual reserved storage or cannot use the exception. Existing containers count only to their real capacity. A dedicated Meal Crock is 0.5 lb empty, 2 sp, 1 quart, AC 13/HP 2; one serving gives 7/6 lb gross. No water, fuel or full Supply is supplied by this food credit. Finished-food shelf life is 24 unprotected elapsed hours.

**Flawed:** {"mode": "treat-as-Failed", "quantity": 0, "materialRecoveryPercent": 25}. Quality can change finite yield or dedicated mundane packaging durability; it does not improve meal potency. A dedicated Meal Crock first improved from maximum HP 2 to 3 gains exactly +1 current HP, preserving existing damage; an already-HP-3 crock gains neither again.

**Nutritional source map:** Fruit counts as ordinary food; Herbs has no credited nutritive bulk in this card; Butter counts as ordinary food; Vegetables counts as ordinary food; shamanic bloodstone has no credited nutritive bulk in this card; infernal marrow has no credited nutritive bulk in this card.

## recipe-114 — Mythic Frost Meal of Sea Sinew

**Source:** director-only; Cooking level 15; tier 8; Very Rare; DC 23; 160 active hours; 1 serving(s). Standard batch reference 66298 gp.

**Preserved effect:** After a 10-minute meal, gain 16 temporary hit points and resistance to cold damage for 1 hour. A creature can benefit from one feast at a time.

**Operational effect:** After completing and accepting this feast, offer 16 temporary HP. Gain resistance to cold damage for 1 elapsed hour(s), ending earlier with the parent feast.

**Duration:** Parent feast and its temporary HP end at the next completed beneficial Long Rest. Every rider also ends when this feast ends or is replaced. Its explicitly shorter deadline remains separate.

**Work:** Cookfire or Kitchen; Cook's utensils, Knife, Pot or pan. Mode haven; field flag false; maximum assistants 1; formula required true.

**Exact ingredients:** 5 × Salt (component tier 8; 0.1 lb/unit; 3000 gp/unit; seasoning; consumed); 3 × Milk (component tier 8; 0.5 lb/unit; 3000 gp/unit; substrate; consumed); 3 × Water (component tier 8; 0.5 lb/unit; 3000 gp/unit; solvent; consumed); 5 × Wine (component tier 8; 0.5 lb/unit; 3000 gp/unit; seasoning; consumed); 1 × Sea sinew (component tier 3; 0.29 lb/unit; 126 gp/unit; material; consumed); 1 × Triceratops sinew (component tier 3; 0.3 lb/unit; 95 gp/unit; material; consumed).

**Food reservation:** 1.5 lb credited nutritive source inputs; up to 0 lb may return as the selected catalyst. For Standard quantity without catalyst retention, add 0 lb real ration-equivalent food. Before any completion check reserve 0 lb supplementary food for full Masterwork yield and worst legal nutritive catalyst retention. This is additional to every exact ingredient. Reservation does not consume food; after the outcome/catalyst choice and before finished servings are created, incorporate only the actual required amount. Generic failure without a finished product leaves all supplement unincorporated; a specific failed product spends only its required supplement. Actual food reference is 25 cp/lb, prorated from 5 sp per 2-lb daily ration; supplier quotes and transaction rounding still apply.

**Serving and storage:** each serving contains exactly 2/3 lb food and credits 1/3 Small/Medium daily food or 1/6 Large daily food after complete consumption. Before rolling, predeclare actual output dispositions for all 1 possible servings: real compatible storage capacity or distinct present recipients ready to begin immediate ten-minute consumption, one simultaneous slot per recipient. Immediate servings commit at batch completion; an invalid immediate slot needs actual reserved storage or cannot use the exception. Existing containers count only to their real capacity. A dedicated Meal Crock is 0.5 lb empty, 2 sp, 1 quart, AC 13/HP 2; one serving gives 7/6 lb gross. No water, fuel or full Supply is supplied by this food credit. Finished-food shelf life is 24 unprotected elapsed hours.

**Flawed:** {"mode": "treat-as-Failed", "quantity": 0, "materialRecoveryPercent": 25}. Quality can change finite yield or dedicated mundane packaging durability; it does not improve meal potency. A dedicated Meal Crock first improved from maximum HP 2 to 3 gains exactly +1 current HP, preserving existing damage; an already-HP-3 crock gains neither again.

**Nutritional source map:** Salt has no credited nutritive bulk in this card; Milk counts as ordinary food; Water has no credited nutritive bulk in this card; Wine has no credited nutritive bulk in this card; Sea sinew has no credited nutritive bulk in this card; Triceratops sinew has no credited nutritive bulk in this card.

## recipe-115 — Ascendant Veiled Meal of Void-Warped Eye

**Source:** director-only; Cooking level 18; tier 9; Very Rare; DC 23; 120 active hours; 1 serving(s). Standard batch reference 112707 gp.

**Preserved effect:** After a 10-minute meal, gain 17 temporary hit points and +2 to Stealth checks. A creature can benefit from one feast at a time.

**Operational effect:** After completing and accepting this feast, offer 17 temporary HP. Gain +2 to actual Stealth checks until the parent feast ends. No automatic Hidden state.

**Duration:** Parent feast and its temporary HP end at the next completed beneficial Long Rest. Every rider also ends when this feast ends or is replaced. Its explicitly shorter deadline remains separate.

**Work:** Cookfire or Kitchen; Cook's utensils, Knife, Pot or pan. Mode haven; field flag false; maximum assistants 2; formula required true.

**Exact ingredients:** 5 × Milk (component tier 9; 0.5 lb/unit; 7500 gp/unit; substrate; consumed); 3 × Sugar (component tier 9; 0.1 lb/unit; 7500 gp/unit; seasoning; consumed); 1 × Herbs (component tier 9; 0.1 lb/unit; 7500 gp/unit; substrate; consumed); 1 × Eggs (component tier 9; 0.1 lb/unit; 7500 gp/unit; substrate; consumed); 1 × Flour (component tier 9; 0.1 lb/unit; 7500 gp/unit; substrate; consumed); 1 × void-warped eye (component tier 3; 0.53 lb/unit; 66 gp/unit; catalyst; consumed); 1 × Vulture sinew (component tier 3; 0.28 lb/unit; 121 gp/unit; material; consumed).

**Food reservation:** 3 lb credited nutritive source inputs; up to 0 lb may return as the selected catalyst. For Standard quantity without catalyst retention, add 0 lb real ration-equivalent food. Before any completion check reserve 0 lb supplementary food for full Masterwork yield and worst legal nutritive catalyst retention. This is additional to every exact ingredient. Reservation does not consume food; after the outcome/catalyst choice and before finished servings are created, incorporate only the actual required amount. Generic failure without a finished product leaves all supplement unincorporated; a specific failed product spends only its required supplement. Actual food reference is 25 cp/lb, prorated from 5 sp per 2-lb daily ration; supplier quotes and transaction rounding still apply.

**Serving and storage:** each serving contains exactly 2/3 lb food and credits 1/3 Small/Medium daily food or 1/6 Large daily food after complete consumption. Before rolling, predeclare actual output dispositions for all 1 possible servings: real compatible storage capacity or distinct present recipients ready to begin immediate ten-minute consumption, one simultaneous slot per recipient. Immediate servings commit at batch completion; an invalid immediate slot needs actual reserved storage or cannot use the exception. Existing containers count only to their real capacity. A dedicated Meal Crock is 0.5 lb empty, 2 sp, 1 quart, AC 13/HP 2; one serving gives 7/6 lb gross. No water, fuel or full Supply is supplied by this food credit. Finished-food shelf life is 24 unprotected elapsed hours.

**Flawed:** {"mode": "treat-as-Failed", "quantity": 0, "materialRecoveryPercent": 25}. Quality can change finite yield or dedicated mundane packaging durability; it does not improve meal potency. A dedicated Meal Crock first improved from maximum HP 2 to 3 gains exactly +1 current HP, preserving existing damage; an already-HP-3 crock gains neither again.

**Nutritional source map:** Milk counts as ordinary food; Sugar counts as ordinary food; Herbs has no credited nutritive bulk in this card; Eggs counts as ordinary food; Flour counts as ordinary food; void-warped eye has no credited nutritive bulk in this card; Vulture sinew has no credited nutritive bulk in this card.

## recipe-116 — Ascendant Venom Pie of Poisonous

**Source:** director-only; Cooking level 18; tier 9; Very Rare; DC 20; 160 active hours; 1 serving(s). Standard batch reference 174406 gp.

**Preserved effect:** After a 10-minute meal, gain 17 temporary hit points and advantage on saves against poison for 4 hours. A creature can benefit from one feast at a time.

**Operational effect:** After completing and accepting this feast, offer 17 temporary HP. Gain advantage on saves against poison for 4 elapsed hours, ending earlier with the parent feast. No poison immunity, condition cure or damage resistance.

**Duration:** Parent feast and its temporary HP end at the next completed beneficial Long Rest. Every rider also ends when this feast ends or is replaced. Its explicitly shorter deadline remains separate.

**Work:** Cookfire or Kitchen; Cook's utensils, Knife, Pot or pan. Mode haven; field flag false; maximum assistants 2; formula required true.

**Exact ingredients:** 2 × Honey (component tier 9; 0.1 lb/unit; 7500 gp/unit; seasoning; consumed); 4 × Spices (component tier 9; 0.1 lb/unit; 7500 gp/unit; seasoning; consumed); 4 × Oil (component tier 9; 0.5 lb/unit; 7500 gp/unit; solvent; consumed); 3 × Water (component tier 9; 0.5 lb/unit; 7500 gp/unit; solvent; consumed); 4 × Wine (component tier 9; 0.5 lb/unit; 7500 gp/unit; seasoning; consumed); 1 × alpha Poisonous trophy (component tier 5; 0.1 lb/unit; 557 gp/unit; catalyst; consumed); 1 × Poisonous sinew (component tier 3; 0.38 lb/unit; 66 gp/unit; catalyst; consumed).

**Food reservation:** 2.2 lb credited nutritive source inputs; up to 0 lb may return as the selected catalyst. For Standard quantity without catalyst retention, add 0 lb real ration-equivalent food. Before any completion check reserve 0 lb supplementary food for full Masterwork yield and worst legal nutritive catalyst retention. This is additional to every exact ingredient. Reservation does not consume food; after the outcome/catalyst choice and before finished servings are created, incorporate only the actual required amount. Generic failure without a finished product leaves all supplement unincorporated; a specific failed product spends only its required supplement. Actual food reference is 25 cp/lb, prorated from 5 sp per 2-lb daily ration; supplier quotes and transaction rounding still apply.

**Serving and storage:** each serving contains exactly 2/3 lb food and credits 1/3 Small/Medium daily food or 1/6 Large daily food after complete consumption. Before rolling, predeclare actual output dispositions for all 1 possible servings: real compatible storage capacity or distinct present recipients ready to begin immediate ten-minute consumption, one simultaneous slot per recipient. Immediate servings commit at batch completion; an invalid immediate slot needs actual reserved storage or cannot use the exception. Existing containers count only to their real capacity. A dedicated Meal Crock is 0.5 lb empty, 2 sp, 1 quart, AC 13/HP 2; one serving gives 7/6 lb gross. No water, fuel or full Supply is supplied by this food credit. Finished-food shelf life is 24 unprotected elapsed hours.

**Flawed:** {"mode": "treat-as-Failed", "quantity": 0, "materialRecoveryPercent": 25}. Quality can change finite yield or dedicated mundane packaging durability; it does not improve meal potency. A dedicated Meal Crock first improved from maximum HP 2 to 3 gains exactly +1 current HP, preserving existing damage; an already-HP-3 crock gains neither again.

**Nutritional source map:** Honey counts as ordinary food; Spices has no credited nutritive bulk in this card; Oil counts as ordinary food; Water has no credited nutritive bulk in this card; Wine has no credited nutritive bulk in this card; alpha Poisonous trophy has no credited nutritive bulk in this card; Poisonous sinew has no credited nutritive bulk in this card.

## recipe-117 — Ascendant Gale Meal of Eagle Sinew

**Source:** director-only; Cooking level 18; tier 9; Legendary; DC 23; 480 active hours; 1 serving(s). Standard batch reference 105917 gp.

**Preserved effect:** After a 10-minute meal, gain 19 temporary hit points and +10 feet movement speed for 1 hour. A creature can benefit from one feast at a time.

**Operational effect:** After completing and accepting this feast, offer 19 temporary HP. Increase walking speed by 10 feet for 1 elapsed hour or until the parent feast ends, whichever comes first. Other movement modes change only if their own rule derives them from walking speed.

**Duration:** Parent feast and its temporary HP end at the next completed beneficial Long Rest. Every rider also ends when this feast ends or is replaced. Its explicitly shorter deadline remains separate.

**Work:** Cookfire or Kitchen; Cook's utensils, Knife, Pot or pan. Mode legacy; field flag false; maximum assistants 2; formula required true.

**Exact ingredients:** 2 × Sugar (component tier 9; 0.1 lb/unit; 7500 gp/unit; seasoning; consumed); 1 × Meat (component tier 9; 0.1 lb/unit; 7500 gp/unit; substrate; consumed); 3 × Butter (component tier 9; 0.1 lb/unit; 7500 gp/unit; seasoning; consumed); 2 × Oil (component tier 9; 0.5 lb/unit; 7500 gp/unit; solvent; consumed); 2 × Milk (component tier 9; 0.5 lb/unit; 7500 gp/unit; substrate; consumed); 1 × Eagle sinew (component tier 3; 0.28 lb/unit; 136 gp/unit; material; consumed); 1 × Vulture sinew (component tier 3; 0.28 lb/unit; 121 gp/unit; material; consumed).

**Food reservation:** 2.6 lb credited nutritive source inputs; up to 0 lb may return as the selected catalyst. For Standard quantity without catalyst retention, add 0 lb real ration-equivalent food. Before any completion check reserve 0 lb supplementary food for full Masterwork yield and worst legal nutritive catalyst retention. This is additional to every exact ingredient. Reservation does not consume food; after the outcome/catalyst choice and before finished servings are created, incorporate only the actual required amount. Generic failure without a finished product leaves all supplement unincorporated; a specific failed product spends only its required supplement. Actual food reference is 25 cp/lb, prorated from 5 sp per 2-lb daily ration; supplier quotes and transaction rounding still apply.

**Serving and storage:** each serving contains exactly 2/3 lb food and credits 1/3 Small/Medium daily food or 1/6 Large daily food after complete consumption. Before rolling, predeclare actual output dispositions for all 1 possible servings: real compatible storage capacity or distinct present recipients ready to begin immediate ten-minute consumption, one simultaneous slot per recipient. Immediate servings commit at batch completion; an invalid immediate slot needs actual reserved storage or cannot use the exception. Existing containers count only to their real capacity. A dedicated Meal Crock is 0.5 lb empty, 2 sp, 1 quart, AC 13/HP 2; one serving gives 7/6 lb gross. No water, fuel or full Supply is supplied by this food credit. Finished-food shelf life is 24 unprotected elapsed hours.

**Flawed:** {"mode": "treat-as-Failed", "quantity": 0, "materialRecoveryPercent": 25}. Quality can change finite yield or dedicated mundane packaging durability; it does not improve meal potency. A dedicated Meal Crock first improved from maximum HP 2 to 3 gains exactly +1 current HP, preserving existing damage; an already-HP-3 crock gains neither again.

**Nutritional source map:** Sugar counts as ordinary food; Meat counts as ordinary food; Butter counts as ordinary food; Oil counts as ordinary food; Milk counts as ordinary food; Eagle sinew has no credited nutritive bulk in this card; Vulture sinew has no credited nutritive bulk in this card.

## recipe-118 — Ascendant Mighty Meal of Sea Sinew

**Source:** director-only; Cooking level 18; tier 9; Legendary; DC 23; 480 active hours; 1 serving(s). Standard batch reference 146331 gp.

**Preserved effect:** After a 10-minute meal, gain 19 temporary hit points and +3 to Athletics checks. A creature can benefit from one feast at a time.

**Operational effect:** After completing and accepting this feast, offer 19 temporary HP. Gain +3 to actual Athletics checks until the parent feast ends.

**Duration:** Parent feast and its temporary HP end at the next completed beneficial Long Rest. Every rider also ends when this feast ends or is replaced. Its explicitly shorter deadline remains separate.

**Work:** Cookfire or Kitchen; Cook's utensils, Knife, Pot or pan. Mode legacy; field flag false; maximum assistants 2; formula required true.

**Exact ingredients:** 4 × Fruit (component tier 9; 0.1 lb/unit; 7500 gp/unit; substrate; consumed); 2 × Honey (component tier 9; 0.1 lb/unit; 7500 gp/unit; seasoning; consumed); 1 × Meat (component tier 9; 0.1 lb/unit; 7500 gp/unit; substrate; consumed); 5 × Water (component tier 9; 0.5 lb/unit; 7500 gp/unit; solvent; consumed); 2 × Butter (component tier 9; 0.1 lb/unit; 7500 gp/unit; seasoning; consumed); 1 × Sea sinew (component tier 3; 0.29 lb/unit; 126 gp/unit; material; consumed); 1 × Dolphin sinew (component tier 3; 0.33 lb/unit; 67 gp/unit; material; consumed).

**Food reservation:** 0.9 lb credited nutritive source inputs; up to 0 lb may return as the selected catalyst. For Standard quantity without catalyst retention, add 0 lb real ration-equivalent food. Before any completion check reserve 0 lb supplementary food for full Masterwork yield and worst legal nutritive catalyst retention. This is additional to every exact ingredient. Reservation does not consume food; after the outcome/catalyst choice and before finished servings are created, incorporate only the actual required amount. Generic failure without a finished product leaves all supplement unincorporated; a specific failed product spends only its required supplement. Actual food reference is 25 cp/lb, prorated from 5 sp per 2-lb daily ration; supplier quotes and transaction rounding still apply.

**Serving and storage:** each serving contains exactly 2/3 lb food and credits 1/3 Small/Medium daily food or 1/6 Large daily food after complete consumption. Before rolling, predeclare actual output dispositions for all 1 possible servings: real compatible storage capacity or distinct present recipients ready to begin immediate ten-minute consumption, one simultaneous slot per recipient. Immediate servings commit at batch completion; an invalid immediate slot needs actual reserved storage or cannot use the exception. Existing containers count only to their real capacity. A dedicated Meal Crock is 0.5 lb empty, 2 sp, 1 quart, AC 13/HP 2; one serving gives 7/6 lb gross. No water, fuel or full Supply is supplied by this food credit. Finished-food shelf life is 24 unprotected elapsed hours.

**Flawed:** {"mode": "treat-as-Failed", "quantity": 0, "materialRecoveryPercent": 25}. Quality can change finite yield or dedicated mundane packaging durability; it does not improve meal potency. A dedicated Meal Crock first improved from maximum HP 2 to 3 gains exactly +1 current HP, preserving existing damage; an already-HP-3 crock gains neither again.

**Nutritional source map:** Fruit counts as ordinary food; Honey counts as ordinary food; Meat counts as ordinary food; Water has no credited nutritive bulk in this card; Butter counts as ordinary food; Sea sinew has no credited nutritive bulk in this card; Dolphin sinew has no credited nutritive bulk in this card.

## recipe-119 — Transcendent Grave Meal of Poisonous

**Source:** director-only; Cooking level 19; tier 10; Legendary; DC 24; 480 active hours; 1 serving(s). Standard batch reference 491401 gp.

**Preserved effect:** After a 10-minute meal, gain 20 temporary hit points and resistance to necrotic damage for 1 hour. A creature can benefit from one feast at a time.

**Operational effect:** After completing and accepting this feast, offer 20 temporary HP. Gain resistance to necrotic damage for 1 elapsed hour(s), ending earlier with the parent feast.

**Duration:** Parent feast and its temporary HP end at the next completed beneficial Long Rest. Every rider also ends when this feast ends or is replaced. Its explicitly shorter deadline remains separate.

**Work:** Cookfire or Kitchen; Cook's utensils, Knife, Pot or pan. Mode legacy; field flag false; maximum assistants 2; formula required true.

**Exact ingredients:** 2 × Salt (component tier 10; 0.1 lb/unit; 18000 gp/unit; seasoning; consumed); 5 × Spices (component tier 10; 0.1 lb/unit; 18000 gp/unit; seasoning; consumed); 5 × Vegetables (component tier 10; 0.1 lb/unit; 18000 gp/unit; substrate; consumed); 2 × Honey (component tier 10; 0.1 lb/unit; 18000 gp/unit; seasoning; consumed); 3 × Oil (component tier 10; 0.5 lb/unit; 18000 gp/unit; solvent; consumed); 3 × Butter (component tier 10; 0.1 lb/unit; 18000 gp/unit; seasoning; consumed); 1 × alpha Poisonous trophy (component tier 5; 0.1 lb/unit; 557 gp/unit; catalyst; consumed); 1 × Poisonous sinew (component tier 3; 0.38 lb/unit; 66 gp/unit; catalyst; consumed).

**Food reservation:** 2.5 lb credited nutritive source inputs; up to 0 lb may return as the selected catalyst. For Standard quantity without catalyst retention, add 0 lb real ration-equivalent food. Before any completion check reserve 0 lb supplementary food for full Masterwork yield and worst legal nutritive catalyst retention. This is additional to every exact ingredient. Reservation does not consume food; after the outcome/catalyst choice and before finished servings are created, incorporate only the actual required amount. Generic failure without a finished product leaves all supplement unincorporated; a specific failed product spends only its required supplement. Actual food reference is 25 cp/lb, prorated from 5 sp per 2-lb daily ration; supplier quotes and transaction rounding still apply.

**Serving and storage:** each serving contains exactly 2/3 lb food and credits 1/3 Small/Medium daily food or 1/6 Large daily food after complete consumption. Before rolling, predeclare actual output dispositions for all 1 possible servings: real compatible storage capacity or distinct present recipients ready to begin immediate ten-minute consumption, one simultaneous slot per recipient. Immediate servings commit at batch completion; an invalid immediate slot needs actual reserved storage or cannot use the exception. Existing containers count only to their real capacity. A dedicated Meal Crock is 0.5 lb empty, 2 sp, 1 quart, AC 13/HP 2; one serving gives 7/6 lb gross. No water, fuel or full Supply is supplied by this food credit. Finished-food shelf life is 24 unprotected elapsed hours.

**Flawed:** {"mode": "treat-as-Failed", "quantity": 0, "materialRecoveryPercent": 25}. Quality can change finite yield or dedicated mundane packaging durability; it does not improve meal potency. A dedicated Meal Crock first improved from maximum HP 2 to 3 gains exactly +1 current HP, preserving existing damage; an already-HP-3 crock gains neither again.

**Nutritional source map:** Salt has no credited nutritive bulk in this card; Spices has no credited nutritive bulk in this card; Vegetables counts as ordinary food; Honey counts as ordinary food; Oil counts as ordinary food; Butter counts as ordinary food; alpha Poisonous trophy has no credited nutritive bulk in this card; Poisonous sinew has no credited nutritive bulk in this card.

## recipe-120 — Transcendent Stone Stew of Shamanic Bloodstone

**Source:** director-only; Cooking level 20; tier 10; Mythic; DC 28; source crafting time 1 year; source active-work hours unspecified/null; 1 serving. Standard batch reference 439171 gp.

**Operational work overlay:** 1 workyear = 1,920 active hours under the reviewed work-year rule.

**Preserved effect:** After a 10-minute meal, gain 22 temporary hit points and advantage against being knocked prone for 1 hour. A creature can benefit from one feast at a time.

**Operational effect:** After completing and accepting this feast, offer 22 temporary HP. For 1 elapsed hour or until the parent feast ends, whichever comes first, gain advantage on an actual check or save whose direct consequence includes becoming Prone. No immunity to automatic Prone effects or benefit when standing.

**Duration:** Parent feast and its temporary HP end at the next completed beneficial Long Rest. Every rider also ends when this feast ends or is replaced. Its explicitly shorter deadline remains separate.

**Work:** Cookfire or Kitchen; Cook's utensils, Knife, Pot or pan. Mode special; field flag false; maximum assistants 3; formula required true.

**Exact ingredients:** 1 × Vegetables (component tier 10; 0.1 lb/unit; 18000 gp/unit; substrate; consumed); 4 × Milk (component tier 10; 0.5 lb/unit; 18000 gp/unit; substrate; consumed); 1 × Flour (component tier 10; 0.1 lb/unit; 18000 gp/unit; substrate; consumed); 5 × Salt (component tier 10; 0.1 lb/unit; 18000 gp/unit; seasoning; consumed); 2 × Oil (component tier 10; 0.5 lb/unit; 18000 gp/unit; solvent; consumed); 5 × Eggs (component tier 10; 0.1 lb/unit; 18000 gp/unit; substrate; consumed); 1 × shamanic bloodstone (component tier 5; 0.14 lb/unit; 582 gp/unit; catalyst; consumed); 1 × Fire sinew (component tier 3; 0.25 lb/unit; 148 gp/unit; material; consumed); 1 × shamanic bloodstone (component tier 5; 0.14 lb/unit; 582 gp/unit; catalyst; consumed).

**Food reservation:** 3.7 lb credited nutritive source inputs; up to 0 lb may return as the selected catalyst. For Standard quantity without catalyst retention, add 0 lb real ration-equivalent food. Before any completion check reserve 0 lb supplementary food for full Masterwork yield and worst legal nutritive catalyst retention. This is additional to every exact ingredient. Reservation does not consume food; after the outcome/catalyst choice and before finished servings are created, incorporate only the actual required amount. Generic failure without a finished product leaves all supplement unincorporated; a specific failed product spends only its required supplement. Actual food reference is 25 cp/lb, prorated from 5 sp per 2-lb daily ration; supplier quotes and transaction rounding still apply.

**Serving and storage:** each serving contains exactly 2/3 lb food and credits 1/3 Small/Medium daily food or 1/6 Large daily food after complete consumption. Before rolling, predeclare actual output dispositions for all 1 possible servings: real compatible storage capacity or distinct present recipients ready to begin immediate ten-minute consumption, one simultaneous slot per recipient. Immediate servings commit at batch completion; an invalid immediate slot needs actual reserved storage or cannot use the exception. Existing containers count only to their real capacity. A dedicated Meal Crock is 0.5 lb empty, 2 sp, 1 quart, AC 13/HP 2; one serving gives 7/6 lb gross. No water, fuel or full Supply is supplied by this food credit. Finished-food shelf life is 24 unprotected elapsed hours.

**Flawed:** {"mode": "treat-as-Failed", "quantity": 0, "materialRecoveryPercent": 25}. Quality can change finite yield or dedicated mundane packaging durability; it does not improve meal potency. A dedicated Meal Crock first improved from maximum HP 2 to 3 gains exactly +1 current HP, preserving existing damage; an already-HP-3 crock gains neither again.

**Nutritional source map:** Vegetables counts as ordinary food; Milk counts as ordinary food; Flour counts as ordinary food; Salt has no credited nutritive bulk in this card; Oil counts as ordinary food; Eggs counts as ordinary food; shamanic bloodstone has no credited nutritive bulk in this card; Fire sinew has no credited nutritive bulk in this card; shamanic bloodstone has no credited nutritive bulk in this card.

**Work-year binding:** source active hours remain null; this card uses the reviewed 1,920-active-hour work-year overlay. Actual eligible artisan time reduction applies to that work without changing the source.

## recipe-632 — Bear-Marrow Expedition Stew

**Source:** public; Cooking level 5; tier 3; Uncommon; DC 13; 8 active hours; 1 serving(s). Standard batch reference 186 gp.

**Preserved effect:** After a 10-minute meal, gain 7 temporary hit points and +1 to Athletics checks. Because it combines multiple parts of one creature or ecology, a critical success also grants one temporary trait associated with the source monster. A creature can benefit from one feast at a time.

**Operational effect:** After completing and accepting this feast, offer 7 temporary HP. Gain +1 to actual Athletics checks until the parent feast ends. On an actual Masterwork craft, also grant the single approved donor trait fixed before work, for 1 hour or until this feast ends. Verified same-creature/shared-ecology provenance and an eligible donor profile are prerequisites to starting this recipe; see the shared procedure.

**Duration:** Parent feast and its temporary HP end at the next completed beneficial Long Rest. Every rider also ends when this feast ends or is replaced. Its explicitly shorter deadline remains separate.

**Work:** Cookfire or Kitchen; Cook's utensils, Knife, Pot or pan. Mode expedition; field flag true; maximum assistants 0; formula required true.

**Exact ingredients:** 1 × Bear meat (component tier 1; 0.14 lb/unit; 7 gp/unit; material; consumed); 1 × Bear bone shard (component tier 2; 0.27 lb/unit; 29 gp/unit; material; consumed); 1 × Water (component tier 3; 0.5 lb/unit; 25 gp/unit; solvent; consumed); 1 × Salt (component tier 3; 0.1 lb/unit; 25 gp/unit; seasoning; consumed); 1 × Vegetables (component tier 3; 0.1 lb/unit; 25 gp/unit; substrate; consumed).

**Food reservation:** 0.24 lb credited nutritive source inputs; up to 0 lb may return as the selected catalyst. For Standard quantity without catalyst retention, add 0.43 lb real ration-equivalent food. Before any completion check reserve 0.43 lb supplementary food for full Masterwork yield and worst legal nutritive catalyst retention. This is additional to every exact ingredient. Reservation does not consume food; after the outcome/catalyst choice and before finished servings are created, incorporate only the actual required amount. Generic failure without a finished product leaves all supplement unincorporated; a specific failed product spends only its required supplement. Actual food reference is 25 cp/lb, prorated from 5 sp per 2-lb daily ration; supplier quotes and transaction rounding still apply.

**Serving and storage:** each serving contains exactly 2/3 lb food and credits 1/3 Small/Medium daily food or 1/6 Large daily food after complete consumption. Before rolling, predeclare actual output dispositions for all 1 possible servings: real compatible storage capacity or distinct present recipients ready to begin immediate ten-minute consumption, one simultaneous slot per recipient. Immediate servings commit at batch completion; an invalid immediate slot needs actual reserved storage or cannot use the exception. Existing containers count only to their real capacity. A dedicated Meal Crock is 0.5 lb empty, 2 sp, 1 quart, AC 13/HP 2; one serving gives 7/6 lb gross. No water, fuel or full Supply is supplied by this food credit. Finished-food shelf life is 24 unprotected elapsed hours.

**Flawed:** {"mode": "treat-as-Failed", "quantity": 0, "materialRecoveryPercent": 25}. Quality can change finite yield or dedicated mundane packaging durability; it does not improve meal potency. A dedicated Meal Crock first improved from maximum HP 2 to 3 gains exactly +1 current HP, preserving existing damage; an already-HP-3 crock gains neither again.

**Nutritional source map:** Bear meat counts as ordinary food; Bear bone shard has no credited nutritive bulk in this card; Water has no credited nutritive bulk in this card; Salt has no credited nutritive bulk in this card; Vegetables counts as ordinary food.

**Required donor record:** record actual donors for every monster-part lot, the same-creature/shared-ecology evidence, the one donor supplying a consumed component, and its approved eligible trait before starting work. No eligible profile means this work order cannot begin. On actual Masterwork, the fixed trait accompanies the normal quality choice for one hour or until the feast ends. No post-roll choice or fallback power.

## recipe-633 — Neutralized Serpent Skewers

**Source:** public; Cooking level 8; tier 5; Rare; DC 16; 16 active hours; 1 serving(s). Standard batch reference 1084 gp.

**Preserved effect:** After a 10-minute meal, gain 6 temporary hit points and advantage on saves against poison for 8 hours. On a failed crafting check, the meal remains poisonous.

**Operational effect:** After completing and accepting this feast, offer 6 temporary HP. Gain advantage on saves against poison for 8 elapsed hours, ending earlier with the parent feast. No poison immunity, condition cure or damage resistance.

**Duration:** Entire successful feast and its temporary HP last eight elapsed hours, including through a Long Rest. Every rider also ends when this feast ends or is replaced. Its explicitly shorter deadline remains separate.

**Work:** Cookfire or Kitchen; Cook's utensils, Knife, Pot or pan. Mode workshop; field flag false; maximum assistants 0; formula required true.

**Exact ingredients:** 1 × Poisonous meat (component tier 1; 0.38 lb/unit; 14 gp/unit; material; consumed); 1 × Poisonous sinew (component tier 3; 0.38 lb/unit; 66 gp/unit; material; consumed); 1 × Salt (component tier 5; 0.1 lb/unit; 200 gp/unit; seasoning; consumed); 1 × Spices (component tier 5; 0.1 lb/unit; 200 gp/unit; seasoning; consumed); 1 × Oil (component tier 5; 0.5 lb/unit; 200 gp/unit; solvent; consumed).

**Food reservation:** 0.88 lb credited nutritive source inputs; up to 0 lb may return as the selected catalyst. For Standard quantity without catalyst retention, add 0 lb real ration-equivalent food. Before any completion check reserve 0 lb supplementary food for full Masterwork yield and worst legal nutritive catalyst retention. This is additional to every exact ingredient. Reservation does not consume food; after the outcome/catalyst choice and before finished servings are created, incorporate only the actual required amount. Generic failure without a finished product leaves all supplement unincorporated; a specific failed product spends only its required supplement. Actual food reference is 25 cp/lb, prorated from 5 sp per 2-lb daily ration; supplier quotes and transaction rounding still apply.

**Serving and storage:** each serving contains exactly 2/3 lb food and credits 1/3 Small/Medium daily food or 1/6 Large daily food after complete consumption. Before rolling, predeclare actual output dispositions for all 1 possible servings: real compatible storage capacity or distinct present recipients ready to begin immediate ten-minute consumption, one simultaneous slot per recipient. Immediate servings commit at batch completion; an invalid immediate slot needs actual reserved storage or cannot use the exception. Existing containers count only to their real capacity. A dedicated Meal Crock is 0.5 lb empty, 2 sp, 1 quart, AC 13/HP 2; one serving gives 7/6 lb gross. No water, fuel or full Supply is supplied by this food credit. Finished-food shelf life is 24 unprotected elapsed hours.

**Flawed:** {"mode": "contaminated-serving", "quantity": 1, "materialRecoveryPercent": 0}. Quality can change finite yield or dedicated mundane packaging durability; it does not improve meal potency. A dedicated Meal Crock first improved from maximum HP 2 to 3 gains exactly +1 current HP, preserving existing damage; an already-HP-3 crock gains neither again.

**Nutritional source map:** Poisonous meat counts as ordinary food; Poisonous sinew has no credited nutritive bulk in this card; Salt has no credited nutritive bulk in this card; Spices has no credited nutritive bulk in this card; Oil counts as ordinary food.

**Contaminated failure:** any total below DC, or Mishap/natural 1, creates one contaminated serving with no feast magic and no material recovery. Mishap also applies normally. Full ten-minute consumption gives ordinary food credit and a DC 13 CON save; failure causes Poisoned for one elapsed hour, success no condition. It does not replace an existing feast. No damage, partial-dose poison, coating or guaranteed sale value.

## recipe-634 — Legendary Blood Sausage

**Source:** director-only; Cooking level 20; tier 10; Mythic; DC 28; 480 active hours; 1 serving(s). Standard batch reference 90972 gp.

**Preserved effect:** After a 10-minute meal, gain 22 temporary hit points and +3 to Constitution saves. Because it combines multiple parts of one creature or ecology, a critical success also grants one temporary trait associated with the source monster. A creature can benefit from one feast at a time.

**Operational effect:** After completing and accepting this feast, offer 22 temporary HP. Gain +3 to actual Constitution saving throws until the parent feast ends, including concentration and Wound/Injury saves when they are CON saves. Other roll types are not converted. On an actual Masterwork craft, also grant the single approved donor trait fixed before work, for 1 hour or until this feast ends. Verified same-creature/shared-ecology provenance and an eligible donor profile are prerequisites to starting this recipe; see the shared procedure.

**Duration:** Parent feast and its temporary HP end at the next completed beneficial Long Rest. Every rider also ends when this feast ends or is replaced. Its explicitly shorter deadline remains separate.

**Work:** Cookfire or Kitchen; Cook's utensils, Knife, Pot or pan. Mode legacy; field flag false; maximum assistants 3; formula required true.

**Exact ingredients:** 1 × legendary beast blood (component tier 6; 0.01 lb/unit; 1622 gp/unit; material; consumed); 1 × chieftain's marrow (component tier 6; 0.08 lb/unit; 1826 gp/unit; material; consumed); 1 × Salt (component tier 10; 0.1 lb/unit; 18000 gp/unit; seasoning; consumed); 1 × Spices (component tier 10; 0.1 lb/unit; 18000 gp/unit; seasoning; consumed); 1 × Herbs (component tier 10; 0.1 lb/unit; 18000 gp/unit; substrate; consumed).

**Food reservation:** 0 lb credited nutritive source inputs; up to 0 lb may return as the selected catalyst. For Standard quantity without catalyst retention, add 0.67 lb real ration-equivalent food. Before any completion check reserve 0.67 lb supplementary food for full Masterwork yield and worst legal nutritive catalyst retention. This is additional to every exact ingredient. Reservation does not consume food; after the outcome/catalyst choice and before finished servings are created, incorporate only the actual required amount. Generic failure without a finished product leaves all supplement unincorporated; a specific failed product spends only its required supplement. Actual food reference is 25 cp/lb, prorated from 5 sp per 2-lb daily ration; supplier quotes and transaction rounding still apply.

**Serving and storage:** each serving contains exactly 2/3 lb food and credits 1/3 Small/Medium daily food or 1/6 Large daily food after complete consumption. Before rolling, predeclare actual output dispositions for all 1 possible servings: real compatible storage capacity or distinct present recipients ready to begin immediate ten-minute consumption, one simultaneous slot per recipient. Immediate servings commit at batch completion; an invalid immediate slot needs actual reserved storage or cannot use the exception. Existing containers count only to their real capacity. A dedicated Meal Crock is 0.5 lb empty, 2 sp, 1 quart, AC 13/HP 2; one serving gives 7/6 lb gross. No water, fuel or full Supply is supplied by this food credit. Finished-food shelf life is 24 unprotected elapsed hours.

**Flawed:** {"mode": "treat-as-Failed", "quantity": 0, "materialRecoveryPercent": 25}. Quality can change finite yield or dedicated mundane packaging durability; it does not improve meal potency. A dedicated Meal Crock first improved from maximum HP 2 to 3 gains exactly +1 current HP, preserving existing damage; an already-HP-3 crock gains neither again.

**Nutritional source map:** legendary beast blood has no credited nutritive bulk in this card; chieftain's marrow has no credited nutritive bulk in this card; Salt has no credited nutritive bulk in this card; Spices has no credited nutritive bulk in this card; Herbs has no credited nutritive bulk in this card.

**Required donor record:** record actual donors for every monster-part lot, the same-creature/shared-ecology evidence, the one donor supplying a consumed component, and its approved eligible trait before starting work. No eligible profile means this work order cannot begin. On actual Masterwork, the fixed trait accompanies the normal quality choice for one hour or until the feast ends. No post-roll choice or fallback power.

## recipe-635 — Living-Root Fey Dumplings

**Source:** public; Cooking level 2; tier 1; Common; DC 10; 2 active hours; 1 serving(s). Standard batch reference 42 gp.

**Preserved effect:** After a 10-minute meal, gain 3 temporary hit points and advantage on saves against poison and disease. Because it combines multiple parts of one creature or ecology, a critical success also grants one temporary trait associated with the source monster. A creature can benefit from one feast at a time.

**Operational effect:** After completing and accepting this feast, offer 3 temporary HP. Gain advantage on saves against poison and disease until the parent feast ends. No automatic condition cure or immunity. On an actual Masterwork craft, also grant the single approved donor trait fixed before work, for 1 hour or until this feast ends. Verified same-creature/shared-ecology provenance and an eligible donor profile are prerequisites to starting this recipe; see the shared procedure.

**Duration:** Parent feast and its temporary HP end at the next completed beneficial Long Rest. Every rider also ends when this feast ends or is replaced. Its explicitly shorter deadline remains separate.

**Work:** Cookfire or Kitchen; Cook's utensils, Knife, Pot or pan. Mode field; field flag true; maximum assistants 0; formula required false.

**Exact ingredients:** 1 × living root (component tier 1; 0.29 lb/unit; 12 gp/unit; material; consumed); 1 × fey pollen (component tier 1; 0.83 lb/unit; 9 gp/unit; material; consumed); 1 × Flour (component tier 1; 0.1 lb/unit; 2 gp/unit; substrate; consumed); 1 × Butter (component tier 1; 0.1 lb/unit; 2 gp/unit; seasoning; consumed); 1 × Herbs (component tier 1; 0.1 lb/unit; 2 gp/unit; substrate; consumed).

**Food reservation:** 0.2 lb credited nutritive source inputs; up to 0 lb may return as the selected catalyst. For Standard quantity without catalyst retention, add 0.47 lb real ration-equivalent food. Before any completion check reserve 0.47 lb supplementary food for full Masterwork yield and worst legal nutritive catalyst retention. This is additional to every exact ingredient. Reservation does not consume food; after the outcome/catalyst choice and before finished servings are created, incorporate only the actual required amount. Generic failure without a finished product leaves all supplement unincorporated; a specific failed product spends only its required supplement. Actual food reference is 25 cp/lb, prorated from 5 sp per 2-lb daily ration; supplier quotes and transaction rounding still apply.

**Serving and storage:** each serving contains exactly 2/3 lb food and credits 1/3 Small/Medium daily food or 1/6 Large daily food after complete consumption. Before rolling, predeclare actual output dispositions for all 1 possible servings: real compatible storage capacity or distinct present recipients ready to begin immediate ten-minute consumption, one simultaneous slot per recipient. Immediate servings commit at batch completion; an invalid immediate slot needs actual reserved storage or cannot use the exception. Existing containers count only to their real capacity. A dedicated Meal Crock is 0.5 lb empty, 2 sp, 1 quart, AC 13/HP 2; one serving gives 7/6 lb gross. No water, fuel or full Supply is supplied by this food credit. Finished-food shelf life is 24 unprotected elapsed hours.

**Flawed:** {"mode": "treat-as-Failed", "quantity": 0, "materialRecoveryPercent": 25}. Quality can change finite yield or dedicated mundane packaging durability; it does not improve meal potency. A dedicated Meal Crock first improved from maximum HP 2 to 3 gains exactly +1 current HP, preserving existing damage; an already-HP-3 crock gains neither again.

**Nutritional source map:** living root has no credited nutritive bulk in this card; fey pollen has no credited nutritive bulk in this card; Flour counts as ordinary food; Butter counts as ordinary food; Herbs has no credited nutritive bulk in this card.

**Required donor record:** record actual donors for every monster-part lot, the same-creature/shared-ecology evidence, the one donor supplying a consumed component, and its approved eligible trait before starting work. No eligible profile means this work order cannot begin. On actual Masterwork, the fixed trait accompanies the normal quality choice for one hour or until the feast ends. No post-roll choice or fallback power.
