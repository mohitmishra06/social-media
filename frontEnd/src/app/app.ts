import { Component } from '@angular/core';
import { RouterOutlet } from '@angular/router';
import { ToasterComponent } from "./components/toastr/toastr";

@Component({
  selector: 'app-root',
  standalone:true,
  imports: [RouterOutlet, ToasterComponent, ToasterComponent],
  templateUrl: './app.html',
  styleUrl: './app.css'
})
export class App {
  protected title = 'frontEnd';
}
