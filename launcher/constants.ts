import * as Store from "electron-store";
import { join, resolve } from "path";
import { app } from "electron"

export const dataFolder = app.getPath("userData");

export const modsFolder = join(dataFolder, "mods");

export const vanillaPath = join(dataFolder, "vanilla");

export const sultanCompiledModsPath = join(modsFolder, ".sultanCompiled");

export const patterns = ["options.rpyc", "*.rpa", "options.rpy"];

export const persistent = new Store({
  defaults: {
    "vanillaInstalled": false
  }
});
