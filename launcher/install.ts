import * as ADMZip from "adm-zip"
import * as tmp from "tmp";
import { join } from "path";

import { mergeInto } from "./fscommon"
import { vanillaPath } from "./constants";

export async function installDDLC(path) {
  const tmpdir = tmp.dirSync();
  const zipfile = new ADMZip(path);
  zipfile.extractAllTo(tmpdir.name);
  const ddlcdir = join(tmpdir.name,'DDLC-1.1.1-pc')
  await mergeInto(vanillaPath, ddlcdir)
  tmpdir.removeCallback();
}
