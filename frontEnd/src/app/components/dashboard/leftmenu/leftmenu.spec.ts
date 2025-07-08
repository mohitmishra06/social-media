import { ComponentFixture, TestBed } from '@angular/core/testing';

import { Leftmenu } from './leftmenu';

describe('Leftmenu', () => {
  let component: Leftmenu;
  let fixture: ComponentFixture<Leftmenu>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [Leftmenu]
    })
    .compileComponents();

    fixture = TestBed.createComponent(Leftmenu);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
