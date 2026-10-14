"""Paid Supreme Sight over explicit actual historical facts and native scopes.

Director-established facts, temporal relations, native protection grants and
local footprints are conditional upstream evidence, not invented timestamps or
authenticated campaign records. No software event log is required by this input.
"""
from copy import deepcopy
from fractions import Fraction
import json
import math
from di7_area_geometry import AreaGeometryTransactions


NOTICE='This reading affirms only the facts stated; it certifies neither complete coverage nor the absence of unreported history.'
FIELDS={'existence','identity','category','school','rank','local-presence','state','transition','persistence'}


def numeric(value):
    if type(value) not in {int,float} or not math.isfinite(value): raise ValueError('Finite actual historical time required')
    return Fraction(str(value))


def bounds(time):
    kind=time['kind']
    if kind=='point': return (numeric(time['at']),numeric(time['at']),True,True)
    if kind=='relative-order': return None
    if kind not in {'occurrence-window','continuous-interval','native-interval'}: raise ValueError('Explicit temporal precision kind required')
    lo,hi=numeric(time['from']),numeric(time['to'])
    if lo>hi or type(time['includeFrom']) is not bool or type(time['includeTo']) is not bool: raise ValueError('Actual ordered native endpoints required')
    if lo==hi and not(time['includeFrom'] and time['includeTo']): raise ValueError('Empty time support cannot establish a fact')
    return lo,hi,time['includeFrom'],time['includeTo']


def intersects(a,b):
    lo=max(a[0],b[0]); hi=min(a[1],b[1])
    if lo<hi: return True
    if lo>hi: return False
    def contains(r,x): return (x>r[0] or x==r[0] and r[2]) and (x<r[1] or x==r[1] and r[3])
    return contains(a,lo) and contains(b,lo)


def subset(a,b):
    return (a[0]>b[0] or a[0]==b[0] and (b[2] or not a[2])) and (a[1]<b[1] or a[1]==b[1] and (b[3] or not a[3]))


def fully_covered(support,intervals):
    points=sorted({support[0],support[1],*[x for r in intervals for x in r[:2] if support[0]<=x<=support[1]]})
    probes=[x for x in points if intersects(support,(x,x,True,True))]
    probes.extend((a+b)/2 for a,b in zip(points,points[1:]) if a<b)
    return all(any(intersects((x,x,True,True),r) for r in intervals) for x in probes)


