import moddb
import shelve

with shelve.open('mods.db') as mods:
    for slug,name in mods.items():
        moddb.addMod(moddb.Mod(slug,name,False))
