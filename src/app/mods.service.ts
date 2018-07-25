import { Injectable } from '@angular/core';

import { Mod } from "../common/types"

import { Observable, fromEventPattern } from "rxjs";
import { IpcRenderer } from 'electron';
import { map } from 'rxjs/operators';

@Injectable({
  providedIn: 'root'
})
export class ModsService {

  constructor() { }

  getMods(ipc: IpcRenderer): Observable<Mod[]> {
    return fromEventPattern(
      function addHandler(h) { return ipc.on("modlist", h) },
      function delHandler(h) { return ipc.removeListener("modlist",h) })
      .pipe(map((value) => value[1])) as Observable<Mod[]>;
  }
}
