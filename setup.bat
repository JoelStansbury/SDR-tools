
set HERE=%~dp0
set WINDOWS_SCRIPTS=%HERE%\scripts\win

where /q wsl
IF ERRORLEVEL 1 (goto :install_prereqs)
where /q usbipd
IF ERRORLEVEL 1 (goto :install_prereqs)
goto :setup_vm

:install_prereqs
powershell -command "Start-Process %WINDOWS_SCRIPTS%\install_prereqs.bat elevated -Verb runas"

:setup_vm
wsl --update
wsl --install Ubuntu --no-launch
wsl --set-version Ubuntu 2
wsl --distribution ubuntu --exec sudo bash scripts/linux/setup.sh

:done
echo Initial setup is now complete. You may now close this window
@pause
EXIT /B