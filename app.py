from flask import Flask, render_template, request
from appJar import gui
from slugify import slugify
from pathlib import Path
import shelve
import shutil
from zipfile import ZipFile
import subprocess
import tempfile
import os

app = Flask(__name__)
modspath = Path.cwd()/"mods"

def findParent(name, path):
    for root, dirs, files in os.walk(path):
        if name in files:
            return root

def forceMergeFlatDir(srcDir, dstDir):
    if not os.path.exists(dstDir):
        os.makedirs(dstDir)
    for item in os.listdir(srcDir):
        srcFile = os.path.join(srcDir, item)
        dstFile = os.path.join(dstDir, item)
        forceCopyFile(srcFile, dstFile)

def forceCopyFile (sfile, dfile):
    if os.path.isfile(sfile):
        shutil.move(sfile, dfile)

def isAFlatDir(sDir):
    for item in os.listdir(sDir):
        sItem = os.path.join(sDir, item)
        if os.path.isdir(sItem):
            return False
    return True

def moveTree(src, dst):
    for item in os.listdir(src):
        s = os.path.join(src, item)
        d = os.path.join(dst, item)
        if os.path.isfile(s):
            if not os.path.exists(dst):
                os.makedirs(dst)
            forceCopyFile(s,d)
        if os.path.isdir(s):
            isRecursive = not isAFlatDir(s)
            if isRecursive:
                copyTree(s, d)
            else:
                forceMergeFlatDir(s, d)
				
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
			with tempfile.TemporaryDirectory() as tmpdirname:
				modzip.extractall(tmpdirname)
				modgamedir = Path(findParent("options.rpyc",tmpdirname)
				moveTree(str(modgamedir),str(modspath/slugify(modname)/'game'))
                                  
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
