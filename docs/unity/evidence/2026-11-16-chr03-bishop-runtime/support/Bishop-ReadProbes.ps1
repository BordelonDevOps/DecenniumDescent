function Get-BishopProbeJson($session,$request) {
    $result=switch($request.op) {
        'query' {$session.QueryCastingCommand($request.seat,(New-TypedCommand $request))}
        'discover' {$session.DiscoverCastingCommands($request.seat,$request.actor)}
        'submit' {$session.Submit($request.seat,(New-TypedCommand $request))}
        'defender-presence' {$session.SubmitDefenderIntimidatingPresence([Decennium.Foundation.Laboratory.LaterDefenderController]::DefenderAuthority(),(New-TypedCommand $request))}
        default {throw "Unsupported read/denial probe operation: $($request.op)"}
    }
    ConvertTo-Json -InputObject $result -Depth 8 -Compress -EnumsAsStrings
}
function New-BishopProbes($snapshot,$markName) {
    $npc='TEST_ONLY.recovery-defender';$hero='TEST_ONLY.actor';$companion='TEST_ONLY.companion'
    foreach($seat in 'Player','FirstOpponent','RecoveryOpponent') {
        @{op='discover';seat=$seat;actor=$companion;evidenceRead=$markName+'.'+$seat+'.companion-discovery.json'}
        @{op='query';seat=$seat;id='probe.bishop-award.'+$snapshot.Revision;actor=$companion;revision=$snapshot.Revision;kind='AwardCharacterMilestone';target='TEST_ONLY.cleric3-recovery-care-departure';x=0;y=0;
            evidenceRead=$markName+'.'+$seat+'.bishop-award-query.json'}
        @{op='query';seat=$seat;id='probe.invocation.'+$snapshot.Revision;actor=$companion;revision=$snapshot.Revision;kind='UseDivineInvocation';target='';x=0;y=0;
            divineInvocation=@{targets=@($hero,$companion);cureTarget=$hero;curePreference='Frightened'};evidenceRead=$markName+'.'+$seat+'.invocation-query.json'}
        @{op='query';seat=$seat;id='probe.dispel.'+$snapshot.Revision;actor=$companion;revision=$snapshot.Revision;kind='CastKnownSpell';target='aura.unknown';x=0;y=0;
            spellCast=@{spellId='dispel-magic-lesser';focusItemId='TEST_ONLY.cleric-casting.holy-symbol';willingTarget=$false;electFocusedDc=$false};evidenceRead=$markName+'.'+$seat+'.dispel-query.json'}
        @{op='discover';seat=$seat;actor=$npc;evidenceRead=$markName+'.'+$seat+'.npc-discovery.json'}
        @{op='query';seat=$seat;id='probe.fear.'+$snapshot.Revision;actor=$npc;revision=$snapshot.Revision;kind='UseIntimidatingPresence';target='';x=0;y=0;
            intimidatingPresence=@{targets=@($hero,$companion)};evidenceRead=$markName+'.'+$seat+'.npc-query.json'}
        @{op='query';seat=$seat;id='probe.guidance.'+$snapshot.Revision;actor=$companion;revision=$snapshot.Revision;kind='CastKnownSpell';target=$companion;x=0;y=0;
            spellCast=@{spellId='guidance';focusItemId='';willingTarget=$true;electFocusedDc=$false};evidenceRead=$markName+'.'+$seat+'.party-query.json'}
    }
    foreach($seat in 'Player','FirstOpponent') {
        @{op='submit';seat=$seat;id='probe.denied.'+$snapshot.Revision;actor=$npc;revision=$snapshot.Revision;kind='UseIntimidatingPresence';target='';x=0;y=0;
            intimidatingPresence=@{targets=@($hero)};evidenceRead=$markName+'.'+$seat+'.npc-denial.json';expectedResponse='NotAuthorized'}
    }
    @{op='defender-presence';id='probe.old-controller.'+$snapshot.Revision;actor=$npc;revision=$snapshot.Revision;kind='UseIntimidatingPresence';target='';x=0;y=0;
        intimidatingPresence=@{targets=@($hero)};evidenceRead=$markName+'.old-controller.npc-denial.json';expectedResponse='NotAuthorized'}
    # A real completed NPC Presence command supports an owner duplicate and two
    # before-disclosure denial probes. Recreate its exact explicit payload.
    # CommandReceipt does not expose actor directly in every supported assembly.
    $presence=$snapshot.Receipts|Where-Object {$_.Principal-eq'TEST_ONLY.post-recovery-defender.v1'}|ForEach-Object {
        [Decennium.Foundation.CommandHistory]::Read($_)
    }|Where-Object Kind -eq 'UseIntimidatingPresence'|Select-Object -Last 1
    if($presence) {
        foreach($seat in 'Player','FirstOpponent','RecoveryOpponent') {
            @{op='submit';seat=$seat;id=$presence.Id;actor=$npc;revision=$presence.ExpectedRevision;kind='UseIntimidatingPresence';target=$presence.Target;x=$presence.X;y=$presence.Y;
                intimidatingPresence=@{targets=@($presence.IntimidatingPresence.TargetIds)};
                evidenceRead=$markName+'.'+$seat+'.npc-duplicate.json';expectedResponse=$(if($seat-eq'RecoveryOpponent'){'Duplicate'}else{'NotAuthorized'})}
        }
    }
    $invocation=$snapshot.BishopEntry.Invocations|Select-Object -Last 1
    if($invocation) {
        $original=$snapshot.Receipts|Where-Object Id -eq $invocation.CommandId|Select-Object -First 1
        $command=[Decennium.Foundation.CommandHistory]::Read($original)
        foreach($seat in 'Player','FirstOpponent','RecoveryOpponent') {
            @{op='submit';seat=$seat;id=$command.Id;actor=$command.Actor;revision=$command.ExpectedRevision;kind='UseDivineInvocation';target='';x=0;y=0;
                divineInvocation=@{targets=@($command.DivineInvocation.TargetIds);cureTarget=$command.DivineInvocation.CureTargetId;curePreference=$command.DivineInvocation.CurePreference.ToString()};
                evidenceRead=$markName+'.'+$seat+'.invocation-duplicate.json';expectedResponse=$(if($seat-eq'Player'){'Duplicate'}else{'NotAuthorized'})}
        }
    }
}
