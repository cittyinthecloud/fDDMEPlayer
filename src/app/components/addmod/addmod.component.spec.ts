import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { AddmodComponent } from './addmod.component';

describe('AddmodComponent', () => {
  let component: AddmodComponent;
  let fixture: ComponentFixture<AddmodComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ AddmodComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(AddmodComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
