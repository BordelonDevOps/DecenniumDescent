"""Retain a reproducible source census, not gameplay or complete semantic qualification."""
import hashlib
import json
import re
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
OUT = Path(__file__).resolve().parent
BASELINE = "4abfdd598b48225002fabdec2f8121ce23fb4d49"
MODEL = ROOT / "engine/com.decennium.foundation/Laboratory/Model"
CORE = ROOT / "engine/com.decennium.foundation/Runtime/Core"


def read(path):
    return path.read_text(encoding="utf-8-sig")


def write(name, value):
    (OUT / name).write_bytes((json.dumps(value, indent=2, ensure_ascii=False) + "\n").encode("utf-8"))


def between(text, begin, end):
    return text[text.index(begin):text.index(end, text.index(begin))]


def kinds(text):
    return set(re.findall(r"CommandKind\.(\w+)", text))


session = read(MODEL / "ConnectedExpeditionSession.cs")
host_region = between(session, "private static bool ExposedCommand", "private static SupplyCacheRecord ReachableCache")
helpers = {
    "ClericRepertoireProfile.IsCommand": ("SpellRepertoireRecords.cs", "IsCommand"),
    "SpellCastingProfile.IsUtilityCommand": ("SpellCastingProfile.cs", "IsUtilityCommand"),
    "ShortRestBerth.IsCommand": ("ShortRestRecord.cs", "IsCommand"),
    "ClericLongRestProfile.IsCommand": ("ClericLongRestValidation.cs", "IsCommand"),
    "WoundTreatmentStation.IsCommand": ("WoundTreatmentRecord.cs", "IsCommand"),
}
expanded = set(kinds(host_region))
helper_pins = []
for name, (filename, method) in helpers.items():
    text = read(CORE / filename)
    match = re.search(r"public static bool " + method + r"\(CommandKind kind\)\s*=>[^;]+;", text)
    assert match, name
    expanded.update(kinds(match.group()))
    helper_pins.append({"symbol": name, "path": (CORE / filename).relative_to(ROOT).as_posix(),
                        "line": text[:match.start()].count("\n") + 1, "expression": match.group()})
work_text = read(MODEL / "ConnectedWorkControlHost.cs")
expanded.update(kinds(between(work_text, "private static bool WorkControlCommand", "public CommandQueryResult QueryCommand")))
fill_text = read(MODEL / "TestOnlyFillingPolicy.cs")
fill_helper = re.search(r"(?:public|internal) static bool IsWaterFillCommand\(CommandKind kind\)\s*=>[^;]+;", fill_text)
assert fill_helper
expanded.update(kinds(fill_helper.group()))
assert len(expanded) == 78, sorted(expanded)

