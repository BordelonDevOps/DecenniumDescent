"""Author FL-19..26; requires the reviewed coin-fine clarification before output."""
from pathlib import Path
from datetime import datetime, timezone
from fractions import Fraction
from hashlib import sha256
import json
import re

G = Path(r'C:\Github\DecenniumDescent')
R = G / 'DescentReviewChanges/ReviewBible'
A = G / 'docs/audit/2026-10-08/full-game'
P = A / 'ex58-final-gpt-verdict'

def read(p): return json.loads(p.read_text('utf-8-sig'))
def info(p):
    b = p.read_bytes()
    return {'bytes': len(b), 'sha256': sha256(b).hexdigest()}
def save(p, d):
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(d, ensure_ascii=False, indent=2) + '\n', encoding='utf8', newline='\n')

SECTIONS = []
def section(i, title, player, director): SECTIONS.append({'id': f'FL-{i:02d}', 'title': title, 'player': player, 'director': director})

section(19, 'Arriving at Haven',
'''Use this order for a full return: **inspection/quarantine → provenance → appraisal → claims/liens → disposition → settlement → recovery → standing → advancement → next descent**.

A Tier-I return may use inspection → appraisal → sale → sponsor settlement → recovery only when every arriving lot qualifies and there is no disputed ownership, strategic cargo, lien, quarantine issue, contraband or faction hearing. The shorter route removes redundant administrative passes. It does not waive taxes, title, actual fees, care, unknown hazards or later standing/advancement records. A discovered disqualifier moves the same return to the full process, keeping work and charges already completed.

| Ordinary work | Active time and unit |
|---|---|
| Intake | 10 minutes per arriving Expedition, with receiving officer and representative |
| Additional flagged-lot inspection | 10 minutes per distinct homogeneous lot/assembly |
| Provenance, including an uncontested claim check | 30 minutes per title/evidence dossier |
| Appraisal | 30 minutes per item or previously constituted homogeneous lot |
| Ordinary disputed-claim hearing | 2 hours with actual parties, evidence and authorized adjudicator |
| Buyer negotiation/disposition | 30 minutes per coherent offered bill |
| Ledger/sponsor settlement | 30 minutes per Expedition bill |
| Standing notification | 10 minutes when needed |
| Advancement record | 10 minutes when needed |
| Next-charter planning | 60 minutes |

Real waiting for staff, evidence or authority adds elapsed time. Independently staffed desks can work on separate lots, but one representative cannot fully participate in incompatible simultaneous tasks. Handing over a completed document uses actual handling time rather than automatically repeating its full review. Exact specialist, identification, emergency or hearing procedures keep their own requirements.

Routine intake and uncontested bookkeeping need no roll. For uncertain appraisal, declare the appropriate INT skill—Arcana, History, Nature, Religion, Engineering or Investigation—or applicable craft tool and method. Add one proficiency where actually applicable; ordinary appraisal has no universal trained-only gate. Use the item's assessment DC, or its actual material-tier DC: I 12, II 13, III 15, IV 16, V 18, VI 19. One knowledgeable helper can provide ordinary Help under the social procedure; do not also add the generic expedition +3.

Success gives reliable conclusions supported by that method/evidence and a valuation in the correct domain. A critical adds the declared extra supported detail or access to a real alternative buyer. Failure leaves only established broad facts and unresolved value. A predeclared critical-failure stake can produce a fallible report, never change the object's real identity. Testing consumes a sample only when declared and actually debited. Rotating appraisers over unchanged evidence does not create fresh checks.

Identification, translation, title evidence, safe containment and a buyer's offer are distinct. Quarantine records an authorized institution's actual custody/location/access restriction; it neither destroys nor cleanses the item. Paid secure storage cannot substitute for an active core's specific containment.''',
'''Record intake arrivals, manifest, restrictions and discrepancies. Preserve completed work when interrupted unless the actual interruption invalidates it; keep paid fees, service time and material age. Unknown cargo cannot be made safe by selecting the fast route.

The governing record supplies appraisal DC even if the tier is not known to the characters. Unsupported higher-tier or exceptional objects require their actual assessment source; do not invent a DC. A skill name supplies no supernatural detection. Critical detail/buyer access must be supported and declared, not universal function, provenance, curse discovery or a guaranteed best market.

Record an appraiser's belief separately from true facts. New evidence or a genuinely different appropriate test can justify another check. A successful title search alone grants no ownership; an enchantment's identification alone grants no complete missing powers. Preserve the source references and completed procedural boundaries rather than resetting the episode when it changes administrative route.''')