class HistoricalInformation:
    def __init__(self,history):
        self.data=deepcopy(history); self.dispositions=[]
        if self.data.get('kind')!='conditional-Director-established-spatial-history': raise ValueError('Explicit actual historical premise required')
        for oid,occurrence in self.data['occurrences'].items():
            if occurrence['id']!=oid or not occurrence.get('authorityEvent') or not occurrence.get('authorityVersion'):
                raise ValueError('Actual occurrence identity/version/authority required')
            for fid in occurrence['facts']:
                f=self.data['facts'][fid]
                if f['id']!=fid or f['occurrence']!=oid or not f.get('authorityEvent') or not f.get('authorityVersion') or f['field'] not in FIELDS:
                    raise ValueError('Actual source-qualified permitted fact required')
                bounds(f['time'])
        for p in self.data['protections']:
            source=p['nativeScopePremise']
            if source.get('kind')!='conditional-actual-native-protection-scope' or not source.get('sourceVersion') or not source.get('sourceGrantEvent') or not source.get('completeScopeText'):
                raise ValueError('Actual native protection grant/scope premise required')
            if p['mode'] not in {'block','mask'}: raise ValueError('Native information-defense behavior required')
            if p['mode']=='mask' and (not source.get('explicitlyAuthorizesAlteredResult') or p['protectsExistence']):
                raise ValueError('This finite mask adapter needs an explicitly authorized field mask, not an invented existence replacement')
            if p['historicalTimeScope'] is not None: bounds(p['historicalTimeScope'])

    def _temporal_relation(self,p,f):
        protected=p['historicalTimeScope']; support=bounds(f['time'])
        if protected is None: computed='applies'
        elif support is None: computed='unresolved'
        else:
            native=bounds(protected)
            computed='outside' if not intersects(support,native) else 'applies' if subset(support,native) else 'partial' if f['time']['kind']=='continuous-interval' else 'unresolved'
        supplied=f.get('nativeTemporalRelations',{}).get(p['id'])
        if supplied:
            if not supplied.get('authorityEvent') or supplied['factVersion']!=f['authorityVersion'] or supplied['protectionVersion']!=p['nativeScopePremise']['sourceVersion']:
                raise ValueError('Actual temporal relation must bind this fact and native scope version')
            relation=supplied['relation']
            if relation not in {'applies','outside'} or computed!='unresolved' and relation!=computed:
                raise ValueError('Additional temporal relation contradicts established history')
            return relation
        return computed

    def _matching(self,p,f,now):
        return (p['queryActiveFrom']<=now<p['queryActiveUntil'] and 'Divination' in p['querySchools']
            and p['minimumQueryRank']<=7<=p['maximumQueryRank'] and bool(set(p['subjects']).intersection(f['subjects']))
            and f['domain'] in p['factDomains'] and f['evidenceChannel'] in p['evidenceChannels']
            and (p['protectsExistence'] or f['field'] in p['fields']))

    def project(self,fid,*,now,readable):
        f=self.data['facts'][fid]
        if f['establishedAtQueryTime']>now: return None
        support=bounds(f['time'])
        if support and support[0]>numeric(now): return None
        if support and support[1]>numeric(now):
            raise ValueError('Supply actual established history through query time; this query cannot certify future persistence')
        local=[readable[p] for p in f['historicalPortions'] if p in readable]
        if not local: return None
        value=deepcopy(f['value']); partial=False; applicable_masks=[]; blocked_intervals=[]
        for p in self.data['protections']:
            if not self._matching(p,f,now): continue
            relation=self._temporal_relation(p,f)
            if relation=='outside': continue
            self.dispositions.append({'factId':fid,'protectionId':p['id'],'relation':relation,'at':now})
            if p['mode']=='block':
                if relation in {'applies','unresolved'}: return None
                # Known continuous support is not an uncertain single event.
                # Readable positive properties can survive outside the covered
                # portion, but its full persistence interval cannot be certified.
                if f['field']=='persistence': return None
                partial=True; blocked_intervals.append(bounds(p['historicalTimeScope']))
            elif relation=='applies': applicable_masks.append(p)
            elif p['maskedFields'][f['field']]!=value:
                # A different masked value in only some admissible/actual
                # portions cannot be rendered as a single unconditional value.
                return None
        if blocked_intervals and fully_covered(support,blocked_intervals): return None
        if len(applicable_masks)>1: raise ValueError('Overlapping native mask arbitration not supplied')
        if applicable_masks: value=deepcopy(applicable_masks[0]['maskedFields'][f['field']])
        if f['field']=='existence':
            return {'existenceReadable':value is True,'localFootprint':[p['localFootprint'] for p in local]}
        # Only genuine historical assertions/intervals supplied by the Director
        # can appear. Filtering never manufactures observations at its endpoints.
        result={'field':f['field'],'value':value,'localFootprint':[p['localFootprint'] for p in local]}
        if f['field'] in {'transition','persistence','state','local-presence'} and not partial:
            result['time']=deepcopy(f['publicTimePrecision'])
        elif f['field'] in {'identity','category','school','rank'} and f['time']['kind'] in {'point','occurrence-window','relative-order'}:
            result['time']=deepcopy(f['publicTimePrecision'])
        return result

    def read(self,*,now,readable):
        rows=[]
        for occurrence in self.data['occurrences'].values():
            if not occurrence['actuallyMagical']: continue
            facts=[]; existence=False
            for fid in occurrence['facts']:
                result=self.project(fid,now=now,readable=readable)
                if result is None: continue
                if 'existenceReadable' in result: existence|=result['existenceReadable']
                else: facts.append(result); existence=True
            if not existence: continue
            # Sort only visible facts; internal IDs, sequence gaps and hidden
            # records never become public ordering or placeholder metadata.
            facts.sort(key=lambda x:json.dumps(x,sort_keys=True,ensure_ascii=False))
            rows.append({'reference':'effect-'+str(len(rows)+1),'assertions':facts})
        return {'effects':rows,'notice':NOTICE}


