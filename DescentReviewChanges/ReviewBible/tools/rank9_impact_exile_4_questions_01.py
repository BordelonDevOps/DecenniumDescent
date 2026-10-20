"""Unselected questions preserving four complete rank-nine impact/displacement promises."""
IDS=['eternal-anvil','reverse-gravity-field','transmute-flesh-to-energy','planar-collapse']
EA,RG,FE,PC=IDS
TIERS={
 EA:('C','A massive summoned hammer,5d12 force and one-round Stunned require an explicit manifestation/use lifecycle and genuine action opportunity.'),
 RG:('C','Everything in60ft rises60ft then falls; body/object enrollment,ascent,field lifetime and collision need precise source-local completion.'),
 FE:('C','12d10 chosen energy with resistance bypass and an exploding body require explicit target,packet,defense and surviving/dead-body outcomes.'),
 PC:('C','An area must actually inflict12d6 force,Prone and exile; save structure,geometry,admission,destination and return are unresolved.')}
Q=[]
def q(n,ids,source,options,recommendation):Q.append((f'R9IE-{n:02}',ids,source,options,recommendation))

q(1,[EA],
 'Eternal Anvil summons a massive war-forge hammer; the source does not say whether it strikes during casting,remains as a controlled effect,or becomes a wieldable object. Core gives a one-round duration.',
 ['A manifested hammer performs a fully described spell strike during the paid casting Action,with any residual expression explicitly bounded.', 'A persistent hammer has a complete object/effect profile and one or more separately lawful uses inside its actual one-round window.'],
 'Preserve a real hammer expression and full5d12/Stunned benefit. Specify source action budget and a genuine positive-use opportunity; neither a free extra Action nor an unusable duration is silently assumed.')
q(2,[EA],
 'The hammer prints5d12 force and Stunned,but supplies no target count,attack/save,reach,impact radius or successful-resistance outcome.',
 ['A single-target attack or save procedure with explicit damage and independent rider admission.', 'An expressly NEW area/impact procedure with exact enrollment,geometry,save and complete per-recipient outcomes.'],
 'Keep five d12 force. Decide the resolution openly; no automatic critical/save shortcut or inferred siege splash. Name whether objects can qualify and whether an immune damage recipient can still suffer the separately legal Stunned rider.')
q(3,[EA],
 'The Stunned rider is specifically one round. The hammer lifetime and target condition lifetime are not automatically the same endpoint.',
 ['One target-round of Stunned under an explicit actual regular-marker endpoint.', 'A precisely defined elapsed/round endpoint expressly chosen as the interpretation of one round.'],
 'Bind the actual shared source-character/target/encounter hard-control admission and exact Stunned immunities. Preserve an admitted condition through its real endpoint without a duplicate application or free hard-guard reset; state whether source suppression/removal affects the rider independently.')
q(4,[EA],
 'Massive does not supply body volume,weight,HP,support,anatomy,strength requirements or a hovering/telekinetic permission.',
 ['A nonphysical spell expression with explicit occupied geometry and no item/support/cargo identity.', 'A fully profiled physical temporary hammer with actual dimensions,mass,handling,destruction and support requirements.'],
 'Match the selected use model. Skybrand is a useful effect-only comparison,not authority to make this hammer float or attack remotely. No forge workstation,free weapon proficiency,indestructibility or valuable salvage follows from its name.')
q(5,[EA],
 'A one-round persistent hammer could otherwise receive repeated attacks,hand-offs,Ready uses or recast resets beyond the intended payload.',
 ['One complete payload use per paid source,with unused/failed use and exact expiry specified.', 'A stated repeat-use budget within the genuine duration,with every actual attack/command/action requirement retained.'],
 'Define permitted controller,range from actual origin,required perception,geometry and retained per-source history. Real extra opportunities can matter only under the chosen bounded rule; no duplicate5d12 packet from appearance,weapon and spell aliases.')