section(20, 'Choose one valuation method',
'''Before pricing, identify the actual offered object and quantity, condition, custody, lawful disposition and buyer. Choose one domain: ordinary equipment, reviewed crafted item, ordinary material/trade lot, true artifact, or an unsupported/unvalued object. A grand name, rarity label, high price, ingredient or magical condition does not choose the domain.

**Ordinary equipment.** Use its actual grade/size/fitting baseline and the reviewed buyer rules. For an undamaged mundane item to which that schedule applies, the buyer's actual Honored/Liked/Neutral/Disliked/Hated relationship gives 75/60/50/40/25% of baseline; refusal remains possible. Damaged goods need a real condition-specific quote. Gems, jewelry, art and trade goods keep their particular transaction rules. Do not apply an additional Loop multiplier to an already calculated equipment price. These percentages are not magical-item buyback.

**Reviewed crafted items.** Use their exact recipe reference and sale restrictions. For the reviewed durable supplemental-body families, use the actual source-batch/Standard-Q plus approved body reference once. Final quality yield, a legacy price, all reusable capital or artifact quality do not replace that reference. Charges, flaw, damage and permitted disposition affect the actual item's quote, without an automatic scrap floor. Retained catalysts and unused output reserves remain separate real stock.

**Ordinary nonartifact, nonequipment material/trade lots.** Where no overriding exact quote applies, use:

`Base × Provenance × Demand × Condition × Urgency`

Base is that lot's actual source reference. If genuinely absent, the Director can establish one finite homogeneous lot using these explicit new provisional references before the offer:

| Source band | Preserved lot range | New median reference |
|---|---:|---:|
| I | 5–15 gp | 10 gp |
| II | 15–50 gp | 30 gp |
| III | 51–148 gp | 100 gp |
| IV | 151–499 gp | 320 gp |
| V | 512–1,465 gp | 950 gp |

There is no general Tier-VI-or-higher median. These are finite lot values, not per-pound prices or values renewed by splitting a lot.

| Factor | Applicable values |
|---|---|
| Provenance | Undocumented 0.5; disputed 0.75; documented 1; actual Gate-Sealed 1.25 |
| Demand | Glut 0.75; normal 1; sought 1.25; strategic 1.5 |
| Condition | Damaged 0.5; worn 0.75; sound 1; actually exceptional 1.25 |
| Urgency | Forced 0.75; normal 1; real patient auction 1.10 |

Apply each factual factor once. An already applied Degraded half-value rule is not halved again as “damaged”; make the duplicate factor 1. Preparation with no price effect does not make material exceptional. A Gate Seal needs actual valid evidence. A patient auction needs its real appointment/buyer and waiting time. A disputed-provenance discount grants no right to sell another owner's property.

**True artifacts.** Use the actual artifact formula and profile, with separately stated Base Function Value and Gate Tier Multiplier or a genuine finite buyer quote. Missing inputs mean *unvalued*, not zero or infinite price. No ordinary sword or crafted Masterwork acquires artifact multipliers by being recovered from the dungeon. Record gross and each deduction separately. A negative net estimate exposes a possible liability; it is not a compulsory purchase, debt or negative payment to a seller.''',
'''For a true artifact, preserve the Core formula:

`BaseFunctionValue × GateTierMultiplier × artifact Quality × Provenance × Demand × Legality − actual uncounted costs`

Keep these source quality factors separate from manufacturing/equipment grades:

| Artifact market quality | Source factor |
|---|---:|
| Crude/damaged | 0.25 |
| Standard | 1 |
| Fine | 1.5 |
| Superior | 2.5 |
| Exceptional | 5 |
| Masterwork or named | 10 |

The source also retains no provenance ×0.5, verified Gate Seal ×1.1–1.5, urgent strategic demand ×2–10, and the illegal-but-desired row ×0.5 lawful/×2 black market. These apply only through a legitimate particular profile/offer with actual predicates and lawful disposition; a range gives no automatic maximum. Sentient, cursed or contagious objects need their actual liability assessment. These source labels do not interpret cosmology or create a new market.

The general table supplies no numeric BaseFunctionValue or GateTierMultiplier. An actual artifact record/finite offer must state its missing values; never invent Tier-VII–X formulas or borrow unrelated item prices. Preserve gross, stabilization, transport, tax and liability entries separately, charging only expenses not already counted. Actual seizure, consent and insurance keep their own procedures.

An ordinary lot's NEW fallback reference names its exact quantity/mass, source band and finite identity before pricing. Subdivision allocates the parent's reference exactly; it creates no new catalog commodity or extra total value. Original Loop and Core formulas, including conflicting grade words, stay preserved in the source layer. All 687 reviewed recipe references retain their domain-specific restrictions.''')

section(21, 'One settlement ledger',
'''Keep exact fractions of copper until each actual final payment. Use 1 sp = 10 cp, 1 gp = 100 cp and 1 pp = 1,000 cp. Where accepted, retain 1 Mithril Mark = 500 cp, Embermark = 2 sp, Soulshard = 1 gp and Tidesilver = 1 sp. Verdant Leaf and otherwise unvalued currency have no invented universal conversion. Names do not establish currency origins.

Round a final purchase, tax or fee payable **up** to copper once; round a final sale receipt **down** once. A coherent homogeneous sale bill is one receipt. Distinct real contracts can have separate final rounding; individual factors or components are not new transactions merely to change rounding. Displayed decimals never replace the exact value.

For each entry, record transaction ID, payer/payee, currency, goods/quantity or service, agreement/authority, exact quote, actual rounded payment, timestamp, status and related prior payment. Quoted, reserved, paid, owed, refunded and lawfully written off are different states. A price quote spends nothing. Apply deposits to their agreed bill. Insurance is an inflow, not sold cargo.

For the default Loop net-share sponsor agreement:

`SponsorBase = max(0, G − T − RQ)`

`SponsorShare = contracted percentage × SponsorBase, rounded once as payment`

`NetExpedition = G − T − RQ − SponsorShare`

G is actual sale receipts, T the direct Haven taxes on them, and RQ the episode's actual mandatory rescue/quarantine expenses. Count RQ once whether paid earlier or now. This sponsor base is before personal wages and discretionary purchases. A signed gross-share or priority-lien agreement instead uses its own declared terms.

True profit includes actual episode inflows less every distinct actual episode cost once: shares, wages, consumed/replaced supplies, operating fuel, repair, interest and other agreed costs. Show capital purchases and borrowed principal separately. Loans and principal repayment are financing, and selling existing personal capital is not earned cargo. Cash allocated to next-expedition reserves is a further allocation, not automatically the same as profit.

Report the charter's gross cargo target, net expedition target and true-profit/distributable-after-reserves target, stating whether the comparison is an appraisal or a realized sale. Appraised value does not pay wages. Keep insufficiently funded obligations owed; do not invent negative inventory, a compulsory new loan or unlimited sponsor funds. Allocations cannot exceed actual available money.''',
'''Every actual cost has one event identity. Do not charge an already-paid provision purchase, transport premium, tool or sponsor advance again. Distinguish using existing capital, buying new capital, financing and operating expense explicitly in the episode's accounts rather than hiding them in a single “net” value.

If an artifact net quote already deducted rescue/quarantine or tax, reconstruct its gross and the visible deductions before applying the sponsor formula. Do not subtract the same deduction from net again. A deposit and final balance settle one bill; an insurance claim does not create another sale of missing cargo.

Preserve exact parent-lot value allocations through subdivisions; individually rounded child estimates cannot exceed the parent's historical reference merely by splitting. Real separately agreed transactions keep their legitimate final rounding. Unknown exchange rates and unresolved liabilities remain explicit, not zeroed for convenience.''')

