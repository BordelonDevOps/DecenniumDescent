"""Explicit table fields for the fifty separated Curse Boons."""
FIELDS={
'Spiral-Touched':[
'Passive; triggered reroll|0|Self|Permanent bonus; immediate reroll|Reroll 1/long rest',
'Passive; triggered additional Action|1 RC for Action|Self, after another creature’s turn|One additional Action|1/encounter; global action cap',
'Triggered at 0 HP|0|Self|Until start of next regular turn|1/long rest',
'Triggered additional Action; attack avoidance|0|Self|One Action; instantaneous avoidance|Action 1/encounter; avoidance once/round',
'Reaction before round 4|0|Recorded encounter participants|Restore recorded encounter-start state|1/long rest'],
'Wound Eater':[
'Triggered after damaging weapon/touch hit|1 RC|One living non-construct enemy hit|Instantaneous|Once/own turn in real encounter',
'Passive; triggered recovery|0|Self; qualifying living hostile reaches 0 HP|Permanent resistance; instantaneous recovery|Shared one RC refund/round',
'Action|0|One dying hostile living creature touched|Instantaneous|1/short rest; no staged/summoned targets',
'Bonus Action; start-of-turn pulses|2 RC start; 1 RC per later pulse|Up to three living enemies within 10 feet|Concentration; at most three pulses|One aura; once/target/round',
'Action|0|Up to three living enemies within 20 feet|Instantaneous|1/long rest'],
'Soul-Cracked':[
'Passive; triggered reroll|0|Self|Permanent immunity; immediate reroll|Reroll 1/long rest',
'Triggered before a damaging Revelation|Normal Revelation cost|One Revelation’s damage|Until that Revelation resolves|1/encounter',
'Triggered when targeted by Charm/domination|0|Self and effect source|Until end of source’s next turn|1/long rest',
'Passive|0|Self|Permanent|Divination check per direct effect',
'Action|0|Self or willing ally within 15 feet; originator on same plane|Instantaneous|1/long rest'],
'Haunted':[
'Passive; declaration at initiative|0|Self|AC bonus permanent; warning one encounter|AC first attack/round; warning 1/long rest',
'Triggered after single-target attack damage|0|Self and attacker|Immediate reduction; attack penalty through next turn|1/encounter',
'Passive while conscious|0|Self and up to three allies within 15 feet|While in range|Continuous',
'Action|0|Up to three enemies within 15 feet|Up to two rounds; save each turn end|1/long rest',
'Action to summon|0|One spirit scout; one-mile same-plane route limit|10 minutes|1/long rest'],
'Tongues':[
'Passive while chorus unsuppressed|0|Self and up to three hearing allies within 25 feet|While interpreting|Continuous',
'Action; speech required|0|One hearing enemy within 15 feet|Until end of its next turn|1/encounter; hard-denial guard',
'Action; speech required|0|One creature within 15 feet|One question|1/long rest',
'Action; speech required|0|Beasts, plants and willing spirits you can address|1 hour|1/long rest',
'Action; speech required|0|Up to three hearing creatures within 30 feet|Until end of their next turns|1/long rest; hard-denial guard'],
'Burning Blood':[
'Passive; triggered retaliation|0|Self; melee attacker; enemies within 5 feet|Permanent resistance; immediate damage|Retaliation and ignition rider once/round',
'Triggered before damaging Revelation|1 RC plus Revelation’s cost|One Revelation damage roll|Until Revelation resolves|Once per Revelation; no recursive riders',
'Triggered when blood ignites|0; optional 1 RC burst|Up to three allies within 10 feet; three enemies within 15 feet|Bonus through start of next turn|Once/round',
'Triggered on first falling below half HP|0|Up to three enemies within 15 feet|Instantaneous|1/short rest',
'Bonus Action|0|Self; up to three enemies/allies within 15 feet|Three rounds|1/long rest; one pulse/target/round'],
'False Life':[
'Passive; triggered survival|0|Self|Permanent advantage; immediate survival|Survival 1/long rest',
'Action|0|Self|Until voluntarily ended or one minute|1/encounter',
'Triggered when reduced to 0 HP|0|Self|Until end of next regular turn|1/long rest',
'Passive; triggered avoidance|0|Self|Permanent resistance; immediate avoidance|Avoidance once/round',
'Triggered at 0 HP|0|Self; undead within 15 feet|Rise next turn; immunity two rounds|1/long rest'],
'Shattered Mind':[
'Bonus Action|0 for movement; normal RC for Revelation|Self or normal Revelation targets|Immediate; Revelation option forfeits full Action|1/encounter',
'Passive|0|Self|Permanent|Continuous',
'Triggered when starting second sustained Revelation|Normal RC for second Revelation; normal upkeep|Your two active Revelations|Until end of next regular turn|1/encounter; third effect ends both',
'Passive; triggered reroll|0|Self|Permanent Insight bonus; immediate reroll|Reroll 1/short rest',
'Triggered on your turn|Normal RC if activating a Revelation|Self; normal Revelation targets|One additional Action|1/long rest; global action cap'],
'Consumed':[
'Passive; Action to suppress appearance|0|Self|Damage reduction permanent; suppression one hour|Reduction first theme damage/round; suppression 1/long rest',
'Passive; triggered damage rider|0|Self; natural/unarmed target|Permanent|Damage rider once/own turn',
'Triggered on weapon/touch hit|0|One creature hit|Instantaneous|Once/own turn',
'Passive during movement|0|Self; up to three following allies within 5 feet|Cleared route until start of next turn|Continuous while moving',
'Bonus Action|0|Self and up to three allies within 10 feet|Three rounds|1/long rest'],
'Fate-Bound':[
'Triggered before a declared check/save|0|One ally within 30 feet|One named roll before scene ends|1/long rest',
'Triggered after attack roll, before damage|0|One attacker targeting you|Immediate reroll|1/encounter',
'Triggered on ally’s natural 1 save|0|One ally within 25 feet and yourself|Immediate transfer; original effect duration|1/long rest',
'Passive; triggered death-save reroll|0|Self|Permanent save bonus; immediate reroll|Reroll 1/long rest',
'Triggered before declared attack/save|0; lose 1 RC if roll not attempted|One ally within 30 feet|One declared roll before encounter end|1/long rest']}

def boon_fields(name,index):
 values=FIELDS[name][index].split('|')
 assert len(values)==5
 return dict(zip(['activation','cost','rangeAndTarget','duration','frequency'],values))