q(6,[EA],
 'Manifestation,impact,Stunned,cargo/object destruction and parent removal may resolve at different stages.',
 ['State complete staged transactions and settle each committed effect once,retaining source-local condition independence.', 'Use one atomic immediate impact where legal,then separately track only genuinely continuing rider or object state.'],
 'Resolve countering,suppression between stages,actual caster self-damage/Ready concentration,miss/invalid target,expiry and replacement. A resolving impact is not replayed by dispelling the hammer or ending its stun.')

q(7,[RG],
 'Reverse Gravity Field prints everything in a60ft radius,with Core cast range60ft. Radius is not range and the three-dimensional zone/center policy is missing.',
 ['A fixed60ft-radius sphere at a legal selected point within60ft,with actual overlap and LoE enrollment rules.', 'An explicitly selected ground/vertical field geometry preserving the full60ft radius and stating its vertical extent.'],
 'Do not change the60ft radius to diameter or center it automatically on the caster. Define partial-body inclusion,full displacement of admitted bodies,occlusion and actual terrain/object boundaries; allies and caster are not silently exempt.')
q(8,[RG],
 'Everything may include creatures,unattended objects,held cargo,liquids,anchored structures and terrain. The source provides no mass ceiling or object-splitting permission.',
 ['Move whole eligible physical assemblies,with explicit treatment of real attachments/support and occupied volumes.', 'Define another complete source-local enrollment/material boundary,expressly identifying any exclusion or new load limit.'],
 'Retain the broad promise and discuss necessary finite-world boundaries. Do not count carried gear twice,turn creatures into inventory,detach a foundation for free,create duplicate liquid volumes or silently exclude heavy targets.')
q(9,[RG],
 'Floats60ft up specifies displacement but not speed,path,ascent timing or whether the field continuously accelerates anything.',
 ['A finite source-driven60ft ascent at a declared event stage/rate followed by the chosen hold/release behavior.', 'A finite staged ascent during an expressly authored short field lifetime,with precise progress/interruption checkpoints.'],
 'Preserve60ft and actual upward path. No teleport,unlimited upward acceleration,lateral travel,unbounded flight or fictitious voluntary movement cost. An obstacle limits actual legal travel; no imaginary60ft completed distance is counted.')
q(10,[RG],
 'Ascent may encounter ceilings,other lifted bodies,overhangs,anchors or a target spanning the zone edge. No crushing or collision damage is printed.',
 ['Stop/suspend at actual legal contact under a complete deterministic multi-body collision policy.', 'Use a separately justified bounded collision/attachment resolution,explicitly authoring any additional effect.'],
 'Supply actual swept volumes,simultaneous movement ordering and room for each body/cargo. Do not push others aside,split bodies,phase through ceilings or infer upward fall damage. Separate admission from later overlap of an already affected body.')
q(11,[RG],
 'The source gives no save,grab,anchor check or voluntary resistance. Existing forced-movement and support protections have exact scopes.',
 ['Automatic admitted lift subject only to actual applicable source-qualified protections.', 'An explicitly NEW save/hold opportunity with exact timing,range,anatomy,action cost and outcomes.'],
 'State the gameplay consequence of any added resistance. Actual grabs require a reachable support and real permission; no free universal Reaction. Distinguish positional movement,external support loss and Falling so a ward does not become general gravity immunity.')
q(12,[RG],
 'Core Instantaneous conflicts with the practical lifetime of a field in which everything floats before fall damage after.',
 ['A one-shot lift/release transaction,with a precise release checkpoint and no persistent entry trigger.', 'A stated NEW continuing field/hold lifetime and concentration policy that preserves the original Core field as evidence.'],
 'Choose a useful complete sequence. Define later entrants/leavers,edge movement,recasts and overlapping fields. A temporarily held body has actual agency under its source; no implicit stasis or indefinite magical support.')
