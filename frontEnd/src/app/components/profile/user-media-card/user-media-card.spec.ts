import { ComponentFixture, TestBed } from '@angular/core/testing';

import { UserMediaCard } from './user-media-card';

describe('UserMediaCard', () => {
  let component: UserMediaCard;
  let fixture: ComponentFixture<UserMediaCard>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [UserMediaCard]
    })
    .compileComponents();

    fixture = TestBed.createComponent(UserMediaCard);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
