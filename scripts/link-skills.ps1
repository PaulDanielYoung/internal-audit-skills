# Maintainer-only script, not a supported install route. Users install through
# `npx skills add` as the README documents.
#
# Links every skill in this repo into the local Claude Code skills directory as
# a junction, so edits here are live in the next session without reinstalling.
# Remove the links (`cmd /c rmdir <link>`, no /s) before testing an npx
# install, which would otherwise collide with them.

param(
    [string]$SkillsDirectory = (Join-Path ([Environment]::GetFolderPath('UserProfile')) '.claude\skills')
)

$ErrorActionPreference = 'Stop'

$repoRoot = [IO.Path]::GetFullPath((Join-Path $PSScriptRoot '..'))
$skillsRoot = Join-Path $repoRoot 'skills'
$linksRoot = [IO.Path]::GetFullPath($SkillsDirectory)
$comparison = [StringComparison]::OrdinalIgnoreCase

if ([string]::Equals($linksRoot, $skillsRoot, $comparison) -or
    $linksRoot.StartsWith($skillsRoot + [IO.Path]::DirectorySeparatorChar, $comparison)) {
    throw 'The destination must be outside the source skills directory.'
}

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
if ($existingRoot -and ($existingRoot.LinkType -or -not $existingRoot.PSIsContainer)) {
    throw "The destination must be a regular directory: $linksRoot"
}

# Check every collision before changing the destination. Only this repo's
# junctions may be replaced or removed; other installed skills belong to the user.
$ownedLinks = @()
if ($existingRoot) {
    foreach ($link in Get-ChildItem -LiteralPath $linksRoot -Force) {
        $owned = $false
        if ($link.LinkType -eq 'Junction') {
            $currentTarget = [IO.Path]::GetFullPath([string]@($link.Target)[0])
            $owned = $currentTarget.StartsWith($skillsRoot + [IO.Path]::DirectorySeparatorChar, $comparison)
        }
        if ($desired.ContainsKey($link.Name) -and -not $owned) {
            throw "Cannot replace existing skill: $($link.FullName). Move it aside or choose a different destination."
        }
        if ($owned) { $ownedLinks += $link }
    }
}

if (-not $existingRoot) {
    New-Item -ItemType Directory -Path $linksRoot -Force | Out-Null
}

foreach ($link in $ownedLinks) {
    $currentTarget = [IO.Path]::GetFullPath([string]@($link.Target)[0])
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
            throw "Cannot replace existing skill: $linkPath"
        }
        continue
    }
    New-Item -ItemType Junction -Path $linkPath -Target $desired[$name] | Out-Null
}

Write-Output "Linked $($desired.Count) skills under $linksRoot."
