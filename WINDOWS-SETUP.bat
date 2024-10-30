@echo off
setlocal

for /f "tokens=*" %%i in ('python --version 2^>nul') do set "version=%%i"

if not defined version (
    echo Python не установлен, либо не найден в PATH.
    exit /b 1
)

echo %version% | findstr /r "Python 3.*" >nul
if errorlevel 1 (
    echo Python версии 3 не обнаружен. Убедитесь, что у вас установлена версия 3.
    exit /b 1
)

python -m venv venv
call venv\Scripts\activate
python -m pip install --upgrade pip
REM Установка зависимостей из requirements.txt
pip install -r requirements.txt

echo Окружение настроено.

start cmd