# Each entry records semantic distinctions to audit; it does not assert that every
# branch is currently executable or that enumerating these axes qualifies them.
GROUPS = [
    ("tactical", "SelectCombatStance AttackClub AttackCreatureFeature TacticalStep EndRegularTurn EncounterDash UseIntimidatingPresence TearExposedSeal", "All factories for CombatCommands; profile/seat predicates for the additional four kinds", "MOVEMENT_AND_UNARMED_RULE_DECISIONS.md CONNECTED_COMBAT_RULE_DECISIONS.md ORDINARY_ATTACK_RULE_DECISIONS.md"),
    ("responses", "RespondOpportunityAttack ResolveKnockout RespondPress RespondSanctuary", "Actual pending owner/seat; Sanctuary requires admitted casting and selected opponent", "MOVEMENT_AND_UNARMED_RULE_DECISIONS.md"),
    ("travel", "BeginWorldStep SuspendWorldStep ResumeWorldStep BeginReinforcementApproach", "KnownServices walk; declared geometry adds run and controls; companion dose/Cleric selects approach", "SHARED_WORLD_RULE_DECISIONS.md EXPLORATION_MOVEMENT_RULE_DECISIONS.md"),
    ("observation", "Hide Search CancelExplorationHide CancelExplorationSearch", "Ordinary stage Hero Hide/Companion Search; Frightened tactical actor/turn", "OBSERVATION_RULE_DECISIONS.md"),
    ("interaction", "Interact", "Hero reachable selected cache; Companion selected Fishing Trap only", "SUPPLY_CACHE_RULE_DECISIONS.md FISHING_TRAP_RULE_DECISIONS.md"),
    ("inventory", "HandlePortableEquipment OpenPortableContainer ClosePortableContainer HandleInventory PortionInventory EquipPortableItem RemovePortableItem HandleVessel", "Actual party-owned/custodied records; selected vial, focus/flask and cache boundaries", "INVENTORY_RULE_DECISIONS.md PORTABLE_EQUIPMENT_RULE_DECISIONS.md MGT01_INVENTORY_STORAGE_RULE_DECISIONS.md"),
    ("intake", "StartIntake InterruptIntake", "Party inventory; existing ordinary intake and contamination constraints", "INVENTORY_RULE_DECISIONS.md"),
    ("alchemy-use", "UseAlchemyDose", "Actual retained dose with current inventory and recipient authority", "MANUFACTURING_RECIPE14_RULE_DECISIONS.md"),
    ("filling", "StartWaterFill PauseWaterFill ResumeWaterFill CancelWaterFill", "WorkControlSelected and KnownWorkControlTarget; ordinary stable water only", "VESSEL_FILLING_RULE_DECISIONS.md"),
    ("mining", "StartMining PauseMining ResumeMining", "Start is baseline KnownServices; pause/resume require WorkControlSelected", "MINING_RULE_DECISIONS.md"),
    ("research", "StartFormulaResearch PauseFormulaWork ResumeFormulaWork CancelFormulaWork", "Start/resume baseline; pause/cancel require WorkControlSelected; current recipe4 research scope", "FORMULA_RESEARCH_RULE_DECISIONS.md"),
    ("manufacture", "StartManufacturing PauseManufacturing ResumeManufacturing CancelManufacturing ResolveManufacturingQuality", "Start/quality baseline; other controls require WorkControlSelected; one actual recipe4 batch", "MANUFACTURING_RECIPE14_RULE_DECISIONS.md"),
    ("preservation", "StartHarvestPreservationTreatment", "Companion, actual selected blood specimen and native source/age/access", "HARVEST_RULE_DECISIONS.md"),
    ("haven-management", "StartHavenAppraisal StartHavenSale PurchaseHavenMeal StartExpeditionBill CloseExpeditionEpisode StartNextCharterPlan AcceptNextCharter StartCharterAttempt ObserveCharterApproach", "KnownServices exact identities; current host transaction grants and native readiness", "evidence/2026-11-11-mgt10-haven-appraisal/SOURCE_API_REVIEW.md evidence/2026-11-11-mgt10-haven-sale/SOURCE_API_REVIEW.md evidence/2026-11-11-mgt10-haven-meal/SOURCE_API_REVIEW.md evidence/2026-11-11-mgt10-expedition-bill/SOURCE_API_REVIEW.md evidence/2026-11-12-int03-playability/SOURCE_API_REVIEW.md"),
    ("care", "StabilizeCompanion StartWoundTreatment InterruptWoundTreatment ConsumeDecay", "Specific selected care profile/actor/target; treatment supplies are sealed and not ordinary inventory", "evidence/2026-11-13-tac06-companion-stabilization/SOURCE_API_CONTRACT.md evidence/2026-11-13-tac06-wound-treatment/SOURCE_API_CONTRACT.md"),
    ("rest", "BeginShortRest InterruptShortRest BeginMutationShortRest BeginLongRest InterruptLongRest ResolveExpeditionStrainRecovery", "Selected native rest profile; Cleric short-rest candidate retains ClassRecoveryUnsupported", "DAILY_PROVISIONING_RULE_DECISIONS.md evidence/2026-11-14-mgt03-short-rest/SOURCE_API_CONTRACT.md evidence/2026-11-15-mgt03-cleric-long-rest/SOURCE_API_CONTRACT.md"),
    ("advancement", "AwardCharacterMilestone AdvanceCharacterLevel AcquireEarnedSpell", "Selected Cleric settlement/repertoire; actual milestone transaction only", "CHARACTER_ADVANCEMENT_RULE_DECISIONS.md"),
    ("magic", "CastKnownSpell GroundCastingStrain EndSpellConcentration FocusDetectedAura UseHealingRite UseDivineInvocation UseConsecrate", "Exact selected repertoire/casting/RP/Bishop/Consecration and current context/actor", "evidence/2026-11-15-tac08-cleric-casting/APPROVED_CASTING_CONTRACT.md evidence/2026-11-16-chr05-consecration-contract/SOURCE_API_DECISIONS.md evidence/2026-11-23-tac01-ordinary-magic/SOURCE_API_CONTRACT.md"),
]
VARIANTS = {
    "SelectCombatStance": ["Aggressive", "Guarded", "Mobile", "Focused", "Carrying: native NoApplicableCargoPenalty"],
    "AttackClub": ["owned/custodied visible-target club", "OrdinaryOutcome/KnockOutIfEligible/AskIfEligible", "ArmOrReplace/KeepExisting", "regular attack vs Sanctuary gate"],
    "AttackCreatureFeature": ["selected Ferry feature/actual creature seat", "same explicit knockout/Press payload disposition", "Sanctuary admission"],
    "TacticalStep": ["native direction/geometry/movement domain", "ordinary completion/OA suspension/Press continuation"],
    "EndRegularTurn": ["aware stance required", "life/conditions/due events and next slot"],
    "EncounterDash": ["selected Ferry current party turn", "Action and movement allowance"],
    "UseIntimidatingPresence": ["RecoveryOpponent seat selected target subsets", "separate LaterDefender grant", "actual cooldown/turn/visibility"],
    "TearExposedSeal": ["actual observed seal", "tactical vs ordinary activity where admitted", "original suppression endpoint and repeated use"],
    "RespondOpportunityAttack": ["decline", "take with owned weapon", "knockout/Press elections", "ordered reactor and continuation"],
    "ResolveKnockout": ["ordinary outcome", "knock out", "existing attack identity; original Press instruction immutable"],
    "RespondPress": ["decline", "follow the actual offer into the provoker's vacated square; no arbitrary destination election", "nested continuation without speculative execution"],
    "RespondSanctuary": ["Forgo", "regular attack Retarget to each visible legal native target", "Opportunity retarget denied outside original source", "native no-free-loop/continuation rules"],
    "BeginWorldStep": ["walk", "run only where host selected", "scheduled/off-calendar activity", "partial progress/encounter admission"],
    "SuspendWorldStep": ["actual own pending traversal", "partial pose/paid budget preserved"],
    "ResumeWorldStep": ["suspended/waiting traversal", "run/Dash revalidation", "actual geometry/fear/access"],
    "BeginReinforcementApproach": ["actual selected approach", "consent/director parameters", "source entry timing/allowance"],
    "Hide": ["ordinary Hero start token", "tactical party turn", "eligible Guidance election/decline"],
    "Search": ["ordinary Companion start token", "tactical party turn", "eligible Guidance election/decline"],
    "CancelExplorationHide": ["actual own pending hide identity"],
    "CancelExplorationSearch": ["actual own pending search identity"],
    "Interact": ["cache PickWithTools/Open/Interrupt", "trap Set/Pause/Resume/Cancel", "trap Retrieve/PauseRetrieval/ResumeRetrieval", "retrieve explicit receiver/handling request", "trap Abandon exists natively but is not admitted by the session"],
    "HandlePortableEquipment": ["Pickup/Drop/Retrieve", "selected vial Stow in pack", "selected focus Handover consent", "companion Club physical adapter", "ordinary vs tactical allowance"],
    "OpenPortableContainer": ["owned accessible actual closure", "selected packed vial", "protected specimen opening consequences"],
    "ClosePortableContainer": ["owned accessible actual closure", "protected contents"],
    "HandleInventory": ["Hero cache ration Pickup only at host", "rational available amount", "no generic transfer expansion"],
    "PortionInventory": ["exact rational amount", "actual eligible source/unit", "reserved/whole-tender/contaminated exclusions", "age/provenance conserved"],
    "EquipPortableItem": ["selected holy symbol and placement/body constraints"],
    "RemovePortableItem": ["selected holy symbol and current state"],
    "HandleVessel": ["selected flask Pickup/Drop/Retrieve/Stow disposition", "willing party Handover", "opening/contents/custody constraints"],
    "StartIntake": ["ordinary food/water rational amounts", "reservations and exact proportional time", "tactical/unsafe intake unsupported"],
    "InterruptIntake": ["actual own intake", "consumed credit retained and untouched quantity released"],
    "UseAlchemyDose": ["owned actual dose/recipient", "ground/carried/stowed/tactical/Companion selected variants", "actual HP caps/blockers and spent dose"],
    "StartWaterFill": ["authorized accessible source/destination", "positive rational amount/unit/capacity", "two hands and 60 active seconds"],
    "PauseWaterFill": ["active own fill", "retain progress/amount/capacity; release worker/opening"],
    "ResumeWaterFill": ["paused own fill", "remaining active labor and current access/hands"],
    "CancelWaterFill": ["active/paused own fill", "no liquid transfer; release claims"],
    "StartMining": ["actual version/category subsets", "Strength/Wisdom", "hurried false/true", "finite source selection and setup", "conditional failure-victim and critical-recovery preferences", "nonempty AssistantId rejected: requires schema77 unavailable in these factories"],
    "PauseMining": ["setup endpoint", "first-positive removal commitment", "productive removal stage"],
    "ResumeMining": ["Paused", "AwaitingCheck native model branch; genuine producer remains OPEN"],
    "StartFormulaResearch": ["actual guild notes/recipe4", "new attempt after cancellation has zero inherited progress"],
    "PauseFormulaWork": ["active research retains labor/progress/claims"],
    "ResumeFormulaWork": ["Paused retained research", "AwaitingCheck native model branch; genuine producer remains OPEN"],
    "CancelFormulaWork": ["zero labor", "positive labor", "native AwaitingCheck cancellation disposition"],
    "StartManufacturing": ["one actual recipe4 order", "ingredients/age/packaging/known formula and actual work window"],
    "PauseManufacturing": ["unfinished phase loses retained phase labor", "completed phase retained and actual labor preserved"],
    "ResumeManufacturing": ["Paused remaining phases", "AwaitingCheck native model branch; genuine producer remains OPEN"],
    "CancelManufacturing": ["zero labor releases ingredients", "positive labor consumes ingredients", "packaging released and batch permanently closed", "AwaitingChoice disallows cancellation"],
    "ResolveManufacturingQuality": ["actual Exceptional FullYield/Durability", "StandardQuantity native applicability disposition", "suspended clock continuation"],
    "StartHarvestPreservationTreatment": ["actual unspoiled selected specimen", "stabilization vs spoilage endpoint", "real preservative/time/access"],
    "StartHavenAppraisal": ["exact desk/seller/stock", "actual appraisal completion/knowledge"],
    "StartHavenSale": ["exact offer/Companion transaction grant", "actual sale inventory/price/payment and custody"],
    "PurchaseHavenMeal": ["exact offer/Companion transaction grant", "whole tender/one-use serving and native consumption"],
    "StartExpeditionBill": ["exact bill and actual prior contributions/results"],
    "CloseExpeditionEpisode": ["exact episode and native settlement readiness"],
    "StartNextCharterPlan": ["exact plan and current resource/readiness assessment"],
    "AcceptNextCharter": ["exact offer and actual bill/plan agreement"],
    "StartCharterAttempt": ["exact accepted charter and departure readiness"],
    "ObserveCharterApproach": ["actual attempt identity and approach state"],
    "StabilizeCompanion": ["Hero Medicine on actual Companion", "casting Guidance election/decline", "genuine stable/dying life gates"],
    "StartWoundTreatment": ["Hero treats selected Companion Wound", "sealed kit/Supply basket", "source choice and eight-hour attempt"],
    "InterruptWoundTreatment": ["Hero/Companion target binding", "active attempt and spent start costs"],
    "ConsumeDecay": ["selected Hero/fixed significant decaying-organic bed at (1,3); no corpse-selection procedure", "actual once-only use and source feature eligibility"],
    "BeginShortRest": ["Hero exact berth", "explicit zero Hit Dice", "beneficial/nonbeneficial attempts", "Cleric ClassRecoveryUnsupported"],
    "InterruptShortRest": ["actual Hero interval", "native interrupted reward/occupancy"],
    "BeginMutationShortRest": ["selected FleshWarden mutation identity", "actual completed-rest equip", "no invented activation/serum route"],
    "BeginLongRest": ["Companion exact berth", "eight-hour interval/cadence/source-specific recovery"],
    "InterruptLongRest": ["actual own interval", "native damage/explicit interruption"],
    "ResolveExpeditionStrainRecovery": ["actual pending offer point IDs", "native source namespace/priority", "clock continuation"],
    "AwardCharacterMilestone": ["actual Cleric milestone", "Bishop selected later milestone", "narrow world-modification grant"],
    "AdvanceCharacterLevel": ["exact Cleric2 settlement selection", "exact Bishop3 declaration/training/source choices", "earned repertoire atomic transaction"],
    "AcquireEarnedSpell": ["EarnedSpellAcquisitionRequiresAdvancementTransaction", "ClericEarnedAdvancementUnavailable; no new acquisition route"],
    "CastKnownSpell": ["arcane-ward/guidance/purify-food-and-drink/sanctuary/spare-the-dying", "earned detect-magic", "earned Bishop dispel", "actual target/shape/payload", "focus identity/WillingTarget/ElectFocusedDc; willingness payload supplies no authority", "tactical vs admitted OMA calendar", "repertoire-only OrdinarySpellcastingUnsupported"],
    "GroundCastingStrain": ["Companion native Dissonance/context/action"],
    "EndSpellConcentration": ["actual own present concentration effect", "native ending/carry semantics"],
    "FocusDetectedAura": ["opaque authorized aura observation", "native detection/focus/school disclosure"],
    "UseHealingRite": ["Companion/party recipient", "current RP/Action/history/context and conditional Radiance cadence; no Rite recharge", "native cure preference and actual HP/condition gates"],
    "UseDivineInvocation": ["actual Bishop feature entitlement", "1–3 authorized targets and at most one selected cure recipient", "native Conviction/RP/action/recharge"],
    "UseConsecrate": ["admitted center geometry", "native terrain/allegiance/life/healing behavior", "tactical vs admitted ordinary calendar"],
}
listed = [kind for _, group, _, _ in GROUPS for kind in group.split()]
assert len(listed) == len(set(listed)) == 78 and set(listed) == expanded
assert set(VARIANTS) == expanded
files = {p: read(p) for p in sorted(MODEL.glob("*.cs"))}
files.update({p: read(p) for p in sorted(CORE.glob("*.cs"))})
reference_index = {kind: [] for kind in expanded}
for path, text in files.items():
    positions_by_kind = {}
    for line_number, line in enumerate(text.splitlines(), 1):
        for kind in set(re.findall(r"\bCommandKind\.(\w+)\b", line)) & expanded:
            positions_by_kind.setdefault(kind, []).append(line_number)
    for kind, positions in positions_by_kind.items():
        reference_index[kind].append({"path": path.relative_to(ROOT).as_posix(), "lines": positions,
                                      "role": "TEXTUAL_REFERENCE_NOT_PROOF_OF_NATIVE_ASSESSOR_OR_ADMISSION"})
