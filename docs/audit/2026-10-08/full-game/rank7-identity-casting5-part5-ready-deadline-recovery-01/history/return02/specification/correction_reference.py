"""Finite Correction02 specifications; not a scheduler, acquisition UI or game engine."""
from copy import deepcopy

def refresh_action(state, start, *, actual_regular_start):
    """Only an explicitly supplied real regular START refreshes this isolated ledger."""
    if not actual_regular_start or start < state["nextRegularStart"]:
        raise ValueError("No new actual regular START")
    out = deepcopy(state)
    out.update(action=True, regularStart=start, nextRegularStart=start+6)
    return out

def commit_action(state, *, legal=True, action_source=True):
    if not legal:
        return deepcopy(state)
    if not action_source or not state["action"]:
        raise ValueError("Actual ordinary Action unavailable")
    out=deepcopy(state);out["action"]=False
    return out

def legal_advancement(initial, choices, level=13, *, operational_feat):
    scores=deepcopy(initial);feats=[];used=set()
    for choice in choices:
        at=choice["classLevel"]
        if at not in (4,8,12,16,19) or at>level or at in used:
            raise ValueError("Unavailable or double-spent milestone")
        used.add(at)
        if choice["kind"]=="asi":
            ability=choice["ability"]
            if choice["amount"]!=2 or scores[ability]+2>20:
                raise ValueError("Invalid supplied ASI")
            scores[ability]+=2
        elif choice["kind"]=="feat":
            if not operational_feat:
                raise ValueError("Operational feat prerequisite remains")
            if choice["featId"]!="metamagicAdept" or at<4:
                raise ValueError("No qualifying named feat")
            modes=choice["modes"]
            if len(modes)!=2 or len(set(modes))!=2 or not set(modes)<= {"Reach","Widen","Sculpt"}:
                raise ValueError("Two distinct actual modes required")
            feats.append({"id":choice["featId"],"at":at,"modes":list(modes)})
        else:
            raise ValueError("One real ASI or feat per milestone")
    return {"scores":scores,"feats":feats}

def save_modifier(score, pb, trained):
    return (score-10)//2+(pb if trained else 0)

def commit_erase_matrix(state, *, actual_legal_action=True, prepared=True):
    """Rank7/base17 current prepared Wizard family; not a full spell implementation."""
    if not actual_legal_action or not prepared or not state["action"]:
        raise ValueError("No lawful prepared ordinary Action")
    if state["dissonance"]>=17:
        raise ValueError("Ranked commitment barred at supplied Limit11+6")
    surcharge=0 if state["dissonance"]<11 else 1+(state["dissonance"]-11)//3
    cost=17+surcharge
    if state["rp"]<cost:
        raise ValueError("Insufficient real RP")
    out=deepcopy(state)
    family="erase-from-reality"
    first=family not in state["preparedFamiliesUsed"]
    repeat=min(3,state["refrain"]+1) if state["lastSpell"]==family else 0
    out.update(action=False,rp=state["rp"]-cost,
               lastSpell=family,refrain=repeat,
               dissonance=state["dissonance"]+(0 if first else 2)+repeat)
    if first: out["preparedFamiliesUsed"].append(family)
    return out

def ready_before_deadline(now, next_regular_start, *, trigger_complete, reaction, concentration):
    return now<next_regular_start and trigger_complete and reaction and concentration
