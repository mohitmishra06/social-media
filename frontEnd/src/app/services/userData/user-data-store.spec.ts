import { TestBed } from '@angular/core/testing';
import { UserDataStore } from './user-data-store';


describe('UserDataStore', () => {
  let service: UserDataStore;

  beforeEach(() => {
    TestBed.configureTestingModule({});
    service = TestBed.inject(UserDataStore);
  });

  it('should be created', () => {
    expect(service).toBeTruthy();
  });
});