rows = []
used_paths = set()
for family, group, predicate, decisions in GROUPS:
    for kind in group.split():
        refs = reference_index[kind]
        used_paths.update(ROOT / reference["path"] for reference in refs)
        decision_paths = ["docs/unity/" + name for name in decisions.split()]
        for path in decision_paths:
            assert (ROOT / path).is_file(), path
            used_paths.add(ROOT / path)
        rows.append({"id": "HC-OP-" + kind, "kind": kind, "family": family,
                     "profileDisposition": predicate,
                     "hostPredicateSources": ["ConnectedExpeditionSession.ExposedCommand", "ExposedPayload", "KnownTarget", "SeatCommandGrant", "Execute", "Simulation.PreflightCommand"],
                     "semanticBranchesToDisposition": VARIANTS[kind],
                     "relatedPriorDecisionPaths": decision_paths,
                     "sourceReferences": refs,
                     "requiredSurface": ["description", "pure-assessment", "discovery-or-domain", "applicable-choices", "authorized-result", "ordered-observation"],
                     "sourceClauseAndNativeGuardReview": "OPEN_EXACT_BINDING_REQUIRED",
                     "witnessAllocation": "OPEN_GENUINE_ROUTE_OR_PRECISE_EXISTING_UNSUPPORTED_DISPOSITION",
                     "runtimeQualified": False})

