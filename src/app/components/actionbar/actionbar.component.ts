import { Component, OnInit } from '@angular/core';
import { BreakpointObserver, Breakpoints, BreakpointState } from '@angular/cdk/layout';
import { Observable } from 'rxjs';
import { map } from 'rxjs/operators';

import { MatDialog } from '@angular/material';
import { InstallDDLCDialogComponent } from '../install-ddlcdialog/install-ddlcdialog.component';
import { ElectronService } from '../../providers/electron.service';
import { getPersistent } from '../../../common/constants';


@Component({
  selector: 'app-actionbar',
  templateUrl: './actionbar.component.html',
  styleUrls: ['./actionbar.component.css'],
})
export class ActionbarComponent {
  ngOnInit(): void {
    window.setTimeout(()=>{
      console.log(getPersistent(this.electron).get("vanillaInstalled"))
      if (!getPersistent(this.electron).get("vanillaInstalled")){
        this.dialog.open(InstallDDLCDialogComponent, {
          hasBackdrop: true,
          disableClose: true
        });
      }
    })
  }
  isHandset$: Observable<boolean> = this.breakpointObserver.observe(Breakpoints.Handset)
    .pipe(
      map(result => result.matches)
    );

  constructor(private breakpointObserver: BreakpointObserver,
              private dialog: MatDialog,
              private electron: ElectronService) {}

  onLoad(): void {
  }
}
