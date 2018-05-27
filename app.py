from flask import Flask, render_template, request, send_from_directory
from appJar import gui
from slugify import slugify
from pathlib import Path
import shelve
import shutil
from zipfile import ZipFile
import subprocess
import tempfile
import os
import logging
import requests
import fnmatch
import configparser
from nocache import nocache

app = Flask(__name__)
modspath = Path.cwd()/"mods"
config = configparser.ConfigParser()
config.read('config.ini')
currentSkin = config["fDDMEPlayer"]["skin"]
logging.basicConfig(filename='fDDMEPlayer.log', filemode='w', level=logging.INFO, format="[%(levelname)s|%(levelno)s] (%(funcName)s) %(message)s")


addmodgui = None

VERSION_URL="https://raw.githubusercontent.com/famous1622/fDDMEPlayer/master/version"
PATTERNS = ("options.rpyc","*.rpa","options.rpy")


class InvalidModError(Exception):
    pass

def saveConfig():
    with open("config.ini", 'w') as configfile:
        config.write(configfile)

@app.route('/assets/<path:filename>')
@nocache
def loadSkinedAsset(filename):
    return send_from_directory(Path.cwd()/"skins"/currentSkin,filename)

def checkVersion():
    r = requests.get(VERSION_URL)
    try:
        r.raise_for_status()
    except requests.exceptions.HTTPError as e:
        logging.warning("Update check failed :( {0}".format(e))
    else:
        with open("version") as fp:
            if fp.read() != r.text:
                print("New version {0} available! Please download this from https://github.com/famous1622/fDDMEPlayer".format(r.text.strip()))

def getSkins():
    return (x.name for x in (Path.cwd()/"skins").iterdir() if x.is_dir())

def findParent(patterns, path):
    for root, dirs, files in os.walk(path):
        for pattern in patterns:
            for name in files:
                if fnmatch.fnmatch(name, pattern):
                    logging.info("Found game folder at: "+root)
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
                moveTree(s, d)
            else:
                forceMergeFlatDir(s, d)

def shutdown_server():
    func = request.environ.get('werkzeug.server.shutdown')
    if func is None:
        raise RuntimeError('Not running with the Werkzeug Server')
    func()

@app.route('/')
@nocache
def modlist():
    with shelve.open('mods.db') as mods:
        return render_template('modlist.html', mods=dict(mods))

@app.route('/settings.html')
def settings():
    return render_template('settings.html', skins=getSkins(), currSkin = currentSkin)

@app.route('/setskin')
@nocache
def setskin():
    global currentSkin
    newskin = request.args.get('skin', 'default')
    config["fDDMEPlayer"]["skin"] = newskin
    currentSkin = newskin
    saveConfig()
    return "<meta http-equiv=\"refresh\" content=\"1; url=http://localhost:5000/\">Please wait..."

@app.route('/addmod')
def addmod():
    global addmodgui
    addmodgui = gui("Add Mod")
    addmodgui.addLabel("title", "Add a Mod")
    addmodgui.addLabelEntry("Mod Name")
    addmodgui.addFileEntry("f1")
    addmodgui.addButtons(["Add", "Cancel"], addmodPress)
    addmodgui.go()
    return "<meta http-equiv=\"refresh\" content=\"1; url=http://localhost:5000/\">Please wait..."

def installZipMod(file,slug):
    with ZipFile(file) as modzip:
        with tempfile.TemporaryDirectory() as tmpdirname:
            modzip.extractall(tmpdirname)
            modGameDir=findParent(PATTERNS,tmpdirname)
            if modGameDir is None:
                print("That isn't a mod")
                logging.error("Not a mod :shrugika:")
                raise InvalidModError
            else:
                moveTree(modGameDir,str(modspath/slug/'game'))

def installRpaMod(file,slug):
    with tempfile.TemporaryDirectory() as tmpdirname:
        shutil.copy(file,tmpdirname)
        moveTree(tmpdirname,str(modspath/slug/'game'))



def addmodPress(button):
    global addmodgui
    modname = addmodgui.getEntry("Mod Name")
    modfile = addmodgui.getEntry("f1")
    if button == "Add":
        shutil.copytree(str(modspath/"vanilla"),str(modspath/slugify(modname)))
        ext = Path(modfile).suffix
        if ext == ".zip":
            try:
                installZipMod(modfile,slugify(modname))
            except InvalidModError:
                shutil.rmtree(str(modspath/slugify(modname)))
                return
        elif ext == ".rpa":
            installRpaMod(modfile,slugify(modname))
        else:
            print("{} files are not a supported mod type. If they should be, please create an issue on GitHub.".format(ext))
            shutil.rmtree(str(modspath/slugify(modname)))
            return
        with shelve.open('mods.db',writeback=True) as mods:
            mods[slugify(modname)]=modname
    addmodgui.stop()
    del addmodgui

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
    checkVersion()
    print("Open your web brower to localhost:5000")
    app.run(threaded=False)
