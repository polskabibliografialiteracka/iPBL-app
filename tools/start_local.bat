@echo off
cd /d "%~dp0.."
echo.
echo iPBL: lokalny serwer uruchomiony pod adresem http://localhost:8000
echo Zatrzymaj serwer klawiszami Ctrl+C.
echo.
start "" http://localhost:8000
python -m http.server 8000
pause
