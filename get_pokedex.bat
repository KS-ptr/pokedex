@echo off
setlocal
cd %~dp0

for /l %%s in (5 1 10) do (
    call :get_pokedex %%s
)
exit /b

:get_pokedex
call python crawling.py %1
echo pokedex_%1.json done.
echo check exception_%~1.log file.
exit /b