"""Bounded reference models for FEAT327 authoring acceptance.

These functions execute only the named local state transition. They are not the
game application, a complete feat interpreter, or proof of campaign premises.
Times in ExpeditionLedger are elapsed hours on the supplied canonical calendar.
"""
from dataclasses import dataclass, field
from fractions import Fraction
from math import ceil, floor


@dataclass
class ExpeditionLedger:
    now: int = 0
    strain: int = 0
    food_pending: int = 0
    sleep_pending: int = 0
    debt: bool = False
    deadline: int | None = None
    operative: bool = True
    assessed: set = field(default_factory=set)
    unsupported_days: set = field(default_factory=set)
    history: list = field(default_factory=list)

    def penalty(self, cause, event):
        if event in self.assessed:return False
        self.assessed.add(event)
        key={'food':'food_pending','sleep':'sleep_pending'}[cause]
        old=getattr(self,key)
        if self.operative:
            setattr(self,key,1-old);gain=old
        else:
            setattr(self,key,0);gain=1
        self.strain+=gain
        self.history.append({'event':event,'at':self.now,'cause':cause,'strain':gain})
        return True

    def advance(self,t):
        if t<self.now:raise ValueError('Cannot rewind the clock')
        if self.debt and self.deadline is not None and self.deadline<=t:
            self.now=self.deadline;self.penalty('sleep',f'debt-due:{self.deadline}')
        self.now=t

    def miss_rest(self,t,second_following_watch_end,event):
        self.advance(t)
        if ('missed',event) in self.assessed:raise ValueError('Same missed rest already processed')
        if second_following_watch_end<=t:raise ValueError('Invalid supplied canonical deadline')
        self.assessed.add(('missed',event))
        if self.debt:self.penalty('sleep','missed-rest:'+event)
        self.debt=True;self.deadline=second_following_watch_end

    def settle_day(self,t,food_ok,water_ok,other_ok=True):
        self.advance(t)
        if t%24:raise ValueError('Not a canonical day endpoint')
        event='day:'+str(t)
        if event in self.assessed:raise ValueError('Daily requirements already settled')
        self.assessed.add(event)
        if food_ok and water_ok:self.food_pending=0
        if not (food_ok and water_ok and other_ok):self.unsupported_days.add(t)
        if not other_ok:
            self.strain+=1
            self.history.append({'event':event,'at':t,'cause':'other-logistics','strain':1})
        elif not (food_ok and water_ok):self.penalty('food','food:'+str(t))

    def safe_rest(self,start,end,safe,uninterrupted):
        if not safe or not uninterrupted or end-start<8:raise ValueError('Not a qualifying eight-hour rest')
        self.advance(end)
        self.debt=False;self.deadline=None;self.sleep_pending=0
        # The caller's separate beneficial-rest ledger owns all resource rewards.

    def snapshot(self):
        return {'time':self.now,'strain':self.strain,'food':self.food_pending,'sleep':self.sleep_pending,
                'debt':self.debt,'deadline':self.deadline,'unsupported':sorted(self.unsupported_days)}


@dataclass
class RestRewards:
    last_long: int | None = None
    short_count: int = 0
    completed: set = field(default_factory=set)

    def claim(self,identity,end,kind,qualifies=True):
        if identity in self.completed or not qualifies:return False
        self.completed.add(identity)
        if kind=='long':
            if self.last_long is not None and end-self.last_long<24:return False
            self.last_long=end;self.short_count=0;return True
        if kind=='short':
            if self.short_count>=2:return False
            self.short_count+=1;return True
        raise ValueError(kind)


def feat_class_bonus(feat_rows,class_bonuses):
    by_id={}
    for identity,value in feat_rows:by_id[identity]=max(value,by_id.get(identity,value))
    return sum(by_id.values())+max([0]+class_bonuses)


def controlled_speed(base,records,hard_zero=False):
    if hard_zero:return 0
    values=[base]
    for r in records:
        if r.get('active',True):
            values.append(max(0,base-r['subtract']) if 'subtract' in r else floor(base*Fraction(*r['factor'])))
    return min(values)


