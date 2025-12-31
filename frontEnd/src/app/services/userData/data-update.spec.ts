import { TestBed } from '@angular/core/testing';

import { DataUpdate } from './data-update';

describe('DataUpdate', () => {
  let service: DataUpdate;

  beforeEach(() => {
    TestBed.configureTestingModule({});
    service = TestBed.inject(DataUpdate);
  });

  it('should be created', () => {
    expect(service).toBeTruthy();
  });
});
