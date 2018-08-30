import logging
import shutil
import subprocess
import tempfile
from pathlib import Path
from zipfile import ZipFile

import slugify

from . import fs, moddb
from .constants import PATTERNS, InvalidModError, modspath


def installZipMod(file,slug):
    with ZipFile(file) as modzip:
        with tempfile.TemporaryDirectory() as tmpdirname:
            modzip.extractall(tmpdirname)
            modGameDir=fs.findParent(PATTERNS,tmpdirname)
            if modGameDir is None:
                print("That isn't a mod")
                logging.error("Not a mod :shrugika:")
                raise InvalidModError
            else:
                fs.moveTree(modGameDir,str(modspath/slug/'game'))

def installRpaMod(file,slug):
    with tempfile.TemporaryDirectory() as tmpdirname:
        shutil.copy(file,tmpdirname)
        fs.moveTree(tmpdirname,str(modspath/slug/'game'))

def addMod(modname, modfile):
    ext = Path(modfile).suffix
    mod = moddb.Mod(slugify(modname),modname)
    shutil.copytree(str(modspath/"vanilla"),str(modspath/mod.slug))
    if ext == ".zip":
        try:
            installZipMod(modfile,mod.slug)
        except InvalidModError as err:
            shutil.rmtree(str(modspath/mod.slug))
            logging.error("Something went wrong {}".format(err))
            return
    elif ext == ".rpa":
        installRpaMod(modfile,slugify(modname))
    else:
        print("{} files are not a supported mod type. If they should be, please create an issue on GitHub.".format(ext))
        logging.error("Unsupported file {}".format(ext))
        shutil.rmtree(str(modspath/slugify(modname)))
        return
    moddb.addMod(mod)



def launchmod(slug):
    subprocess.Popen(str(modspath/slug/"DDLC.exe
