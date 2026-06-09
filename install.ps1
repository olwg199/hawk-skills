param(
    [switch]$Claude,
    [switch]$Codex,
    [switch]$All,
    [switch]$NoClaudeCommands,
    [switch]$ClaudeCommands,
    [switch]$Help
)

$ErrorActionPreference = "Stop"

$RepoDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$SkillsDir = Join-Path $RepoDir "skills"
$PublicRemoteUrl = "https://github.com/olwg199/hawk-skills.git"
$SshPushRemoteUrl = "git@github.com:olwg199/hawk-skills.git"
$ClaudeCommandsManifest = Join-Path $HOME ".hawk-skills-claude-commands"

function Ok {
    param([string]$Message)
    Write-Host "  [OK] $Message" -ForegroundColor Green
}

function Usage {
    Write-Host "Usage: .\install.ps1 [-Claude | -Codex | -All] [-NoClaudeCommands | -ClaudeCommands]"
    Write-Host ""
    Write-Host "  -Claude            Install for Claude Code"
    Write-Host "  -Codex             Install for Codex CLI"
    Write-Host "  -All               Install for all CLIs (default)"
    Write-Host "  -NoClaudeCommands  Remove and skip legacy Claude command mirrors (default)"
    Write-Host "  -ClaudeCommands    Install legacy Claude command mirrors for older Claude Code versions"
}

function Save-RepoPath {
    Set-Content -Path (Join-Path $HOME ".hawk-skills-repo") -Value $RepoDir
    Ok "repo path saved to ~/.hawk-skills-repo"
}

function Normalize-OriginRemote {
    & git -C $RepoDir rev-parse --git-dir *> $null
    if ($LASTEXITCODE -ne 0) {
        return
    }

    $originUrl = (& git -C $RepoDir remote get-url origin 2>$null)

    if ($originUrl -eq "git@github.com:olwg199/hawk-skills.git" -or $originUrl -eq "ssh://git@github.com/olwg199/hawk-skills.git") {
        & git -C $RepoDir remote set-url origin $PublicRemoteUrl
        & git -C $RepoDir remote set-url --push origin $SshPushRemoteUrl
        Ok "origin fetch switched to HTTPS; push preserved over SSH"
    }
}

