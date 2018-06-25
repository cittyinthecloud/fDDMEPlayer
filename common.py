from pathlib import Path
import shutil
import tempfile
import os
import fnmatch
import logging
from zipfile import ZipFile
from tarfile import TarFile
import moddb
from moddb import Mod

PATTERNS = ("options.rpyc","*.rpa","options.rpy")

def installZipMod(modspath,file,slug):
    with tempfile.TemporaryDirectory() as tmpdirname:
        with ZipFile(file) as modzip:
            modzip.extractall(tmpdirname)
        modGameDir=findGameFolder(tmpdirname)
        if modGameDir is None:
            print("That isn't a mod")
            logging.error("Not a mod :shrugika:")
            raise InvalidModError
        else:
            moveTree(modGameDir,str(modspath/slug/'game'))

def installTarballMod(modspath,file,slug):
    with tempfile.TemporaryDirectory() as tmpdirname:
        with TarFile(file) as tarball:
            tarball.extractall(tmpdirname)
        modGameDir=findGameFolder(tmpdirname)
        if modGameDir is None:
            print("That isn't a mod")
            logging.error("Not a mod :shrugika:")
            raise InvalidModError
        else:
            moveTree(modGameDir,str(modspath/slug/'game'))

def installRpaMod(modspath,file,slug):
    with tempfile.TemporaryDirectory() as tmpdirname:
        shutil.copy(file,tmpdirname)
        moveTree(tmpdirname,str(modspath/slug/'game'))


def installMod(modspath, name, slug, file):
    shutil.copytree(str(modspath/"vanilla"),str(modspath/slug))
    ext = Path(file).suffix
    try:
        {
            ".zip":installZipMod,
            ".gz":installTarballMod,
            ".rpa":installRpaMod,
        }[ext](modspath,file,slug)
    except InvalidModError:
        shutil.rmtree(str(modspath/slug))
        logging.error("Invalid Mod")
        print("Invalid Mod :Uwaaaa:")
        return
    except KeyError:
        print("{} files are not a supported mod type. If they should be, please create an issue on GitHub.".format(ext))
        shutil.rmtree(str(modspath/slug))
        return
    with open(modspath/slug/"environment.txt","w") as f:
        f.write('FDDME_LAUNCHED = "1"\n')
    moddb.addMod(Mod(slug,name,False))

def findGameFolder(path):
    for root, dirs, files in os.walk(path):
        for pattern in PATTERNS:
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

class InvalidModError(Exception):
    pass
