import { join, resolve } from "path";
import { path as appRoot } from "app-root-path";

export const dataFolder = resolve(join(appRoot, "data"));

export const modsFolder = join(dataFolder, "mods");

export const vanillaPath = join(modsFolder, "vanilla");

export const sultanCompiledModsPath = join(modsFolder, ".sultanCompiled");

export const patterns = ["options.rpyc", "*.rpa", "options.rpy"];
