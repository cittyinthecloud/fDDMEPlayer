import { Mod } from "./types"
import { modsFolder, vanillaPath, PATTERNS } from "./constants";
import { join, extname, basename, dirname, relative } from "path";
import { spawn } from "child_process";
import * as moddb from "./moddb"
import * as fs from "fs-extra";
import * as tmp from "tmp";
import * as ADMZip from "adm-zip";
import * as klaw from "klaw-sync";
import * as minimatch from "minimatch";
import * as tar from "tar"


export async function launchMod(mod : Mod) {
    const executableName = join(modsFolder, mod.slug, "DDLC.exe");
    const subprocess = spawn(executableName, [], {
        detached: true,
        stdio: 'ignore'
    });
    subprocess.unref()
}

export async function installMod(slug: string, name: string, path: string) {
    const newModFolder = join(modsFolder, slug);
    await fs.mkdirs(newModFolder)
    await fs.copy(vanillaPath, newModFolder)
    const extension = extname(path);
    if (extension == ".zip"){
        installZipMod(newModFolder, path);
    } else if (extension == ".gz"|| extension == ".tgz") {
        installTarballMod(newModFolder, path);
    } else if (extension == ".rpa") {
        installRpaMod(newModFolder, path);
    } else {
        throw new Error("InvalidModExt")
    }


    const mod = new Mod(slug, name);
    moddb.addMod(mod);
}

async function installZipMod(modFolder: string, path: string) {
    const tmpdir = tmp.dirSync()
    const zipfile = new ADMZip(path);
    zipfile.extractAllTo(tmpdir.name);
    const gamePath = findGameFolder(tmpdir.name);
    await mergeInto(join(modFolder,"game"),gamePath);
    tmpdir.removeCallback()
}

async function installTarballMod(modFolder: string, path: string) {
    const tmpdir = tmp.dirSync()
    await tar.extract({
        cwd: tmpdir.name,
        file: path
    })
    const gamePath = findGameFolder(tmpdir.name);
    await mergeInto(join(modFolder,"game"),gamePath);
    tmpdir.removeCallback()
}

async function installRpaMod(modFolder: string, path: string) {
}

async function mergeInto(into: string, from: string){
    const promises = klaw(from).map(x => {
        const src = x.path;
        const dst = join(into,relative(from, src));
        return fs.move(src, dst, {overwrite:true});
    });
    await Promise.all(promises)
}

function findGameFolder(path: string) {
    const items = klaw(path);
    let gamePath: string = null;
    const foundMatching = items.some(function(item){
        const itemname = basename(item.path);
        const isLandmark = PATTERNS.some(pattern => minimatch(itemname, pattern))
        if (isLandmark){
            gamePath = dirname(item.path)
        }
        return isLandmark
    })
    if (foundMatching){
        return gamePath;
    } else {
        throw Error("InvalidModDir")
    }
}
