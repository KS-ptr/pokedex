@echo off
cd "%~dp0"

call :get_types
call :get_special_case
call :get_moves
exit /b

:get_types
call python %~dp0\get_types.py
echo "types.json done."
exit /b

:get_special_case
call python %~dp0\special_dynamax_power.py
echo "special_case_dynamax_power.json done."
exit /b

:get_moves
call python %~dp0\moves_prep.py
echo "moves_prep.py done."
call python "moves_2.py"
echo "moves.json done."
exit /b