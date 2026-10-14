"""Instantiate all 24 preserved social proposals under the EX58 directions."""
from pathlib import Path
from datetime import datetime, timezone
import base64
import copy
import hashlib
import json

G=Path(__file__).resolve().parents[3]
R=G/'DescentReviewChanges/ReviewBible'
A=G/'docs/audit/2026-10-08/full-game'
OUT=[R/'data/public/expedition_candidate/social_scenarios.json',
     R/'data/director/expedition_candidate/social_scenarios.json',
     R/'docs/mechanics/expedition/SOCIAL_SCENARIO_WALKTHROUGHS.md',
     R/'docs/mechanics/expedition/SOCIAL_SCENARIO_RECORDS.md',
     A/'EX58_SOCIAL_SCENARIO_CANDIDATE_CHECK.json']
CHECKS=[]

def read(p):return json.loads(p.read_text(encoding='utf-8-sig'))
def digest(p):
    b=p.read_bytes()
    return {'path':p.relative_to(G).as_posix(),'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()}
def check(name,passed,actual=None):
    CHECKS.append({'name':name,'passed':bool(passed),'actual':actual})
    if not passed:raise AssertionError(name+': '+repr(actual))
def interval(a,b,actors,activity):
    return {'startSeconds':a,'endSeconds':b,'actualSeconds':b-a,'actors':actors,'activity':activity,'halfOpen':True}
def task(natural,modifier,dc):
    m=natural+modifier-dc
    d=3 if m>=10 else 2 if m>=0 else 0 if m<=-10 else 1
    return ['Critical Failure','Failure','Success','Critical Success'][max(0,min(3,d+(1 if natural==20 else -1 if natural==1 else 0)))]
def roll(actor,natural,modifier,dc):
    return {'actor':actor,'nativeProcedure':'Core fixed-DC task','natural':natural,'modifier':modifier,'DC':dc,
            'total':natural+modifier,'degree':task(natural,modifier,dc)}
def raw_record(text,version):
    b=text.encode('utf-8')
    return {'utf8':text,'base64':base64.b64encode(b).decode(),'sha256':hashlib.sha256(b).hexdigest(),
            'producerVersion':version,'orderedMembers':[[k,v] for k,v in json.loads(text,object_pairs_hook=list)],'immutable':True,'realSave':False}
def frame(want,leverage,limit,seconds,witness):
    return {'Want':want,'Leverage':leverage,'Limit':limit,'ClockSeconds':seconds,'Witness':witness}

def main():
    for p in OUT:
        if p.exists():
            saved=read(A/'ex58-social-before-pair-representation-fix/manifest.json')[p.relative_to(G).as_posix()]
            assert digest(p)['sha256']==saved['sha256'],f'Unexpected output version; preserve before replacement: {p}'
    source_path=A/'ex58-final-gpt-verdict/EX58_WORKED_SEQUENCES.json'
    original=read(source_path)['originalProposalScenarios']
    part4_path=R/'data/director/expedition_candidate/part04.json'
    part6_path=R/'data/director/expedition_candidate/part06.json'
    part4=read(part4_path);part6=read(part6_path)
    player_source=next(x for x in part4['completeSelectedSourceBlocks'] if x['id']=='P-SOCIAL')
    alignment_receipt=[x for x in player_source['blocks'] if x.get('kind')=='paragraph' and 7820<=x.get('paragraphIndex',-1)<=7829]
    inputs=[source_path,part4_path,part6_path,
            R/'data/public/expedition_candidate/part04.json',R/'data/public/expedition_candidate/part06.json',
            R/'data/director/expedition_candidate/source_contracts_corrected.json',
            R/'docs/mechanics/CORE_RESOLUTION_PLAYTEST.md',R/'docs/mechanics/COMBAT_ACTION_PLAYTEST.md',
            R/'docs/mechanics/CONDITIONS_PLAYTEST.md',R/'docs/mechanics/LANGUAGE_COMMUNICATION_PLAYTEST.md']
    sources=[digest(p) for p in inputs]
    cases=[]
    def add(n,title,records,result,explanation):
        src=next(x for x in original if x['id']==f'SO-P-{n:02d}')
        cases.append({'id':src['id'],'schemaVersion':'EX58-social-instance-v1',
                      'status':'draft exact-candidate example','evidenceClass':'authored expectation; no executed gameplay',
                      'sourceQuestion':src['sourceQuestion'],'title':title,
                      'originalScenarioAndDisposition':copy.deepcopy(src),
                      'timeModel':'Each independent synthetic scenario has its own one shared clock; alternatives fork, not combine.',
                      'actualSyntheticRecords':records,'expectedFinalState':result,'readerExplanation':explanation,
                      'sourceBinding':{**digest(source_path),'pointer':f'/originalProposalScenarios/{n-1}'},
                      'newCanonicalWorldFact':False,'newPromotion':False})

    add(1,'An agreed request needs no check',
        {'scene':'SP01-ledger','participants':['Mira','clerk Ione'],
         'frame':frame('view ledger-1','existing signed appointment','view only; no copying or title transfer',600,['Ione']),
         'authority':{'IoneOwnsDeskPermission':True,'ledgerAvailable':True,'ledgerReadable':True},
         'agreement':{'atSeconds':0,'alreadyAccepted':True,'conditions':['supervised viewing','return ledger to same desk']},
         'viewing':interval(0,600,['Mira','Ione'],'actual supervised reading'),
         'roll':{'performed':False,'reason':'no unresolved uncertainty'},'cargoAfter':{'ledger-1':'original desk'}},
        {'elapsedSeconds':600,'viewingCompleted':True,'extraBenefitFromRoll':False},
        'The clerk already agrees and has the authority. Ten real minutes of supervised viewing occur without a roll, a free copy or any transfer of the ledger.')

    add(2,'A proposed natural 20 cannot create authority',
        {'scene':'SP02-title','participants':['Mira','clerk Ione'],'owner':'absent owner Hale',
         'frame':frame('transfer Hale’s storehouse','an appeal to convenience','Ione can schedule appointments only',60,['Ione']),
         'offeredDie':{'natural':20,'acceptedAsResolution':False},'missingPrerequisite':'actual owner authority or lawful representative instrument',
         'state':{'ownerBefore':'Hale','ownerAfter':'Hale'},
         'changedRequest':{'request':'schedule a meeting with Hale','authorityAvailable':True,'separateRecord':'SP02-meeting','elapsedSeconds':60}},
        {'ownershipChanged':False,'transferRollMade':False,'separateFeasibleRequestAvailable':True},
        'No roll is made for the unauthorized transfer. Asking for a meeting is a new feasible request with its own actual time and agreement.')

    add(3,'Meeting the announced DC earns the promised result',
        {'scene':'SP03-access','participants':['Mira','warden Oren'],
         'frame':frame('one supervised archive visit','actual appointment and stated research purpose','one room, one hour, real escort',600,['desk clerk']),
         'stakesBeforeRoll':{'DC':12,'Success':'grant the stated supervised visit without fee','CriticalSuccess':'same result; no additional benefit declared','Failure':'refuse this approach','CriticalFailure':'refusal, no invented fine'},
         'approach':interval(0,600,['Mira','Oren'],'actual negotiation'),'roll':roll('Mira',8,4,12),
         'result':{'visitGranted':True,'escort':'actual available Fen','newFeeCp':0,'hiddenDC22Applied':False}},
        {'total':12,'degree':'Success','promisedTermsHonored':True,'undisclosedCostCp':0},
        'A total of 12 meets DC 12 and grants exactly the promised visit. The Director does not reserve ordinary success for 22 or invent a fee after the roll.')
    check('SP03 exact success threshold',task(8,4,12)=='Success')

    add(4,'A costly agreement and an opposed tie are distinct',
        {'scene':'SP04-access','participants':['Mira','warden Oren'],'approach':interval(0,600,['Mira','Oren'],'fixed-DC negotiation'),
         'roll':roll('Mira',7,4,12),'predeclaredFailureOffer':{'id':'SP04-escort','amountCp':500,'realEscort':'Fen','expiresAtSeconds':1200},
         'openingCashCp':700,'acceptAlternative':{'consent':True,'paymentId':'SP04-paid','paidCp':500,'cashAfterCp':200,'supervisedVisitGranted':True,'dieDegreeStill':'Failure'},
         'declineAlternative':{'consent':False,'paidCp':0,'cashAfterCp':700,'visitGranted':False},
         'separateOpposedCase':{'id':'SP04-contest','nativeProcedure':'opposed totals','A':{'natural':10,'modifier':4,'total':14},
                               'B':{'natural':12,'modifier':2,'total':14},'priorCustody':'B','afterCustody':'B','taskDegreesOrNaturalShiftsUsed':False}},
        {'fixedTotal':11,'fixedDegree':'Failure','paymentOptional':True,'opposedTieKeepsPriorState':True},
        'The fixed task fails. Mira may separately pay the predeclared 5-gp escort fee or keep the money and refusal. In the independent 14-versus-14 contest, the prior state remains; Core task-degree shifts do not break the tie.')
    check('SP04 failure, actual payment and opposed tie',task(7,4,12)=='Failure' and 700-500==200 and 10+4==12+2)

    add(5,'Insight is bounded by available evidence',
        {'scene':'SP05-hesitation','participants':['Mira','messenger Fen'],
         'frame':frame('understand visible hesitation about timing','observable delay and glance at the dispatch seal','sealed document unavailable',60,['Mira']),
         'stakes':{'Success':'notice that the messenger is unsure about the delivery deadline','Failure':'no reliable inference','cosmicOrHiddenContent':'outside obtainable information'},
         'approach':interval(0,60,['Mira','Fen'],'one actual question and observed response'),'roll':roll('Mira',10,3,13),
         'knownAfter':['observable uncertainty about deadline'],'unknownAfter':['sealed document text','unspoken motive','alignment meaning'],
         'failureAlternative':{'natural':5,'modifier':3,'DC':13,'forcedBelief':'none; uncertainty remains'}},
        {'boundedInferenceObtained':True,'documentRead':False,'alignmentDetermined':False,'failureForcesFalseBelief':False},
        'Success identifies the declared observable uncertainty. It does not read the sealed document, establish an unspoken motive or interpret alignment. Failure leaves uncertainty rather than forcing belief in invented information.')
    check('SP05 declared inference uses normal task',task(10,3,13)=='Success' and task(5,3,13)=='Failure')

    add(6,'Performance earns the stated audience response',
        {'scene':'SP06-performance','performer':'Mira','audience':['five actual consenting listeners'],'licensingOfficerPresent':False,
         'frame':frame('hold the audience for one song','actual song and suitable audible venue','audience cannot issue a civic license',600,['listeners']),
         'performance':interval(0,600,['Mira','listeners'],'one actual performance'),'roll':roll('Mira',9,4,13),
         'promisedSuccess':'listeners remain to hear the complete song and applaud','actualResult':'promised audience response',
         'additionalRequests':[{'request':'automatic performance license','result':'missing issuing authority'},
                               {'request':'another free Persuasion roll','result':'no new unresolved approach defined'}]},
        {'audienceResponseHonored':True,'licenseCreated':False,'freeExtraRoll':False},
        'The successful Performance receives its promised audience response. A license needs the actual issuing authority, and another roll needs a genuinely separate unresolved request.')

    companion=raw_record('{"local-desk":2}','companion-score-v1-evidenced')
    loop=raw_record('{"local-desk":2}','loop-eleven-band-v1-evidenced')
    add(7,'The same raw number can have different source meanings',
        {'companion':{'raw':companion,'binding':{'subject':'A','institution':'actual local desk'},'policy':'companion-score-v1-evidenced','activeScore':2,'band':'Honored'},
         'loopBeforeDecision':{'raw':loop,'binding':{'subject':'B','institution':'actual local desk'},'activeInterpretation':'unapplied until a named policy decision'},
         'explicitLoopDecision':{'id':'SP07-map','policy':'optional RP-A01 Loop mapping','rawValue':2,'activeScore':1,'band':'Liked',
                                 'oldElevenBandLabelAndEarnedRightsPreserved':True,'sourceBytesRewritten':False},
         'unknownProducerBranch':{'rawValue':2,'producer':'unknown','activeScoreStatus':'unresolved','guessFromMagnitude':False}},
        {'companionRaw2Active':2,'explicitlyMappedLoopRaw2Active':1,'bothRawValuesStill2':True},
        'The evidenced companion +2 remains +2/Honored. The older Loop +2 is not automatically imported; an explicit use of the named mapping gives +1/Liked while retaining the old raw meaning and earned rights. Unknown versions stay unresolved.')
    check('SP07 raw versions distinguish interpretations',companion['utf8']==loop['utf8'] and companion['producerVersion']!=loop['producerVersion'])

    medic_raw=raw_record('{"war-veterans":2,"opposing-forces":0,"unknown-local":5,"explicit-zero":0,"malformed":"uncertain"}','standing-v1 with retained extension fields')
    add(8,'Reapplying a background does not reset earned standing',
        {'subject':'Battlefield Medic A','raw':medic_raw,
         'originalInitialization':{'id':'SP08-bg-once','backgroundId':'battlefield-medic','sourceVersion':'current full feature',
                                   'actualServedVeterans':'local veterans','initialVeteranScore':1,'actualOpposingSide':'local opposing veterans','initialOpposingScore':0},
         'earnedHistory':[{'id':'SP08-earned','institution':'local veterans','cause':'actual subsequent aid','delta':1}],
         'duplicateApplication':{'sameInitializationId':'SP08-bg-once','operation':'idempotent no-op','earnedScoreAfter':2,'opposingScoreAfter':0},
         'preservation':{'unknown-local':5,'explicit-zero':0,'malformed':'uncertain','absent-key':{'presence':'absent'}},
         'malformedInterpretation':'unresolved, not Neutral zero'},
        {'earnedVeteranScore':2,'unknownKeysDeleted':0,'zeroEqualsAbsence':False,'backgroundBonusReapplied':False},
        'The once-applied Medic contribution stays in history, followed by the actual earned event. Applying the same background again changes nothing. Unknown keys, recorded zero, absence and the unresolved string remain distinct.')
    check('SP08 earned contribution retained',1+1==2 and json.loads(medic_raw['utf8'])['explicit-zero']==0 and 'absent-key' not in json.loads(medic_raw['utf8']))

    add(9,'Keep the older alignment passage as a source receipt',
        {'sourceReceipt':{'path':player_source['source'],'paragraphIndices':[x['paragraphIndex'] for x in alignment_receipt],
                          'fullOriginalPreservedInDirectorEnvelope':True,'sourceBytesChanged':False},
         'ordinaryProcedureDecision':{'authority':'EX58 SO-05 source direction','automaticAlignmentModifier':0,'automaticAlignmentAdvantage':False},
         'sampleCheck':{'actualCHAAndOnePB':4,'natural':8,'DC':12,'otherActualModifiers':[],'total':12},
         'deferred':{'alignmentMeaningInterpreted':False,'cosmologyReviewed':False,'pendingClassPredicateApproved':False}},
        {'ordinaryAutomaticAlignmentModifier':0,'legacyTextDeleted':False,'deepInterpretationMade':False},
        'SO-05 supplies the new ordinary procedure: no automatic alignment modifier. The complete older passage remains a source receipt. This does not interpret alignment, review cosmology or approve a pending feature.')
    check('SP09 full source passage is present',any(x['paragraphIndex']==7823 for x in alignment_receipt) and any(x['paragraphIndex']==7827 for x in alignment_receipt))

    add(10,'A communicated purpose can be ordinary leverage',
        {'scene':'SP10-civic-plan','participants':['Mira','organizer Hale'],
         'statements':[{'speaker':'Mira','heardBy':'Hale','content':'repair the public bridge'},{'speaker':'Hale','heardBy':'Mira','content':'repair the public bridge'}],
         'frame':frame('agree on a real work appointment','the explicitly shared civic objective','no claim about hidden convictions or alignment',600,['both speakers']),
         'alignmentState':{'Mira':'unknown','Hale':'unknown'},'procedure':{'automaticAlignmentAdvantage':False,'actualSharedPurposeRecorded':True},
         'agreement':{'actualVoluntaryAssent':True,'workersOrMaterialsCreated':False,'timeSeconds':600}},
        {'sharedObjectiveKnown':True,'identicalAlignmentEstablished':False,'legacyAutomaticAdvantageGranted':False},
        'Their heard statements provide ordinary leverage for a real agreement. The shared goal does not identify their alignment or grant the old automatic advantage.')

    serial_turns=[]
    for n in range(10):
        start=n*60
        serial_turns += [{'speaker':['A','B','C'][n%3],'startSeconds':start,'endSeconds':start+30,'language':'speaker’s known tongue'},
                         {'speaker':'interpreter Ione','startSeconds':start+30,'endSeconds':start+60,'language':'audience’s known tongue','interpretsPreviousSegment':True}]
    add(11,'An interpreter uses real serial speaking time',
        {'participants':['A','B','C','interpreter Ione'],'communication':{'IoneActuallyKnowsBothLanguages':True,'allHearAtActualDistance':True},
         'exchange':interval(0,600,['A','B','C','Ione'],'ten-minute exchange including serial interpretation'),
         'speakingSegments':serial_turns,'actorMinutesAreNotElapsedMinutes':True,
         'overflowBranch':{'additionalActualOriginalSpeechSeconds':60,'additionalInterpretationSeconds':60,'newEndSeconds':720},
         'spellComponents':{'IoneVoiceSubstitutesForAnotherCasterV':False,'translationCreatesSpellKnowledge':False}},
        {'baseElapsedSeconds':600,'baseParticipantMinutes':40,'overflowElapsedSeconds':720,'elapsedMultipliedByParticipants':False},
        'Ten paired thirty-second contributions and translations fit exactly into ten minutes. Four participants do not turn that into forty elapsed minutes. Another minute of original speech plus its translation adds two real minutes, and the interpreter cannot supply another caster’s verbal component.')
    check('SP11 serial interpretation actual clock',len(serial_turns)==20 and all(x['endSeconds']==y['startSeconds'] for x,y in zip(serial_turns,serial_turns[1:])) and serial_turns[-1]['endSeconds']==600 and 600+60+60==720)

    add(12,'A combat round cannot contain a blocked minute-long bargain',
        {'scene':'SP12-combat','round':1,'roundInterval':interval(0,6,['Mira','warden'],'actual initiative round'),
         'declaredBargainSeconds':60,'channel':{'voiceBlockedByActualBarrier':True,'alternateSharedChannelAvailable':False},
         'attempt':{'freeSpeechBudgetSeconds':6,'ActionSpentForAdditionalSpeech':False,'effectiveUnderstoodSpeechSeconds':0,'rollMade':False},
         'stateCarry':{'roundsElapsed':1,'effectExpiryAtSeconds':18,'expiryExtendedByNegotiationLabel':False,'opposingThreatStillApplies':True},
         'laterRepair':{'requiresActualChannelAndTime':True,'backdatedAgreement':False}},
        {'bargainCompleted':False,'understoodSpeechSeconds':0,'freeExtraTime':False},
        'The real round advances six seconds. With no usable channel, the intended bargain contributes no understood exchange. Its minute of work, ordinary action costs, opposing threats and existing deadlines do not disappear.')
    check('SP12 minute exceeds one round',60>6)

    add(13,'Help expires at the actual regular-turn boundary',
        {'helper':'Fen','beneficiary':'Mira','round1':{'helperSlot':12,'beneficiarySlot':10,
          'helperAction':{'id':'SP13-help','kind':'Help','qualifyingAssistance':'present and explain the relevant original permit','ActionSpent':True}},
         'deadline':{'event':'Fen next regular turn start','round':2,'slot':12},
         'beneficiaryCheck':{'round':2,'slot':10,'afterDeadline':True,'oldHelpAdvantage':False,
                             'natural':8,'modifier':4,'DC':12,'total':12},
         'extraTurnOrSocialLabelChangesExpiry':False},
        {'oldHelpExpired':True,'ordinaryCheckStillPossible':True,'advantageFromExpiredHelp':False},
        'Mira waits until after Fen’s next regular start. The Help benefit has expired, even though the conversation continues. The check uses its remaining legal modifiers only.')

    add(14,'A new speaker is not new evidence',
        {'scene':'SP14-access','initialApproach':{'interval':interval(0,600,['A','warden'],'actual negotiation'),'roll':roll('A',7,4,12),'result':'refusal'},
         'sameFactsRequests':[{'speaker':x,'newResolution':False,'preservedSceneId':'SP14-access'} for x in ['B','C','D','E']],
         'newEvidence':{'id':'SP14-letter','arrivesAtSeconds':3600,'issuer':'actual authorized owner','authenticityKnownFromActualSealAndRegister':True},
         'newApproach':{'id':'SP14-letter-request','interval':interval(3600,4200,['A','warden'],'consider the genuinely new authorization'),
                        'newDisclosedTerms':'one authorized supervised inspection','earlierRefusalDeleted':False,'oldExpensesRefunded':False}},
        {'speakerRotationExtraRolls':0,'laterMaterialChangePermitsNewApproach':True,'historyRetained':True},
        'Four repeats with unchanged facts create no new resolutions. The real authorization letter later changes the approach; its consideration takes fresh time while the original refusal and costs remain in history.')

    add(15,'Charmed does not make an unauthorized concession possible',
        {'speaker':'Mira','target':'clerk Ione','condition':{'name':'Charmed','charmer':'Mira','sourceEvent':'existing-lawful-effect','expirySeconds':600},
         'request':{'concession':'transfer absent Hale’s property','IoneCanAuthorize':False,'resolutionRoute':'impossible now','rollMade':False},
         'legalAlternative':{'request':'arrange a meeting Ione can schedule','actualUncertainty':True,'interval':interval(0,60,['Mira','Ione'],'actual request'),
                             'eligibleAdvantageDice':[4,10],'modifier':4,'DC':12,'selectedTotal':14,'outcome':'Success'},
         'conditionBoundaries':{'IoneMayAttackOrHarmCharmer':False,'obeysAllRequests':False,'propertyAuthorityCreated':False}},
        {'unauthorizedTransfer':False,'socialAdvantageOnLegalCheckRetained':True,'obedienceGranted':False},
        'There is no roll for the impossible transfer. If Mira makes a different, legally possible request with real uncertainty, the existing Charmed advantage applies normally. The condition creates neither authority nor obedience.')
    check('SP15 legal alternative only',max(4,10)+4==14 and task(10,4,12)=='Success')

    add(16,'Intimidation and Frightened remain separate procedures',
        {'intimidation':{'scene':'SP16-warning','frame':frame('make an intruder leave a privately controlled doorway','credible actual warning','no threat to player boundaries or forced magical state',60,['guard']),
                         'interval':interval(0,60,['Mira','intruder'],'ordinary social warning'),'roll':roll('Mira',10,3,13),
                         'declaredSuccess':'intruder voluntarily leaves the doorway','FrightenedApplied':False},
         'independentConditionCase':{'actor':'Fen','FrightenedSource':'actual existing hostile source','expiresAtSeconds':60,
                                     'visibleUntilSeconds':12,'after12AttackCheckVisibilityPenalty':False,
                                     'after12VoluntaryApproachProhibited':True,'conditionEndsAt12':False,'unrelatedAttackTargetsGrantAutoSuccess':False}},
        {'ordinaryIntimidationCreatesFrightened':False,'visibilityDependentPenaltyEndsWhenHidden':True,'approachRestrictionPersists':True},
        'The social success earns the declared voluntary withdrawal without applying Frightened. In the separate condition case, losing sight of the source removes only the visibility-dependent disadvantage; its approach restriction continues to the actual endpoint.')

    add(17,'An NPC can agree only within its stated authority',
        {'scene':'SP17-bargain','speaker':'Mira','NPC':'tenant Fen','owner':'absent Hale',
         'authorityBeforeRoll':{'FenCan':'personally carry an offer to Hale','FenCannot':'sell or pledge Hale’s workshop'},
         'declaredTask':'persuade Fen to carry the written offer','roll':roll('Mira',10,3,13),
         'acceptedAgreement':{'obligation':'Fen carries the offer','considerationCp':0,'assent':True},
         'property':{'id':'Hale-workshop','ownerBefore':'Hale','ownerAfter':'Hale'},
         'NPCUnsupportedPromise':{'words':'I agree you should have it','transfersOwnership':False}},
        {'promisedWithinAuthorityTaskHonored':True,'absentOwnerPropertyTransferred':False},
        'The check can secure Fen’s own promised act of carrying the offer. Fen’s separate expression of agreement does not transfer Hale’s property or enlarge the stated scope of success.')

    add(18,'A character feature does not replace table agreement',
        {'tableContract':{'id':'session-zero-1','participants':['Player A','Player B','Director'],'boundary':'no player-versus-player social control without both players’ agreement'},
         'request':{'Player A':'invoke a social feature to compel Player B’s character','Player BConsents':False},
         'tableResponse':{'pauseRequested':True,'fictionTimeAdvancedByPause':0,'mechanicalRoll':False,'resourcePenalty':0,'standingPenalty':0},
         'revisedScene':{'offered':'voluntary discussion with each player retaining decisions','requiresActualAssent':True,'assentAssumedFromSilence':False}},
        {'boundaryOverridden':False,'penaltyForUsingTableProcedure':0,'continuationRequiresActualAgreement':True},
        'The table pauses or revises under its existing agreement. A feature supplies no missing player consent, and using the agreed safety procedure causes no character penalty.')

    add(19,'Keep capped standing and its nonbankable overflow',
        {'institution':'local desk','subject':'Mira','policy':'standing-v1','scene':'SP19-scene','openingVersion':5,'openingScore':2,
         'event':{'id':'SP19-major-aid','cause':'actual completed witnessed relief','proposedDelta':2,'sceneCappedDelta':2,
                  'appliedDelta':1,'endingScore':3,'rangeOverflow':1,'knowledgeReceipt':'actual desk witness'},
         'replay':{'id':'SP19-major-aid','newDelta':0,'currentStill':3},
         'futureScene':{'startingScore':3,'oldOverflowApplied':0}},
        {'opening':2,'attemptedDelta':2,'appliedDelta':1,'endingScore':3,'overflow':1,'overflowBanked':False},
        'The +2 event from +2 applies only +1 before the range cap. Both attempted change and overflow survive as history, but replaying the event or entering another scene does not spend the overflow as credit.')
    check('SP19 range cap retains overflow',min(3,2+2)==3 and 3-2==1 and (2+2)-3==1)

    add(20,'A report is a real information event',
        {'rescue':{'id':'SP20-rescue','timeSeconds':0,'rescuer':'Mira','recipient':'Fen','knownBy':['Mira','Fen'],'private':True},
         'personalRelationship':{'subject':'Fen','actualReaction':'gratitude','changedAtSeconds':60},
         'institutionBeforeReport':{'id':'local guild','knowsRescue':False,'standingChange':0},
         'report':{'id':'SP20-report','author':'Fen','travel':interval(3600,7200,['Fen'],'actual trip to the local desk'),
                    'receivedBy':'Ione','receivedAtSeconds':7200,'status':'first-person report, not omniscient certification'},
         'verification':{'interval':interval(7200,10800,['Ione'],'check original infirmary record with available staff'),'corroborated':True},
         'institutionResponse':{'cause':'SP20-rescue','knownAtSeconds':10800,'predeclaredOrdinaryDelta':1,'opening':0,'ending':1},
         'unrelatedInstitutions':{'newKnowledge':False,'standingChanges':0}},
        {'immediateGlobalStanding':False,'actualInformationPathPreserved':True,'oneReceivingInstitutionResponds':True},
        'Fen can react personally to the rescue. The guild does not know until a real report arrives, and its own record distinguishes the report from later corroboration. The same private act does not update every institution.')

    add(21,'Returning halfway through a faction task does not finish it',
        {'institution':'local guild','actionId':'SP21-interview','interview':interval(36000,43200,['interviewer','witness'],'actual two-hour interview'),
         'return':{'id':'SP21-return','timeSeconds':39600,'observedProgressSeconds':3600,'complete':False,'newWorkGranted':0},
         'thresholdRecross':{'timeSeconds':39900,'sameReturnId':'SP21-return','newCheckpoint':False,'clockDelta':0},
         'completion':{'atSeconds':43200,'performedWorkSeconds':7200,'receiptId':'SP21-completed','remoteKnowledgeAutomatic':False}},
        {'interviewCompleteAt11h':False,'completeAt12h':True,'secondThresholdCrossingFreeAction':False},
        'At 11:00 only one of the interview’s two hours is complete. Crossing the threshold again at 11:05 supplies no new checkpoint, work or clock segment. The actual interview completes at 12:00.')
    check('SP21 actual progress and duration',39600-36000==3600 and 43200-36000==7200)

    add(22,'Use one worldwide checkpoint and reject overlapping jobs',
        {'campaignClock':{'epoch':'SP22-epoch','canonicalCheckpointSeconds':86400,'arrivalSeconds':86400,'resetAtArrival':False},
         'checkpoint':{'id':'SP22-day1','reasons':['canonical24h','genuine return'],'processedCount':1,'watchedInstitutions':['guild','archive']},
         'actor':'Fen','requestedAssignments':[interval(57600,86400,['Fen'],'guard a physically separate depot'),
                                                interval(57600,86400,['Fen'],'perform eight-hour archive research')],
         'actualHistory':{'performed':'guard the depot','guardSeconds':28800,'researchSeconds':0,'researchCompleted':False},
         'researchRepair':'schedule actual future qualified research time; the checkpoint supplies no substitute hours',
         'offscreenInstitution':{'keepsSameClock':True,'freeExtraActionAtPartyArrival':False}},
        {'coincidentCheckpointCount':1,'actualGuardHours':8,'actualResearchHours':0,'twentyFourNewHavenHoursRequired':False},
        'The return and canonical 24-hour event form one checkpoint. Fen actually guarded the depot, so the incompatible research has zero hours. Arriving in Haven neither restarts the worldwide cadence nor creates another worker.')
    check('SP22 overlap is real rather than credited twice',max(57600,57600)<min(86400,86400))

    add(23,'One witness event supplies one clock segment',
        {'clock':{'id':'SP23-Claim','length':4,'opening':2,'thresholdConsequence':'schedule actual authorized title hearing'},
         'events':[{'id':'witness-event','causeId':'actual-original-testimony','receivedAtSeconds':600,'qualifying':True,'delta':1,'after':3},
                   {'id':'report-copy-A','causeId':'actual-original-testimony','receivedAtSeconds':900,'delta':0,'after':3},
                   {'id':'report-copy-B','causeId':'actual-original-testimony','receivedAtSeconds':1200,'delta':0,'after':3},
                   {'id':'distinct-document','causeId':'actual-new-signed-title','receivedAtSeconds':3600,'qualifying':True,'delta':1,'after':4}],
         'threshold':{'reachedAtSeconds':3600,'resolvedOnce':True,'actualHearingScheduledForSeconds':86400,'immediatePropertyTransfer':False}},
        {'afterWitness':3,'afterTwoCopies':3,'afterDistinctDocument':4,'thresholdConsequencesScheduled':1},
        'The new witness raises Claim from 2 to 3. Two reports of that testimony are preserved without more segments. A distinct qualifying document can supply the fourth segment, scheduling the stated real procedure once.')
    check('SP23 cause deduplication arithmetic',2+1+0+0==3 and 3+1==4)

    add(24,'A full clock still needs a real route and action',
        {'Depth':{'id':'SP24-Depth','length':6,'current':6,'thresholdEventId':'SP24-depth-threshold',
                   'desiredConsequence':'reach the licensed archive','actualRoute':'blocked physical collapse at the known crossing',
                   'status':'threshold reached; consequence blocked','rivalTeleported':False,'retryingSameThresholdAddsAnotherConsequence':False},
         'Grudge':{'id':'SP24-Grudge','length':4,'opening':3,'actualConversationCause':'one witnessed hostile declaration','delta':1,'current':4,
                    'thresholdEventId':'SP24-grudge-threshold','statedResponse':'send a formal challenge through a real messenger',
                    'responseOrder':{'id':'SP24-response','actor':'messenger Oren','authorizedAtSeconds':600,'work':interval(600,4200,['Oren'],'actual preparation and travel'),
                                     'receivedAtSeconds':4200,'freeImmediateAttack':False,'deliveredCount':1}},
         'separateActualAttack':'would require a real actor, access, initiative and its own normal action; no attack has been created here'},
        {'DepthConsequenceBlocked':True,'GrudgeCreatesFreeAttack':False,'responseHasRealTimeAndActor':True,'duplicateConsequences':0},
        'Depth records its missing physical prerequisite instead of moving the rival through a collapse. Grudge commissions the stated response through Oren’s real hour of work and travel. Neither filled clock supplies a free immediate attack or repeated consequence.')

    # Verify only what these finite source/record calculations can establish.
    check('all24 original IDs have concrete instances',[x['id'] for x in cases]==[x['id'] for x in original] and len(cases)==24)
    for c in cases:
        src=next(x for x in original if x['id']==c['id'])
        check(c['id']+' original proposal and final disposition retained',c['originalScenarioAndDisposition']==src)
        check(c['id']+' actual records and outcome supplied',bool(c['actualSyntheticRecords']) and bool(c['expectedFinalState']))
    raw_fixtures=[companion,loop,medic_raw]
    for i,raw in enumerate(raw_fixtures):
        b=base64.b64decode(raw['base64'])
        check(f'raw fixture {i} complete bytes/hash/pairs preserved',b.decode('utf-8')==raw['utf8'] and hashlib.sha256(b).hexdigest()==raw['sha256'] and [[k,v] for k,v in json.loads(b,object_pairs_hook=list)]==raw['orderedMembers'])
    check('all original source input bytes unchanged',all(digest(G/x['path'])==x for x in sources))
    public={'schemaVersion':'EX58-social-scenarios-v1','status':'24 authored scenario instances; exact review pending',
            'selectionEnabled':False,'completeExpeditionCandidate':False,'cases':cases,'sourceBindings':sources,
            'evidenceScope':'Synthetic record/provenance and finite reference arithmetic only. No NPC/player agency is overridden, no real saves are accessed, and no cosmology is interpreted.',
            'remainingWork':'Assemble the complete player/Director expedition candidate, independently reconstruct its public envelope, and submit the exact package to GPT.'}
    internal={'schemaVersion':'EX58-social-scenarios-director-v1','publicEnvelope':copy.deepcopy(public),
              'completeOriginalScenarios':original,'completeOldAlignmentReceipt':{'source':player_source['source'],'blocks':alignment_receipt},
              'completePlayerSocialSourceBlock':player_source,
              'completeCurrentSocialDirections':part4['completeCurrentDirections'],
              'completeCurrentStandingDirections':part6['completeCurrentDirections'],
              'completeSocialClassInterface':part4['completeClassInterfaceDisposition'],
              'newPromotions':0,'sourceInformationDeleted':0,'runtimeImplemented':False,'realSavesReadOrWritten':0,
              'cosmologyInterpreted':False,'independentFullPublicReconstructionStillRequired':True}
    for p,obj in zip(OUT[:2],[public,internal]):
        p.parent.mkdir(parents=True,exist_ok=True)
        p.write_text(json.dumps(obj,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    player=['# Social scenarios — the original 24 cases','',
            'These cases preserve the original proposals and apply the final EX58 source directions through concrete synthetic records. They are awaiting exact review of the assembled expedition candidate. Each case is independent; alternative branches do not spend the same money twice.','']
    director=['# Social scenarios — complete records','',
              'Every original scenario, its original proposed result, the final source disposition and its concrete candidate record are retained below. These are authored expectations, not runtime or human-playtest results. The full older alignment passage remains in the internal source receipt without interpretation.','']
    for c in cases:
        player += [f"## {c['id']} — {c['title']}",'',c['originalScenarioAndDisposition']['originalScenario']['premise'],'',c['readerExplanation'],'']
        director += [f"## {c['id']} — {c['title']}",'',c['readerExplanation'],'','```json',json.dumps(c,ensure_ascii=False,indent=2),'```','']
    player += ['The [complete scenario records](SOCIAL_SCENARIO_RECORDS.md) retain actual actors, clocks, native rolls, permissions, balances and original wording. These examples add no pending feature or real-world faction fact.']
    OUT[2].write_text('\n'.join(player)+'\n',encoding='utf-8')
    OUT[3].write_text('\n'.join(director)+'\n',encoding='utf-8')
    check('saved whole public projection matches internal',read(OUT[1])['publicEnvelope']==read(OUT[0])==public)
    check('all24 explanations rendered in player reading path',all(c['readerExplanation'] in OUT[2].read_text(encoding='utf-8') for c in cases))
    check('older alignment paragraph intact',read(OUT[1])['completeOldAlignmentReceipt']['blocks']==alignment_receipt)
    receipt={'generatedAtUtc':datetime.now(timezone.utc).isoformat(),'id':'EX58-SOCIAL-INSTANCES-24',
             'status':'All24 original social proposals preserved with final dispositions and concrete candidate records; full assembly and exact GPT review remain.',
             'originalScenariosPreserved':24,'candidateInstances':24,'rawFixtures':3,
             'checks':len(CHECKS),'failures':[x for x in CHECKS if not x['passed']],
             'scope':'Complete original-source retention, typed/raw fixtures, finite task/clock/standing arithmetic and rendering/projection equality only; qualitative outcomes remain authored.',
             'outputs':{p.relative_to(G).as_posix():{k:v for k,v in digest(p).items() if k!='path'} for p in OUT[:4]},
             'builder':digest(Path(__file__)),'inputs':sources,'details':CHECKS,
             'newPromotions':0,'runtimeTestsExecuted':0,'realSavesReadOrWritten':0,'sourceInformationDeleted':0,'cosmologyInterpreted':False}
    OUT[4].write_text(json.dumps(receipt,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print(json.dumps({k:v for k,v in receipt.items() if k not in ('inputs','details')},indent=2))

if __name__=='__main__':main()
