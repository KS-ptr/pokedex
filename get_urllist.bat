@echo off
setlocal
cd "%~dp0"

call :get_urllist
exit /b

:get_urllist
call python %~dp0\get_urllist.py
echo "pokemon_url_list.txt done."
exit /b