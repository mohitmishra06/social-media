import { Component } from '@angular/core';
import NavbarComponent from '../navbar/navbar';
import { RouterOutlet } from '@angular/router';

@Component({
  selector: 'app-layout',
  standalone:true,
  imports: [NavbarComponent, RouterOutlet],
  templateUrl: './layout.html',
  styleUrls: ['./layout.css']
})
export class LayoutComponent {

}
