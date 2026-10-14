"""Finite Prodigy choice replay; not a full character builder or game runtime.

World contact/admission lists are explicitly conditional premises. This module
does not authenticate campaign history or grant class/secret-language access.
"""
from copy import deepcopy
from feat_exact_01_acquisition_models import PaidChoices, pb
from feat_exact_01_training_prerequisite_model import materialize_training, normalize_name


def tool_projection(equipment, trade_reference):
    """Include actual equipment, Fishing tackle and the five reviewed new kits."""
    profiles = {sid: deepcopy(r) for sid, r in equipment.items() if r['category'] == 'Tools'}
    fishing = equipment['adventuring-gear.fishing-tackle']
    profiles[fishing['id']] = deepcopy(fishing)
    kit_section = trade_reference.split('## New mundane kits', 1)[1].split('## Actual stations', 1)[0]
    for line in kit_section.splitlines():
        if not line.startswith('| ') or ' gp |' not in line:
            continue
        name, price, weight, contents = [s.strip() for s in line.strip('|').split('|')]
        # These are projection-local references to exact table rows, not new
        # canonical equipment IDs or new physical items in a character inventory.
        sid = 'trade-reference:' + name
        profiles[sid] = {'id': sid, 'name': name, 'category': 'Tools', 'group': 'reviewed-new-kit',
                         'sourceSection': 'CRAFTING_TRADE_REFERENCE.md#new-mundane-kits',
                         'price': price, 'weight': weight, 'contents': contents}
    primary = {}
    for line in trade_reference.split('Existing equipment supplies', 1)[0].splitlines():
        if not line.startswith('| ') or line.startswith('| Trade |'):
            continue
        trade, ability, tool, artisan, injury = [s.strip() for s in line.strip('|').split('|')]
        hits = [sid for sid, p in profiles.items() if normalize_name(p['name']) == normalize_name(tool)]
        if len(hits) != 1:
            raise ValueError('Missing or ambiguous actual primary tool: ' + tool)
        primary[hits[0]] = trade
    if len(primary) != 16:
        raise ValueError('Actual sixteen-trade source mapping changed')
    return profiles, primary


class LanguageChoices:
    def __init__(self, source, available):
        self.source = source
        self.identities = {r['canonicalId']: r for r in source['grants']['identities']}
        self.modes = set(source['rules']['permanentModeConvention']['ordinaryModes'])
        self.available = deepcopy(available)
        self.known = {}; self.scripts = set(); self.receipts = []
        for row in self.available:
            sid = row['language']
            if row.get('evidenceMode') != 'conditional_fixture' or not row.get('contactPremise'):
                raise ValueError('Declare actual contact/admission as a conditional premise')
            if sid not in self.identities or sid in {'the-voice', 'resonant-cant', 'druidic', 'deep-speech'} or sid.startswith('forgotten-script/'):
                raise ValueError('This finite ordinary/contact slice supplies no such restricted entitlement')
            permitted = self.attested_modes(sid)
            if set(row['modes']) != permitted:
                raise ValueError('Contact list cannot fabricate unattested modes')
            ordinary = self.identities[sid]['operationalScope'].startswith('ordinary') and sid != 'draconic'
            if row.get('admission') != ('ordinary-contact' if ordinary else 'source-qualified-contact'):
                raise ValueError('Exotic or special option requires its separately declared allowed-contact premise')
        if len({r['language'] for r in self.available}) != len(self.available):
            raise ValueError('Duplicate available identity')

    def attested_modes(self, sid):
        if sid == 'runic':
            return {'reading', 'writing'}
        if sid not in self.identities:
            raise ValueError('Unknown language identity; no fuzzy aliases')
        return set(self.modes)

    def add(self, sid, modes, source):
        if not set(modes) <= self.attested_modes(sid):
            raise ValueError('Grant contains unattested modes')
        self.known.setdefault(sid, set()).update(modes)
        if {'reading', 'writing'} & set(modes):
            shared = self.source['grants']['scripts']['dwarvish-script']['attestedLanguageUsers']
            self.scripts.add('dwarvish-script' if sid in shared else 'language-local:' + sid)
        self.receipts.append({'language': sid, 'modes': sorted(modes), 'source': source})

    def eligible(self):
        return {r['language']: set(r['modes']) - self.known.get(r['language'], set())
                for r in self.available if set(r['modes']) - self.known.get(r['language'], set())}

    def choose(self, sid, source):
        eligible = self.eligible()
        if not eligible:
            if sid is not None:
                raise ValueError('Language slot is exhausted; no invented substitute')
            result = {'source': source, 'state': 'exhausted', 'futureCredit': False}
            self.receipts.append(result)
            return deepcopy(result)
        if sid not in eligible:
            raise ValueError('Choose an eligible unsatisfied language or genuinely missing modes')
        missing = eligible[sid]
        self.add(sid, missing, source)
        return {'source': source, 'state': 'resolved', 'language': sid, 'newModes': sorted(missing)}

    def snapshot(self):
        return {'known': {k: sorted(v) for k, v in self.known.items()}, 'scripts': sorted(self.scripts),
                'receipts': deepcopy(self.receipts), 'conditionalAvailableOptions': deepcopy(self.available)}


