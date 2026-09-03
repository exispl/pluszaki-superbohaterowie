@echo off
echo ============================================================
echo   PLUSZAKI SUPERBOHATEROWIE - Firefly Auto-Generator
echo ============================================================
echo.

REM Sprawdź czy Python jest zainstalowany
python --version >nul 2>&1
if errorlevel 1 (
    echo [BLAD] Python nie jest zainstalowany!
    echo Pobierz z: https://python.org
    pause
    exit /b 1
)

REM Zainstaluj zależności
echo [1/3] Instaluję zależności...
pip install playwright pillow --quiet
playwright install chromium --quiet

echo.
echo [2/3] Sprawdzam Chrome z CDP...
REM Spróbuj otworzyć Chrome z remote debugging
start "" "chrome.exe" --remote-debugging-port=9222 --user-data-dir="%TEMP%\chrome_firefly" 2>nul

timeout /t 3 /nobreak >nul

echo.
echo [3/3] Uruchamiam generator...
echo.
echo UWAGA: Jeśli Chrome się otworzy - zaloguj się do Adobe Firefly
echo        a skrypt zacznie automatycznie generować obrazy.
echo.
echo Output: %~dp0autogen_models\
echo.

python "%~dp0autogen_firefly.py"

echo.
echo ============================================================
echo   GOTOWE! Sprawdź folder: autogen_models\
echo   Raport HTML:            autogen_models\raport.html
echo ============================================================
pause
