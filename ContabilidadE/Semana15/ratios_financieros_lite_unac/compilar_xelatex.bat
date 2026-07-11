@echo off
setlocal
cd /d "%~dp0"
python 04_scripts\verificar_utf8.py || exit /b 1
python 04_scripts\verificar_calculos.py || exit /b 1
cd 01_presentacion
xelatex -interaction=nonstopmode -halt-on-error main.tex || exit /b 1
xelatex -interaction=nonstopmode -halt-on-error main.tex || exit /b 1
copy /Y main.pdf "..\05_salida\pdf\Ratios_Financieros_Lite_UNAC.pdf" >nul
echo PDF generado en 05_salida\pdf\Ratios_Financieros_Lite_UNAC.pdf
