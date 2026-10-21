[CmdletBinding(PositionalBinding = $false)]
param(
    [ValidateSet("apply", "check")]
    [string]$Mode = "apply",
    [switch]$Replace,
    [Parameter(ValueFromRemainingArguments = $true)]
    [string[]]$Items
)
# Installs the owner's agent environment from this folder (see environment.py). Windows PowerShell 5.1 or later.
# -Replace (apply only) also replaces CHANGED items after backing them up: the ones listed after it
# (for example -Replace ~/.claude/CLAUDE.md core.hooksPath), or all of them when none are listed.
$ErrorActionPreference = "Stop"
$Script = Join-Path $PSScriptRoot "environment.py"

$Python = $null
foreach ($candidate in @("py", "python", "python3")) {
    $cmd = Get-Command $candidate -ErrorAction SilentlyContinue
    if ($cmd -and $cmd.Source -notlike "*WindowsApps*") { $Python = $cmd.Source; break }
}
if (-not $Python) { Write-Error "Python 3.9 or later is required (the Claude Code PR hook runs on it too). Install it and run again."; exit 1 }

$Arguments = @($Script, $Mode)
if ($Replace) { $Arguments += "--replace"; if ($Items) { $Arguments += $Items } }
if ((Split-Path $Python -Leaf) -eq "py.exe") { & $Python -3 @Arguments } else { & $Python @Arguments }
exit $LASTEXITCODE
