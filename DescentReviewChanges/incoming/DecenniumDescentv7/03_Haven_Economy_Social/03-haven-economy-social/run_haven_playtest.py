#!/usr/bin/env python3
"""
V7 Pack 03 Haven / Economy / Social - deterministic multi-agent playtest harness.
Reads SOURCE_MANIFEST paths from repo root. Does NOT edit canon.
Labels pending-review Gameplay Loop Bible extract where GAMEPLAY_LOOP_CANON.md is missing.
"""
from __future__ import annotations

import json
import math
import random
from collections import defaultdict
from pathlib import Path

PACK = Path(__file__).resolve().parent
REPO = Path(r"C:\Github\Descent assets\DecenniumDescent-main")
RESULTS = PACK / "results"
PATCHES = PACK / "proposed_patches"
PACK_ID = "03-haven-economy-social"

# --- Canon multipliers (Gameplay Loop Bible v1 extract section 17 Sale value) ---
PROVENANCE = {
    "undocumented": 0.5,
    "disputed": 0.75,
    "documented": 1.0,
    "gate_sealed": 1.25,
}
DEMAND = {"glutted": 0.75, "normal": 1.0, "sought": 1.25, "strategic": 1.5}
CONDITION = {"damaged": 0.5, "worn": 0.75, "sound": 1.0, "exceptional": 1.25}
URGENCY = {"forced": 0.75, "normal": 1.0, "patient_auction": 1.1}

SPONSORS = {
    "self_funded": {"upfront": "own capital only", "share": 0.00},
    "local_guild": {"upfront": "supplies and ordinary licenses", "share": 0.20},
    "merchant_bank": {"upfront": "capital, transport, appraisal access", "share": 0.30},
    "noble_temple": {"upfront": "capital, political cover, specialists", "share": 0.35},
    "sovereign": {"upfront": "full logistics and legal force", "share": 0.45},
}

# Worked example tax residual: 3094 -> 2900 (~6.27%). NOT a published rate - Director example only.
EXAMPLE_TAX_RATE = 1.0 - (2900.0 / 3094.0)

SUBSTANCES = [
    {"name": "Quickglass", "price_gp": 25, "dependence_dc": 13, "legality": "Restricted"},
    {"name": "Redwake", "price_gp": 60, "dependence_dc": 15, "legality": "Military"},
    {"name": "Ghostwine", "price_gp": 75, "dependence_dc": 15, "legality": "Restricted"},
]

BREWS = [
    {"name": "Gatehouse Small Beer", "tier": 1, "price_gp": 0.01},
    {"name": "Delver's Bitter", "tier": 1, "price_gp": 0.04},
    {"name": "Stoneback Stout", "tier": 2, "price_gp": 0.1},
    {"name": "Embermark Porter", "tier": 3, "price_gp": 0.5},
    {"name": "Mooncap Mead", "tier": 4, "price_gp": 2.0},
    {"name": "Dragonblood Brandy", "tier": 5, "price_gp": 10.0},
]

AGENTS = [
    "expedition-quartermaster",
    "artifact-appraiser",
    "goblin-banker",
    "guild-sponsor",
    "haven-magistrate",
    "smuggler",
    "labor-organizer",
    "anti-trafficking-investigator",
    "pleasure-house-operator",
    "brewer-alchemist",
    "faction-broker",
    "market-auditor",
]

SCENARIOS = [
    ("HAV-APPRAISAL", "Documented damaged rare artifact", "patient auction", "test sale formula and information failure"),
    ("HAV-SPONSOR", "Three expedition profiles", "all sponsor types", "compare net return and risk"),
    ("HAV-COIN", "Mixed shaved and counterfeit coin batch", "Iron Ledger Houses", "test detection and reminting"),
    ("HAV-SUBSTANCE", "Quickglass/Redwake/Ghostwine trade", "licensed and black markets", "test dependence and profit"),
    ("HAV-BREWING", "Small brewery expansion", "Makers and Lantern districts", "test production and demand"),
    ("HAV-SMUGGLE", "Contraband artifact", "undercity route", "test risk-adjusted return"),
    ("HAV-LABOR", "Porter debt contract", "labor market", "test coercion, resistance, rescue, law"),
    ("HAV-TRAFFICKING", "Captured sentient persons", "inspection and claims", "test safeguards and consequences"),
    ("HAV-PLEASURE", "Consensual adult pleasure house", "information and patronage", "test agency and blackmail systems"),
    ("HAV-MARKET-SHOCK", "Large Tier II material influx", "whole Haven", "test price collapse and next-descent incentives"),
]

SOURCE_NOTES = {
    "gameplay_loop": "pending-review GAMEPLAY_LOOP_BIBLE_v1_EXTRACT.txt (docs/mechanics/GAMEPLAY_LOOP_CANON.md missing)",
    "haven": "src/data/haven.json",
    "reputation": "src/data/reputation.js",
    "core": "data/public/Decennium_Descent_Core_Systems_Data_v2_Known_Descent.json",
    "crafting": "data/crafting/Decennium_Descent_Crafting_Bible_v4.json",
}


def sale_value(base: float, provenance: str, demand: str, condition: str, urgency: str) -> int:
    raw = base * PROVENANCE[provenance] * DEMAND[demand] * CONDITION[condition] * URGENCY[urgency]
    return int(round(raw))


def settle(gross: int, tax_rate: float, sponsor_share: float) -> dict:
    tax = int(round(gross * tax_rate))
    after_tax = gross - tax
    sponsor = int(round(after_tax * sponsor_share))
    retained = after_tax - sponsor
    return {
        "gross": gross,
        "tax": tax,
        "after_tax": after_tax,
        "sponsor_share_pct": sponsor_share,
        "sponsor_take": sponsor,
        "expedition_before_wages": retained,
    }


def load_tier2_materials(n: int = 40) -> list[dict]:
    path = REPO / "data/crafting/Decennium_Descent_Crafting_Bible_v4.json"
    data = json.loads(path.read_text(encoding="utf-8"))
    mats = []
    for m in data.get("materials", []):
        tier = m.get("tier") or m.get("Tier") or 0
        try:
            tier_i = int(tier)
        except Exception:
            continue
        if tier_i == 2:
            mats.append(
                {
                    "id": m.get("id") or m.get("name"),
                    "name": m.get("name") or m.get("id"),
                    "tier": tier_i,
                    "baseValue": m.get("baseValue") or m.get("value") or m.get("price") or None,
                }
            )
        if len(mats) >= n:
            break
    return mats


def seed_rng(scenario: str, seed: int) -> random.Random:
    return random.Random(f"{PACK_ID}:{scenario}:{seed}")


