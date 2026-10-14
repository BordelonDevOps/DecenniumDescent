"""Record reversible review metadata after EX58-X01 fulfillment; change no rules."""
from pathlib import Path
from hashlib import sha256
from datetime import datetime, timezone
import copy
import json
import re

G=Path(r'C:\Github\DecenniumDescent')
R=G/'DescentReviewChanges/ReviewBible'
A=G/'docs/audit/2026-10-08/full-game'
STATUS='Reviewed authored expedition, transport, social and reputation candidate under EX58-EXACT-2026-10-11; runtime, human testing and final whole-game flow remain open.'
def read(p):return json.loads(p.read_text('utf-8-sig'))
def info(p):
    b=p.read_bytes();return {'bytes':len(b),'sha256':sha256(b).hexdigest()}
def encode(d):return (json.dumps(d,ensure_ascii=False,indent=2)+'\n').encode('utf-8')

def main():
    fulfillment=read(A/'EX58_X01_FULFILLMENT.json')
    assert fulfillment['exactCandidateAuthoredApproval'] is True
    target=A/'EX58_REVIEW_LABEL_NORMALIZATION.json'
    statusfile=R/'docs/mechanics/expedition/EXPEDITION_REVIEW_STATUS.json'
    backup=A/'ex58-before-review-labels'
    assert not target.exists() and not backup.exists() and not statusfile.exists()
    for rel,row in fulfillment['changedCandidateFiles'].items():assert info(G/rel)==row['preLabelCurrent']
    pub='DescentReviewChanges/ReviewBible/data/public/expedition_candidate/complete_candidate.json'
    internal='DescentReviewChanges/ReviewBible/data/director/expedition_candidate/complete_candidate.json'
    player='DescentReviewChanges/ReviewBible/docs/mechanics/expedition/EXPEDITION_PLAYER_BOOK.md'
    director='DescentReviewChanges/ReviewBible/docs/mechanics/expedition/EXPEDITION_DIRECTOR_BOOK.md'
    json_ops=[{'path':pub,'key':'status','old':'Complete EX58 authored assembly; exact GPT candidate review pending','new':STATUS},
              {'path':pub,'key':'exactCandidateApproved','old':False,'new':True},
              {'path':internal,'key':'status','old':'Complete EX58 authored assembly; exact GPT candidate review pending','new':STATUS}]
    text_ops=[
        {'path':player,'old':'Review candidate. These six chapters form one reading path for expedition play, transport, social scenes and standing. Exact GPT review remains pending. Use the existing Core rules alongside this book.',
         'new':'These six chapters form the reviewed authored playtest reading path for expedition play, transport, social scenes and standing. GPT’s exact review is fulfilled, including the EX-W13 resource correction. Use the existing Core rules alongside this book. Runtime implementation, human testing and final whole-game flow review remain open. [Review status](EXPEDITION_REVIEW_STATUS.json).'},
        {'path':player,'old':'## Timing change awaiting review','new':'## Reviewed example timing'},
        {'path':director,'old':'Read the [Expedition Player Book](EXPEDITION_PLAYER_BOOK.md) for the complete player procedures. This companion holds all Director procedures, worked chapter cases, record contracts and complete integrated examples. Exact GPT review remains pending.',
         'new':'Read the [Expedition Player Book](EXPEDITION_PLAYER_BOOK.md) for the complete player procedures. This companion holds the reviewed authored Director procedures, worked chapter cases, record contracts and complete integrated examples. The exact EX58 review is fulfilled, including the EX-W13 resource correction; runtime implementation, human testing and final whole-game flow review remain open. [Review status](EXPEDITION_REVIEW_STATUS.json). Historical component review labels remain preserved.'},
        {'path':director,'old':'## Explicit review issue','new':'## Reviewed example timing'},
        {'path':director,'old':'Review the entire revised chronology, including rest, light, provisions, faction work and provider schedules.','new':'The exact review retains the entire revised chronology, including rest, light, provisions, faction work and provider schedules.'},
    ]
    paths=[pub,internal,player,director]
    originals={rel:(G/rel).read_bytes() for rel in paths}
    staged={}
    for rel in [pub,internal]:
        obj=read(G/rel)
        for op in json_ops:
            if op['path']==rel:assert obj[op['key']]==op['old'];obj[op['key']]=op['new']
        inverse=copy.deepcopy(obj)
        for op in json_ops:
            if op['path']==rel:inverse[op['key']]=op['old']
        assert encode(inverse)==originals[rel], 'JSON inverse must restore full pre-label bytes'
        staged[rel]=encode(obj)
    for rel in [player,director]:
        text=originals[rel].decode('utf-8')
        for op in text_ops:
            if op['path']==rel:assert text.count(op['old'])==1;text=text.replace(op['old'],op['new'])
        inverse=text
        for op in reversed(text_ops):
            if op['path']==rel:assert inverse.count(op['new'])==1;inverse=inverse.replace(op['new'],op['old'])
        assert inverse.encode('utf-8')==originals[rel], 'Text inverse must restore complete rendered book'
        staged[rel]=text.encode('utf-8')
    for rel,b in originals.items():
        p=backup/rel;p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes(b)
        assert p.read_bytes()==b
    for rel,b in staged.items():(G/rel).write_bytes(b)
    checked=[]
    for rel in [player,director]:
        p=G/rel
        for url in re.findall(r'\[[^\]]*\]\(([^)]+)\)',p.read_text('utf-8')):
            if '://' in url:continue
            file,sep,anchor=url.partition('#'); q=(p.parent/file).resolve() if file else p
            assert q.is_file() or q==statusfile
            if anchor and q.suffix=='.md':
                source=q.read_text('utf-8')
                anchors=re.findall(r'<a id="([^"]+)"',source)
                anchors += [re.sub(r'[^\w\- ]','',s.lower()).replace(' ','-') for s in re.findall(r'^#+\s+(.*)$',source,re.M)]
                assert anchor in anchors,(rel,url)
            checked.append({'file':rel,'link':url})
    for rel in fulfillment['changedCandidateFiles']:
        if rel not in paths: assert info(G/rel)==fulfillment['changedCandidateFiles'][rel]['preLabelCurrent']
    current={rel:info(G/rel) for rel in fulfillment['changedCandidateFiles']}
    status={'status':STATUS,'reviewId':'EX58-EXACT-2026-10-11','replyId':'e1b66405-efca-40d8-9986-31fe30323dff',
            'correction':'EX58-X01 fulfilled','exactCandidateAuthoredApproval':True,'newRuleChanges':0,
            'reviewedScope':{'sourceDirections':58,'chapterExamples':190,'transportProfiles':29,'auxiliaries':4,'integratedEvents':21,'contracts':15,'boundaryExamples':28,'socialExamples':24},
            'originalSourceStatusLabels':'Preserved as historical evidence. Current review applies only to the EX58 authored candidate.',
            'runtimeImplemented':False,'selectionEnabled':False,'humanPlaytestConfirmed':False,'balanceApproved':False,'wholeGameFlowConfirmed':False,'pushPerformed':False,'cosmologyReviewed':False,
            'currentArtifactBindings':current,'fulfillmentReceipt':(A/'EX58_X01_FULFILLMENT.json').relative_to(G).as_posix(),
            'labelProof':target.relative_to(G).as_posix(),
            'generatorPolicy':'Original assembly and boundary builders are historical and must not overwrite the reviewed descendants. The two one-use amendment tools and exact before/after receipts reproduce the reviewed current version.'}
    statusfile.write_bytes(encode(status))
    result={'recordedAtUtc':datetime.now(timezone.utc).isoformat(),'reviewId':status['reviewId'],'status':'PASS — independently reversible review-label-only normalization',
            'jsonOperations':json_ops,'textOperations':text_ops,'originalsPreserved':{rel:{'path':(backup/rel).relative_to(G).as_posix(),**info(backup/rel)} for rel in paths},
            'currentEightCandidateFiles':current,'fullInverseEquality':True,'gameplayValuesChanged':0,'historicalSourceLabelsChanged':0,
            'readingLinksChecked':len(checked),'links':checked,'reviewStatusFile':{'path':statusfile.relative_to(G).as_posix(),**info(statusfile)},
            'scope':'Three top-level JSON metadata fields and five exact review/presentation strings only. Inversion reconstructs all four complete verified pre-label files byte for byte; the other four corrected files are unchanged.'}
    target.write_bytes(encode(result))
    print(json.dumps({k:result[k] for k in ['status','fullInverseEquality','gameplayValuesChanged','readingLinksChecked']},indent=2))

if __name__=='__main__':main()
