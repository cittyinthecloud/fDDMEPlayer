import { modsFolder, patterns, vanillaPath } from "./constants";
import * as moddb from "./moddb";
import { Mod } from "../src/common/types";
import { mergeInto } from "./fscommon"

import * as ADMZip from "adm-zip";
import { spawn } from "child_process";
import * as fs from "fs-extra";
import * as klaw from "klaw-sync";
import * as minimatch from "minimatch";
import { basename, dirname, extname, join, relative } from "path";
import * as tar from "tar";
import * as tmp from "tmp";
import { slug as slugify } from "slug";

export async function launchMod(mod: Mod) {
    const executableName = join(modsFolder, slugify(mod.title), "DDLC.exe");
    const subprocess = spawn(executableName, [], {
        cwd: join(modsFolder, slugify(mod.title)),
        detached: true,
        stdio: "ignore",
    });
    subprocess.unref();
}

export async function installMod(mod: Mod, path: string) {
    const slug = slugify(mod.title)
    const newModFolder = join(modsFolder, slug);
    await fs.mkdirs(newModFolder);
    await fs.copy(vanillaPath, newModFolder);
    const extension = extname(path);
    if (extension === ".zip") {
        installZipMod(newModFolder, path);
    } else if (extension === ".gz" || extension === ".tgz") {
        installTarballMod(newModFolder, path);
    } else if (extension === ".rpa") {
        installRpaMod(newModFolder, path);
    } else {
        throw new Error("InvalidModExt");
    }
    moddb.addMod(mod);
}

async function installZipMod(modFolder: string, path: string) {
    const tmpdir = tmp.dirSync();
    const zipfile = new ADMZip(path);
    zipfile.extractAllTo(tmpdir.name);
    const gamePath = findGameFolder(tmpdir.name);
    await mergeInto(join(modFolder, "game"), gamePath);
    tmpdir.removeCallback();
}

async function installTarballMod(modFolder: string, path: string) {
    const tmpdir = tmp.dirSync();
    await tar.extract({
        cwd: tmpdir.name,
        file: path,
    });
    const gamePath = findGameFolder(tmpdir.name);
    await mergeInto(join(modFolder, "game"), gamePath);
    tmpdir.removeCallback();
}

async function installRpaMod(modFolder: string, path: string) {
    await fs.move(path, join(modFolder, "game", basename(path)));
}

function findGameFolder(path: string) {
    const items = klaw(path);
    var gamePath: string = "";
    const foundMatching = items.some((item) => {
        const itemname = basename(item.path);
        const isLandmark = patterns.some((pattern) => minimatch(itemname, pattern));
        if (isLandmark) {
            gamePath = dirname(item.path);
        }
        return isLandmark;
    });
    if (foundMatching) {
        return gamePath;
    } else {
        throw Error("InvalidModDir");
    }
}
