Set WshShell = CreateObject("WScript.Shell")
' 0 表示隐藏窗口，False 表示不等待执行完毕
WshShell.Run "python D:\Code\OmniLLM\agent\auto_build.py", 0, False