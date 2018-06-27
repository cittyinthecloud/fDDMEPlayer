pyinstaller --add-data templates;templates --add-data static;static ^
            --add-binary distlibs;. --icon icon.ico fDDMEPlayer.py
move dist\fDDMEPlayer dist\bin