factories = []
for m in re.finditer(r"public static ConnectedExpeditionSession\s+(Start\w*)\s*\([\s\S]*?=>\s*new ConnectedExpeditionSession\([\s\S]*?;", session):
    factories.append({"id": m.group(1), "source": "engine/com.decennium.foundation/Laboratory/Model/ConnectedExpeditionSession.cs",
                      "line": session[:m.start()].count("\n") + 1, "exactDeclaration": m.group(),
                      "selectedParameterAndInheritanceReview": "OPEN",
                      "operationPredicate": "Evaluate each HC-OP row against this exact factory and original policy; do not equate candidate membership with executability."})
assert len(factories) == 24
operator_kinds = kinds(between(session, "public ExpeditionActionResult SubmitSessionCommand", "public ExpeditionActionResult AdvanceAutomaticDefender"))
assert operator_kinds == {"AdvanceClock", "EndFixedEncounter"}
capabilities = ["Save", "Restore", "RecoverBackup", "SetSeatEnabled", "AdvanceAutomaticDefender", "SubmitDefenderIntimidatingPresence", "SubmitDefenderSanctuary", "View", "ObserveFerryDecision", "ExplainManufacturingQuality", "ObserveWork", "ObserveConsecration", "ObserveConsecrationHealing", "ObserveExposedSeal"]
inventory = {"schemaVersion": 1, "baseline": BASELINE, "status": "STATIC_CENSUS_AND_SEMANTIC_AUDIT_WORKLIST_NOT_ACCEPTED_CONTRACT",
             "counts": {"seatCommandCandidates": 78, "publicStartupFactories": 24, "sessionOperatorKinds": 2},
             "factoryOperationCrossProduct": "24 factories x 78 candidate dispositions; native payload/source/authority intersections remain explicit OPEN review work, not claimed coverage.",
             "helperExpansion": helper_pins, "factories": factories, "operations": rows,
             "operatorKinds": sorted(operator_kinds), "hostCapabilities": capabilities,
             "notClaimed": ["78 universally executable commands", "exhaustive source clause binding", "complete semantic branch enumeration", "runtime implementation", "test or gameplay execution", "module acceptance"]}
