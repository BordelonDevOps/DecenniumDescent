"""Scoped DI7 geometry over paid casts; information payloads remain separate.

Exact rational shape predicates execute the two source definitions. Actual
occupied volumes and readable clipped portions are conditional world premises;
this is not a general movement, body-shape, perception or ray-tracing engine.
"""
from copy import deepcopy
from fractions import Fraction
import math
from di7_fate_transactions import FateTransactions


def vector(value):
    if not isinstance(value, list) or len(value) != 3:
        raise ValueError('Three actual coordinates required')
    if any(type(x) not in {int, float} or not math.isfinite(x) for x in value):
        raise ValueError('Finite numeric coordinates required')
    return [Fraction(str(x)) for x in value]


def dot(a,b): return sum(x*y for x,y in zip(a,b))


def grid_distance(a,b): return max(abs(x-y) for x,y in zip(vector(a),vector(b)))


def mass_contains(origin,direction,center):
    o=vector(origin); d=vector(direction); p=vector(center); dsq=dot(d,d)
    if not dsq: raise ValueError('Nonzero facing required')
    v=[x-y for x,y in zip(p,o)]; q=dot(v,d)
    # a=q/sqrt(dsq), perpendicular squared=dot(v,v)-q*q/dsq.
    # Cross multiplication avoids square-root rounding at either boundary.
    return q>0 and q*q<=3600*dsq and 4*(dot(v,v)*dsq-q*q)<=q*q


