@echo off
setlocal
cd %~dp0

for /l %%s in (1 1 10) do (
    call :get_pokedex %%s
    timeout /t 60
)
exit /b

:get_pokedex
call python %~dp0\crawling.py %1
echo pokedex_%1.json done.
echo check exception_%~1.log file.
exit /b