class SupremeTransactions(AreaGeometryTransactions):
    def __init__(self,*args,history,**kwargs):
        super().__init__(*args,**kwargs)
        self.history=HistoricalInformation(history); self.readings={}; self.communications=[]

    def snapshot(self):
        return {**super().snapshot(),'privateHistoricalWorld':deepcopy(self.history.data),'privateReadabilityDispositions':deepcopy(self.history.dispositions),
            'readings':deepcopy(self.readings),'communications':deepcopy(self.communications)}

    def resolve_supreme(self,cast_id):
        cast=self.casts[cast_id]
        if cast['spellId']!='resonance-sight-supreme': raise ValueError('Actual paid Supreme Sight required')
        gate=self.resolve_area_geometry(cast_id)
        if gate is None: return None
        readable={p['portionId']:p for p in gate['readableSpatialPortions']}
        result=self.history.read(now=self.now,readable=readable)
        self.readings[cast_id]={'caster':cast['actor'],'at':self.now,'result':result}
        cast.update(status='resolved',resolvedAt=self.now,castingCompletedAt=self.now,informationPayloadExecuted=True,privateRecipient=cast['actor'])
        return deepcopy(result)

    def establish_temporal_relation(self,fid,protection_id,relation,*,event_id,authority_event):
        f=self.history.data['facts'][fid]; p=next(x for x in self.history.data['protections'] if x['id']==protection_id)
        if not event_id or not authority_event or any(x.get('event')==event_id for x in self.events): raise ValueError('Unique actual additional historical evidence required')
        if protection_id in f.get('nativeTemporalRelations',{}): raise ValueError('Do not overwrite a prior temporal relation')
        if relation not in {'applies','outside'} or self.history._temporal_relation(p,f)!='unresolved': raise ValueError('Actual unresolved relation required')
        before=deepcopy(f)
        f.setdefault('nativeTemporalRelations',{})[protection_id]={'relation':relation,'authorityEvent':authority_event,
            'factVersion':f['authorityVersion'],'protectionVersion':p['nativeScopePremise']['sourceVersion']}
        self.events.append({'event':event_id,'kind':'conditional-new-established-temporal-relation','at':self.now,'factId':fid,
            'authorityEvent':authority_event,'before':before,'relation':relation,'exactDateCreated':False})

    def communicate(self,cast_id,listener,channel_id):
        reading=self.readings[cast_id]; channel=self.world['informationChannels'].get(channel_id)
        if not channel or not channel['authorityEvent'] or channel['from']!=reading['caster'] or channel['to']!=listener or channel['at']!=self.now or not channel['received'] or not channel['understood']:
            raise ValueError('Actual source-qualified delivered and understood channel required')
        if any(x['channelId']==channel_id for x in self.communications): raise ValueError('Actual communication event cannot be replayed')
        delivered=channel['deliveredAssertions']; available=[a for e in reading['result']['effects'] for a in e['assertions']]
        if not delivered or any(a not in available for a in delivered): raise ValueError('Only actually delivered literal assertions implemented')
        result={'channelId':channel_id,'listener':listener,'at':self.now,'assertions':deepcopy(delivered),'notice':NOTICE}
        self.communications.append(result); return deepcopy(result)