q(13,[RG],
 'A lifted body might voluntarily leave the original area,be independently moved,or gain real flight/support before release. The field has no explicit spatial retention/agency policy.',
 ['The selected lift/hold follows each admitted body through its stated finite operation,with separate actual movement permissions.', 'The lift/support exists only while the body satisfies a precise current-zone overlap predicate; leaving ends that support.'],
 'Select the field-local rule without adding Incapacitated,stasis,free lateral motion or flight immunity. On genuine unsupported release,inherit the settled Falling marker/distance/damage rules. Ordinary60ft uncontrolled descent is3d6; an Action Feather Fall remains an Action. Existing real flight or support can prevent Falling. Never count ascent as descent or apply impact before landing.')

q(14,[FE],
 'Transmute Flesh to Energy names flesh but describes a target; it does not enumerate living,Undead,Construct,plant,form,corpse or object eligibility.',
 ['A source-local actual-flesh creature predicate with explicit boundaries for each relevant current body.', 'Another expressly defined target predicate preserving the intended bodily conversion,with each extension stated.'],
 'Use actual current anatomy and legal targeting,not the actor name or an assumed soul. Unknown eligibility must not leak hidden state. Corpses,creatures,temporary forms and equipment remain distinct identities.')
q(15,[FE],
 'The target explodes into raw power for12d10 chosen energy,but no blast radius or recipient allocation is printed.',
 ['A complete target-directed12d10 conversion/damage operation with precisely stated external expression.', 'An expressly NEW explosion geometry and target/bystander allocation,stating whether the target receives the same or a separate packet.'],
 'Preserve twelve d10 and the exploding-target promise. Do not assume an area or double the rolled damage on the primary target. Declare center,witnesses,LoE,ally/caster exposure and actual body-origin coordinates.')
q(16,[FE],
 'Core Automatic or opposed as described supplies no actual attack/save or success outcome.',
 ['An explicit attack or save procedure with defined damage and body-conversion outcomes.', 'Automatic legal-target resolution only if consciously selected,with actual remaining defenses and full costs.'],
 'State the real resolution type,DC/attack provenance,die pool,critical applicability and successful-resistance consequences. Source-target invariants are revalidated at the appropriate stage; do not treat a tag as a save or defense.')
q(17,[FE],
 'Chosen energy has no listed damage menu,selection moment or per-recipient choice permission.',
 ['One explicitly enumerated energy type selected for the entire cast before commitment.', 'Another clearly bounded source-local choice model preserving real type provenance and no after-outcome optimization.'],
 'Use actual game damage identifiers. Null is root provenance,not an automatic selectable energy type; raw power does not create RP,relic fuel or a new cosmological element. Any mixed-type mode must preserve exact twelve-die allocation.')
q(18,[FE],
 'No resistances apply is an explicit bypass. It does not automatically say immunity,prevention,damage reduction,temporary HP,sharing,wards or all defenses are ignored.',
 ['Bypass actual resistance multiplication only; resolve other real defenses by their own wording.', 'Any broader override must be explicitly selected and justified as NEW beyond the printed resistance clause.'],
 'Retain the full resistance bypass without mislabeling every defense resistance. Provide mixed defense examples,actual prevention and Null/life interactions; avoid sharing recursion or applying the bypass twice to one root.')
q(19,[FE],
 'Explodes into raw power must reconcile with actual positive HP,zero/death saves,damage-caused death,NullDisabled or survival,remains and held equipment.',
 ['A complete damage-linked transient bodily expression,with explicit surviving-body restoration and source-qualified death/remains results.', 'A separately authored persistent/terminal conversion rule with exact admission,identity,lifecycle and consequences,if the source requires it.'],
 'Confer on literal body conversion rather than inventing automatic death or silently erasing it. Keep real gear and prior body history; Null does not erase independent non-damage endings,but no extra body destruction is implied. No copied remains,free resurrection or automatic harvested energy.')

