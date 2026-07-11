@echo off
setlocal
cd /d "%~dp0"
python 09_scripts\verificar_utf8.py || exit /b 1
python 09_scripts\verificar_calculos.py || exit /b 1
cd 02_documento_maestro
xelatex -interaction=nonstopmode -halt-on-error documento_maestro.tex || exit /b 1
xelatex -interaction=nonstopmode -halt-on-error documento_maestro.tex || exit /b 1
cd ..
copy /Y 02_documento_maestro\documento_maestro.pdf 10_salida\pdf\documento_maestro_ratios.pdf >nul
echo Documento generado en 10_salida\pdf\documento_maestro_ratios.pdf