write("OPERATION_INVENTORY.json", inventory)

used_paths.update(CORE / name for name, _ in helpers.values())
used_paths.update([MODEL / "ConnectedWorkControlHost.cs", MODEL / "TestOnlyFillingPolicy.cs",
                  MODEL / "ConnectedExpeditionQualityExplanation.cs", MODEL / "ConnectedExpeditionView.cs",
                  MODEL / "ConnectedCastingView.cs", ROOT / "engine/tools/Open-ConnectedExpedition.ps1",
                  ROOT / "docs/unity/PRE_UNITY_COMPLETION_CONTRACT.json"])
pins = []
paths = sorted(used_paths)
batch_input = "".join(BASELINE + ":" + p.relative_to(ROOT).as_posix() + "\n" for p in paths)
batch = subprocess.check_output(["git", "cat-file", "--batch"], input=batch_input.encode("utf-8"), cwd=ROOT)
offset = 0
for path in paths:
    rel = path.relative_to(ROOT).as_posix()
    newline = batch.index(b"\n", offset)
    header = batch[offset:newline].decode("ascii").split()
    assert len(header) == 3 and header[1] == "blob", (rel, header)
    count = int(header[2])
    blob = batch[newline + 1:newline + 1 + count]
    offset = newline + count + 2
    working = path.read_bytes()
    pins.append({"path": rel, "gitBlobSha256": hashlib.sha256(blob).hexdigest(), "workingSha256": hashlib.sha256(working).hexdigest(),
                 "gitBlobBytes": len(blob), "workingBytes": len(working), "workingEqualsGitBlob": working == blob})
write("CENSUS_SOURCE_PINS.json", {"baseline": BASELINE, "role": "Exact source census inputs; not complete original-rule bindings", "pins": pins})
print(json.dumps({"status": "STATIC_CENSUS_RECONCILED_NOT_RUNTIME_OR_SOURCE_API_ACCEPTANCE", **inventory["counts"],
                  "semanticAxes": sum(len(x["semanticBranchesToDisposition"]) for x in rows), "pinnedFiles": len(pins),
                  "workingBytesDifferFromBaselineBlobs": [x["path"] for x in pins if not x["workingEqualsGitBlob"]]}))
