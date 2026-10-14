"""ACQ-03 acquisition snapshots for actual supplied feat and Wizard routes.

These are conditional source-qualified projections, not a casting engine or a
complete character builder. File evidence authenticates source versions, never
the occurrence of a campaign acquisition, study period or other supplied event.
"""
from copy import deepcopy
from hashlib import sha256
import json


def at(value, pointer):
    for key in pointer.strip('/').split('/'):
        value = value[int(key)] if isinstance(value, list) else value[key]
    return value


class CastingSources:
    def __init__(self, root, dependencies, supplements, wizard):
        self.root = root; self.dependencies = dependencies; self.supplements = supplements; self.wizard = wizard
        self.cache = {}
        self.focus = supplements['SUP-05']['newSpellFocus']
        if self.focus.get('castingPrerequisitePolicyRef') != 'FEAT327-ACQ-03':
            raise ValueError('Current controlling Spell Focus acquisition policy required')

    def ordinary(self, spell_id, source_class):
        dep = self.dependencies.get(spell_id)
        if not dep or dep['authoredIndexEntry']['authoredStatus'] != 'reviewed-authored-operational-playtest':
            raise ValueError('No complete reviewed authored payload evidence supplied')
        binding = dep['binding']; path = self.root / binding['file']
        if binding['file'] not in self.cache:
            data = path.read_bytes()
            self.cache[binding['file']] = (len(data), sha256(data).hexdigest(), json.loads(data))
        size, digest, document = self.cache[binding['file']]
        if size != binding['bytes'] or digest != binding['sha256']:
            raise ValueError('Authored payload source binding changed')
        card = at(document, binding['pointer'])
        if card != dep['completeCurrentProcedureCard'] or card.get('id') != spell_id:
            raise ValueError('Exact current whole payload is not the supplied source')
        if not card.get('operational', card.get('operationalCandidate')):
            raise ValueError('Null or unfinished operational payload')
        placement = dep['originalCatalogRecord']['classAccess'].get(source_class)
        if not placement or card['classAccess'].get(source_class) != placement:
            raise ValueError('Missing or mismatched exact source-class placement')
        return {'spellId': spell_id, 'sourceClass': source_class, 'rank': placement['rank'],
                **({'school': placement['school']} if 'school' in placement else {}),
                'minimumClassLevel': placement['minimumClassLevel'], 'placement': deepcopy(placement),
                'payloadBinding': deepcopy(binding), 'authoredIndexEntry': deepcopy(dep['authoredIndexEntry'])}

    def blast(self):
        profile = self.supplements['SUP-07']['eldritchBlast']
        return {'spellId': profile['id'], 'rank': profile['rank'],
                **({'school': profile['school']} if 'school' in profile else {}),
                'supplement': 'SUP-07/eldritchBlast', 'completeProfile': deepcopy(profile)}


def school_state(route):
    return {'presence': 'absent'} if 'school' not in route else {'presence': 'null' if route['school'] is None else 'value', 'value': route['school']}


