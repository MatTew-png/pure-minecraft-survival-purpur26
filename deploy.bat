@echo off
if "%~1"=="" (
    echo Usage: deploy.bat ^<path_to_plugin.jar^>
    exit /b 1
)
python "%~dp0scripts\remote_ops.py" upload "%~1" "C:\Users\Administrator\Desktop\survival\update_staging\%~nx1"
echo [OK] Plugin staged to update_staging\%~nx1. It will be loaded on server boot or restart.
