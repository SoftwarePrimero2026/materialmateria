@echo off
REM ===========================================================================
REM  Lanzador del juego de dados 10.000 (Windows)
REM ===========================================================================
REM
REM  Uso (doble clic sobre el archivo, o desde la consola):
REM
REM    ejecutar.bat              Lanza el juego
REM    ejecutar.bat --editor     Abre el proyecto en el editor de Godot
REM    ejecutar.bat --tests      Corre todos los tests
REM    ejecutar.bat --python     Corre la version de consola (Python)
REM    ejecutar.bat --ayuda      Muestra esta ayuda
REM
REM  Si Godot no esta instalado, el script lo descarga solo (una vez) dentro de
REM  la carpeta .godot-bin\ del proyecto.
REM
REM  Variable de entorno:
REM    GODOT_BIN    Ruta a un Godot.exe ya instalado (tiene prioridad).
REM    GODOT_VER    Version a descargar si falta (por defecto 4.7.2-stable).
REM ===========================================================================

setlocal EnableDelayedExpansion
chcp 65001 >nul 2>&1

set "AQUI=%~dp0"
if "%AQUI:~-1%"=="\" set "AQUI=%AQUI:~0,-1%"
set "PROYECTO=%AQUI%\diezmil_godot"
set "BIN_DIR=%AQUI%\.godot-bin"

if not defined GODOT_VER set "GODOT_VER=4.7.2-stable"
set "GODOT_ZIP=Godot_v%GODOT_VER%_win64.exe.zip"
set "GODOT_URL=https://github.com/godotengine/godot/releases/download/%GODOT_VER%/%GODOT_ZIP%"

set "GODOT="
set "MODO=%~1"
if "%MODO%"=="" set "MODO=juego"

REM --- Ayuda: no hace falta buscar Godot -----------------------------------
if /i "%MODO%"=="--ayuda"  goto :ayuda
if /i "%MODO%"=="-h"       goto :ayuda
if /i "%MODO%"=="--help"   goto :ayuda
if /i "%MODO%"=="ayuda"    goto :ayuda
if /i "%MODO%"=="help"     goto :ayuda

REM --- Version de consola: tampoco necesita Godot --------------------------
if /i "%MODO%"=="--python" goto :python
if /i "%MODO%"=="python"   goto :python

REM --- Asegurar Godot para todo lo demas -----------------------------------
call :detectar_godot
if not defined GODOT (
  call :descargar_godot
  if not defined GODOT (
    echo.
    echo   XX No se pudo obtener Godot.
    pause
    exit /b 1
  )
)

if /i "%MODO%"=="--tests"  goto :tests
if /i "%MODO%"=="tests"    goto :tests
if /i "%MODO%"=="--editor" goto :editor
if /i "%MODO%"=="editor"   goto :editor
if /i "%MODO%"=="juego"    goto :juego
if /i "%MODO%"=="--juego"  goto :juego
if /i "%MODO%"=="-j"       goto :juego
if /i "%MODO%"=="--2d"     goto :juego2d
if /i "%MODO%"=="2d"       goto :juego2d

echo   XX Opcion desconocida: %MODO%
echo.
goto :ayuda


REM ===========================================================================
REM  Detectar un Godot utilizable
REM ===========================================================================
:detectar_godot
REM 1) Variable de entorno explicita.
if defined GODOT_BIN (
  if exist "%GODOT_BIN%" (
    set "GODOT=%GODOT_BIN%"
    exit /b 0
  )
  echo   !! GODOT_BIN apunta a "%GODOT_BIN%" pero no existe; lo ignoro.
)

REM 2) Descarga previa dentro del proyecto.
if exist "%BIN_DIR%\Godot_v*_win64.exe" (
  for %%F in ("%BIN_DIR%\Godot_v*_win64.exe") do (
    set "GODOT=%%~fF"
  )
  exit /b 0
)

REM 3) Instalaciones tipicas del usuario.
for %%D in ("%USERPROFILE%\godot" "%USERPROFILE%\Godot" "%USERPROFILE%\Downloads" "%USERPROFILE%\Descargas" "%LOCALAPPDATA%\Programs\Godot") do (
  if exist "%%~D\Godot_v*_win64.exe" (
    for %%F in ("%%~D\Godot_v*_win64.exe") do (
      set "GODOT=%%~fF"
    )
    exit /b 0
  )
)

REM 4) PATH del sistema.
for %%C in (godot4.exe godot.exe Godot.exe) do (
  for /f "delims=" %%P in ('where %%C 2^>nul') do (
    if not defined GODOT set "GODOT=%%~fP"
  )
)
if defined GODOT exit /b 0

exit /b 0


REM ===========================================================================
REM  Descargar Godot si hace falta
REM ===========================================================================
:descargar_godot
echo.
echo ==^> Godot no esta instalado. Lo descargo ^(una sola vez^).
echo      Version: %GODOT_VER%
echo      Destino: %BIN_DIR%
echo.

if not exist "%BIN_DIR%" mkdir "%BIN_DIR%" >nul 2>&1

set "ZIP=%BIN_DIR%\%GODOT_ZIP%"

REM Descargar con PowerShell (viene en Windows 10/11).
where powershell >nul 2>&1
if errorlevel 1 (
  echo   XX No encuentro PowerShell, necesario para descargar Godot.
  echo   XX Baja Godot a mano desde https://godotengine.org/download
  echo   XX y despues define GODOT_BIN=C:\ruta\a\Godot.exe
  exit /b 1
)

