$Action = New-ScheduledTaskAction -Execute "C:\Users\pedro.augusto\Documents\auto_lock_pc\win_lock_env\Scripts\pythonw.exe" -Argument "C:\Users\pedro.augusto\Documents\auto_lock_pc\src\main.py"
$Trigger = New-ScheduledTaskTrigger -AtLogon
$Settings = New-ScheduledTaskSettingsSet -AllowStartIfOnBatteries -DontStopIfGoingOnBatteries -ExecutionTimeLimit 0

# Register for the Current User only (doesn't usually require Admin)
Register-ScheduledTask -Action $Action -Trigger $Trigger -Settings $Settings -TaskName "AutoLockPC_Tray" -Description "Auto Lock PC Proximity Monitor" -Force

Write-Host "Tarefa 'AutoLockPC_Tray' instalada com sucesso!"
Write-Host "Ela iniciará automaticamente no próximo login."
Write-Host "Para iniciar agora, execute: Start-ScheduledTask -TaskName 'AutoLockPC_Tray'"
