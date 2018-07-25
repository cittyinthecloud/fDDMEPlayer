import { TestBed, inject } from '@angular/core/testing';

import { ModsService } from './mods.service';

describe('ModsService', () => {
  beforeEach(() => {
    TestBed.configureTestingModule({
      providers: [ModsService]
    });
  });

  it('should be created', inject([ModsService], (service: ModsService) => {
    expect(service).toBeTruthy();
  }));
});