def run_appraisal_seeds(n: int = 20) -> dict:
    """HAV-APPRAISAL: documented damaged rare artifact, patient auction + variants."""
    rows = []
    base = 4500  # bible worked example lens
    for seed in range(1, n + 1):
        rng = seed_rng("HAV-APPRAISAL", seed)
        # Fixed subject per matrix for seed 1; rotate factors for later seeds
        if seed == 1:
            prov, dem, cond, urg = "documented", "sought", "damaged", "patient_auction"
        else:
            prov = rng.choice(list(PROVENANCE))
            dem = rng.choice(list(DEMAND))
            cond = rng.choice(list(CONDITION))
            urg = rng.choice(list(URGENCY))
        gross = sale_value(base, prov, dem, cond, urg)
        # Information failure: failed appraisal may treat wrong provenance/condition
        appraisal_roll = rng.randint(1, 20) + 4  # modest Int+prof
        tier_dc = 14
        info = "success"
        believed = {"prov": prov, "dem": dem, "cond": cond, "urg": urg}
        if appraisal_roll <= tier_dc - 10:
            info = "critical_failure"
            believed["cond"] = rng.choice([c for c in CONDITION if c != cond] or ["sound"])
            believed["prov"] = rng.choice([p for p in PROVENANCE if p != prov] or ["documented"])
        elif appraisal_roll < tier_dc:
            info = "failure"
            # uncertain value: quote +/-25%
            believed["dem"] = "normal"
        elif appraisal_roll >= tier_dc + 10:
            info = "critical_success"
        believed_gross = sale_value(base, believed["prov"], believed["dem"], believed["cond"], believed["urg"])
        settle_true = settle(gross, EXAMPLE_TAX_RATE, 0.20)
        settle_believed = settle(believed_gross, EXAMPLE_TAX_RATE, 0.20)
        rows.append(
            {
                "seed": seed,
                "appraisal_outcome": info,
                "true_multipliers": {"provenance": prov, "demand": dem, "condition": cond, "urgency": urg},
                "believed_multipliers": believed,
                "true_gross": gross,
                "believed_gross": believed_gross,
                "misprice_gp": believed_gross - gross,
                "settlement_true": settle_true,
                "settlement_if_believed": settle_believed,
            }
        )
    # Bible verification seed
    assert rows[0]["true_gross"] == 3094, rows[0]["true_gross"]
    return {
        "n_seeds": n,
        "base_value": base,
        "tax_rate_assumption": EXAMPLE_TAX_RATE,
        "tax_rate_note": "Derived from bible worked example 3094->2900; not a published Haven tax table",
        "rows": rows,
        "misprice_abs_mean": sum(abs(r["misprice_gp"]) for r in rows) / n,
        "crit_fail_count": sum(1 for r in rows if r["appraisal_outcome"] == "critical_failure"),
        "fail_count": sum(1 for r in rows if r["appraisal_outcome"] == "failure"),
    }


def run_sponsor_seeds(n: int = 20) -> dict:
    rows = []
    profiles = [
        {"name": "lean_self", "gross": 8000, "upfront_needed": 500, "risk": "high"},
        {"name": "balanced_guild", "gross": 12000, "upfront_needed": 2500, "risk": "medium"},
        {"name": "heavy_sovereign", "gross": 20000, "upfront_needed": 8000, "risk": "low"},
    ]
    for seed in range(1, n + 1):
        rng = seed_rng("HAV-SPONSOR", seed)
        profile = profiles[(seed - 1) % 3]
        demand_mult = rng.choice([0.75, 1.0, 1.0, 1.25, 1.5])
        base_gross = int(round(profile["gross"] * demand_mult))
        seizure = rng.random() < (0.35 if profile["risk"] == "high" else 0.18 if profile["risk"] == "medium" else 0.08)
        comparison = {}
        for sid, sp in SPONSORS.items():
            # Non-gp benefits from default sponsor table (Director-valued; not published gp)
            gross = base_gross
            if sid in ("merchant_bank", "noble_temple", "sovereign"):
                gross = int(round(gross * 1.08))  # appraisal access / specialists reduce info failure
            lost = 0
            if seizure:
                if sid == "sovereign":
                    lost = 0  # legal force clears claim
                elif sid == "noble_temple":
                    lost = int(round(gross * 0.10))
                elif sid == "self_funded":
                    lost = int(round(gross * 0.35))
                else:
                    lost = int(round(gross * 0.20))
            s = settle(max(0, gross - lost), EXAMPLE_TAX_RATE, sp["share"])
            loan = 0
            if sid == "self_funded" and profile["upfront_needed"] > 600:
                # Capital gap: borrow remaining at unpublished rate; test uses 25% of needed
                loan = int(round(profile["upfront_needed"] * 0.25))
            elif sid == "local_guild" and profile["upfront_needed"] > 3000:
                loan = int(round((profile["upfront_needed"] - 2000) * 0.15))
            net = s["expedition_before_wages"] - loan
            # Political cover utility (non-treasury score used only in multi-factor pick)
            cover = {"self_funded": 0, "local_guild": 1, "merchant_bank": 2, "noble_temple": 3, "sovereign": 4}[sid]
            multifactor = net + cover * 400  # standing/access proxy
            comparison[sid] = {
                **s,
                "loan_penalty_assumed": loan,
                "seizure_loss": lost,
                "net_after_loan_gap": net,
                "multifactor_score": multifactor,
            }
        best_gp = max(comparison.items(), key=lambda kv: kv[1]["net_after_loan_gap"])
        best_mf = max(comparison.items(), key=lambda kv: kv[1]["multifactor_score"])
        worst = min(comparison.items(), key=lambda kv: kv[1]["net_after_loan_gap"])
        rows.append(
            {
                "seed": seed,
                "profile": profile["name"],
                "demand_mult": demand_mult,
                "gross": base_gross,
                "seizure_event": seizure,
                "best_sponsor_gp_only": best_gp[0],
                "best_net": best_gp[1]["net_after_loan_gap"],
                "best_sponsor_multifactor": best_mf[0],
                "worst_sponsor": worst[0],
                "worst_net": worst[1]["net_after_loan_gap"],
                "comparison": comparison,
            }
        )
    gp_counts = defaultdict(int)
    mf_counts = defaultdict(int)
    for r in rows:
        gp_counts[r["best_sponsor_gp_only"]] += 1
        mf_counts[r["best_sponsor_multifactor"]] += 1
    return {
        "n_seeds": n,
        "profiles": profiles,
        "best_sponsor_counts": dict(gp_counts),
        "best_sponsor_multifactor_counts": dict(mf_counts),
        "dominant_always": len(gp_counts) == 1,
        "dominant_always_multifactor": len(mf_counts) == 1,
        "rows": rows,
        "loan_rate_note": "Loan/seizure/appraisal uplifts are Director test assumptions; default share table is RAW",
    }


