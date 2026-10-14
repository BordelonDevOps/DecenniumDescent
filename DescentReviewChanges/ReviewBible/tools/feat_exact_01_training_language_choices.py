"""Bounded skill/tool/language selections under the existing reviewed sources.

Separate Lore/culture records are explicit conditional prior credentials, never
new world lore, a twenty-first ordinary skill or authenticated campaign facts.
"""
from copy import deepcopy
from feat_exact_01_prodigy_choices import ProdigyAcquisition
from feat_exact_01_acquisition_models import pb


class TrainingLanguageChoices(ProdigyAcquisition):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.half_skill_choices = []
        self.language_anchors = {}
        self.cultural = None
        self.culture_records = {}
        self.lore_sources = {}
        self.subject_sources = {}

    def snapshot(self):
        return {**super().snapshot(), 'halfSkillChoices': deepcopy(self.half_skill_choices),
            'languageAnchors': deepcopy(self.language_anchors), 'culturalChoice': deepcopy(self.cultural),
            'conditionalCultureRecords': deepcopy(self.culture_records),
            'separateLoreSources': deepcopy(self.lore_sources), 'boundedHistorySources': deepcopy(self.subject_sources)}

    def qualification(self, sid):
        requirement = self.contracts[sid]['requirements']
        if requirement['kind'] == 'noPrintedPrerequisite':
            return True
        if requirement['kind'] == 'permanentAbility':
            return self.pay.scores[requirement['ability']] >= requirement['minimum']
        raise ValueError('Unmodeled prerequisite cannot be assumed satisfied')

    def commit(self, sid, level, choices, resolved):
        grant = self.pay.commit(sid, self.actor['firstClass'] + ':' + str(level),
            choice=choices, prerequisites_met=self.qualification(sid))
        event = {'feat': sid, 'orderedChoices': deepcopy(resolved), 'grant': grant,
            'abilityIncrease': 0, 'newPhysicalItems': [], 'newCourseCredit': 0, 'futureChoiceCredit': False}
        self.events.append(event)
        return deepcopy(event)

    def acquire_skilled(self, level, choices):
        if not isinstance(choices, list) or len(choices) != 3:
            raise ValueError('Resolve exactly three actual skill/tool slots')
        sources = deepcopy(self.skill_sources); tools = set(self.tools); trades = deepcopy(self.trades)
        resolved = []
        for choice in choices:
            missing_skills = set(self.skill_catalog) - {s for s, grants in sources.items() if max(grants.values()) >= 1}
            missing_tools = set(self.tool_catalog) - tools
            if not missing_skills and not missing_tools:
                if choice is not None:
                    raise ValueError('Exhausted choice has no invented substitute or future credit')
                resolved.append({'part': 'skill-or-tool', 'state': 'exhausted', 'choice': None}); continue
            if not isinstance(choice, dict) or set(choice) != {'kind', 'id'}:
                raise ValueError('Choose one genuinely missing skill or profiled tool')
            sid = choice['id']
            if choice['kind'] == 'skill' and sid in missing_skills:
                sources.setdefault(sid, {})['skilled'] = 1
            elif choice['kind'] == 'tool' and sid in missing_tools:
                tools.add(sid)
                if sid in self.primary:
                    trades.setdefault(self.primary[sid], {'level': 1, 'xp': 0})
            else:
                raise ValueError('Duplicate, existing or ineligible skill/tool choice')
            resolved.append({'part': 'skill-or-tool', 'state': 'resolved', 'choice': deepcopy(choice)})
        result = self.commit('skilled', level, choices, resolved)
        self.skill_sources = sources; self.tools = tools; self.trades = trades
        return result

    def acquire_jack(self, level, choices):
        if not isinstance(choices, list) or len(choices) != 2:
            raise ValueError('Two actual unproficient skill choices required')
        eligible = {s for s in self.skill_catalog if self.skill_factor(s) == 0}
        selected = []; resolved = []
        for choice in choices:
            if not eligible:
                if choice is not None:
                    raise ValueError('No remaining actual skill; mark exhaustion')
                resolved.append({'part': 'unproficient-skill', 'state': 'exhausted', 'choice': None}); continue
            if choice not in eligible:
                raise ValueError('Choose a distinct actual unproficient skill, never a tool')
            selected.append(choice); eligible.remove(choice)
            resolved.append({'part': 'unproficient-skill', 'state': 'resolved', 'choice': choice})
        result = self.commit('jack_of_all_trades', level, choices, resolved)
        self.half_skill_choices = selected
        return result

    def task_pb_contribution(self, skill, other_untrained=0):
        if skill not in self.skill_catalog or other_untrained < 0:
            raise ValueError('Actual skill and nonnegative independent contribution required')
        current_pb = pb(sum(self.pay.current_classes.values())); factor = self.skill_factor(skill)
        half = current_pb // 2 if skill in self.half_skill_choices and factor == 0 else 0
        return max(current_pb * factor, half, other_untrained)

    def acquire_languages(self, sid, level, choices):
        if sid not in {'linguist', 'polyglot'} or not isinstance(choices, list) or len(choices) != 3:
            raise ValueError('Linguist/Polyglot each resolves three ordered language slots')
        languages = deepcopy(self.languages); resolved = []
        for selected in choices:
            resolved.append(languages.choose(selected, sid))
        result = self.commit(sid, level, choices, resolved)
        self.languages = languages
        self.language_anchors[sid] = [r['language'] for r in resolved if r['state'] == 'resolved']
        return result

    def admit_conditional_culture_record(self, record):
        required = {'id', 'evidenceMode', 'existingCulturePremise', 'sourceRef', 'separateLoreCredential'}
        if not required <= record.keys() or record['evidenceMode'] != 'conditional_fixture' or not record['existingCulturePremise'] or not record['sourceRef']:
            raise ValueError('Explicitly conditional pre-existing culture and record reference required')
        if record['id'] in self.culture_records:
            raise ValueError('Retain predecessor identity; no overwritten culture receipt')
        lore = record['separateLoreCredential']
        if lore is not None and (not isinstance(lore, dict) or not {'id', 'recordRef'} <= lore.keys() or not lore['id'] or not lore['recordRef']):
            raise ValueError('Separate Lore is permitted only with its own recorded credential')
        self.culture_records[record['id']] = deepcopy(record)

    def acquire_cultural(self, level, choice):
        if not isinstance(choice, dict) or set(choice) != {'kind', 'id'}:
            raise ValueError('One exact credential or named existing culture required')
        kind, sid = choice['kind'], choice['id']
        sources = deepcopy(self.skill_sources); lore = deepcopy(self.lore_sources); subjects = deepcopy(self.subject_sources)
        if kind == 'skill' and sid in {'History', 'Religion'}:
            factor = self.skill_factor(sid)
            if factor == 0:
                sources.setdefault(sid, {})['cultural_expert'] = 1
            entry = {'kind': kind, 'id': sid, 'branch': 'expertise-in-cultural-context' if factor else 'proficiency', 'snapshotFactor': factor}
        elif kind == 'culture' and sid in self.culture_records:
            prior = self.culture_records[sid]
            if prior['separateLoreCredential'] is not None:
                credential = prior['separateLoreCredential']['id']
                factor = max([0] + list(lore.get(credential, {}).values()))
                if factor == 0:
                    lore.setdefault(credential, {})['cultural_expert'] = 1
                entry = {'kind': 'separate-Lore', 'id': credential, 'culture': sid,
                    'branch': 'expertise-in-cultural-context' if factor else 'proficiency', 'snapshotFactor': factor}
            else:
                factor = max(self.skill_factor('History'), max([0] + list(subjects.get(sid, {}).values())))
                if factor == 0:
                    subjects.setdefault(sid, {})['cultural_expert'] = 1
                entry = {'kind': 'bounded-History', 'id': sid,
                    'branch': 'expertise-in-cultural-context' if factor else 'proficiency', 'snapshotFactor': factor}
        else:
            raise ValueError('No invented culture, ordinary skill, or absent Lore credential')
        result = self.commit('cultural_expert', level, choice, [entry])
        self.skill_sources = sources; self.lore_sources = lore; self.subject_sources = subjects; self.cultural = entry
        return result

    def cultural_factor(self, skill, culture=None, cultural_context=False):
        if skill in self.skill_catalog:
            ordinary = self.skill_factor(skill)
        elif skill in self.lore_sources:
            ordinary = max(self.lore_sources[skill].values())
        else:
            ordinary = 0
        if skill == 'History' and culture in self.subject_sources:
            ordinary = max(ordinary, max(self.subject_sources[culture].values()))
        entry = self.cultural
        if not entry or entry['branch'] != 'expertise-in-cultural-context' or not cultural_context:
            return ordinary
        match = entry['kind'] == 'skill' and entry['id'] == skill
        match |= entry['kind'] == 'separate-Lore' and entry['id'] == skill and entry['culture'] == culture
        match |= entry['kind'] == 'bounded-History' and skill == 'History' and entry['id'] == culture
        return max(ordinary, 2) if match else ordinary
