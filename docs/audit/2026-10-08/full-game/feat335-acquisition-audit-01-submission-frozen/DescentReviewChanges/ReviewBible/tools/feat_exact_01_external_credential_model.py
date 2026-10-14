"""Finite ACQ04-EC1 record adapter for authored acceptance examples.

The caller supplies an independently admitted world-root binding. A submitted
record cannot admit its own world, authority, source or credential. In this
authoring exercise every admitted world is an explicitly conditional fixture;
no campaign-positive record is supplied or authenticated.
"""
from copy import deepcopy
from hashlib import sha256
import json
from pathlib import Path

MISSING = object()


class EvidenceFailure(Exception):
    def __init__(self, reason, outcome='UNESTABLISHED', field_state=None):
        self.reason = reason; self.outcome = outcome; self.field_state = field_state


def require(condition, reason, outcome='UNESTABLISHED'):
    if not condition:
        raise EvidenceFailure(reason, outcome)


def ordered(value):
    require(isinstance(value, dict) and set(value) == {'elapsed', 'sequence'}, 'missing authoritative time/sequence')
    require(type(value['elapsed']) is int and value['elapsed'] >= 0 and type(value['sequence']) is int and value['sequence'] >= 0,
            'invalid authoritative time/sequence')
    return value['elapsed'], value['sequence']


