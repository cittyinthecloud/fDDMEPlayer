pyinstaller --add-data templates;templates --add-data static;static ^
            --add-binary distlibs;. --hidden-import=clr fDDMEPlayer.py
