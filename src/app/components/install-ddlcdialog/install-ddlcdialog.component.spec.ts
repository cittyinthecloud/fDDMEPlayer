import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { InstallDDLCDialogComponent } from './install-ddlcdialog.component';

describe('InstallDDLCDialogComponent', () => {
  let component: InstallDDLCDialogComponent;
  let fixture: ComponentFixture<InstallDDLCDialogComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ InstallDDLCDialogComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(InstallDDLCDialogComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
