"""Build a blank, interactive tabletop record; no character rules are executed."""
from pathlib import Path
import hashlib
import json
import re

from reportlab.pdfgen import canvas
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from pypdf import PdfReader

R = Path(__file__).resolve().parents[1]
G = R.parents[1]
OUT = R / 'output/pdf/Decennium_Descent_Character_Sheet_Playtest.pdf'
FIELDS = R / 'data/playtest/character_sheet_form_fields.json'
WIDTH, HEIGHT = letter
LEFT, RIGHT = 36, 576
INK = colors.HexColor('#172532')
ACCENT = colors.HexColor('#284D61')
LINE = colors.HexColor('#A7B4BD')
PALE = colors.HexColor('#EDF2F4')


def token(s):
    return re.sub(r'[^a-z0-9]+', '_', s.lower()).strip('_')


class Sheet:
    def __init__(self):
        OUT.parent.mkdir(parents=True, exist_ok=True)
        self.c = canvas.Canvas(str(OUT), pagesize=letter, invariant=1)
        self.c.setTitle('Decennium Descent - Character Record - Playtest presentation draft')
        self.c.setAuthor('Decennium Descent playtest')
        self.fields = []
        self.page = 0

    def text(self, text, x, y, size=8.5, bold=False, color=INK):
        assert all(ord(c) < 128 for c in text), text
        self.c.setFillColor(color)
        self.c.setFont('Helvetica-Bold' if bold else 'Helvetica', size)
        assert self.c.stringWidth(text, 'Helvetica-Bold' if bold else 'Helvetica', size) <= RIGHT - x + 0.01, text
        self.c.drawString(x, y, text)

    def page_start(self, subtitle):
        if self.page:
            self.c.showPage()
        self.page += 1
        self.text('DECENNIUM DESCENT', LEFT, 755, 17, True)
        self.text(subtitle, LEFT, 734, 12, True, ACCENT)
        self.c.setStrokeColor(ACCENT)
        self.c.setLineWidth(1.2)
        self.c.line(LEFT, 724, RIGHT, 724)
        self.text('PLAYTEST PRESENTATION DRAFT  |  Enter actual values; fields do not calculate.', LEFT, 28, 7)
        self.c.setFillColor(INK)
        self.c.setFont('Helvetica', 8)
        self.c.drawRightString(RIGHT, 28, f'{self.page} / 5')
        return 708

    def note(self, s, y):
        self.text(s, LEFT, y, 8)
        return y - 15

    def section(self, title, y):
        self.c.setFillColor(PALE)
        self.c.rect(LEFT, y - 18, RIGHT - LEFT, 18, stroke=0, fill=1)
        self.text(title.upper(), LEFT + 6, y - 12, 8.5, True)
        return y - 25

    def field(self, name, label, x, y, w, h=20, multiline=False):
        assert name not in {f['name'] for f in self.fields}, name
        assert x >= LEFT and x + w <= RIGHT + 0.01 and y >= 46 and y + h <= 723, (name, x, y, w, h)
        self.c.acroForm.textfield(
            name=name, tooltip=label, x=x, y=y, width=w, height=h,
            value='', fontName='Helvetica', fontSize=9,
            textColor=INK, borderColor=LINE, fillColor=colors.white,
            borderWidth=0.55, borderStyle='solid', forceBorder=True,
            fieldFlags='multiline' if multiline else '',
            maxlen=1400 if multiline else 240,
        )
        self.fields.append({'name': name, 'label': label, 'page': self.page, 'rect': [x, y, x + w, y + h], 'multiline': multiline, 'initialValue': ''})

    def row(self, prefix, labels, y, heights=20):
        gap = 9
        w = (RIGHT - LEFT - gap * (len(labels) - 1)) / len(labels)
        for i, label in enumerate(labels):
            x = LEFT + i * (w + gap)
            self.text(label, x, y - 6, 7.3, True)
            self.field(f'{prefix}_{i+1}', label, x, y - 13 - heights, w, heights, heights > 24)
        return y - heights - 22

    def table(self, title, prefix, columns, rows, y, row_h=24, fixed=None):
        assert sum(w for _, w in columns) == RIGHT - LEFT
        y = self.section(title, y)
        x = LEFT
        for title, w in columns:
            assert self.c.stringWidth(title, 'Helvetica-Bold', 7.1) <= w - 4, title
            self.text(title, x + 2, y - 6, 7.1, True)
            x += w
        y -= 13
        fixed = fixed or {}
        for row in range(rows):
            x = LEFT
            for col, (title, w) in enumerate(columns):
                if (row, col) in fixed:
                    value = fixed[row, col]
                    assert self.c.stringWidth(value, 'Helvetica', 8) <= w - 6, value
                    self.text(value, x + 3, y - row_h / 2 - 3, 8)
                else:
                    label = f'{title}, row {row+1}, {prefix.replace("_", " ")}'
                    self.field(f'{prefix}_{row+1}_{col+1}', label, x + 2, y - row_h + 2, w - 4, row_h - 4, row_h >= 32)
                x += w
            y -= row_h
        return y - 8

    def finish(self):
        assert self.page == 5
        self.c.save()
        reader = PdfReader(OUT)
        fields = reader.get_fields() or {}
        expected = {f['name']: f for f in self.fields}
        assert set(fields) == set(expected)
        widgets = []
        for page in reader.pages:
            for ref in page.get('/Annots', []):
                widget = ref.get_object()
                if widget.get('/Subtype') == '/Widget':
                    widgets.append(widget)
                    name = widget['/T']
                    assert name in expected
                    assert str(widget.get('/V', '')) == ''
                    assert widget.get('/AP', {}).get('/N') is not None
        assert len(widgets) == len(fields) == len(expected)
        for name, f in fields.items():
            assert str(f.get('/V', '')) == '', name
        FIELDS.write_text(json.dumps({
            'status': 'blank-paper-form-presentation-review-pending',
            'document': OUT.relative_to(G).as_posix(),
            'pages': 5, 'fieldCount': len(self.fields), 'fields': self.fields,
            'isCompanionSaveSchema': False, 'automatedCalculations': False,
            'mechanicalOrHumanApproval': False,
            'pdfSha256': hashlib.sha256(OUT.read_bytes()).hexdigest(),
            'checks': {'canonicalFieldsEqualWidgets': True, 'allValuesBlank': True, 'allWidgetsHaveAppearances': True, 'fieldRectanglesInsidePageMargins': True},
        }, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
        print(json.dumps({'pdf': str(OUT), 'pages': 5, 'fields': len(fields), 'bytes': OUT.stat().st_size, 'sha256': hashlib.sha256(OUT.read_bytes()).hexdigest()}))


def main():
    s = Sheet()
    y = s.page_start('01  Character, abilities and training')
    y = s.note('Start with a Base class. Arch and Hero are later stages within that class.', y)
    y = s.row('identity', ['Character / record reference', 'Campaign / player', 'Last updated / session'], y)
    y = s.row('origins', ['Ancestry and variant', 'Background', 'Ability-generation method'], y)
    y = s.row('classes', ['Base classes / each class level', 'Entry order / total level / PB', 'Chosen paths / Oath / Curse / Circle'], y)
    ability_cols = [('Ability', 52), ('Assigned', 60), ('Ancestry', 60), ('Other', 60), ('Score', 60), ('Modifier', 50), ('Save training', 100), ('Save total', 98)]
    y = s.table('Abilities and saves', 'abilities', ability_cols, 6, y, 23, {(i, 0): a for i, a in enumerate(['STR', 'DEX', 'CON', 'INT', 'WIS', 'CHA'])})
    foundation = json.loads((R / 'data/playtest/character_foundation.json').read_text(encoding='utf-8-sig'))
    skills = [(name, ability) for ability, names in foundation['skillAbilities'].items() for name in names]
    assert len(skills) == 20
    fixed = {}
    for i in range(10):
        for col, idx in [(0, i), (3, i + 10)]:
            name, ability = skills[idx]
            fixed[i, col] = f'{name} ({ability})'
    y = s.table('Skills - record actual training; add PB only once', 'skills', [('Skill', 123), ('Training / source', 91), ('Total', 46), ('Skill', 123), ('Training / source', 91), ('Total', 66)], 10, y, 19, fixed)
    y = s.row('training', ['Armor / weapons / special training', 'Tools / kits / instruments / source'], y, 28)
    s.note('Languages and modes: attach the Character Language and Communication Record.', y)

    y = s.page_start('02  Combat, health and active effects')
    y = s.note('Keep source, owner and ending for each effect. A blank field grants no rule or recovery.', y)
    y = s.row('encounter', ['Encounter / scene reference', 'Round / regular-turn marker', 'Initiative / modifier'], y)
    y = s.row('body', ['Root body / current form', 'Size / actual space', 'Speeds / current penalties'], y)
    y = s.row('defense', ['AC / one chosen formula / legal bonuses', 'Resistances / immunities / source limits'], y)
    y = s.row('health', ['Current HP', 'Base maximum HP', 'Effective maximum', 'Healing ceiling', 'Temporary HP'], y)
    y = s.row('life', ['Life: positive / dying / Stable / Dead', 'Death successes / failures', 'Stable recovery deadline'], y)
    y = s.table('Wounds - each injury stays linked to its own Wound', 'wounds', [('Wound reference / gained', 140), ('Linked Injury', 130), ('Current penalty / source', 170), ('Treatment / removal', 100)], 3, y, 25)
    y = s.table('Conditions, temporary HP grant and other active effects', 'effects', [('Effect / grant reference', 130), ('Owner / source', 120), ('Amount / restriction', 140), ('Deadline / dependency / blocked recovery', 150)], 4, y, 31)
    y = s.row('concentration', ['Concentration / maintained source / next cost', 'Other pending effect / actual target / endpoint'], y, 28)
    y = s.row('turn_budget', ['Action / extra Action used', 'Bonus Action used', 'Reaction / refresh marker', 'Movement spent / remaining'], y)

    y = s.page_start('03  Equipment, carrying and attacks')
    y = s.note('Count each physical item once. Continue longer inventories using these same column headings.', y)
    y = s.table('Possessions - source profile, physical custody and current state', 'inventory', [('Item / profile / grade / fit', 142), ('Qty / contents / charges', 102), ('Owner / custodian / location', 138), ('lb / Load', 58), ('Condition / HP / access', 100)], 12, y, 27)
    y = s.row('money', ['Coins by denomination / count', 'Starting package OR wealth route', 'Purchases / transactions reference'], y)
    y = s.row('carrying', ['Body / carried weight (lb)', 'Total Load / capacity', 'Burden / current penalty', 'Container capacities / access'], y)
    y = s.table('Attack options - actual equipped item and acquired permission', 'attacks', [('Weapon / technique / source', 152), ('Hit bonus / DC', 88), ('Damage / type', 104), ('Range / reach', 82), ('Ammo / hands / special cost', 114)], 4, y, 27)
    y = s.row('equipment_state', ['Held / worn / free hands', 'Melded / inaccessible / pending placement'], y)

    y = s.page_start('04  Magic, class resources and companions')
    y = s.note('Choose the casting class for each cast. RP capacity never grants spell access.', y)
    y = s.row('magic_pool', ['Primary RP class / secondary contributor', 'Current RP / maximum RP', 'Dissonance / last spell / Refrain'], y)
    y = s.row('magic_limits', ['Casting class / ability / attack / DC / Limit', 'Known, prepared or book capacity / sources'], y)
    y = s.table('Spell and matrix record - retain distinct source permissions', 'spells', [('Spell identity / version', 135), ('Casting class / actual access', 125), ('Rank / price / components', 110), ('Known / prepared / book / family', 170)], 10, y, 23)
    y = s.table('Class pools, stock, recharge and limited uses', 'resources', [('Resource / acquired feature', 145), ('Current / maximum', 90), ('Spent allowance / scope', 135), ('Recovery / expiry / source', 170)], 5, y, 24)
    y = s.table('Companions and devices - use actual source profiles', 'companions', [('Identity / owner / profile', 160), ('HP / service / contents', 115), ('Command / channel / task', 135), ('Expiry / limits / source', 130)], 2, y, 30)

    y = s.page_start('05  Advancement, recovery and continuing records')
    y = s.note('Add levels in order. Keep spent resources when capacity changes; only actual recovery refills them.', y)
    y = s.table('Chronological advancement - retain the original HP die result before CON', 'advancement', [('Total / class level', 100), ('Class / entry order', 100), ('HD / stored HP base', 100), ('Automatic / chosen grants / ASI / source', 240)], 6, y, 24)
    y = s.row('hit_dice', ['Hit Dice owned by die size', 'Hit Dice spent / available by size', 'Maximum-HP adjustments / sources'], y)
    y = s.table('Actual rest and recovery events - no double-counted time or rewards', 'rests', [('Start / completion / event', 135), ('Type / eligibility / interruptions', 155), ('Benefits actually applied', 135), ('Remaining limits / blocks', 115)], 4, y, 25)
    y = s.table('Ongoing work, courses and treatment', 'projects', [('Activity / source / target', 155), ('Start / active time / endpoint', 140), ('Paid inputs / participant', 125), ('Result / remaining limit', 120)], 3, y, 25)
    y = s.row('records', ['Language worksheet / source-grant records', 'Craft work orders / recipe / inventory records'], y, 27)
    y = s.row('continuity', ['Story ties / goals / agreed table boundaries', 'Unresolved field / rule reference / next check'], y, 27)
    y = s.note('Keep the source of every nonordinary grant. Preserve original choices and actual transaction history.', y)
    y = s.note('Reference guides: Character Foundation; Core Resolution; Equipment; Class Resources; Language.', y)
    s.note('See CHARACTER_SHEET_PLAYTEST.md for current rule links and additional-record instructions.', y)
    s.finish()


if __name__ == '__main__':
    main()