class CastingCredentials:
    def __init__(self, sources, moment=0):
        self.sources = sources; self.moment = moment
        self.grants = {}; self.routes = []; self.wizard_level = 0
        self.book = set(); self.known = set(); self.prepared = set(); self.book_present = True
        self.substitution_used = False
        self.use_state = {'rp': 0, 'temporaryBlocks': [], 'renewableCharges': {}}

    def snapshot(self):
        return deepcopy({k: v for k, v in self.__dict__.items() if k != 'sources'})

    def import_initiate(self, acquisition, acquired_at):
        snapshot = acquisition.snapshot()
        for grant in snapshot['featRoutes']:
            record = next((r for r in snapshot['paidGrants'] if r['identity'] == grant['grantIdentity'] and r['opportunity'] == grant['paidOpportunity']), None)
            if not record or not snapshot['opportunities'][record['opportunity']]['spent']:
                raise ValueError('Real paid Initiate acquisition history required')
            gid = record['identity'] + '/' + record['opportunity']
            if gid in self.grants:
                raise ValueError('Grant history already imported')
            self.grants[gid] = {'source': 'actual-paid-Magic-Initiate', 'acquiredAt': acquired_at, 'payment': deepcopy(record)}
            for spell in grant['spells']:
                route = self.sources.ordinary(spell['id'], spell['sourceClass'])
                if route['rank'] != spell['rank'] or route.get('school') != spell.get('school') or route['payloadBinding'] != spell['payloadBinding']:
                    raise ValueError('The acquired spell route differs from its exact source evidence')
                self.routes.append({**route, 'grantId': gid, 'kind': 'personal-feat', 'ability': grant['castingAbility']})
            self.use_state['renewableCharges'][gid] = deepcopy(grant['rankOneCharge'])

    def wizard_snapshot(self, level, known_cantrips, book_spells, prepared_spells, acquired_at, intelligence=16):
        if self.wizard_level or type(level) is not int or not 1 <= level <= 20:
            raise ValueError('One supplied lawful Wizard projection is required')
        maximum = self.sources.wizard['maxSpellRankByClassLevel'][level - 1]
        if len(known_cantrips) != len(set(known_cantrips)) or len(book_spells) != len(set(book_spells)):
            raise ValueError('Duplicate repertoire entry')
        if not set(prepared_spells) <= set(book_spells) or len(prepared_spells) > max(1, level + (intelligence - 10) // 2):
            raise ValueError('Prepared subset must be legal within the actual matrix capacity')
        if len(known_cantrips) > (3 if level < 4 else 4 if level < 10 else 5):
            raise ValueError('Known-cantrip subset exceeds actual source capacity')
        rows = []
        for sid in known_cantrips:
            route = self.sources.ordinary(sid, 'Wizard')
            if route['rank'] != 0 or route['minimumClassLevel'] > level:
                raise ValueError('Known cantrip lacks an actual legal Wizard binding')
            rows.append({**route, 'grantId': 'Wizard/class-engine', 'kind': 'wizard-known'})
        for sid in book_spells:
            route = self.sources.ordinary(sid, 'Wizard')
            if not 1 <= route['rank'] <= maximum or route['minimumClassLevel'] > level:
                raise ValueError('Book entry exceeds actual Wizard rank/class access')
            rows.append({**route, 'grantId': 'Wizard/class-engine', 'kind': 'wizard-prepared'})
            if level >= 2 and sid in self.sources.supplements['SUP-05']['newRitualTagOverlay']['ids'] and route['rank'] == 1:
                rows.append({**route, 'grantId': 'Wizard/automatic-ritual-2', 'kind': 'wizard-ritual'})
        self.wizard_level = level; self.known = set(known_cantrips); self.book = set(book_spells); self.prepared = set(prepared_spells)
        self.grants['Wizard/class-engine'] = {'source': 'actual-Wizard-level-and-repertoire-projection', 'classLevel': level, 'acquiredAt': acquired_at, 'engineIndices': [2, 3, 4, 8, 31]}
        if level >= 2:
            self.grants['Wizard/automatic-ritual-2'] = {'source': 'Wizard/engine/13', 'classLevel': level, 'acquiredAt': acquired_at}
        self.routes.extend(rows)

    def import_forbidden_pact(self, paid, acquired_at, sigil):
        if sigil not in {x['id'] for x in self.sources.supplements['SUP-07']['pactSigils']}:
            raise ValueError('Actual finite sigil required')
        record = next((r for r in paid.grants if r['identity'] == 'forbidden_pact'), None)
        if not record or record['abilitySnapshotBefore']['CHA'] < 13 or sum(paid.current_classes.values()) < 3 or record['choice'] != {'sigil': sigil}:
            raise ValueError('Paid source-qualified Forbidden Pact with permanent sigil required')
        if sigil == 'energyResistance':
            raise ValueError('This finite witness uses hex/shadowstep; resistance needs its additional permanent type choice')
        gid = 'forbidden_pact/' + record['opportunity']
        self.grants[gid] = {'source': 'actual-paid-Forbidden-Pact', 'acquiredAt': acquired_at, 'payment': deepcopy(record)}
        self.routes.append({**self.sources.blast(), 'grantId': gid, 'kind': 'personal-feat', 'ability': 'CHA'})

    def qualifying(self):
        result = []
        for route in self.routes:
            grant = self.grants.get(route['grantId'])
            if not grant or grant['acquiredAt'] > self.moment:
                continue
            if any(key in grant and grant[key] <= self.moment for key in ['removedAt', 'expiresAt']):
                continue
            sid = route['spellId']; kind = route['kind']
            if kind == 'wizard-known' and sid not in self.known:
                continue
            if kind == 'wizard-prepared' and sid not in self.prepared:
                continue
            if kind == 'wizard-ritual' and (not self.book_present or sid not in self.book or self.wizard_level < 2):
                continue
            if kind not in {'personal-feat', 'wizard-known', 'wizard-prepared', 'wizard-ritual'}:
                raise ValueError('Route outside this finite projection')
            result.append(deepcopy(route))
        return result

    def matches(self, node):
        if node.get('castingPrerequisitePolicyRef') != 'FEAT327-ACQ-03' or node['kind'] not in {'actualSpellcastingRoute', 'actualCastAccess'}:
            raise ValueError('An actual ACQ-03 casting predicate is required')
        for route in self.qualifying():
            if 'spellId' in node and route['spellId'] != node['spellId']:
                continue
            if 'school' in node and ('school' not in route or route['school'] is None or route['school'] != node['school']):
                continue
            if 'exactRank' in node and route['rank'] != node['exactRank']:
                continue
            if 'minimumRank' in node and route['rank'] < node['minimumRank']:
                continue
            if 'sourceClass' in node and route.get('sourceClass') != node['sourceClass']:
                continue
            return True
        return False

    def supported_schools(self):
        return {r['school'] for r in self.qualifying() if isinstance(r.get('school'), str) and r['school']}

    def acquire_spell_focus(self, paid, opportunity, school):
        if school not in self.supported_schools():
            raise ValueError('A real qualifying acquired spell must support the permanent school selection')
        sid = self.sources.focus['id']
        if sid not in paid.valid_feat_ids:
            raise ValueError('Supplement must be explicitly included as a separate paid identity')
        return paid.commit(sid, opportunity, choice=school, prerequisites_met=bool(self.qualifying()))

    def substitute(self, old_spell, new_spell, completed_minutes):
        if self.substitution_used or not self.book_present or old_spell not in self.prepared or new_spell not in self.book or completed_minutes < 10:
            raise ValueError('An actual lawful completed substitution is required')
        self.prepared.remove(old_spell); self.prepared.add(new_spell); self.substitution_used = True
