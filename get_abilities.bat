@echo off
setlocal
cd "%~dp0"

call :get_abilities
REM call :get_items
exit /b

:get_abilities
call python %~dp0\abilities.py
echo "abilities.json done."
exit /b

:get_items
call python %~dp0\items.py
echo "items.json done."
exit /b