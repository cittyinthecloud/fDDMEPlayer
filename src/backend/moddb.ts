import { dataFolder } from "./constants";
import { Mod } from "./types";

import * as fs from "fs-extra";
import { join } from "path";

const modlistpath = join(dataFolder, "modlist.json");

export async function getMods(): Promise<Mod[]> {
    const modlistexists = await fs.pathExists(modlistpath);
    if (!modlistexists) {
        return [];
    } else {
        return await fs.readJSON(modlistpath);
    }
}

export async function saveMods(mods: Mod[]) {
    await fs.outputJSON(modlistpath, mods);
}

export async function addMod(mod: Mod) {
    const mods = await getMods();
    mods.push(mod);
    saveMods(mods);
}
