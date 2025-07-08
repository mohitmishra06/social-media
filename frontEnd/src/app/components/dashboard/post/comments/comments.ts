import { Component } from '@angular/core';
import { FontAwesomeModule } from '@fortawesome/angular-fontawesome';
import { faThumbsUp } from '@fortawesome/free-solid-svg-icons';

@Component({
  selector: 'app-comments',
  imports: [FontAwesomeModule],
  templateUrl: './comments.html',
  styleUrl: './comments.css'
})
export class Comments {
  icon = {faThumbsUp}
}
