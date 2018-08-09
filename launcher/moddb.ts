import { dataFolder } from "./constants";
import { Mod } from "../src/common/types";

import * as fs from "fs"
import { join } from "path";
import { promisify } from "util";

import * as Store from "electron-store";

const modStore = new Store({
  name: "moddb",
  defaults:{
    "mods": []
  }
})

export function getMods(): Mod[] {
    return modStore.get("mods")
}

export async function saveMods(mods: Mod[]) {
  modStore.set("mods", mods)
}

export async function addMod(mod: Mod) {
    const mods = await getMods();
    mods.push(mod);
    saveMods(mods);
}
