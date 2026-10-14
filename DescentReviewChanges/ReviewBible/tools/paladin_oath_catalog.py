"""Pair every preserved Sacred Oath with its named Oathbreaker and playtest cards."""
import re


def card_anchor(card):
    return card['id'].replace('.', '-')


def add_oath_catalog(packet, oaths):
    catalog = []
    for index, oath in enumerate(oaths):
        prefix = f'SACRED_OATHS[{index}].'
        normal, inverted = [], []
        for card in packet['cards']:
            ref = card['source'].get('reference') or ''
            if not re.search(r'(?<![A-Za-z_0-9])' + re.escape(prefix), ref):
                continue
            broken = prefix + 'oathbreaker.' in ref
            card.update(oathId=oath['id'], oathName=oath['name'],
                        oathbreakerName=oath['oathbreaker']['name'])
            card['displayPath'] = (f"{oath['oathbreaker']['name']} — {oath['name']} Oathbreaker"
                                   if broken else oath['name'])
            if broken:
                card['acquisition'] = 'automatic for corresponding Oathbreaker'
            (inverted if broken else normal).append(card['id'])
        catalog.append({
            'oathId': oath['id'], 'oathName': oath['name'],
            'oathbreakerName': oath['oathbreaker']['name'],
            'theme': oath['theme'], 'conductClauses': oath['conductClause'],
            'sourceReference': f'SACRED_OATHS[{index}]',
            'oathCardIds': normal, 'oathbreakerCardIds': inverted,
        })
    shared = [c for c in packet['cards'] if c['path'] == 'Oathbreaker shared']
    for card in shared:
        card['acquisition'] = 'automatic for selected Oathbreaker'
    packet['oathCatalog'] = catalog
    packet['sharedOathbreakerCardIds'] = [c['id'] for c in shared]
    packet['oathCatalogGuide'] = '../../../docs/mechanics/PALADIN_OATHS_AND_OATHBREAKERS.md'


def render_oath_catalog(packet):
    cards = {c['id']: c for c in packet['cards']}
    catalog = packet['oathCatalog']
    shared = [cards[i] for i in packet['sharedOathbreakerCardIds']]
    count = sum(len(o['oathCardIds']) + len(o['oathbreakerCardIds']) for o in catalog)
    lines = [
        '# Paladin — all Sacred Oaths and Oathbreakers', '',
        '**Provisional playtest rules.** Every Oath and named Oathbreaker in the preserved '
        'Sacred Oaths source is paired below. Original source wording and conduct clauses remain intact.', '',
        '[Full Paladin rules and cards](classes/paladin.md) · '
        '[All Base classes](CLASS_PLAYTEST_INDEX.md) · '
        '[Preserved Oath source](../../data/playtest/class_sources/supplements.json) · '
        '[Card data and paired catalog](../../data/public/class_playtests/paladin.json)', '',
        f'Coverage: **{len(catalog)} Oaths, {len(catalog)} named Oathbreaker paths, '
        f'{count} path cards and {len(shared)} shared Oathbreaker cards.** '
        'Each Oath has a Smite, aura, five Revelation spells, Signature Power and Final Gift. '
        'Each corresponding Oathbreaker has its own Death Touch, inverted aura and Blasphemous Word.', '',
        '## Progression and oathbreaking', '',
        '**Paladin is the Base class:** levels 1–2 establish its core abilities. Choose one Oath '
        'at level 3 as the Arch specialization. At level 10 enter Hero mastery of that same Oath; '
        'Signature Power unlocks at 11 and Final Gift at 20. The names below are later Paladin '
        'paths, not additional Base classes.', '',
        'Use the conduct clauses beneath each Oath when judging a breach. The Director identifies '
        'a relevant clause and a knowingly chosen serious breach. Disagreement, a failed roll, '
        'coercion or an unknown fact does not silently strip the character. Record a fall with '
        'the player, then choose the corresponding inversion or an agreed restoration scene.', '',
        'An Oathbreaker replaces the normal Oath package: Death Touch uses the current Lay on '
        'Hands pool; the inverted aura, Blasphemous Word, shared Forbidden spells and Black '
        'Manifestation replace their normal counterparts. Preserve level and spent resources '
        'when switching. Normal and inverted packages do not stack. All level gates still apply. '
        'The full Paladin guide supplies the resource, timing, aura and restoration context.', '',
        '## Paired index', '',
        '| Sacred Oath | Corresponding Oathbreaker |', '|---|---|',
    ]
    for oath in catalog:
        anchor = 'oath-' + oath['oathId']
        lines.append(f"| [{oath['oathName']}](#{anchor}) | "
                     f"[{oath['oathbreakerName']}](#{anchor}-oathbreaker) |")
    lines += ['', '## Shared Oathbreaker spells and capstone', '',
              'These five Forbidden spells and Black Manifestation are **new, shared playtest '
              'completions**. The historical source names a Forbidden Spell List but does not '
              'supply a separate complete spell list for every inversion. All ten Oathbreakers '
              'automatically gain the entries below at their listed levels; the five spells '
              'replace the normal Oath Revelations and the capstone replaces the Final Gift.', '']
    lines += card_table(shared)
    for oath in catalog:
        anchor = 'oath-' + oath['oathId']
        lines += [f'<a id="{anchor}"></a>', '', f"## {oath['oathName']}", '',
                  oath['theme'], '', '**Preserved conduct clauses:**', '']
        lines += ['- ' + clause for clause in oath['conductClauses']]
        lines += ['', '**Normal Oath package:**', '']
        lines += card_table([cards[i] for i in oath['oathCardIds']])
        lines += [f'<a id="{anchor}-oathbreaker"></a>', '',
                  f"### {oath['oathbreakerName']} — Oathbreaker", '',
                  f"The named inversion of {oath['oathName']}. Use these three unique cards "
                  'with the shared Forbidden spells and Black Manifestation above.', '']
        lines += card_table([cards[i] for i in oath['oathbreakerCardIds']])
        lines += [f"Source: `{oath['sourceReference']}` in the preserved supplements. "
                  'Open each linked card for its action, cost, targets, duration, frequency, '
                  'effect and source wording.', '']
    return '\n'.join(lines)


def card_table(cards):
    roles = {'oathSmite': 'Smite', 'oathAura': 'Aura', 'signaturePower': 'Signature Power',
             'oathSpell': 'Revelation spell', 'revelationSpell': 'Revelation spell',
             'finalOathGift': 'Final Gift', 'deathTouch': 'Death Touch',
             'oathbreakerAura': 'Inverted aura', 'blasphemousWord': 'Blasphemous Word',
             'new forbidden spell': 'Shared Forbidden spell', 'new capstone': 'Shared capstone'}
    lines = ['| Paladin level | Feature | Full card |', '|---:|---|---|']
    for card in sorted(cards, key=lambda c: c['minimumClassLevel']):
        lines.append(f"| {card['minimumClassLevel']} | {roles.get(card['sourceKind'], card['sourceKind'])} | "
                     f"[{card['name']}](classes/paladin.md#{card_anchor(card)}) |")
    return lines + ['']
