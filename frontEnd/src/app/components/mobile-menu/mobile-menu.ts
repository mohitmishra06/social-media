import { CommonModule } from '@angular/common';
import { Component } from '@angular/core';

@Component({
  selector: 'app-mobile-menu',
  standalone:true,
  imports: [CommonModule],
  templateUrl: './mobile-menu.html',
  styleUrls: ['./mobile-menu.css']
})
export class MobileMenuComponent {
  // Open/close mobile menu
  isOpen:boolean = false

  // This function works on mobile screen for menu open/close
  isOpenMenu(){
    this.isOpen = (this.isOpen === true) ? false : true;
  }
}
