from collections import namedtuple
import shelve

Mod = namedtuple("Mod", ("slug", "name"))
def addMod(mod):
    with shelve.open('mods.db',writeback=True) as mods:
        mods[mod.slug]=mod.name
