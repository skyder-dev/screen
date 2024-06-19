@echo off
echo Installation des requirements Python...
echo.

REM Assurez-vous d'utiliser pip compatible avec votre environnement
python -m pip install --upgrade pip

REM Installez les packages requis en utilisant requirements.txt
python -m pip install -r requirements.txt

echo.
echo Installation terminée.
echo Appuyez sur une touche pour fermer cette fenêtre.
pause > nul
