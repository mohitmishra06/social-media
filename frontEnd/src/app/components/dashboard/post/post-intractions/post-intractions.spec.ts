import { ComponentFixture, TestBed } from '@angular/core/testing';

import { PostIntractions } from './post-intractions';

describe('PostIntractions', () => {
  let component: PostIntractions;
  let fixture: ComponentFixture<PostIntractions>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [PostIntractions]
    })
    .compileComponents();

    fixture = TestBed.createComponent(PostIntractions);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