q(20,[PC],
 'Planar Collapse affects an area,but supplies no radius,shape,eligibility,center,witness or boundary policy; cast range is120ft.',
 ['A declared bounded three-dimensional area at a perceived point within120ft,with exact recipient snapshot and LoE.', 'Another complete source-local geometry preserving a genuinely multiple-recipient area.'],
 'Specify allies,caster,objects versus creatures,partial-body overlap and actual height. No implied whole battlefield,wall penetration,unlimited victims beyond the zone or hidden-target disclosure.')
q(21,[PC],
 'The three printed outcomes are12d6 force,Prone and banished. Core supplies no save type or distribution of these outcomes on success.',
 ['One stated save with independently enumerated damage,Prone and exile results.', 'A complete staged attack/automatic/save model with each printed component independently resolved under its actual defenses.'],
 'Preserve all three real effects. Force immunity is not Prone immunity or a planar guard. Prone is not forced positional movement or a whole-Action hard-control claim; exile may require the actual hard-denial admission.')
q(22,[PC],
 'Damage,Prone and exile order can change target eligibility,concentration,defenses and whether a body exists to transport.',
 ['A precise damage-then-condition-then-exile sequence with revalidation at each applicable checkpoint.', 'Another justified complete operation order,including snapshots and intervening real responses.'],
 'State actual death/Null/survival branches,damage reduced to zero,condition prevention and unsuccessful exile. Already-resolved damage is not refunded by a later blocked transport; no postmortem creature save or duplicate death/return body is manufactured.')
q(23,[PC],
 'Ripped between dimensions and banished do not identify a native plane,destination,transport type or actual exile lifetime; Core says Instantaneous.',
 ['Explicitly extend a named finite private-cell/exile interface with a selected clock and full source-local rules.', 'Select a real destination/transport relation supported by actual current cosmology and a complete admission/lifetime contract.'],
 'Resolve useful positive banishment without inventing a new realm or assuming foreign-game mechanics. A Planar tag alone is not a portal,teleport permission or an exception to actual Anchor/ward predicates.')
q(24,[PC],
 'Area exile must preserve separate bodies,passengers,gear,agency,knowledge and concurrent clocks. Ordinary Banishment has one primary cell and narrowly bounded admission/closure rules.',
 ['Separate per-target exile records/cells with explicit cargo,other-body separation and individual ending.', 'A specifically authored shared exile space with complete geometry,occupancy,agency and independent target-source identities.'],
 'Do not silently merge targets into one creature,make them Incapacitated/stasis,or treat passengers as gear. Preserve current effects/recharge/concentration and lawful visitor/escape behavior. Any source-local cell growth rule is explicitly inherited or newly chosen.')
q(25,[PC],
 'Return can face blocked space,plane wards,source expiry,death,escaped targets or unavailable support. The accepted Banishment terminal endpoint exception is deliberately narrow.',
 ['Explicitly extend that exact return/placement-conflict interface to named Planar Collapse exiles.', 'Author another complete lawful return contract,with no unbounded relocation search or automatic rescue.'],
 'State original plane/anchor,return timing,body fit,squeeze/adjacent/local conflict,actual clocks and available actions. No old-world waypoint cargo teleport,revival,occupant displacement or imaginary Falling while no legal footprint exists. Explain any blocker exception rather than assuming it.')
q(26,[PC],
 'Multiple target exiles,initial rift manifestation,source suppression and rank-qualified removal may have distinct ongoing records after the instantaneous cast.',
 ['Define per-target ongoing exile applications and any parent link,with exact full/local suppression and dispel capture.', 'Use another explicitly bounded source graph that cleanly separates the immediate packet from continued banishment.'],
 'Resolve recast conflicts,shared or individual clocks,concentration if newly selected,one-target removal versus parent removal,and correct closure of each remaining cell. Suppression never replays an instantaneous packet or regenerates departed/dead bodies; other independent continuing effects retain their real rules.')

