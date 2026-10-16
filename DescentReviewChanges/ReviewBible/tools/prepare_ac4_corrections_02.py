"""Freeze independent semantic findings and the complete current AC4 review context."""
from datetime import datetime, timezone
from pathlib import Path
from zipfile import ZipFile, ZIP_DEFLATED
import json
from apply_di7_ap_as_01 import G, R, A, info, encoded

def read(p): return json.loads(p.read_bytes())

def main():
    root=A/'ac4-corrections-02-input'
    archive=A/'DD_AC4_Corrections_02.zip'
    receipt=A/'AC4_CORRECTIONS_02_PREPARATION.json'
    assert not any(p.exists() for p in [root,archive,receipt])
    original=read(A/'ac4-current-review-01-input/CURRENT_REVIEW_INPUT.json')
    returned=A/'ac4-current-review-01-return-01'
    model=read(returned/'SPELLS_MODEL.json')
    player=(returned/'PLAYER_CHAPTER.md').read_text(encoding='utf8')
    checks=[]
    def ck(name, value):
        checks.append({'name':name,'passed':bool(value)})
    for b in original['sourceBindings']:
        ck('Current frozen source '+b['path'], info(G/b['path'])==b)
    for card in model['spells']:
        ck('Player exact full procedure '+card['spellId'],player.count(card['procedure'])==1)
    assert all(c['passed'] for c in checks)
    findings=[
      {'id':'AC4-C01','kind':'exact clock omission','locations':['SPELLS_MODEL.json#/sharedRules/timing','SPELLS_MODEL.json#/spells/1/procedure','PLAYER_CHAPTER.md Time and Spell Shield'],
       'finding':'Shared timing scopes the one-minute clock to concentration effects, but Spell Shield expressly has no concentration and supplies no exact endpoint of its own.',
       'proposal':'Give Spell Shield the tenth future caster regular-start marker after application in initiative, excluding a start already in progress/past; outside initiative application+60 seconds. Preserve the fixed virtual/absolute deadline across entry/exit, reorder, extra turns, absence/death and suppression; caster death alone does not end this nonconcentration ward. Keep source-specific clocks distinct. Add a concrete expiry/suppression example.'},
      {'id':'AC4-C02','kind':'contradictory eligibility','locations':['SPELLS_MODEL.json#/spells/14/procedure','CASEBOOK.json AC4-16-B'],
       'finding':'Faction Ally first requires actual membership AND invocation permission, but its appended interface permits membership/affiliation and permission only where required. Those are different gates. The original example expressly requires both.',
       'proposal':'Use actual recorded membership in one exact canonical faction AND recorded source/campaign invocation permission under Faction Seal. Affiliation/standing alone cannot qualify. Keep Sanctuary caster invocation permission independent from recipient membership. If you prefer a different NEW gate, explicitly justify it and harmonize every procedure/example; do not leave both readings.'},
      {'id':'AC4-C03','kind':'cast identity versus damage-root creation','locations':['SPELLS_MODEL.json#/spells/1/procedure','CASEBOOK.json AC4-X01 and AC4-X02','COSMOLOGY_EPILOGUE_RELIC_NULL_PLAYTEST.md creation-time damage flag'],
       'finding':'Pure redirection is coherent, but wording that no new damage root is created and that a pending cast already has its Null root can be read as allocating all damage roots at cast commitment. Accepted EPI instead evaluates the actual dealer at each damage-root creation; cast identity and damage-root identity are not synonyms.',
       'proposal':'Spell Shield itself creates no replacement damage root and does not advance the original spell damage-root checkpoint. Preserve an already-created root flag; when the original spell has not created its root yet, create it at its ordinary checkpoint under the original caster/dealer, then evaluate that dealer actual Veil state. Descendants inherit their real parent flag. Non-damaging Charm Person requires no damage root. Make X01 concrete with unchanged Veil through the real root checkpoint, then include a boundary variant where Veil changes before versus after creation. Do not invent a universal cast-time root.'},
      {'id':'AC4-C04','kind':'finite summon zero-state ambiguity','locations':['SPELLS_MODEL.json#/spells/7/procedure','SPELLS_MODEL.json#/spells/14/procedure','SPELLS_MODEL.json#/factionAllyProfile/lifecycle','CASEBOOK.json AC4-X06'],
       'finding':'The original prose still says at 0 HP it vanishes, while the appended exception only covers a positive-to-zero event. The accepted finite-summon rule replaces damage-caused disappearance and must also remain coherent for further qualifying Null damage to an already Disabled0 body.',
       'proposal':'Integrate the exception directly: ordinary non-Null damage can invoke the actual finite-summon endpoint; qualifying Null damage reaching or striking its already-Disabled0 body preserves that same body without death/loot, new recovery/expiry clocks or reapplication. Independent expiry, dismissal, replacement and concentration ending remain real. Add a repeated-Null-at0 case and an independent-expiry case. This is clarification of accepted EPI scope, not new immunity to unrelated ending.'},
      {'id':'AC4-C05','kind':'missing playable profile in player chapter','locations':['PLAYER_CHAPTER.md Faction Ally','SPELLS_MODEL.json#/factionAllyProfile'],
       'finding':'The player procedure promises the complete Faction Envoy profile below, but the chapter goes directly to Banishment. Its AC, HP, abilities, saves, attacks, commands and lifecycle appear only in the model. The Director prose also does not supply that profile.',
       'proposal':'Include the complete exact Envoy profile in PLAYER_CHAPTER.md, with all fields and the corrected eligibility/lifecycle. Reference its structured model location from the Director chapter. Keep nominal CR3 explicitly provisional, not certified. Check every other promised below/reference for actual content.'},
      {'id':'AC4-C06','kind':'unfinished targeting predicates','locations':['SPELLS_MODEL.json#/spells/7/procedure','SPELLS_MODEL.json#/spells/13/procedure','SPELLS_MODEL.json#/factionAllyProfile','CASEBOOK.json AC4-X06'],
       'finding':'Water Pet source heals an ally, whereas procedure says any willing living creature; preserve the actual ally requirement. The new living restriction for its heal and Beacon needs an explicit scope, and the two newly authored summon profiles have no living/nonliving targeting classification. X06 expressly leaves whether this Elemental qualifies for Healing Rite unresolved.',
       'proposal':'Complete these local predicates explicitly as NEW authorship. Preserve willing ally for Water Pet. Decide whether Beacon requires active creature identity rather than living biology, or state and justify the narrower new exclusion. Give Water Pet and Envoy exact mechanical eligibility for living-target effects/ordinary healing while they exist, without claiming natural origins, souls, corpse/loot or generic construct/undead rules. Use actual Cleric Healing Rite (living ally, Action2RP30ft,Sd8+M) for a fully resolved positive recovery example or a fully resolved rejection; do not hide the decision behind an unspecified independently legal heal.'},
      {'id':'AC4-C07','kind':'incorrect named comparison and incomplete transaction','locations':['CASEBOOK.json AC4-X09'],
       'finding':'The current reviewed ordinary spell is Summon Spectral Steed, stable ID summon-spectral-steed; Planar Crossing is its one-attempt Action. There is no reviewed Planar Steed identity in the catalog. The example omits the finite crossing use and supposes an unspecified legal foreign-plane mid-resolution cast.',
       'proposal':'Use exact Summon Spectral Steed and preserve owner BA command, mount Action, one crossing attempt spent at start, real rider/cargo limits and original concentration clock. A concrete independently maintained destination Anchor unknown to the traveler can defeat the committed crossing without inventing a free interrupt or cross-plane trigger perception. If retaining an after-commit event, identify an actual legal trigger/Reaction/source and all original paid costs; no free Action while another Action resolves.'},
      {'id':'AC4-C08','kind':'integration examples need resolved state and legal event order','locations':['CASEBOOK.json AC4-X03, AC4-X08, AC4-X13, AC4-X15'],
       'finding':'Several requested integration examples remain conditional sketches. X03 never supplies Suggestion caster orientation or resulting one-step overlay; X13 leaves Warding Bond shares/tempHP arithmetic unresolved; X08 uses generic unnamed waivers; X15 assumes an unspecified independent legal event between commitment and resolution.',
       'proposal':'Complete X03 with actual axis values/cast order/costs/saves/clocks in both lock-before and lower-overlay-before variants. X13 must state exact conserved shares, recipient HP/tempHP results and no second mitigation. X08 should use actual supplied class/source waiver examples with exact field-before-final-Influence arithmetic. X15 must use an actual sourced event timing permission or label a narrow NEW Beacon commit/revalidation checkpoint explicitly for joint agreement; no generic new interrupt windows. Preserve all original30 IDs/texts and existing X01..X15 identities. Additional bounded authored cases may be added with new IDs if needed. These are authored examples, not executed tests.'}
    ]
    catalog=read(R/'data/public/spell_playtests/catalog.json')
    refs=[]
    for name in ['acid-arrow','charm-person','summon-spectral-steed','warding-bond','resonance-influence','alignment-suggestion','faction-seal']:
        index=next(i for i,c in enumerate(catalog['spells']) if c['id']==name)
        refs.append({'id':name,'file':info(R/'data/public/spell_playtests/catalog.json'),'pointer':f'/spells/{index}','exactCurrentRecord':catalog['spells'][index]})
    cleric=R/'data/public/class_playtests/cleric.json';cd=read(cleric)
    index=next(i for i,c in enumerate(cd['cards']) if c['id']=='cleric.base.healing-rite')
    refs.append({'id':'cleric.base.healing-rite','file':info(cleric),'pointer':f'/cards/{index}','exactCurrentRecord':cd['cards'][index]})
    root.mkdir()
    finding_doc={'id':'DD-AC4-CORRECTIONS-02','recordedAtUtc':datetime.now(timezone.utc).isoformat(),'status':'Independent semantic findings for actual GPT conference; no adoption',
      'reviewedReturn':info(A/'DD_AC4_Current_Review_01_Return_01.zip'),'sourceIntegrityCheck':info(A/'AC4_CURRENT_REVIEW_01_RETURN_SOURCE_CHECK_01.json'),
      'readingCompleted':['All15 complete model procedures and shared interfaces','All45 examples','All original/current question dispositions','Full Player chapter, with15 exact procedure equality checks','Full Director chapter','Full Envoy profile','Current named comparison cards and scoped EPI Null damage/lifecycle rules'],
      'findings':findings,'exactComparisonRecords':refs,'checks':checks,'checkCount':len(checks),'failureCount':0,
      'newRulesAdopted':False,'sourceInformationDeleted':0,'runtimeTestsExecuted':0,'humanPlaytested':False}
    (root/'INDEPENDENT_FINDINGS.json').write_bytes(encoded(finding_doc))
    (root/'SOURCE_BINDINGS.json').write_bytes(encoded({'bindings':original['sourceBindings']}))
    instruction='''Continue the same AC4 fifteen-spell conference. Codex independently read your complete return, all45 examples and current source counterparts. Source integrity passed175 checks; a further85 source/prose checks pass. Those do not approve semantics. INDEPENDENT_FINDINGS.json lists AC4-C01..C08 with exact locations and proposed resolutions. Resolve all eight independently, disagree with evidence where appropriate, and harmonize the complete candidate. Do not merely append contradictory exceptions.

This archive includes every current frozen source file, your exact prior eight-file return, original CURRENT_REVIEW_INPUT.json, and exact current comparison records (including actual Summon Spectral Steed and Cleric Healing Rite). All70 source files remain byte-identical to your prior input. The original source/access records and source conflicts must remain intact. Keep all15 spell IDs/order, all30 original case IDs/text verbatim, and X01..X15 IDs. Additional authored cases may be added without deleting prior identity/history. Preserve Banishment source-only receipt; do not author or approve it in this correction batch.

Return one complete replacement DD_AC4_Corrections_02_Return.zip with exactly these eight root files: REGISTER.json, SPELLS_MODEL.json, PLAYER_CHAPTER.md, DIRECTOR_REVIEW.md, CASEBOOK.json, SOURCE_HASHES.json, VERDICT.md, EVIDENCE_MANIFEST.json. REGISTER must explicitly disposition C01..C08 and distinguish corrections from NEW scoped authorship. Model/chapter/profile/examples must agree. Include a full usable Envoy profile in the Player chapter. Preserve original question/source evidence, operational access, and named AP-AS-01/AC4-ALIGN-01 scope. Do not silently settle cosmology, natural origin or soul identity. Report archive bytes/SHA256 and an exact output-file manifest, and verify all70 supplied source bytes/hashes. Authoring examples are not runtime/human/balance tests. No whole-game approval. Complete the actual files before presenting the download.
'''
    (root/'README_REVIEW.txt').write_text(instruction,encoding='utf8',newline='\n')
    (root/'CURRENT_REVIEW_INPUT.json').write_bytes((A/'ac4-current-review-01-input/CURRENT_REVIEW_INPUT.json').read_bytes())
    with ZipFile(archive,'w',ZIP_DEFLATED,compresslevel=9) as z:
        for p in sorted(root.iterdir()): z.write(p,p.name)
        for p in sorted(returned.iterdir()): z.write(p,'prior-return/'+p.name)
        for b in original['sourceBindings']: z.write(G/b['path'],'sources/'+b['path'])
    request=A/'AC4_CORRECTIONS_02_REQUEST.txt'
    request.write_text(instruction+'\nAttached archive: '+archive.name+'\n'+json.dumps(info(archive),ensure_ascii=False)+'\n',encoding='utf8',newline='\n')
    receipt.write_bytes(encoded({'recordedAtUtc':datetime.now(timezone.utc).isoformat(),'archive':info(archive),'request':info(request),'findings':info(root/'INDEPENDENT_FINDINGS.json'),'sourceFiles':70,'findingsCount':8,'comparisonRecords':8,'checks':len(checks),'failureCount':0,'newRulesAdopted':False,'sourceInformationDeleted':0,'runtimeTestsExecuted':0,'actualGptSubmission':'Not yet submitted'}))
    print(json.dumps({'receipt':info(receipt),'archive':info(archive),'findings':8,'checks':len(checks),'failures':0}))

if __name__=='__main__': main()
