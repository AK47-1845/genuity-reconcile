$ErrorActionPreference = 'Stop'
$repoRoot = Split-Path -Parent $MyInvocation.MyCommand.Path
Set-Location -LiteralPath $repoRoot
$env:PYTHONPATH = (Join-Path $repoRoot 'source') + [IO.Path]::PathSeparator + $env:PYTHONPATH
py -3 -m genuity_reconcile demo --output-dir demo_output --overwrite-demo
