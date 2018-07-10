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
import tempfile
from zipfile import ZipFile

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
    common.checkVersion()
    if not moddb.modExists("vanilla"):
        if not (Path.cwd()/"ddlc-win.zip").exists():
            print("Place a copy of ddlc-win.zip into this apps folder, then run it again to setup.")
            print("Press Enter to continue...")
            input()
            sys.exit()

        os.makedirs(str(Path.cwd()/"mods"),exist_ok=True)
        with tempfile.TemporaryDirectory() as tmpdirname:
            with ZipFile(str(Path.cwd()/"ddlc-win.zip")) as modzip:
                modzip.extractall(tmpdirname)
                ddlcpath = next(Path(tmpdirname).glob("DDLC*"))
                shutil.move(str(ddlcpath),str(Path.cwd()/"mods"/"vanilla"))
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
