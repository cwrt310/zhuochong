$ErrorActionPreference = 'Stop'
$package = Join-Path $PSScriptRoot 'xiaoba\native'
$manifestFile = Join-Path $package 'pet.json'
$spriteFile = Join-Path $package 'spritesheet.webp'
$validationFile = Join-Path $package 'validation-extended.json'
if (!(Test-Path -LiteralPath $manifestFile) -or !(Test-Path -LiteralPath $spriteFile) -or !(Test-Path -LiteralPath $validationFile)) {
    throw 'The validated Xiaoba package has not been completed yet.'
}
$manifest = Get-Content -Raw -LiteralPath $manifestFile | ConvertFrom-Json
$validation = Get-Content -Raw -LiteralPath $validationFile | ConvertFrom-Json
if ($manifest.id -ne 'xiaoba' -or $manifest.spriteVersionNumber -ne 2 -or !$validation.ok) {
    throw 'Invalid pet manifest or failed validation.'
}
$digest = (Get-FileHash -LiteralPath $spriteFile -Algorithm SHA256).Hash.ToLowerInvariant()
if ($digest -ne $validation.sha256) { throw 'Sprite bytes do not match validated bytes.' }
$codexRoot = Join-Path $env:USERPROFILE '.codex'
$petDir = Join-Path $codexRoot 'pets\xiaoba'
$configFile = Join-Path $codexRoot 'config.toml'
New-Item -ItemType Directory -Path $petDir -Force | Out-Null
Copy-Item -LiteralPath $spriteFile -Destination (Join-Path $petDir 'spritesheet.webp') -Force
Copy-Item -LiteralPath $manifestFile -Destination (Join-Path $petDir 'pet.json') -Force
if (Test-Path -LiteralPath $configFile) {
    $config = [System.IO.File]::ReadAllText($configFile)
    Copy-Item -LiteralPath $configFile -Destination (Join-Path $codexRoot 'config.before-xiaoba.toml') -Force
} else { $config = '' }
$desktopMatch = [regex]::Match($config, '(?ms)^\[desktop\]\s*\r?\n.*?(?=^\[|\z)')
if ($desktopMatch.Success) {
    $desktop = $desktopMatch.Value
    foreach ($entry in @(@('selected-avatar-id', '"xiaoba"'), @('avatar-overlay-pet-visible', 'true'))) {
        $pattern = '(?m)^' + [regex]::Escape($entry[0]) + '\s*=.*$'
        $line = $entry[0] + ' = ' + $entry[1]
        if ([regex]::IsMatch($desktop, $pattern)) { $desktop = [regex]::Replace($desktop, $pattern, $line) }
        else { $desktop = $desktop.TrimEnd() + "`r`n" + $line + "`r`n`r`n" }
    }
    $config = $config.Substring(0, $desktopMatch.Index) + $desktop + $config.Substring($desktopMatch.Index + $desktopMatch.Length)
} else {
    $config = $config.TrimEnd() + "`r`n`r`n[desktop]`r`nselected-avatar-id = `"xiaoba`"`r`navatar-overlay-pet-visible = true`r`n"
}
[System.IO.File]::WriteAllText($configFile, $config, (New-Object System.Text.UTF8Encoding($false)))
Write-Output 'Xiaoba installed; selected-avatar-id=xiaoba; avatar-overlay-pet-visible=true.'
Write-Output 'Refresh Settings > Pets if the app has not reloaded the local collection yet.'