def percent_packet(native,percentages):
    """Input is already critical-adjusted native typed damage, excluding riders."""
    if any(x<0 for x in native):raise ValueError('Negative native damage')
    total=sum(native);result=native[:]
    for numerator,denominator in percentages:
        amount=floor(total*Fraction(numerator,denominator))
        shares=[Fraction(amount*x,total) if total else Fraction(0) for x in native]
        add=[floor(x) for x in shares]
        order=sorted(range(len(native)),key=lambda i:(-(shares[i]-add[i]),i))
        for i in order[:amount-sum(add)]:add[i]+=1
        result=[a+b for a,b in zip(result,add)]
    return result


def actual_damage(normal_hp,temp_hp,resolved_damage):
    if min(normal_hp,temp_hp,resolved_damage)<0:raise ValueError('Invalid damage state')
    absorbed=min(temp_hp,resolved_damage);lost=min(normal_hp,resolved_damage-absorbed)
    return {'normalHP':normal_hp-lost,'tempHP':temp_hp-absorbed,'actualDamage':absorbed+lost,'overkill':resolved_damage-absorbed-lost}


@dataclass
class ResourceLedger:
    current: int
    maximum: int
    payments: dict = field(default_factory=dict)
    refunds: dict = field(default_factory=dict)
    def pay(self,root,amount):
        if amount<0 or amount>self.current or root in self.payments:raise ValueError('Illegal resource payment')
        self.current-=amount;self.payments[root]=amount
    def refund(self,root,requested):
        remaining=self.payments.get(root,0)-self.refunds.get(root,0)
        amount=max(0,min(requested,remaining,self.maximum-self.current))
        self.current+=amount;self.refunds[root]=self.refunds.get(root,0)+amount
        return amount
    def capacity(self,maximum):
        if maximum<0:raise ValueError('Negative capacity')
        self.maximum=maximum;self.current=min(self.current,maximum)


@dataclass
class CaltropField:
    field_pieces: set = field(default_factory=lambda:set(range(20)))
    bag: set = field(default_factory=set)
    embedded: dict = field(default_factory=dict)
    entries: set = field(default_factory=set)
    def enter(self,event,creature,saved,half_speed=False):
        if event in self.entries:raise ValueError('Replayed entry')
        self.entries.add(event)
        if not self.field_pieces:return 'no-field'
        if half_speed:return 'avoided'
        if saved:return 'saved'
        piece=min(self.field_pieces);self.field_pieces.remove(piece)
        self.embedded.setdefault(creature,set()).add(piece)
        return 'piercing1-stop-and-slow'
    def collect(self,minutes,safe,unoccupied):
        if minutes<1 or not safe or not unoccupied:raise ValueError('No safe collection')
        self.bag.update(self.field_pieces);self.field_pieces.clear()
    def replacement_can_arm(self):return not self.field_pieces
    def total_pieces(self):
        parts=[self.field_pieces,self.bag,*self.embedded.values()]
        if sum(len(x) for x in parts)!=len(set().union(*parts)):raise ValueError('Duplicated physical piece')
        return sum(len(x) for x in parts)


@dataclass
class CommandLedger:
    phases: dict = field(default_factory=dict)
    commands: set = field(default_factory=set)
    offenses: set = field(default_factory=set)
    def elect_phase(self,body,round_id,controller,route):
        key=(body,round_id);value=(controller,route)
        if key in self.phases and self.phases[key]!=value:raise ValueError('Second phase for same body')
        self.phases[key]=value
    def command(self,owner,round_id,bodies,action,recipient_cap,channel=True,offensive_body=None):
        key=(owner,round_id)
        if not channel or key in self.commands or not bodies or len(set(bodies))!=len(bodies) or len(bodies)>recipient_cap:
            raise ValueError('Illegal shared command')
        self.commands.add(key)
        if action=='Attack':
            if offensive_body not in bodies or key in self.offenses:raise ValueError('No offensive allowance')
            self.offenses.add(key)
            return {b:('Attack' if b==offensive_body else 'defensive/Dodge') for b in bodies}
        return {b:action for b in bodies}
    def trap_attack(self,owner,round_id,actual_entry):
        key=(owner,round_id)
        if not actual_entry or key in self.offenses:return False
        self.offenses.add(key);return True


def self_ally_move(selected,commander,reactions,speed):
    if len(selected)>3 or len(set(selected))!=len(selected):raise ValueError('Invalid recipient roster')
    result={}
    for target in selected:
        if reactions.get(target,0)>0:
            reactions[target]-=1;result[target]=floor(speed[target]/2)
        else:result[target]=0
    return result


