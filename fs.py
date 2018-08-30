import fnmatch
import logging
import os
import shutil


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


def forceCopyFile(sfile, dfile):
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
            forceCopyFile(s, d)
        if os.path.isdir(s):
            isRecursive = not isAFlatDir(s)
            if isRecursive:
                moveTree(s, d)
            else:
                forceMergeFlatDir(s, d)
