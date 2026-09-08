$ErrorActionPreference = "Stop"

$packageRoot = Split-Path -Parent $MyInvocation.MyCommand.Path
$backendPath = Join-Path $packageRoot "backend"

if (-not (Test-Path (Join-Path $backendPath "manage.py"))) {
    Write-Host "A pasta backend nao foi encontrada ao lado deste arquivo." -ForegroundColor Red
    exit 1
}

if (-not (Get-Command python -ErrorAction SilentlyContinue)) {
    Write-Host "Python nao foi encontrado. Instale o Python e tente novamente." -ForegroundColor Red
    exit 1
}

if (-not (Get-Command cloudflared -ErrorAction SilentlyContinue)) {
    Write-Host "cloudflared nao foi encontrado." -ForegroundColor Yellow
    Write-Host "Instale com: winget install Cloudflare.cloudflared"
    exit 1
}

Push-Location $backendPath
try {
    python manage.py migrate
    python manage.py check
    $django = Start-Process -FilePath "python" -ArgumentList @("manage.py", "runserver", "127.0.0.1:8000", "--noreload") -WindowStyle Hidden -PassThru
} finally {
    Pop-Location
}

Write-Host ""
Write-Host "IncluiEdu iniciado localmente." -ForegroundColor Green
Write-Host "O Cloudflare exibira abaixo o endereco publico HTTPS." -ForegroundColor Cyan
Write-Host "Mantenha esta janela aberta durante a demonstracao." -ForegroundColor Yellow
Write-Host ""

try {
    cloudflared tunnel --url http://127.0.0.1:8000
} finally {
    if ($django -and -not $django.HasExited) {
        Stop-Process -Id $django.Id
    }
}