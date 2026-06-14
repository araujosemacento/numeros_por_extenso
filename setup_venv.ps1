#Requires -Version 5.1
<#
.SYNOPSIS
    Configura e ativa o ambiente virtual Python (.venv) do projeto.
.DESCRIPTION
    Verifica se o .venv existe, cria se necessario, ativa e instala
    as dependencias listadas em requirements.txt (pytest por padrao).
#>

param(
    [string]$VenvNome = ".venv"
)

$ErrorActionPreference = "Stop"

$DirProjeto = $PSScriptRoot
if ([string]::IsNullOrEmpty($DirProjeto)) {
    $DirProjeto = Get-Location
}

$VenvCaminho = Join-Path $DirProjeto $VenvNome

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  Configuracao do Ambiente Virtual" -ForegroundColor Cyan
Write-Host "  SO:      Windows" -ForegroundColor Cyan
Write-Host "  Projeto: $DirProjeto" -ForegroundColor Cyan
Write-Host "  venv:    $VenvNome" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan

$PythonCmd = Get-Command python -ErrorAction SilentlyContinue
if (-not $PythonCmd) {
    Write-Error "Python nao encontrado. Instale o Python 3.10+ e adicione ao PATH."
    exit 1
}

Write-Host "`nPython encontrado: $($PythonCmd.Source)" -ForegroundColor Green

if (-not (Test-Path $VenvCaminho)) {
    Write-Host "`n[VENV] Criando ambiente virtual em $VenvNome..." -ForegroundColor Yellow
    & $PythonCmd.Source -m venv $VenvCaminho
    Write-Host "Ambiente virtual criado." -ForegroundColor Green
} else {
    Write-Host "`n[VENV] Ambiente virtual ja existe em $VenvNome." -ForegroundColor Green
}

$ActivatePath = Join-Path $VenvCaminho "Scripts" "Activate.ps1"

if (Test-Path $ActivatePath) {
    Write-Host "`n[VENV] Ativando ambiente virtual..." -ForegroundColor Yellow
    & $ActivatePath
} else {
    Write-Warning "Script de ativacao nao encontrado em $ActivatePath"
    exit 1
}

Write-Host "`n[PIP] Instalando dependencias..." -ForegroundColor Yellow
if (Test-Path (Join-Path $DirProjeto "requirements.txt")) {
    pip install -r (Join-Path $DirProjeto "requirements.txt")
} else {
    pip install pytest
}

Write-Host "`n========================================" -ForegroundColor Green
Write-Host "  Ambiente configurado com sucesso!" -ForegroundColor Green
Write-Host "  Python: $(Get-Command python | Select-Object -ExpandProperty Source)" -ForegroundColor Green
Write-Host "  venv:   $VenvNome" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Green

Write-Host "`nPara ativar manualmente, execute:" -ForegroundColor Cyan
Write-Host "    $VenvNome\Scripts\Activate.ps1" -ForegroundColor Cyan
Write-Host ""
