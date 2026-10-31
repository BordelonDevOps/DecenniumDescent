#!/usr/bin/env python3
"""Prepare a current-authority, one-identity Faction Incarnate Director packet."""
from __future__ import annotations
import hashlib, json, shutil, zlib
from datetime import datetime, timezone
from pathlib import Path
from zipfile import ZipFile, ZIP_DEFLATED

A = Path(__file__).resolve().parent
ROOT = A.parents[4]
OUT = A / "rank9_faction_incarnate_review_337_prepared_v2"
PK = OUT / "packet"
ARCHIVE = OUT / "DD_Rank9_FactionIncarnate_Review337.zip"
DELIVERY = OUT / "DD_Rank9_FactionIncarnate_Review337_DELIVERY.json"
QUEUE = A / "CURRENT_SPELL_QUEUE_336.json"
PENDING = A / "CURRENT25_PENDING_IDENTITY_AUDIT_336.json"
HANDOFF = A / "CURRENT_HANDOFF_336.json"
CATALOG = ROOT / "DescentReviewChanges/ReviewBible/data/public/spell_playtests/catalog.json"
INDEX = ROOT / "DescentReviewChanges/ReviewBible/data/public/spell_playtests/authored_review_index.json"
CORE = ROOT / "DescentReviewChanges/ReviewBible/data/public/Decennium_Descent_Core_Systems_Data_v2_Known_Descent.json"
OLD = A / "rank9_alignmentfactionpurification5_current_source_287_prepared/CURRENT_SOURCE_CONFERENCE_CANDIDATE_287.json"
RETURN287 = A / "rank9_alignmentfactionpurification5_return287_received/DD_Rank9_AlignmentFactionPurification5_Director_Return287_HELD.zip"
RETURN336 = A / "rank9_alignment_perfection_return336_received/DD_AlignmentPerfection_Director_Return336_HELD.zip"
SPELL, BLOCKER = "faction-incarnate", "AFP211-B03"
AUTH = {"reviewedApplied": 823, "pending": 25, "acceptedUnapplied": 0, "completeStandaloneProcedures": 547, "scopedInterfaces": 173}
SOURCE_PATHS = [
    "DescentReviewChanges/ReviewBible/docs/mechanics/REPUTATION.md",
    "DescentReviewChanges/ReviewBible/src/data/reputation.js",
    "DescentReviewChanges/ReviewBible/docs/mechanics/CREATURE_LIFECYCLE_PLAYTEST.md",
    "DescentReviewChanges/ReviewBible/docs/mechanics/SPELL_INTEGRATION_RULES.md",
    "DescentReviewChanges/ReviewBible/src/data/resonance-economy.js",
    "DescentReviewChanges/ReviewBible/data/public/spell_candidates/abjuration_conjuration_rank4_reviewed_03.json",
    "DescentReviewChanges/ReviewBible/data/public/spell_candidates/abjuration_conjuration_rank5_reviewed_05.json",
    "DescentReviewChanges/ReviewBible/data/public/spell_candidates/ward7_reviewed_136/MODEL.json",
    "DescentReviewChanges/ReviewBible/data/public/spell_candidates/manifestation7_reviewed_137/MODEL.json",
    "DescentReviewChanges/ReviewBible/data/public/spell_candidates/rank8summonstructure5_reviewed_153/MODEL.json",
]

def sha(b: bytes) -> str: return hashlib.sha256(b).hexdigest()
def crc(b: bytes) -> str: return f"{zlib.crc32(b) & 0xffffffff:08x}"
def bind(path: Path) -> dict:
    b = path.read_bytes()
    return {"path": path.relative_to(ROOT).as_posix(), "bytes": len(b), "sha256": sha(b), "crc32": crc(b)}
def load(path: Path): return json.loads(path.read_text(encoding="utf-8"))
def save(path: Path, value): path.write_text(json.dumps(value, indent=2, ensure_ascii=False)+"\n",encoding="utf-8",newline="\n")
def find_id(node, ident):
    if isinstance(node, dict):
        if node.get("id") == ident: return node
        for v in node.values():
            got = find_id(v, ident)
            if got is not None: return got
    elif isinstance(node, list):
        for v in node:
            got = find_id(v, ident)
            if got is not None: return got
    return None

