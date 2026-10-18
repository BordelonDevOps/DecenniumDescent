"""Explicit conditional caster/geometry fixtures, not authored character records."""
from copy import deepcopy
from di7_area_geometry import AreaGeometryTransactions

def volume(cell,center): return {'cellId':cell,'min':[x-2.5 for x in center],'max':[x+2.5 for x in center]}
def make(sources,sid='mass-revelation',provider='Wizard',*,center=None,origin=None,direction=None,points=None):
    center=[0,0,0] if center is None else center; origin=[0,0,0] if origin is None else origin
    direction=[1,0,0] if direction is None else direction; points=[[10,0,0]] if points is None else points
    level=13 if provider in {'Wizard','Cleric'} else 20; actors={}
    for aid,cls,lv,pos in [('owner',provider,level,0),('counter','Wizard',13,10)]:
        actors[aid]={'provider':cls,'classLevel':lv,'totalLevel':lv,'abilityScore':18,
            'attainmentPremise':'Conditional attained ordinary caster/body/rest slice; no full character progression claimed.',
            'heroPath':'Soothsayer' if cls=='Shaman' else 'ordinary-provider-retained','specialization':'Evocation',
            'providerRetained':True,'bookPresent':True,'studyUninterrupted':True,'positionFeet':pos,'position3d':[pos,0,0],
            'knownFactions':[],'body':{'conscious':True,'canAct':True,'ordinarySpellProhibited':False,'silenced':False,'canSpeak':True,'reactionLegal':True,
                'hands':{'left':{'usable':True,'holding':None},'right':{'usable':True,'holding':'focus/'+aid}},
                'focus':{'id':'focus/'+aid,'owner':aid,'qualifiedClasses':[cls],'accessible':True}}}
    entities={aid:{'kind':'creature','positionFeet':a['positionFeet'],'willing':True,'alliedTo':{},'relatedQuestions':[]} for aid,a in actors.items()}
    entities['point']={'kind':'point','positionFeet':center[0],'position3d':deepcopy(center)}
    cells={'origin':{'center':[0,0,0]},'counter-cell':{'center':[10,0,0]}}; portions={}
    origin_key=','.join(str(x) for x in (origin if sid=='mass-revelation' else center))
    for i,p in enumerate(points):
        cell='test-cell-'+str(i); cells[cell]={'center':p}
        portions['portion-'+str(i)]={'cellId':cell,'actuallyOccupiedNow':True,'authorityEvent':'conditional-actual-portion/'+str(i),
            'actualLocalFootprint':{'part':'local-portion-'+str(i),'center':p},'clippingByOrigin':{origin_key:{
                'authorityEvent':'conditional-current-open-source-line/'+str(i),'lineOfEffect':True,'totalCover':False,'blockedCorner':False}}}
    geometry={'kind':'conditional-actual-occupied-volumes-and-source-clipping','cells':cells,'portions':portions,
        'bodies':{a:{'authorityEvent':'conditional-actual-body/'+a,'sourceVersion':'world-v1','actualOccupiedVolumes':[volume('origin' if a=='owner' else 'counter-cell',v['position3d'])]} for a,v in actors.items()},
        'pointRelations':{'owner>point':{'authorityEvent':'conditional-perception-and-open-line','point':deepcopy(center),'perceived':True,'lineOfEffect':True,'blockedCorner':False}}}
    world={'entities':entities,'relations':{a+'>'+t:{'sourceFact':'conditional-straight-line-counter-range','perceived':True,'visible':True,'lineOfEffect':True} for a in actors for t in actors},
        'geometry':geometry,'alignmentActors':{a:{'underlying':{'order':'Lawful','ethics':'Good'},'immunities':[],'permanentIdentity':{'id':a},'acquisitionSnapshots':[],'usedAllowances':{}} for a in actors},
        'encounter':{'id':'conditional-real-encounter','isRealEncounter':True},'identificationFacts':{},'triggerEvents':{}}
    m=AreaGeometryTransactions(sources,actors,world)
    m.learn('owner',sid,level,'actual-owner-learning'); m.learn('counter','counterspell',5,'actual-counter-learning')
    for aid,a in m.actors.items():
        if a['provider']=='Wizard': m.prepare_wizard(aid,list(a['learned']),aid+'/study',{'actor':aid,'completedAt':0,'sourceEvent':'conditional-completed-rest'})
    m.begin_turn('owner','turn-1')
    request={'origin':origin,'originCell':'origin','direction':direction} if sid=='mass-revelation' else {'target':'point'}
    return m,request