section(22, 'Claims, sponsors, taxes and insurance',
'''Record entitlement and permitted disposition before spending or selling. The Core priority is actual authorized emergency survival use; existing liens/charter claims; wages, porter shares and rescue costs; Gate/sovereign taxes and authorized seizure; written party division; then sale, donation, study, crafting or retirement. A title dispute or incompatible orders needs a real hearing. Priority neither waives a due sale tax nor charges a bill twice.

Use the **single highest applicable** Loop levy on the same taxable disposition:

| Actual transaction category | Levy |
|---|---:|
| Registered routine goods | 3% |
| Licensed crafting materials/goods | 5% |
| Artifact auction | 6% |
| Strategic/regulated cargo | 8% |
| Authorized contraband-amnesty disposal | 12% |

Identify category and jurisdiction before the offer. Written pre-sale exemptions affect only their stated charges. The 12% bracket does not legalize unlawful trade. Ordinary purchases do not acquire this sale levy; separate tolls, hearings or seizures need their actual authority/contract.

The default Loop sponsor shares use the preceding net-share base and must be accepted before expenditure:

| Sponsor | Share | Source support, when actually provided |
|---|---:|---|
| Self | 0% | Own capital |
| Local guild | 20% | Supplies and ordinary licenses |
| Merchant/bank | 30% | Capital, transport, appraisal access |
| Noble/temple | 35% | Capital, political cover, specialists |
| Sovereign/great institution | 45% | Full logistical support and legal force within actual authority |

A contract must state its chosen rate, exact gross/net base, contribution as grant or loan, title/material exceptions, due date and payer. Support must really be provided. Never stack two alternative schedules for one obligation or impose them retroactively. Quoted rights cannot exceed real institutional authority or the table's Session Zero agreement.

For the standard Loop cargo policy, declare finite insured lots, insured value I, beneficiary, episode, carrier, provenance, covered hazards and exclusions, and pay the premium before loss. Charge the highest applicable premium once: ordinary 5%; dangerous/Volatile/Cursed/Living 10%; Attention/strategic 15%.

The deductible is **D = 20% of I once per policy episode**. The provenance rate r is 60% undocumented, 75% disputed or 90% documented/Gate-Sealed. For cumulative eligible covered loss L:

`TotalEntitlement = max(0, min(I, r × min(L, I) − D))`

`AdditionalPayment = max(0, TotalEntitlement − prior actual payouts)`

Apply the genuine policy terms and remaining insured value. This new partial-loss calculation matches the source whole-loss formula when L = I. A later claim does not restart the deductible or pay the full total again. The same already compensated interest cannot collect twice. Recovery of insured property requires its real return/subrogation adjustment.

Give an actual safe-access claim notice within 72 elapsed hours of return; an earlier authenticated notice counts. Declared inability to communicate postpones the deadline until communication is restored, without backdating coverage. Routine examination needs two active hours of qualified work plus real evidence-gathering time. It is not guaranteed payment in two hours.

Fraud, undeclared cargo, voluntary abandonment without a prior insured-sacrifice clause, and loss after knowingly ignoring an applicable abort condition are excluded. Insurance supplies money under terms, never new material, HP, souls or a restored person.''',
'''Preserve actual claims, unmet obligations and each claimant's authority. Emergency-use priority needs a genuinely necessary authorized use, not unrestricted consumption. Establish permitted disposal first, then calculate/remit the transaction's taxes and sponsor base. No appraisal settles title.

Core alternative sponsor offers remain distinct negotiations:

| Offer | Source terms to complete in the actual contract |
|---|---|
| Merchant | 20–35% gross; agreed first-purchase option |
| Guild | 15–25%; actual dues and stated formula/patent rights |
| Noble | 25–50%; particular strategic claims |
| Religious | Actual tithe and relic priority |
| Consortium | 30–60%; actual liens/audit |
| Criminal | 40–70%; actual unlawful risks |

Where a row omits its percentage base or exact tithe, the offer must supply it. Do not import another row's default. These are alternatives to the Loop net-share defaults, not additional shares.

Core also offers separate Life/Return at 5% of expected share, Cargo at 8–20% value, Gate-Delay at 3%, Artifact-Liability at 10%+, and an annual ransom bond. They are not automatic riders or duplicate premiums on the standard Loop policy. Before purchase, every binder needs an exact premium, currency/value basis, term, named beneficiary, finite payout cap, deductible/rate or fixed-benefit formula, covered trigger, evidence, exclusions and notice/due terms. A missing annual fee, payout size or other undefined term needs an ordinary finite offer; the incomplete policy cannot be bought or claimed.

Life/Return keeps its actual named death-and-body-recovery trigger. Delay requires an actual covered closure/Guardian delay, not poor planning. Liability needs its real lawful-sale loss and disclosed risks. Ransom needs actual capture, authorized payee and release terms. Preserve exceptional exclusions as literal source receipts without cosmological interpretation. Notice, accepted claim, entitlement and payment remain different records.''')

section(23, 'Standing and earned history',
'''The new ordinary policy, **standing-v1**, uses an integer from −3 to +3 for each resolved individual/institution relationship:

| Score | Description | Ordinary access guide |
|---:|---|---|
| −3 or −2 | Hated | An actual willing provider, safe intermediary or specific exception; no automatic attack |
| −1 | Disliked | The provider's ordinary public dealings under its real restrictions |
| 0 | Neutral | Eligibility to ask for public goods, lodging and contracts |
| +1 | Liked | Consideration for an offered introduction/license/buyer process |
| +2 or +3 | Honored | Consideration for offered bonded storage, credit, sensitive desks or senior audiences |

These are opportunities to seek actual services, not granted offices, ownership, credit balances, licenses, waivers or auction admission. Named existing entitlements keep their own terms. Hated with one institution does not ban unrelated public services. Keep +2 and +3 distinct even though both display Honored; absence, unresolved information and hidden data are not an explicit known Neutral 0.

Saved standing supplies **no automatic d20 modifier or magic discount**. It changes no RP, RC, spell rank, Dissonance, charges or alignment by itself. Reputation as a CHA skill is a separate applicable check: add proficiency once, not proficiency plus the relationship score. The actual known-buyer mundane sale fraction remains its specific equipment rule.

A significant public attributable ordinary event can propose ±1; a major public success/betrayal ±2. Within one subject/institution/scene, add the signed proposals, cap their sum at −2…+2, then apply it to that scene's opening score and clamp the result to −3…+3. Record every event, its contribution, actual applied change and overflow. Recompute from the opening score when opposite events occur; do not exploit the order of saturation. No banked overflow or extra award per witness/report.

A campaign-defining exception requires its real distinct event and expressly predeclared magnitude/cap exception. Other institutions respond only to information actually reaching them and their own stakes. NPC attitude, Expedition renown, legal status and named privileges remain separate.

For a genuinely fresh Cult Escapee, bind the full background to actual institutions: former cult Hated/−2, suspicious religious authority Disliked/−1, anti-cult group Liked/+1. This does not target every cult or religious order. Existing earned history is never overwritten by a fresh-start value.''',
'''This is an explicit NEW adoption, replacing the older Loop −5…+5 standing/access ladder and the Player's Revered +5 / Respected +3 / Friendly +1 / Neutral 0 / Suspicious −1 / Hostile −3 / Hated −5 automatic social-modifier table in the integrated ordinary procedure. Preserve all three full tables and source versions. The Player numbers were modifiers, not evidence of a saved standing scale. Activating an old record requires its source-version interpretation; neither old table silently stacks with standing-v1.

Preserve the runtime Cult Escapee religious-orders:+1 map as historical data. Only when its source and later earned events establish that it was an erroneous initialization, explicitly replace that initial contribution with −1 and replay the real events. For example, erroneous +1 plus earned +1 becomes corrected −1 plus earned +1 = 0. If origin/history is unknown, retain raw +1 and flag that relationship rather than guessing. Full lossless handling and all 20 background comparisons follow RP-A01–06.

Keep Loop renown as historical/cultural descriptors: surviving Tier I, proven adventurer; reaching Tier II, established professional; profitable Haven return, career-defining success; operating through Tier III, elite expedition member; returning from IV, famous or feared; returning from V, living legend. Whether an NPC knows a deed needs actual information. Sixth-Gate, seasonal and deeper-setting statements stay literal receipts only, granting no faction number, authority or cosmological conclusion.''')

