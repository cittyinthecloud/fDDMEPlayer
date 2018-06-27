from flask import Flask, render_template, jsonify
from appJar import gui
from slugify import slugify
import common
import moddb

server = Flask(__name__)

@server.after_request
def add_header(response):
    response.headers['Cache-Control'] = 'no-store'
    return response

@server.route("/")
def landing():
    return render_template("modlist.html", mods=moddb.getModList())

@server.route("/api/<slug>/launch")
def launch_endpoint(slug):
    common.launch_mod(slug)
    return jsonify({})

@server.route("/api/<slug>/delete")
def delete_endpoint(slug):
    common.delete_mod(slug)
    return jsonify({})

@server.route("/api/openInstallModGUI")
def installmodgui():
    global addmodgui
    addmodgui = gui("Add Mod")
    addmodgui.addLabel("title", "Add a Mod")
    addmodgui.addLabelEntry("Mod Name")
    addmodgui.addFileEntry("f1")
    addmodgui.addButtons(["Add", "Cancel"], addmodPress)
    addmodgui.go()
    return jsonify({})

def addmodPress(button):
    global addmodgui
    modname = addmodgui.getEntry("Mod Name")
    modfile = addmodgui.getEntry("f1")
    modslug = slugify(modname)
    if button == "Add":
        while moddb.modExists(modslug):
            modslug += "-"
        common.installMod(modname,modslug,modfile)
    addmodgui.stop()
    del addmodgui

def run_server():
    server.run(host="127.0.0.1", port=23948, threaded=True)
