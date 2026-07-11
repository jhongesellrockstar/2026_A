@echo off
setlocal
cd /d "%~dp0"
python 09_scripts\verificar_utf8.py || exit /b 1
python 09_scripts\verificar_calculos.py || exit /b 1
cd 03_presentacion_beamer
xelatex -interaction=nonstopmode -halt-on-error main.tex || exit /b 1
xelatex -interaction=nonstopmode -halt-on-error main.tex || exit /b 1
cd ..
copy /Y 03_presentacion_beamer\main.pdf 10_salida\pdf\presentacion_ratios_financieros.pdf >nul
echo Presentación generada en 10_salida\pdf\presentacion_ratios_financieros.pdf
