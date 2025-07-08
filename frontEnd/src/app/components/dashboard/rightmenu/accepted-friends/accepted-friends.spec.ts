import { ComponentFixture, TestBed } from '@angular/core/testing';

import { AcceptedFriends } from './accepted-friends';

describe('AcceptedFriends', () => {
  let component: AcceptedFriends;
  let fixture: ComponentFixture<AcceptedFriends>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [AcceptedFriends]
    })
    .compileComponents();

    fixture = TestBed.createComponent(AcceptedFriends);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