class AreaGeometryTransactions(FateTransactions):
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        spatial=self.world['geometry']
        if spatial.get('kind')!='conditional-actual-occupied-volumes-and-source-clipping':
            raise ValueError('Explicit actual geometry premises required')
        self.geometry_events=[]

    def snapshot(self):
        return {**super().snapshot(),'geometryEvents':deepcopy(self.geometry_events)}

    def _origin_legal(self,actor,origin,direction,source_cell=None):
        o=vector(origin); d=vector(direction)
        if not dot(d,d): return False
        body=self.world['geometry']['bodies'][actor]
        if not body.get('authorityEvent') or not body.get('sourceVersion'):
            raise ValueError('Actual occupied-body provenance required')
        for volume in body['actualOccupiedVolumes']:
            if source_cell is not None and volume['cellId']!=source_cell: continue
            lo=vector(volume['min']); hi=vector(volume['max'])
            if any(a>=b for a,b in zip(lo,hi)): raise ValueError('Nonempty actual volumes required')
            if all(a<x<b for a,x,b in zip(lo,o,hi)): return True
            if all(a<=x<=b for a,x,b in zip(lo,o,hi)):
                # Conditional fixtures use actual filled boxes. An exposed face
                # is forward only when its outward normal has positive dot F.
                if any((x==b and f>0) or (x==a and f<0) for a,x,b,f in zip(lo,o,hi,d)): return True
        return False

    def _point_legal(self,actor,point_id,center):
        vector(center); position=self.actors[actor]['position3d']; vector(position)
        relation=self.world['geometry']['pointRelations'].get(actor+'>'+point_id)
        return bool(relation and relation.get('authorityEvent') and relation['point']==center
            and relation['perceived'] and relation['lineOfEffect'] and not relation['blockedCorner']
            and grid_distance(position,center)<=120)

    def _chosen_geometry(self,actor,sid,request):
        if sid=='mass-revelation':
            origin=request.get('origin'); direction=request.get('direction'); cell=request.get('originCell')
            vector(origin); d=vector(direction)
            if not dot(d,d) or cell not in self.world['geometry']['cells'] or not self._origin_legal(actor,origin,direction,cell):
                raise ValueError('Actual legal occupied source origin/cell and nonzero direction required')
            length=math.sqrt(float(dot(d,d)))
            return {'kind':'mass-euclidean-axial-circular-cone','origin':deepcopy(origin),'direction':deepcopy(direction),
                'unitDirectionDisplayOnly':[float(x)/length for x in d], 'originCell':cell,'axialExtent':60,
                'predicate':'0<a<=60 and4*perpendicularSquared<=aSquared; no radial cap'}
        if sid=='resonance-sight-supreme':
            point_id=request.get('target'); target=self.world['entities'].get(point_id)
            if not target or target['kind']!='point': raise ValueError('Actual nominated point required')
            center=target.get('position3d'); vector(center)
            if not self._point_legal(actor,point_id,center): raise ValueError('Actual perceived point within scoped grid120 and line of effect required')
            return {'kind':'supreme-three-axis-max-grid-sphere','center':deepcopy(center),'pointId':point_id,'radius':20,
                'predicate':'max(abs(deltaX),abs(deltaY),abs(deltaZ))<=20'}
        return None

    def _target(self,actor,sid,request,op):
        if sid in {'mass-revelation','resonance-sight-supreme'}:
            self._chosen_geometry(actor,sid,request); return
        return super()._target(actor,sid,request,op)

    def declare(self,actor,sid,cast_id,request):
        chosen=self._chosen_geometry(actor,sid,request)
        super().declare(actor,sid,cast_id,request)
        if chosen:
            self.casts[cast_id]['committedGeometry']=chosen
            self.casts[cast_id]['geometryCommitPosition']=deepcopy(self.actors[actor]['position3d'])
            self.casts[cast_id]['geometryCommitBody']=deepcopy(self.world['geometry']['bodies'][actor])
        return deepcopy(self.casts[cast_id])

    def move_actor(self,actor,position,volumes,*,event_id,authority_event):
        if not event_id or not authority_event or any(x['id']==event_id for x in self.geometry_events):
            raise ValueError('Unique actual legally authorized displacement event required')
        vector(position)
        for v in volumes:
            if v['cellId'] not in self.world['geometry']['cells']: raise ValueError('Actual registered occupied cell required')
            if any(a>=b for a,b in zip(vector(v['min']),vector(v['max']))): raise ValueError('Actual nonempty occupied volume required')
        if not volumes: raise ValueError('This conditional fixture supplies a persisting body')
        before={'position':deepcopy(self.actors[actor]['position3d']),'body':deepcopy(self.world['geometry']['bodies'][actor])}
        self.actors[actor]['position3d']=deepcopy(position)
        # Other existing Counterspell fixtures remain explicitly straight-line.
        self.actors[actor]['positionFeet']=position[0]; self.world['entities'][actor]['positionFeet']=position[0]
        self.world['geometry']['bodies'][actor]={'actualOccupiedVolumes':deepcopy(volumes),'sourceVersion':event_id,'authorityEvent':authority_event}
        self.geometry_events.append({'id':event_id,'at':self.now,'actor':actor,'authorityEvent':authority_event,
            'kind':'conditional-legal-displacement-not-granted-by-spell','before':before,'position':deepcopy(position),'volumes':deepcopy(volumes)})

    def resolve_area_geometry(self,cast_id):
        cast=self.casts[cast_id]
        if cast['spellId'] not in {'mass-revelation','resonance-sight-supreme'}: raise ValueError('Actual area spell required')
        receipt=self.take_payload_resolution(cast_id)
        if receipt['status']!='ready-for-payload': return None
        actor=cast['actor']; chosen=cast['committedGeometry']
        if cast['spellId']=='mass-revelation':
            legal=self._origin_legal(actor,chosen['origin'],chosen['direction'])
        else: legal=self._point_legal(actor,chosen['pointId'],chosen['center'])
        cast['geometryResolutionState']={'at':self.now,'casterPosition':deepcopy(self.actors[actor]['position3d']),
            'casterBody':deepcopy(self.world['geometry']['bodies'][actor]),'committedGeometryStillLegal':legal}
        if not legal:
            cast.update(status='failed-area-geometry-no-refund',publicResult='No information.',resolvedAt=self.now)
            return None
        readable=[]
        origin=chosen.get('origin',chosen.get('center'))
        for pid,portion in self.world['geometry']['portions'].items():
            if not portion.get('authorityEvent'): raise ValueError('Actual spatial portion provenance required')
            cell=portion['cellId']; center=self.world['geometry']['cells'][cell]['center']
            if cast['spellId']=='mass-revelation':
                included=portion['actuallyOccupiedNow'] and cell!=chosen['originCell'] and mass_contains(origin,chosen['direction'],center)
            else: included=grid_distance(origin,center)<=20
            if not included: continue
            clipping=portion['clippingByOrigin'].get(','.join(str(x) for x in origin))
            if not clipping or not clipping.get('authorityEvent'):
                raise ValueError('Current source-qualified portion clipping premise required')
            if clipping['lineOfEffect'] and not clipping['totalCover'] and not clipping['blockedCorner']:
                # Portions already describe actual clipped sub-footprints, never
                # the enclosing whole object/effect or a bounding-box fill.
                readable.append({'portionId':pid,'cellId':cell,'center':deepcopy(center),
                    'localFootprint':deepcopy(portion['actualLocalFootprint']),'clipping':deepcopy(clipping)})
        gate={'castId':cast_id,'resolvedAt':self.now,'committedGeometry':deepcopy(chosen),'readableSpatialPortions':readable,
            'informationPayloadExecuted':False,'publicInformationDelivered':False}
        cast.update(status='geometry-resolved-payload-pending',geometryGate=gate)
        return deepcopy(gate)
