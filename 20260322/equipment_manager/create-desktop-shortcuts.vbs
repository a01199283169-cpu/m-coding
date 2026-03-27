Set WshShell = CreateObject("WScript.Shell")
Set fso = CreateObject("Scripting.FileSystemObject")

' Get Desktop path
DesktopPath = WshShell.SpecialFolders("Desktop")

' Get current script directory (WSL path to Windows path)
ScriptPath = "\\wsl.localhost\Ubuntu-24.04\home\snowwon5\m-coding\20260322\equipment_manager"

' Create Start shortcut
Set StartLink = WshShell.CreateShortcut(DesktopPath & "\Equipment Manager - START.lnk")
StartLink.TargetPath = ScriptPath & "\start-equipment-app.bat"
StartLink.WorkingDirectory = ScriptPath
StartLink.Description = "Start Equipment Manager Server"
StartLink.IconLocation = "%SystemRoot%\system32\SHELL32.dll,21"
StartLink.Save

' Create Stop shortcut
Set StopLink = WshShell.CreateShortcut(DesktopPath & "\Equipment Manager - STOP.lnk")
StopLink.TargetPath = ScriptPath & "\stop-equipment-app.bat"
StopLink.WorkingDirectory = ScriptPath
StopLink.Description = "Stop Equipment Manager Server"
StopLink.IconLocation = "%SystemRoot%\system32\SHELL32.dll,28"
StopLink.Save

MsgBox "Desktop shortcuts created successfully!" & vbCrLf & vbCrLf & _
       "- Equipment Manager - START" & vbCrLf & _
       "- Equipment Manager - STOP", vbInformation, "Success"
