import { Component, OnInit } from '@angular/core';
import { Mod } from '../../../common/types';
import { ElectronService } from '../../providers/electron.service';

@Component({
  selector: 'app-addmod',
  templateUrl: './addmod.component.html',
  styleUrls: ['./addmod.component.css']
})
export class AddmodComponent implements OnInit {

  fileSelected: boolean;
  selectedPath: string;

  model = new Mod("","");

  constructor(private electron: ElectronService) {
    this.fileSelected = false;
  }

  ngOnInit() {
  }

  submitted = false;

  onSubmit() {
    this.submitted = true;
    this.electron.ipcRenderer.send("installMod", {mod: new Mod(this.model.title,this.model.author,this.model.releaseDate),path: this.selectedPath})
  }

  onFileInput(event) {
    this.fileSelected = true;
    console.log(event)
    this.selectedPath = event.srcElement.files[0].path
  }

   get diagnostic() { return JSON.stringify(this.model); }

}
