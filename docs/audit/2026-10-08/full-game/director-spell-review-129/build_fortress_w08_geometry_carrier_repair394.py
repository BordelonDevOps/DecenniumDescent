from __future__ import annotations
import copy, hashlib, json, math, zipfile
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent
BASE = ROOT / "fortress_w08_occupied_antimagic_prebuild_386"
OUT = ROOT / "fortress_w08_occupied_antimagic_repair_394"
ZIP_NAME = "DD_Rank9_ConjureDemiplaneFortress_PG328-W08_GeometryCarrierRepair394_TESTONLY.zip"
PREBUILD = "PG328-W08_OCCUPIED_ANTIMAGIC_PREBUILD_TESTONLY.json"
MANIFEST = "PG328-W08_PREBUILD_SOURCE_BINDINGS_394.json"
GEOMETRY = "PG328-W01_W08_OCCUPIED_PANEL_GEOMETRY_PROPOSAL_394_TESTONLY.json"
CARRIER = "PG328-W08_Q27_CARRIER_BOUNDS_PROPOSAL_394_TESTONLY.json"
TERMINATION = "OWNER_PG328_W08_FIELD_TERMINATION_PROPOSAL_386_TESTONLY.json"
REQUEST = "PG328-W08_DIRECTOR_REVIEW_REQUEST_394.json"
DELIVERY = "DD_Rank9_ConjureDemiplaneFortress_PG328-W08_GeometryCarrierRepair394_TESTONLY_DELIVERY.json"
CASE_SHA = "f12414164a641a6b8912b43e8f426f027772f3a58d92dbadfcbd45b4f5b14900"
SPACE = "RANK9PLANARGATES5129-CONJURE-DEMIPLANE-FORTRESS-B/occupied-antimagic/cast1/space"
NOW = datetime.now(timezone.utc).isoformat(timespec="seconds").replace("+00:00", "Z")

def sha(b): return hashlib.sha256(b).hexdigest()
def put(p, obj):
    b=(json.dumps(obj,ensure_ascii=False,indent=2)+"\n").encode("utf-8")
    p.parent.mkdir(parents=True,exist_ok=True); p.write_bytes(b); return b
def ptr(s): return s.replace("~","~0").replace("/","~1")