class ExternalCredentialEvidence:
    BRANCHES = {'frenzied_rage': {'class_rage'}, 'divine_favor': {'worship'},
                'elemental_body': {'exposure'}, 'dragon_blood': {'Dragonborn', 'Sorcerer'}}

    def __init__(self, root, admitted_worlds, contract_refs, current_rage_rejections):
        self.root = Path(root).resolve()
        self.admitted_worlds = deepcopy(admitted_worlds)
        self.contract_refs = deepcopy(contract_refs)
        self.current_rage_rejections = deepcopy(current_rage_rejections)
        self.cache = {}

    def resolve(self, ref):
        if ref is MISSING:
            raise EvidenceFailure('reference absent', field_state='absent')
        if ref is None:
            raise EvidenceFailure('reference explicitly null', field_state='null')
        require(isinstance(ref, dict) and {'path', 'sha256', 'pointer'} <= set(ref), 'incomplete bound reference')
        require(all(isinstance(ref[k], str) for k in ['path', 'sha256', 'pointer']), 'reference field type mismatch')
        path = (self.root / ref['path']).resolve()
        require(path.is_relative_to(self.root) and not Path(ref['path']).is_absolute(), 'reference escapes source root')
        require(path.is_file(), 'unresolved reference path')
        if ref['path'] not in self.cache:
            data = path.read_bytes()
            try:
                document = json.loads(data)
            except (ValueError, UnicodeError):
                raise EvidenceFailure('reference does not resolve a JSON record')
            self.cache[ref['path']] = sha256(data).hexdigest(), document
        digest, document = self.cache[ref['path']]
        require(digest == ref['sha256'], 'reference hash/version mismatch')
        pointer = ref['pointer']; require(pointer == '' or pointer.startswith('/'), 'invalid exact record pointer')
        value = document
        try:
            for token in pointer[1:].split('/') if pointer else []:
                token = token.replace('~1', '/').replace('~0', '~')
                value = value[int(token)] if isinstance(value, list) else value[token]
        except (KeyError, IndexError, TypeError, ValueError):
            raise EvidenceFailure('unresolved exact record pointer')
        if 'version' in ref:
            require(isinstance(value, dict) and value.get('version') == ref['version'], 'reference record version mismatch')
        return deepcopy(value)

    def evaluate(self, evidence):
        try:
            return self._evaluate(evidence)
        except EvidenceFailure as error:
            return {'outcome': error.outcome, 'reason': error.reason,
                    'referenceFieldState': error.field_state, 'campaignAcquisitionEstablished': False}

    def _evaluate(self, evidence):
        require(isinstance(evidence, dict), 'evidence must be an explicit record')
        mode = evidence.get('evidenceMode')
        require(mode in {'conditional_fixture', 'campaign_record'}, 'explicit evidence domain required')
        acquisition = self.resolve(evidence.get('acquisitionRef', MISSING))
        require(isinstance(acquisition, dict) and acquisition.get('recordType') == 'acquisition_snapshot', 'wrong acquisition record')
        world_ref = acquisition.get('worldRef', MISSING)
        admitted = next((x for x in self.admitted_worlds if x['worldRef'] == world_ref), None)
        require(admitted is not None, 'world root not independently admitted')
        require(admitted['evidenceMode'] == mode, 'fixture/campaign admission-domain mismatch')
        world = self.resolve(world_ref)
        require(isinstance(world, dict) and world.get('recordType') == 'world' and world.get('evidenceMode') == mode, 'world record/domain mismatch')
        world_id = evidence.get('worldId'); actor_id = evidence.get('characterId')
        require(world_id == world.get('worldId') and isinstance(world_id, str) and bool(world_id), 'world identity mismatch')
        require(acquisition.get('worldId') == world_id and acquisition.get('characterId') == actor_id and acquisition.get('evidenceMode') == mode,
                'acquisition actor/world/domain mismatch')
        require(acquisition.get('characterRef') in world.get('characterRefs', []), 'character not admitted in world')
        character = self.resolve(acquisition['characterRef'])
        require(isinstance(character, dict) and character.get('characterId') == actor_id and character.get('worldId') == world_id and character.get('evidenceMode') == mode,
                'character identity/domain mismatch')
        require(acquisition.get('permanentScores') == character.get('permanentScores') and acquisition.get('classLevels') == character.get('classLevels'),
                'acquisition statistics differ from bound character snapshot')
        acquired_at = ordered(acquisition.get('at'))
        predicate = evidence.get('predicate', {})
        require(isinstance(predicate, dict), 'missing exact predicate record')
        sid = predicate.get('featId'); branch = predicate.get('branch')
        require(sid in self.BRANCHES and branch in self.BRANCHES[sid], 'unsupported exact feat/branch')
        require(acquisition.get('featId') == sid, 'wrong feat acquisition snapshot')
        contract_ref = predicate.get('contractRef', MISSING)
        contract = self.resolve(contract_ref)
        require(contract_ref == self.contract_refs[sid] and isinstance(contract, dict) and contract.get('id') == sid, 'wrong controlling contract/version')
        authority_ref = evidence.get('authorityRef', MISSING)
        authority = self.resolve(authority_ref)
        require(authority_ref in world.get('authorityRefs', []), 'authority not admitted by world')
        require(isinstance(authority, dict) and authority.get('worldId') == world_id and authority.get('evidenceMode') == mode, 'authority world/domain mismatch')
        require(actor_id in authority.get('subjects', []) and sid + '/' + branch in authority.get('predicateScopes', []), 'authority lacks actor/predicate scope')
        require(ordered(authority.get('effectiveFrom')) <= acquired_at, 'authority not effective at acquisition')
        if authority.get('effectiveUntil') is not None:
            require(acquired_at < ordered(authority['effectiveUntil']), 'authority expired at acquisition')

        def source(ref):
            value = self.resolve(ref)
            require(ref in world.get('sourceRefs', []), 'source not admitted in this world')
            require(isinstance(value, dict), 'source pointer does not select a source record')
            if isinstance(value, dict) and 'evidenceMode' in value:
                require(value['evidenceMode'] == mode, 'source fixture/campaign domain mismatch')
            return value

        def credential(ref):
            value = self.resolve(ref)
            require(ref in world.get('credentialRefs', []), 'credential not admitted in this world')
            require(isinstance(value, dict) and value.get('characterId') == actor_id and value.get('worldId') == world_id,
                    'supporting credential actor/world mismatch')
            require(value.get('evidenceMode') == mode, 'supporting credential fixture/campaign mismatch')
            require(value.get('authorityRef') == authority_ref, 'supporting credential authority mismatch')
            established = ordered(value.get('at'))
            require(established < acquired_at, 'credential not established before acquisition')
            require(ordered(authority['effectiveFrom']) <= established, 'credential predates scoped authority')
            if authority.get('effectiveUntil') is not None:
                require(established < ordered(authority['effectiveUntil']), 'credential postdates scoped authority')
            return value

        refs = evidence.get('credentialRefs', MISSING)
        require(isinstance(refs, list) and bool(refs), 'missing bound supporting credentials')
        records = [credential(ref) for ref in refs]

        def one(kind):
            matches = [x for x in records if x.get('recordType') == kind]
            require(len(matches) == 1, 'missing or ambiguous ' + kind)
            return matches[0]

        def actual_class(ref, expected_name):
            assignment = credential(ref)
            require(assignment.get('recordType') == 'class_assignment', 'no bound class assignment')
            class_source = source(assignment.get('sourceRef', MISSING))
            literal = class_source.get('name', class_source.get('class'))
            require(literal == expected_name, 'actual class is not literal ' + expected_name, 'CONTRADICTED')
            require(assignment.get('className') == expected_name and type(assignment.get('classLevel')) is int and assignment['classLevel'] >= 1,
                    'missing actual class level assignment')
            require(character['classLevels'].get(expected_name) == assignment['classLevel'], 'class assignment differs from bound character')
            return assignment, class_source

        if sid == 'frenzied_rage':
            grant = one('class_feature_assignment'); feature_ref = grant.get('featureRef', MISSING)
            feature = source(feature_ref)
            require(feature_ref not in self.current_rage_rejections, 'reviewed current card grants no rage state', 'CONTRADICTED')
            require(feature.get('recordType') == 'class_feature' and feature.get('grantedState') == 'rage', 'source does not expressly grant a class rage state', 'CONTRADICTED')
            assignment, class_source = actual_class(grant.get('classAssignmentRef', MISSING), feature.get('className'))
            require(feature.get('id') in class_source.get('featureIds', []) and type(feature.get('minimumClassLevel')) is int and assignment['classLevel'] >= feature['minimumClassLevel'],
                    'feature absent from class or required class level not attained')
            require(ordered(assignment['at']) <= ordered(grant['at']), 'feature predates its class assignment')
            require(grant.get('path') == feature.get('requiredPath'), 'required feature path not acquired')
            if feature.get('acquisition') == 'automatic':
                require(grant.get('acquisition') == 'automatic', 'automatic feature grant history mismatch')
            elif feature.get('acquisition') == 'selection':
                selection = credential(grant.get('selectionRef', MISSING))
                require(selection.get('recordType') == 'class_feature_selection' and selection.get('featureId') == feature['id']
                        and selection.get('classAssignmentRef') == grant['classAssignmentRef'], 'feature selection does not match assignment')
                slots = [x for x in class_source.get('featureSelections', []) if x['id'] == selection.get('slotId')]
                require(len(slots) == 1 and feature['id'] in slots[0]['allowedFeatureIds'] and assignment['classLevel'] >= slots[0]['minimumClassLevel'],
                        'source-qualified feature selection opportunity missing')
                require(ordered(selection['at']) <= ordered(grant['at']) and ordered(assignment['at']) <= ordered(selection['at']), 'feature selection chronology mismatch')
                same_slot = [credential(ref) for ref in world.get('credentialRefs', [])
                             if self.resolve(ref).get('recordType') == 'class_feature_selection'
                             and self.resolve(ref).get('classAssignmentRef') == grant['classAssignmentRef']
                             and self.resolve(ref).get('slotId') == selection.get('slotId')]
                require(len(same_slot) == 1, 'class feature selection opportunity spent more than once')
            else:
                raise EvidenceFailure('source feature lacks its acquired automatic/selection procedure')
        elif sid == 'divine_favor':
            relationship = one('worship_relationship'); deity = source(relationship.get('deityRef', MISSING))
            require(deity.get('recordType') == 'opaque_referent' and deity.get('referentKind') == 'deity', 'no established deity reference')
            require(relationship.get('relationship') == 'worship', 'record does not establish worship')
            if relationship.get('endedAt') is not None:
                require(acquired_at < ordered(relationship['endedAt']), 'worship relationship ended before snapshot', 'CONTRADICTED')
        elif sid == 'elemental_body':
            event = one('exposure_event'); plane = source(event.get('planeRef', MISSING))
            require(plane.get('recordType') == 'opaque_referent' and plane.get('referentKind') == 'elemental_plane', 'no established elemental-plane reference')
            require(event.get('predicate') == 'exposure_to_elemental_plane', 'event does not establish literal exposure')
            choices = evidence.get('choiceBindings')
            require(isinstance(choices, dict) and set(choices) == {'permanentType'} and choices['permanentType'] in {'acid', 'cold', 'fire', 'lightning', 'thunder'}, 'missing or invalid permanent elemental type')
            require(acquisition.get('choices') == choices, 'permanent choice not bound to acquisition')
        elif sid == 'dragon_blood':
            if branch == 'Dragonborn':
                assignment = one('lineage_assignment'); lineage = source(assignment.get('sourceRef', MISSING))
                require(lineage.get('name') == 'Dragonborn', 'actual lineage is not literal Dragonborn', 'CONTRADICTED')
                require(assignment.get('lineage') == 'Dragonborn' and character.get('lineage') == 'Dragonborn', 'lineage assignment mismatch')
                qualifying_source_ref = assignment['sourceRef']
                grant = assignment
            else:
                grant = one('bloodline_assignment')
                assignment, class_source = actual_class(grant.get('classAssignmentRef', MISSING), 'Sorcerer')
                bloodline = source(grant.get('sourceRef', MISSING))
                require(bloodline.get('recordType') == 'bloodline' and bloodline.get('bloodlineKind') == 'draconic' and bloodline.get('className') == 'Sorcerer', 'no actual draconic bloodline source')
                require(bloodline.get('id') in class_source.get('bloodlineIds', []) and ordered(assignment['at']) <= ordered(grant['at']), 'bloodline not granted by the actual class history')
                qualifying_source_ref = grant['sourceRef']
            choices = evidence.get('choiceBindings')
            require(isinstance(choices, dict) and set(choices) == {'damageType', 'sourceRef', 'characterId'}, 'missing source-bound ancestry damage type')
            type_ref = choices['sourceRef']; source_type = self.resolve(type_ref)
            expected_type_ref = {**qualifying_source_ref, 'pointer': qualifying_source_ref['pointer'] + '/damageType'}
            require(type_ref == expected_type_ref and grant.get('damageTypeRef') == type_ref and choices['characterId'] == actor_id,
                    'damage type belongs to another actor or qualifying source')
            require(isinstance(source_type, str) and bool(source_type) and choices['damageType'] == source_type, 'recorded damage type does not match qualifying source')
            require(acquisition.get('choices') == choices, 'sourced damage type not bound to acquisition')
        return {'outcome': 'CONDITIONAL_ONLY' if mode == 'conditional_fixture' else 'ESTABLISHED_FOR_SNAPSHOT',
                'evidenceMode': mode, 'featId': sid, 'branch': branch,
                'worldId': world_id, 'characterId': actor_id, 'acquisitionRef': deepcopy(evidence['acquisitionRef']),
                'reason': 'bound external predicate established within the independently admitted evidence domain',
                'campaignAcquisitionEstablished': False}


