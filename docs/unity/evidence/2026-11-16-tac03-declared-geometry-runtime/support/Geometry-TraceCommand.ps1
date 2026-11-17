function ConvertTo-GeometryRequest($receipt) {
    # Trace preparation only. Independent typed execution reconstructs the retained
    # JSON through the existing public constructor adapter, not this receipt reader.
    $c=[Decennium.Foundation.CommandHistory]::Read($receipt)
    $r=@{op='submit';id=$c.Id;actor=$c.Actor;revision=$c.ExpectedRevision;kind=$c.Kind.ToString();target=$c.Target;x=$c.X;y=$c.Y;
        seat=$(if($c.Actor-eq'TEST_ONLY.third-combatant'){'FirstOpponent'}elseif($c.Actor-eq'TEST_ONLY.recovery-defender'){'RecoveryOpponent'}else{'Player'})}
    if($receipt.Principal-eq'TEST_ONLY.tac10-later-defender.v1'-and$c.Id.StartsWith('tac10.')){$r.op='auto';return $r}
    if($c.Kind-eq'AdvanceClock'){$r.op='clock'}
    elseif($c.Kind-eq'EndFixedEncounter'){$r.op='close'}
    elseif($c.Kind-eq'UseIntimidatingPresence'-and$c.Actor-eq'TEST_ONLY.later-defender'){$r.op='defender-presence'}
    elseif($c.Kind-eq'RespondSanctuary'-and$receipt.Principal-eq'TEST_ONLY.tac10-later-defender.v1'){$r.op='defender-sanctuary'}
    if($c.Inventory){$v=$c.Inventory;$r.inventory=@{numerator=$v.Amount.Numerator;denominator=$v.Amount.Denominator;destination=$v.Destination;handling=$v.Handling.ToString()}}
    if($c.Combat){$v=$c.Combat;$r.combat=@{turn=$v.TurnId;weapon=$v.WeaponId;stance=$v.Stance;knockout=$v.Knockout.ToString();choice=$v.Choice;press=$v.PressInstruction.ToString()}}
    if($c.MiningSelection){$v=$c.MiningSelection;$r.mining=@{version=$v.DepositVersionId;categories=@($v.CategoryIds);ability=$v.Ability.ToString();hurried=$v.Hurried;failureVictim=$v.FailureVictimPreference;criticalRecovery=$v.CriticalRecoveryPreference;assistant=$v.AssistantId}}
    if($c.Advancement){$v=$c.Advancement;$r.advancement=@{features=@($v.FeatureIds);invocationPath=$v.InvocationPath.ToString();earnedSpell=$v.EarnedSpell}}
    if($c.IntimidatingPresence){$r.intimidatingPresence=@{targets=@($c.IntimidatingPresence.TargetIds)}}
    if($c.HealingRite){$r.healingRite=@{curePreference=$c.HealingRite.CurePreference.ToString()}}
    if($c.SpellCast){$v=$c.SpellCast;$r.spellCast=@{spellId=$v.SpellId;focusItemId=$v.FocusItemId;willingTarget=$v.WillingTarget;electFocusedDc=$v.ElectFocusedDc}}
    if($c.Guidance){$r.guidance=@{effectId=$c.Guidance.EffectId}}
    if($c.SanctuaryResponse){$r.sanctuaryResponse=@{kind=$c.SanctuaryResponse.Kind.ToString();targetId=$c.SanctuaryResponse.TargetId}}
    if($c.DivineInvocation){$v=$c.DivineInvocation;$r.divineInvocation=@{targets=@($v.TargetIds);cureTarget=$v.CureTargetId;curePreference=$v.CurePreference.ToString()}}
    # Reject a lossy export, including any future payload not mapped above.
    $roundtrip=New-TypedCommand $r
    $fingerprint=$roundtrip.GetType().GetProperty('Fingerprint',[Reflection.BindingFlags]'Instance,NonPublic').GetValue($roundtrip)
    if($fingerprint-cne$receipt.Fingerprint){throw "Lossy trace export at $($receipt.Revision)"}
    return $r
}
