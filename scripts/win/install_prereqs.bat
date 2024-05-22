where /q wsl
IF ERRORLEVEL 1 (
    winget install --interactive --exact Microsoft.WSL
)
where /q usbipd
IF ERRORLEVEL 1 (
    winget install --interactive --exact dorssel.usbipd-win
)