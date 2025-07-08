import { Component } from '@angular/core';
import { FontAwesomeModule } from '@fortawesome/angular-fontawesome';
import { faCamera, faImage, faPenFancy, faVideoCamera } from '@fortawesome/free-solid-svg-icons';

@Component({
  selector: 'app-addpost',
  imports: [FontAwesomeModule],
  templateUrl: './addpost.html',
  styleUrl: './addpost.css'
})
export class Addpost {
  icon = { faPenFancy, faVideoCamera, faImage, faCamera }
}
