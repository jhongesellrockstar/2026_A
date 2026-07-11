@echo off
setlocal

set "ROOT=%~dp0"
set "BEAMER_DIR=%ROOT%03_presentacion_beamer"
set "OUT_DIR=%ROOT%08_salida\pdf"
set "LOG_DIR=%ROOT%08_salida\compilacion_log"

if not exist "%OUT_DIR%" mkdir "%OUT_DIR%"
if not exist "%LOG_DIR%" mkdir "%LOG_DIR%"

where xelatex >nul 2>nul
if not "%errorlevel%"=="0" (
    echo No se encontro xelatex en PATH.
    echo Instale MiKTeX/TeX Live o agregue sus binarios al PATH.
    exit /b 1
)

pushd "%BEAMER_DIR%"
xelatex -interaction=nonstopmode -halt-on-error -output-directory="%OUT_DIR%" main.tex > "%LOG_DIR%\xelatex_presentacion_1.log" 2>&1
set "ERR=%errorlevel%"
if "%ERR%"=="0" (
    xelatex -interaction=nonstopmode -halt-on-error -output-directory="%OUT_DIR%" main.tex > "%LOG_DIR%\xelatex_presentacion_2.log" 2>&1
    set "ERR=%errorlevel%"
)
popd

if "%ERR%"=="0" (
    echo Presentacion compilada correctamente: "%OUT_DIR%\main.pdf"
) else (
    echo Error al compilar la presentacion. Revisar logs en "%LOG_DIR%"
)

exit /b %ERR%
