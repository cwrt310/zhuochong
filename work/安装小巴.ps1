$ErrorActionPreference = 'Stop'
. (Join-Path $PSScriptRoot 'Update-XiaobaConfig.ps1')
$package = Join-Path $PSScriptRoot 'xiaoba\native'
$manifestFile = Join-Path $package 'pet.json'
$spriteFile = Join-Path $package 'spritesheet.webp'
if (!(Test-Path -LiteralPath $manifestFile) -or !(Test-Path -LiteralPath $spriteFile)) {
    throw 'Xiaoba package files are missing.'
}
$manifest = Get-Content -Raw -Encoding UTF8 -LiteralPath $manifestFile | ConvertFrom-Json
if ($manifest.id -ne 'xiaoba' -or $manifest.spriteVersionNumber -ne 2 -or $manifest.spritesheetPath -ne 'spritesheet.webp') {
    throw 'Invalid Xiaoba pet manifest.'
}
$codexRootInput = if ($env:CODEX_HOME) { $env:CODEX_HOME } else { Join-Path $env:USERPROFILE '.codex' }
$codexRoot = $ExecutionContext.SessionState.Path.GetUnresolvedProviderPathFromPSPath($codexRootInput)
$petDir = Join-Path $codexRoot 'pets\xiaoba'
$configFile = Join-Path $codexRoot 'config.toml'
$backupFile = Join-Path $codexRoot 'config.before-xiaoba.toml'
if (Test-Path -LiteralPath $configFile) {
    $config = [System.IO.File]::ReadAllText($configFile)
} else { $config = '' }
$updatedConfig = Update-XiaobaConfig -Text $config

# Resolve configuration errors before overwriting an installed pet.
New-Item -ItemType Directory -Path $petDir -Force | Out-Null
Copy-Item -LiteralPath $spriteFile -Destination (Join-Path $petDir 'spritesheet.webp') -Force
Copy-Item -LiteralPath $manifestFile -Destination (Join-Path $petDir 'pet.json') -Force
if (Test-Path -LiteralPath $configFile) {
    if (!(Test-Path -LiteralPath $backupFile)) {
        Copy-Item -LiteralPath $configFile -Destination $backupFile
    }
}
if ($updatedConfig -cne $config) {
    $temporaryConfig = Join-Path $codexRoot ('config.xiaoba-' + [guid]::NewGuid().ToString('N') + '.tmp')
    try {
        [System.IO.File]::WriteAllText($temporaryConfig, $updatedConfig, (New-Object System.Text.UTF8Encoding($false)))
        if (Test-Path -LiteralPath $configFile) {
            [System.IO.File]::Replace($temporaryConfig, $configFile, [NullString]::Value)
        } else { [System.IO.File]::Move($temporaryConfig, $configFile) }
    } finally {
        if (Test-Path -LiteralPath $temporaryConfig) { Remove-Item -LiteralPath $temporaryConfig }
    }
}
Write-Output 'Xiaoba installed; selected-avatar-id=xiaoba; avatar-overlay-pet-visible=true.'
Write-Output 'Refresh Settings > Pets if the app has not reloaded the local collection yet.'
