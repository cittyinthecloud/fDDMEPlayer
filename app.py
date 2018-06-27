from threading import Thread
import logging
import webview
import time
from backend import run_server
import moddb
from http.client import HTTPConnection
import sys
from pathlib import Path
import os
import shutil
logger = logging.getLogger(__name__)


def url_ok(url, port):
    try:
        conn = HTTPConnection(url, port)
        conn.request("GET", "/")
        r = conn.getresponse()
        return r.status == 200
    except:
        logger.exception("Server not started")
        return False

def main():
    if not moddb.modExists("vanilla"):
        if not (Path.cwd()/"DDLC").exists():
            print("Move the download of DDLC into fDDMEPlayer's folder, rename the folder to DDLC, and run setup again")
            print("Press Enter to continue...")
            input()
            sys.exit()
        os.makedirs(str(Path.cwd()/"mods"),exist_ok=True)
        shutil.move(str(Path.cwd()/"DDLC"),str(Path.cwd()/"mods"/"vanilla"))
        moddb.addMod(moddb.Mod("vanilla", "Doki Doki Literature Club"))
        logger.info("Setup complete!")

    logger.debug("Starting server")
    t = Thread(target=run_server)
    t.daemon = True
    t.start()
    logger.debug("Checking server")

    while not url_ok("127.0.0.1", 23948):
        time.sleep(0.1)

    logger.debug("Server started")
    webview.create_window("fDDMEPlayer",
                          "http://127.0.0.1:23948",min_size=(1280,720))

if __name__ == '__main__':
    main()
