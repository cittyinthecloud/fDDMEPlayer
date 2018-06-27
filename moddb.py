import json
from pathlib import Path

def saveModList(list):
    moddict = {}
    for mod in list:
        if mod.sayonika:
            sayoid=mod.sayonikaid
        else:
            sayoid=None
        moddict[mod.slug]={"name":mod.name,"sayonika":sayoid,"sayonikaVersion":mod.sayonikaVersion}
    with open("modlist.json","w") as f:
        json.dump(moddict, f)

if not Path("modlist.json").exists():
    saveModList([])

class Mod:
    def __init__(self, slug, name, sayonika=False, sayonikaid=None, sayonikaVersion=None):
        self.slug=slug
        self.name=name
        self.sayonika=sayonika
        self.sayonikaid=sayonikaid
        self.sayonikaVersion=sayonikaVersion
    def __eq__(self, other):
        try:
            return self.slug == other.slug
        except AttributeError:
            return False

def getModList():
    moddict=None
    modlist=[]
    with open("modlist.json") as f:
        moddict=json.load(f)
    for slug,details in moddict.items():
        if details["sayonika"] is None:
            modlist.append(Mod(slug,details["name"],False))
        else:
            modlist.append(Mod(slug,details["name"],True,details["sayonika"],details["sayonikaVersion"]))
    return modlist

def getModBySlug(slug):
    moddict=None
    with open("modlist.json") as f:
        moddict=json.load(f)
    details=moddict[slug]
    if details["sayonika"] is None:
        return Mod(slug,details["name"],False)
    else:
        return Mod(slug,details["name"],True,details["sayonika"],details["sayonikaVersion"])

def addMod(mod):
    modlist = getModList()
    modlist.append(mod)
    saveModList(modlist)

def removeMod(mod):
    modlist = getModList()
    modlist.remove(mod)
    saveModList(modlist)

def removeModBySlug(slug):
    mod = getModBySlug(slug)
    removeMod(mod)

def modExists(slug):
    moddict=None
    with open("modlist.json") as f:
        moddict=json.load(f)
    return slug in moddict
