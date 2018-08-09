import { Component, OnInit } from '@angular/core';

@Component({
  selector: 'app-addmod',
  templateUrl: './addmod.component.html',
  styleUrls: ['./addmod.component.css']
})
export class AddmodComponent implements OnInit {

  fileSelected: boolean;
  selectedPath: string;
  constructor() {
    this.fileSelected = false;
  }

  ngOnInit() {
  }

  onFileInput(event) {
    this.fileSelected = true;
    console.log(event)
    this.selectedPath = event.srcElement.files[0].path
  }

}