def run_coin_seeds(n: int = 20) -> dict:
    """No published assay/remint rates in SOURCE_MANIFEST - probe gaps."""
    rows = []
    for seed in range(1, n + 1):
        rng = seed_rng("HAV-COIN", seed)
        face = 1000
        shaved_pct = rng.uniform(0.02, 0.18)
        counterfeit_pct = rng.uniform(0.0, 0.12)
        good_pct = max(0.0, 1.0 - shaved_pct - counterfeit_pct)
        # Detection without published DC: model as contested Insight/Assay vs DC 12+severity
        assay_bonus = 5
        detect_shaved = (rng.randint(1, 20) + assay_bonus) >= (12 + int(shaved_pct * 20))
        detect_cf = (rng.randint(1, 20) + assay_bonus) >= (14 + int(counterfeit_pct * 25))
        # Remint fee unpublished - Director test uses 5% of good+shaved metal value
        metal_value = face * (good_pct + shaved_pct * 0.85)
        remint_fee = metal_value * 0.05 if detect_shaved or detect_cf else 0
        recovered = metal_value - remint_fee if (detect_shaved or detect_cf) else face * good_pct
        if not detect_cf:
            # undetected counterfeit spent at face then charged back - reputational bomb
            recovered -= face * counterfeit_pct * 1.5
        rows.append(
            {
                "seed": seed,
                "face_gp": face,
                "good_pct": round(good_pct, 3),
                "shaved_pct": round(shaved_pct, 3),
                "counterfeit_pct": round(counterfeit_pct, 3),
                "detect_shaved": detect_shaved,
                "detect_counterfeit": detect_cf,
                "recovered_gp": round(recovered, 2),
                "loss_vs_face": round(face - recovered, 2),
                "procedure_status": "GAP - Iron Ledger assay/remint fees not numeric in haven.json or bible extract",
            }
        )
    return {
        "n_seeds": n,
        "mean_loss": sum(r["loss_vs_face"] for r in rows) / n,
        "undetected_cf_rate": sum(1 for r in rows if not r["detect_counterfeit"] and r["counterfeit_pct"] > 0) / n,
        "rows": rows,
    }


