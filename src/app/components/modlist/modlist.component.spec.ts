import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { ModlistComponent } from './modlist.component';

describe('ModlistComponent', () => {
  let component: ModlistComponent;
  let fixture: ComponentFixture<ModlistComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ ModlistComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(ModlistComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