FINDINGS=[
 'All four are rank9/class17/base26RP,Action,V/S/F. Reverse Gravity Field alone has60ft cast range; the other three have120ft. Eternal Anvil Core duration is1round; the other three are Instantaneous. These source facts are not reopened.',
 'The three Transmutation spells use Druid/Mage/Wizard access. Planar Collapse uses Universal through Cleric/Mage/Wizard; Druid does not acquire it from another class school. No transmutation grant is supplied to Cleric by the group.',
 'Eternal Anvil keeps a massive war-forge hammer,5d12 force and1round Stunned. Skybrand proves one possible effect-only model but its two attacks,command,concentration and60s lifespan do not automatically apply.',
 'Reverse Gravity Field keeps everything in60ft radius moving60ft up with real later fall damage. The current Falling bridge uses up to300ft descent per actual step and min(10,floor(uncontrolledFeet/20))d6; ordinary60ft is3d6,not6d6. Feather Fall is an Action with its own nonzero landing exposure.',
 'Actual Prone is distinct from forced displacement,Stunned and hard Action denial. Force Spike supplies a reviewed example of damage first and a separate Prone-only save,not a mandatory resolution template for these four.',
 'Transmute Flesh to Energy preserves12d10 chosen energy and explicit resistance bypass. Immunity,prevention,sharing,temporary HP,Null provenance,death and physical body loss require their actual separate source rules.',
 'Planar Collapse retains all12d6force/Prone/exile consequences. Exact existing Banishment cell/admission/closure/conflict/terminal-return rules are provided in full but need an explicit extension; no native plane identity or new cosmology is supplied by the name.',
 'The unaccepted Rank8Damage6 return and all eight local findings/correction request are included as proposed comparison evidence. Its559 integrity checks and92-of96 finite diagnostics do not grant semantic acceptance; the six identities are not added to39 accepted-but-unapplied.',
 'Full pending Reverse Gravity/Telekinesis/Disintegrate,catastrophe and storm/control conferences remain comparisons only. Existing authored rules are inherited within exact scope; no rejected fixture geometry or missing Ready concentration event is repeated as an approved example.',
 'Full original cosmology manuscripts,saved website and current owner corrections accompany actual body,equipment,healing,damage,control,clock and class sources. No donor powers,foreign spell imports,Equation reconstruction or Hunt exception is invented.'
]
CASES=[
 'At least two complete positive encounters per identity plus meaningful independent branches. Include actual original caster class17/access/repertoire/automatic features,26RP plus real modifiers,Action/Reaction/Ready and concentration history,initial bodies/gear/geometry,specified RNG,operation stages and expected final state.',
 'Eternal Anvil: genuinely lawful positive5d12force/Stunned use in the actual one-round model; independent miss/save/immunity/hard-guard failure; persistent-object/effect geometry and final disposition where selected. No fabricated free attack or expired-before-use fixture.',
 'Reverse Gravity Field: several actual bodies and objects lift the full legal60ft,with exact support/cargo; a second case includes ceiling or attachment/partial-zone geometry and lawful agency. Resolve real first Fall Marker,60ft3d6 landing,existing mitigation,field ending and overlapping source ordering.',
 'Flesh to Energy: full12d10 type choice and actual resistance bypass; positiveHP/zero/actual death/Null branches,distinct immunity/prevention and temporary HP,body/gear consequences. If an area is selected,prove all geometric recipients and avoid double-counting the primary target.',
 'Planar Collapse: all three printed outcomes succeed on a source-qualified target; independent save/condition defense/blocked exile branches with already-resolved damage retained. Supply multiple actual exiles,cell agency/clocks/cargo,legal escape,removal/expiry and occupied/warded return endpoints.',
 'Every source: real self-damage during Ready requires the actual concentration check before the hold ends; a ray must physically intersect its claimed cover; Greater Dispel captures all eligible applications in its real immutable area. Include actual class-level and body/save values,not the invalid premises flagged in Rank8.',
 'Source packaging is not authored acceptance. Arithmetic/geometry/specification checking is not engine execution; balance,human gameplay,cosmology,all75domains,whole-game and release approval remain distinct.'
]
assert len(Q)==26 and len({x[0] for x in Q})==26
