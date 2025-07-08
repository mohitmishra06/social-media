import { Component } from '@angular/core';
import { FontAwesomeModule } from '@fortawesome/angular-fontawesome';
import { faPlus } from '@fortawesome/free-solid-svg-icons';

@Component({
  selector: 'app-stories',
  imports: [FontAwesomeModule],
  templateUrl: './stories.html',
  styleUrl: './stories.css'
})
export class Stories {
  icon = { faPlus }
}
