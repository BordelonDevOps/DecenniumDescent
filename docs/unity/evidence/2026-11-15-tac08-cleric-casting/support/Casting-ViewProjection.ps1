function Get-CastingViewJson($session,$seat) {
    # Compare the documented console projection of the public seat-filtered DTO.
    # These exclusions are the existing adapter's profile fields, not game-state access.
    $view=$session.View($seat)
    $targets=[ordered]@{}
    foreach($target in $view.KnownTargets.GetEnumerator()){$targets[$target.Key.ToString()]=$target.Value}
    $view=$view|Select-Object -Property * -ExcludeProperty KnownTargets,FleshWarden,ShortRest
    $view|Add-Member -NotePropertyName KnownTargets -NotePropertyValue $targets
    $view.Actors=@($view.Actors|Select-Object -Property * -ExcludeProperty TemporaryHp,TemporaryHpUntil)
    ConvertTo-Json -InputObject $view -Depth 8 -Compress -EnumsAsStrings
}
