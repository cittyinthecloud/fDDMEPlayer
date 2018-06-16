from flask import Flask, render_template, request, send_from_directory
from appJar import gui
from slugify import slugify
from pathlib import Path
import shutil
from zipfile import ZipFile
from tarfile import TarFile
import subprocess
import tempfile
import os
import logging
import requests
import fnmatch
import configparser
from nocache import nocache
import moddb
from moddb import Mod
from common import installMod

app = Flask(__name__)
modspath = Path.cwd()/"mods"
config = configparser.ConfigParser()
config.read('config.ini')
currentSkin = config["fDDMEPlayer"]["skin"]
logging.basicConfig(filename='fDDMEPlayer.log', filemode='w', level=logging.INFO, format="[%(levelname)s|%(levelno)s] (%(funcName)s) %(message)s")


addmodgui = None

VERSION_URL="https://raw.githubusercontent.com/famous1622/fDDMEPlayer/master/version"

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


def shutdown_server():
    func = request.environ.get('werkzeug.server.shutdown')
    if func is None:
        raise RuntimeError('Not running with the Werkzeug Server')
    func()

@app.route('/')
@nocache
def modlist():
    return render_template('modlist.html', mods=moddb.getModList())

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

def addmodPress(button):
    global addmodgui
    modname = addmodgui.getEntry("Mod Name")
    modfile = addmodgui.getEntry("f1")
    modslug = slugify(modname)
    if button == "Add":
        while moddb.modExists(modslug):
            modslug += "-"
        installMod(modspath, modname,modslug,modfile)
    addmodgui.stop()
    del addmodgui

@app.route('/launchmod/<slug>')
def launchmod(slug):
    subprocess.Popen(str(modspath/slug/"DDLC.exe"))
    return "<meta http-equiv=\"refresh\" content=\"1; url=http://localhost:5000/\">Please wait..."

@app.route('/deletemod/<slug>')
def deletemod(slug):
    moddb.removeModBySlug(slug)
    shutil.rmtree(str(modspath/slug))
    return "<meta http-equiv=\"refresh\" content=\"1; url=http://localhost:5000/\">Please wait..."

@app.route('/quit')
def quitprogram():
    shutdown_server()
    return "Application closed."


if __name__ == '__main__':
    if not moddb.modExists("vanilla"):
        print("Please run setup.bat as administrator before run.bat.")
        print("Run migrate.bat as admin if you came from v0.2 or before")
        print("Press enter to continue...")
        input()
        raise SystemExit
    checkVersion()
    print("Open your web brower to localhost:5000")
    app.run(threaded=False)
