function New-TypedCommand($request){
    # Independent constructor dispatch from retained typed JSON: no receipt reader,
    # snapshot reader, console parser or private rule resolver participates here.
    $inventory=$null;$combat=$null;$mining=$null;$presence=$null;$advancement=$null;$healingRite=$null
    $spellCast=$null;$guidance=$null;$sanctuaryResponse=$null;$invocation=$null
    if($request['inventory']){$i=$request.inventory;$inventory=[Decennium.Foundation.InventoryRequest]::new(
        [Decennium.Foundation.RuleQuantity]::new($i.numerator,$i.denominator),$i.destination,$i.handling)}
    if($request['combat']){$c=$request.combat;$combat=[Decennium.Foundation.CombatRequest]::new(
        $c.turn,($c.weapon ?? ''),($c.stance ?? 0),($c.knockout ?? 'OrdinaryOutcome'),
        ($c.choice ?? $false),($c.press ?? 'ArmOrReplace'),($c.feature ?? ''))}
    if($request['mining']){$m=$request.mining;$mining=[Decennium.Foundation.MiningSelectionRequest]::new(
        $m.version,[string[]]$m.categories,$m.ability,$m.hurried,$m.failureVictim,$m.criticalRecovery,$m.assistant)}
    if($request['intimidatingPresence']){$presence=[Decennium.Foundation.IntimidatingPresenceRequest]::new([string[]]$request.intimidatingPresence.targets)}
    if($request['advancement']){$a=$request.advancement;$advancement=[Decennium.Foundation.CharacterAdvancementRequest]::new([string[]]$a.features,$a.invocationPath,$a.earnedSpell)}
    if($request['healingRite']){$healingRite=[Decennium.Foundation.HealingRiteRequest]::new($request.healingRite.curePreference)}
    if($request['spellCast']){$a=$request.spellCast;$spellCast=[Decennium.Foundation.SpellCastRequest]::new($a.spellId,$a.focusItemId,$a.willingTarget,$a.electFocusedDc)}
    if($request['guidance']){$guidance=[Decennium.Foundation.GuidanceChoice]::new($request.guidance.effectId)}
    if($request['sanctuaryResponse']){$a=$request.sanctuaryResponse;$sanctuaryResponse=[Decennium.Foundation.SanctuaryResponseRequest]::new($a.kind,$a.targetId)}
    if($request['divineInvocation']){$a=$request.divineInvocation;$invocation=[Decennium.Foundation.DivineInvocationRequest]::new([string[]]$a.targets,($a.cureTarget ?? ''),($a.curePreference ?? 'None'))}
    [Decennium.Foundation.Command]::new($request.id,$request.actor,$request.revision,$request.kind,$request.target,$request.x,$request.y,
        $inventory,$combat,$advancement,$null,'None',$null,$null,$null,$null,$mining,$null,$null,$presence,$healingRite,$spellCast,$guidance,$sanctuaryResponse,$invocation)
}
