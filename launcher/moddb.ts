import { dataFolder } from "../src/common/constants";
import { Mod } from "../src/common/types";

import * as fs from "fs"
import { join } from "path";
import { promisify } from "util";

const modlistpath = join(dataFolder, "modlist.json");

async function readJSON(path) {
  return JSON.parse(await promisify(fs.readFile)(path, "utf-8"));
}

function outputJSON(path, object) {
  return promisify(fs.writeFile)(path, JSON.stringify(object), "utf-8");
}



export async function getMods(): Promise<Mod[]> {
    try {
      return await readJSON(modlistpath)
    } catch {
      return []
    }
}

export async function saveMods(mods: Mod[]) {
    await outputJSON(modlistpath, mods);
}

export async function addMod(mod: Mod) {
    const mods = await getMods();
    mods.push(mod);
    saveMods(mods);
}