section(24, 'Haven work, services, learning and recovery',
'''A Haven Turn is **24 elapsed hours**, not a token that buys any result. Queue real workers, providers, facilities, materials and intervals. The normal day has two eight-hour productive Watches and Rest. Waiting is elapsed time, not productive labor or automatically beneficial rest. A Haven provides no teacher, workshop, buyer, cure, safe berth, food or license merely by being named.

Exact recipes keep all their gates, phases, assistant limits and hours—including a 960-hour order. “Brew a Batch in one day” is an activity label, not permission to finish a longer recipe. Repair, service, charging and creation remain distinct.

| Learning procedure | Retained requirement |
|---|---|
| Ordinary trade training | 80 active hours with qualified instructor; 10 gp tuition; actual tools/living costs; grants only its stated proficiency/trade 1/XP 0 |
| Ordinary spoken language module | 240 hours |
| Ordinary literacy module | 80 hours, including 40 for script |
| Full language with new script | 320 hours total |
| Full language with already known script | 280 hours total |

Language learning credits actual 15-minute phases, genuine instruction and the 1 gp per eight instruction-hour reference. A shared script or translated passage does not teach the language or a recipe. Keep actual Scribing Insight earning and the three-point/eight-hour supported-passage consultation, specific to its language. There is no universal Insight exchange or ordinary instruction purchase of combat feats/proficiencies. Class, spell and feat choices keep their real gates and pending status.

Short Rest, safe eight-hour Rest/beneficial Long Rest, four consecutive hours of voluntary Morale recreation, and 24 consecutive hours of full Haven care are separate procedures. Debt-clearing Rest inside the reward limit does not refill resources again. Actual compatible patients may rest during care; active practitioners cannot count the same work as their rest. Wound treatment retains eight hours, kit, one Supply and its actual result degrees. A Haven label neither removes a Wound nor bypasses the three-Wound healing ceiling.

Dependence recovery keeps its reviewed seven consecutive no-dose project days, each with one actual treatment hour and one Supply. The designated practitioner uses the chosen Medicine, Religion or Alchemy method and the final substance DC, or fallback 14 where applicable. Failure needs a fresh seven-day project. A qualifying eight-hour daily care activity includes that day's treatment hour, grants one nonstockpiled advantage on the next recovery check, and prevents only an actually defined ordinary escalation. It does not cure dependence automatically or alter crashes, doses or tolerance. Exact interruption rules still govern.

| Core service reference | Tiers I–III | Tiers IV–VI |
|---|---:|---:|
| Clean water, one mapped person-day | 1 cp | 1 sp |
| Ordinary hot meal | 2 cp | 5 sp |
| Qualifying eight-hour lodging/berth, per person | 5 sp | 5 gp |
| Verified map update | 1 gp | 25 gp |
| Preservation, per begun 10 lb accepted bill | 5 sp | 10 gp |
| Ordinary repair service | 10% of applicable undamaged reference | 15% |
| Actual escort journey, per floor/person | 2 gp | 50 gp |

These are available-provider offers, not automatic stock or extra fees on an inclusive bill. Water and meal quantities follow part 1. Lodging supplies a real qualifying stay, not automatic rest rewards. A map update takes one active desk hour using actual relevant records; it adds their true facts, not secured terrain or firsthand mapping marks. An escort needs its actual team, journey, food and availability, not a free additional army.

Preservation charges once per begun 10 lb of the accepted nonempty bill. The provider supplies compatible real inputs and the exact method/lot limits: use 30 minutes per lot and the 24-hour treatment where that is the governing method. Payment cannot preserve an unsupported active core. Ordinary repair service takes the actual qualifications and at least max(1 hour, maximum HP/10 hours); special Broken magic bodies retain their specific requirements. An inclusive service price replaces the self-repair material bill.''',
'''Keep all 687 recipe creation/research/copying procedures, finite primary bodies/ingredients and source-specific charges. Parallel work requires distinct actual compatible workers. Real care, sleep, recreation and treatment may overlap only where the exact procedures allow them; active labor cannot be credited twice.

If no provider can furnish the published preservation price, that offer is unavailable. Do not conjure preservatives or bill a second self-treatment charge for the same operation. Material freshness, access, volume, containment and original clocks still matter. Resurrection requires an actual available operative effect and finite contract; a service-price row cannot author a missing resurrection procedure.

Ordinary license administration takes one active hour with the actual desk, applicant and evidence. Before work the offer must state its posted fee, qualification, jurisdiction, scope and expiry; the source supplied no universal fee. Routine satisfied requirements issue without a roll. Uncertain evidence/persuasion uses its own procedure, and success grants nothing beyond the official's authority.

Patronage and information use the actual social-scene time/stakes and venue quote. A Core rumor-network fee grants its printed advantage only to real relevant Gather Information work using the appropriate existing skill; it creates no new proficiency. A private meeting protects only against the ordinary surveillance measures actually provided. Faction's 24-hour reporting checkpoints do not add labor or free service hours.''')