echo   Descargando ^(~50 MB^)...
powershell -NoProfile -ExecutionPolicy Bypass -Command ^
  "$ProgressPreference='SilentlyContinue'; try { Invoke-WebRequest -Uri '%GODOT_URL%' -OutFile '%ZIP%' -UseBasicParsing } catch { exit 1 }"
if errorlevel 1 (
  echo   XX Fallo la descarga desde %GODOT_URL%
  if exist "%ZIP%" del /q "%ZIP%" >nul 2>&1
  exit /b 1
)

echo   Descomprimiendo...
powershell -NoProfile -ExecutionPolicy Bypass -Command ^
  "Expand-Archive -Path '%ZIP%' -DestinationPath '%BIN_DIR%' -Force"
if errorlevel 1 (
  echo   XX Fallo al descomprimir %ZIP%
  exit /b 1
)

if exist "%ZIP%" del /q "%ZIP%" >nul 2>&1

call :detectar_godot
if defined GODOT (
  echo   OK Godot descargado en !GODOT!
) else (
  echo   XX La descarga termino pero no encuentro el .exe en %BIN_DIR%
)
exit /b 0


REM ===========================================================================
REM  Modos
REM ===========================================================================
:juego
echo.
echo ==^> Lanzando el juego 3D ^(dados con fisica real^)...
echo      Proyecto: %PROYECTO%
echo.
echo   Controles: clic en los dados para seleccionarlos,
echo              "Separar seleccionados" suma los puntos,
echo              "Volver a tirar" relanza, "Plantarse" cierra el turno.
echo.
"%GODOT%" --path "%PROYECTO%"
goto :fin

:juego2d
echo.
echo ==^> Lanzando la variante 2D ^(dados planos^)...
echo      Proyecto: %PROYECTO%
echo.
"%GODOT%" --path "%PROYECTO%" res://scenes/Main.tscn
goto :fin

:editor
echo.
echo ==^> Abriendo el proyecto en el editor de Godot...
echo.
"%GODOT%" --path "%PROYECTO%" --editor
goto :fin

:tests
echo.
echo ==^> Corriendo todos los tests...
echo.
set "GODOT_BIN=%GODOT%"
set "FALLOS=0"

REM --- Motor de reglas (Python), si esta disponible ---
where python >nul 2>&1
if errorlevel 1 (
  echo   !! Python no encontrado: omito los tests del motor de reglas.
) else (
  echo --- Python: motor de reglas ---
  pushd "%AQUI%"
  python -m unittest test_reglas10000 2>&1 | findstr /C:"Ran " /C:"OK" /C:"FAILED"
  if errorlevel 1 set "FALLOS=1"
  popd
)

echo.
echo --- Godot: paridad con Python ^(46656 tiradas^) ---
"%GODOT%" --headless --path "%PROYECTO%" --script res://tests/test_paridad.gd 2>&1 | findstr /C:"Chequeos" /C:"RESULTADO" /C:"discrepancias"
if errorlevel 1 set "FALLOS=1"

echo.
echo --- Godot: partidas completas ^(300^) ---
"%GODOT%" --headless --path "%PROYECTO%" --script res://tests/test_partida.gd 2>&1 | findstr /C:"Chequeos" /C:"RESULTADO" /C:"Promedio"
if errorlevel 1 set "FALLOS=1"

echo.
echo --- Godot: end-to-end de la UI ---
"%GODOT%" --path "%PROYECTO%" res://tests/E2ERunner.tscn 2>&1 | findstr /C:"Chequeos" /C:"RESULTADO"
if errorlevel 1 set "FALLOS=1"

echo.
if "!FALLOS!"=="0" (
  echo ============================================================
  echo  RESULTADO GLOBAL: TODO OK
  echo ============================================================
) else (
  echo ============================================================
  echo  RESULTADO GLOBAL: hubo fallos
  echo ============================================================
)
goto :fin

:python
echo.
echo ==^> Lanzando la version de consola ^(Python^)...
echo.
where python >nul 2>&1
if errorlevel 1 (
  echo   XX No encuentro Python. Instalalo desde https://www.python.org/downloads/
  echo   XX ^(marca "Add Python to PATH" durante la instalacion^).
  pause
  exit /b 1
)
pushd "%AQUI%"
python diezmil.py
popd
goto :fin


REM ===========================================================================
REM  Ayuda y salida
REM ===========================================================================
:ayuda
echo.
echo ============================================================================
echo  Juego de dados 10.000 - Lanzador (Windows)
echo ============================================================================
echo.
echo  Uso:
echo    ejecutar.bat              Lanza el juego 3D (dados con fisica real)
echo    ejecutar.bat --2d         Lanza la variante 2D (dados planos)
echo    ejecutar.bat --editor     Abre el proyecto en el editor de Godot
echo    ejecutar.bat --tests      Corre todos los tests
echo    ejecutar.bat --python     Version de consola (Python)
echo    ejecutar.bat --ayuda      Muestra esta ayuda
echo.
echo  Si Godot no esta instalado, se descarga solo la primera vez dentro de
echo  la carpeta .godot-bin\ del proyecto.
echo.
echo  Variables de entorno utiles:
echo    set GODOT_BIN=C:\ruta\a\Godot.exe    Usar un Godot ya instalado
echo    set GODOT_VER=4.6.3-stable           Otra version a descargar
echo.
pause
exit /b 0

:fin
echo.
REM Si se lanzo con doble clic, no cerrar la ventana de golpe.
echo %CMDCMDLINE% | find /i "/c" >nul
if not errorlevel 1 pause
endlocal
exit /b 0