def slayer_attack_reaction(dragon,perceived,target_self,melee,breath,before_roll,reaction):
    return bool(dragon and perceived and target_self and (melee or breath) and before_roll and reaction)


def whole_repair_bonus(total_minutes,inside_minutes,beneficial_rest,authorized,base_restored,pb,current,maximum):
    eligible=authorized and beneficial_rest and total_minutes<=30 and inside_minutes==total_minutes
    bonus=min(pb,max(0,maximum-current-base_restored)) if eligible else 0
    return {'restException':eligible,'featExtraHP':bonus}


def assay(false_face,fees):
    total=max(Fraction(false_face,10),Fraction(fees))
    return {'total':total,'fees':Fraction(fees),'additional':max(Fraction(0),total-fees)}


def copy_profile(original_rank,native_magnitude,rolled,owned_ceiling):
    if original_rank is None or native_magnitude is None or original_rank<0 or native_magnitude<0:raise ValueError('Missing actual observed source')
    q=0 if original_rank==0 else max(1,original_rank//2)
    if owned_ceiling is None or q>owned_ceiling:raise ValueError('No actual rank permission')
    return {'rank':q,'dice':q+1,'magnitude':min(rolled,native_magnitude//2),
            'copyDerived':True,'canCapture':False,'canGenerateClassResource':False,'newPaidCast':True}


def ritual_seconds(base,additional,quick=False,channel=False):
    if min(base,additional)<0:raise ValueError('Negative labor')
    adjusted=min(additional,max(300,ceil(Fraction(additional,2)))) if quick else additional
    total=base+adjusted
    return min(total,max(base+300,ceil(Fraction(total*3,4)))) if channel else total


@dataclass
class Spellweave:
    identity: str | None
    deadline: int
    def commit_next(self,now,eligible_channel,countered=False):
        if self.identity is None or now>=self.deadline:return {'attached':False,'consumed':False,'benefit':False}
        identity=self.identity;self.identity=None
        return {'attached':True,'consumed':True,'benefit':not countered and eligible_channel,'identity':identity,'requiresNewConcentration':False}


def invisible_before_event(active,kind,legal=True):
    ends=active and legal and kind in ('Action','Bonus Action','Reaction')
    return {'activeAfter':active and not ends,'order':['end-invisibility','commit'] if ends else ['event']}


def entire_darkness(cells):return bool(cells) and all(c=='dark' for c in cells)


def mutation_state(level,equipped_vital,active_vital,temporary_active_exception=False):
    slots=1+(level>=5)+(level>=13)+(level>=20)
    if len(set(equipped_vital))!=len(equipped_vital) or len(equipped_vital)>slots:raise ValueError('Impossible equipped mutation snapshot')
    if not set(active_vital)<=set(equipped_vital):raise ValueError('Unowned active mutation')
    if len(active_vital)>2 and not temporary_active_exception:raise ValueError('No active-count exception')
    return {'slots':slots,'acquisitionGate':level>=8 and len(equipped_vital)>=3,'livingFortressOperative':level>=8 and len(set(active_vital))>=3}


def terror_ready(records):
    return len({x['creature'] for x in records if x['ownWarriorSource'] and x['inRange'] and x['lineOfEffect'] and x['active'] and not x['suppressed'] and x['condition'] in {'Shaken','Frightened','Disoriented'}})>=2


@dataclass
class UndyingEpisode:
    hp: int
    alive: bool = True
    available: bool = True
    pending: str | None = None
    wounds: int = 0
    prone: bool = True
    def register(self,identity,previous_hp,incapacity_from_drop):
        if not self.alive or self.hp!=0 or previous_hp<=0 or not self.available:return False
        # This exact feat permits registration despite this drop's incapacity.
        self.pending=identity;self.available=False;return True
    def heal(self,amount):
        if self.alive and amount>0:self.hp+=amount;self.pending=None
    def die(self):self.alive=False;self.pending=None
    def resolve(self,identity,hp_gain_blocked=False):
        if self.pending!=identity:return False
        self.pending=None
        if not self.alive or self.hp!=0 or hp_gain_blocked:return False
        self.hp=1;return True


def consume_hemocraft(record,owner,now):
    if record['owner']!=owner or record['ended'] or now>=record['expires']:raise ValueError('No actual consumable own record')
    record['ended']=True
    return True  # Its explicit exception includes suppressed unexpired records.
