import * as ADMZip from "adm-zip"
import * as tmp from "tmp-promise";
import { join } from "path";
import * as rimraf from "rimraf"

import { mergeInto } from "./fscommon"
import { vanillaPath } from "./constants";

export async function installDDLC(path: string) {
  const tmpdir = await tmp.dir({unsafeCleanup: true});
  const zipfile = new ADMZip(path);
  zipfile.extractAllTo(tmpdir.path);
  const ddlcdir = join(tmpdir.path,'DDLC-1.1.1-pc')
  return mergeInto(vanillaPath, ddlcdir);
}
