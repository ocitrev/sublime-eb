# sublime-eb

Mes préférences et outils pour Sublime Text et Sublime Merge

## Install

```pwsh
$packages = Join-Path $env:APPDATA 'Sublime Text\Packages'
New-Item -ItemType Junction -Path (Join-Path $packages 'SublimeEB') -Target ([io.path]::GetFullPath('./SublimeText'))
```

```pwsh
$packages = Join-Path $env:APPDATA 'Sublime Merge\Packages'
New-Item -ItemType Junction -Path (Join-Path $packages 'SublimeEB') -Target ([io.path]::GetFullPath('./SublimeMerge'))
```
