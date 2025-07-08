import { Component } from '@angular/core';
import { faUsers } from '@fortawesome/free-solid-svg-icons';
import { MobileMenuComponent } from '../mobile-menu/mobile-menu';
import { CommonModule } from '@angular/common';

@Component({
  selector: 'app-navbar',
  standalone: true,
  imports: [CommonModule, MobileMenuComponent],
  templateUrl: './navbar.html',
  styleUrls: ['./navbar.css']
})
export default class NavbarComponent {
  icon = { faUsers }
}
