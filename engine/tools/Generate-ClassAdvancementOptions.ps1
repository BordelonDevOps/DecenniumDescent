param(
    [string]$RepositoryRoot = (Join-Path $PSScriptRoot '../..'),
    [string]$OutputPath = (Join-Path $PSScriptRoot '../com.decennium.foundation/Laboratory/Model/ClassAdvancementOptionCatalog.cs')
)
$ErrorActionPreference = 'Stop'
$RepositoryRoot = [IO.Path]::GetFullPath($RepositoryRoot)
$OutputPath = [IO.Path]::GetFullPath($OutputPath)
$sourceRevision = '46a4d52728ee6956f0bebcb5d2103ffd5bc67ba4'
$manifestPath = 'DescentReviewChanges/ReviewBible/data/public/class_playtests/manifest.json'

function Resolve-PinnedBlob([string]$RelativePath) {
    $spec = $sourceRevision + ':' + $RelativePath
    $blob = (git -C $RepositoryRoot rev-parse --verify $spec).Trim()
    if ($LASTEXITCODE -ne 0 -or $blob -notmatch '^[0-9a-f]{40}$') { throw ('Could not resolve pinned source ' + $spec) }
    return $blob
}

function Read-GitBlob([string]$Blob) {
    $start = [Diagnostics.ProcessStartInfo]::new()
    $start.FileName = 'git'
    $start.Arguments = '-C "' + $RepositoryRoot + '" cat-file blob ' + $Blob
    $start.UseShellExecute = $false
    $start.RedirectStandardOutput = $true
    $start.RedirectStandardError = $true
    $process = [Diagnostics.Process]::new()
    $process.StartInfo = $start
    if (-not $process.Start()) { throw ('Could not start git cat-file for ' + $Blob) }
    $stream = [IO.MemoryStream]::new()
    $process.StandardOutput.BaseStream.CopyTo($stream)
    $errorText = $process.StandardError.ReadToEnd()
    $process.WaitForExit()
    if ($process.ExitCode -ne 0) { throw ('git cat-file failed for ' + $Blob + ': ' + $errorText) }
    $bytes = $stream.ToArray()
    $stream.Dispose()
    $process.Dispose()
    return ,$bytes
}

function Text-Field($Value) {
    if ($null -eq $Value) { return '' }
    return [string]$Value
}

function Json-Field($Object,[string]$Name) {
    $property = $Object.PSObject.Properties[$Name]
    if ($null -eq $property) { return 'null' }
    return ConvertTo-Json -InputObject $property.Value -Depth 32 -Compress
}

function Base64-Text([string]$Value) {
    return [Convert]::ToBase64String([Text.UTF8Encoding]::new($false).GetBytes($Value))
}