section(25, 'Coins, unlawful operations, labor and rescue',
'''Track each coin's denomination, composition, count/weight, custody and actual mint acceptance. Declare the assay method and suspected defect before the roll; do not make a generic and specific test for the same uncertainty or switch to the easier one after failure.

| Generic bulk assay | DC |
|---|---:|
| Obvious defect | 10 |
| Mixed/clipped coin | 13 |
| Plated/adulterated coin | 16 |
| Expert false mint | 19 |

| Specific Core method/defect | DC | Preserved value range |
|---|---:|---|
| Trace shaving, 1–3% | 12 | 95–99% face |
| Light shaving, 4–8% | 14 | 85–95% face |
| Heavy shaving, 9–15% | 16 | 70–85% face |
| Ruined shaving, 16–30%, once weighed | 10 | 40–70% face |
| Washed/plated, without cutting or magic | 18 | 5–25% recoverable value |

One ordinary assay work unit handles up to 100 coins or 10 lb, whichever limit is reached first, in 30 active minutes. Keep materially different variants identified. Use INT (Investigation) or the relevant actual proficient tool once. An applicable functioning jeweler's-scale, touchstone, milled-edge or merchant-test-kit method can supply its source proficiency contribution to that assay, not a second proficiency bonus, general training or supernatural detection. Destructive testing spends the actual sample. Routine documented weighing needs no new roll.

Failure leaves uncertainty. Only a declared false-assessment stake can give a fallible critical-failure report; no die changes metal. New evidence or a genuinely different test can justify more work and another roll. Changing the appraiser alone cannot.

__CONFIRMED_COIN_FINE_PARAGRAPH__

Unlawful trade still needs real contacts, agreed terms, actual cargo movement, any real concealment/document act and actual payment. Resolve only stages that exist as separate uncertainties. A deal does not create forged authority, a new skill or a free Scribing recipe.

Underways Heat is 0–6 for the actual operation/institution pursuit history. A triggering act adds its highest applicable category once: petty illicit 1, restricted 2, strategic theft/smuggling 3, trafficking/forbidden 4. At each completed 24-hour Haven interval with an active operation, roll once; d6 at or below Heat triggers the declared enforcement complication. Heat 0 has none. Faction reporting does not add a second roll.

An actual accepted bribe of 10% of the agreed lot value reduces Heat by 1, or 25% by 2, spending the payment once. An active operation's Heat cannot fall below 1; no bribe is paid at 0. Refusal or unsuccessful negotiation grants no reduction. Renaming/repacking an operation does not reset evidence, Heat or unresolved legal consequences. Enforcement requires actual actors, authority and means, not remote automatic seizure.

People remain actors with factual and asserted legal status recorded separately: Free, Contracted, Debt-Bound, Penal, Enslaved, Rescued/Liberated or Disputed. A label creates no ownership, restraint or immunity. Use actual body weight, equipment and reviewed casualty Load: Tiny 1.5, Small 3, Medium 6, Large 12; larger unsupported bodies require their profile. Petrification multiplies body pounds by 10, not casualty Load. All melded and external passenger equipment burdens an outside carrier. Voluntary passengers use their actual seats/custody facts, not captive ownership.

Ordinary lawful wages are 1 gp/day unskilled, 3 gp skilled or 10 gp specialist; dangerous expedition work doubles them unless the named service or real contract supplies its own rate. Do not charge both. A wage day buys at most two eight-hour work Watches and a protected Rest opportunity. Extra risky/emergency duty requires actual agreement and its costs/Rest Debt. A lawful debt bond records principal, credited wages and agreed simple interest no greater than 10% per literal Opening; no hidden compounding or automatic debt. Coercion, kidnapping, fraud or unlawful confinement cannot demand an invented buyout.

An actual trafficking investigation uses an Evidence Clock 0–4. A concrete accessible lead takes one active hour and the appropriate Investigation/relevant-skill task at declared DC/stakes. Success adds 1, Critical Success 2, capped at 4; repeated evidence adds nothing. At 4, seek a real authorized warrant/hearing or plan a genuine rescue/raid. The clock does not conjure police, prove a false report or resolve combat. Guards, restraints and escape routes are actual scene facts. Consent-based adult services remain distinct from trafficking, with the table's boundaries controlling.''',
'''Coin-service accounting and the fine use the confirmed correction reproduced in the player module. No service minimum is charged per coin, material variant or every 30-minute stage of a single commissioned bill. A private owned toolkit does not charge its owner a fictional desk fee. Cutting/reminting uses actual provider work and links spent coin identities to the real metal/output quantities without duplication.

Route undefined legacy skill names through existing methods: Streetwise uses CHA/Reputation or Persuasion for actual networks; Banking uses INT/Investigation or appropriate real commercial tools/records; Forgery uses the actual forgery kit with DEX or INT as the physical task warrants. No new universal skill or legal authority is created. Contact/terms/collection use declared social-scene time, movement uses routes, and document production its actual reviewed work. Do not insist on five rolls where one real transaction resolves the uncertainties, or roll an impossible stage.

Maintain stable Heat event IDs through fronts, repacking, splits and joins. Ended activity retains unresolved evidence/legal consequences. Never presume intent from ancestry, suspicion or a failed assay. Actual arrest, hearing, seizure and standing effects need their real scope.

Preserve person-market quotations only as reports of abusive/particular fictional institutions. They are not universal ancestry prices or a purchasable player-agency mechanic. The older captive 1/2–4 Load shorthand is superseded by the reviewed body/casualty rules, preserving the original as evidence.

If the source six-step rebellion clock is used for an actual coercive situation, add one step per distinct learned abuse, opportunity, allied-help or security-failure event. At 6, schedule the predeclared real escape/resistance action; do not manufacture mind control or a remote revolt. Evidence, reports, lawful authority and successful rescue remain separate facts. Literal soul-linked currency, religious, planar and deep-setting references are retained without interpretation.''')

