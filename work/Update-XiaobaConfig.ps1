function Update-XiaobaConfig {
    param([AllowEmptyString()][string]$Text)

    $newline = if ($Text.Contains("`r`n")) { "`r`n" } else { "`n" }
    $lines = [regex]::Split($Text, '\r?\n')
    $codeLines = New-Object 'System.Collections.Generic.List[int]'
    $comments = @{}
    $multiline = ''
    for ($lineIndex = 0; $lineIndex -lt $lines.Count; $lineIndex++) {
        $line = $lines[$lineIndex]
        if (!$multiline) { $codeLines.Add($lineIndex) }
        for ($i = 0; $i -lt $line.Length;) {
            if ($multiline) {
                if ($multiline -eq '"""' -and $line[$i] -eq '\') { $i += 2; continue }
                if ($i + 2 -lt $line.Length -and $line.Substring($i, 3) -eq $multiline) {
                    $i += 3
                    # Four/five quote endings include one/two literal quotes.
                    while ($i -lt $line.Length -and $line[$i] -eq $multiline[0]) { $i++ }
                    $multiline = ''
                } else { $i++ }
                continue
            }
            $character = $line[$i]
            if ($character -eq '#') { $comments[$lineIndex] = $line.Substring($i); break }
            if ($character -eq '"' -or $character -eq "'") {
                $quote = [string]$character
                if ($i + 2 -lt $line.Length -and $line.Substring($i, 3) -eq ($quote * 3)) {
                    $multiline = $quote * 3
                    $i += 3
                } else {
                    $i++
                    while ($i -lt $line.Length) {
                        if ($quote -eq '"' -and $line[$i] -eq '\') { $i += 2; continue }
                        if ([string]$line[$i] -eq $quote) { $i++; break }
                        $i++
                    }
                }
            } else { $i++ }
        }
    }
    if ($multiline) { throw 'Unterminated multiline TOML string; configuration was not changed.' }

    $headers = @($codeLines | Where-Object { $lines[$_] -match '^\s*\[' })
    $rootEnd = if ($headers.Count) { $headers[0] } else { $lines.Count }
    foreach ($index in $codeLines) {
        if ($index -lt $rootEnd -and $lines[$index] -cmatch '^\s*(?:desktop|"desktop"|''desktop'')\s*[.=]') {
            throw 'Desktop uses root dotted keys or an inline table; use a [desktop] table before installing.'
        }
    }
    $desktopHeaders = @($headers | Where-Object {
        $lines[$_] -cmatch '^\s*\[\s*(?:desktop|"desktop"|''desktop'')\s*\]\s*(?:#.*)?$'
    })
    if ($desktopHeaders.Count -gt 1) { throw 'Duplicate desktop tables; configuration was not changed.' }
    if ($desktopHeaders.Count -eq 0) {
        $separator = if (!$Text) { '' } elseif ($Text.EndsWith($newline)) { $newline } else { $newline + $newline }
        return $Text + $separator + '[desktop]' + $newline + 'selected-avatar-id = "xiaoba"' + $newline + 'avatar-overlay-pet-visible = true' + $newline
    }

    $start = $desktopHeaders[0]
    $end = $lines.Count
    foreach ($header in $headers) {
        if ($header -gt $start) { $end = $header; break }
    }
    $missing = New-Object 'System.Collections.Generic.List[string]'
    foreach ($entry in @(@('selected-avatar-id', '"xiaoba"'), @('avatar-overlay-pet-visible', 'true'))) {
        $key = [regex]::Escape($entry[0])
        $pattern = '^(\s*)(?:' + $key + '|"' + $key + '"|''' + $key + ''')\s*='
        $settingLines = @($codeLines | Where-Object { $_ -gt $start -and $_ -lt $end -and $lines[$_] -cmatch $pattern })
        if ($settingLines.Count -gt 1) { throw ('Duplicate desktop setting: ' + $entry[0]) }
        $replacement = $entry[0] + ' = ' + $entry[1]
        if ($settingLines.Count -eq 1) {
            $index = $settingLines[0]
            $value = ($lines[$index] -split '=', 2)[1]
            if ($value.Contains('"""') -or $value.Contains("'" * 3)) {
                throw ('Unsupported multiline desktop setting: ' + $entry[0])
            }
            $indent = [regex]::Match($lines[$index], '^\s*').Value
            $lines[$index] = $indent + $replacement
            if ($comments.ContainsKey($index)) { $lines[$index] += ' ' + $comments[$index] }
        } else { $missing.Add($replacement) }
    }
    $result = New-Object 'System.Collections.Generic.List[string]'
    for ($i = 0; $i -le $lines.Count; $i++) {
        if ($i -eq $end) { foreach ($line in $missing) { $result.Add($line) } }
        if ($i -lt $lines.Count) { $result.Add($lines[$i]) }
    }
    return [string]::Join($newline, $result.ToArray())
}
