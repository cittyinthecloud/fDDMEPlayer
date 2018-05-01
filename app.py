from flask import Flask, render_template, request
from appJar import gui
from slugify import slugify
from pathlib import Path
import shelve
import shutil
from zipfile import ZipFile
import subprocess

app = Flask(__name__)
modspath = Path.cwd()/"mods"

def shutdown_server():
    func = request.environ.get('werkzeug.server.shutdown')
    if func is None:
        raise RuntimeError('Not running with the Werkzeug Server')
    func()

@app.route('/')
def modlist():
    with shelve.open('mods.db') as mods:
        return render_template('modlist.html', mods=dict(mods))

@app.route('/addmod')
def addmod():
    addmodgui.go()
    return "<meta http-equiv=\"refresh\" content=\"1; url=http://localhost:5000/\">Please wait..."

def addmodPress(button):
    modname = addmodgui.getEntry("Mod Name")
    modfile = addmodgui.getEntry("f1")
    if button == "Add":
        shutil.copytree(str(modspath/"vanilla"),str(modspath/slugify(modname)))
        with ZipFile(modfile) as modzip:
            modzip.extractall(modspath/slugify(modname)/'game')
        with shelve.open('mods.db',writeback=True) as mods:
            mods[slugify(modname)]=modname
    addmodgui.clearAllEntries()
    addmodgui.stop()

@app.route('/launchmod/<slug>')
def launchmod(slug):
    subprocess.Popen(str(modspath/slug/"DDLC.exe"))
    return "<meta http-equiv=\"refresh\" content=\"1; url=http://localhost:5000/\">Please wait..."

@app.route('/quit')
def quitprogram():
    shutdown_server()
    return "Application closed."


if __name__ == '__main__':
    with shelve.open('mods.db') as mods:
        if "vanilla" not in mods.keys():
            print("Please run setup.bat before run.bat.")
            print("Press enter to continue...")
            input()
            raise SystemExit
    addmodgui = gui("Add Mod")
    addmodgui.addLabel("title", "Add a Mod")
    addmodgui.addLabelEntry("Mod Name")
    addmodgui.addFileEntry("f1")
    addmodgui.addButtons(["Add", "Cancel"], addmodPress)
    print("Open your web brower to localhost:5000")
    app.run(threaded=False)
