"""Independently replay the finite patch and check preservation, not game execution."""
from copy import deepcopy
from datetime import datetime,timezone
from pathlib import Path
import hashlib,json
from apply_di7_ap_as_01 import G,R,A,info,encoded

def read(p):return json.loads(p.read_bytes())

def main():
    root=A/'relic-null-03-local-patch-01';cand=root/'candidate';old=A/'cosmology-epilogue-relic-null-03-return'
    receipt=A/'RELIC_NULL_03_LOCAL_PATCH_01_VALIDATION.json';assert not receipt.exists()
    patch=read(root/'PATCH_MANIFEST.json');checks=[]
    def ck(name,ok):checks.append({'name':name,'passed':bool(ok)})
    trees={n:read(old/n) for n in ['RELIC_NULL_MODEL.json','CASEBOOK.json']}
    texts={n:(old/n).read_text(encoding='utf-8') for n in ['PLAYER_CHAPTER.md','DIRECTOR_CHAPTER.md']}
    for i,op in enumerate(patch['operations']):
        name=op['file']
        if 'jsonPointer' in op:
            parts=op['jsonPointer'].strip('/').split('/');node=trees[name]
            for p in parts[:-1]:node=node[int(p)] if isinstance(node,list) else node[p]
            key=int(parts[-1]) if isinstance(node,list) else parts[-1]
            present=(isinstance(node,list) and key<len(node)) or (isinstance(node,dict) and key in node)
            ck(f'operation{i+1}-precondition',node[key]==op['old'] if present else op['old'] is None)
            node[key]=deepcopy(op['replacement'])
        else:
            ck(f'operation{i+1}-precondition',texts[name].count(op['old'])==op['expectedOccurrences'])
            texts[name]=texts[name].replace(op['old'],op['replacement'])
    for name,tree in trees.items():
        got=read(cand/name);got.pop('localCorrectionProposal');ck(name+'-exact-replay',tree==got)
    for name,value in texts.items():
        value=value.replace('the same 84 frozen/current source bindings are used.','the original84 frozen/current source bindings are retained; current GAMEPLAY_LOOP_CANON.md is additionally supplied as source85 for the existing12-character cap.')
        value='> Local correction proposal01 to the preserved revision03. GPT review is pending; this is not adopted.\n\n'+value
        ck(name+'-exact-replay',value==(cand/name).read_text(encoding='utf-8'))
    reg=read(cand/'REGISTER.json');reg.pop('localCorrectionProposal');ck('register-history-preserved',reg==read(old/'REGISTER.json'))
    sources=read(cand/'SOURCE_HASHES.json')['sources'];ck('84-source-entries-identical',sources[:84]==read(old/'SOURCE_HASHES.json')['sources'])
    extra=sources[-1];ck('source85-exact-current-and-frozen',len(sources)==85 and info(G/extra['path'])==extra and (root/'additional_sources'/extra['path']).read_bytes()==(G/extra['path']).read_bytes())
    for entry in read(cand/'EVIDENCE_MANIFEST.json')['files']:
        b=(cand/entry['path']).read_bytes();ck('manifest-'+entry['path'],len(b)==entry['bytes'] and hashlib.sha256(b).hexdigest()==entry['sha256'])
    native=read(A/'RELIC_NULL_LOCAL_PATCH_01_NATIVE_DELIVERY.json')['nativeRead']
    actual=Path(next(x['path'] for x in native['attachments'] if x['name']=='DD_Relic_Null_03_Local_Patch_01.zip'))
    ck('actual-upload-byte-identical',actual.read_bytes()==(A/'DD_Relic_Null_03_Local_Patch_01.zip').read_bytes())
    ck('native-user-request-exact',native['turns'][0]['items'][0]['content'][0]['text'].startswith((A/'RELIC_NULL_03_LOCAL_PATCH_01_REVIEW_REQUEST.txt').read_text(encoding='utf-8').rstrip()))
    fail=[x for x in checks if not x['passed']]
    receipt.write_bytes(encoded({'recordedAtUtc':datetime.now(timezone.utc).isoformat(),'patchArchive':info(A/'DD_Relic_Null_03_Local_Patch_01.zip'),'checks':checks,'checkCount':len(checks),'failureCount':len(fail),'failures':fail,'scope':'Exact patch replay, manifest/source preservation and actual submitted bytes. Not runtime, semantic approval or human testing.','newRulesAdopted':False,'runtimeTestsExecuted':0}))
    print(json.dumps({'receipt':info(receipt),'checks':len(checks),'failures':fail}))

if __name__=='__main__':main()
