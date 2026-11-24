param(
    [Parameter(Mandatory)][string[]]$Sources,
    [Parameter(Mandatory)][string[]]$References,
    [Parameter(Mandatory)][string[]]$CompilerOptions,
    [Parameter(Mandatory)][string]$OutputAssembly
)
$ErrorActionPreference = 'Stop'
# Add-Type chooses a random assembly identity even when OutputAssembly has a fixed
# filename. Compile with the actual package identity so friend access is tested.
if (-not ('Decennium.HeadlessCompiler' -as [type])) {
    $compilerReferences = @(Get-ChildItem -LiteralPath (Join-Path $PSHOME 'ref') -Filter '*.dll' | ForEach-Object FullName)
    $compilerReferences += Join-Path $PSHOME 'Microsoft.CodeAnalysis.dll'
    $compilerReferences += Join-Path $PSHOME 'Microsoft.CodeAnalysis.CSharp.dll'
    # Only this host adapter references PowerShell's bundled Roslyn (built for the
    # preceding runtime). Keep all package compilation warnings as errors below.
    Add-Type -ReferencedAssemblies $compilerReferences -CompilerOptions '/nowarn:1701' -TypeDefinition @'
using System;
using System.IO;
using System.Linq;
using Microsoft.CodeAnalysis;
using Microsoft.CodeAnalysis.CSharp;
namespace Decennium {
    public static class HeadlessCompiler {
        public static string Compile(string[] sources, string[] references, string[] options, string output) {
            var parsed = CSharpCommandLineParser.Default.Parse(options.Concat(new[] { "/out:" + output }).Concat(sources), Directory.GetCurrentDirectory(), null);
            var trees = sources.Select(path => CSharpSyntaxTree.ParseText(File.ReadAllText(path), parsed.ParseOptions, path));
            var refs = references.Select(path => MetadataReference.CreateFromFile(path));
            var compilation = CSharpCompilation.Create(Path.GetFileNameWithoutExtension(output), trees, refs,
                parsed.CompilationOptions.WithOutputKind(OutputKind.DynamicallyLinkedLibrary));
            using (var stream = File.Create(output)) {
                var emitted = compilation.Emit(stream);
                var diagnostics = string.Join(Environment.NewLine, parsed.Errors.Concat(emitted.Diagnostics));
                File.WriteAllText(output + ".compile.log", diagnostics);
                return emitted.Success && !parsed.Errors.Any(x => x.Severity == DiagnosticSeverity.Error)
                    ? null : diagnostics;
            }
        }
    }
}
'@
}
$failure = [Decennium.HeadlessCompiler]::Compile($Sources, $References, $CompilerOptions, $OutputAssembly)
if ($failure) { throw ('Named C# compilation failed: ' + $failure) }
$expected = [IO.Path]::GetFileNameWithoutExtension($OutputAssembly)
if ([Reflection.AssemblyName]::GetAssemblyName($OutputAssembly).Name -ne $expected) {
    throw 'Compiled assembly identity differs from the package identity.'
}
