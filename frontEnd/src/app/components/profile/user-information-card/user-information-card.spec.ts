import { ComponentFixture, TestBed } from '@angular/core/testing';

import { UserInformationCard } from './user-information-card';

describe('UserInformationCard', () => {
  let component: UserInformationCard;
  let fixture: ComponentFixture<UserInformationCard>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [UserInformationCard]
    })
    .compileComponents();

    fixture = TestBed.createComponent(UserInformationCard);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