function Get-SkillNameFromTarget {
    param([string]$Target)

    $fullSkillsDir = [System.IO.Path]::GetFullPath($SkillsDir).TrimEnd('\', '/')
    $fullTarget = [System.IO.Path]::GetFullPath($Target)

    if (-not $fullTarget.StartsWith($fullSkillsDir + [System.IO.Path]::DirectorySeparatorChar, [System.StringComparison]::OrdinalIgnoreCase)) {
        return $null
    }

    $relative = $fullTarget.Substring($fullSkillsDir.Length).TrimStart('\', '/')
    return ($relative -split '[\\/]')[0]
}

function Test-SkillExists {
    param([string]$SkillName)
    return (Test-Path -LiteralPath (Join-Path (Join-Path $SkillsDir $SkillName) "SKILL.md") -PathType Leaf)
}

function Remove-StaleSkillLinks {
    param(
        [string]$LinkDir,
        [string]$Label
    )

    if (-not (Test-Path -LiteralPath $LinkDir -PathType Container)) {
        return
    }

    Get-ChildItem -LiteralPath $LinkDir -Force | ForEach-Object {
        if (-not ($_.Attributes -band [System.IO.FileAttributes]::ReparsePoint)) {
            return
        }

        $target = $_.Target
        if ($target -is [array]) {
            $target = $target[0]
        }
        if (-not $target) {
            return
        }

        $skillName = Get-SkillNameFromTarget -Target $target
        if (-not $skillName) {
            return
        }

        if (-not (Test-SkillExists -SkillName $skillName)) {
            Remove-Item -LiteralPath $_.FullName -Force
        }
    }
}

function Remove-StaleCopiedCommands {
    param([string]$CommandsDir)

    if (-not (Test-Path -LiteralPath $ClaudeCommandsManifest -PathType Leaf)) {
        return
    }

    Get-Content -LiteralPath $ClaudeCommandsManifest | ForEach-Object {
        $skillName = $_.Trim()
        if (-not $skillName -or (Test-SkillExists -SkillName $skillName)) {
            return
        }

        $commandPath = Join-Path $CommandsDir "$skillName.md"
        if (-not (Test-Path -LiteralPath $commandPath -PathType Leaf)) {
            return
        }

        $item = Get-Item -LiteralPath $commandPath -Force
        if ($item.Attributes -band [System.IO.FileAttributes]::ReparsePoint) {
            return
        }

        Remove-Item -LiteralPath $commandPath -Force
    }
}

function Remove-LegacyCopiedCommands {
    param([string]$CommandsDir)

    if (-not (Test-Path -LiteralPath $CommandsDir -PathType Container)) {
        return
    }

    # TODO(next-commit): remove this temporary h- prefix migration cleanup.
    # One-time migration for the h- prefix rename. Remove after old unprefixed
    # skill commands have been cleaned from existing installs.
    @("quick-review", "hawk-skills-update") | ForEach-Object {
        $skillName = $_
        $commandPath = Join-Path $CommandsDir "$skillName.md"
        if (-not (Test-Path -LiteralPath $commandPath -PathType Leaf)) {
            return
        }

        $item = Get-Item -LiteralPath $commandPath -Force
        if ($item.Attributes -band [System.IO.FileAttributes]::ReparsePoint) {
            return
        }

        if (Select-String -LiteralPath $commandPath -Pattern "^name: $skillName$" -Quiet) {
            Remove-Item -LiteralPath $commandPath -Force
        }
    }
}

function Remove-ClaudeCommandMirrors {
    param([string]$CommandsDir)

    Remove-StaleSkillLinks -LinkDir $CommandsDir -Label "Claude command"

    Get-ChildItem -LiteralPath $CommandsDir -Force | ForEach-Object {
        if (-not ($_.Attributes -band [System.IO.FileAttributes]::ReparsePoint)) {
            return
        }

        $target = $_.Target
        if ($target -is [array]) {
            $target = $target[0]
        }
        if (-not $target) {
            return
        }

        $skillName = Get-SkillNameFromTarget -Target $target
        if (-not $skillName) {
            return
        }

        Remove-Item -LiteralPath $_.FullName -Force
    }

    # TODO(next-commit): remove this copied mirror cleanup after one migration cycle.
    Get-ChildItem -LiteralPath $SkillsDir -Directory | ForEach-Object {
        $skillFile = Join-Path $_.FullName "SKILL.md"
        if (-not (Test-Path -LiteralPath $skillFile -PathType Leaf)) {
            return
        }

        $skillName = $_.Name
        $commandPath = Join-Path $CommandsDir "$skillName.md"
        if (-not (Test-Path -LiteralPath $commandPath -PathType Leaf)) {
            return
        }

        $item = Get-Item -LiteralPath $commandPath -Force
        if ($item.Attributes -band [System.IO.FileAttributes]::ReparsePoint) {
            return
        }

        if (Select-String -LiteralPath $commandPath -Pattern "^name: $skillName$" -Quiet) {
            Remove-Item -LiteralPath $commandPath -Force
        }
    }

    if (Test-Path -LiteralPath $ClaudeCommandsManifest -PathType Leaf) {
        Get-Content -LiteralPath $ClaudeCommandsManifest | ForEach-Object {
            $skillName = $_.Trim()
            if (-not $skillName) {
                return
            }

            $commandPath = Join-Path $CommandsDir "$skillName.md"
            if (-not (Test-Path -LiteralPath $commandPath -PathType Leaf)) {
                return
            }

            $item = Get-Item -LiteralPath $commandPath -Force
            if ($item.Attributes -band [System.IO.FileAttributes]::ReparsePoint) {
                return
            }

            Remove-Item -LiteralPath $commandPath -Force
        }
    }

    Remove-Item -LiteralPath $ClaudeCommandsManifest -Force -ErrorAction SilentlyContinue
}

function Set-DirectoryLink {
    param(
        [string]$Path,
        [string]$Target
    )

    if (Test-Path -LiteralPath $Path) {
        $item = Get-Item -LiteralPath $Path -Force
        if (-not ($item.Attributes -band [System.IO.FileAttributes]::ReparsePoint)) {
            throw "Refusing to replace non-link directory: $Path"
        }
        Remove-Item -LiteralPath $Path -Force
    }

    try {
        New-Item -ItemType Junction -Path $Path -Target $Target | Out-Null
    } catch {
        New-Item -ItemType SymbolicLink -Path $Path -Target $Target | Out-Null
    }
}

function Set-FileLinkOrCopy {
    param(
        [string]$Path,
        [string]$Target
    )

    if (Test-Path -LiteralPath $Path) {
        Remove-Item -LiteralPath $Path -Force
    }

    try {
        New-Item -ItemType SymbolicLink -Path $Path -Target $Target | Out-Null
    } catch {
        Copy-Item -LiteralPath $Target -Destination $Path -Force
    }
}

function Install-ClaudeCode {
    Write-Host "Installing for Claude Code..."

    $commandsDir = Join-Path $HOME ".claude\commands"
    $claudeSkillsDir = Join-Path $HOME ".claude\skills"
    New-Item -ItemType Directory -Force -Path $commandsDir, $claudeSkillsDir | Out-Null
    Remove-StaleSkillLinks -LinkDir $claudeSkillsDir -Label "Claude skill"
    Remove-LegacyCopiedCommands -CommandsDir $commandsDir

    if ($NoClaudeCommands) {
        Remove-ClaudeCommandMirrors -CommandsDir $commandsDir
    } else {
        Remove-StaleSkillLinks -LinkDir $commandsDir -Label "Claude command"
        Remove-StaleCopiedCommands -CommandsDir $commandsDir
    }

    $installedCommands = @()
    Get-ChildItem -LiteralPath $SkillsDir -Directory | ForEach-Object {
        $skillFile = Join-Path $_.FullName "SKILL.md"
        if (-not (Test-Path -LiteralPath $skillFile -PathType Leaf)) {
            return
        }

        $skillName = $_.Name
        if (-not $NoClaudeCommands) {
            $installedCommands += $skillName
            Set-FileLinkOrCopy -Path (Join-Path $commandsDir "$skillName.md") -Target $skillFile
            Ok "command: /$skillName"
        }
        Set-DirectoryLink -Path (Join-Path $claudeSkillsDir $skillName) -Target $_.FullName
        Ok "skill:   /$skillName (agent + slash command)"
    }

    if ($NoClaudeCommands) {
        Remove-Item -LiteralPath $ClaudeCommandsManifest -Force -ErrorAction SilentlyContinue
    } else {
        Set-Content -Path $ClaudeCommandsManifest -Value $installedCommands
    }
}

function Install-Codex {
    Write-Host "Installing for Codex CLI..."

    $codexSkillsDir = Join-Path $HOME ".codex\skills"
    New-Item -ItemType Directory -Force -Path $codexSkillsDir | Out-Null
    Remove-StaleSkillLinks -LinkDir $codexSkillsDir -Label "Codex skill"

    Get-ChildItem -LiteralPath $SkillsDir -Directory | ForEach-Object {
        $skillFile = Join-Path $_.FullName "SKILL.md"
        if (-not (Test-Path -LiteralPath $skillFile -PathType Leaf)) {
            return
        }

        $skillName = $_.Name
        Set-DirectoryLink -Path (Join-Path $codexSkillsDir $skillName) -Target $_.FullName
        Ok "skill: /$skillName"
    }
}

if ($Help) {
    Usage
    exit 0
}

$explicitNoClaudeCommands = $NoClaudeCommands
if ($explicitNoClaudeCommands -and $ClaudeCommands) {
    throw "Use only one of -NoClaudeCommands or -ClaudeCommands."
}

if ($ClaudeCommands) {
    $NoClaudeCommands = $false
} else {
    $NoClaudeCommands = $true
}

if (-not $Claude -and -not $Codex -and -not $All) {
    $Claude = $true
    $Codex = $true
}

if ($All) {
    $Claude = $true
    $Codex = $true
}

Save-RepoPath
Normalize-OriginRemote
if ($Claude) { Install-ClaudeCode }
if ($Codex) { Install-Codex }

Write-Host ""
Write-Host "Done. Restart your CLI to pick up new skills."