section(26, 'Advancement and the next descent',
'''Choose milestone or optional XP advancement before awards. Do not grant both for the same achievement. The milestone default grants an earned stated level when its actual objective is confirmed, not simply after a Watch, appraisal or return. Follow the real class, ASI, Arch and Hero schedule and pending acquisition constraints. A higher maximum does not heal or refill a pool; retain spent resources and grant only the actually earned new unspent Hit Die.

For optional XP, freeze each eligible recipient's actual gap to their next level at the beginning of the distinct award scene:

| Achievement | Percentage of that frozen gap |
|---|---:|
| Routine | 5% |
| Standard | 10% |
| Hard | 15% |
| Severe | 25% |
| Guardian victory | 40% |
| Actual profitable extraction meeting its declared threshold | 10% |
| First qualifying route/text/faction discovery | 5–15%, chosen before resolution |

Sum that scene's eligible predeclared percentages, cap at 60% of the frozen gap, then round the scene award once to the nearest 10 XP, halves upward. If rounding exceeds the exact 60% ceiling, limit the award to floor(0.60 × gap ÷ 10) × 10. Do not recalculate earlier percentages against a larger new gap after a mid-scene level. At a level cap or without a supplied next threshold, invent no next gap or XP award.

All materially contributing members can qualify, including real reconnaissance, research, transport and support contributions away from the fight. Roster presence, unrelated waiting, repeated reports or reused evidence are not automatic contributions. Name the actual contribution, unique achievement and eligible recipient. Notifications, sale, claim or auction records of the same achievement do not award it again. Crafting-domain XP stays its own ledger. A valuable failed objective can have a predeclared reward; do not invent one after failure.

Close the episode at its actual time with outcomes and the declared success metric, each member's location, routes/camps, Pressure, pursuit/Heat, provisions and containers, HP/Wounds/injuries/Strain/Rest Debt/resources, companions/devices/corpses, cargo title/custody and terminal harvest/salvage claims. Include quotes, actual payments, liabilities, insurance, attributable standing/renown, pending faction actions and earned advancement.

Then accept the next charter prospectively, with real access, budget, reserves and abort conditions. A new descent does not erase unresolved disputes, replenish stock, reset clocks or replay an old claim. It can proceed only when its actual conditions allow it.''',
'''Award records preserve the frozen per-recipient gap, exact percentages, rounding, scene cap and unique actual contributions. Do not divide one party award into hidden unequal per-roll bonuses. A reward never promotes a pending spell, feat or class option. Use the supplied actual character schedules and thresholds, not a guessed level-cap extension.

The complete EX58 worked sequence is a synthetic source-bound example; it does not authenticate its people, route, buyer, coins, stock or factions as actual campaign facts. The full candidate must retain that 21-event sequence, 28 additional boundaries and 24 adjudicated proposal scenarios alongside its own complete records. This module's examples do not replace them.

Opening/Horn timing, retirement and seasonal references remain literal receipts. This chapter grants no new Cycle renewal, mind continuity, legacy infrastructure or cosmological interpretation. Keep public knowledge distinct from Director-sealed records. The separate full-candidate, runtime, human balance and whole-game flow reviews remain open.''')

CASES = [
    ('03-01', ['FL-19'], 'A Tier-I fast return uncovers a real lien after intake.', 'Move the same return to full intake, retaining the completed ten minutes and actual paid fees. Do not restart intake or charge both routes.'),
    ('03-02', ['FL-19'], 'One representative is required for two different 30-minute desk proceedings.', 'Without compatible actual participation or another qualified representative, schedule 60 minutes sequentially. Two staffed desks alone do not duplicate the person.'),
    ('03-03', ['FL-20'], 'A 100-gp undamaged mundane item is sold under the actual Liked-buyer equipment schedule.', 'Its offered reference is 60 gp before actual separate obligations. Do not also multiply by the Loop demand/provenance table.'),
    ('03-04', ['FL-20'], 'An ordinary lot has a genuine 100-gp base, documented provenance, sought demand, sound condition and a real patient auction.', 'The scoped commodity estimate is 137.5 gp. The buyer, auction wait and lawful sale remain actual prerequisites; this is not a guaranteed receipt.'),
    ('03-05', ['FL-20'], 'A material’s actual source reference already includes its Degraded half-value adjustment.', 'Do not apply the same loss again as the Loop damaged factor. Keep the existing condition adjustment and use 1 for its duplicate factor.'),
    ('03-06', ['FL-20'], 'A named object is offered without an actual artifact BaseFunctionValue or GateTierMultiplier, and no finite buyer quote supplies them.', 'It remains unvalued. A grand title or recipe Masterwork quality does not supply the missing factors.'),
    ('03-07', ['FL-21'], 'The final exact purchase amount is 7/3 cp; a separate final sale receipt is also 7/3 cp.', 'Pay 3 cp for the purchase and receive 2 cp for the sale. Do not round their internal multiplications independently.'),
    ('03-08', ['FL-21', 'FL-22'], 'Actual cargo receipts are120gp, direct tax6gp, mandatory inspection/quarantine2gp, and the accepted default guild share is20%.', 'SponsorBase is112gp; share22.40gp; NetExpedition89.60gp. If the2gp was already paid, it is still counted only once.'),
    ('03-09', ['FL-21'], 'The same episode has20.20gp of other actual operating costs and requires20gp retained from profit for its next reserve.', 'Operating profit is69.40gp; profit available for distribution after that reserve is49.40gp. Neither is the gross120gp or NetExpedition89.60gp.'),
    ('03-10', ['FL-22'], 'A single disposition is both licensed crafted goods and strategic regulated cargo.', 'Use the one highest applicable8% bracket, not5%+8% or an additional routine3% levy.'),
    ('03-11', ['FL-22'], 'A documented standard cargo policy insures100gp; first cumulative eligible loss is40gp, then reaches100gp.', 'The once-per-episode20gp deductible gives first entitlement16gp, then total entitlement70gp. With16gp actually paid, the later payment is54gp, not70gp again.'),
    ('03-12', ['FL-22'], 'A separate Core ransom-bond offer omits its annual premium or payout cap.', 'It is an incomplete quote. Complete the real finite offer before purchase; do not invent terms or treat the standard cargo policy as a free rider.'),
    ('03-13', ['FL-23'], 'A scene opens at standing+2 and contains actual ordinary proposals+2 and−2.', 'The signed sum is0; recompute from opening+2, leaving+2. Applying one saturated change then the opposite must not create a different result.'),
    ('03-14', ['FL-23'], 'A version-proven Cult Escapee relationship started at erroneous+1 and later earned+1.', 'Replace only the initialization with−1 and replay earned+1, giving0. Unknown history would remain raw and flagged instead of reset.'),
    ('03-15', ['FL-24'], 'A preservation provider accepts one coherent21-lb bill under the low-tier service reference.', 'Charge three begun10-lb units at5sp, totaling15sp, for that accepted service. The actual compatible method/materials and lot work remain required.'),
    ('03-16', ['FL-24'], 'A language learner already knows the needed script and completes actual instruction at the published reference rate.', 'The full module needs280 active hours, credited in15-minute phases. The reference instruction amount is35gp; a shared script alone does not grant fluency.'),
    ('03-17', ['FL-24'], 'A960-hour recipe is assigned two eight-hour productive Watches each day.', 'It requires60 such productive days before its other exact gates. One Haven Turn cannot finish it, and actual interruptions may extend elapsed time.'),
    ('03-18', ['FL-25'], 'One commissioned assay contains150 light coins under the10-lb weight cap.', 'It needs two30-minute work units. The combined bill’s actual minimum assay fee applies once, not once per coin or work unit.'),
    ('03-19', ['FL-25'], 'A skilled worker accepts the ordinary dangerous-expedition wage schedule.', 'The reference is6gp per wage day for at most two eight-hour work Watches and protected Rest, not24 compulsory labor hours.'),
    ('03-20', ['FL-25'], 'An Evidence Clock is3 and a genuinely new accessible lead earns Critical Success.', 'Record the distinct+2 contribution but cap the clock at4. It supports a real warrant/rescue process; it does not itself free anyone or summon officers.'),
    ('03-21', ['FL-26'], 'A scene freezes an XP gap of1200 and has a legitimate Severe25% award.', 'The scene reference is300XP, with no recalculation of that frozen gap after an intervening level.'),
    ('03-22', ['FL-26'], 'A frozen gap of125 has eligible scene percentages totaling at least60%.', 'The exact ceiling is75XP; nearest10 with halves upward would give80, so preserve the cap and award70XP.'),
    ('03-23', ['FL-21', 'FL-26'], 'A return is appraised above the charter’s gross target but has made no sale and lacks reserve cash.', 'Record the unrealized gross comparison. It neither pays wages nor proves the realized profit/reserve target or permits an otherwise unfunded next descent.'),
    ('03-24', ['FL-19', 'FL-25'], 'A false coin is detected in a holder’s documented innocent possession.', 'Identify legitimate portions, actual authorized seizure and real service charges separately. A failed check or possession alone does not establish knowing fraud.'),
]

