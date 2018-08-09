import { Component, OnInit } from '@angular/core';
import { ElectronService } from '../../providers/electron.service';
import { crc32 } from 'crc';
import { MatDialogRef } from '@angular/material';

@Component({
  selector: 'app-install-ddlcdialog',
  templateUrl: './install-ddlcdialog.component.html',
  styleUrls: ['./install-ddlcdialog.component.scss']
})
export class InstallDDLCDialogComponent implements OnInit {

  fileSelected: boolean;
  selectedPath: string;
  isValidDDLC: boolean;
  DDLCChecked: boolean;
  installing: boolean;

  constructor(public dialogRef: MatDialogRef<InstallDDLCDialogComponent>,
              private electron: ElectronService) {
    this.fileSelected = false;
    this.isValidDDLC = true;
    this.selectedPath = "";
    this.DDLCChecked = false;
    this.installing = false;
  }

  ngOnInit() {
  }

  onFileInput(event) {
    this.isValidDDLC = true;
    this.fileSelected = true;
    this.DDLCChecked = false;
    console.log(event)
    this.selectedPath = event.srcElement.files[0].path;
    this.electron.fs.readFile(this.selectedPath,(err, buf) =>{
        const crc = crc32(buf).toString(16)
        if (crc != "153a7b13"){
            this.isValidDDLC = false
        }
        this.DDLCChecked = true
    })

  }

  openBrowser(event, url: string) {
    event.preventDefault(true)
    this.electron.ipcRenderer.send("openExternal",url)
  }

  okayClick() {
    this.installing = true;
    this.electron.ipcRenderer.once("DDLCInstalled",()=>{
        this.dialogRef.close()
    })
    this.electron.ipcRenderer.send("installDDLC", this.selectedPath)
  }
}
