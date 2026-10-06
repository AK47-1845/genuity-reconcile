$ErrorActionPreference = 'Stop'
$bundleRoot = Split-Path -Parent $MyInvocation.MyCommand.Path
Set-Location -LiteralPath $bundleRoot
$env:PYTHONPATH = (Join-Path $bundleRoot 'source') + [IO.Path]::PathSeparator + $env:PYTHONPATH
py -3 -W error::ResourceWarning -m unittest discover -s tests -p 'test_genuity_reconcile.py' -v
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
py -3 -m genuity_reconcile verify --output-dir demo_output
exit $LASTEXITCODE
