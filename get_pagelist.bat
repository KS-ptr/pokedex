@echo off
setlocal
cd "%~dp0"

call :get_urllist
exit /b

:get_urllist
call python %~dp0\get_pagelist.py
echo "pokemon_page_list.txt done."
exit /b