function CSharp-Literal([string]$Value) {
    return '"' + $Value.Replace('\','\\').Replace('"','\"').Replace("`r",'\r').Replace("`n",'\n') + '"'
}

$utf8 = [Text.UTF8Encoding]::new($false,$true)
$manifestBlob = Resolve-PinnedBlob $manifestPath
$manifest = $utf8.GetString((Read-GitBlob $manifestBlob)) | ConvertFrom-Json
if ($manifest.classes.Count -ne 17) { throw 'The pinned class manifest does not contain 17 classes.' }
$rows = [Collections.Generic.List[string]]::new()
$ids = [Collections.Generic.HashSet[string]]::new([StringComparer]::Ordinal)
foreach ($entry in $manifest.classes) {
    $slug = ($entry.class -replace ' ','-').ToLowerInvariant()
    $relative = if ($entry.class -eq 'Bard') {
        'DescentReviewChanges/ReviewBible/data/public/Decennium_Descent_Bard_Playtest_v0_1.json'
    } else {
        'DescentReviewChanges/ReviewBible/data/public/class_playtests/' + $slug + '.json'
    }
    $blob = Resolve-PinnedBlob $relative
    $source = $utf8.GetString((Read-GitBlob $blob)) | ConvertFrom-Json
    for ($i=0; $i -lt @($source.cards).Count; $i++) {
        $card = $source.cards[$i]
        $kindProperty = if ($null -ne $card.PSObject.Properties['sourceKind']) { 'sourceKind' }
            elseif ($null -ne $card.PSObject.Properties['kind']) { 'kind' } else { '' }
        $kindValue = if ($kindProperty -eq '') { '' } else { Text-Field $card.$kindProperty }
        $minimumLevel = if ($null -eq $card.minimumClassLevel) { 1 } else { [int]$card.minimumClassLevel }
        if ($minimumLevel -lt 1 -or $minimumLevel -gt 20) { throw ('Invalid minimumClassLevel for ' + $card.id) }
        $key = $entry.class + '|' + (Text-Field $card.id)
        if (-not $ids.Add($key)) { throw ('Duplicate class card ID ' + $key) }
        $simple = @(
            (Text-Field $entry.class),(Text-Field $card.id),(Text-Field $card.name),(Text-Field $card.band),
            (Text-Field $card.path),$minimumLevel.ToString([Globalization.CultureInfo]::InvariantCulture),
            (Text-Field $card.acquisition),$kindProperty,$kindValue,(Text-Field $card.activation),
            (Base64-Text (Json-Field $card 'prerequisite')),(Base64-Text (Json-Field $card 'prerequisites')),
            (Text-Field $card.designStatus),$relative,('/cards/' + $i.ToString([Globalization.CultureInfo]::InvariantCulture))
        )
        foreach ($requiredIndex in @(0,1,2,3,6,7,8,9,12,13,14)) {
            if ($simple[$requiredIndex] -eq '') { throw ('Required class-card field is empty at ' + $relative + '/cards/' + $i) }
        }
        if ($simple.Where({ $_.Contains('|') }).Count -gt 0) { throw ('Unescaped card field delimiter at ' + $relative + '/cards/' + $i) }
        $rows.Add(($simple -join '|'))
    }
}
if ($rows.Count -ne 1223) { throw ('Expected 1,223 pinned class cards; found ' + $rows.Count) }

$lines = [Collections.Generic.List[string]]::new()
@(
    'using System;',
    'using System.Collections.Generic;',
    'using System.Collections.ObjectModel;',
    'using System.Globalization;',
    'using System.Linq;',
    'using System.Text;',
    '',
    'namespace Decennium.Foundation.Laboratory',
    '{',
    '    /// <summary>Source projection for authored class-card acquisition options. It preserves source prerequisites and paths without claiming that the runtime resolves them.</summary>',
    '    public sealed class ClassAdvancementOption',
    '    {',
    '        public string ClassName { get; }',
    '        public string Id { get; }',
    '        public string Name { get; }',
    '        public string Band { get; }',
    '        public string Path { get; }',
    '        public int MinimumClassLevel { get; }',
    '        public string Acquisition { get; }',
    '        public string KindProperty { get; }',
    '        public string Kind { get; }',
    '        public string Activation { get; }',
    '        public string PrerequisiteJson { get; }',
    '        public string PrerequisitesJson { get; }',
    '        public string DesignStatus { get; }',
    '        public string SourcePath { get; }',
    '        public string SourceLocator { get; }',
    '        public bool HasPathConstraint => Path.Length != 0;',
    '        public bool HasDeclaredPrerequisite => !NoConstraint(PrerequisiteJson) || !NoConstraint(PrerequisitesJson);',
    '        internal ClassAdvancementOption(string className,string id,string name,string band,string path,int minimumClassLevel,string acquisition,',
    '            string kindProperty,string kind,string activation,string prerequisiteJson,string prerequisitesJson,string designStatus,string sourcePath,string sourceLocator)',
    '        {',
    '            if(string.IsNullOrEmpty(className)||string.IsNullOrEmpty(id)||string.IsNullOrEmpty(name)||string.IsNullOrEmpty(band)',
    '                ||minimumClassLevel<1||minimumClassLevel>20||string.IsNullOrEmpty(acquisition)||string.IsNullOrEmpty(kindProperty)',
    '                ||string.IsNullOrEmpty(kind)||string.IsNullOrEmpty(activation)||prerequisiteJson==null||prerequisitesJson==null',
    '                ||string.IsNullOrEmpty(designStatus)||string.IsNullOrEmpty(sourcePath)||string.IsNullOrEmpty(sourceLocator))',
    '                throw new ArgumentException("Invalid class advancement option.");',
    '            ClassName=className;Id=id;Name=name;Band=band;Path=path??"";MinimumClassLevel=minimumClassLevel;Acquisition=acquisition;',
    '            KindProperty=kindProperty;Kind=kind;Activation=activation;PrerequisiteJson=prerequisiteJson;PrerequisitesJson=prerequisitesJson;',
    '            DesignStatus=designStatus;SourcePath=sourcePath;SourceLocator=sourceLocator;',
    '        }',
    '        private static bool NoConstraint(string json)=>json=="null"||json=="\"\""||json=="[]"||json=="{}";',
    '    }',
    '',
    '    /// <summary>Finite class-card source projection at the same pinned revision as the class-level schedule catalog.</summary>',
    '    public static class ClassAdvancementOptionCatalog',
    '    {',
    '        public const string SourceRevision=ClassAdvancementScheduleCatalog.SourceRevision;',
    '        private static readonly UTF8Encoding Utf8=new UTF8Encoding(false,true);',
    '        private static readonly string[] EncodedOptions=new string[] {'
) | ForEach-Object { $lines.Add($_) }
for ($i=0; $i -lt $rows.Count; $i++) {
    $suffix = if ($i -lt $rows.Count - 1) { ',' } else { '' }
    $lines.Add('            ' + (CSharp-Literal $rows[$i]) + $suffix)
}
@(
    '        };',
    '        private static readonly ReadOnlyCollection<ClassAdvancementOption> options;',
    '        private static readonly Dictionary<string,ClassAdvancementOption> byId;',
    '        public static ReadOnlyCollection<ClassAdvancementOption> Options=>options;',
    '        static ClassAdvancementOptionCatalog()',
    '        {',
    '            var values=new List<ClassAdvancementOption>(EncodedOptions.Length);',
    '            foreach(var line in EncodedOptions) {',
    '                var f=line.Split(''|'');if(f.Length!=15)throw new InvalidOperationException("Invalid encoded class-card option.");',
    '                string Decode(string value)=>Utf8.GetString(Convert.FromBase64String(value));',
    '                values.Add(new ClassAdvancementOption(f[0],f[1],f[2],f[3],f[4],int.Parse(f[5],CultureInfo.InvariantCulture),f[6],f[7],f[8],f[9],',
    '                    Decode(f[10]),Decode(f[11]),f[12],f[13],f[14]));',
    '            }',
    '            if(values.Count!=1223||values.Select(x=>x.ClassName+"|"+x.Id).Distinct(StringComparer.Ordinal).Count()!=values.Count)',
    '                throw new InvalidOperationException("Pinned class-card option catalog is incomplete or duplicated.");',
    '            options=Array.AsReadOnly(values.ToArray());',
    '            byId=values.ToDictionary(x=>x.ClassName+"|"+x.Id,StringComparer.Ordinal);',
    '        }',
    '        public static ClassAdvancementOption Get(string className,string id)',
    '        {',
    '            if(className==null)throw new ArgumentNullException(nameof(className));',
    '            if(id==null)throw new ArgumentNullException(nameof(id));',
    '            return byId.TryGetValue(className+"|"+id,out var option)?option:null;',
    '        }',
    '        /// <summary>Returns band/level/selection candidates only. Path and prerequisite fields still require rule evaluation.</summary>',
    '        public static ReadOnlyCollection<ClassAdvancementOption> Candidates(ClassAdvancementScheduleRow row)',
    '        {',
    '            if(row==null)throw new ArgumentNullException(nameof(row));',
    '            if(row.Kind!=ClassAdvancementScheduleKind.Structured)return Array.AsReadOnly(Array.Empty<ClassAdvancementOption>());',
    '            var found=options.Where(x=>x.ClassName==row.ClassName&&x.Acquisition=="selection"&&x.MinimumClassLevel<=row.ClassLevel&&row.Bands.Contains(x.Band,StringComparer.Ordinal)).ToArray();',
    '            return Array.AsReadOnly(found);',
    '        }',
    '    }',
    '}'
) | ForEach-Object { $lines.Add($_) }

$directory = Split-Path -Parent $OutputPath
New-Item -ItemType Directory -Force -Path $directory | Out-Null
[IO.File]::WriteAllText($OutputPath,([string]::Join("`r`n",$lines) + "`r`n"),[Text.UTF8Encoding]::new($false))
Write-Output ('Generated ' + $rows.Count + ' class-card acquisition options from ' + $sourceRevision + ': ' + $OutputPath)
