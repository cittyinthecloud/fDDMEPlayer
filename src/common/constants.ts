import * as Store from "electron-store";
import { ElectronService } from "../app/providers/electron.service";

let persistent;

export function getPersistent(electron: ElectronService){
  return persistent || (persistent = new Store({
    defaults: {
      "vanillaInstalled": false
    },
    cwd: electron.remote.app.getPath("userData")
  }))
}
