"""Preserve the original Faction runner and create its narrowly extended successor."""
from apply_di7_ap_as_01 import R


def main():
    old=R/'tools/validate_di7_faction_transactions.py'; new=R/'tools/validate_di7_faction_transactions_v2.py'
    assert not new.exists(); text=old.read_text(encoding='utf-8')
    text=text.replace('DI7_FACTION_TRANSACTIONS_CHECK.json','DI7_FACTION_TRANSACTIONS_V2_CHECK.json')
    text=text.replace("R / 'tools/validate_di7_faction_transactions.py'","R / 'tools/validate_di7_faction_transactions_v2.py'")
    marker='    bindings = sources.bindings + '
    assert text.count(marker)==1
    extra='''    for provider in ['Wizard', 'Cleric', 'Mirrorsage', 'Shaman']:
        m = make(provider, start=False)
        m.world['relations']['owner>reference'].update(visible=False, perceived=True,
            sourceFact='conditional-actual-governing-nonvisual-sense-perceives-this-creature; no new selectable sense authored')
        m.declare('owner', 'faction-omniscience', 'feed', {'target':'reference', 'faction':'guild'})
        check(provider+'/perceived-unseen-legal-paid-reference', m.actors['owner']['rp']==m.actors['owner']['maxRP']-17)
        m.resolve_faction('feed')
        check(provider+'/perceived-unseen-real-member-feed', bool(m.feeds) and len(entries(m))==4 and not m.world['relations']['owner>reference']['visible'])
        record('DI7-FACTION-REF-A/'+provider,m)
    m=make(start=False)
    m.world['relations']['owner>reference'].update(visible=False, perceived=False, sourceFact='conditional-suspected-location-only')
    reject('DI7-FACTION-REF-B/unseen-guess-no-payment',m,lambda:m.declare('owner','faction-omniscience','feed',{'target':'reference','faction':'guild'}))
    record('DI7-FACTION-REF-B',m)
    for label in ['false', 'protected', 'unrelated-scope']:
        m=make(start=False)
        m.world['relations']['owner>reference'].update(visible=False, perceived=True,
            sourceFact='conditional-actual-governing-nonvisual-creature-perception')
        if label=='false': m.information.data['facts']['actual-member']['publicFields']['value']['current']=False
        elif label=='protected': m.information.data['protections'].append(protect('reference','membership'))
        else: m.information.data['protections'].append(protect('reference','unrelated-private-thoughts'))
        m.declare('owner','faction-omniscience','feed',{'target':'reference','faction':'guild'})
        check(label+'/unseen-reference-hidden-test-after-payment',m.actors['owner']['rp']==31 and m.casts['feed']['status']=='pending')
        m.resolve_faction('feed')
        check(label+'/exact-membership-scope',bool(m.feeds)==(label=='unrelated-scope'))
        if label!='unrelated-scope': check(label+'/same-no-feed-diagnostic',m.casts['feed']['publicResult']=='No usable institutional reading.' and m.casts['feed']['refund']==0)
        record('DI7-FACTION-REF-C/'+label,m)
'''
    text=text.replace(marker,extra+marker)
    text=text.replace("'Original source says perceived reference and elsewhere visible creature; these histories use both, without resolving the perceived-but-unseen edge case.',", "'Perceived-versus-visible wording is settled by actual GPT DI7-FACTION-REFERENCE-01; underlying nonvisual sense acquisition remains a conditional premise.',")
    text=text.replace('Mass/Supreme geometry question is pending GPT; their payloads, Suggestion initiative clock and actual Shaman ordinary totem remain unfinished.', 'Mass/Supreme geometry source ruling is terminal and applied; payloads, Suggestion initiative clock and actual Shaman ordinary totem remain unfinished.')
    text=text.replace('and local visible/perceived reference geometry.', 'and local reference geometry. Additional unseen cases explicitly premise an existing governing nonvisual sense; no new sense is created.')
    text=text.replace("R / 'docs/mechanics/COMBAT_ACTION_PLAYTEST.md',", "A / 'DI7_FACTION_REFERENCE_RECEIVED.json', R / 'docs/mechanics/COMBAT_ACTION_PLAYTEST.md',")
    compile(text,str(new),'exec'); new.write_text(text,encoding='utf-8',newline='\n')
    print('Created separate V2 runner; historical runner unchanged.')


if __name__=='__main__': main()