def main():
    OUT.mkdir(parents=True,exist_ok=True)
    base_dir=BASE
    old_packet_path=base_dir/PREBUILD
    old_packet_bytes=old_packet_path.read_bytes()
    old_manifest=json.loads((base_dir/"PG328-W08_PREBUILD_SOURCE_BINDINGS_386.json").read_text(encoding="utf-8"))
    old_zip_path=base_dir/"DD_Rank9_ConjureDemiplaneFortress_PG328-W08_Prebuild386_DirectorRepair.zip"
    old_zip=zipfile.ZipFile(old_zip_path)
    old_zip_sha=sha(old_zip_path.read_bytes())
    packet=json.loads(old_packet_bytes)

    # Revised candidate point is inside the proposed tower interior.
    center=[16,12,8]
    panel={"x":[12.5,17.5],"y":[7.5,12.5],"z":0}
    corners=[[panel["x"][0],panel["y"][0],0],[panel["x"][1],panel["y"][0],0],
             [panel["x"][0],panel["y"][1],0],[panel["x"][1],panel["y"][1],0]]
    distances=[math.dist(center,p) for p in corners]
    range_ft=math.sqrt((center[0]-15)**2+(center[1]-10)**2+center[2]**2)
    assert max(distances)<20 and panel["z"]==0
    assert all(0<=panel[a][0]<panel[a][1]<=120 for a in ("x","y"))

    geometry={
      "id":"PG328-W01-W08-OCCUPIED-PANEL-GEOMETRY-PROPOSAL-394",
      "createdAtUtc":NOW,
      "status":"PROPOSED_TEST_ONLY_INPUT_PENDING_OWNER_ADOPTION_AND_DIRECTOR_REVIEW",
      "supersedes":"PG328-W01-W08-OCCUPIED-PANEL-GEOMETRY-PROPOSAL-386",
      "scope":{"witnessId":"PG328-W08","subWitnessId":"PG328-W01",
        "caseId":"RANK9PLANARGATES5129-CONJURE-DEMIPLANE-FORTRESS-B/occupied-antimagic",
        "fixtureMutated":False,"canonicalGeometryChanged":False,"actualCastPerformed":False,
        "W01CompatibleDamageObligationCompleted":False,"ownerAdoptionRequired":True},
      "sourceBindings":[
        {"path":"payload/rules/PG328_QUESTION_DISPOSITIONS.json#/questions/2/answer",
         "sha256":"149d4098591799f51afa37837ccca722eb9ae08c3ea437c640d943f33b1bb637",
         "use":"Q23 defines the existing Fortress envelope, 20x20 corner towers, stairs, floors and 5x5 structural panels, while keeping the exact support graph unresolved."},
        {"path":"Return284_HELD.zip#cases/RANK9PLANARGATES5129-CONJURE-DEMIPLANE-FORTRESS-B__occupied-antimagic.json#/final/actors/A",
         "sha256":CASE_SHA,"use":"A at [15,10,0], Medium bodyBox [5,5,6], two hands, focus accessible, and focus-A/pack-A/cargo-A equipment."},
        {"path":"Return284_HELD.zip#cases/RANK9PLANARGATES5129-CONJURE-DEMIPLANE-FORTRESS-B__occupied-antimagic.json#/final/spaces/"+ptr(SPACE)+"/support",
         "sha256":CASE_SHA,"use":"Inherited aggregate support z=0 over [0,120]x[0,120]; proposed local panel must instantiate this existing patch, not add an independent footing."},
        {"path":"payload/sources/ANTIMAGIC_FIELD_MODEL_149.json#/spells/2/procedure",
         "sha256":"ceeff51cb3b9e8000bf845e299d4d9e66b46792133ae5931ad823ce98ea51e57",
         "use":"Fixed-center 20ft field; actual-solid total-cover clipping is checked against explicit local geometry."}],
      "spaceEnvelope":{"spaceId":SPACE,"inheritedBoundsFeet":[0,120,0,120,0,40],
        "inheritedSupport":{"z":0,"boundsXY":[0,120,0,120]},
        "courtyardBoundsXY":[5,115,5,115],"noBoundsOrSupportExpansion":True,
        "panelOutsideEnvelope":False},
      "proposedLocalFortressInstantiation":{
        "status":"Scoped test-only local layout; not an unbound campaign fact.",
        "partOfExistingSource":"The existing PG200 Fortress effect and generated space in the bound case; no new space or spell source.",
        "towerPlacementsFeet":{
          "southwest":{"x":[5,25],"y":[5,25],"z":[0,40]},
          "southeast":{"x":[95,115],"y":[5,25],"z":[0,40]},
          "northwest":{"x":[5,25],"y":[95,115],"z":[0,40]},
          "northeast":{"x":[95,115],"y":[95,115],"z":[0,40]}},
        "southwestTower":{
          "id":"W08-SW-TOWER","boundsFeet":{"x":[5,25],"y":[5,25],"z":[0,40]},
          "wallThicknessFeet":5,
          "wallSolids":[
            {"id":"W08-SW-WALL-W","x":[5,10],"y":[5,25],"z":[0,40]},
            {"id":"W08-SW-WALL-E","x":[20,25],"y":[5,25],"z":[0,40]},
            {"id":"W08-SW-WALL-N","x":[5,25],"y":[20,25],"z":[0,40]},
            {"id":"W08-SW-WALL-S","x":[5,25],"y":[5,10],"z":[0,40],"subtract":"W08-SW-DOOR-S"}],
          "southDoor":{"id":"W08-SW-DOOR-S","clearApertureFeet":{"x":[12.5,17.5],"y":[5,10],"z":[0,8]},
            "sizeFeet":[5,8],"state":"open; no door leaf occupies aperture in proposed branch"},
          "openInterior":{"x":[10,20],"y":[10,20],"z":[0,40]},
          "floorSurfacesFeet":[0,10,20,30,40],
          "stairPath":{"boundsFeet":{"x":[15,20],"y":[15,20],"z":[0,40]},
            "widthFeet":5,"reserved":True,"intersectsPanelRays":False}},
        "perimeterAndOtherStructures":{
          "outerWalls":"Q23 perimeter walls are 5ft thick and 30ft high at x/y 0..5 and 115..120; none of the candidate panel rays reaches them.",
          "otherTowers":"The other three towers are at the listed opposite corners and do not intersect the panel rays.",
          "otherLocalSolids":[],"noUnlistedObstructionAssumed":True}},
      "occupiedPanel":{
        "id":"W08-FLOOR-PANEL-A-01","partOf":"W08-SW-TOWER / existing PG200 Fortress source",
        "planSizeFeet":[5,5],"surfaceBoundsFeet":panel,"areaSquareFeet":25,
        "AC":17,"HP":60,
        "thickness":"Q23 does not specify floor-panel thickness. No positive-thickness prism is asserted; the panel is proposed only as a structural surface on the inherited z=0 support datum.",
        "AContactFootprint":{"x":[12.5,17.5],"y":[7.5,12.5]},
        "supportGraph":{
          "existingGeneratedSpace":SPACE,
          "existingAggregateSupportPointer":"/final/spaces/"+ptr(SPACE)+"/support",
          "testOnlyInstantiation":"The panel is proposed as the 25 sq ft structural floor patch represented by the matching region of the existing aggregate z=0 support plane.",
          "edges":[
            {"from":SPACE,"to":"W08-SW-TOWER","relation":"existing Fortress source contains proposed corner tower"},
            {"from":"W08-SW-TOWER","to":"W08-FLOOR-PANEL-A-01","relation":"tower contains the named ground-floor structural panel"},
            {"from":"existing aggregate support patch z=0","to":"W08-FLOOR-PANEL-A-01","relation":"same inherited support datum; no additional footing or support plane"},
            {"from":"W08-FLOOR-PANEL-A-01","to":"A","relation":"supports A's full 5x5 ground-contact footprint"}],
          "noIndependentFooting":True,"noNewSpace":True},
        "occupancy":{"AFeetPosition":[15,10,0],"bodyBoundsFeet":{"x":[12.5,17.5],"y":[7.5,12.5],"z":[0,6]},
          "groundContactZ":0,"doorwayFit":"A's footprint aligns with the 5x8 south aperture; body height 0..6 fits within aperture height 0..8."}},
      "fieldIntersectionAndCover":{
        "centerFeet":center,"centerCandidateRevision":"Moved from 386's [20,10,8], which lay on the proposed east wall, into the proposed open interior.",
        "centerRangeFromAFeet":round(range_ft,6),"radiusFeet":20,
        "panelCornerPointsFeet":corners,"panelCornerDistancesFeet":[round(x,6) for x in distances],
        "farthestPanelPointFeet":corners[distances.index(max(distances))],
        "farthestPanelDistanceFeet":round(max(distances),6),"sphereContainsWholePanelSurface":max(distances)<20,
        "southWallCrossings":[
          {"target":p,"crossingAtY10":{"x":round(center[0]+(p[0]-center[0])*((center[1]-10)/(center[1]-p[1])),6),
             "z":round(center[2]*(1-((center[1]-10)/(center[1]-p[1]))),6)} if p[1]<10 else None}
          for p in corners],
        "solidReview":"For targets with y<10, the line crosses the south wall only inside x=12.5..17.5,z=0..8 aperture; all other line portions remain inside open interior. Rays do not intersect other tower walls, reserved stair path, upper floors, or perimeter walls. The ground floor is the target surface itself; no penetration through a separate solid is assumed.",
        "solidsEnumerated":["four 5ft tower walls, z=0..40, with the exact 5x8 south opening",
          "tower floor surfaces z=0,10,20,30,40","reserved 5ft internal stair path","Q23 perimeter walls"],
        "AIsIntendedOccupant":"A is the expressly declared occupant; its own body is not treated as an architectural total-cover solid. Director should flag any contrary interpretation.",
        "secondaryWestWallCheck":{"pointFeet":[5,10,15],"distanceTo394CenterFeet":round(math.dist(center,[5,10,15]),6),
          "calculation":"sqrt((16-5)^2+(12-10)^2+(8-15)^2)=sqrt(174)=13.190906ft",
          "historical386Comparison":"Old center [20,10,8] gave sqrt(274)=16.552945ft; not the candidate center in 394."},
        "fieldClippingConclusion":"Only the named panel's surface intersection is assessed; no field penetration through a wall is inferred."},
      "Q27TriggerQuestion":"If this geometry is adopted and Director-reviewed, does suppression of the surface panel under A's full footprint satisfy PG9-Q27's occupied-structural-region trigger? This proposal does not decide the rule.",
      "adoptionBoundary":"Test-only geometry premise; not campaign fact, no W01 compatible-damage completion, no PG200-B06 clearance, no W08 acceptance."}

    # Proposed carrier arrangement uses explicit hand/strap relations; item
    # boxes are clear of each other, A, tower walls, and stair path.
    anchor=[15,10,0]
    exterior=[15,0,0]
    rel={
      "focus-A":{"x":[2.5,3.0],"y":[0.75,1.25],"z":[3.0,3.5]},
      "pack-A":{"x":[-0.25,0.25],"y":[2.5,3.0],"z":[2.0,2.5]},
      "cargo-A":{"x":[0.25,1.25],"y":[2.5,3.5],"z":[1.0,2.0]}}
    def translate(b,a):
        return {k:[b[k][0]+a[i],b[k][1]+a[i]] for i,k in enumerate(("x","y","z"))}
    before={k:translate(v,anchor) for k,v in rel.items()}
    after={k:translate(v,exterior) for k,v in rel.items()}
    body_before={"x":[12.5,17.5],"y":[7.5,12.5],"z":[0,6]}
    body_after={"x":[12.5,17.5],"y":[-2.5,2.5],"z":[0,6]}
    def overlap(a,b):
        return all(min(a[k][1],b[k][1])>max(a[k][0],b[k][0]) for k in ("x","y","z"))
    assert all(not overlap(v,body_before) for v in before.values())
    assert all(not overlap(before[x],before[y]) for x,y in (("focus-A","pack-A"),("focus-A","cargo-A"),("pack-A","cargo-A")))
    assert all(not overlap(v,body_after) for v in after.values())
    carrier={
      "id":"PG328-W08-Q27-CARRIER-BOUNDS-PROPOSAL-394","createdAtUtc":NOW,
      "status":"PROPOSED_TEST_ONLY_PLACEMENT_INPUT_PENDING_DIRECTOR_REVIEW",
      "supersedes":"PG328-W08-Q27-CARRIER-BOUNDS-PROPOSAL-386",
      "scope":{"witnessId":"PG328-W08","caseId":"RANK9PLANARGATES5129-CONJURE-DEMIPLANE-FORTRESS-B/occupied-antimagic",
        "candidateQ27ProjectionOnly":True,"fixtureMutated":False,"terminalStateExecuted":False,"ownerAdoptionRequired":True},
      "sourceBindings":[
        {"path":"Return284_HELD.zip#cases/...occupied-antimagic.json#/final/actors/A","sha256":CASE_SHA,
          "use":"Anchor, orientation, body bounds, two hands, equipment, and casting access."},
        {"path":"Return284_HELD.zip#cases/...occupied-antimagic.json#/final/items/focus-A","sha256":CASE_SHA,"use":"0.5ft cube, A custody; held in left hand."},
        {"path":"Return284_HELD.zip#cases/...occupied-antimagic.json#/final/items/pack-A","sha256":CASE_SHA,"use":"0.5ft cube, A custody; clipped to its own harness point."},
        {"path":"Return284_HELD.zip#cases/...occupied-antimagic.json#/final/items/cargo-A","sha256":CASE_SHA,"use":"1ft cube, A custody; clipped to its own belt point."},
        {"path":"payload/sources/BODY_EQUIPMENT_PLAYTEST.md#Placement and involuntary endings; #Carrying and Load",
          "sha256":"5fa622f43b6948e7e991f1ca5a237de584900e92cfd4f37eed47586d73222039",
          "use":"Explicit placement, identity, custody and collision constraints."},
        {"path":GEOMETRY,"use":"Proposed tower interior and open doorway used for pre-cast local checks."}],
      "bodyConvention":{"plane":SPACE,"feetAnchor":anchor,"orientation":[1,0,0],
        "bodyBoundsFeet":body_before,"relativeAxes":"x forward; y left; z up."},
      "arrangement":[
        {"id":"focus-A","owner":"A","custodian":"A","sizeFeet":[0.5,0.5,0.5],
          "relativeBoundsFeet":rel["focus-A"],"relation":"Held in left hand at forward-left reach point; focus accessible. Right hand remains free for somatic components.",
          "preCastWorldBoundsFeet":before["focus-A"],"postReturnWorldBoundsFeet":after["focus-A"]},
        {"id":"pack-A","owner":"A","custodian":"A","sizeFeet":[0.5,0.5,0.5],
          "relativeBoundsFeet":rel["pack-A"],"relation":"Independently clipped to left-side torso harness; not supported by contact with cargo-A.",
          "preCastWorldBoundsFeet":before["pack-A"],"postReturnWorldBoundsFeet":after["pack-A"]},
        {"id":"cargo-A","owner":"A","custodian":"A","sizeFeet":[1,1,1],
          "relativeBoundsFeet":rel["cargo-A"],"relation":"Independently clipped to belt loop; not supported by contact with pack-A.",
          "preCastWorldBoundsFeet":before["cargo-A"],"postReturnWorldBoundsFeet":after["cargo-A"]}],
      "insideFortressCheck":{"towerInteriorBoundsFeet":{"x":[10,20],"y":[10,20],"z":[0,40]},
        "doorOpeningFeet":{"x":[12.5,17.5],"y":[5,10],"z":[0,8]},
        "AWholeFootprintFitsDoorway":True,"itemsInsideClearInterior":True,
        "itemsAvoidWallsAndStairs":True,"noPositiveVolumeItemBodyOverlap":True,
        "noPositiveVolumeItemItemOverlap":True,"allItemAttachmentsExplicit":True},
      "postReturnCheck":{"exteriorFeetAnchor":exterior,"bodyBoundsFeet":body_after,
        "outsideBodies":{"B":{"x":[-2.5,2.5],"y":[12.5,17.5],"z":[0,6]},
          "C":{"x":[-2.5,2.5],"y":[-2.5,2.5],"z":[0,6]},
          "D":{"x":[2.5,7.5],"y":[2.5,7.5],"z":[0,6]}},
        "allItemsAvoidPositiveVolumeOverlapWithBody":True,
        "allItemsAvoidPositiveVolumeOverlapWithB_C_D":True,
        "custody":"Same item IDs and A custody; no item created, lost, consumed or transferred."},
      "loadAndHands":{"carriedLoad":1.2,"carriedWeightLb":12,"loadChanged":False,
        "hands":2,"leftHandHoldsFocus":True,"rightSomaticHandFree":True,
        "castOrTerminalEventExecuted":False},
      "reviewLimit":"Proposed arrangement only. Do not update case bytes or certify terminal placement until separately reviewed and adopted."}

    request={
      "id":"PG328-W08-DIRECTOR-REVIEW-REQUEST-394","createdAtUtc":NOW,
      "scope":"Corrected W08 geometry/carrier inputs for the Return284 occupied-antimagic branch only.",
      "supersedesPrebuild386Sha256":sha(old_packet_bytes),
      "reviewQuestions":[
        "Does one named z=0 5x5 surface panel correctly instantiate the existing aggregate support patch inside the unchanged envelope, with no added footing/space? Is a surface without invented thickness adequate, or is another exact scoped premise required?",
        "Do the explicit southwest tower walls, open 5x8 doorway, floor elevations, stair path and center-to-panel rays reconcile the local geometry and total-cover rule?",
        "Is revised unexecuted center [16,12,8] a valid candidate within range and sphere bounds, with later perception/line of effect still to be checked?",
        "Does this occupied panel input address Q27 narrowly while leaving W01 compatible damage and PG200-B06 unresolved?",
        "Do proposal 394's hand/strap relations, clear right hand, accessible focus, item custody, bounds and inside/after-return collision checks pass?",
        "Is unchanged field-termination proposal 386 coherent for separate owner adoption?",
        "What exact remaining repair or authorization precedes an integrated W08 witness?"],
      "doNot":["cast Antimagic Field","mutate case/fixture bytes","adopt either W08 proposal",
        "settle/terminate the Fortress or field","accept/apply Fortress","clear PG200-B06",
        "change any hold/seal or queue count"],
      "queue":{"applied":828,"pending":20,"acceptedUnapplied":0}}

    # Update only the proposed candidate view; original case member remains byte-exact.
    cast=packet["proposedCastState"]["proposedCastAfterRefresh"]
    cast["centerCandidate"].update({"feet":center,"distanceFromAFeet":round(range_ft,6),
      "within20Feet":range_ft<=20,"perceivedPointAndLineOfEffectMustBeRechecked":True,
      "geometryProposal":"394 only; neither adopted nor executed"})
    cast["candidateHistoryEntry"]["targetCenterFeet"]=center
    cast["postCommitHistoryAppend"]["spellHistory"]["targetCenterFeet"]=center
    packet["candidateGeometry"]={
      "candidateOnly":True,"samePlaneAsCasterAndFortressStructure":SPACE,
      "centerFeet":center,"radiusFeet":20,"casterAFeet":[15,10,0],
      "centerRangeFeet":round(range_ft,6),
      "sourceGeometry":{"source":"Q23 answer plus inherited case and proposal 394",
        "bounds":[0,120,0,120,0,40],"courtyard":[5,115,5,115],"support":{"z":0,"bounds":[0,120,0,120]},
        "wallThicknessFeet":5,"outerWallHeightFeet":30,"towerProposal":"394"},
      "occupiedPanelProposal394":geometry["occupiedPanel"],
      "fieldIntersectionAndCoverProposal394":geometry["fieldIntersectionAndCover"],
      "secondaryWestWallCandidate":{"point":[5,10,15],"distanceFromNewCenterFeet":round(math.dist(center,[5,10,15]),6),
        "distanceFromOld386CenterFeet":16.552945},
      "triggerRule":"Do not establish Q27 until geometry adoption, Director review, and actual paid-field evidence."}
    packet["conditionalTerminalPlan"]["placementBoundsProposal"]="PG328-W08-Q27-CARRIER-BOUNDS-PROPOSAL-394"
    packet["openRequirementsBeforeIntegratedWitness"][0]["requirement"]="Review proposal 394's support patch, tower/opening/stair geometry, and actual center-to-panel rays; then consider a scoped W01 Q27 sub-witness."
    packet["openRequirementsBeforeIntegratedWitness"][0]["sourceStatus"]="Proposal 394 is unadopted and awaits Director review; W01 compatible damage remains open."
    packet["openRequirementsBeforeIntegratedWitness"][4]["requirement"]="Only after accepted panel predicate and terminal contract, build reversible integrated W08 witness with proposal 394 carrier bounds."
    packet["directorReviewRequest"]["questions"]=[
      "Does proposal 394 validly bind the 5x5 panel to the inherited z=0 support and existing Fortress without extending the envelope or adding an independent footing?",
      "Do the proposed southwest tower, door aperture, actual walls/floors/stairs and listed panel rays avoid total cover without assuming field penetration?",
      "Is the revised [16,12,8] center candidate and all range/sphere math correct, pending later perception and line-of-effect verification?",
      "Is the panel-under-A premise sufficient for a narrow Q27 proposal while leaving W01 compatible damage open?",
      "Do the exact carrier/worn/held arrangement and collision checks pass inside the tower and after return?",
      "Is termination proposal 386 coherent for separate owner adoption?",
      "What is the exact next step before integrated W08 construction?"]
    packet["proposedGeometryProposal394"]={"path":GEOMETRY,"status":geometry["status"]}
    packet["proposedCarrierBounds394"]={"path":CARRIER,"status":carrier["status"]}
    packet["proposedGeometryProposal386"]["status"]="SUPERSEDED_BY_PROPOSAL_394"
    packet["proposedCarrierBounds386"]["status"]="SUPERSEDED_BY_PROPOSAL_394"
    packet["geometryCarrierRepair394"]={"priorPrebuild386Sha256":sha(old_packet_bytes),
      "geometryProposalPath":GEOMETRY,"carrierProposalPath":CARRIER,
      "terminationProposalPath":TERMINATION,"requestPath":REQUEST,
      "fixtureMutated":False,"actualCast":False,"ownerAdoptionOf394":False}
    packet["id"]="PG328-W08-OCCUPIED-ANTIMAGIC-PREBUILD-GEOMETRY-CARRIER-REPAIR-394"
    packet["createdAtUtc"]=NOW
    packet["status"]="CORRECTED_TESTONLY_GEOMETRY_AND_CARRIER_PENDING_DIRECTOR_REVIEW_AND_OWNER_ADOPTION"
    packet["scope"]["supersedes"]="PG328-W08-OCCUPIED-ANTIMAGIC-PREBUILD-DIRECTOR-REPAIR-386"
    packet["scope"].update({"actualCastPerformed":False,"fixtureMutated":False,
      "spellIdentityAcceptedOrApplied":False,"ordinarySpellQueueChanged":False,"noCanonicalRuleChange":True})
    geometry_raw=put(OUT/GEOMETRY,geometry)
    carrier_raw=put(OUT/CARRIER,carrier)
    request_raw=put(OUT/REQUEST,request)
    packet_raw=put(OUT/PREBUILD,packet)
    packet["proposedGeometryProposal394"]["sha256"]=sha(geometry_raw)
    packet["proposedCarrierBounds394"]["sha256"]=sha(carrier_raw)
    packet_raw=put(OUT/PREBUILD,packet)

    manifest=copy.deepcopy(old_manifest)
    manifest.update({"id":"PG328-W08-PREBUILD-SOURCE-BINDINGS-394","createdAtUtc":NOW,
      "status":"HASH_VERIFIED_CORRECTED_UNADOPTED_TESTONLY_GEOMETRY_AND_CARRIER",
      "prebuildPath":PREBUILD,"prebuildSha256":sha(packet_raw),
      "supersedesManifest":"PG328-W08-PREBUILD-SOURCE-BINDINGS-386",
      "bundleMemberPath":"payload/"+PREBUILD})
    term_bytes=old_zip.read("payload/proposals/"+TERMINATION)
    manifest["reviewProposals"]=[
      {"name":GEOMETRY,"bundleMember":"payload/proposals/"+GEOMETRY,"sha256":sha(geometry_raw),"bytes":len(geometry_raw),"status":geometry["status"]},
      {"name":CARRIER,"bundleMember":"payload/proposals/"+CARRIER,"sha256":sha(carrier_raw),"bytes":len(carrier_raw),"status":carrier["status"]},
      {"name":TERMINATION,"bundleMember":"payload/proposals/"+TERMINATION,"sha256":sha(term_bytes),"bytes":len(term_bytes),
       "status":"PROPOSED_NEW_SCOPED_TEST_ONLY_CONTRACT_PENDING_DIRECTOR_REVIEW_AND_OWNER_ADOPTION"}]
    manifest["supersededProposalHashes"]={"geometry386":"83d942662c8ddac274f8e9c3b03aa65bd0a8bd23c0a462ebe0ee5ca705f47465",
      "carrier386":"cae91912315af9a14ea749750a39dc33f6a986b969b0f22868d9eb3a86e8e674"}
    manifest["reviewRequest"]={"bundleMember":"payload/"+REQUEST,"sha256":sha(request_raw),"bytes":len(request_raw)}
    manifest["nonAdoptionNotice"]="394 geometry/carrier are proposals only. No cast, rule adoption, fixture mutation, W08 seal, hold change, or queue change."
    manifest_raw=put(OUT/MANIFEST,manifest)

    zip_path=OUT/ZIP_NAME
    with zipfile.ZipFile(zip_path,"w",compression=zipfile.ZIP_DEFLATED,compresslevel=9) as z:
      for info in old_zip.infolist():
        name=info.filename
        data=old_zip.read(name)
        if name=="authority/PG328-W08_PREBUILD_SOURCE_BINDINGS_386.json":
          z.writestr("prior386/"+name,data)
        elif name=="payload/"+PREBUILD:
          z.writestr("prior386/"+name,data)
        elif name.startswith("payload/proposals/"):
          z.writestr("prior386/"+name,data)
        else: z.writestr(info,data)
      z.writestr("authority/"+MANIFEST,manifest_raw)
      z.writestr("payload/"+PREBUILD,packet_raw)
      z.writestr("payload/proposals/"+GEOMETRY,geometry_raw)
      z.writestr("payload/proposals/"+CARRIER,carrier_raw)
      z.writestr("payload/proposals/"+TERMINATION,term_bytes)
      z.writestr("payload/"+REQUEST,request_raw)


    zip_bytes=zip_path.read_bytes()
    delivery={"id":"DD-RANK9-PG328-W08-GEOMETRY-CARRIER-REPAIR-394-TESTONLY-DELIVERY",
      "createdAtUtc":NOW,"status":"READY_FOR_DIRECTOR_REVIEW_PENDING_TRANSMISSION",
      "supersedes":"DD-RANK9-PG328-W08-PREBUILD-386-DIRECTOR-REPAIR-DELIVERY",
      "artifact":ZIP_NAME,"sha256":sha(zip_bytes),"bytes":len(zip_bytes),
      "bundleMemberCount":len(zipfile.ZipFile(zip_path).infolist()),
      "prebuildPath":PREBUILD,"prebuildSha256":sha(packet_raw),
      "sourceBindingsPath":MANIFEST,"sourceBindingsSha256":sha(manifest_raw),
      "geometryProposalPath":GEOMETRY,"geometryProposalSha256":sha(geometry_raw),
      "carrierProposalPath":CARRIER,"carrierProposalSha256":sha(carrier_raw),
      "reviewRequestPath":REQUEST,"reviewRequestSha256":sha(request_raw),
      "priorPrebuild386Sha256":sha(old_packet_bytes),"priorPackage386Sha256":old_zip_sha,
      "originalCaseMemberSha256":CASE_SHA,"fixtureMutated":False,"actualCast":False,
      "ownerAdoptionOf394Proposals":False,"ordinaryQueue":{"applied":828,"pending":20,"acceptedUnapplied":0},
      "directorConversation":"https://chatgpt.com/g/g-p-67f17555a8dc8191a2b5b81e6d8adc12-dungeon-crawler/c/6ae66c6d-2d08-83ea-a1fa-042d649855a2",
      "transmissionStatus":"NOT_YET_SENT"}
    put(OUT/DELIVERY,delivery)
    with zipfile.ZipFile(zip_path) as z:
      assert z.testzip() is None
      assert z.read("payload/"+PREBUILD)==packet_raw
      assert z.read("payload/proposals/"+GEOMETRY)==geometry_raw
      assert z.read("payload/proposals/"+CARRIER)==carrier_raw
      assert z.read("payload/proposals/"+TERMINATION)==term_bytes
      assert z.read("prior386/payload/"+PREBUILD)==old_packet_bytes
      assert len(z.infolist())==delivery["bundleMemberCount"]
    assert sha(old_packet_path.read_bytes())==delivery["priorPrebuild386Sha256"]
    assert sha(old_zip_path.read_bytes())==old_zip_sha
    print(json.dumps({"zip":str(zip_path),"sha256":delivery["sha256"],"bytes":delivery["bytes"],
      "members":delivery["bundleMemberCount"],"prebuildSha256":delivery["prebuildSha256"],
      "geometrySha256":delivery["geometryProposalSha256"],"carrierSha256":delivery["carrierProposalSha256"],
      "requestSha256":delivery["reviewRequestSha256"],"center":center,
      "maxPanelDistanceFeet":max(distances),"centerRangeFeet":range_ft,"assertions":"PASS"},indent=2))

if __name__=="__main__": main()
