"""Recover complete ordinary transport source records for the expedition review."""
from pathlib import Path
from datetime import datetime, timezone
import hashlib
import json
import re
import xml.etree.ElementTree as ET
import zipfile

G = Path(__file__).resolve().parents[3]
R = G / "DescentReviewChanges/ReviewBible"
A = G / "docs/audit/2026-10-08/full-game"
NS = {"w": "http://schemas.openxmlformats.org/wordprocessingml/2006/main"}
TAG = "{" + NS["w"] + "}"
PLAYER = "books/player/Decennium_Descent_Player_Rulebook_v6.docx"
CORE = "books/player/Decennium_Descent_Core_Systems_Bible_v2_Known_Descent.docx"
MONSTERS = "books/player/Decennium_Descent_Monster_Manual_of_the_Known_Descent_v2.docx"


def sha(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()


def load(p):
    return json.loads(p.read_text(encoding="utf-8-sig"))


def text(x):
    return "".join(t.text or "" for t in x.findall(".//w:t", NS))


def body(path):
    with zipfile.ZipFile(G / path) as z:
        return ET.fromstring(z.read("word/document.xml")).find("w:body", NS)


def selected(path, ranges):
    out, pi, ti = [], -1, -1
    for bi, elem in enumerate(body(path)):
        if elem.tag == TAG + "p":
            pi += 1
        elif elem.tag == TAG + "tbl":
            ti += 1
        if not any(start <= pi < end for start, end in ranges):
            continue
        if elem.tag == TAG + "p":
            out.append({"kind": "paragraph", "bodyElementIndex": bi, "paragraphIndex": pi, "text": text(elem)})
        elif elem.tag == TAG + "tbl":
            out.append({"kind": "table", "bodyElementIndex": bi, "afterParagraphIndex": pi, "tableIndex": ti, "rows": [[[text(p) for p in cell.findall("w:p", NS)] for cell in row.findall("w:tc", NS)] for row in elem.findall("w:tr", NS)]})
    return {"source": path, "ranges": ranges, "indexConvention": "zero-based direct body paragraphs; half-open ranges; full intervening tables", "blocks": out}


QUESTIONS = [
    ("TR-01", ["FL-17", "FL-16"], "Nine named mounts have partial profiles", "Keep all nine exact Player purchase prices, tactical speeds and pound-carry capacities. Complete actual size, body weight where needed, ability/AC/HP/save/action/sense/training profiles from real sources or explicitly NEW authoring. Do not reverse-engineer Strength or size from a capacity or import another game's stat block. The bounded Known Descent search found no exact mount-name paragraphs, including table paragraphs; that is not a claim about every archive."),
    ("TR-02", ["FL-02", "FL-16", "FL-17"], "Living mount control and agency", "The Player explicitly distinguishes trained controlled mounts from independent intelligent or untrained mounts. Decide how actual training, willingness and compatible anatomy establish that relation, including rider incapacity and loss of contact. The controlled Action list is Dash, Disengage, Dodge; do not silently add an attack or impose crafted-automaton binding. State any shared actor/command budgets by actual governing source. An independent creature keeps its actual agency, rather than becoming a free second player character."),
    ("TR-03", ["FL-03", "FL-16", "FL-17"], "Shared initiative and regular turn order", "Complete 'shares your initiative' with a precise controlled-mount phase, whole-turn order, movement splitting and regular start/end markers. Preserve existing effect clocks, Reaction refreshes, full-Action ceilings and spent movement. Mounting, dismounting, changing control or initiative, and extra rider turns cannot mint new mount turns or refresh existing resources. Decide mid-round entry and a mount whose regular turn already occurred."),
    ("TR-04", ["FL-17"], "Mounting, dismounting and losing the seat", "Preserve half-Speed cost and the printed DC10 Dexterity save when a mount is moved against its will or knocked Prone. Complete reach, remaining movement, Speed0, fitting destination, frequency, prone rider, forced dismount and trigger identity. Distinguish the mount becoming Prone, actual falling and the rider becoming Prone; apply current Core saves and fixed falling procedures without inventing generic natural shifts or repeated saves for one event."),
    ("TR-05", ["FL-17", "FL-16"], "Opportunity attacks and mounted geometry", "The Player permits an opportunity attack provoked by a mount to target rider or mount. Reconcile actual sight, reach, line, legal targeting, Disengage, forced movement, teleport and one Reaction before attack resolution. Define rider position/footprint and area targeting without treating rider and mount as one creature, unlimited cover or a free extra attack."),
    ("TR-06", ["FL-17", "FL-16"], "Mounted feats and motion-triggered class hooks", "Cavalry and Mounted Combatant remain the two exact pending source feat records; they are not granted by the general riding rules. The 17 full class datasets contain no literal mount/vehicle terms under the recorded search, but motion, distance, leap and owner-turn hooks can still interact. Explicitly distinguish moving in a mount's custody from spending the rider's own movement, a leap, forced displacement and movement by another actor. Preserve actual Dragoon Momentum and all source-specific restrictions; no comparison record is promoted."),
    ("TR-07", ["FL-05", "FL-17"], "Tack, feed and source nulls", "Keep all14 original tack/drawn-vehicle/service rows, including the literal comma placeholders and null numeric weights. Barding prints cost×4 but no weight rule or automatically granted armor profile. Complete actual saddle/harness/container weights, capacities, fit and use, feed quantities/species/water needs and stabling service scope. A price per day is not a nutrition quantity; generic small-item weight fallback explicitly excludes these large objects, living mounts and services."),
    ("TR-08", ["FL-17", "FL-18"], "Drawn vehicles and the two sled entries", "Preserve Player Sled20gp and Core Dungeon sled25gp/12Loads as distinct source entries until an explicit decision relates them. Complete frame weight, cargo/passenger limits, pullers, harness, crew, speed, route width/terrain, brakes and actual damage/repair. A Cart's existing30 structuralHP is not its cargo capacity, armor or loaded weight. No unsourced five-times towing multiplier follows from the generic push/drag rule."),
    ("TR-09", ["FL-17", "FL-03"], "Six waterborne vehicles", "Retain all six names/prices and missing speed/capacity fields. Supply actual crew, passengers, cargo, empty mass when required, propulsion, movement/travel rates, draft/space, docking, current/weather and damage procedures or an explicit reviewed exclusion for each option. Price alone does not grant a ship, trained crew or a usable route. Distinguish tactical feet from travel units and preserve named missing fields."),
    ("TR-10", ["FL-02", "FL-04", "FL-17"], "Core porter and pack-animal services", "Core lists hired porter2Loads/2sp per day plus danger pay, skilled bearer3Loads/1gp per day, and pack animal6Loads/5sp per day plus feed. Reconcile these actual service commitments with reviewed body-specific pound/Load capacity, individual purchased mount profiles and actual crew assignments. Define whether the service figure is contracted cargo allowance rather than biological maximum; do not choose silently or double charge purchase/hire/feed. Keep people, wages, consent, information, fatigue and morale distinct from inert cargo."),
    ("TR-11", ["FL-17", "FL-18", "FL-05"], "Hauler construct and specialist transport", "Core's hauler construct20Loads/500gp plus fuel is a service/item source, not automatically a current Tinker feature or reviewed recipe chassis. Complete its actual fuel, service, controls, capacities, body and repair against the appropriate full recipe/device records. Keep Gate caravan100+Loads/10% cargo and teleport extraction Tier×100gp per Load as conditional source services; a price table grants neither availability nor an unknown operative teleport or post-push cosmological permission."),
    ("TR-12", ["FL-17", "FL-25"], "Passengers, casualties and nested cargo", "Apply the reviewed separate effective pounds and casualty Load, including all associated equipment once. The carrier counts a passenger's melded equipment too; Petrified changes body pounds but not casualty Load. Complete shared stretcher teams, vehicle occupants, safety restraints and loading/unloading costs without turning people into generic items or equating Extraction Class with mass. FL-25 owns any old captive-load conflict; preserve voluntary passenger status and actual person agency."),
    ("TR-13", ["FL-10", "FL-11", "FL-13", "FL-17"], "Routes, convoy speeds and transfer events", "Keep the whole Core Route Quality table as evidence, including deferred specialist labels without interpreting them. Reconcile secured/known/contested/collapsed route time modifiers with Loop Progress, mapping and carrying restrictions. One failure cannot apply both overlapping loss procedures without a named decision. Complete transfers between transport methods, physical bottlenecks and whether riders spend any personal movement; no extra travel or duplicate extraction checkpoint follows from relabeling cargo."),
    ("TR-14", ["FL-17", "FL-18", "FL-24"], "Injury, recovery, repairs and rescue", "Living mounts use their actual creature HP/conditions, death significance, food/rest and healing rules. Vehicles use their actual structural damage and approved repair scope; payment or a repair check cannot restore a dead animal or missing chassis. Decide each named source's destruction/stranding and rescue outcomes, including actual time and transport of a disabled mount. Preserve the 220-item equipment approval without promoting these remaining profiles."),
]


def main():
    out = A / "TRANSPORT_SOURCE_PREPARATION.json"
    assert not out.exists(), "Preserve any prior preparation before replacing it"
    selected_blocks = [selected(PLAYER, [(6897, 6934), (8053, 8068)]), selected(CORE, [(6924, 6926)])]
    assert sum(b["kind"] == "paragraph" for s in selected_blocks for b in s["blocks"]) == 54
    assert sum(b["kind"] == "table" for s in selected_blocks for b in s["blocks"]) == 2
    catalog = load(R / "data/playtest/equipment_source_catalog.json")
    records = [x for x in catalog["records"] if x["category"] == "Mounts vehicles and services"]
    assert len(records) == 29
    rows = [b for b in selected_blocks[0]["blocks"] if b["kind"] == "paragraph" and b["text"].startswith("| ")]
    bindings = []
    for record in records:
        matches = [b for b in rows if b["text"].split("|")[1].strip() == record["name"]]
        assert len(matches) == 1, record["name"]
        match = matches[0]
        fields = [s.strip() for s in match["text"].strip("|").split("|")]
        assert fields == [record["sourceFields"][k] for k in ["Item", "Cost", "Speed", "Carrying Capacity"]], record["name"]
        bindings.append({"id": record["id"], "paragraphIndex": match["paragraphIndex"], "sourceExtractLine": record["sourceLine"], "exactBookRow": match["text"], "allFieldsEqual": True})
    mount_records = [x for x in records if x["group"] == "Mounts"]
    assert len(mount_records) == 9
    operative = load(R / "data/playtest/equipment_acquisition_candidate.json")
    active_ids = {x["id"] for x in operative["items"]}
    assert not active_ids.intersection(x["id"] for x in records)
    feats_path = R / "data/public/feat_playtests/catalog.json"
    feats = [x for x in load(feats_path)["feats"] if re.search(r"\b(mount|mounts|mounted|riding)\b", json.dumps(x["sourceObject"], ensure_ascii=False), re.I)]
    assert {x["id"] for x in feats} == {"cavalry", "mounted_combatant"}
    assert all(x["operationalStatus"] == "full-feat-review-pending" for x in feats)
    class_paths = [p for p in sorted((R / "data/public/class_playtests").glob("*.json")) if p.name != "manifest.json"] + [R / "data/public/Decennium_Descent_Bard_Playtest_v0_1.json"]
    assert len(class_paths) == 17
    pattern = re.compile(r"\b(mount|mounts|mounted|riding|saddle|barding|horse|warhound|vehicle|vehicles)\b", re.I)
    class_scan, total_cards = [], 0
    for path in class_paths:
        d = load(path)
        cards = d["cards"]
        total_cards += len(cards)
        class_scan.append({"path": path.relative_to(G).as_posix(), "cardCount": len(cards), "literalMatches": [x for x in cards if pattern.search(json.dumps(x, ensure_ascii=False))]})
    assert total_cards == 1223
    creature_pattern = re.compile(r"\b(camel|donkey|mule|elephant|horse|mastiff|pony|warhound)\b", re.I)
    all_monster_paragraphs = body(MONSTERS).findall(".//w:p", NS)
    monster_matches = [{"allXmlParagraphIndex": i, "text": text(p)} for i, p in enumerate(all_monster_paragraphs) if creature_pattern.search(text(p))]
    sources = [G / PLAYER, G / CORE, G / MONSTERS, R / "data/playtest/equipment_source_catalog.json", R / "data/playtest/equipment_acquisition_candidate.json", feats_path,
               R / "docs/mechanics/EQUIPMENT_ACQUISITION_PLAYTEST.md", R / "docs/mechanics/BODY_EQUIPMENT_PLAYTEST.md", R / "docs/mechanics/COMBAT_ACTION_PLAYTEST.md", R / "docs/mechanics/CORE_RESOLUTION_PLAYTEST.md", R / "docs/mechanics/CONDITIONS_PLAYTEST.md", R / "docs/mechanics/CLASS_PLAYTEST_RULES.md", R / "docs/mechanics/LANGUAGE_COMMUNICATION_PLAYTEST.md", R / "docs/mechanics/DEVICE_LIFECYCLE_PLAYTEST.md", R / "docs/mechanics/GAMEPLAY_LOOP_CANON.md", A / "EXPEDITION_HAVEN_FLOW_SOURCE_PREPARATION.json"] + class_paths
    source_hashes = {p.relative_to(G).as_posix(): {"bytes": p.stat().st_size, "sha256": sha(p)} for p in sources}
    frozen = load(A / "TEACHING_NAVIGATION_EXACT_V1_PREPARATION.json")["manifest"]
    preserved = []
    for rel, meta in frozen.items():
        if rel == "README_TEACHING_EXACT_V1.md":
            continue
        assert sha(G / rel) == meta["sha256"], rel
        preserved.append(rel)
    assert len(preserved) == 217
    d = {"status": "prepared-unsent-transport-source-addendum", "preparedAtUtc": datetime.now(timezone.utc).isoformat(), "scope": "Ordinary transport and mounted-combat source preparation; refine existing expedition cases, without new rules or promotions", "questions": [{"id": key, "parentCases": parents, "title": title, "question": question} for key, parents, title, question in QUESTIONS], "selectedSourceBlocks": selected_blocks, "sourceEquipmentRecords": records, "actualBookBindings": bindings, "counts": {"sourceRecords": len(records), "mounts": 9, "tackDrawnVehiclesServices": 14, "waterborneVehicles": 6, "selectedParagraphs": 54, "fullCoreTables": 2}, "pendingFeatComparisons": feats, "fullClassSourceScan": class_scan, "classCardCount": total_cards, "literalClassScanPattern": pattern.pattern, "literalClassScanLimit": "Zero explicit mount-word cards does not prove absence of motion, custody, control or timing interactions; all17 full class source files remain available for comparison", "knownBestiaryScan": {"source": MONSTERS, "allXmlParagraphs": len(all_monster_paragraphs), "pattern": creature_pattern.pattern, "matches": monster_matches, "limit": "Exact term search in Known Descent including table paragraphs only; no conclusion about other books or sealed material"}, "fullSourceFiles": source_hashes, "activeTeachingDiskPayloadsUnchanged": len(preserved), "sourceFilesModified": 0, "sourceRecordsPromoted": 0, "classCardsPromoted": 0, "featCardsPromoted": 0, "runtimeImplemented": False, "cosmologyInterpreted": False, "humanTested": False}
    out.write_text(json.dumps(d, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    md = ["# Transport and mounted combat source audit", "", "**Prepared and unsent.** This addendum refines FL-17 and the connected expedition cases. It recovers actual source values rather than treating all transport rules as absent. Current equipment, body, combat and language rules remain unchanged.", "", "[Complete records, actual book bindings, original paragraphs and tables](TRANSPORT_SOURCE_PREPARATION.json)", "", "The Player book supplies **nine mounts**, **14 tack/drawn-vehicle/service entries** and **six waterborne entries**, plus its complete mounted-combat subsection. All29 table rows match the preserved equipment source catalog field for field. Missing values remain missing, including literal comma placeholders; none becomes zero or a guessed weight.", "", "Core supplies its full transport-services and route-quality tables. Its generic pack-animal service has6Loads, while the Player mount table supplies individual pound limits. Player Sled20gp and Core Dungeon sled25gp/12Loads remain separate source records. The already-reviewed Cart30 structuralHP is a durability fact, not a completed transport profile.", "", "The Known Descent book contains no exact candidate-mount-name paragraph match, including paragraphs in tables. That bounded search does not prove no source exists elsewhere. Neither generic service rates nor another game's familiar animal profile can substitute for the missing actual creature procedure.", "", "Cavalry and Mounted Combatant are retained in full with their pending feat status. All17 class collections/1223 cards are available for comparison; the recorded literal search has zero mount/vehicle matches, but movement, leap, custody and timing hooks still need explicit adjudication. No class or feat approval follows.", "", "| Question | Existing expedition cases | Decision needed |", "|---|---|---|"]
    md.extend(f"| {key}: {title} | {', '.join(parents)} | {question} |" for key, parents, title, question in QUESTIONS)
    md += ["", "Full evidence retains54 selected Player/Core paragraphs, two complete Core tables and33 whole source files. All217 disk payloads of the live teaching submission remain unchanged. Specialist and Pact-labelled rows are preserved literally; this audit grants no availability, teleport procedure or interpretation of cosmology. Confer after teaching fulfillment with the existing expedition/bestiary/feat work, then author the actual profiles and mounted procedure.", ""]
    (A / "TRANSPORT_SOURCE_AUDIT.md").write_text("\n".join(md), encoding="utf-8")
    assert len(source_hashes) == 33
    assert all(sha(G / rel) == meta["sha256"] for rel, meta in source_hashes.items())
    print(json.dumps({"questions": len(QUESTIONS), "sourceRecords": len(records), "bookBindings": len(bindings), "sourceParagraphs": 54, "sourceTables": 2, "sourceFiles": len(source_hashes), "classCardsComparedByLiteralSearch": total_cards, "pendingFeatComparisons": len(feats), "knownBestiaryExactNameMatches": len(monster_matches), "unchangedTeachingPayloads": len(preserved)}, indent=2))


if __name__ == "__main__":
    main()