class ProdigyAcquisition:
    def __init__(self, actor, classes, equipment, skills, ancestry, backgrounds, contracts,
                 language_source, available, starting_choices, trade_reference):
        self.actor = deepcopy(actor); self.classes = classes; self.skill_catalog = deepcopy(skills)
        self.contracts = contracts
        if actor['ancestry'] != 'human' or actor['variant'] != 'imperial-human' or actor['priorFeatChoices']:
            raise ValueError('This paid history uses actual Human/Imperial sources and no unearned prior feats')
        training = materialize_training(actor, classes, equipment, skills, ancestry, backgrounds)
        self.training = deepcopy(training)
        self.skill_sources = {s: {'starting-source-projection': f} for s, f in training['skills'].items()}
        self.tools = set(training['tools'])
        self.tool_catalog, self.primary = tool_projection(equipment, trade_reference)
        self.trades = {self.primary[s]: {'level': 1, 'xp': 0} for s in self.tools if s in self.primary}
        self.pay = PaidChoices({c: r['asiClassLevels'] for c, r in classes.items()}, {},
                              deepcopy(actor['classLevels']), deepcopy(training['scores']), set(contracts))
        self.languages = LanguageChoices(language_source, available)
        human = next(r for r in language_source['grants']['baseGrants'] if r['ancestryId'] == actor['ancestry'])
        variant = next(r for r in language_source['grants']['variants'] if r['variantId'] == actor['variant'])
        background = next(r for r in language_source['grants']['backgrounds'] if r['backgroundId'] == actor['background'])
        for sid in human['derivedFixed']:
            self.languages.add(sid, {m for m, present in human['modes'].items() if present}, 'Human fixed language')
        for sid in background['derivedGrant']['fixed']:
            self.languages.add(sid, self.languages.attested_modes(sid), 'background fixed language')
        count = human['derivedChoice']['count'] + variant['countAdded'] + background['derivedGrant']['choice']['count']
        slots = ['Human choice'] * human['derivedChoice']['count'] + ['Imperial choice'] * variant['countAdded']
        slots += ['background choice ' + str(i+1) for i in range(background['derivedGrant']['choice']['count'])]
        if len(starting_choices) != count:
            raise ValueError('Resolve every real starting language slot exactly once')
        for sid, label in zip(starting_choices, slots):
            self.languages.choose(sid, label)
        self.events = []

    def skill_factor(self, skill):
        return max([0] + list(self.skill_sources.get(skill, {}).values()))

    def skill_modifier(self, skill):
        return (self.pay.scores[self.skill_catalog[skill]] - 10)//2 + pb(sum(self.pay.current_classes.values())) * self.skill_factor(skill)

    def advance(self, level):
        first = self.actor['firstClass']
        if type(level) is not int or not self.pay.current_classes[first] <= level <= 20:
            raise ValueError('Invalid forward class level')
        self.actor['classLevels'][first] = level; self.pay.current_classes[first] = level
        self.training['totalLevel'] = level

    def earn(self, level):
        first = self.actor['firstClass']; self.pay.earn_class_opportunity(first + ':' + str(level), first, level)

    def snapshot(self):
        return {'actor': deepcopy(self.actor), 'payment': deepcopy(self.pay.__dict__),
                'skills': {s: self.skill_factor(s) for s in self.skill_sources},
                'skillSources': deepcopy(self.skill_sources), 'tools': sorted(self.tools), 'trades': deepcopy(self.trades),
                'languages': self.languages.snapshot(), 'events': deepcopy(self.events)}

    def acquire(self, sid, level, choices):
        if sid not in {'prodigy', 'skill_expert'}:
            raise ValueError('Only the two exact ordered-training procedures are modeled')
        expected = {'skill', 'expertise'} | ({'tool', 'language'} if sid == 'prodigy' else set())
        if not isinstance(choices, dict) or set(choices) != expected:
            raise ValueError('All and only the actual choice fields are required')
        # Validate a prospective transaction before the paid history is changed.
        sources = deepcopy(self.skill_sources); tools = set(self.tools); trades = deepcopy(self.trades)
        languages = deepcopy(self.languages); ordered = []
        missing = set(self.skill_catalog) - {s for s in sources if max(sources[s].values()) >= 1}
        selected = choices['skill']
        if missing:
            if selected not in missing:
                raise ValueError('Select a genuinely new actual skill')
            sources.setdefault(selected, {})[sid] = 1
        elif selected is not None:
            raise ValueError('All actual skills already known; mark skill slot exhausted')
        ordered.append({'part': 'skill', 'choice': selected, 'state': 'resolved' if missing else 'exhausted'})
        if sid == 'prodigy':
            missing_tools = set(self.tool_catalog) - tools
            tool = choices['tool']
            if missing_tools:
                if tool not in missing_tools:
                    raise ValueError('Select a genuinely new actual profiled tool')
                tools.add(tool)
                if tool in self.primary:
                    trades.setdefault(self.primary[tool], {'level': 1, 'xp': 0})
            elif tool is not None:
                raise ValueError('All actual profiled tools known; mark tool slot exhausted')
            ordered.append({'part': 'tool', 'choice': tool, 'state': 'resolved' if missing_tools else 'exhausted'})
            ordered.append({'part': 'language', **languages.choose(choices['language'], 'prodigy')})
        eligible = {s for s, grants in sources.items() if max(grants.values()) == 1}
        expert = choices['expertise']
        if eligible:
            if expert not in eligible:
                raise ValueError('Expertise chooses one now-proficient nonexpert skill; never a tool or already expert skill')
            sources[expert][sid] = 2
        elif expert is not None:
            raise ValueError('No remaining eligible Expertise skill; no invented substitute')
        ordered.append({'part': 'expertise', 'choice': expert, 'state': 'resolved' if eligible else 'exhausted'})
        if sid == 'prodigy':
            branches = self.contracts[sid]['requirements']
            if branches != {'kind': 'any', 'requirements': [
                {'kind': 'actualLineageReceipt', 'lineage': s, 'noSilentAlias': True} for s in ['Half-elf', 'Half-orc', 'Human']]}:
                raise ValueError('Actual lineage gate changed')
            qualified = self.actor['ancestry'] == 'human'
        else:
            qualified = self.contracts[sid]['requirements'] == {'kind': 'noPrintedPrerequisite'}
        grant = self.pay.commit(sid, self.actor['firstClass'] + ':' + str(level), choice=choices, prerequisites_met=qualified)
        self.skill_sources = sources; self.tools = tools; self.trades = trades; self.languages = languages
        self.events.append({'feat': sid, 'orderedChoices': ordered, 'grant': grant, 'abilityIncrease': 0,
                            'newPhysicalItems': [], 'newCourseCredit': 0, 'futureChoiceCredit': False})
        return deepcopy(self.events[-1])
