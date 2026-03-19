Set WshShell = CreateObject("WScript.Shell")
WshShell.Run "cmd /c start_with_ui.bat", 0
Set WshShell = Nothing