def acquisition_gate(sid, result, paid_history, opportunity, expected_snapshot, owned_berserker=False):
    """Other gates use actual source-derived PaidChoices; no payment is mutated."""
    external = result.get('outcome') in {'CONDITIONAL_ONLY', 'ESTABLISHED_FOR_SNAPSHOT'}
    credential = external or (sid == 'frenzied_rage' and owned_berserker and paid_history.has('berserker'))
    failures = []
    if not credential:
        failures.append('required external credential or lawful printed alternative not established')
    if paid_history.scores != expected_snapshot['permanentScores']:
        failures.append('bound acquisition ability snapshot mismatch')
    ability = {'frenzied_rage': 'CON', 'elemental_body': 'CON', 'divine_favor': 'CHA'}.get(sid)
    if ability and paid_history.scores[ability] < 15:
        failures.append(ability + ' below permanent15')
    op = paid_history.opportunities.get(opportunity)
    if op is None or op['spent']:
        failures.append('no independently payable earned opportunity')
    if paid_history.has(sid):
        failures.append('nonrepeatable feat already acquired')
    return {'decision': 'DENIED' if failures else 'CONDITIONAL_ACQUISITION_CASE',
            'failures': failures, 'externalOutcome': result.get('outcome'),
            'campaignAcquisitionEstablished': False, 'paymentCommitted': False}
