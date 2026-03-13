@echo off
:: Run as Administrator: Right-click -> Run as administrator
netsh advfirewall firewall add rule name="Assistive Agent 8765" dir=in action=allow protocol=TCP localport=8765
if %errorlevel% equ 0 (
    echo Port 8765 opened. You can now access the app from your phone.
) else (
    echo Failed. Make sure you right-clicked and selected "Run as administrator".
)
pause
