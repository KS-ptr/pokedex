@echo off
setlocal
cd "%~dp0"

call :get_types
call :get_remarks
call :get_moves_prep
call :get_moves
exit /b

:get_types
call python %~dp0\get_types.py
echo "types.json done."
exit /b

:get_remarks
call python %~dp0\moves_with_remarks.py
echo "remarked_moves.json done."
exit /b

:get_moves_prep
call python %~dp0\moves_prep.py
echo "moves_prep.json done."
exit /b

:get_moves
call python %~dp0\moves_2.py
echo "moves.json done."
exit /b