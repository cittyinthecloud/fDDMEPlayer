import 'zone.js/dist/zone-mix';
import 'reflect-metadata';
import '../polyfills';
import { BrowserModule } from '@angular/platform-browser';
import { NgModule } from '@angular/core';
import { FormsModule } from '@angular/forms';

import { HttpClientModule } from '@angular/common/http';

import { AppRoutingModule } from './app-routing.module';

import { ElectronService } from './providers/electron.service';

import { WebviewDirective } from './directives/webview.directive';

import { AppComponent } from './app.component';
import { HomeComponent } from './components/home/home.component';

import { ActionbarComponent } from './components/actionbar/actionbar.component';

import { ModlistComponent } from './components/modlist/modlist.component';

import { LayoutModule } from '@angular/cdk/layout';
import { BrowserAnimationsModule } from '@angular/platform-browser/animations';
import {
  MatToolbarModule,
  MatButtonModule,
  MatSidenavModule,
  MatIconModule,
  MatListModule,
  MatCardModule,
  MatGridListModule,
  MatSnackBarModule,
  MatFormFieldModule,
  MatInputModule,
  MatDialogModule,
  MatProgressSpinnerModule,
} from '@angular/material';
import { AddmodComponent } from './components/addmod/addmod.component';
import { InstallDDLCDialogComponent } from './components/install-ddlcdialog/install-ddlcdialog.component';

@NgModule({
  declarations: [
    AppComponent,
    HomeComponent,
    ActionbarComponent,
    ModlistComponent,
    WebviewDirective,
    AddmodComponent,
    InstallDDLCDialogComponent,
  ],
  imports: [
    MatToolbarModule,
    MatButtonModule,
    MatSidenavModule,
    MatIconModule,
    MatListModule,
    MatCardModule,
    MatGridListModule,
    MatSnackBarModule,
    MatFormFieldModule,
    MatInputModule,
    MatDialogModule,
    MatProgressSpinnerModule,
    BrowserAnimationsModule,
    BrowserModule,
    FormsModule,
    HttpClientModule,
    AppRoutingModule,
    LayoutModule,
  ],
  entryComponents:[InstallDDLCDialogComponent],
  providers: [ElectronService],
  bootstrap: [AppComponent]
})
export class AppModule { }
