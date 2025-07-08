import { Component, Input } from '@angular/core';

@Component({
  selector: 'app-user-media-card',
  imports: [],
  templateUrl: './user-media-card.html',
  styleUrl: './user-media-card.css'
})
export class UserMediaCard {
  @Input() userId?:string
}