def main():
    marker = OUT / "PREPARATION_AUDIT_337.json"
    if OUT.exists() and any(OUT.rglob("*")):
        if not marker.exists() or load(marker).get("id") != "FACTION-INCARNATE-REVIEW337-PREPARATION-AUDIT":
            raise RuntimeError(f"Refusing to overwrite non-owned output directory: {OUT}")
    PK.mkdir(parents=True, exist_ok=True)
    queue, pending, handoff = load(QUEUE), load(PENDING), load(HANDOFF)
    catalog, index, core = load(CATALOG), load(INDEX), load(CORE)
    spell, index_row = find_id(catalog, SPELL), find_id(index, SPELL)
    core_rows=[]
    def walk(x):
        if isinstance(x,dict):
            if x.get("name")=="Faction Incarnate": core_rows.append(x)
            for v in x.values(): walk(v)
        elif isinstance(x,list):
            for v in x: walk(v)
    walk(core)
    if spell is None or index_row is None or len(core_rows)!=1: raise RuntimeError("Current target source rows are incomplete or ambiguous.")
    with ZipFile(RETURN287) as z:
        d287=json.loads(z.read("DIRECTOR_DECISION.json")); h287=json.loads(z.read("HOLD_REGISTER.json"))
        q287=json.loads(z.read("QUESTION_DISPOSITIONS.json")); cd287=json.loads(z.read("CASE_DISPOSITIONS.json"))
        proc287=json.loads(z.read("PROCEDURES.json")); comp287=json.loads(z.read("COMPARATOR_VERIFICATION.json"))
        dec=next(x for x in d287["decisions"] if x.get("id")==SPELL)
        hold=next(x for x in h287["identityBlockers"] if x.get("id")==BLOCKER)
        questions=[x for x in q287 if x.get("id") in {"FI9-13","FI9-14","FI9-15","FI9-16","FI9-17"}]
        case_ids=["AFP211-FI-profile","AFP211-FI-admission"]
        cases={x:json.loads(z.read(f"cases/{x}.json")) for x in case_ids}
        case_dispositions=[x for x in cd287 if x.get("id") in case_ids]
        prior_procedure=next(x for x in proc287 if x.get("id")==SPELL)
        factions=[x for x in comp287.get("comparators",[]) if x.get("id") in {"faction-paragon","faction-aegis","faction-citadel"}]
        return287_binding=bind(RETURN287)
    with ZipFile(RETURN336) as z:
        d336=json.loads(z.read("DIRECTOR_DECISION.json"))
        e01=d336.get("closedEvidenceFinding",{})
        return336_decision={"reviewId":"Return336","identity":"alignment-perfection","heldIds":d336.get("heldIds"),"acceptedIds":d336.get("acceptedIds"),"appliedIds":d336.get("appliedIds"),"authorityAfter":d336.get("authorityAfter"),"closedEvidenceFinding":e01,"nextPendingIdentity":d336.get("nextPendingIdentity"),"nextBlockerId":d336.get("nextBlockerId")}
    old=load(OLD); old_rec=next(x for x in old.get("records",[]) if x.get("spellId")==SPELL)
    old_catalog=old_rec.get("completeCurrentCatalogSourceAndAccess")
    old_index=old_rec.get("currentIndexEntry")
    if queue.get("currentAuthority")!=AUTH or queue.get("next")!=SPELL or queue.get("activeReview",{}).get("blockerIds")!=[BLOCKER]:
        raise RuntimeError("Queue336 does not designate Faction Incarnate / AFP211-B03 at current authority.")
    if hold.get("spellIds")!=[SPELL] or hold.get("decision")!="hold" or len(questions)!=5 or len(case_dispositions)!=2:
        raise RuntimeError("Return287 target history is incomplete or not a HOLD.")
    if dec.get("accepted") is not False or dec.get("applied") is not False or e01.get("id")!="AFP211-E01" or e01.get("status")!="CLOSED" or e01.get("reopened") is not False:
        raise RuntimeError("Historical hold/comparator boundary does not match the expected sealed record.")
    source_bindings=[]
    for i,rel in enumerate(SOURCE_PATHS):
        path=ROOT/rel
        if not path.is_file(): raise RuntimeError(f"Missing current relevant source: {rel}")
        row=bind(path); row["packetMember"]=f"sources/{i:02d}_{path.name}"; source_bindings.append(row)
    source_diff=[]
    prior_by_path={x.get("path"):x for x in old.get("sourceBindings",[])}
    for row in old.get("sourceBindings",[]):
        path=ROOT/row["path"]
        if not path.is_file(): source_diff.append({"path":row["path"],"status":"MISSING"}); continue
        cur=bind(path)
        if (cur["bytes"],cur["sha256"])!=(row.get("bytes"),row.get("sha256")):
            source_diff.append({"path":row["path"],"old":{"bytes":row.get("bytes"),"sha256":row.get("sha256")},"current":{"bytes":cur["bytes"],"sha256":cur["sha256"]}})
    payload={
      "00_CURRENT_AUTHORITY_336.json":{"authority":AUTH,"queue":bind(QUEUE),"pendingAudit":bind(PENDING),"handoff":bind(HANDOFF),"activeReview":queue.get("activeReview"),"retainedHolds":queue.get("separatelyRetainedHolds",[])},
      "01_CURRENT_FACTION_INCARNATE_CATALOG_ROW.json":spell,
      "02_CURRENT_FACTION_INCARNATE_INDEX_ROW.json":index_row,
      "03_CURRENT_CORE_FACTION_INCARNATE_ROW.json":core_rows[0],
      "04_RETURN287_TARGET_DECISION_AND_HOLD.json":{"historicalAuthorityOnly":d287.get("authorityBefore"),"targetDecision":dec,"identityHold":hold,"priorArchiveBinding":return287_binding},
      "05_RETURN287_TARGET_SOURCE_PROPOSAL.json":{"candidateBinding":bind(OLD),"targetRecord":old_rec,"incompleteProcedureProposal":prior_procedure},
      "06_RETURN287_TARGET_QUESTION_DISPOSITIONS.json":questions,
      "07_RETURN287_TARGET_CASE_DISPOSITIONS.json":case_dispositions,
      "08_RETURN287_PRESERVED_CONDITIONAL_CASES.json":{"caseIds":case_ids,"cases":cases,"dataReplayPreviouslyPassed":True,"completePositiveSpellWitness":False,"completeActorClockWitness":False,"replayedOrReauditedFor337":False},
      "09_FACTION_COMPARATOR_BOUNDARIES.json":{"closedEvidenceFinding":"AFP211-E01","comparators":factions,"scope":"Current index-bound Faction Ally/Champion/Paragon/Aegis/Citadel material is comparison-only. No inherited admission, profile, actions, healing, equipment, authority or resource permission is granted to Faction Incarnate."},
      "10_RETURN336_CURRENT_GROUP_CONTEXT.json":{"return336Archive":bind(RETURN336),"decision":return336_decision,"scope":"Return336 is the immediately prior sealed AFP211-B02 HOLD; its AFP211-E01 boundary remains closed. No B02 procedure or permission transfers to B03."},
      "11_CURRENT_SOURCE_RECONCILIATION.json":{"catalog":bind(CATALOG),"index":bind(INDEX),"core":bind(CORE),"targetCatalogRowEqualsReturn287":old_catalog==spell,"targetIndexRowEqualsReturn287":old_index==index_row,"verifiedCurrentRelevantSources":source_bindings,"historical130SourceBindingDifferenceCount":len(source_diff),"historical130SourceBindingDifferences":source_diff,"priorCandidateSourceSetWasHistoricalNotCurrentAuthority":True},
    }
    for name,value in payload.items(): save(PK/name,value)
    # Include exact source bytes, not excerpts alone.
    for i,rel in enumerate(SOURCE_PATHS):
        src=ROOT/rel; dst=PK/"sources"/f"{i:02d}_{src.name}"; dst.parent.mkdir(parents=True,exist_ok=True); shutil.copyfile(src,dst)
    # Current queue records are included exactly so Director can follow authority and priority.
    for src in (QUEUE,PENDING,HANDOFF,A/"CURRENT_SPELL_REVIEW_SNAPSHOT_336.md"):
        dst=PK/"context"/src.name; dst.parent.mkdir(parents=True,exist_ok=True); shutil.copyfile(src,dst)
    request="""# Director review request — Faction Incarnate / AFP211-B03

Review only Faction Incarnate, one identity. Current queue336 designates it next at 823 reviewed/applied, 25 pending, 0 accepted-unapplied (547 complete standalone procedures; 173 scoped interfaces). The packet binds the exact current catalog, authored-index and Core rows; queue336/handoff/pending audit; the prior B03 HOLD, selected spell-local directions, source proposal, and two prior conditional gate traces; and current faction, companion, lifecycle, spell-integration, and resonance sources. Historical 811/37 authority is not current.

Reassess only AFP211-B03 against the bound current source set. Preserve the native promise, current Conjuration class access, Action, 120 feet, V/S/F, 26 base RP and one-minute concentration. Do not inherit Faction Ally or Champion admission, Paragon/Aegis/Citadel profile, ability, healing, gear, permissions, or reputation effects. They are boundary comparators only. No faction ID, institutional history, authority, member, benefit, resource, or cosmology may be invented.

Decide whether exact sources fully specify: (1) a complete useful source-owned manifestation profile with faction-dependent actions/support, defenses, movement/senses, finite resources, equipment, death and custody; (2) explicit invocation/admission to an actually supported faction and the eligible caster/recipient relationship; and (3) attached-phase command/default/expiry plus shared action/resource limits, source-qualified healing, ordinary zero/Null, standing changes, suppression, ending and gear/return settlement within native concentration. Bind actual faction and caster facts and require two useful complete paid encounters, including budgets, healing/Null/zero, suppression/expiry and custody, before acceptance.

Preserve AFP211-E01 as CLOSED. Do not replay or re-audit AFP211-FI-profile or AFP211-FI-admission; they are prior conditional review-gate components, not casts or positive witnesses. Do not reopen Alignment Ascension/Perfection or transfer their permissions. Do not change canonical files or perform application. If any native content or positive witness remains missing, seal a focused one-identity HOLD with the smallest explicit contracts, exact IDs, counts, authority, and next current pending priority. Attach a sealed ZIP and matching delivery JSON. Application requires a separate exact sealed acceptance.
"""
    (OUT/"REQUEST_337.md").write_text(request,encoding="utf-8",newline="\n")
    rows=[]
    for f in sorted(PK.rglob("*")):
        if f.is_file() and f.name!="MEMBER_MANIFEST.json":
            b=f.read_bytes(); rows.append({"path":f.relative_to(PK).as_posix(),"bytes":len(b),"sha256":sha(b),"crc32":crc(b)})
    save(PK/"MEMBER_MANIFEST.json",{"id":"FACTION-INCARNATE-REVIEW337-PAYLOAD-MANIFEST","payloadMemberCount":len(rows),"members":rows})
    archive_members=[]
    for f in [OUT/"REQUEST_337.md",*sorted(PK.rglob("*"))]:
        if f.is_file():
            b=f.read_bytes(); arc=f.name if f==OUT/"REQUEST_337.md" else f.relative_to(PK).as_posix()
            archive_members.append({"path":arc,"bytes":len(b),"sha256":sha(b),"crc32":crc(b)})
    with ZipFile(ARCHIVE,"w",ZIP_DEFLATED,compresslevel=9) as z:
        z.write(OUT/"REQUEST_337.md","REQUEST_337.md")
        for f in sorted(PK.rglob("*")):
            if f.is_file(): z.write(f,f.relative_to(PK).as_posix())
    ab=ARCHIVE.read_bytes()
    with ZipFile(ARCHIVE) as z:
        names=z.namelist()
        if z.testzip() or len(names)!=len(set(names)) or set(names)!={x["path"] for x in archive_members}: raise RuntimeError("Archive member/index validation failed.")
        for row in archive_members:
            b=z.read(row["path"])
            if (len(b),sha(b),crc(b))!=(row["bytes"],row["sha256"],row["crc32"]): raise RuntimeError(f"Archive member mismatch: {row['path']}")
    delivery={"id":"FACTION-INCARNATE-REVIEW337-DELIVERY","reviewId":"Review337","targetIds":[SPELL],"blockerIds":[BLOCKER],"authority":AUTH,"acceptedIds":[],"appliedIds":[],"decisionRequested":"current-source reassessment; no canonical mutation or application","archive":{"fileName":ARCHIVE.name,"bytes":len(ab),"sha256":sha(ab),"crc32":crc(ab)},"archiveMemberCount":len(archive_members),"payloadMemberCount":len(rows)+1,"members":archive_members,"exactAllowlist":[x["path"] for x in archive_members],"priorReturn287":return287_binding,"priorReturn336":bind(RETURN336),"sourceSetBindings":source_bindings,"sourceChecks":{"currentCatalogRowMatchesReturn287":old_catalog==spell,"currentIndexRowMatchesReturn287":old_index==index_row,"caseReplayOrReaudit":False},"nextIfHeld":"Determine from current queue and sealed decision; no guessed priority."}
    save(DELIVERY,delivery)
    checks=[
      {"id":"current-authority-and-priority","passed":queue.get("currentAuthority")==AUTH and queue.get("next")==SPELL and queue.get("activeReview",{}).get("blockerIds")==[BLOCKER]},
      {"id":"exact-target-source-rows","passed":spell.get("id")==SPELL and index_row.get("id")==SPELL and len(core_rows)==1 and core_rows[0].get("name")=="Faction Incarnate"},
      {"id":"prior-hold-and-contract-scope","passed":hold.get("id")==BLOCKER and hold.get("spellIds")==[SPELL] and [x.get("id") for x in questions]==["FI9-13","FI9-14","FI9-15","FI9-16","FI9-17"]},
      {"id":"prior-components-retained-no-replay","passed":len(cases)==len(case_dispositions)==2 and all(x.get("completeSpellWitness") is False for x in case_dispositions)},
      {"id":"closed-shared-boundary","passed":e01=={"id":"AFP211-E01","status":"CLOSED","reopened":False}},
      {"id":"no-accepted-or-applied-target","passed":dec.get("accepted") is False and dec.get("applied") is False and hold.get("accepted") is False and hold.get("applied") is False},
      {"id":"all-current-source-files-bound","passed":len(source_bindings)==len(SOURCE_PATHS) and all((ROOT/x["path"]).is_file() and all(bind(ROOT/x["path"])[k]==x[k] for k in ("path","bytes","sha256","crc32")) for x in source_bindings)},
      {"id":"archive-and-manifest-integrity","passed":len(archive_members)==len(names)==len(set(names)) and not ZipFile(ARCHIVE).testzip()},
    ]
    if not all(x["passed"] for x in checks): raise RuntimeError("Preparation audit failed: "+json.dumps(checks))
    save(marker,{"id":"FACTION-INCARNATE-REVIEW337-PREPARATION-AUDIT","recordedAtUtc":datetime.now(timezone.utc).isoformat(timespec="seconds"),"status":"PASS","checks":checks,"checkCount":len(checks),"passed":sum(x["passed"] for x in checks),"failed":0,"archive":{"path":ARCHIVE.relative_to(ROOT).as_posix(),"bytes":len(ab),"sha256":sha(ab),"crc32":crc(ab)},"delivery":{"path":DELIVERY.relative_to(ROOT).as_posix(),"bytes":DELIVERY.stat().st_size,"sha256":sha(DELIVERY.read_bytes())},"memberCount":len(archive_members),"authority":AUTH,"target":SPELL,"blocker":BLOCKER,"canonicalMutation":False})
    print(json.dumps({"status":"PASS","checks":len(checks),"archive":str(ARCHIVE),"bytes":len(ab),"sha256":sha(ab),"delivery":str(DELIVERY),"members":len(archive_members),"sourceFiles":len(source_bindings),"historicalSourceDiffs":len(source_diff)},indent=2))

if __name__=="__main__": main()