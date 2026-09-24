$ErrorActionPreference = 'Stop'

$repoRoot = [IO.Path]::GetFullPath((Join-Path $PSScriptRoot '..'))
$skillsRoot = Join-Path $repoRoot 'skills'
$linksRoot = Join-Path $repoRoot '.claude\skills'
$comparison = [StringComparison]::OrdinalIgnoreCase

$skillDirs = @(
    Get-ChildItem -LiteralPath $skillsRoot -Directory | ForEach-Object {
        Get-ChildItem -LiteralPath $_.FullName -Directory | Where-Object {
            Test-Path -LiteralPath (Join-Path $_.FullName 'SKILL.md')
        }
    }
)

$desired = @{}
foreach ($skill in $skillDirs) {
    if ($desired.ContainsKey($skill.Name)) {
        throw "Duplicate skill folder name: $($skill.Name)"
    }
    $desired[$skill.Name] = [IO.Path]::GetFullPath($skill.FullName)
}

$existingRoot = Get-Item -LiteralPath $linksRoot -Force -ErrorAction SilentlyContinue
if ($existingRoot -and $existingRoot.LinkType -eq 'Junction') {
    $currentTarget = [IO.Path]::GetFullPath([string]@($existingRoot.Target)[0])
    if (-not [string]::Equals($currentTarget, $skillsRoot, $comparison)) {
        throw "Unexpected .claude/skills junction target: $currentTarget"
    }
    Remove-Item -LiteralPath $linksRoot -Force
    $existingRoot = $null
}

if (-not $existingRoot) {
    New-Item -ItemType Directory -Path $linksRoot | Out-Null
} elseif ($existingRoot.LinkType -or -not $existingRoot.PSIsContainer) {
    throw '.claude/skills must be a directory or the old junction onto skills/'
}

foreach ($link in Get-ChildItem -LiteralPath $linksRoot -Force) {
    if ($link.LinkType -ne 'Junction') { continue }
    $currentTarget = [IO.Path]::GetFullPath([string]@($link.Target)[0])
    if (-not $currentTarget.StartsWith($skillsRoot + [IO.Path]::DirectorySeparatorChar, $comparison)) {
        continue
    }
    if (-not $desired.ContainsKey($link.Name) -or
        -not [string]::Equals($currentTarget, $desired[$link.Name], $comparison)) {
        Remove-Item -LiteralPath $link.FullName -Force
    }
}

foreach ($name in ($desired.Keys | Sort-Object)) {
    $linkPath = Join-Path $linksRoot $name
    $existingLink = Get-Item -LiteralPath $linkPath -Force -ErrorAction SilentlyContinue
    if ($existingLink) {
        if ($existingLink.LinkType -ne 'Junction' -or
            -not [string]::Equals([IO.Path]::GetFullPath([string]@($existingLink.Target)[0]), $desired[$name], $comparison)) {
            throw "Cannot replace existing .claude/skills/$name"
        }
        continue
    }
    New-Item -ItemType Junction -Path $linkPath -Target $desired[$name] | Out-Null
}

Write-Output "Linked $($desired.Count) skills under .claude/skills/."