def render(env, audience):
    lines = [f'# {audience.title()} expedition procedures — Haven, settlement and continuation', '', env['notice'], '',
             'Use with [organization and provisions](EXPEDITION_PART01_PLAYER.md), [routes and extraction](EXPEDITION_PART02_PLAYER.md), and the current [Core resolution](../CORE_RESOLUTION_PLAYTEST.md) rules.', '']
    if audience == 'director': lines += ['Read the complete [player Haven module](EXPEDITION_PART03_PLAYER.md) alongside these Director procedures.', '']
    for s in env['sections']: lines += ['## ' + s['title'], '', s['text'], '']
    if audience == 'director':
        lines += ['## Authored boundary examples', '', 'These expected outcomes are not executed campaign scenarios or human playtest evidence.', '']
        for c in env['workedCases']: lines += ['### ' + c['id'], '', c['given'], '', c['expected'], '']
    return '\n'.join(lines)

def main():
    # Bind the delivered correction and its measured descendants, preserving
    # the original source direction separately as historical provenance.
    fine = read(A / 'EX58_EDIT_02_FULFILLMENT.json')
    assert fine['finalAssistantMessageId'] and fine['status'] == 'fulfilled'
    fine_paragraph = fine['exactReplacementParagraph']
    assert len(fine_paragraph) > 100
    for s in SECTIONS:
        s['player'] = s['player'].replace('__CONFIRMED_COIN_FINE_PARAGRAPH__', fine_paragraph)
    paths = {'public': R / 'data/public/expedition_candidate/part03.json', 'internal': R / 'data/director/expedition_candidate/part03.json',
             'player': R / 'docs/mechanics/expedition/EXPEDITION_PART03_PLAYER.md', 'director': R / 'docs/mechanics/expedition/EXPEDITION_PART03_DIRECTOR.md',
             'receipt': A / 'EX58_CANDIDATE_PART03_CHECK.json'}
    assert not any(p.exists() for p in paths.values()), 'Preserve previous outputs before revision'
    checks = []
    def ck(n, v):
        checks.append({'name': n, 'pass': bool(v)})
        assert v, n
    manifest = read(P / 'FILE_MANIFEST.json')
    for x in manifest['files']: ck('Original final payload preserved: ' + x['path'], info(P / x['path']) == {k: x[k] for k in ['bytes', 'sha256']})
    directions = read(P / 'EX58_AUTHORING_REGISTER.json')['directions']; by = {x['id']: x for x in directions}
    for rel, expected in fine['descendants'].items():
        ck('Confirmed fine correction descendant: ' + rel, info(G / rel) == expected)
    current_directions = read(R / 'data/director/expedition_candidate/source_register_corrected.json')['directions']
    current_by = {x['id']: x for x in current_directions}
    ck('Current FL25 contains exact confirmed paragraph', current_by['FL-25']['authoringWording'].split('\n\n')[2] == fine_paragraph)
    ids = [s['id'] for s in SECTIONS]
    ck('Exactly eight FL19..26 directions', ids == [f'FL-{i:02d}' for i in range(19, 27)])
    prior = read(R / 'data/director/expedition_candidate/part02.json')['cumulativeAuthoredQuestionIds']
    ck('Prior eighteen distinct directions present', prior == [f'FL-{i:02d}' for i in range(1, 19)])
    ck('Confirmed correction inserted once', sum(s['player'].count(fine_paragraph) for s in SECTIONS) == 1)
    public = {'schemaVersion': 1, 'moduleId': 'EX58-PART03', 'status': 'authored-partial-candidate-awaiting-exact-review',
              'notice': 'Working chapter module 3. The three module pairs now draft all26 FL directions. Social, transport and reputation detail, full profiles and integrated records remain to assemble before exact review.',
              'questionIds': ids, 'completeExpeditionCandidate': False, 'selectionEnabled': False,
              'sections': [{'id': x['id'], 'title': x['title'], 'text': x['player']} for x in SECTIONS]}
    cases = [{'id': 'EX' + i, 'questions': q, 'given': g, 'expected': e} for i, q, g, e in CASES]
    director = {'notice': public['notice'], 'sections': [{'id': s['id'], 'title': s['title'], 'text': s['director']} for s in SECTIONS], 'workedCases': cases}
    names = ['GAMEPLAY_LOOP_CANON.md', 'CORE_RESOLUTION_PLAYTEST.md', 'EQUIPMENT_ACQUISITION_PLAYTEST.md', 'BODY_EQUIPMENT_PLAYTEST.md', 'STRAIN_PLAYTEST.md', 'CONDITION_RECOVERY_PLAYTEST.md', 'LANGUAGE_COMMUNICATION_PLAYTEST.md', 'CRAFTING_HARVEST_PLAYTEST.md', 'REPUTATION.md', 'CHARACTER_CREATION_PLAYTEST.md', 'CLASS_PLAYTEST_RULES.md']
    sources = [R / 'docs/mechanics' / n for n in names]
    reputation = read(A / 'REPUTATION_PRESERVATION_SOURCE_ADDENDUM.json')
    economy = read(A / 'EXPEDITION_HAVEN_FLOW_SOURCE_PREPARATION.json')['coreEconomySource']
    current_contracts = read(R / 'data/director/expedition_candidate/source_contracts_corrected.json')['contracts']
    internal = {'schemaVersion': 1, 'moduleId': public['moduleId'], 'status': public['status'], 'sourceReview': 'EX58-SOURCE-2026-10-11',
                'completeExpeditionCandidate': False, 'authoredQuestionIds': ids, 'cumulativeAuthoredQuestionIds': prior + ids,
                'remainingSourceDirections': [x['id'] for x in directions if x['id'] not in prior + ids],
                'publicEnvelope': public, 'directorModule': director, 'completeOriginalDirections': [by[i] for i in ids],
                'completeCurrentDirections': [current_by[i] for i in ids],
                'confirmedCoinFineCorrection': fine, 'completeCurrentContracts': [c for c in current_contracts if c['id'] in ['EC-09', 'EC-10', 'EC-12', 'EC-14']],
                'fullGoverningSources': [{'path': p.relative_to(G).as_posix(), **info(p), 'completeText': p.read_text('utf-8-sig')} for p in sources],
                'completePreservedStandingExcerpts': reputation['exactSourceExcerpts'], 'completePreservedCoreEconomyBinding': economy,
                'audienceBoundary': 'General player procedures only in public projection. No44faction dossiers, secret plans or source-version private campaign histories are projected.',
                'semanticCoverageNote': 'Manual authored wording against eight complete directions and confirmed fine correction. Structural parity/arithmetic checks do not certify full semantic integration.',
                'newPromotions': 0, 'runtimeImplemented': False, 'examplesAreRuntimeTests': False}
    ck('All eight directions have authored examples', set(ids) <= {q for c in cases for q in c['questions']})
    for rel, expected in read(A / 'EXPEDITION_INTEGRATED_V3_PREPARATION.json')['manifest'].items():
        if rel != 'README_EXPEDITION_INTEGRATED_V3.md': ck('Original submission current file preserved: ' + rel, info(G / rel) == expected)
    for p in sources: ck('Bound full source exists: ' + p.name, p.is_file())
    calc = [
        ('two incompatible desks', 30 + 30, 60), ('Liked mundane price', 100 * Fraction(3, 5), 60),
        ('commodity factors', 100 * 1 * Fraction(5, 4) * 1 * Fraction(11, 10), Fraction(275, 2)),
        ('purchase ceiling', -(-Fraction(7, 3) // 1), 3), ('sale floor', Fraction(7, 3) // 1, 2),
        ('sponsorbase', max(0, 12000 - 600 - 200), 11200), ('guild share', 11200 * Fraction(1, 5), 2240),
        ('net expedition', 12000 - 600 - 200 - 2240, 8960), ('profit', 8960 - 2020, 6940), ('distributable profit', 6940 - 2000, 4940),
        ('highest tax once', max(3, 5, 8), 8), ('first partial covered entitlement', max(0, Fraction(9, 10) * 40 - 20), 16),
        ('whole covered entitlement', max(0, min(100, Fraction(9, 10) * 100 - 20)), 70), ('later actual payment', 70 - 16, 54),
        ('scene signed standing', min(3, max(-3, 2 + max(-2, min(2, 2 - 2)))), 2), ('Cult corrected replay', -1 + 1, 0),
        ('21lb service units', -(-Fraction(21, 10) // 1), 3), ('three low-tier preservation units', 3 * 5, 15),
        ('known-script learning', 240 + 80 - 40, 280), ('known-script instructiongp', Fraction(280, 8), 35),
        ('960hour workdays', Fraction(960, 16), 60), ('150coin assay work units', -(-Fraction(150, 100) // 1), 2),
        ('skilled dangerous wage', 3 * 2, 6), ('new evidence cap', min(4, 3 + 2), 4),
        ('Severe gap1200', 1200 * Fraction(1, 4), 300), ('gap125 cap', 125 * Fraction(3, 5), 75),
        ('cap-conforming tens', (125 * Fraction(3, 5) // 10) * 10, 70),
    ]
    for label, actual, expected in calc: ck('Plain arithmetic: ' + label, actual == expected)
    save(paths['public'], public); save(paths['internal'], internal)
    for audience, env in [('player', public), ('director', director)]:
        paths[audience].parent.mkdir(parents=True, exist_ok=True)
        paths[audience].write_text(render(env, audience), encoding='utf8', newline='\n')
    ck('Whole public envelope parity', read(paths['public']) == read(paths['internal'])['publicEnvelope'])
    ck('Whole player chapter parity', paths['player'].read_text('utf8') == render(read(paths['public']), 'player'))
    ck('Whole Director chapter parity', paths['director'].read_text('utf8') == render(read(paths['internal'])['directorModule'], 'director'))
    links = []
    for audience in ['player', 'director']:
        for target in re.findall(r'\]\(([^)]+)\)', paths[audience].read_text('utf8')):
            ck('Actual local link ' + target, (paths[audience].parent / target).resolve().is_file()); links.append(target)
    for x in manifest['files']: ck('Original verdict unchanged after authoring: ' + x['path'], info(P / x['path']) == {k: x[k] for k in ['bytes', 'sha256']})
    receipt = {'generatedAtUtc': datetime.now(timezone.utc).isoformat(), 'moduleId': public['moduleId'], 'status': 'All26FLdirections drafted across3modules; full58candidate still incomplete/unreviewed.',
               'questionIds': ids, 'cumulativeQuestionIds': prior + ids, 'remainingDirections': len(internal['remainingSourceDirections']),
               'workedCases': len(cases), 'plainArithmeticChecks': len(calc), 'localLinkChecks': len(links), 'checks': len(checks), 'failures': [c for c in checks if not c['pass']],
               'outputs': {p.relative_to(G).as_posix(): info(p) for k, p in paths.items() if k != 'receipt'}, 'builder': {'path': Path(__file__).resolve().relative_to(G).as_posix(), **info(Path(__file__))},
               'scope': 'Source preservation, full representation parity, real local links and plain arithmetic. Authored cases are not full campaign execution.',
               'runtimeTestsExecuted': 0, 'newPromotions': 0, 'realSavesReadOrWritten': 0, 'sourceInformationDeleted': 0, 'details': checks}
    save(paths['receipt'], receipt)
    print(json.dumps({k: receipt[k] for k in ['moduleId', 'remainingDirections', 'workedCases', 'checks', 'failures', 'outputs']}, indent=2))

if __name__ == '__main__': main()
