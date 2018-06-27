pyinstaller --add-data templates;templates --add-data static;static ^
            --add-binary distlibs;. fDDMEPlayer.py
move dist\fDDMEPlayer dist\bin
