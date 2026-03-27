Set WshShell = CreateObject("WScript.Shell")
Set fso = CreateObject("Scripting.FileSystemObject")

' Get username
username = WshShell.ExpandEnvironmentStrings("%USERNAME%")

' Get Desktop path
DesktopPath = WshShell.SpecialFolders("Desktop")

' Get WSL username (assume same as Windows username, or use 'snowwon5' as default)
wslUsername = InputBox("Enter your WSL Ubuntu username:" & vbCrLf & vbCrLf & _
                       "If you don't know, try your Windows username: " & username & vbCrLf & _
                       "Or contact your system administrator.", _
                       "WSL Username", username)

If wslUsername = "" Then
    MsgBox "Username is required. Please run this script again.", vbExclamation, "Error"
    WScript.Quit
End If

' Define paths
SourcePath = "\\wsl.localhost\Ubuntu-24.04\home\" & wslUsername & "\equipment_manager"
BatFile = SourcePath & "\EquipmentManager.bat"

' Check if source exists
If Not fso.FolderExists(SourcePath) Then
    MsgBox "Equipment Manager folder not found at:" & vbCrLf & vbCrLf & _
           SourcePath & vbCrLf & vbCrLf & _
           "Please make sure:" & vbCrLf & _
           "1. WSL Ubuntu is installed" & vbCrLf & _
           "2. equipment_manager folder is copied to WSL" & vbCrLf & _
           "3. Username is correct: " & wslUsername, vbCritical, "Error"
    WScript.Quit
End If

' Create desktop shortcut
Set oShellLink = WshShell.CreateShortcut(DesktopPath & "\기자재 관리.lnk")
oShellLink.TargetPath = BatFile
oShellLink.WorkingDirectory = SourcePath
oShellLink.Description = "Equipment Manager - 기자재 관리 시스템"
oShellLink.IconLocation = "%SystemRoot%\system32\imageres.dll,1"
oShellLink.Save

MsgBox "Desktop shortcut created successfully!" & vbCrLf & vbCrLf & _
       "바탕화면에 '기자재 관리' 아이콘이 생성되었습니다." & vbCrLf & vbCrLf & _
       "Double-click the icon to start the server.", vbInformation, "Success"
