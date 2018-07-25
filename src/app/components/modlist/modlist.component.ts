import { Component, OnInit } from '@angular/core';
import { MatSnackBar } from '@angular/material';

import { ModsService } from '../../mods.service';
import { Mod } from '../../../common/types';
import { ElectronService } from '../../providers/electron.service';

@Component({
  selector: 'app-modlist',
  templateUrl: './modlist.component.html',
  styleUrls: ['./modlist.component.css']
})
export class ModlistComponent implements OnInit {

  mods: Mod[];

  constructor(private modsservice: ModsService,
              private electron: ElectronService,
              public snackbar: MatSnackBar) { }

  getMods(): void {
    this.modsservice.getMods(this.electron.ipcRenderer)
        .subscribe((mods) => this.mods = mods);
  }

  ngOnInit() {
    this.getMods();
    this.electron.ipcRenderer.send("getMods")
    this.electron.ipcRenderer.on("launchReply", (e, state)=> {
      console.log("launchReply: "+JSON.stringify(state));
      if(state["success"]){
        this.snackbar.open("Launched "+state["mod"].name,"Dismiss",{
          duration: 3000
        })
      } else {
        this.snackbar.open("Launch failed :(")
      }
    })
  }

  startLaunch(mod: Mod) {
    this.electron.ipcRenderer.send("launch", mod)
  }
}
