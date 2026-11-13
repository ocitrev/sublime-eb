# sublime-eb

This repository holds Sublime application packages in separate subdirectories. `SublimeText/` is the Sublime Text 4 package, containing custom commands, syntax support, builds, key bindings, themes, snippets, and migrated preferences. A future Sublime Merge package can live beside it.

## Install for development

```pwsh
$packages = Join-Path $env:APPDATA 'Sublime Text\Packages'
New-Item -ItemType Junction -Path (Join-Path $packages 'SublimeEB') -Target ./SublimeText
```
