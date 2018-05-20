from pathlib import Path
import shutil
import shelve
import os

if not (Path.cwd()/"DDLC").exists():
    print("Move the download of DDLC into fDDMEPlayer's folder, rename the folder to DDLC, and run setup again")
    raise SystemExit

with shelve.open('mods.db',writeback=True) as db:
    if "vanilla" in db.keys():
        print("This install is already setup. Please run it using run.bat")
        raise SystemExit
    db["vanilla"] = "Doki Doki Literature Club"
os.makedirs(str(Path.cwd()/"mods"),exist_ok=True)
shutil.copytree(str(Path.cwd()/"DDLC"),str(Path.cwd()/"mods"/"vanilla"))
shutil.rmtree(str(Path.cwd()/"DDLC"))
print("Setup complete!")
