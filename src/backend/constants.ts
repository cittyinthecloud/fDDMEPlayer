import { join, resolve } from "path";
import { cwd } from "process";

export const dataFolder = resolve(join(cwd(), "data"));

export const modsFolder = join(dataFolder, "mods");

export const vanillaPath = join(modsFolder, "vanilla");

export const patterns = ["options.rpyc", "*.rpa", "options.rpy"];
