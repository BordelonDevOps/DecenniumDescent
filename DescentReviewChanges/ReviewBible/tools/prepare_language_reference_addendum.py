"""Reproduce the portable ZIP failure, then validate an unchanged four-file overlay."""
from pathlib import Path
from datetime import datetime, timezone
from zipfile import ZipFile, ZIP_DEFLATED
import hashlib
import json
import shutil
import subprocess
import sys

R=Path(__file__).resolve().parents[1];G=R.parents[1];A=G/'docs/audit/2026-10-08/full-game'
WORK=Path(r'C:\Users\cbord\Documents\ChatGPT\Decennium Descent\la-package-check')
def read(p):return json.loads(p.read_text(encoding='utf-8'))
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def save(p,d):p.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')

def main():
    archive=A/'DD_Language_Communication_Exact_Review_v1.zip'
    addition=A/'DD_Language_Exact_V1_Reference_Addendum.zip'
    assert not WORK.exists() and not addition.exists()
    expected_archive=read(A/'LANGUAGE_EXACT_V1_PREPARATION.json')['sha256']
    assert sha(archive)==expected_archive
    working_report=A/'LANGUAGE_CANDIDATE_VALIDATION.json';working_report_sha=sha(working_report)
    missing=read(A/'LANGUAGE_EXACT_V1_ARCHIVE_LINK_AUDIT.json')['missing']
    assert len(missing)==4
    with ZipFile(archive) as z:
        for name in z.namelist():
            assert not Path(name).is_absolute() and '..' not in Path(name).parts and ':' not in name and not name.startswith(('\\','/'))
        manifest=json.loads(z.read('FILE_MANIFEST.json'))
        assert all(hashlib.sha256(z.read(k)).hexdigest()==v['sha256'] for k,v in manifest.items())
        z.extractall(WORK)
    audit_in_work=WORK/'docs/audit/2026-10-08/full-game'
    copied_report=audit_in_work/'LANGUAGE_CANDIDATE_VALIDATION.json'
    shutil.copy2(copied_report,audit_in_work/'LANGUAGE_CANDIDATE_VALIDATION_AS_SUBMITTED.json')
    validator=WORK/'DescentReviewChanges/ReviewBible/tools/validate_language_candidate.py'
    baseline=subprocess.run([sys.executable,'-X','utf8',str(validator)],capture_output=True,text=True,encoding='utf-8')
    baseline_report=read(copied_report)
    assert baseline.returncode==1 and len(baseline_report['failed'])==4
    assert all(c['group']=='local-links' for c in baseline_report['failed'])
    shutil.copy2(copied_report,A/'LANGUAGE_EXACT_V1_PORTABLE_BASELINE.json')
    payload={}
    for entry in missing:
        p=G/entry['target'];assert sha(p)==entry['workingTreeSha256'] and p.stat().st_size==entry['workingTreeBytes']
        payload[entry['target']]=p.read_bytes()
        dest=WORK/entry['target'];assert not dest.exists();dest.parent.mkdir(parents=True,exist_ok=True);dest.write_bytes(payload[entry['target']])
    completed=subprocess.run([sys.executable,'-X','utf8',str(validator)],capture_output=True,text=True,encoding='utf-8')
    overlay_report=read(copied_report)
    assert completed.returncode==0 and overlay_report['candidateChecks']==496 and not overlay_report['failed']
    shutil.copy2(copied_report,A/'LANGUAGE_EXACT_V1_REFERENCE_OVERLAY_VALIDATION.json')
    readme='''# Four missing reference files for the frozen LA exact candidate v1

Prepared locally; UNSENT while request b152ba58-ee3a-4a1b-bcbe-4d7cc27e55cb remains under review. Do not interrupt or resend that active request. Incorporate this material into the final verdict fulfillment, with any actual bounded corrections.

This addendum contains the complete unchanged CLASS_PLAYTEST_INDEX.md, PALADIN_OATHS_AND_OATHBREAKERS.md, SCRIBING_CANDIDATE_RECIPE_CARDS.md and TINKERING_CANDIDATE_RECIPE_CARDS.md at the exact relative paths referenced by the submitted player chapter. They were omitted from the original ZIP but existed in the working tree; its link check therefore passed locally while failing in an isolated extraction.

The original ZIP, all184 payloads, source records, guide/data candidate bytes and original local496 report are preserved. In a new isolated extraction, the frozen validator reproduces exactly four missing-link failures. Adding only these four original reference files then produces496 checks/zero failures. These checks retain their original limited scope: source/static/public parity and38 reference calculations/boundaries. The32 semantic cases remain authored adjudications; no gameplay/runtime/human or GPT exact approval follows.

Apply only as an additive overlay to the actual frozen candidate. No source interpretation, class/spell/feat promotion, recipe change, deletion, push or cosmology review is included.
'''
    payload['README_REFERENCE_ADDENDUM.md']=readme.encode('utf-8')
    manifest={k:{'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()} for k,b in payload.items()}
    with ZipFile(addition,'w',ZIP_DEFLATED,compresslevel=9) as z:
        for name,b in payload.items():z.writestr(name,b)
        z.writestr('FILE_MANIFEST.json',json.dumps(manifest,ensure_ascii=False,indent=2)+'\n')
    assert sha(archive)==expected_archive and sha(working_report)==working_report_sha
    save(A/'LANGUAGE_EXACT_V1_REFERENCE_ADDENDUM_PREPARATION.json',{
        'atUtc':datetime.now(timezone.utc).isoformat(),'status':'Four-file additive reference repair prepared and verified in isolated extraction; UNSENT pending final exact verdict',
        'zip':str(addition),'bytes':addition.stat().st_size,'sha256':sha(addition),'payloadFiles':5,'manifest':manifest,
        'frozenArchive':str(archive),'frozenArchiveSha256':expected_archive,'isolatedValidationDirectory':str(WORK),
        'baselineReport':str(A/'LANGUAGE_EXACT_V1_PORTABLE_BASELINE.json'),'baselineChecks':496,'baselineFailures':4,
        'additiveOverlayReport':str(A/'LANGUAGE_EXACT_V1_REFERENCE_OVERLAY_VALIDATION.json'),'overlayChecks':496,'overlayFailures':0,
        'sourceAndCandidateBytesChanged':0,'originalWorkingTreeReportUnchanged':True,'submitted':False,'candidateApproved':False,'pushPerformed':False})
    print(json.dumps({'addendumBytes':addition.stat().st_size,'sha256':sha(addition),'baselineFailures':4,'afterOverlayChecks':496,'afterOverlayFailures':0,'submitted':False},indent=2))

if __name__=='__main__':main()
