"""Independent read-only DI7 submission checks. No submitted file is written.
This checks preservation, complete mirrors/rendering and referenced evidence.
It does not execute arbitrary spell effects or authenticate campaign premises.
"""
from pathlib import Path
from copy import deepcopy
import argparse, collections, hashlib, json, zipfile

def sha(b): return hashlib.sha256(b).hexdigest()
def node(d,p):
    if p=='': return d
    for k in p.strip('/').split('/'):
        k=k.replace('~1','/').replace('~0','~')
        d=d[int(k)] if isinstance(d,list) else d[k]
    return d

def locate(d,p):
    parent,_,key=p.rpartition('/'); d=node(d,parent)
    return d,int(key) if isinstance(d,list) else key.replace('~1','/').replace('~0','~')
def encode(d,crlf=False):
    b=(json.dumps(d,ensure_ascii=False,indent=2)+'\n').encode()
    return b.replace(b'\n',b'\r\n') if crlf else b

def main():
    pa=argparse.ArgumentParser();pa.add_argument('--submission',type=Path,required=True);pa.add_argument('--out',type=Path,required=True);args=pa.parse_args()
    root=args.submission;out=args.out;checks=[]
    def ck(label,predicate,detail=None):
        checks.append({'label':label,'pass':bool(predicate),**({'detail':detail} if detail is not None else {})})
    cache={}
    def read(p):
        if p not in cache: cache[p]=json.loads((root/p).read_bytes())
        return cache[p]
    manifest=read('PACKAGE_MANIFEST.json');data={};byhash=collections.defaultdict(list)
    for rel,binding in manifest.items():
        b=(root/rel).read_bytes();data[rel]=b;byhash[sha(b)].append(rel)
        ck('payload/'+rel,len(b)==binding['bytes'] and sha(b)==binding['sha256'])
    R='DescentReviewChanges/ReviewBible/';A='docs/audit/2026-10-08/full-game/';V=A+'di7-joint-review-01-verdict/'
    ppath=R+'data/public/spell_candidates/divination_rank7_exact_01.json';ipath=R+'data/director/spell_candidates/divination_rank7_exact_01.json';mpath=R+'docs/spells/candidates/DIVINATION_RANK7_EXACT_01.md';epath=R+'data/playtest/spell_candidates/divination_rank7_exact_01_expectations.json'
    public=read(ppath);internal=read(ipath);catalog=read(R+'data/public/spell_playtests/catalog.json');cat={x['id']:x for x in catalog['spells']};contexts=read('CURRENT_REVIEW_CONTEXT.json')
    def binding(b):
        return b['path'] in data and len(data[b['path']])==b['bytes'] and sha(data[b['path']])==b['sha256']
    for b in contexts['currentCandidates']:ck('context/'+b['path'],binding(b))
    ck('whole-public-envelope-equality',public==internal['completePublicEnvelope'])
    ck('public-byte-binding',binding(internal['publicEnvelopeBinding']))
    ck('whole-current-expectation-envelope',read(epath)==internal['finiteExpectations'])
    ids=['mass-revelation','premonition-shield','fate-echo','vision-quest','faction-omniscience','alignment-purge','resonance-sight-supreme']
    ck('seven-exact-ids-and-order',[c['id'] for c in public['cards']]==ids)
    ck('seven-original-null-operations',all(cat[i]['operational'] is None for i in ids))
    sourceenv=internal['preservedSourceDirectionEnvelope'];srecords={x['spellId']:x for x in sourceenv['records']}
    for i,c in enumerate(public['cards']):
        sid=c['id'];orig=c['preservedSourceAndProposalFields'];op=c['operationalCandidate']
        ck(sid+'/complete-original-equality',orig['fullSourceAndCurrentAccessRecord']==cat[sid])
        ck(sid+'/preserved-source-metadata',orig=={k:v for k,v in srecords[sid].items() if k not in ['procedure','workedCases']})
        ck(sid+'/actual-access',op['classAccess']==cat[sid]['classAccess'])
        ck(sid+'/school-rank-price-components',(op['school'],op['rank'],op['baseRpCost'],op['activation'],op['components'])==('Divination',7,17,'Action',['V','S','F']))
        ck(sid+'/range',op['rangeFeet']==(60 if sid=='mass-revelation' else 120))
        ck(sid+'/concentration',op['concentrationRequiredByOuterEffect']==(sid in ['vision-quest','alignment-purge']))
        ck(sid+'/unapproved-flags',c['approved'] is False and c['selectable'] is False)
        ck(sid+'/full-procedure',isinstance(op['completeProcedure'],str) and len(op['completeProcedure'])>1000)
        ck(sid+'/two-original-corrected-examples',len(op['workedCases'])==2)
        ck(sid+'/source-public',cat[sid]['visibility']=='public-source-review')
    ck('receipt-not-operative',cat['planar-summons-greater']['operational'] is None and 'planar-summons-greater' not in ids)
    ck('14-issues-in-order',[x['id'] for x in public['issueMap']]==['DI7-X%02d'%i for i in range(1,15)])
    for issue in public['issueMap']:ck('issue-source/'+issue['id'],issue in internal['completeSourceDecisionRegister']['issues'] if 'issues' in internal['completeSourceDecisionRegister'] else issue['exactApproval'] is False)
    ck('14-example-dispositions',len(internal['originalExampleDispositions'])==14)
    examples={e['id']:e for e in internal['originalExampleDispositions']}
    for c in public['cards']:
        for e in c['operationalCandidate']['workedCases']:
            ck('corrected-example/'+e.split(':')[0],e==examples[e.split(':')[0]]['replacement'])
    for entry in contexts['currentClassEnvelopes']:
        ck('current-class/'+entry['path'],binding(entry['currentBinding']))
    for entry in sourceenv['completeClassComparisons']:
        ck('whole-class-envelope/'+entry['path'],read(entry['path'])==entry['completeCurrentEnvelope'])
    for entry in internal['activeCounterparts']:
        ck('whole-active-counterpart/'+entry['id'],entry['completeCurrentCatalogCard']==cat[entry['id']])
        ck('counterpart-binding/'+entry['id'],binding(entry['currentCatalogBinding']))
    # Reconstruct the complete manuscript independently, including every paragraph.
    parts=['# Divination rank 7 — exact candidate 01','Seven complete authored candidate procedures. Source-direction agreement is recorded; finite follow-through and separate exact-card review remain. No ordinary catalog entry is promoted.','These are complete unapproved candidate cards. Original source fields are preserved in the accompanying public/internal records. KEEP and NEW labels distinguish retained source from the agreed authored directions.','## Shared operating rules']
    for key,val in public['sharedOperatingRules'].items():parts += ['### '+key,val]
    for c in public['cards']:
        op=c['operationalCandidate'];parts += [f"## {c['name']} ({c['id']})",f"{op['activation']} · {op['school']} rank {op['rank']} · base {op['baseRpCost']} RP · {'/'.join(op['components'])} · {op['rangeFeet']} feet",'Access: Cleric/Wizard class 13; Mirrorsage/Shaman class 19, with actual retained acquisition and repertoire.',op['targetingSummary'],op['durationSummary'],op['concentrationQualification'],op['completeProcedure'],'### Corrected conditional examples',*op['workedCases']]
    pair=public['alignmentPairControllingException'];parts += ['## Alignment Suggestion counterpart',pair['lowerCardReplacement'],pair['sharedGuideReplacement'],'## Boundaries',public['audienceBoundary'],public['receiptOnlyBoundary']]
    rendered='\n\n'.join(parts)+'\n'
    ck('entire-manuscript-render-equality',data[mpath]==rendered.encode(),{'expectedBytes':len(rendered.encode()),'actualBytes':len(data[mpath])})
    ck('alignment-public-entire-active-card',pair['completeCurrentAlignmentSuggestionCard']==cat['alignment-suggestion'])
    ck('alignment-exact-lower-resolution',pair['lowerCardReplacement']==cat['alignment-suggestion']['operational']['resolution'])
    ck('alignment-active-guide',pair['sharedGuideReplacement'] in data[R+'docs/mechanics/SPELL_INTEGRATION_RULES.md'].decode())
    # Replay and reverse all eighteen source-direction substitutions, in memory.
    ops=read(V+'EXACT_DI7_CORRECTIONS.json')['changes']
    ck('18-source-substitutions',len(ops)==18)
    for proof in internal['sourceDescendantProofs']:
        for name in ['source','reviewerReference','newDescendant']:ck('source-proof-binding/'+proof[name]['path'],binding(proof[name]))
        original=read(proof['source']['path']);d=deepcopy(original)
        for n,op in enumerate(ops):
            parent,key=locate(d,op['pointer']);ck('source-old-guard/'+proof['source']['path']+'/'+str(n),parent[key]==op['old']);parent[key]=deepcopy(op['replacement'])
        ck('whole-source-descendant/'+proof['newDescendant']['path'],d==read(proof['newDescendant']['path']))
        for op in reversed(ops):
            parent,key=locate(d,op['pointer']);ck('source-inverse-guard/'+proof['source']['path']+op['pointer'],parent[key]==op['replacement']);parent[key]=deepcopy(op['old'])
        b=data[proof['source']['path']];ck('source-byte-inverse/'+proof['source']['path'],d==original and b in [encode(d),encode(d,True)])
    # Every later guarded change must have both measured endpoints somewhere in this frozen packet.
    names=['DI7_AP_AS_01_DERIVED_OPERATIONS.json','DI7_ACQ19_DERIVED_OPERATIONS.json','DI7_SHIELD_LATE_DERIVED_OPERATIONS.json','DI7_VISION_COMMUNICATION_DERIVED_OPERATIONS.json','DI7_GEOMETRY_DERIVED_OPERATIONS.json','DI7_FACTION_REFERENCE_DERIVED_OPERATIONS.json','DI7_SUPREME_TIME_SCOPE_DERIVED_OPERATIONS.json','DI7_SHAMAN_VENT_DERIVED_OPERATIONS.json','DI7_ALIGNMENT_COPY_SOURCE_DERIVED_OPERATIONS.json']
    for name in names:
        delta=read(A+name)
        for n,change in enumerate(delta['changes']):
            b=change['before'];aft=change['after'];bp=b['preservedCopy'];before=data[bp];ck(name+f'/{n}/before',sha(before)==b['sha256'] and len(before)==b['bytes'])
            ck(name+f'/{n}/after-present',aft['sha256'] in byhash)
            if aft['sha256'] not in byhash:continue
            after=data[byhash[aft['sha256']][0]]
            seq=change.get('operations',[change['operation']] if 'operation' in change else [])
            if b['path'].endswith('.json'):
                orig=json.loads(before);d=deepcopy(orig)
                for j,op in enumerate(seq):
                    parent,key=locate(d,op['pointer'])
                    if op.get('add'):
                        ck(name+f'/{n}/{j}/absent-add',key not in parent);parent[key]=deepcopy(op['replacement'])
                    else:
                        ck(name+f'/{n}/{j}/old',parent[key]==op['old']);parent[key]=deepcopy(op['replacement'])
                ck(name+f'/{n}/complete-object-change',d==json.loads(after))
                for op in reversed(seq):
                    parent,key=locate(d,op['pointer'])
                    if op.get('add'):del parent[key]
                    else:parent[key]=deepcopy(op['old'])
                ck(name+f'/{n}/exact-byte-inverse',d==orig and before in [encode(d),encode(d,True)])
            else:
                text=before.decode()
                for j,op in enumerate(seq):
                    ck(name+f'/{n}/{j}/text-occurrence',text.count(op['old'])==op.get('expectedOccurrences',op.get('occurrences',1)))
                    text=text.replace(op['old'],op['replacement'])
                ck(name+f'/{n}/text-change',text.encode()==after)
    # Verify all exact finite expectation memberships and pointed-to histories.
    expectations=read(epath);groups=expectations['groups']+expectations['supplementalSourceExpectations'];vs=[v for g in groups for v in g['variants']];vmap={v['id']:v for v in vs};inv=read(A+'DI7_FINITE_93_EVIDENCE_INVENTORY.json')
    ck('49-original-44-supplemental',sum(len(g['variants']) for g in expectations['groups'])==49 and sum(len(g['variants']) for g in expectations['supplementalSourceExpectations'])==44)
    ck('93-unique-expectations',len(vs)==len(vmap)==93)
    ck('inventory-exact-membership',{x['id'] for x in inv['rows']}==set(vmap))
    for row in inv['rows']:
        ck('inventory-expectation/'+row['id'],row['expectation']==vmap[row['id']])
        for n,e in enumerate(row.get('evidence',[])):
            if isinstance(e,dict) and 'report' in e:
                ck('evidence-binding/'+row['id']+f'/{n}',binding(e['report']))
                if 'pointer' in e and e['pointer'].startswith('/histories/'):
                    h=node(read(e['report']['path']),e['pointer']);ck('history-identity/'+row['id']+f'/{n}',h.get('id')==e['historyId'])
    ck('flags-retained',all(public[x] is False for x in ['exactReviewReceived','selectionEnabled','runtimeImplemented','cosmologyReviewed','pushed']))
    ck('catalog848-retained',len(cat)==848)
    for b in read(A+'DI7_AP_AS_01_ACTIVE_COUNTERPART_CONTROL.json')['activeMirrors']:ck('AP-AS-current-mirror/'+b['path'],binding(b))
    # This is an exact pass/fail list, not a semantic/runtime certification.
    result={'scope':'Executed read-only byte, object, full-render, provenance, exact-case/history-reference checks. Not full spell runtime or campaign authentication.','checks':len(checks),'passed':sum(c['pass'] for c in checks),'failed':[c for c in checks if not c['pass']],'rows':checks}
    out.write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps({k:v for k,v in result.items() if k!='rows'},ensure_ascii=False,indent=2))
if __name__=='__main__':main()
