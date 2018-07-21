import { cwd } from "process";
import { join, resolve } from "path";

export const dataFolder = resolve(join(cwd(),"data"));

export const modsFolder = join(dataFolder, "mods")

export const vanillaPath = join(modsFolder, "vanilla")

export const PATTERNS = ["options.rpyc","*.rpa","options.rpy"]
