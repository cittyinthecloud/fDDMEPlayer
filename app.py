import configparser
import logging
from pathlib import Path

import requests

config = configparser.ConfigParser()

logging.basicConfig(filename='fDDMEPlayer.log', filemode='w', level=logging.DEBUG,
                    format="[%(levelname)s|%(levelno)s] (%(funcName)s) %(message)s")

addmodgui = None

VERSION_URL = "https://raw.githubusercontent.com/famous1622/fDDMEPlayer/master/version"




def saveConfig():
    with open("config.ini", 'w') as configfile:
        config.write(configfile)


def checkVersion():
    r = requests.get(VERSION_URL)
    try:
        r.raise_for_status()
    except requests.exceptions.HTTPError as e:
        logging.warning("Update check failed :( {0}".format(e))
    else:
        with open("version") as fp:
            if fp.read() != r.text:
                print(
                    "New version {0} available! Please download this from https://github.com/famous1622/fDDMEPlayer".format(r.text.strip()))


if __name__ == '__main__':
    if config["fDDMEPlayer"].getBoolean("installed", fallback=False):
        if not (Path.cwd()/"DDLC").exists():
            print("Move the download of DDLC into fDDMEPlayer's folder, rename the folder to DDLC, and run setup again")
            raise SystemExit
    checkVersion()
