@echo off
title Instalador e Executor - Operacoes com Imagens

echo =============================================================
echo  Verificando dependencias e iniciando a aplicacao...
echo =============================================================
echo.

REM Verifica se o Python esta instalado e disponivel no PATH
python --version >nul 2>nul
if %errorlevel% neq 0 (
    echo [ERRO] Python nao encontrado.
    echo Por favor, instale Python 3 e adicione-o ao PATH do sistema.
    pause
    exit /b
)

echo Python encontrado!
echo.

echo Verificando e instalando bibliotecas necessarias (numpy, pillow)...
pip install -r requirements.txt

echo.
echo Bibliotecas instaladas com sucesso!
echo.
echo =============================================================
echo  Iniciando a aplicacao...
echo =============================================================
echo.

python run.py

echo.
echo A aplicacao foi fechada.
pause