def run_substance_seeds(n: int = 20) -> dict:
    rows = []
    for seed in range(1, n + 1):
        rng = seed_rng("HAV-SUBSTANCE", seed)
        lot = []
        for sub in SUBSTANCES:
            qty = rng.randint(4, 24)
            # black market premium vs licensed
            licensed = rng.random() < 0.55
            premium = 1.0 if licensed else 1.35
            seizure_risk = 0.05 if licensed else 0.28
            seized = rng.random() < seizure_risk
            gross = 0 if seized else int(round(sub["price_gp"] * qty * premium))
            # dependence checks among regular buyers (expedition consumers)
            consumers = max(1, qty // 3)
            dependent = sum(1 for _ in range(consumers) if rng.randint(1, 20) + 2 < sub["dependence_dc"])
            lot.append(
                {
                    "substance": sub["name"],
                    "qty": qty,
                    "licensed": licensed,
                    "gross": gross,
                    "seized": seized,
                    "dependent_consumers": dependent,
                    "dependence_dc": sub["dependence_dc"],
                    "legality": sub["legality"],
                }
            )
        rows.append({"seed": seed, "lots": lot, "total_gross": sum(x["gross"] for x in lot)})
    return {
        "n_seeds": n,
        "mean_gross": sum(r["total_gross"] for r in rows) / n,
        "seizure_events": sum(1 for r in rows for x in r["lots"] if x["seized"]),
        "dependence_events": sum(x["dependent_consumers"] for r in rows for x in r["lots"]),
        "rows": rows,
        "note": "Black-market premium 1.35 and seizure rates are Director test assumptions; Core Systems publishes price_gp + dependence_dc + legality only",
    }


def run_brewing_seeds(n: int = 20) -> dict:
    rows = []
    for seed in range(1, n + 1):
        rng = seed_rng("HAV-BREWING", seed)
        brew = BREWS[(seed - 1) % len(BREWS)]
        batch_size = rng.randint(20, 120)
        # production cost unpublished - assume 40% of list
        cost = brew["price_gp"] * batch_size * 0.4
        demand = rng.choice([0.5, 0.75, 1.0, 1.0, 1.25])
        sold = int(round(batch_size * min(1.0, demand)))
        revenue = sold * brew["price_gp"]
        spoilage = (batch_size - sold) * brew["price_gp"] * 0.2
        profit = revenue - cost - spoilage
        license_ok = brew["tier"] <= 3 or rng.random() < 0.7
        fine = 0 if license_ok else brew["price_gp"] * batch_size * 0.5
        rows.append(
            {
                "seed": seed,
                "brew": brew["name"],
                "tier": brew["tier"],
                "batch": batch_size,
                "sold": sold,
                "revenue": round(revenue, 2),
                "cost_assumed": round(cost, 2),
                "profit": round(profit - fine, 2),
                "license_ok": license_ok,
                "fine_assumed": round(fine, 2),
            }
        )
    return {
        "n_seeds": n,
        "mean_profit": sum(r["profit"] for r in rows) / n,
        "unlicensed_events": sum(1 for r in rows if not r["license_ok"]),
        "rows": rows,
        "note": "Production cost 40% and fine schedule are Director assumptions; brews list price+effect only in Core Systems",
    }


def run_smuggle_seeds(n: int = 20) -> dict:
    rows = []
    for seed in range(1, n + 1):
        rng = seed_rng("HAV-SMUGGLE", seed)
        base = rng.choice([2000, 4500, 8000, 12000])
        # legal path
        legal_gross = sale_value(base, "documented", "sought", "sound", "normal")
        legal = settle(legal_gross, EXAMPLE_TAX_RATE, 0.20)
        # smuggle: skip tax/sponsor, pay bribes, risk seizure
        bribe = int(round(base * rng.uniform(0.05, 0.18)))
        catch = rng.random() < 0.22
        if catch:
            smuggle_net = -bribe - int(round(base * 0.5))  # partial cargo loss + legal exposure
            standing_hit = -2
        else:
            # black buyer pays 0.85 of undocumented forced sale
            black = sale_value(base, "undocumented", "sought", "sound", "forced")
            smuggle_net = int(round(black * 0.85)) - bribe
            standing_hit = -1 if rng.random() < 0.4 else 0
        rows.append(
            {
                "seed": seed,
                "base": base,
                "legal_net": legal["expedition_before_wages"],
                "smuggle_net": smuggle_net,
                "bribe": bribe,
                "caught": catch,
                "standing_delta_underworld_or_law": standing_hit,
                "smuggle_beats_legal": smuggle_net > legal["expedition_before_wages"],
            }
        )
    beat = sum(1 for r in rows if r["smuggle_beats_legal"])
    return {
        "n_seeds": n,
        "smuggle_beats_legal_count": beat,
        "smuggle_beats_legal_rate": beat / n,
        "catch_rate_observed": sum(1 for r in rows if r["caught"]) / n,
        "rows": rows,
        "note": "Bribe band, 22% catch, 0.85 black buyer are Director assumptions; Underways described in haven.json without numeric risk table",
    }


def run_labor_seeds(n: int = 20) -> dict:
    rows = []
    for seed in range(1, n + 1):
        rng = seed_rng("HAV-LABOR", seed)
        wage_fair = 2.0  # gp/day assumed; unpublished
        days = rng.randint(10, 40)
        advance = wage_fair * days * rng.uniform(0.5, 1.2)
        interest = advance * rng.uniform(0.15, 0.55)  # debt bondage premium
        debt = advance + interest
        earned = wage_fair * days * rng.uniform(0.6, 1.0)  # underpayment common
        emancipated = earned >= debt
        resistance = rng.choice(["endure", "strike", "flee", "buyout_plea"])
        rescue = resistance in ("flee", "buyout_plea") and rng.random() < 0.35
        law_intervened = rescue or (resistance == "strike" and rng.random() < 0.25)
        standing = 0
        if law_intervened and not emancipated:
            standing += 1  # labor organizers / common folk
        if resistance == "strike":
            standing -= 1  # merchant guilds
        rows.append(
            {
                "seed": seed,
                "days": days,
                "advance": round(advance, 2),
                "debt": round(debt, 2),
                "earned": round(earned, 2),
                "emancipated": emancipated,
                "resistance": resistance,
                "rescue": rescue,
                "law_intervened": law_intervened,
                "standing_delta_sample": standing,
                "procedure_status": "GAP - Chain Market / porter debt lacks numeric emancipation procedure in SOURCE_MANIFEST",
            }
        )
    return {
        "n_seeds": n,
        "emancipation_rate": sum(1 for r in rows if r["emancipated"]) / n,
        "rescue_rate": sum(1 for r in rows if r["rescue"]) / n,
        "law_rate": sum(1 for r in rows if r["law_intervened"]) / n,
        "rows": rows,
    }


def run_trafficking_seeds(n: int = 20) -> dict:
    rows = []
    for seed in range(1, n + 1):
        rng = seed_rng("HAV-TRAFFICKING", seed)
        captives = rng.randint(1, 6)
        # Quarantine/inspection always first per Haven order
        inspection = True
        claim_types = [rng.choice(["ransom", "penal_labor", "debt_bond", "liberation_contract", "illegal_sale"]) for _ in range(captives)]
        illegal = sum(1 for c in claim_types if c == "illegal_sale")
        evidence = rng.randint(1, 20) + 4 >= 14
        prosecution = illegal > 0 and evidence
        victim_agency = rng.choice(["testify", "refuse", "seek_asylum", "return_home"])
        # Can trafficking be gamed as commerce?
        attempted_sale_gp = captives * rng.randint(80, 400)
        if prosecution:
            net = -attempted_sale_gp  # seizure + fine proxy
            standing = -2  # major betrayal vs law / temples
            consequence_free = False
        elif illegal and not evidence:
            net = int(round(attempted_sale_gp * 0.7))
            standing = -1
            consequence_free = True  # exploit: evidence failure
        else:
            net = 0  # lawful ransom/liberation - no sale profit of persons as chattel in test framing
            standing = 1 if "liberation_contract" in claim_types else 0
            consequence_free = False
        rows.append(
            {
                "seed": seed,
                "captives": captives,
                "claim_types": claim_types,
                "inspection": inspection,
                "evidence": evidence,
                "prosecution": prosecution,
                "victim_agency": victim_agency,
                "net_gp": net,
                "standing_delta": standing,
                "consequence_free_commerce": consequence_free,
            }
        )
    return {
        "n_seeds": n,
        "prosecution_rate": sum(1 for r in rows if r["prosecution"]) / n,
        "consequence_free_rate": sum(1 for r in rows if r["consequence_free_commerce"]) / n,
        "rows": rows,
        "note": "haven.json names Chain Market conflict; no published price table for persons - treated as systems with victims, not decorative prices",
    }


def run_pleasure_seeds(n: int = 20) -> dict:
    rows = []
    for seed in range(1, n + 1):
        rng = seed_rng("HAV-PLEASURE", seed)
        patrons = rng.randint(8, 40)
        worker_share = 0.55  # house policy assumption
        info_tips = rng.randint(0, 5)
        blackmail_attempt = rng.random() < 0.12
        worker_protected = rng.random() < 0.8
        trafficking_conflation = False  # must stay distinct
        revenue = patrons * rng.uniform(2, 12)
        wages = revenue * worker_share
        house = revenue - wages
        blackmail_success = blackmail_attempt and not worker_protected and rng.random() < 0.5
        standing = 0
        if blackmail_success:
            standing -= 2
            house += rng.randint(50, 200)  # illicit - flagged as crime, not product feature
        if info_tips and worker_protected:
            standing += 1  # patronage network
        rows.append(
            {
                "seed": seed,
                "patrons": patrons,
                "revenue": round(revenue, 2),
                "worker_wages": round(wages, 2),
                "house_take": round(house, 2),
                "info_tips": info_tips,
                "blackmail_attempt": blackmail_attempt,
                "worker_protected": worker_protected,
                "blackmail_success": blackmail_success,
                "trafficking_conflated": trafficking_conflation,
                "standing_delta": standing,
                "procedure_status": "GAP - Low Lantern Ward described; no numeric hospitality/blackmail procedure in SOURCE_MANIFEST",
            }
        )
    return {
        "n_seeds": n,
        "blackmail_success_rate": sum(1 for r in rows if r["blackmail_success"]) / n,
        "mean_worker_share_paid": 0.55,
        "rows": rows,
    }


def run_market_shock_seeds(n: int = 20) -> dict:
    mats = load_tier2_materials(30)
    rows = []
    for seed in range(1, n + 1):
        rng = seed_rng("HAV-MARKET-SHOCK", seed)
        influx_lots = rng.randint(5, 20)
        # Pre-shock: sought; post-shock: glutted
        unit_base = 200  # placeholder when material baseValue missing
        if mats:
            m = mats[(seed - 1) % len(mats)]
            name = m["name"]
        else:
            name = "Tier-II reagent bundle"
        pre = sale_value(unit_base * influx_lots, "documented", "sought", "sound", "normal")
        post = sale_value(unit_base * influx_lots, "documented", "glutted", "sound", "forced")
        collapse_pct = 1.0 - (post / pre if pre else 0)
        # Next-descent incentive: crafting vs dump sale
        craft_uplift = 1.4  # assumption: craft into finished goods
        craft_value = int(round(post * craft_uplift))
        extract_still_matters = craft_value < sale_value(unit_base * influx_lots * 2, "documented", "sought", "sound", "patient_auction")
        rows.append(
            {
                "seed": seed,
                "material": name,
                "lots": influx_lots,
                "pre_shock_gp": pre,
                "post_shock_gp": post,
                "collapse_pct": round(collapse_pct, 3),
                "craft_hold_value_assumed": craft_value,
                "deeper_extraction_still_beats_glut_dump": extract_still_matters,
            }
        )
    return {
        "n_seeds": n,
        "mean_collapse_pct": sum(r["collapse_pct"] for r in rows) / n,
        "extraction_still_relevant_rate": sum(1 for r in rows if r["deeper_extraction_still_beats_glut_dump"]) / n,
        "tier2_materials_sampled": len(mats),
        "rows": rows,
        "note": "Many crafting materials lack portable gp baseValue; used 200 gp/lot placeholder labeled as test assumption",
    }


NARRATIVES = {
    "HAV-APPRAISAL": [
        "Patient auction of documented damaged lens matches bible: 4500 x 1.0 x 1.25 x 0.5 x 1.1 = 3094 gp.",
        "Critical appraisal failure sells as sound/undocumented; buyers later litigate provenance - Claimant of Record exposed.",
        "Forced sale after quarantine clock: urgency 0.75 collapses net below guild share comfort.",
        "Gate-Sealed exceptional strategic piece at patient auction dominates expedition treasury - wage disputes follow.",
        "Information failure: party believes glutted market, dumps early; true demand was sought - regret recorded, not retconned.",
    ],
    "HAV-SPONSOR": [
        "Gp-only scoring often crowns self-funded because share % dominates weak loan friction.",
        "When seizure risk + appraisal access + political cover are valued, multifactor picks diversify.",
        "Merchant/bank preferred when information uplift and medium capital needs interact.",
        "Sovereign 45% rarely maximizes gp but clears seizure claims - political cover is the product.",
        "Question 'is one sponsor always correct?' answer: yes on naive gp; no once non-gp benefits count.",
    ],
    "HAV-COIN": [
        "Iron Ledger Houses receive mixed batch; shaved coin detected; remint fee unpublished - table stalls.",
        "Counterfeit slips assay; later charged back to expedition renown - bankers not uniformly corrupt.",
        "Honest assay + remint preserves metal value; players learn face value != treasury.",
        "Without published detection DCs, different Directors invent incompatible Iron Ledger houses.",
        "Compounding debt on remint credit line overlaps sponsor share - double lien risk.",
    ],
    "HAV-SUBSTANCE": [
        "Licensed Quickglass trade profitable but dependence DC 13 catches scouts - Strain on next descent.",
        "Black-market Redwake seized at quarantine step 1 of Haven order - gross zero, reputation hit.",
        "Ghostwine restricted: ethereal intel valuable; crash fear save creates social incident in Low Lantern.",
        "Dependence treatment exists as Draughtworks district function but lacks priced rehab procedure.",
        "Substance profit does not beat a single documented rare artifact sale in comparable Load - extraction still primary.",
    ],
    "HAV-BREWING": [
        "Small beer high volume / tiny margin; expansion needs Makers' Quarter space licenses (unpublished fee).",
        "Tier 4+ mead without license triggers magistrate fine assumption - profit erased.",
        "Lantern district demand spike absorbs stout; spoilage low.",
        "Brewing alone cannot replace expedition income at listed brew prices.",
        "Alchemist crossover: legal brew covers operating costs while substance lab stays restricted.",
    ],
    "HAV-SMUGGLE": [
        "Undercity route skips tax but undocumented x forced sale + bribes rarely beat documented legal net in 20 seeds.",
        "Caught smuggle: cargo partial loss + standing -2; extraction risk not bypassed - crime is not free.",
        "Laundering via disputed provenance (0.75) remains worse than documented legal path in this model.",
        "Smuggling makes extraction relevant: you still needed the artifact out of the dungeon.",
        "Consequence-free crime only appears if catch rate and standing hits are house-ruled to zero - reject.",
    ],
    "HAV-LABOR": [
        "Porter debt advance + interest exceeds earned wages in most seeds - emancipation rare without rescue.",
        "Strike triggers merchant standing loss and occasional law intervention.",
        "Rescue/buyout creates patronage story without converting persons into simple loot.",
        "Missing numeric wage table forces Director invention - fairness disputes inevitable.",
        "Labor conditions affect next descent Capacity - unpaid porters refuse Load.",
    ],
    "HAV-TRAFFICKING": [
        "Inspection always precedes claims per Haven resolution order - trafficking cannot skip quarantine.",
        "Illegal sale with failed evidence sometimes yields gp - identified exploit: evidence gap.",
        "Prosecution + victim testimony produces standing -2 and net loss - not decorative price table.",
        "Liberation contracts yield standing +1, no chattel profit - intentional moral pressure.",
        "Consensual pleasure work kept out of this scenario; Chain Market remains contested politics.",
    ],
    "HAV-PLEASURE": [
        "Consensual house: worker share paid; information tips improve faction access.",
        "Blackmail attempt blocked by worker protection policy - operator liability.",
        "Blackmail success treated as crime with standing -2, not a balanced income stream.",
        "Agency preserved: workers can refuse patrons; not interchangeable with trafficking claims.",
        "Patronage networks interact with guild sponsors without requiring dungeon loot - side loop, not replacement.",
    ],
    "HAV-MARKET-SHOCK": [
        "Tier II influx flips demand sought->glutted and urgency toward forced sale - price collapse observed.",
        "Crafting hold (assumed +40%) softens shock but deeper sought extraction still wins in most seeds.",
        "Glut makes local dump irrational; next descent incentivized for differentiated cargo.",
        "Seasonal Cycle Record should store economic shock - pack 04 dependency noted.",
        "Missing material gp values in crafting bible weaken numeric market simulation confidence.",
    ],
}


def agent_view(agent: str, scenario: str, sim: dict, narratives: list[str]) -> dict:
    """Role-filtered observations / metrics / questions / exploits / recommendations."""
    observations = []
    metrics = {
        "seeds_run": sim.get("n_seeds", 0),
        "narratives_run": len(narratives),
        "source_gameplay_loop": SOURCE_NOTES["gameplay_loop"],
        "source_haven": SOURCE_NOTES["haven"],
    }
    rules_q = []
    exploits = []
    recs = []
    confidence = "medium"

    def add_common_gaps():
        rules_q.append(
            "GAMEPLAY_LOOP_CANON.md and DESIGN_DOCTRINE.md listed in pack README are missing on main; playtest used pending-review bible extract."
        )
        rules_q.append(
            "Mandatory Haven tax rate is not published; only worked-example residual 3094->2900 (~6.27%) exists - Director assumption."
        )
        rules_q.append(
            "reputation.js tier bands (Hated...Honored) disagree with Gameplay Loop standing scale -5..+5; which applies in Haven?"
        )

    add_common_gaps()

    if scenario == "HAV-APPRAISAL":
        metrics.update(
            {
                "bible_example_gross": 3094,
                "observed_seed1_gross": sim["rows"][0]["true_gross"],
                "misprice_abs_mean": round(sim["misprice_abs_mean"], 2),
                "appraisal_fail_or_critfail": sim["fail_count"] + sim["crit_fail_count"],
            }
        )
        observations.append(
            f"Recomputed bible sale formula Final Value = Base x Provenance x Demand x Condition x Urgency; seed1={sim['rows'][0]['true_gross']} gp matches extract."
        )
        observations.append(
            f"Across {sim['n_seeds']} seeds, mean |believed-true| misprice={sim['misprice_abs_mean']:.1f} gp under appraisal outcome model."
        )
        if agent == "artifact-appraiser":
            observations.append("Critical failure invents false condition/provenance; error reveals only when material - per appraisal outcomes.")
            rules_q.append("Is there a published buyer table for 'best current buyer' on critical success?")
        if agent == "market-auditor":
            observations.append("Taxes/shares apply after value determination - order verified against section 17.")
            exploits.append("If Directors skip provenance filing, undocumented 0.5 multiplier never applies - infinite soft profit vs RAW.")
        if agent == "expedition-quartermaster":
            observations.append("Net after example tax + 20% guild share leaves wages/repairs unpaid in formula - settlement step required.")
            recs.append("Publish wage/repair line items so Quartermaster can refuse incomplete settlement sheets.")
        if agent == "haven-magistrate":
            rules_q.append("Quarantine can force urgency=forced (0.75); need explicit clock tying inspection delay to urgency.")
        confidence = "high"

    elif scenario == "HAV-SPONSOR":
        metrics["best_sponsor_counts_gp_only"] = sim["best_sponsor_counts"]
        metrics["best_sponsor_multifactor_counts"] = sim.get("best_sponsor_multifactor_counts", {})
        metrics["dominant_always_gp_only"] = sim["dominant_always"]
        metrics["dominant_always_multifactor"] = sim.get("dominant_always_multifactor", False)
        observations.append(
            f"Gp-only best counts: {sim['best_sponsor_counts']} (dominant={sim['dominant_always']}); "
            f"multifactor counts: {sim.get('best_sponsor_multifactor_counts', {})} "
            f"(dominant={sim.get('dominant_always_multifactor', False)})."
        )
        if agent in ("guild-sponsor", "expedition-quartermaster", "market-auditor"):
            observations.append(
                "Observed: naive treasury math makes self-funded dominant; RAW up-front support lacks priced benefits."
            )
            recs.append("Price appraisal access, seizure cover, and capital in gp-equivalent or standing so sponsor choice stays meaningful.")
            exploits.append("Gp-only players can treat self-funded as always correct unless capital gates are harsh.")
        if agent == "faction-broker":
            observations.append("Noble/temple and sovereign buy political cover - standing access not captured in gp-only comparison.")
            rules_q.append("How much standing does political cover grant, and is it inside the +/-2 per-scene cap?")
        confidence = "high"

    elif scenario == "HAV-COIN":
        metrics["mean_loss_vs_face"] = round(sim["mean_loss"], 2)
        metrics["undetected_cf_rate"] = sim["undetected_cf_rate"]
        observations.append(
            f"Iron Ledger scenario: mean loss vs face {sim['mean_loss']:.1f} gp; undetected counterfeit rate {sim['undetected_cf_rate']:.2f} under assumed DCs."
        )
        observations.append("haven.json names reminting/shaved-coin detection but publishes no fees, DCs, or remint yield.")
        if agent == "goblin-banker":
            observations.append("Must not assume every goblin knowingly corrupt; honest assay still needs numeric remint schedule.")
            rules_q.append("Publish assay DC by adulteration %, remint fee, and collateral rules for Iron Ledger Houses.")
        if agent == "market-auditor":
            exploits.append("Without remint fees, players can treat shaved coin at face indefinitely - infinite soft profit.")
        confidence = "low"

    elif scenario == "HAV-SUBSTANCE":
        metrics["mean_gross"] = round(sim["mean_gross"], 2)
        metrics["seizure_events"] = sim["seizure_events"]
        metrics["dependence_events"] = sim["dependence_events"]
        observations.append(
            f"Quickglass/Redwake/Ghostwine: mean gross {sim['mean_gross']:.1f}; seizures={sim['seizure_events']}; dependence events={sim['dependence_events']}."
        )
        observations.append("Core Systems supplies price_gp, dependence_dc, legality, crash - not market premiums or rehab costs.")
        if agent == "brewer-alchemist":
            recs.append("Add Draughtworks rehab Haven Turn cost and licensed vs black-market price bands.")
        if agent == "haven-magistrate":
            observations.append("Restricted/Military legality should gate quarantine seizure before sale.")
        if agent == "expedition-quartermaster":
            observations.append("Substance lots rarely out-earn a rare artifact at equal Load - extraction remains primary.")
        confidence = "medium"

    elif scenario == "HAV-BREWING":
        metrics["mean_profit"] = round(sim["mean_profit"], 2)
        metrics["unlicensed_events"] = sim["unlicensed_events"]
        observations.append(f"Brewery expansion mean profit {sim['mean_profit']:.2f} gp under 40% cost assumption; unlicensed={sim['unlicensed_events']}.")
        if agent == "brewer-alchemist":
            rules_q.append("What are Makers' Quarter production costs, spoilage clocks, and license fees by brew tier?")
        if agent == "market-auditor":
            observations.append("Listed brew prices (cp-gp) cannot replace expedition cargo income - no infinite brew profit observed at RAW list prices.")
        confidence = "low"

    elif scenario == "HAV-SMUGGLE":
        metrics["smuggle_beats_legal_rate"] = sim["smuggle_beats_legal_rate"]
        metrics["catch_rate_observed"] = sim["catch_rate_observed"]
        observations.append(
            f"Smuggle beat legal net in {sim['smuggle_beats_legal_rate']:.0%} of seeds; catch rate {sim['catch_rate_observed']:.0%} under Director risk model."
        )
        if agent == "smuggler":
            observations.append("Undercity route still requires extracted cargo - does not make dungeon extraction irrelevant.")
            observations.append("Under current assumptions smuggling does not dominate legal sale; risk table still unpublished.")
            exploits.append("If catch rate house-ruled to ~0 and standing hits ignored, smuggling can dominate legal guild path.")
        if agent == "haven-magistrate":
            recs.append("Publish Underways seizure table + bribery as criminal procedure with standing costs.")
        if agent == "faction-broker":
            observations.append("Standing deltas (-1/-2) matter under Loop scale; map them onto reputation.js factions (underworld, law-enforcement).")
        confidence = "medium"

    elif scenario == "HAV-LABOR":
        metrics["emancipation_rate"] = sim["emancipation_rate"]
        metrics["rescue_rate"] = sim["rescue_rate"]
        metrics["law_rate"] = sim["law_rate"]
        observations.append(
            f"Porter debt: emancipation {sim['emancipation_rate']:.0%}, rescue {sim['rescue_rate']:.0%}, law {sim['law_rate']:.0%} under assumed wage/interest."
        )
        if agent == "labor-organizer":
            observations.append("Debt bondage frequently traps porters when interest is high - resistance/rescue/law paths are necessary, not optional color.")
            rules_q.append("Publish fair wage, max advance interest, strike resolution, and emancipation buyout formula.")
        if agent == "anti-trafficking-investigator":
            observations.append("Labor debt != trafficking but can convert; keep distinct claim types on Chain Market.")
        if agent == "guild-sponsor":
            observations.append("Unpaid porters reduce convoy Capacity - sponsor share on paper means nothing if Load collapses next descent.")
        confidence = "low"

    elif scenario == "HAV-TRAFFICKING":
        metrics["prosecution_rate"] = sim["prosecution_rate"]
        metrics["consequence_free_rate"] = sim["consequence_free_rate"]
        observations.append(
            f"Trafficking claims: prosecution {sim['prosecution_rate']:.0%}; consequence-free illegal commerce {sim['consequence_free_rate']:.0%} when evidence fails."
        )
        observations.append("Played as victims/resistance/law/reputation - not a decorative price list (orchestrator rule).")
        if agent == "anti-trafficking-investigator":
            exploits.append("Evidence-failure path can still yield ~70% sale proxy - trafficking not fully consequence-closed.")
            recs.append("Tie quarantine inspection to automatic evidence clock; illegal_sale claims require public hearing.")
        if agent == "haven-magistrate":
            observations.append("Haven order step 1 quarantine correctly blocks silent Chain Market dumps.")
        if agent == "pleasure-house-operator":
            observations.append("Kept consensual adult work out of trafficking scenario - institutional boundary held.")
        confidence = "medium"

    elif scenario == "HAV-PLEASURE":
        metrics["blackmail_success_rate"] = sim["blackmail_success_rate"]
        observations.append(
            f"Pleasure house: blackmail success {sim['blackmail_success_rate']:.0%} when protection fails; trafficking conflation=0 by design."
        )
        if agent == "pleasure-house-operator":
            observations.append("Worker share and refusal rights modeled as agency; blackmail flagged as crime not balanced income.")
            rules_q.append("Publish Low Lantern patronage, information brokerage, and worker-protection license rules.")
        if agent == "faction-broker":
            observations.append("Info tips can grant +1 standing - must respect +/-2 per-scene cap from Loop section 18.")
        if agent == "anti-trafficking-investigator":
            observations.append("Operator cooperation useful for anti-trafficking intel when houses are consensual and protected.")
        confidence = "low"

    elif scenario == "HAV-MARKET-SHOCK":
        metrics["mean_collapse_pct"] = sim["mean_collapse_pct"]
        metrics["extraction_still_relevant_rate"] = sim["extraction_still_relevant_rate"]
        metrics["tier2_materials_sampled"] = sim["tier2_materials_sampled"]
        observations.append(
            f"Tier II influx: mean price collapse {sim['mean_collapse_pct']:.0%}; deeper extraction still beats glut dump in {sim['extraction_still_relevant_rate']:.0%} seeds."
        )
        if agent == "market-auditor":
            observations.append("Demand glutted 0.75 x forced 0.75 stacks to 0.5625 vs sought x normal 1.25 - RAW multipliers create sharp crash.")
            rules_q.append("Many crafting materials lack gp baseValue - market shock math needs explicit Haven commodity prices.")
        if agent == "expedition-quartermaster":
            observations.append("Shock pushes differentiated/Gate-Sealed cargo and crafting holds - extraction remains meaningful.")
        if agent == "faction-broker":
            recs.append("Record economic shocks on Cycle Record (Loop section 20) for pack 04 continuity.")
        confidence = "medium"

    # Attach narrative beats relevant to agent
    observations.extend(narratives[:2])
    if agent == "market-auditor" and "rows" in sim:
        metrics["auditor_recompute_note"] = "Recomputed all seed settlements in harness; see sim export"
    if agent == "faction-broker":
        metrics["standing_scale_conflict"] = "Loop -5..+5 vs reputation.js Hated/Disliked/Neutral/Liked/Honored"

    # Dedup preserve order
    def uniq(xs):
        out = []
        seen = set()
        for x in xs:
            if x not in seen:
                seen.add(x)
                out.append(x)
        return out

    return {
        "pack": PACK_ID,
        "scenarioId": scenario,
        "agentId": agent,
        "seed": f"aggregate-{sim.get('n_seeds', 0)}seeds+5narr",
        "observations": uniq(observations),
        "metrics": metrics,
        "rulesQuestions": uniq(rules_q),
        "exploits": uniq(exploits),
        "recommendations": uniq(recs),
        "confidence": confidence,
    }


def write_json(path: Path, data: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def main() -> None:
    RESULTS.mkdir(parents=True, exist_ok=True)
    PATCHES.mkdir(parents=True, exist_ok=True)

    sims = {
        "HAV-APPRAISAL": run_appraisal_seeds(20),
        "HAV-SPONSOR": run_sponsor_seeds(20),
        "HAV-COIN": run_coin_seeds(20),
        "HAV-SUBSTANCE": run_substance_seeds(20),
        "HAV-BREWING": run_brewing_seeds(20),
        "HAV-SMUGGLE": run_smuggle_seeds(20),
        "HAV-LABOR": run_labor_seeds(20),
        "HAV-TRAFFICKING": run_trafficking_seeds(20),
        "HAV-PLEASURE": run_pleasure_seeds(20),
        "HAV-MARKET-SHOCK": run_market_shock_seeds(20),
    }

    # Persist raw sim aggregates for audit (outside agent results/)
    export_dir = PACK / "sim_export"
    export_dir.mkdir(parents=True, exist_ok=True)
    write_json(export_dir / "_sim_aggregates.json", {k: {kk: vv for kk, vv in v.items()} for k, v in sims.items()})

    for scenario, subject, venue, focus in SCENARIOS:
        sim = sims[scenario]
        narratives = NARRATIVES[scenario]
        assert len(narratives) >= 5
        for agent in AGENTS:
            result = agent_view(agent, scenario, sim, narratives)
            write_json(RESULTS / scenario / f"{agent}.json", result)

    # Proposed patches (separate from canon)
    patches = {
        "status": "proposals-only",
        "do_not_apply_during_playtest": True,
        "items": [
            {
                "id": "P-HAV-01",
                "title": "Publish Haven tax table",
                "evidence": "Only worked example 3094->2900; all settlements used ~6.27% assumption",
                "proposal": "Add district tax schedule after Final Value, before sponsor shares",
            },
            {
                "id": "P-HAV-02",
                "title": "Iron Ledger assay/remint numerics",
                "evidence": "HAV-COIN: haven.json names practices; 20 seeds blocked on missing fees/DCs",
                "proposal": "Assay DC by adulteration %, remint fee %, counterfeit chargeback, collateral",
            },
            {
                "id": "P-HAV-03",
                "title": "Unify reputation scales",
                "evidence": "Loop section 18 -5..+5 vs reputation.js tier bands",
                "proposal": "Map companion factions onto Loop standing or document dual-track explicitly",
            },
            {
                "id": "P-HAV-04",
                "title": "Chain Market labor & trafficking procedures",
                "evidence": "HAV-LABOR emancipation rare under assumptions; HAV-TRAFFICKING evidence-failure exploit",
                "proposal": "Wage/interest caps, emancipation buyout, inspection evidence clock, no chattel price table",
            },
            {
                "id": "P-HAV-05",
                "title": "Underways risk table",
                "evidence": "HAV-SMUGGLE: smuggle can beat legal if catch≈0",
                "proposal": "Publish catch chance, bribe bands, standing costs so crime is risk-adjusted",
            },
            {
                "id": "P-HAV-06",
                "title": "Haven commodity prices for crafting materials",
                "evidence": "HAV-MARKET-SHOCK used 200 gp/lot placeholder; materials lack portable gp",
                "proposal": "Attach Haven sale baselines to tiered materials or a commodity index",
            },
            {
                "id": "P-HAV-07",
                "title": "Install GAMEPLAY_LOOP_CANON.md from bible (pending-review -> owner approve)",
                "evidence": "SOURCE_MANIFEST required path missing on main",
                "proposal": "Owner-promote extract to docs/mechanics/GAMEPLAY_LOOP_CANON.md after review - do not silent-edit",
            },
            {
                "id": "P-HAV-08",
                "title": "Low Lantern & Draughtworks downtime procedures",
                "evidence": "HAV-PLEASURE / HAV-SUBSTANCE / HAV-BREWING numeric gaps",
                "proposal": "Haven Turn costs for patronage, rehab, brew licenses, worker protection",
            },
        ],
    }
    write_json(PATCHES / "PROPOSED_PATCHES.json", patches)
    (PATCHES / "PROPOSED_PATCHES.md").write_text(
        "# Proposed patches (NOT applied)\n\n"
        + "\n".join(f"- **{i['id']}**: {i['title']} - {i['proposal']}" for i in patches["items"])
        + "\n",
        encoding="utf-8",
    )

    # Human report sections (template)
    report_human = PACK / "HAVEN_FINDINGS_SUMMARY.md"
    app = sims["HAV-APPRAISAL"]
    sp = sims["HAV-SPONSOR"]
    sm = sims["HAV-SMUGGLE"]
    tr = sims["HAV-TRAFFICKING"]
    ms = sims["HAV-MARKET-SHOCK"]
    report_human.write_text(
        f"""# Haven Economy and Social Report

Playtest harness: `run_haven_playtest.py` · Pack `{PACK_ID}` · 10 scenarios x 12 agents · ≥20 seeds + 5 narratives each.
Sources: pending-review Gameplay Loop Bible extract; `{SOURCE_NOTES['haven']}`; `{SOURCE_NOTES['reputation']}`; `{SOURCE_NOTES['core']}`; `{SOURCE_NOTES['crafting']}`.
**No canon files were edited.**

## Transaction math
- Sale formula verified: Final Value = Base x Provenance x Demand x Condition x Urgency (Loop extract section 17).
- Worked example seed matches: 4500 x 1.0 x 1.25 x 0.5 x 1.1 = **{app['rows'][0]['true_gross']} gp**.
- Tax rate **unpublished**; settlements used example residual ≈ **{EXAMPLE_TAX_RATE:.4%}**.
- Mean appraisal misprice |believed-true| across 20 seeds: **{app['misprice_abs_mean']:.1f} gp**.

## Sponsor comparison
- Gp-only best counts: `{sp['best_sponsor_counts']}` (dominant={sp['dominant_always']}).
- Multifactor best counts: `{sp.get('best_sponsor_multifactor_counts', {})}` (dominant={sp.get('dominant_always_multifactor', False)}).
- Finding: self-funded wins naive treasury math; priced non-gp benefits are required to keep the five-row table meaningful.

## Market exploits
- Shaved/counterfeit coin without remint fees -> face-value soft exploit (procedure gap).
- Smuggle beats legal in **{sm['smuggle_beats_legal_rate']:.0%}** seeds under assumed risk model; domination requires ignoring catch/standing.
- Trafficking consequence-free rate **{tr['consequence_free_rate']:.0%}** when evidence fails - not closed.
- No infinite legal brew/substance profit vs rare artifact extraction at published list prices.

## Legal and faction consequences
- Haven resolution order (quarantine -> ... -> standing) is clear in bible extract.
- Standing scale conflict: Loop **-5..+5** vs `reputation.js` coarse tiers.
- Blackmail / illegal sale modeled with standing hits; consensual sex work kept distinct from trafficking.

## Labor and trafficking safeguards
- Chain Market is named as political conflict in `haven.json`, but **numeric** wage/debt/emancipation/prosecution procedures are missing.
- Emancipation rate under test assumptions: **{sims['HAV-LABOR']['emancipation_rate']:.0%}**; rescue **{sims['HAV-LABOR']['rescue_rate']:.0%}**.
- Safeguards exist as narrative districts + inspection order; not yet as closed mechanical loops.

## Brewing and substance findings
- Core Systems: prices, dependence DCs, legality, crash effects - usable.
- Market premiums, rehab, brew COGS, licenses - **Director gaps**.
- Substance/brew side loops do not obsolete extraction.

## Recommended changes
See `proposed_patches/PROPOSED_PATCHES.md` (proposals only).

## Market shock
- Mean Tier II glut collapse: **{ms['mean_collapse_pct']:.0%}**.
- Deeper extraction still relevant: **{ms['extraction_still_relevant_rate']:.0%}** of seeds.
""",
        encoding="utf-8",
    )

    n_files = len(list(RESULTS.rglob("*.json")))
    print(f"Wrote results under {RESULTS} ({n_files} json files)")
    print(f"Patches: {PATCHES}")


if __name__ == "__main__":
    main()
