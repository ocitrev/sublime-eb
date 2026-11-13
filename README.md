# sublime-eb

Mes préfrénces et outils pour Sublime Text et Sublime Merge

## Install for development

```pwsh
$packages = Join-Path $env:APPDATA 'Sublime Text\Packages'
New-Item -ItemType Junction -Path (Join-Path $packages 'SublimeEB') -Target ./SublimeText
```

```pwsh
$packages = Join-Path $env:APPDATA 'Sublime Merge\Packages'
New-Item -ItemType Junction -Path (Join-Path $packages 'SublimeEB') -Target ./SublimeMerge
```
