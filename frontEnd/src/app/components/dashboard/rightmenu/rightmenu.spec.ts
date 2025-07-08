import { ComponentFixture, TestBed } from '@angular/core/testing';

import { Rightmenu } from './rightmenu';

describe('Rightmenu', () => {
  let component: Rightmenu;
  let fixture: ComponentFixture<Rightmenu>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [Rightmenu]
    })
    .compileComponents();

    fixture = TestBed.createComponent(Rightmenu);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
